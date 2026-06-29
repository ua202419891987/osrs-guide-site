#!/usr/bin/env python3
"""提交 Crimson Desert 新文章到 Google Indexing API
   24 篇全新文章（第三批，2026-06-29）
"""
import os, sys, json, time, socket, requests

# ---- 24 篇全新文章（2026-06-29 第三批） ----
URLS = [
    # === NEW 24 articles (June 29 batch) ===
    # 武器强化系统
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-weapon-enhancement-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-enhancement-materials-guide-2026.html",
    # 深渊圣所地牢
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-abyss-sanctum-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-sanctum-rewards-guide-2026.html",
    # 中期装备
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-mid-game-gear-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-mid-gear-locations-guide-2026.html",
    # 通关后内容
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-post-game-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-post-game-secrets-guide-2026.html",
    # Kliff角色
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-kliff-build-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-kliff-combos-guide-2026.html",
    # Oongka角色
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-oongka-build-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-oongka-dual-wield-guide-2026.html",
    # Damiane角色
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-damiane-build-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-damiane-shield-guide-2026.html",
    # 转换率系统
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-conversion-mechanics-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-conversion-farming-guide-2026.html",
    # 成就系统
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-achievements-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-achievement-speedrun-guide-2026.html",
    # 深渊核心系统
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-abyss-core-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-core-farming-guide-2026.html",
    # 卡牌游戏
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-card-game-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-card-collection-guide-2026.html",
    # Kuku Pot系统
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-kuku-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-kuku-evolution-guide-2026.html",
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
ok = fail = 0

print(f"\n{'='*70}")
print(f"  Crimson Desert — 提交 {len(URLS)} 篇（第三批 2026-06-29）")
print(f"  (24 篇全新攻略文章)")
print(f"{'='*70}\n")

for i, url in enumerate(URLS, 1):
    body = {'url': url, 'type': 'URL_UPDATED'}
    try:
        resp = requests.post(API_URL, json=body, headers={
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }, proxies=proxies, timeout=15)

        if resp.status_code == 200:
            short = url.split('/')[-1].replace('crimson-desert-', '').replace('-guide-2026', '').replace('.html', '')
            print(f"[{i:2d}/{len(URLS)}] ✅ {short}")
            ok += 1
        elif resp.status_code == 429:
            print(f"[{i:2d}/{len(URLS)}] 🚨 429 配额耗尽！已成功 {ok} 篇，剩余 {len(URLS)-ok} 篇待提交")
            break
        elif resp.status_code == 403:
            print(f"[{i:2d}/{len(URLS)}] ⏭ 403（可能已索引）— {url.split('/')[-1][:40]}")
        else:
            print(f"[{i:2d}/{len(URLS)}] ⏭ {resp.status_code} — {url.split('/')[-1][:40]}")
            fail += 1
    except Exception as e:
        print(f"[{i:2d}/{len(URLS)}] ❌ 网络错误 — {url.split('/')[-1][:40]}: {str(e)[:40]}")
        fail += 1

    time.sleep(0.6)

print(f"\n{'='*70}")
print(f"  结果: ✅ {ok} | ⏭ 跳过/失败 {fail} | 📝 总计 {ok+fail}/{len(URLS)}")
print(f"{'='*70}")
