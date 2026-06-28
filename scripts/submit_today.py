#!/usr/bin/env python
"""submit_today.py — 一键提交今天修改的45篇到Google索引"""
import os, json, time, socket, webbrowser, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

URLS = [
  "https://osrsguru.com/guides/osrs-best-updates-2026-ranked.html",
  "https://osrsguru.com/guides/osrs-bond-farming-strategy-2026.html",
  "https://osrsguru.com/guides/osrs-coming-back-2026-guide-2026.html",
  "https://osrsguru.com/guides/osrs-crystal-extractor-guide-2026.html",
  "https://osrsguru.com/guides/osrs-f2p-to-bond-guide-2026.html",
  "https://osrsguru.com/guides/osrs-frustration-solutions-guide-2026.html",
  "https://osrsguru.com/guides/osrs-gear-before-price-hike-2026.html",
  "https://osrsguru.com/guides/osrs-mid-game-breakthrough-guide-2026.html",
  "https://osrsguru.com/guides/osrs-mid-year-meta-shift-2026.html",
  "https://osrsguru.com/guides/osrs-money-making-no-skills-guide-2026.html",
  "https://osrsguru.com/guides/osrs-returning-player-guide-2026.html",
  "https://osrsguru.com/guides/osrs-sailing-best-quest-order-after-sailing-2026.html",
  "https://osrsguru.com/guides/osrs-sailing-money-making-guide-2026.html",
  "https://osrsguru.com/guides/osrs-sailing-phase-2-prep-guide-2026.html",
  "https://osrsguru.com/guides/osrs-sailing-training-guide-2026.html",
  "https://osrsguru.com/guides/osrs-stuck-progression-guide-2026.html",
  "https://osrsguru.com/guides/osrs-summer-sweep-up-2026-guide.html",
  "https://osrsguru.com/guides/osrs-zero-req-moneymaker-2026.html",
  "https://osrsguru.com/guides/vault-of-ralos-raid-guide-2026.html",
  "https://osrsguru.com/guides/mid-game-money-making-2026.html",
  "https://osrsguru.com/guides/osrs-afk-money-making-ultimate-guide-2026.html",
  "https://osrsguru.com/guides/osrs-best-money-making-methods-2026.html",
  "https://osrsguru.com/guides/osrs-bond-farming-free-membership-2026.html",
  "https://osrsguru.com/guides/osrs-boss-profit-comparison-2026.html",
  "https://osrsguru.com/guides/osrs-boss-profit-tier-list-2026.html",
  "https://osrsguru.com/guides/osrs-daily-weekly-money-routine-2026.html",
  "https://osrsguru.com/guides/osrs-f2p-ironman-money-making-early-game.html",
  "https://osrsguru.com/guides/osrs-how-to-beat-zulrah-beginners-rotation.html",
  "https://osrsguru.com/guides/osrs-how-to-make-money-with-zulrah.html",
  "https://osrsguru.com/guides/osrs-hunter-money-making-guide-2026.html",
  "https://osrsguru.com/guides/osrs-ironman-money-making-f2p-2026.html",
  "https://osrsguru.com/guides/osrs-mid-game-money-making-roadmap-2026.html",
  "https://osrsguru.com/guides/osrs-money-making-tier-list-2026.html",
  "https://osrsguru.com/guides/osrs-slayer-money-making-guide-2026.html",
  "https://osrsguru.com/guides/combat-achievements-guide-2026.html",
  "https://osrsguru.com/guides/osrs-1-99-hitpoints-training-guide-2026.html",
  "https://osrsguru.com/guides/osrs-1-99-prayer-guide-all-methods-2026.html",
  "https://osrsguru.com/guides/osrs-affordable-leveling-guide-2026.html",
  "https://osrsguru.com/guides/osrs-efficient-training-routes-beginners-2026.html",
  "https://osrsguru.com/guides/osrs-fastest-1-99-crafting-guide-2026.html",
  "https://osrsguru.com/guides/osrs-hunter-training-guide-2026.html",
  "https://osrsguru.com/guides/osrs-optimal-leveling-guide-2026.html",
  "https://osrsguru.com/guides/osrs-training-guide-complete-2026.html",
]

BASE = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE, 'token.json')
CLIENT_SECRET_PATH = os.path.join(BASE, 'client_secret.json')

# 自动找代理
for port in [7897, 7890, 10808]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    if s.connect_ex(('127.0.0.1', port)) == 0:
        os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
        os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
        print(f'[OK] Proxy: 127.0.0.1:{port}')
        break
    s.close()

# OAuth登录
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ['https://www.googleapis.com/auth/indexing']

creds = None
if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    creds = flow.run_local_server(port=8888, open_browser=True)
    with open(TOKEN_PATH, 'w') as f: f.write(creds.to_json())

# 提交
session = AuthorizedSession(creds)
ok, fail = 0, 0
for i, url in enumerate(URLS):
    try:
        r = session.post('https://indexing.googleapis.com/v3/urlNotifications:publish',
            data=json.dumps({'url': url, 'type': 'URL_UPDATED'}), timeout=30)
        if r.status_code == 200:
            ok += 1; print(f'✅ [{i+1}/45] {url.split("/")[-1]}')
        else:
            fail += 1; print(f'❌ [{i+1}/45] {url.split("/")[-1]} ({r.status_code})')
    except:
        fail += 1; print(f'❌ [{i+1}/45] {url.split("/")[-1]} timeout')
    time.sleep(0.5)

print(f'\n🎉 完成！成功 {ok} 篇，失败 {fail} 篇')
