#!/usr/bin/env python3
"""提交 中文站 (zh/) 所有未推送文章到 Google Indexing API
   配额 45 次，约 172 篇待推送，脚本会在 429 时自动停止
   剩余文章可明天继续推送
"""
import os, sys, time, socket, requests, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP = os.path.join(os.path.dirname(SCRIPT_DIR), "sitemap.xml")
SUBMITTED_FILE = os.path.join(SCRIPT_DIR, "submitted_urls.txt")

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

# ---- 3. 加载 URL 列表 ----
def load_urls():
    """从 sitemap 解析所有 zh/ URL，排除已提交的"""
    with open(SITEMAP, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取所有 zh/ URL
    all_urls = re.findall(r'<loc>(https://osrsguru\.com/zh/[^<]+)</loc>', content)
    
    # 加载已提交
    submitted = set()
    if os.path.exists(SUBMITTED_FILE):
        with open(SUBMITTED_FILE, "r") as f:
            submitted = set(line.strip() for line in f if line.strip())
    
    unsubmitted = [u for u in all_urls if u not in submitted]
    return unsubmitted, submitted

urls_to_submit, submitted_set = load_urls()

print(f"\n{'='*70}")
print(f"  中文站 (zh/) — 待提交 {len(urls_to_submit)} 篇")
print(f"  今日配额剩余约 45 次，用完自动停止")
print(f"{'='*70}\n")

if not urls_to_submit:
    print("✅ 所有中文站 URL 已提交完毕！")
    sys.exit(0)

# ---- 4. 提交 ----
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
ok = fail = 0
MAX = min(len(urls_to_submit), 45)  # 最多推 45 篇

for i, url in enumerate(urls_to_submit):
    body = {'url': url, 'type': 'URL_UPDATED'}
    try:
        resp = requests.post(API_URL, json=body, headers={
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }, proxies=proxies, timeout=15)

        if resp.status_code == 200:
            short = url.replace('https://osrsguru.com/zh/', '').replace('guides/', '').replace('.html', '')[:55]
            print(f"[{i+1:3d}/{len(urls_to_submit)}] ✅ {short}")
            ok += 1
            # 记录到文件
            with open(SUBMITTED_FILE, "a") as f:
                f.write(url + "\n")
        elif resp.status_code == 429:
            print(f"[{i+1:3d}/{len(urls_to_submit)}] 🚨 429 配额耗尽！已成功 {ok} 篇")
            break
        elif resp.status_code == 403:
            short = url.replace('https://osrsguru.com/zh/', '').replace('guides/', '').replace('.html', '')[:55]
            print(f"[{i+1:3d}/{len(urls_to_submit)}] ⏭ 403 — {short}")
        else:
            short = url.replace('https://osrsguru.com/zh/', '').replace('guides/', '').replace('.html', '')[:55]
            print(f"[{i+1:3d}/{len(urls_to_submit)}] ⏭ {resp.status_code} — {short}")
            fail += 1
    except Exception as e:
        short = url.replace('https://osrsguru.com/zh/', '').replace('guides/', '').replace('.html', '')[:55]
        print(f"[{i+1:3d}/{len(urls_to_submit)}] ❌ 网络错误 — {short}: {str(e)[:30]}")
        fail += 1

    time.sleep(0.6)

print(f"\n{'='*70}")
print(f"  结果: ✅ {ok} | ⏭ {fail} | 剩余 {len(urls_to_submit) - ok - fail} 篇待推送")
print(f"  明天可继续：python submit_zh.py")
print(f"{'='*70}")
