@echo off
title OSRS Guru - 提交今天修改的45篇到Google索引
chcp 65001 >nul
echo ============================================
echo   OSRS Guru - 提交今日45篇修改到Google
echo ============================================
echo.

cd /d "C:\Users\Lenovo\osrs-guide-site"

REM 用Git获取今天修改的URL列表
echo [1/2] 提取今天修改的文章URL...
git log --oneline --since="2026-06-28 00:00" --until="2026-06-29 00:00" --format="---" >nul
(for /f "tokens=*" %%f in ('git diff --name-only a39a7ba~1..d86f9e3 ^| findstr /i "^guides/.*\.html$" ^| findstr /v "crimson"') do (
  echo https://osrsguru.com/%%f
)) > scripts\today_urls.txt

REM 统计条数
findstr /r "https://" scripts\today_urls.txt >nul
if %errorlevel% equ 0 (
    for /f %%c in ('type scripts\today_urls.txt ^| find /c /v ""') do set COUNT=%%c
) else (
    set COUNT=0
)
echo 找到 %COUNT% 篇修改文章

REM 写一个简版提交脚本
echo [2/2] 启动Google Indexing提交...
echo.
echo 准备提交到Google索引，配额200条，今天用了%COUNT%条
echo.
echo A browser window will open for Google login.
echo Make sure your VPN/Clash proxy is running!
echo.

REM === 设置代理（Clash默认7897端口） ===
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897

REM 生成临时的Python单次提交脚本
python -c ^
"import requests, json, os; ^
urls = [l.strip() for l in open('scripts/today_urls.txt').readlines() if l.strip()]; ^
print(f'Total URLs to submit: {len(urls)}'); ^
f = open('scripts/today_submit.py', 'w'); ^
f.write('''import sys, json, os, time, socket, webbrowser, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# === 今天修改的45篇URL ===
URLS = %s

CLIENT_SECRET = r\"C:\\Users\\Lenovo\\osrs-guide-site\\scripts\\client_secret.json\"
TOKEN_PATH = r\"C:\\Users\\Lenovo\\osrs-guide-site\\scripts\\token.json\"
PROXY_PORTS = [7897, 7890, 10808]

def find_port():
    for p in PROXY_PORTS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(('127.0.0.1', p))
            s.close()
            return p
        except: pass
    return None

PROXY = find_port()
if PROXY:
    os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{PROXY}'
    os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{PROXY}'
    print(f\"Proxy: 127.0.0.1:{PROXY}\")
else:
    print(\"WARNING: No proxy found, may timeout in China\")

# OAuth + submit (simplified flow)
try:
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = [\"https://www.googleapis.com/auth/indexing\"]

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
        creds = flow.run_local_server(port=8888, open_browser=True, authorization_prompt_message=\"Please log in with your Google account\")
        with open(TOKEN_PATH, 'w') as t: t.write(creds.to_json())

    session = AuthorizedSession(creds)
    success = 0; fail = 0
    for i, url in enumerate(URLS):
        content = json.dumps({'url': url, 'type': 'URL_UPDATED'})
        try:
            r = session.post('https://indexing.googleapis.com/v3/urlNotifications:publish', data=content, timeout=30)
            if r.status_code == 200:
                success += 1; print(f\"[{i+1}/{len(URLS)}] ✅ {url.split('/')[-1]}\")
            else:
                fail += 1; print(f\"[{i+1}/{len(URLS)}] ❌ {url.split('/')[-1]} - {r.status_code}\")
        except Exception as e:
            fail += 1; print(f\"[{i+1}/{len(URLS)}] ❌ {url.split('/')[-1]} - timeout\")
        time.sleep(0.5)
    print(f\"\\\\nDone! Success: {success}, Failed: {fail}\")
except Exception as e:
    print(f\"Error: {e}\")
    print(\"Make sure client_secret.json exists in scripts/ folder\")
    print(\"Make sure your internet/VPN is working\")
''' % json.dumps(urls))
f.close()"

echo.
echo Running submission...
python scripts/today_submit.py

echo.
echo ============================================
pause
