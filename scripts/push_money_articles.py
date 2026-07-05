#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OSRS Guru Money Articles - Google Indexing API auto-submit
===========================================================
Reads money_article_urls_51.txt and submits 51 URLs to Google Indexing API.
Uses OAuth + proxy, works in China.

Usage:
  C:/Users/Lenovo/.workbuddy/binaries/python/versions/3.13.12/python.exe "C:/Users/Lenovo/osrs-guide-site/scripts/push_money_articles.py"
"""
import os
import sys
import json
import time
import socket
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# ========== 配置 ==========
URL_LIST_PATH = r'D:\网站下载文件专栏\profit-finder-tools\money_article_urls_51.txt'
TOKEN_PATH = r'C:\Users\Lenovo\osrs-guide-site\scripts\token.json'
CLIENT_SECRET_PATH = r'C:\Users\Lenovo\osrs-guide-site\scripts\client_secret.json'
REDIRECT_URI = 'http://localhost:8888'
REDIRECT_PORT = 8888
BATCH_SIZE = 10
BATCH_DELAY = 2

# 代理端口 (自动检测)
PROXY_HOST = '127.0.0.1'
PROXY_PORTS = [7897, 7890, 10808, 10809, 8888, 9999]

oauth_code = None
oauth_error = None
server_started = threading.Event()

# ========== 代理检测 ==========
def find_proxy():
    for port in PROXY_PORTS:
        try:
            s = socket.create_connection((PROXY_HOST, port), timeout=3)
            s.close()
            proxies = {
                'http': f'http://{PROXY_HOST}:{port}',
                'https': f'http://{PROXY_HOST}:{port}',
            }
            r = requests.get('https://www.googleapis.com/', proxies=proxies, timeout=8)
            if r.status_code < 500:
                print(f'[OK] 代理已找到: {PROXY_HOST}:{port}')
                return proxies
        except Exception:
            continue
    print('[WARN] 未找到可用代理，尝试直连...')
    return None

# ========== OAuth 回调 ==========
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global oauth_code, oauth_error
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        if 'code' in params:
            oauth_code = params['code'][0]
            html = '<html><body><h2>授权成功!</h2><p>可以关闭此窗口。</p></body></html>'
        elif 'error' in params:
            oauth_error = params.get('error_description', params['error'])[0]
            html = f'<html><body><h2>授权失败</h2><p>{oauth_error}</p></body></html>'
        else:
            html = '<html><body><h2>等待授权...</h2></body></html>'
        self.wfile.write(html.encode('utf-8'))
        threading.Thread(target=self.server.shutdown).start()
    def log_message(self, format, *args):
        pass

def start_oauth_server():
    global oauth_code, oauth_error
    oauth_code = None
    oauth_error = None
    server = HTTPServer(('localhost', REDIRECT_PORT), OAuthCallbackHandler)
    server.timeout = 120
    print('[INFO] 启动 OAuth 回调服务器 (端口 8888)...')
    server_started.set()
    server.handle_request()
    if oauth_code:
        print('[OK] 授权码已收到!')
        return oauth_code
    elif oauth_error:
        raise Exception(f'OAuth 错误: {oauth_error}')
    else:
        raise Exception('OAuth 超时')

def get_access_token(proxies):
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            token_data = json.load(f)
        if token_data.get('expires_at', 0) > time.time() + 300:
            print('[OK] 使用已保存的 OAuth token')
            return token_data['access_token']
        else:
            print('[INFO] 已保存的 token 过期，重新授权...')
    
    if not os.path.exists(CLIENT_SECRET_PATH):
        print('=' * 60)
        print('错误: client_secret.json 未找到!')
        print('=' * 60)
        print(f'请将 client_secret.json 放在:')
        print(f'  {CLIENT_SECRET_PATH}')
        print('=' * 60)
        sys.exit(1)
    
    with open(CLIENT_SECRET_PATH, 'r') as f:
        client_config = json.load(f)
    client_id = client_config['installed']['client_id']
    
    auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        f'client_id={client_id}'
        f'&redirect_uri={REDIRECT_URI}'
        '&response_type=code'
        '&scope=https://www.googleapis.com/auth/indexing'
        '&access_type=offline'
        '&prompt=consent'
    )
    
    print('=' * 60)
    print('正在打开浏览器进行 Google 授权...')
    print('请在弹出的页面中允许访问。')
    print('=' * 60)
    
    server_thread = threading.Thread(target=start_oauth_server, daemon=True)
    server_thread.start()
    server_started.wait(timeout=5)
    time.sleep(0.5)
    print('[INFO] 正在打开浏览器...')
    webbrowser.open(auth_url)
    server_thread.join(timeout=130)
    
    if oauth_code is None:
        print('[ERROR] 未收到授权码，请重试。')
        sys.exit(1)
    
    client_secret = client_config['installed']['client_secret']
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': oauth_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    print('[INFO] 正在换取 access token...')
    r = requests.post('https://oauth2.googleapis.com/token', data=token_data, proxies=proxies, timeout=30)
    if r.status_code != 200:
        print(f'[ERROR] token 换取失败: {r.text}')
        sys.exit(1)
    tokens = r.json()
    tokens['expires_at'] = time.time() + tokens.get('expires_in', 3600)
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tokens, f)
    print('[OK] OAuth token 已保存!')
    return tokens['access_token']

# ========== 推送 51 篇赚钱文章 URL ==========
def push_urls(access_token, proxies):
    print(f'\n[INFO] 读取 URL 列表: {URL_LIST_PATH}')
    
    urls = []
    with open(URL_LIST_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    
    print(f'[INFO] 共 {len(urls)} 个 URL 等待推送')
    print(f'[INFO] 批量推送，每批 {BATCH_SIZE} 个...\n')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    api_url = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for url in batch:
            body = {'url': url, 'type': 'URL_UPDATED'}
            try:
                r = requests.post(api_url, headers=headers, json=body, proxies=proxies, timeout=30)
                if r.status_code == 200:
                    result = r.json()
                    notify_time = result.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime', 'unknown')
                    t = notify_time[:19] if len(notify_time) > 19 else notify_time
                    print(f'  [OK] {url} -> {t}')
                    success_count += 1
                elif r.status_code == 403:
                    print(f'  [SKIP] {url} -> 403 (Search Console 未验证)')
                    skipped_count += 1
                elif r.status_code == 429:
                    print(f'  [RATE] {url} -> 429 限流，等待 60 秒...')
                    time.sleep(60)
                    r = requests.post(api_url, headers=headers, json=body, proxies=proxies, timeout=30)
                    if r.status_code == 200:
                        print(f'  [OK] {url} -> 重试成功')
                        success_count += 1
                    else:
                        print(f'  [FAIL] {url} -> {r.status_code}')
                        error_count += 1
                else:
                    print(f'  [FAIL] {url} -> {r.status_code}: {r.text[:100]}')
                    error_count += 1
            except requests.exceptions.Timeout:
                print(f'  [TIMEOUT] {url} -> 请求超时')
                error_count += 1
            except Exception as e:
                print(f'  [ERROR] {url} -> {str(e)}')
                error_count += 1
        
        if i + BATCH_SIZE < len(urls):
            time.sleep(BATCH_DELAY)
    
    print(f'\n{"=" * 60}')
    print(f'推送完成: 成功 {success_count} | 跳过 {skipped_count} | 失败 {error_count}')
    print(f'{"=" * 60}')
    return success_count, skipped_count, error_count

# ========== 启动 ==========
if __name__ == '__main__':
    print('=' * 60)
    print('OSRS Guru — 赚钱文章 Indexing API 自动推送')
    print('=' * 60)
    proxies = find_proxy()
    access_token = get_access_token(proxies)
    push_urls(access_token, proxies)
    input('\n按 Enter 键退出...')
