import json, sys, time, requests, io, os
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ====== 配置 ======
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(SCRIPT_DIR, 'osrsguru-site-bc6b38956cb3.json')
MAX_PER_DAY = 200
SCOPES = ['https://www.googleapis.com/auth/indexing']
API_URL = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
# ==================

URLS = [
    # === 22篇新中文站文章 ===
    'https://osrsguru.com/zh/guides/osrs-china-vpn-registration-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-china-payment-membership-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-runelite-install-hanhua-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-runelite-essential-plugins-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-newbie-day1-14-roadmap-2026.html',
    'https://osrsguru.com/zh/guides/osrs-newbie-day15-30-roadmap-2026.html',
    'https://osrsguru.com/zh/guides/osrs-glossary-items-equipment-2026.html',
    'https://osrsguru.com/zh/guides/osrs-glossary-skills-quests-bosses-2026.html',
    'https://osrsguru.com/zh/guides/osrs-pvp-pure-account-build-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-pvp-gear-switching-basics-2026.html',
    'https://osrsguru.com/zh/guides/osrs-mobile-setup-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-mobile-efficient-playing-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-dragon-slayer-2-complete-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-desert-treasure-2-complete-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-gear-progression-beginner-mid-2026.html',
    'https://osrsguru.com/zh/guides/osrs-gear-progression-mid-endgame-2026.html',
    'https://osrsguru.com/zh/guides/osrs-toa-beginner-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-cox-beginner-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-achievement-diary-easy-medium-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-achievement-diary-hard-elite-guide-2026.html',
    'https://osrsguru.com/zh/guides/osrs-sailing-1-99-training-route-2026.html',
    'https://osrsguru.com/zh/guides/osrs-sailing-money-making-2026.html',
    # === 8个更新栏目页 ===
    'https://osrsguru.com/zh/forum-hot-topics.html',
    'https://osrsguru.com/zh/index.html',
    'https://osrsguru.com/zh/beginner.html',
    'https://osrsguru.com/zh/money-making.html',
    'https://osrsguru.com/zh/skill-training.html',
    'https://osrsguru.com/zh/quest-guides.html',
    'https://osrsguru.com/zh/boss-guides.html',
    'https://osrsguru.com/zh/membership.html',
]

def find_proxy():
    """自动检测本地代理"""
    ports = [7897, 7890, 10809, 10808, 8080, 1080]
    for p in ports:
        try:
            proxies = {"http": f"http://127.0.0.1:{p}", "https": f"http://127.0.0.1:{p}"}
            r = requests.get("https://www.googleapis.com/", proxies=proxies, timeout=5)
            if r.status_code in [200, 301, 302, 404]:
                print(f"✅ 检测到代理: 127.0.0.1:{p}")
                return proxies
        except: continue
    print("⚠️ 未检测到代理，尝试直连...")
    return None

def main():
    proxy = find_proxy()
    if not proxy:
        print("❌ 需要 VPN/代理才能连接 Google API")
        return

    credentials = service_account.Credentials.from_service_account_file(CRED_FILE, scopes=SCOPES)

    success, fail = 0, 0
    results = []

    print(f"\n📊 今日 Indexing API 提交")
    print(f"   共 {len(URLS)} 个 URL")
    print(f"   每日配额: {MAX_PER_DAY}")
    print()

    for i, url in enumerate(URLS[:MAX_PER_DAY]):
        try:
            # 获取 access token
            auth_req = Request()
            credentials.refresh(auth_req)
            token = credentials.token

            payload = json.dumps({'url': url, 'type': 'URL_UPDATED'})
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            resp = requests.post(API_URL, headers=headers, data=payload, proxies=proxy, timeout=30)

            if resp.status_code == 200:
                print(f"  [{i+1}/{len(URLS)}] ✅ {url}")
                success += 1
                results.append({"url": url, "status": "ok"})
            elif resp.status_code == 429:
                print(f"  [{i+1}/{len(URLS)}] 🚨 配额用完！已成功 {success} 篇")
                results.append({"url": url, "status": "429"})
                break
            elif resp.status_code == 403:
                print(f"  [{i+1}/{len(URLS)}] ❌ 403 {resp.text[:100]}")
                fail += 1
                results.append({"url": url, "status": "403", "error": resp.text[:100]})
            else:
                print(f"  [{i+1}/{len(URLS)}] ⚠️ {resp.status_code} {resp.text[:80]}")
                fail += 1
                results.append({"url": url, "status": str(resp.status_code)})
        except Exception as e:
            print(f"  [{i+1}/{len(URLS)}] ❌ {str(e)[:80]}")
            fail += 1
            results.append({"url": url, "status": "error", "error": str(e)[:100]})
            break

        time.sleep(0.3)

    print(f"\n=== 提交完成 ===")
    print(f"✅ 成功: {success}")
    print(f"❌ 失败: {fail}")
    print(f"\n💡 下次还需要提交 Windrose 的 12 篇新文章 + 30篇现存文章")

    # 打印结果到屏幕，不写文件（避开沙箱权限）
    print(f"\n📋 提交报告 (屏幕日志):")
    for r in results[:5]:
        print(f"  {r.get('status','?')} {r['url']}")
    if len(results) > 5:
        print(f"  ... 共 {len(results)} 条")

if __name__ == '__main__':
    main()
