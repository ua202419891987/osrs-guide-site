#!/usr/bin/env python3
"""提交中文站「赚钱方法」专栏的 URL 到 Google Indexing API"""

import json, os, sys, time, subprocess, re
from pathlib import Path

# ============ 要推送的 URL 列表 ============
URLS = [
    # === 赚钱方法 (31篇 + 1列表页) ===
    "https://osrsguru.com/zh/money-making.html",
    "https://osrsguru.com/zh/guides/osrs-best-money-making-methods-2026.html",
    "https://osrsguru.com/zh/guides/osrs-f2p-money-making-no-stats.html",
    "https://osrsguru.com/zh/guides/osrs-f2p-ironman-money-making-early-game.html",
    "https://osrsguru.com/zh/guides/osrs-ironman-money-making-f2p-2026.html",
    "https://osrsguru.com/zh/guides/osrs-low-effort-money-making-beginners.html",
    "https://osrsguru.com/zh/guides/osrs-f2p-money-making-first-bond-2026.html",
    "https://osrsguru.com/zh/guides/osrs-ironman-p2p-money-making-2026.html",
    "https://osrsguru.com/zh/guides/osrs-mid-game-money-making-roadmap-2026.html",
    "https://osrsguru.com/zh/guides/osrs-wilderness-money-making-2026.html",
    "https://osrsguru.com/zh/guides/osrs-bond-farming-free-membership-2026.html",
    "https://osrsguru.com/zh/guides/osrs-afk-money-making-ultimate-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-flipping-guide-beginners-2026.html",
    "https://osrsguru.com/zh/guides/osrs-daily-weekly-money-routine-2026.html",
    "https://osrsguru.com/zh/guides/osrs-quest-unlocked-money-methods-2026.html",
    "https://osrsguru.com/zh/guides/osrs-how-to-spend-gp-wisely-2026.html",
    "https://osrsguru.com/zh/guides/osrs-money-making-fishing-2026.html",
    "https://osrsguru.com/zh/guides/osrs-passive-money-making-offline.html",
    "https://osrsguru.com/zh/guides/osrs-hunter-money-making-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-how-to-make-money-with-crafting-low-level.html",
    "https://osrsguru.com/zh/guides/osrs-how-to-rune-spinning-profit-2026.html",
    "https://osrsguru.com/zh/guides/osrs-skilling-money-post-sailing-2026.html",
    "https://osrsguru.com/zh/guides/osrs-killing-green-dragons-money-per-hour.html",
    "https://osrsguru.com/zh/guides/osrs-how-to-make-money-with-zulrah.html",
    "https://osrsguru.com/zh/guides/osrs-chambers-of-xeric-loot-profit-guide.html",
    "https://osrsguru.com/zh/guides/osrs-how-to-flip-items-profit-mid-game.html",
    "https://osrsguru.com/zh/guides/osrs-cheap-flipping-methods-new-players.html",
    "https://osrsguru.com/zh/guides/osrs-wintertodt-money-making-per-hour.html",
    "https://osrsguru.com/zh/guides/osrs-slayer-money-making-guide-2026.html",
    "https://osrsguru.com/zh/guides/osrs-boss-profit-comparison-2026.html",
    "https://osrsguru.com/zh/guides/osrs-combat-money-making-non-boss-2026.html",
    "https://osrsguru.com/zh/guides/osrs-money-making-tier-list-2026.html",
]

# Deduplicate
URLS = list(dict.fromkeys(URLS))

# ============ 配置 ============
SCRIPT_DIR = Path(__file__).parent
SUBMITTED_FILE = SCRIPT_DIR / "submitted_urls.txt"
CREDENTIALS_FILE = SCRIPT_DIR / "google_credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"
API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# ============ 检测代理 ============
PROXY_PORTS = [7897, 7890, 10809, 10808, 7891, 9090]
def detect_proxy():
    for port in PROXY_PORTS:
        try:
            r = subprocess.run(
                f'curl -s -o /dev/null -w "%{{http_code}}" --connect-timeout 2 -x http://127.0.0.1:{port} https://www.google.com',
                shell=True, capture_output=True, text=True, timeout=5
            )
            if r.stdout.strip() in ("200", "302", "301"):
                return f"http://127.0.0.1:{port}"
        except:
            continue
    return None

# ============ 获取 Token ============
def get_token(proxy_url):
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import google.auth

    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url

    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ 缺少 {CREDENTIALS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.parent.mkdir(exist_ok=True)
        TOKEN_FILE.write_text(creds.to_json())

    return creds

# ============ 加载已提交 ============
def load_submitted():
    if SUBMITTED_FILE.exists():
        return set(SUBMITTED_FILE.read_text(encoding="utf-8").splitlines())
    return set()

def save_submitted(url):
    SUBMITTED_FILE.parent.mkdir(exist_ok=True)
    with open(SUBMITTED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

# ============ 主流程 ============
def main():
    # 过滤已提交
    submitted = load_submitted()
    pending = [u for u in URLS if u not in submitted]
    print(f"总 URL: {len(URLS)} | 已提交: {len(URLS)-len(pending)} | 待推送: {len(pending)}")

    if not pending:
        print("✅ 全部已推送")
        return

    # 检测代理
    proxy = detect_proxy()
    if not proxy:
        print("❌ 未检测到代理，请先打开 Clash/V2Ray")
        sys.exit(1)
    print(f"✅ 代理: {proxy}")

    # 获取 Token
    creds = get_token(proxy)
    from google.auth.transport.requests import AuthorizedSession
    authed_session = AuthorizedSession(creds)

    # 逐个推送
    success, failed, skipped_429 = 0, 0, 0
    for i, url in enumerate(pending, 1):
        if skipped_429 > 0:
            print(f"[{i}/{len(pending)}] ⏭️  配额不足，跳过: {url}")
            skipped_429 += 1
            continue

        body = json.dumps({"url": url, "type": "URL_UPDATED"})
        try:
            resp = authed_session.post(API_URL, data=body, headers={"Content-Type": "application/json"})
            if resp.status_code == 200:
                print(f"[{i}/{len(pending)}] ✅ {url}")
                success += 1
                save_submitted(url)
            elif resp.status_code == 429:
                print(f"[{i}/{len(pending)}] ⛔ 429 配额用尽，停止")
                skipped_429 = len(pending) - i + 1
                break
            else:
                print(f"[{i}/{len(pending)}] ❌ {resp.status_code} {url}")
                print(f"    Response: {resp.text[:200]}")
                failed += 1
        except Exception as e:
            print(f"[{i}/{len(pending)}] ❌ {url} - {e}")
            failed += 1

        time.sleep(0.35)  # Google 推荐延迟

    # 汇总
    print(f"\n{'='*50}")
    print(f"✅ 成功: {success}  |  ❌ 失败: {failed}  |  ⛔ 被429截断: {skipped_429}")
    if skipped_429:
        remaining = pending[success+failed:]
        print(f"📌 剩余 {len(remaining)} 篇等待明天配额重置后继续推送。")

if __name__ == "__main__":
    main()
