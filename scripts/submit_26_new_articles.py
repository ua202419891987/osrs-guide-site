#!/usr/bin/env python
"""submit_26_new_articles.py — 提交26篇新文章到Google索引"""
import os, json, time, socket
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

URLS = [
  # ===== 24 篇英文新攻略 =====
  "https://osrsguru.com/guides/osrs-best-in-slot-gear-guide-2026.html",
  "https://osrsguru.com/guides/osrs-birdhouse-runs-guide-2026.html",
  "https://osrsguru.com/guides/osrs-blast-furnace-smithing-guide-2026.html",
  "https://osrsguru.com/guides/osrs-clue-scrolls-rewards-guide-2026.html",
  "https://osrsguru.com/guides/osrs-colosseum-fortis-guide-2026.html",
  "https://osrsguru.com/guides/osrs-combat-achievements-master-guide-2026.html",
  "https://osrsguru.com/guides/osrs-dragon-defender-guide-2026.html",
  "https://osrsguru.com/guides/osrs-forestry-guide-2026.html",
  "https://osrsguru.com/guides/osrs-giants-foundry-guide-2026.html",
  "https://osrsguru.com/guides/osrs-god-wars-dungeon-boss-guide-2026.html",
  "https://osrsguru.com/guides/osrs-hallowed-sepulchre-guide-2026.html",
  "https://osrsguru.com/guides/osrs-inferno-guide-2026.html",
  "https://osrsguru.com/guides/osrs-mahogany-homes-construction-guide-2026.html",
  "https://osrsguru.com/guides/osrs-motherlode-mine-guide-2026.html",
  "https://osrsguru.com/guides/osrs-pet-hunting-guide-2026.html",
  "https://osrsguru.com/guides/osrs-pyramid-plunder-guide-2026.html",
  "https://osrsguru.com/guides/osrs-quest-cape-guide-2026.html",
  "https://osrsguru.com/guides/osrs-revenants-caves-guide-2026.html",
  "https://osrsguru.com/guides/osrs-rune-dragons-money-guide-2026.html",
  "https://osrsguru.com/guides/osrs-seaweed-runs-guide-2026.html",
  "https://osrsguru.com/guides/osrs-volcanic-mine-guide-2026.html",
  "https://osrsguru.com/guides/osrs-vorkath-money-making-guide-2026.html",
  "https://osrsguru.com/guides/osrs-wilderness-bosses-guide-2026.html",
  "https://osrsguru.com/guides/osrs-zulrah-money-making-guide-2026.html",
  # ===== 2 篇中文旗舰攻略 =====
  "https://osrsguru.com/zh/guides/osrs-china-beginner-roadmap-2026.html",
  "https://osrsguru.com/zh/guides/osrs-china-money-making-guide-2026.html",
]

BASE = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE, 'token.json')
CLIENT_SECRET_PATH = os.path.join(BASE, 'client_secret.json')

# 自动找代理
for port in [7897, 7890, 10808]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        if s.connect_ex(('127.0.0.1', port)) == 0:
            os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
            os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
            print(f'[OK] Proxy: 127.0.0.1:{port}')
            break
    finally:
        s.close()

# OAuth登录
SCOPES = ['https://www.googleapis.com/auth/indexing']
creds = None
if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    creds = flow.run_local_server(port=8888, open_browser=True)
    with open(TOKEN_PATH, 'w') as f: f.write(creds.to_json())

# 提交
total = len(URLS)
session = AuthorizedSession(creds)
ok, fail = 0, 0
for i, url in enumerate(URLS):
    try:
        r = session.post('https://indexing.googleapis.com/v3/urlNotifications:publish',
            data=json.dumps({'url': url, 'type': 'URL_UPDATED'}), timeout=30)
        if r.status_code == 200:
            ok += 1; print(f'✅ [{i+1}/{total}] {url.split("/")[-1]}')
        else:
            fail += 1; print(f'❌ [{i+1}/{total}] {url.split("/")[-1]} ({r.status_code}) {r.text[:100]}')
    except Exception as e:
        fail += 1; print(f'❌ [{i+1}/{total}] {url.split("/")[-1]} error: {e}')
    time.sleep(0.5)

print(f'\n🎉 Done! Success: {ok}, Failed: {fail}')
