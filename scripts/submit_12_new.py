#!/usr/bin/env python
"""submit_12_new.py — 提交12篇新文章到Google索引"""
import os, json, time, socket
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

URLS = [
  "https://osrsguru.com/guides/osrs-wyrmscraig-activities-guide-2026.html",
  "https://osrsguru.com/guides/osrs-wyrmscraig-rewards-ranking-2026.html",
  "https://osrsguru.com/guides/osrs-bank-tags-beginners-guide-2026.html",
  "https://osrsguru.com/guides/osrs-bank-tags-layout-guide-2026.html",
  "https://osrsguru.com/guides/osrs-trouver-system-rework-guide-2026.html",
  "https://osrsguru.com/guides/osrs-trouver-parchment-complete-guide-2026.html",
  "https://osrsguru.com/guides/osrs-fractured-archive-prep-guide-2026.html",
  "https://osrsguru.com/guides/osrs-fractured-archive-rewards-analysis-2026.html",
  "https://osrsguru.com/guides/osrs-ge-max-cash-guide-2026.html",
  "https://osrsguru.com/guides/osrs-inflation-gear-prices-2026.html",
  "https://osrsguru.com/guides/osrs-jagex-account-migration-guide-2026.html",
  "https://osrsguru.com/guides/osrs-jagex-account-faq-2026.html",
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
session = AuthorizedSession(creds)
ok, fail = 0, 0
for i, url in enumerate(URLS):
    try:
        r = session.post('https://indexing.googleapis.com/v3/urlNotifications:publish',
            data=json.dumps({'url': url, 'type': 'URL_UPDATED'}), timeout=30)
        if r.status_code == 200:
            ok += 1; print(f'✅ [{i+1}/12] {url.split("/")[-1]}')
        else:
            fail += 1; print(f'❌ [{i+1}/12] {url.split("/")[-1]} ({r.status_code})')
    except:
        fail += 1; print(f'❌ [{i+1}/12] {url.split("/")[-1]} timeout')
    time.sleep(0.5)

print(f'\n🎉 Done! Success: {ok}, Failed: {fail}')
