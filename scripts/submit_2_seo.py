#!/usr/bin/env python3
"""
提交2篇已升级的SEO文章到 Google Indexing API
"""
import os, json, time, requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH  = os.path.join(SCRIPT_DIR, 'token.json')
PROXY       = {'http': 'http://127.0.0.1:7897', 'https': 'http://127.0.0.1:7897'}

URLS = [
    'https://osrsguru.com/guides/osrs-viggora-chainmace-guide-2026.html',
    'https://osrsguru.com/guides/osrs-1-99-hunter-guide-2026.html',
]

def load_creds():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError('token.json 不存在，请先运行 submit_crimson_desert.py 授权')
    creds = Credentials.from_authorized_user_file(TOKEN_PATH,
              ['https://www.googleapis.com/auth/indexing'])
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())
        except Exception as e:
            print(f'⚠️ Token刷新失败: {e}')
    return creds

def submit(url, creds, proxy):
    headers = {'Authorization': f'Bearer {creds.token}',
               'Content-Type': 'application/json'}
    body    = json.dumps({'url': url, 'type': 'URL_UPDATED'})
    r = requests.post(
        'https://indexing.googleapis.com/v3/urlNotifications:publish',
        headers=headers, data=body, proxies=proxy, timeout=15)
    return r

def main():
    print('=== 提交2篇SEO文章到 Google Indexing ===')
    # 检测代理
    proxy = None
    for p in ['http://127.0.0.1:7897','http://127.0.0.1:7890',
               'http://127.0.0.1:10809','http://127.0.0.1:10808']:
        try:
            if requests.get('https://www.google.com', proxies={'http':p,'https':p},
                           timeout=3).status_code == 200:
                proxy = {'http': p, 'https': p}
                print(f'✅ 代理: {p}')
                break
        except:
            continue
    if not proxy:
        print('⚠️ 未检测到代理，直接尝试...')

    creds = load_creds()
    print(f'✅ Token加载成功\n')

    submitted = set()
    log_path = os.path.join(SCRIPT_DIR, 'submitted_urls.txt')
    if os.path.exists(log_path):
        with open(log_path) as f:
            submitted = set(l.strip() for l in f if l.strip())

    for i, url in enumerate(URLS, 1):
        if url in submitted:
            print(f'[{i}/{len(URLS)}] ⏭️ 已提交，跳过: {url}')
            continue
        try:
            r = submit(url, creds, proxy)
            if r.status_code == 200:
                print(f'[{i}/{len(URLS)}] ✅ 成功: {url}')
                with open(log_path, 'a') as f:
                    f.write(url + '\n')
            elif r.status_code == 429:
                print(f'[{i}/{len(URLS)}] ⛔ 429 配额用尽，停止')
                break
            else:
                print(f'[{i}/{len(URLS)}] ❌ {r.status_code}: {r.text[:100]}')
        except Exception as e:
            print(f'[{i}/{len(URLS)}] ❌ 异常: {e}')
        time.sleep(1)

    print('\n=== 完成 ===')

if __name__ == '__main__':
    main()
