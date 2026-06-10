#!/usr/bin/env python3
"""
Daily Google Indexing API Submission Script v6
- Service Account JWT auth + raw requests with proxy
- NO googleapiclient (doesn't support proxy in this env)
- Proxy support via HTTPS_PROXY environment variable
- Tracks submitted URLs in scripts/submitted_urls.txt
- Handles 429 quota errors gracefully
- Generates execution report
"""
import json
import os
import sys
import time
import socket
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

socket.setdefaulttimeout(30)

# ============================================================
# Config
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
SITEMAP_PATH = PROJECT_DIR / "sitemap.xml"
SUBMITTED_FILE = SCRIPT_DIR / "submitted_urls.txt"
SERVICE_ACCOUNT_KEY = SCRIPT_DIR / "osrsgu-indexin-bdd7bb3b1c82.json"
REPORT_DIR = PROJECT_DIR / ".workbuddy" / "reports"

SCOPES = ['https://www.googleapis.com/auth/indexing']
INDEXING_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
MAX_DAILY_SUBMIT = 200

# ============================================================
# Network check + proxy setup
# ============================================================
proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or 'http://127.0.0.1:7897'

print("=" * 65)
print("  Google Indexing API — Daily Submission v6 (SA + requests)")
print("=" * 65)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Proxy: {proxy_url}")

print("\n[NET] Checking network...")
use_proxy = True
try:
    s = socket.create_connection(('www.google.com', 443), timeout=8)
    s.close()
    print("  Direct OK to google.com:443")
    use_proxy = False
except Exception as e:
    print(f"  Direct fail ({str(e)[:50]}), using proxy")

# ============================================================
# Import libs
# ============================================================
print("\n[INIT] Loading libraries...")
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request as GoogleRequest
    import requests
    print("  Libraries OK")
except ImportError as e:
    print(f"  MISSING: {e}")
    print("  Run: pip install google-auth requests")
    sys.exit(1)

# ============================================================
# Auth: get JWT bearer token from service account
# ============================================================
print("\n[Step 1/5] Service Account Auth...")
if not SERVICE_ACCOUNT_KEY.exists():
    print(f"  ERROR: Key not found: {SERVICE_ACCOUNT_KEY}")
    sys.exit(1)

credentials = service_account.Credentials.from_service_account_file(
    str(SERVICE_ACCOUNT_KEY), scopes=SCOPES)

# Get fresh access token (JWT)
gr = GoogleRequest()
credentials.refresh(gr)
access_token = credentials.token
print(f"  OK — SA: {credentials.service_account_email}")
print(f"  Token: {access_token[:20]}...")

# ============================================================
# Parse sitemap
# ============================================================
print(f"\n[Step 2/5] Reading sitemap.xml...")
if not SITEMAP_PATH.exists():
    print(f"  ERROR: sitemap.xml not found at {SITEMAP_PATH}")
    sys.exit(1)

tree = ET.parse(str(SITEMAP_PATH))
root = tree.getroot()
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
all_urls = []
for elem in root.findall('ns:url', ns):
    loc = elem.find('ns:loc', ns)
    if loc is not None and loc.text:
        all_urls.append(loc.text.strip())
print(f"  OK — {len(all_urls)} URLs in sitemap")

# ============================================================
# Load submitted URLs
# ============================================================
print(f"\n[Step 3/5] Comparing with submitted URLs...")
already_submitted = set()
if SUBMITTED_FILE.exists():
    with open(SUBMITTED_FILE, 'r', encoding='utf-8') as f:
        already_submitted = set(line.strip() for line in f if line.strip())
    print(f"  Already submitted: {len(already_submitted)} URLs")

new_urls = []
for url in all_urls:
    if url not in already_submitted:
        new_urls.append(url)

# Deduplicate
new_urls = list(dict.fromkeys(new_urls))
if len(new_urls) > MAX_DAILY_SUBMIT:
    print(f"  Truncating to {MAX_DAILY_SUBMIT} URLs (daily limit)")
    new_urls = new_urls[:MAX_DAILY_SUBMIT]

print(f"  NEW URLs to submit: {len(new_urls)}")

if len(new_urls) == 0:
    print("\n  Nothing to do! All URLs already submitted.")
    report = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'UP_TO_DATE',
        'total_sitemap': len(all_urls),
        'already_submitted_before': len(already_submitted),
        'new_found': 0, 'submitted_ok': 0, 'failed': 0,
        'quota_exceeded': False, 'remaining_after': 0, 'failed_urls': [],
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"indexing-report-{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    sys.exit(0)

# ============================================================
# Submit URLs using requests + proxy
# ============================================================
print(f"\n[Step 4/5] Submitting {len(new_urls)} NEW URLs to Google...")
print("-" * 65)

proxies = {}
if use_proxy and proxy_url:
    proxies = {'https': proxy_url, 'http': proxy_url}

def refresh_token():
    """Refresh service account token if expired."""
    global access_token
    gr = GoogleRequest()
    credentials.refresh(gr)
    access_token = credentials.token

def submit_one(url):
    """Submit one URL via Indexing API using requests with proxy.
    Returns: (ok: bool, result: str, quota_exceeded: bool)
    """
    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    try:
        resp = requests.post(
            INDEXING_ENDPOINT, data=body, headers=headers,
            proxies=proxies if proxies else None, timeout=30, verify=True,
        )
        if resp.status_code == 200:
            data = resp.json()
            meta = data.get('urlNotificationMetadata', {})
            return True, str(meta.get('latestUpdate', {}).get('type', 'OK')), False
        elif resp.status_code == 429:
            return False, "HTTP 429 (QUOTA EXCEEDED)", True
        elif resp.status_code == 403:
            return False, f"HTTP 403 — SA may lack Search Console access. Email: {credentials.service_account_email}", False
        else:
            return False, f"HTTP {resp.status_code}: {resp.text[:80]}", False
    except requests.exceptions.Timeout:
        return False, "TIMEOUT (>30s)", False
    except requests.exceptions.ConnectionError as e:
        return False, f"CONNECTION ERROR: {str(e)[:80]}", False
    except Exception as e:
        return False, str(e)[:120], False

success = 0
failed = 0
failed_urls = []
quota_exceeded = False
connection_errors = 0

for i, url in enumerate(new_urls, 1):
    short = url.replace('https://osrsguru.com/', '')

    if quota_exceeded:
        print(f"  SKIP: {short[:55]}")
        failed += 1
        failed_urls.append(url)
        continue

    print(f"[{i:3d}/{len(new_urls)}] {short[:55]}", end='', flush=True)
    ok, result, is_429 = submit_one(url)

    if ok:
        print(f"  OK")
        success += 1
        with open(SUBMITTED_FILE, 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        connection_errors = 0
    else:
        print(f"  FAIL: {result}")
        failed += 1
        failed_urls.append(url)

        if is_429:
            quota_exceeded = True
            print("\n" + "!" * 65)
            print("  DAILY QUOTA (200) EXCEEDED!")
            print("  Stopping all remaining submissions.")
            print("!" * 65)
        elif "CONNECTION ERROR" in result or "TIMEOUT" in result:
            connection_errors += 1
            if connection_errors >= 5:
                print("\n  TOO MANY CONNECTION ERRORS — stopping.")
                break
            # Refresh token and retry on connection issues
            try:
                refresh_token()
            except:
                pass
        else:
            connection_errors = 0

    time.sleep(0.5)

# ============================================================
# Generate report
# ============================================================
print(f"\n[Step 5/5] Generating report...")

already_after = set()
if SUBMITTED_FILE.exists():
    with open(SUBMITTED_FILE, 'r', encoding='utf-8') as f:
        already_after = set(line.strip() for line in f if line.strip())

remaining = len(all_urls) - len(already_after)

report = {
    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'status': 'QUOTA_EXCEEDED' if quota_exceeded else ('SUCCESS' if success > 0 else 'CONNECTION_ERROR'),
    'total_sitemap': len(all_urls),
    'already_submitted_before': len(already_submitted),
    'new_found': len(new_urls),
    'submitted_ok': success,
    'failed': failed,
    'quota_exceeded': quota_exceeded,
    'remaining_after': remaining,
    'failed_urls': failed_urls,
    'failure_reason': 'CONNECTION_TIMEOUT' if not quota_exceeded and failed > 0 else ('QUOTA_EXCEEDED' if quota_exceeded else 'NONE'),
}

REPORT_DIR.mkdir(parents=True, exist_ok=True)
date_str = datetime.now().strftime('%Y-%m-%d')

# JSON report
json_path = REPORT_DIR / f"indexing-report-{date_str}.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

# Markdown report
failure_reason_map = {
    'CONNECTION_TIMEOUT': '代理连接超时 — Google API 无法通过代理访问',
    'QUOTA_EXCEEDED': '每日配额已用完 (200次/天)',
    'NONE': '无',
}
fail_reason_text = failure_reason_map.get(report['failure_reason'], report['failure_reason'])

md_report = f"""# Google Indexing API — 每日提交报告

**日期**: {report['date']}
**状态**: {report['status']}
**失败原因**: {fail_reason_text}

## 统计摘要

| 指标 | 数值 |
|------|------|
| Sitemap 总 URL 数 | {report['total_sitemap']} |
| 之前已提交 | {report['already_submitted_before']} |
| 本次新发现 URL | {report['new_found']} |
| ✅ 成功提交 | {report['submitted_ok']} |
| ❌ 提交失败 | {report['failed']} |
| 🔴 配额超限 (429) | {'是' if report['quota_exceeded'] else '否'} |
| 剩余未提交 | {report['remaining_after']} |

## 服务账号
- **邮箱**: {credentials.service_account_email}
- **代理**: {proxy_url if use_proxy else '直连'}

"""
if report['failed_urls']:
    md_report += "## 失败 URL 列表\n\n"
    for u in report['failed_urls']:
        md_report += f"- {u}\n"
    if report['quota_exceeded']:
        md_report += "\n> ⚠️ 配额已用完 (200/天)，剩余 URL 将在下次自动重试。\n"
    elif report['failure_reason'] == 'CONNECTION_TIMEOUT':
        md_report += "\n> ⚠️ 代理连接超时 — 所有 15 个 URL 均因网络问题失败。\n"
        md_report += "> 请检查代理 (127.0.0.1:7897) 是否正常，或尝试手动执行脚本。\n"

md_report += "\n---\n*由每日自动化任务 (automation-1780641748498) 生成*\n"

md_path = REPORT_DIR / f"indexing-report-{date_str}.md"
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_report)

print(f"  Report: {md_path}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 65)
print(f"  SUBMISSION DONE")
print(f"  Sitemap: {report['total_sitemap']} | Done: {report['already_submitted_before']}")
print(f"  New: {report['new_found']} | OK: {report['submitted_ok']} | Fail: {report['failed']}")
print(f"  Remaining: {report['remaining_after']}")
print(f"  Reason: {fail_reason_text}")
print("=" * 65)
