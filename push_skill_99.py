#!/usr/bin/env python3
"""
Skill/1-99 专栏 Google Indexing API 推送脚本
覆盖 Phase 3 标准化的 42 篇文章
"""
import json
import os
import sys
import time
import socket
from datetime import datetime
from pathlib import Path

socket.setdefaulttimeout(30)

SCRIPT_DIR = Path(__file__).resolve().parent
SERVICE_ACCOUNT_KEY = SCRIPT_DIR / 'scripts' / 'osrsgu-indexin-bdd7bb3b1c82.json'
REPORT_DIR = SCRIPT_DIR / '.workbuddy' / 'reports'
SUBMITTED_FILE = SCRIPT_DIR / 'scripts' / 'submitted_urls.txt'

SCOPES = ['https://www.googleapis.com/auth/indexing']
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
MAX_DAILY_SUBMIT = 200

URLS = [
    'https://osrsguru.com/guides/osrs-1-99-crafting-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-hitpoints-training-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-hunter-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-magic-training-cheap-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-thieving-guide-ironman.html',
    'https://osrsguru.com/guides/osrs-agility-training-guide-2026.html',
    'https://osrsguru.com/guides/osrs-blast-furnace-smithing-guide-2026.html',
    'https://osrsguru.com/guides/osrs-cheapest-99-runecrafting-2026.html',
    'https://osrsguru.com/guides/osrs-construction-1-99-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-hitpoints-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-prayer-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-prayer-guide-all-methods-2026.html',
    'https://osrsguru.com/guides/osrs-ironman-1-99-smithing-guide.html',
    'https://osrsguru.com/guides/osrs-low-cost-1-99-herblore-guide.html',
    'https://osrsguru.com/guides/osrs-1-99-hunter-guide-afk-method.html',
    'https://osrsguru.com/guides/osrs-fastest-1-99-crafting-guide-2026.html',
    'https://osrsguru.com/guides/osrs-fastest-99-attack-strength-defence.html',
    'https://osrsguru.com/guides/osrs-fastest-99-cooking-f2p.html',
    'https://osrsguru.com/guides/osrs-fastest-hunter-training-2026.html',
    'https://osrsguru.com/guides/osrs-fastest-leveling-guide-2026.html',
    'https://osrsguru.com/guides/osrs-how-to-get-99-agility-fast-2026.html',
    'https://osrsguru.com/guides/osrs-how-to-get-99-fishing-afk-method.html',
    'https://osrsguru.com/guides/osrs-how-to-train-prayer-cheap-f2p.html',
    'https://osrsguru.com/guides/osrs-hunter-training-guide-2026.html',
    'https://osrsguru.com/guides/osrs-mahogany-homes-construction-guide-2026.html',
    'https://osrsguru.com/guides/osrs-maxing-99-order-guide-2026.html',
    'https://osrsguru.com/guides/osrs-optimal-leveling-guide-2026.html',
    'https://osrsguru.com/guides/osrs-range-training-1-99-guide-2026.html',
    'https://osrsguru.com/guides/osrs-affordable-leveling-guide-2026.html',
    'https://osrsguru.com/guides/osrs-bond-farming-free-membership-2026.html',
    'https://osrsguru.com/guides/osrs-bond-farming-strategy-2026.html',
    'https://osrsguru.com/guides/osrs-complete-skill-training-guide-2026.html',
    'https://osrsguru.com/guides/osrs-leveling-milestones-guide-2026.html',
    'https://osrsguru.com/guides/osrs-sailing-1-99-guide-2026.html',
    'https://osrsguru.com/guides/osrs-sailing-afk-training-guide-2026.html',
    'https://osrsguru.com/guides/osrs-sailing-training-guide-2026.html',
    'https://osrsguru.com/guides/osrs-skill-training-after-sweep-up-2026.html',
    'https://osrsguru.com/guides/osrs-skill-training-endgame-guide-2026.html',
    'https://osrsguru.com/guides/osrs-skill-training-max-account-2026.html',
    'https://osrsguru.com/guides/osrs-skill-training-mid-game-guide-2026.html',
    'https://osrsguru.com/guides/osrs-skill-training-mid-game-optimization-2026.html',
    'https://osrsguru.com/guides/osrs-training-guide-complete-2026.html',
]

print('=' * 65)
print('  Skill/1-99 专栏 — Google Indexing API 推送')
print('=' * 65)
print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'总 URL: {len(URLS)}')

print('\n[INIT] 检查依赖...')
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request as GoogleRequest
    import requests
    print('  OK google-auth / requests')
except ImportError as e:
    print(f'  FAIL: {e}')
    sys.exit(1)

print('\n[Step 1/5] 检查服务账号凭证...')
if not SERVICE_ACCOUNT_KEY.exists():
    print(f'  FAIL: {SERVICE_ACCOUNT_KEY}')
    sys.exit(1)
print(f'  OK {SERVICE_ACCOUNT_KEY.name}')

proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or 'http://127.0.0.1:7897'
print(f'\n[Step 2/5] 网络检测 (代理: {proxy_url})...')
use_proxy = True
try:
    s = socket.create_connection(('www.google.com', 443), timeout=8)
    s.close()
    print('  OK 直连')
    use_proxy = False
except Exception as e:
    print(f'  使用代理 ({str(e)[:50]})')
proxies = {'https': proxy_url, 'http': proxy_url} if use_proxy and proxy_url else {}

print('\n[Step 3/5] 获取 access token...')
try:
    credentials = service_account.Credentials.from_service_account_file(str(SERVICE_ACCOUNT_KEY), scopes=SCOPES)
    credentials.refresh(GoogleRequest())
    access_token = credentials.token
    print(f'  OK {credentials.service_account_email}')
except Exception as e:
    print(f'  FAIL: {e}')
    sys.exit(1)

print('\n[Step 4/5] 过滤已提交 URL...')
already_submitted = set()
if SUBMITTED_FILE.exists():
    with open(SUBMITTED_FILE, 'r', encoding='utf-8') as f:
        already_submitted = set(line.strip() for line in f if line.strip())
    print(f'  历史已提交: {len(already_submitted)}')
urls_to_submit = [u for u in URLS if u not in already_submitted]
print(f'  本次待提交: {len(urls_to_submit)}')
if not urls_to_submit:
    print('\n  全部已提交过')
    sys.exit(0)

print('\n[Step 5/5] 提交到 Google Indexing API...')
print('-' * 65)

def submit_one(url):
    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    try:
        resp = requests.post(API_URL, data=body, headers=headers, proxies=proxies if proxies else None, timeout=30, verify=True)
        if resp.status_code == 200:
            return True, 'OK', False
        elif resp.status_code == 429:
            return False, 'HTTP 429 配额已用完', True
        elif resp.status_code == 403:
            return False, f'HTTP 403 SA 无权限: {credentials.service_account_email}', False
        else:
            return False, f'HTTP {resp.status_code}: {resp.text[:80]}', False
    except Exception as e:
        return False, str(e)[:120], False

success = failed = 0
failed_urls = []
quota_exceeded = False
for i, url in enumerate(urls_to_submit[:MAX_DAILY_SUBMIT], 1):
    if quota_exceeded:
        print(f'  SKIP: {url}')
        failed_urls.append(url); failed += 1
        continue
    short = url.replace('https://osrsguru.com/', '')
    print(f'[{i:2d}/{len(urls_to_submit)}] {short[:55]}', end='', flush=True)
    ok, result, is_429 = submit_one(url)
    if ok:
        print('  OK')
        success += 1
        with open(SUBMITTED_FILE, 'a', encoding='utf-8') as f:
            f.write(url + '\n')
    else:
        print(f'  FAIL: {result}')
        failed += 1; failed_urls.append(url)
        if is_429:
            quota_exceeded = True
            print('\n' + '!' * 65 + '\n  每日配额 (200) 已用完\n' + '!' * 65)
    time.sleep(0.5)

REPORT_DIR.mkdir(parents=True, exist_ok=True)
date_str = datetime.now().strftime('%Y-%m-%d')
report = {'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'source': 'skill_99_col', 'total': len(URLS), 'already_submitted': len(already_submitted), 'to_submit': len(urls_to_submit), 'success': success, 'failed': failed, 'quota_exceeded': quota_exceeded, 'failed_urls': failed_urls}
with open(REPORT_DIR / f'skill-99-index-{date_str}.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print('\n' + '=' * 65)
print(f'  完成: 总数 {len(URLS)} | 已提交过 {len(already_submitted)} | 本次 {len(urls_to_submit)}')
print(f'  OK: {success} | FAIL: {failed}')
print(f'  报告: .workbuddy/reports/skill-99-index-{date_str}.json')
print('=' * 65)
