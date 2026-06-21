import json
import sys
import time
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# ====== 配置 ======
CRED_FILE = 'google_indexing_creds.json'  # 改为你的凭证文件路径
URL_FILE = 'C:/Users/Lenovo/WorkBuddy/2026-06-19-20-59-46/remaining_urls.txt'
REPORT_FILE = 'C:/Users/Lenovo/WorkBuddy/2026-06-19-20-59-46/indexing-report-2026-06-20.txt'
MAX_PER_DAY = 200  # Google Indexing API 每日配额
# ======================

SCOPES = ['https://www.googleapis.com/auth/indexing']
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

def get_credentials(cred_file):
    return service_account.Credentials.from_service_account_file(cred_file, scopes=SCOPES)

def submit_url(url, creds):
    headers = {}
    creds.before_request(Request(), 'POST', API_URL, headers)
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({'url': url, 'type': 'URL_UPDATED'})
    resp = requests.post(API_URL, headers=headers, data=payload, timeout=30)
    return resp.status_code, resp.text

def main():
    if len(sys.argv) > 1:
        cred_file = sys.argv[1]
    else:
        cred_file = CRED_FILE

    with open(URL_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f'Total URLs to submit: {len(urls)}')
    print(f'Max per day: {MAX_PER_DAY}')

    creds = get_credentials(cred_file)
    success, failed_403, failed_other = 0, 0, 0
    results = []

    for i, url in enumerate(urls[:MAX_PER_DAY]):
        status, text = submit_url(url, creds)
        if status == 200:
            success += 1
            msg = f'  OK [{i+1}] {url}'
            print(msg)
            results.append(f'OK: {url}')
        elif status == 403:
            failed_403 += 1
            msg = f'  403 (already indexed, skip) [{i+1}] {url}'
            print(msg)
            results.append(f'403 (skip): {url}')
            # 403 不重试，不浪费配额
        else:
            failed_other += 1
            msg = f'  FAIL [{i+1}] {url} — {status} {text[:100]}'
            print(msg)
            results.append(f'FAIL ({status}): {url} — {text[:200]}')

        time.sleep(0.6)  # 避免 429

    print(f'\nDone! Success: {success}, 403 (skip): {failed_403}, Other fail: {failed_other}')

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f'Report: {time.strftime("%Y-%m-%d %H:%M")}\n')
        f.write(f'Success: {success}\n403 (skip): {failed_403}\nOther fail: {failed_other}\n\n')
        f.write('\n'.join(results))

    print(f'Report saved to: {REPORT_FILE}')
    print(f'\nremaining URLs for tomorrow: {max(0, len(urls) - MAX_PER_DAY)}')

if __name__ == '__main__':
    main()
