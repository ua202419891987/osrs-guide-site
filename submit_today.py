import json
import sys
import time
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# ====== 配置 ======
CRED_FILE = 'google_indexing_creds.json'  # 你的 Google API 凭证文件
MAX_PER_DAY = 200  # Google Indexing API 每日配额
# ======================

SCOPES = ['https://www.googleapis.com/auth/indexing']
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

# 按优先级排序的 URL 列表（今天新增的 33 个）
PRIORITY_URLS = [
    # P0: 最高优先级（首页 + 核心新手攻略）
    'https://osrsguru.com/',
    'https://osrsguru.com/index.html',
    'https://osrsguru.com/guides/osrs-new-player-guide-2026.html',
    'https://osrsguru.com/guides/osrs-grand-exchange-guide-2026.html',
    'https://osrsguru.com/guides/osrs-prayer-training-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-slayer-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-ironman-beginner-guide-2026.html',

    # P1: 高优先级（热门内容）
    'https://osrsguru.com/guides/osrs-mobile-guide-2026.html',
    'https://osrsguru.com/guides/osrs-pvm-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-account-security-anti-scam-guide-2026.html',
    'https://osrsguru.com/guides/osrs-common-beginner-mistakes-avoid-2026.html',
    'https://osrsguru.com/guides/osrs-returning-player-guide-2026.html',
    'https://osrsguru.com/guides/osrs-barrows-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-low-level-skilling-money-makers-2026.html',

    # P2: 中优先级（其余 OSRS 新手攻略）
    'https://osrsguru.com/guides/osrs-achievement-diary-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-clan-social-guide-2026.html',
    'https://osrsguru.com/guides/osrs-clue-scrolls-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-daily-weekly-reset-activities-guide-2026.html',
    'https://osrsguru.com/guides/osrs-farming-herb-runs-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-minigames-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-nmz-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-poh-beginner-guide-2026.html',
    'https://osrsguru.com/guides/osrs-wilderness-survival-beginner-2026.html',

    # P3: 低优先级（Windrose 攻略）
    'https://osrsguru.com/guides/windrose/index.html',
    'https://osrsguru.com/guides/windrose/windrose-beginner-guide-2026.html',
    'https://osrsguru.com/guides/windrose/windrose-base-building-tips-2026.html',
    'https://osrsguru.com/guides/windrose/windrose-boss-guide-2026.html',
    'https://osrsguru.com/guides/windrose/windrose-combat-ship-guide-2026.html',
    'https://osrsguru.com/guides/windrose/windrose-crafting-gear-guide-2026.html',
    'https://osrsguru.com/guides/windrose/windrose-quest-exploration-guide-2026.html',

    # 栏目页
    'https://osrsguru.com/monthly-updates.html',
    'https://osrsguru.com/weekly-updates.html',
    'https://osrsguru.com/community.html',
    'https://osrsguru.com/contact.html',
]

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
    try:
        resp = requests.post(API_URL, headers=headers, data=payload, timeout=30)
        return resp.status_code, resp.text
    except Exception as e:
        return 500, str(e)

def main():
    if len(sys.argv) > 1:
        cred_file = sys.argv[1]
    else:
        cred_file = CRED_FILE

    print(f'📊 今日 Indexing API 提交任务')
    print(f'   总 URL 数: {len(PRIORITY_URLS)}')
    print(f'   每日配额: {MAX_PER_DAY}')
    print()

    creds = get_credentials(cred_file)
    success, failed_403, failed_other = 0, 0, 0
    results = []

    for i, url in enumerate(PRIORITY_URLS[:MAX_PER_DAY]):
        status, text = submit_url(url, creds)
        result = {'url': url, 'status': status}
        if status == 200:
            success += 1
            result['result'] = '✅ 成功'
            print(f'  [{i+1}/{len(PRIORITY_URLS)}] ✅ {url}')
        elif status == 403:
            failed_403 += 1
            result['result'] = '❌ 403 无权限'
            print(f'  [{i+1}/{len(PRIORITY_URLS)}] ❌ 403 {url}')
        elif status == 429:
            failed_other += 1
            result['result'] = '🚨 429 配额用完'
            print(f'  [{i+1}/{len(PRIORITY_URLS)}] 🚨 429 配额用完！停止提交')
            results.append(result)
            break
        else:
            failed_other += 1
            result['result'] = f'❌ {status}'
            print(f'  [{i+1}/{len(PRIORITY_URLS)}] ❌ {status} {url}')

        results.append(result)
        time.sleep(0.5)  # 避免 QPS 超限

    print()
    print('=== 提交完成 ===')
    print(f'✅ 成功: {success}')
    print(f'❌ 403 错误: {failed_403}')
    print(f'❌ 其他错误: {failed_other}')
    print(f'🚨 429 配额用完: { "是" if any(r["status"] == 429 for r in results) else "否"}')

    # 保存报告
    report_file = f'.workbuddy/reports/indexing-report-2026-06-21.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({'date': '2026-06-21', 'total': len(results), 'success': success, 'failed_403': failed_403, 'failed_other': failed_other, 'results': results}, f, ensure_ascii=False, indent=2)
    print(f'\n报告已保存: {report_file}')

if __name__ == '__main__':
    main()
