"""
提交5篇冲排名文章 URL 到 Google Indexing API
- 2篇升级文章 (viggora-guide, f2p-leveling-guide)
- 3篇新文章 (sub-70-boss, f2p-money-ranked, budget-gear)
"""

import os, sys, json, time, random, requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
SUBMITTED_FILE = os.path.join(SCRIPT_DIR, "submitted_urls.txt")
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")

# === 5 篇待推送 URL ===
URLS = [
    "https://osrsguru.com/guides/osrs-viggora-guide-2026.html",
    "https://osrsguru.com/guides/osrs-f2p-leveling-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sub-70-combat-bossing-guide-2026.html",
    "https://osrsguru.com/guides/osrs-f2p-money-making-ranked-2026.html",
    "https://osrsguru.com/guides/osrs-budget-gear-by-combat-level-2026.html",
]

def find_proxy():
    ports = [7897, 7890, 10809, 10808]
    for p in ports:
        try:
            r = requests.get("http://www.google.com", proxies={"http": f"http://127.0.0.1:{p}", "https": f"http://127.0.0.1:{p}"}, timeout=3)
            if r.status_code == 200:
                print(f"✅ 检测到代理: 127.0.0.1:{p}")
                return {"http": f"http://127.0.0.1:{p}", "https": f"http://127.0.0.1:{p}"}
        except: continue
    print("⚠️ 未检测到代理，尝试直连...")
    return None

def load_submitted():
    if os.path.exists(SUBMITTED_FILE):
        with open(SUBMITTED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_submitted(url):
    with open(SUBMITTED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def get_token(PROXY):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else: creds = None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f: f.write(creds.to_json())
        print("✅ Token 刷新成功")
        return creds
    if not creds or not creds.valid:
        print("❌ 需要重新授权！先运行 submit_crimson_desert.py 完成浏览器授权")
        sys.exit(1)
    return creds

def index_url(creds, url, PROXY, idx, total):
    from googleapiclient.discovery import build
    service = build("indexing", "v3", credentials=creds)
    body = {"url": url, "type": "URL_UPDATED"}
    try:
        service.urlNotifications().publish(body=body).execute()
        print(f"[{idx}/{total}] ✅ {url.split('/')[-1][:50]}")
        save_submitted(url)
        return True
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
            print(f"\n⛔ 429 配额用尽！已推 {idx-1}/{total}，剩余明天续推")
            return "QUOTA"
        print(f"[{idx}/{total}] ❌ {url.split('/')[-1][:40]} → {err[:80]}")
        return False

if __name__ == "__main__":
    PROXY = find_proxy()
    submitted = load_submitted()
    pending = [u for u in URLS if u not in submitted]
    print(f"\n📋 待推送: {len(pending)}/5 篇（{len(URLS)-len(pending)} 篇已跳过）\n")
    if not pending: print("全部已完成！"); sys.exit(0)

    try:
        import google.auth, googleapiclient, google.oauth2
    except ImportError:
        os.system(f"{sys.executable} -m pip install google-auth-oauthlib google-auth-httplib2 requests -q")
    
    creds = get_token(PROXY)
    ok = fail = 0
    for i, url in enumerate(pending, 1):
        result = index_url(creds, url, PROXY, i, len(pending))
        if result == "QUOTA": break
        if result: ok += 1
        else: fail += 1
        time.sleep(random.uniform(1.5, 3.0))
    
    print(f"\n🎉 完成！成功 {ok}，失败 {fail}，剩余 {len(pending)-ok-fail}")
