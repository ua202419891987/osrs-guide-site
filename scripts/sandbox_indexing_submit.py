#!/usr/bin/env python3
"""
Streamlined Google Indexing API submission script for sandbox environment.
- Bypasses socket.create_connection network check (hangs in sandbox)
- Always uses proxy 127.0.0.1:7897
- OAuth token refresh with pickle-based token.json
- Tracks submitted URLs in scripts/submitted_urls.txt
- Handles 429 quota errors gracefully
"""
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# ============================================================
# Config
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
SITEMAP_PATH = PROJECT_DIR / "sitemap.xml"
SUBMITTED_FILE = SCRIPT_DIR / "submitted_urls.txt"
TOKEN_FILE = SCRIPT_DIR / "token.json"
SECRET_FILE = SCRIPT_DIR / "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/indexing']
INDEXING_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
MAX_DAILY_SUBMIT = 200
PROXY_URL = 'http://127.0.0.1:7897'

print("=" * 65)
print("  Google Indexing API — Daily Submission (Sandbox Edition)")
print("=" * 65)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Proxy: {PROXY_URL} (always used in sandbox)")

# ============================================================
# Import libs
# ============================================================
print("\n[INIT] Loading libraries...")
try:
    from google.auth.transport.requests import Request as AuthRequest
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    import requests
    print("  Libraries OK")
except ImportError as e:
    print(f"  MISSING: {e}")
    print("  Run: pip install google-auth-oauthlib google-auth requests")
    sys.exit(1)

# ============================================================
# OAuth credentials
# ============================================================
print("\n[Step 1/5] OAuth Authentication...")
creds = None

if TOKEN_FILE.exists():
    import pickle
    with open(TOKEN_FILE, 'rb') as f:
        creds = pickle.load(f)

if creds and creds.valid:
    print(f"  Token valid (expires: {creds.expiry})")
elif creds and creds.expired and creds.refresh_token:
    print("  Token expired, refreshing...")
    try:
        creds.refresh(AuthRequest())
        print("  Token refreshed OK!")
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(creds, f)
    except Exception as e:
        print(f"  Token refresh FAILED: {e}")
        print("  Need manual OAuth re-authorization (cannot do in sandbox)")
        print("  Please run submit_index_oauth.py locally to re-authorize")
        # Generate report and exit
        report_text = f"OAuth token refresh failed: {e}. Manual re-authorization required."
        print(f"\n{'='*65}")
        print(f"  ABORTED: OAuth token expired/revoked")
        print(f"  Action: Run submit_index_oauth.py locally to re-authorize")
        print(f"{'='*65}")
        sys.exit(1)
else:
    print("  No valid token or refresh token available")
    print("  Cannot perform OAuth in sandbox - need manual authorization")
    sys.exit(1)

print(f"  Auth OK - Bearer token: {creds.token[:20]}...")

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

# Deduplicate
all_urls = list(dict.fromkeys(all_urls))
print(f"  OK — {len(all_urls)} unique URLs in sitemap")

# ============================================================
# Load submitted URLs and compute diff
# ============================================================
print(f"\n[Step 3/5] Comparing with submitted URLs...")
already_submitted = set()
if SUBMITTED_FILE.exists():
    with open(SUBMITTED_FILE, 'r', encoding='utf-8') as f:
        already_submitted = set(line.strip() for line in f if line.strip())
    print(f"  Already submitted: {len(already_submitted)} URLs")

new_urls = [u for u in all_urls if u not in already_submitted]
# Deduplicate
new_urls = list(dict.fromkeys(new_urls))

if len(new_urls) > MAX_DAILY_SUBMIT:
    print(f"  Truncating to {MAX_DAILY_SUBMIT} URLs (daily limit)")
    new_urls = new_urls[:MAX_DAILY_SUBMIT]

print(f"  NEW URLs to submit: {len(new_urls)}")

if len(new_urls) == 0:
    print("\n  All URLs already submitted! Nothing to do.")
    sys.exit(0)

# ============================================================
# Submit URLs
# ============================================================
print(f"\n[Step 4/5] Submitting {len(new_urls)} NEW URLs to Google...")
print("-" * 65)

proxies = {'https': PROXY_URL, 'http': PROXY_URL}

success_count = 0
fail_count = 0
failed_urls = []
quota_exceeded = False
conn_errors = 0

for i, url in enumerate(new_urls, 1):
    short = url.replace('https://osrsguru.com/', '')

    if quota_exceeded:
        print(f"  SKIP (quota): {short[:55]}")
        fail_count += 1
        failed_urls.append(url)
        continue

    print(f"[{i:3d}/{len(new_urls)}] {short[:55]}", end='', flush=True)

    # Refresh token if expired mid-session
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(AuthRequest())
        except:
            pass

    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.token}',
    }

    try:
        resp = requests.post(
            INDEXING_ENDPOINT, data=body, headers=headers,
            proxies=proxies, timeout=30, verify=True,
        )
        if resp.status_code == 200:
            print("  OK")
            success_count += 1
            with open(SUBMITTED_FILE, 'a', encoding='utf-8') as f:
                f.write(url + '\n')
            conn_errors = 0
        elif resp.status_code == 429:
            print("  429 QUOTA EXCEEDED")
            fail_count += 1
            failed_urls.append(url)
            quota_exceeded = True
            print("\n" + "!" * 65)
            print("  DAILY QUOTA (200) EXCEEDED! Stopping.")
            print("!" * 65)
        elif resp.status_code == 403:
            print(f"  403 FORBIDDEN")
            fail_count += 1
            failed_urls.append(url)
        else:
            print(f"  FAIL: HTTP {resp.status_code}")
            fail_count += 1
            failed_urls.append(url)
    except requests.exceptions.Timeout:
        print("  TIMEOUT")
        fail_count += 1
        failed_urls.append(url)
        conn_errors += 1
        if conn_errors >= 5:
            print("  Too many timeouts, stopping.")
            break
    except requests.exceptions.ConnectionError as e:
        err_msg = str(e)[:60]
        print(f"  CONN_ERR: {err_msg}")
        fail_count += 1
        failed_urls.append(url)
        conn_errors += 1
        if conn_errors >= 5:
            print("  Too many connection errors, stopping.")
            break
    except Exception as e:
        print(f"  ERROR: {str(e)[:60]}")
        fail_count += 1
        failed_urls.append(url)

    time.sleep(0.5)

# ============================================================
# Generate report
# ============================================================
print(f"\n[Step 5/5] Generating report...")

# Recalculate remaining
already_after = set()
if SUBMITTED_FILE.exists():
    with open(SUBMITTED_FILE, 'r', encoding='utf-8') as f:
        already_after = set(line.strip() for line in f if line.strip())

remaining = len(all_urls) - len(already_after)

report = {
    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'status': 'QUOTA_EXCEEDED' if quota_exceeded else ('SUCCESS' if success_count > 0 else 'FAILED'),
    'total_sitemap': len(all_urls),
    'already_submitted_before': len(already_submitted),
    'new_found': len(new_urls),
    'submitted_ok': success_count,
    'failed': fail_count,
    'quota_exceeded': quota_exceeded,
    'remaining_after': remaining,
    'failed_urls': failed_urls[:20],  # Limit to first 20 for readability
}

# Save JSON report
REPORT_DIR = PROJECT_DIR / ".workbuddy" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
date_str = datetime.now().strftime('%Y-%m-%d')
json_path = REPORT_DIR / f"indexing-report-{date_str}.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f"  JSON report: {json_path}")

# ============================================================
# Final summary
# ============================================================
print("\n" + "=" * 65)
print(f"  SUBMISSION COMPLETE")
print(f"  Sitemap: {len(all_urls)} | Previously submitted: {len(already_submitted)}")
print(f"  New found: {len(new_urls)} | Success: {success_count} | Failed: {fail_count}")
print(f"  Remaining: {remaining}")
print(f"  Quota exceeded: {'YES' if quota_exceeded else 'NO'}")
print("=" * 65)

# Print the report as structured output for automation
print("\n## AUTOMATION_REPORT ##")
print(json.dumps(report, ensure_ascii=False))
print("## END_REPORT ##")