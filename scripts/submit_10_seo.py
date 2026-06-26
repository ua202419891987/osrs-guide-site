#!/usr/bin/env python3
"""提交最后10篇SEO专项文章到Google Indexing API"""
import os, sys, json, time, socket, requests

URLS = [
    "https://osrsguru.com/guides/osrs-viggora-guide-2026.html",
    "https://osrsguru.com/guides/osrs-viggora-chainmace-guide-2026.html",
    "https://osrsguru.com/guides/osrs-curse-of-the-empty-lord-quest-2026.html",
    "https://osrsguru.com/guides/osrs-training-guide-complete-2026.html",
    "https://osrsguru.com/guides/osrs-fastest-leveling-guide-2026.html",
    "https://osrsguru.com/guides/osrs-leveling-milestones-guide-2026.html",
    "https://osrsguru.com/guides/osrs-f2p-leveling-guide-2026.html",
    "https://osrsguru.com/guides/osrs-1-99-hunter-guide-2026.html",
    "https://osrsguru.com/guides/osrs-fastest-hunter-training-2026.html",
    "https://osrsguru.com/guides/osrs-best-money-making-methods-2026.html",
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- 1. 检测代理 ----
def find_proxy():
    for port in [7897, 7890, 10809, 10808]:
        try:
            s = socket.create_connection(('127.0.0.1', port), timeout=2)
            s.close()
            proxies = {'https': f'http://127.0.0.1:{port}'}
            r = requests.get('https://www.googleapis.com/', proxies=proxies, timeout=5)
            if r.status_code < 500:
                print(f"[OK] 代理找到: 127.0.0.1:{port}")
                return proxies
        except:
            pass
    print("[FAIL] 未检测到可用代理，请先打开代理客户端")
    sys.exit(1)

proxies = find_proxy()

# ---- 2. Token ----
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.json')
CLIENT_SECRET_PATH = os.path.join(SCRIPT_DIR, 'client_secret.json')

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/indexing']

creds = None
if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            print("[OK] Token 已刷新")
        except:
            print("[INFO] Token刷新失败，打开浏览器重新授权...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
    else:
        print("[INFO] 打开浏览器授权...")
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, 'w') as f:
        f.write(creds.to_json())
    print("[OK] Token 已保存")

# ---- 3. 提交 ----
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
ok = fail = skip = 0

print(f"\n{'='*60}")
print(f"开始提交 {len(URLS)} 篇 SEO 专项文章")
print(f"{'='*60}\n")

for i, url in enumerate(URLS, 1):
    body = {'url': url, 'type': 'URL_UPDATED'}
    try:
        resp = requests.post(API_URL, json=body, headers={
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }, proxies=proxies, timeout=15)

        if resp.status_code == 200:
            print(f"[{i:2d}/{len(URLS)}] ✅ {url.split('/')[-1]}")
            ok += 1
        elif resp.status_code == 429:
            print(f"[{i:2d}/{len(URLS)}] 🚨 429 配额耗尽，已成功{ok}篇")
            break
        else:
            print(f"[{i:2d}/{len(URLS)}] ⏭ {resp.status_code} — {url.split('/')[-1]}")
            fail += 1
    except Exception as e:
        print(f"[{i:2d}/{len(URLS)}] ❌ 网络错误 — {url.split('/')[-1]}: {str(e)[:40]}")
        fail += 1

    time.sleep(0.6)

print(f"\n{'='*60}")
print(f"结果: ✅ {ok} | ⏭ {fail} | 📝 总计 {ok+fail}/{len(URLS)}")
print(f"{'='*60}")
