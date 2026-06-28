import json, sys, time, requests
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest

# ====== 配置 ======
SCRIPT_DIR = Path(__file__).resolve().parent
CRED_FILE = SCRIPT_DIR / "osrsguru-site-bc6b38956cb3.json"
MAX_PER_DAY = 200
SCOPES = ["https://www.googleapis.com/auth/indexing"]
# ==================

URLS = [
    "https://osrsguru.com/zh/guides/osrs-china-vpn-registration-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-china-payment-membership-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-runelite-install-hanhua-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-runelite-essential-plugins-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-newbie-day1-14-roadmap-2026.html",
    "https://osrsguru.com/zh/guides/osrs-newbie-day15-30-roadmap-2026.html",
    "https://osrsguru.com/zh/guides/osrs-glossary-items-equipment-2026.html",
    "https://osrsguru.com/zh/guides/osrs-glossary-skills-quests-bosses-2026.html",
    "https://osrsguru.com/zh/guides/osrs-pvp-pure-account-build-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-pvp-gear-switching-basics-2026.html",
    "https://osrsguru.com/zh/guides/osrs-mobile-setup-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-mobile-efficient-playing-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-dragon-slayer-2-complete-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-desert-treasure-2-complete-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-gear-progression-beginner-mid-2026.html",
    "https://osrsguru.com/zh/guides/osrs-gear-progression-mid-endgame-2026.html",
    "https://osrsguru.com/zh/guides/osrs-toa-beginner-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-cox-beginner-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-achievement-diary-easy-medium-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-achievement-diary-hard-elite-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-sailing-1-99-training-route-2026.html",
    "https://osrsguru.com/zh/guides/osrs-sailing-money-making-2026.html",
    "https://osrsguru.com/zh/forum-hot-topics.html",
    "https://osrsguru.com/zh/index.html",
    "https://osrsguru.com/zh/beginner.html",
    "https://osrsguru.com/zh/money-making.html",
    "https://osrsguru.com/zh/skill-training.html",
    "https://osrsguru.com/zh/quest-guides.html",
    "https://osrsguru.com/zh/boss-guides.html",
    "https://osrsguru.com/zh/membership.html",
]

def find_proxy():
    """自动检测本地代理"""
    ports = [7897, 7890, 10809, 10808, 8080, 1080]
    for p in ports:
        try:
            r = requests.get("https://www.google.com", proxies={"http": f"http://127.0.0.1:{p}", "https": f"http://127.0.0.1:{p}"}, timeout=3)
            if r.status_code == 200:
                print(f"✅ 检测到代理: 127.0.0.1:{p}")
                return {"http": f"http://127.0.0.1:{p}", "https": f"http://127.0.0.1:{p}"}
        except: continue
    print("⚠️ 未检测到代理，尝试直连...")
    return None

def submit_with_proxy(url, service, proxy=None):
    """提交 URL，支持代理"""
    try:
        body = {"url": url, "type": "URL_UPDATED"}
        if proxy:
            # 使用代理需要手动处理 HTTP 请求
            from google.auth.transport.requests import AuthorizedSession
            creds = service_account.Credentials.from_service_account_file(
                str(CRED_FILE), scopes=SCOPES
            )
            session = AuthorizedSession(creds)
            session.proxies = proxy
            resp = session.post(
                "https://indexing.googleapis.com/v3/urlNotifications:publish",
                json=body
            )
            if resp.status_code == 200:
                return "ok", resp.json()
            else:
                return f"error:{resp.status_code}", resp.text
        else:
            response = service.urlNotifications().publish(body=body).execute()
            return "ok", response
    except Exception as e:
        return "error", str(e)

def main():
    if not CRED_FILE.exists():
        print(f"❌ 凭证文件不存在: {CRED_FILE}")
        sys.exit(1)

    # 检测代理
    proxy = find_proxy()

    credentials = service_account.Credentials.from_service_account_file(
        str(CRED_FILE), scopes=SCOPES
    )
    
    # 如果检测到代理，设置代理
    if proxy:
        import os
        os.environ['HTTP_PROXY'] = proxy['http']
        os.environ['HTTPS_PROXY'] = proxy['https']
    
    service = build("indexing", "v3", credentials=credentials)

    success, fail = 0, 0
    results = []

    print(f"📊 今日中文站 Indexing API 提交")
    print(f"   文章: 22 篇 + 栏目页: 8 个 = 共 {len(URLS)} 个 URL")
    print(f"   每日配额: {MAX_PER_DAY}")
    print()

    for i, url in enumerate(URLS[:MAX_PER_DAY]):
        try:
            body = {"url": url, "type": "URL_UPDATED"}
            response = service.urlNotifications().publish(body=body).execute()
            meta = response.get("urlNotificationMetadata", {})
            up = meta.get("latestUpdate", {})
            status = up.get("type", "OK")
            print(f"  [{i+1}/{len(URLS)}] ✅ {status}  {url}")
            success += 1
            results.append({"url": url, "status": "ok", "result": status})
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
                print(f"  [{i+1}/{len(URLS)}] 🚨 配额用完！已成功 {success} 篇")
                results.append({"url": url, "status": "429", "result": "quota exceeded"})
                fail += 1
                break
            elif "WinError 10060" in err or "timeout" in err.lower() or "connect" in err.lower():
                print(f"  [{i+1}/{len(URLS)}] ❌ 网络连接失败，请检查 VPN/代理")
                print(f"       错误: {err[:60]}")
                results.append({"url": url, "status": "network", "result": str(e)[:80]})
                fail += 1
                break
            else:
                print(f"  [{i+1}/{len(URLS)}] ❌ {err[:80]}")
                fail += 1
                results.append({"url": url, "status": "error", "result": str(e)[:100]})

        time.sleep(0.3)

    print()
    print(f"=== 提交完成 ===")
    print(f"✅ 成功: {success}")
    print(f"❌ 失败: {fail}")

    if fail > 0 and success == 0:
        print()
        print("⚠️ 提示: Google API 在中国需要 VPN/代理")
        print("   请开启 VPN 后重新运行此脚本")

    # 保存报告
    report_dir = SCRIPT_DIR.parent / ".workbuddy" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "indexing-report-2026-06-28.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "date": "2026-06-28",
            "total": len(results),
            "success": success,
            "failed": fail,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
