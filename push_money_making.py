#!/usr/bin/env python3
"""
Money Making 专栏 Google Indexing API 推送脚本
- 复用现有 SA 凭证 scripts/osrsgu-indexin-bdd7bb3b1c82.json
- 自动检测代理，和 daily_indexing_submit.py 保持一致
- 预检查配额、凭证、网络，失败不浪费调用
- 输出报告到 .workbuddy/reports/
"""
import json
import os
import sys
import time
import socket
from datetime import datetime
from pathlib import Path

socket.setdefaulttimeout(30)

# ============================================================
# 配置
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
SERVICE_ACCOUNT_KEY = SCRIPT_DIR / 'scripts' / 'osrsgu-indexin-bdd7bb3b1c82.json'
REPORT_DIR = SCRIPT_DIR / '.workbuddy' / 'reports'
SUBMITTED_FILE = SCRIPT_DIR / 'scripts' / 'submitted_urls.txt'

SCOPES = ['https://www.googleapis.com/auth/indexing']
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
MAX_DAILY_SUBMIT = 200

URLS = [
    'https://osrsguru.com/guides/osrs-afk-money-making-ultimate-guide-2026.html',
    'https://osrsguru.com/guides/osrs-best-money-making-methods-2026.html',
    'https://osrsguru.com/guides/osrs-chambers-of-xeric-loot-profit-guide.html',
    'https://osrsguru.com/guides/osrs-cheap-flipping-methods-new-players.html',
    'https://osrsguru.com/guides/osrs-combat-money-making-non-boss-2026.html',
    'https://osrsguru.com/guides/osrs-daily-weekly-money-routine-2026.html',
    'https://osrsguru.com/guides/osrs-f2p-ironman-money-making-early-game.html',
    'https://osrsguru.com/guides/osrs-f2p-money-making-first-bond-2026.html',
    'https://osrsguru.com/guides/osrs-f2p-money-making-no-stats.html',
    'https://osrsguru.com/guides/osrs-f2p-money-making-ranked-2026.html',
    'https://osrsguru.com/guides/osrs-f2p-to-bond-guide-2026.html',
    'https://osrsguru.com/guides/osrs-first-100k-gp-challenge-2026.html',
    'https://osrsguru.com/guides/osrs-ge-max-cash-guide-2026.html',
    'https://osrsguru.com/guides/osrs-grand-exchange-flipping-guide-2026.html',
    'https://osrsguru.com/guides/osrs-grand-exchange-guide-2026.html',
    'https://osrsguru.com/guides/osrs-how-to-flip-items-profit-mid-game.html',
    'https://osrsguru.com/guides/osrs-how-to-make-money-with-crafting-low-level.html',
    'https://osrsguru.com/guides/osrs-how-to-make-money-with-zulrah.html',
    'https://osrsguru.com/guides/osrs-how-to-rune-spinning-profit-2026.html',
    'https://osrsguru.com/guides/osrs-how-to-spend-gp-wisely-2026.html',
    'https://osrsguru.com/guides/osrs-hunter-money-making-guide-2026.html',
    'https://osrsguru.com/guides/osrs-inflation-gear-prices-2026.html',
    'https://osrsguru.com/guides/osrs-ironman-money-making-f2p-2026.html',
    'https://osrsguru.com/guides/osrs-ironman-p2p-money-making-2026.html',
    'https://osrsguru.com/guides/osrs-killing-green-dragons-money-per-hour.html',
    'https://osrsguru.com/guides/osrs-low-effort-money-making-beginners.html',
    'https://osrsguru.com/guides/osrs-mid-game-money-making-roadmap-2026.html',
    'https://osrsguru.com/guides/osrs-money-making-fishing-2026.html',
    'https://osrsguru.com/guides/osrs-money-making-no-skills-guide-2026.html',
    'https://osrsguru.com/guides/osrs-money-making-tier-list-2026.html',
    'https://osrsguru.com/guides/osrs-money-making-under-1m-investment-2026.html',
    'https://osrsguru.com/guides/osrs-passive-money-making-offline.html',
    'https://osrsguru.com/guides/osrs-revenants-caves-guide-2026.html',
    'https://osrsguru.com/guides/osrs-rune-dragons-money-guide-2026.html',
    'https://osrsguru.com/guides/osrs-sailing-money-making-guide-2026.html',
    'https://osrsguru.com/guides/osrs-skilling-money-post-sailing-2026.html',
    'https://osrsguru.com/guides/osrs-slayer-money-making-guide-2026.html',
    'https://osrsguru.com/guides/osrs-sub-70-combat-bossing-guide-2026.html',
    'https://osrsguru.com/guides/osrs-vorkath-money-making-guide-2026.html',
    'https://osrsguru.com/guides/osrs-wilderness-money-making-2026.html',
    'https://osrsguru.com/guides/osrs-wintertodt-money-making-per-hour.html',
    'https://osrsguru.com/guides/osrs-zero-req-moneymaker-2026.html',
    'https://osrsguru.com/guides/osrs-zulrah-money-making-guide-2026.html',
]

# ============================================================
# 导入依赖
# ============================================================
print('=' * 65)
print('  Money Making 专栏 — Google Indexing API 推送')
print('=' * 65)
print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'总 URL: {len(URLS)}')

print('\n[INIT] 检查依赖...')
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request as GoogleRequest
    import requests
    print('  ✅ google-auth / requests 已安装')
except ImportError as e:
    print(f'  ❌ 缺少依赖: {e}')
    print('  请运行: pip install google-auth requests')
    sys.exit(1)

# ============================================================
# 凭证预检查
# ============================================================
print('\n[Step 1/5] 检查服务账号凭证...')
if not SERVICE_ACCOUNT_KEY.exists():
    print(f'  ❌ 凭证文件不存在: {SERVICE_ACCOUNT_KEY}')
    print('  请确认 scripts/osrsgu-indexin-bdd7bb3b1c82.json 存在')
    sys.exit(1)
print(f'  ✅ 凭证文件存在: {SERVICE_ACCOUNT_KEY.name}')

# ============================================================
# 网络和代理检测
# ============================================================
proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or 'http://127.0.0.1:7897'
print(f'\n[Step 2/5] 网络检测 (代理: {proxy_url})...')

use_proxy = True
try:
    s = socket.create_connection(('www.google.com', 443), timeout=8)
    s.close()
    print('  ✅ 可直连 google.com:443')
    use_proxy = False
except Exception as e:
    print(f'  ℹ️  直连失败 ({str(e)[:50]}), 使用代理')

proxies = {}
if use_proxy and proxy_url:
    proxies = {'https': proxy_url, 'http': proxy_url}

# ============================================================
# 认证
# ============================================================
print('\n[Step 3/5] 获取 access token...')
try:
    credentials = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_KEY), scopes=SCOPES)
    gr = GoogleRequest()
    credentials.refresh(gr)
    access_token = credentials.token
    print(f'  ✅ 认证成功: {credentials.service_account_email}')
except Exception as e:
    print(f'  ❌ 认证失败: {e}')
    sys.exit(1)

# ============================================================
# 已提交 URL 过滤
# ============================================================
print('\n[Step 4/5] 过滤已提交 URL...')
already_submitted = set()
if SUBMITTED_FILE.exists():
    with open(SUBMITTED_FILE, 'r', encoding='utf-8') as f:
        already_submitted = set(line.strip() for line in f if line.strip())
    print(f'  历史已提交: {len(already_submitted)} 条')

urls_to_submit = [u for u in URLS if u not in already_submitted]
print(f'  本次待提交: {len(urls_to_submit)} 条')

if not urls_to_submit:
    print('\n  ✅ 所有 URL 都已提交过，无需重复推送。')
    sys.exit(0)

# ============================================================
# 提交 URL
# ============================================================
print('\n[Step 5/5] 提交到 Google Indexing API...')
print('-' * 65)

def submit_one(url):
    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    try:
        resp = requests.post(
            API_URL, data=body, headers=headers,
            proxies=proxies if proxies else None, timeout=30, verify=True,
        )
        if resp.status_code == 200:
            return True, 'OK', False
        elif resp.status_code == 429:
            return False, 'HTTP 429 配额已用完', True
        elif resp.status_code == 403:
            return False, f'HTTP 403 SA 无 Search Console 权限: {credentials.service_account_email}', False
        else:
            return False, f'HTTP {resp.status_code}: {resp.text[:80]}', False
    except requests.exceptions.Timeout:
        return False, 'TIMEOUT (>30s)', False
    except requests.exceptions.ConnectionError as e:
        return False, f'CONNECTION ERROR: {str(e)[:80]}', False
    except Exception as e:
        return False, str(e)[:120], False

success = 0
failed = 0
failed_urls = []
quota_exceeded = False

for i, url in enumerate(urls_to_submit[:MAX_DAILY_SUBMIT], 1):
    if quota_exceeded:
        print(f'  SKIP: {url}')
        failed_urls.append(url)
        failed += 1
        continue

    short = url.replace('https://osrsguru.com/', '')
    print(f'[{i:2d}/{len(urls_to_submit)}] {short[:55]}', end='', flush=True)
    ok, result, is_429 = submit_one(url)

    if ok:
        print('  ✅ OK')
        success += 1
        with open(SUBMITTED_FILE, 'a', encoding='utf-8') as f:
            f.write(url + '\n')
    else:
        print(f'  ❌ {result}')
        failed += 1
        failed_urls.append(url)
        if is_429:
            quota_exceeded = True
            print('\n' + '!' * 65)
            print('  每日配额 (200) 已用完，停止后续提交')
            print('!' * 65)

    time.sleep(0.5)

# ============================================================
# 报告
# ============================================================
REPORT_DIR.mkdir(parents=True, exist_ok=True)
date_str = datetime.now().strftime('%Y-%m-%d')

report = {
    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'source': 'money_making_col',
    'total': len(URLS),
    'already_submitted': len(already_submitted),
    'to_submit': len(urls_to_submit),
    'success': success,
    'failed': failed,
    'quota_exceeded': quota_exceeded,
    'failed_urls': failed_urls,
}

with open(REPORT_DIR / f'money-making-index-{date_str}.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print('\n' + '=' * 65)
print(f'  完成')
print(f'  总数: {len(URLS)} | 已提交过: {len(already_submitted)} | 本次提交: {len(urls_to_submit)}')
print(f'  ✅ 成功: {success} | ❌ 失败: {failed}')
print(f'  报告: .workbuddy/reports/money-making-index-{date_str}.json')
print('=' * 65)

if failed > 0 and not quota_exceeded:
    sys.exit(1)
