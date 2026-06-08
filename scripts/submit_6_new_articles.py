#!/usr/bin/env python3
"""
OSRS Guru - Submit ONLY the 6 new June 2026 articles
Run this tomorrow (June 8) when quota refreshes (200/day reset).
"""

import os
import sys
import json
import time
import pickle
import socket

# === Config: Only these 6 URLs ===
NEW_URLS = [
    "https://osrsguru.com/guides/osrs-mid-game-breakthrough-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-ship-crew-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-afk-training-guide-2026.html",
    "https://osrsguru.com/guides/osrs-toa-solo-beginner-guide-2026.html",
    "https://osrsguru.com/guides/osrs-slayer-block-skip-list-2026.html",
    "https://osrsguru.com/guides/osrs-corrupted-gauntlet-guide-2026.html",
]

# === Global socket timeout ===
socket.setdefaulttimeout(30)

script_dir = os.path.dirname(os.path.abspath(__file__))
SUBMITTED_FILE = os.path.join(script_dir, 'submitted_urls.txt')

print("=" * 60)
print("  OSRS Guru - Submit 6 NEW Articles (June 2026)")
print("=" * 60)

# === Step 0: Proxy check ===
proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or 'http://127.0.0.1:7897'
print(f"\nProxy: {proxy_url or '(none)'}")

print("[TEST] Checking network to Google...")
try:
    s = socket.create_connection(('www.google.com', 443), timeout=8)
    s.close()
    print("  Socket OK: google.com:443 reachable")
    use_proxy = False
except Exception:
    print("  Direct fail, will use proxy")
    use_proxy = True

# === Step 1: Load libraries ===
print("\n[INIT] Loading libraries...")
try:
    from google.auth.transport.requests import Request as AuthRequest
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    import requests
    print("  Libraries loaded OK")
except ImportError as e:
    print(f"  MISSING LIB: {e}")
    print("  Run: pip install google-auth-oauthlib google-auth requests")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/indexing']

# === Step 2: OAuth credentials ===
def get_credentials():
    token_file = os.path.join(script_dir, 'token.json')
    secret_file = os.path.join(script_dir, 'client_secret.json')
    creds = None

    if not os.path.exists(secret_file):
        print(f"\nERROR: {secret_file} not found!")
        sys.exit(1)

    if os.path.exists(token_file):
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(AuthRequest())
        else:
            print("\n" + "=" * 60)
            print("  Google OAuth Authorization Required")
            print("=" * 60)
            print("\n1. A browser tab will open")
            print("2. Log in with: 1530398390@qq.com")
            print("3. Click 'Allow'")
            print("4. Browser will show 'This site can't be reached' - THAT'S OK!")
            print("   The script already received the token.\n")

            flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
            ports = [8888, 9999, 7777, 5555]
            for port in ports:
                try:
                    creds = flow.run_local_server(port=port, open_browser=True)
                    break
                except OSError:
                    continue
            else:
                print("ERROR: All ports in use.")
                sys.exit(1)

        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)
        print("\nToken saved for future runs.")

    return creds


# === Step 3: Submit one URL ===
def submit_url(creds, url):
    endpoint = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')

    proxies = {}
    if use_proxy and proxy_url:
        proxies['https'] = proxy_url
        proxies['http'] = proxy_url

    try:
        if creds.expired and creds.refresh_token:
            creds.refresh(AuthRequest())

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {creds.token}',
        }

        resp = requests.post(
            endpoint,
            data=body,
            headers=headers,
            proxies=proxies if proxies else None,
            timeout=30,
            verify=True,
        )
        if resp.status_code == 200:
            return True, resp.json().get('urlNotificationMetadata', {})
        elif resp.status_code == 429:
            return False, "HTTP 429 (QUOTA EXCEEDED)"
        else:
            return False, f"HTTP {resp.status_code}: {resp.text[:100]}"
    except requests.exceptions.Timeout:
        return False, "TIMEOUT (>30s)"
    except Exception as e:
        return False, str(e)[:120]


# === Step 4: Load already-submitted URLs ===
def load_submitted():
    if os.path.exists(SUBMITTED_FILE):
        with open(SUBMITTED_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_submitted(url):
    with open(SUBMITTED_FILE, 'a') as f:
        f.write(url + '\n')


# === MAIN ===
def main():
    creds = get_credentials()
    print("\nOK - Authenticated!")

    already = load_submitted()

    # Filter out already submitted
    to_submit = [u for u in NEW_URLS if u not in already]

    if not to_submit:
        print("\n✅ All 6 URLs already submitted! Nothing to do.")
        return

    print(f"\n[SUBMIT] Submitting {len(to_submit)} NEW URLs to Google Indexing API...")
    print("-" * 60)

    success = 0
    failed = 0
    failed_urls = []

    for i, url in enumerate(to_submit, 1):
        short = url.replace('https://osrsguru.com/', '')
        print(f"[{i}/{len(to_submit)}] {short[:55]}")
        ok, result = submit_url(creds, url)
        if ok:
            print("         ✅ OK")
            success += 1
            save_submitted(url)
        else:
            print(f"         ❌ FAIL: {result}")
            failed += 1
            failed_urls.append(url)
        time.sleep(1)  # Be gentle

    print("\n" + "=" * 60)
    print(f"DONE!  Success: {success}  |  Failed: {failed}")
    print("=" * 60)

    if success > 0:
        print(f"\n✅ {success} URLs submitted! Check Search Console in 2-3 days.")
    if failed > 0:
        print(f"\n❌ {failed} URLs failed:")
        for u in failed_urls:
            print(f"  - {u}")


if __name__ == '__main__':
    main()
