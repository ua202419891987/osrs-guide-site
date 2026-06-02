#!/usr/bin/env python3
"""
OSRS Guru - Google Indexing API OAuth Submit v4
Uses 'requests' library for proper proxy support.
"""

import os
import sys
import json
import time
import pickle
import socket
import urllib.request
import urllib.error

# Global socket timeout
socket.setdefaulttimeout(30)

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Step 0: Quick network check (socket test only, no proxy test)
# ============================================================
print("=" * 60)
print("  OSRS Guru - Indexing API Submit v4")
print("=" * 60)

proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or ''
print(f"\nProxy: {proxy_url or '(none)'}")

# Quick socket test (won't hang like urllib proxy test)
print("[TEST] Checking network to Google...")
try:
    s = socket.create_connection(('www.google.com', 443), timeout=8)
    s.close()
    print("  Socket OK: google.com:443 reachable")
    use_proxy = False
except Exception:
    print("  Direct fail, will use proxy")
    use_proxy = True

# ============================================================
# Step 1: Imports (after confirming network works)
# ============================================================
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


# ============================================================
# Step 2: Get OAuth credentials
# ============================================================
def get_credentials():
    token_file = os.path.join(script_dir, 'token.json')
    secret_file = os.path.join(script_dir, 'client_secret.json')
    creds = None

    if not os.path.exists(secret_file):
        print(f"\nERROR: {secret_file} not found!")
        print("Download OAuth client secret from Google Cloud Console.")
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


# ============================================================
# Step 3: Submit URL using requests (BEST proxy support)
# ============================================================
def submit_url(creds, url):
    """Submit one URL using requests library (proper proxy support)."""
    endpoint = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')

    # Refresh token if needed
    if creds.expired and creds.refresh_token:
        creds.refresh(AuthRequest())

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.token}',
    }

    # Build proxies dict for requests
    proxies = {}
    if use_proxy and proxy_url:
        proxies['https'] = proxy_url
        proxies['http'] = proxy_url

    try:
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
        else:
            return False, f"HTTP {resp.status_code}: {resp.text[:100]}"
    except requests.exceptions.Timeout:
        return False, "TIMEOUT (>30s)"
    except requests.exceptions.ConnectionError as e:
        return False, f"CONNECTION ERROR: {str(e)[:80]}"
    except Exception as e:
        return False, str(e)[:120]


# ============================================================
# Step 4: Parse sitemap
# ============================================================
def get_urls(sitemap_path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    urls = []
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    for elem in root.findall('ns:url', ns):
        loc = elem.find('ns:loc', ns)
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
    return urls


# ============================================================
# MAIN
# ============================================================
def main():
    print("\n[Step 1/4] Authenticating with Google...")
    creds = get_credentials()
    print("OK - Authenticated!")

    print("\n[Step 2/4] Submitting URLs with requests + proxy support...")
    if use_proxy and proxy_url:
        print(f"  Using proxy: {proxy_url}")
    else:
        print("  Using direct connection (no proxy needed)")

    print("\n[Step 3/4] Reading sitemap.xml...")
    sitemap = os.path.join(script_dir, '..', 'sitemap.xml')
    if not os.path.exists(sitemap):
        sitemap = os.path.join(script_dir, 'sitemap.xml')
    if not os.path.exists(sitemap):
        print(f"ERROR: sitemap.xml not found!")
        sys.exit(1)

    urls = get_urls(sitemap)
    print(f"OK - Found {len(urls)} URLs")

    print(f"\n[Step 4/4] Submitting {len(urls)} URLs to Google...")
    print("-" * 60)

    success = 0
    failed = 0

    for i, url in enumerate(urls, 1):
        short = url.replace('https://osrsguru.com/', '')
        print(f"[{i:2d}/{len(urls)}] {short[:50]}")
        ok, result = submit_url(creds, url)
        if ok:
            print("         OK")
            success += 1
        else:
            print(f"         FAIL: {result}")
            failed += 1
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"DONE!  Success: {success}  |  Failed: {failed}")
    print("=" * 60)

    if success > 0:
        print(f"\n{success} URLs submitted to Google Indexing API!")
        print("Check Search Console in a few days for indexing status.")
    if failed > 0:
        print(f"\n{failed} URLs failed. Common reasons:")
        print("  - 403: URL not claimed in Search Console")
        print("  - 429: Rate limited (wait and retry)")


if __name__ == '__main__':
    main()
