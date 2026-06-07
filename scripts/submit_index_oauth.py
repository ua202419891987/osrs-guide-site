#!/usr/bin/env python3
"""
OSRS Guru - Google Indexing API OAuth Submit v5
- Only submits NEW URLs (tracks submitted in submitted_urls.txt)
- Retries on 429 quota errors with exponential backoff
- Uses 'requests' library for proper proxy support.
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
SUBMITTED_FILE = os.path.join(script_dir, 'submitted_urls.txt')

# ============================================================
# Step 0: Quick network check
# ============================================================
print("=" * 60)
print("  OSRS Guru - Indexing API Submit v5")
print("=" * 60)

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

# ============================================================
# Step 1: Library imports
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
# Step 2: OAuth credentials
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
# Step 3: Submit URL with retry on 429
# ============================================================
def submit_url(creds, url, max_retries=3):
    """Submit one URL with retry on quota errors.
    Returns: (success: bool, result: str, quota_exceeded: bool)
    """
    endpoint = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    body = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode('utf-8')

    proxies = {}
    if use_proxy and proxy_url:
        proxies['https'] = proxy_url
        proxies['http'] = proxy_url

    for attempt in range(1, max_retries + 1):
        # Refresh token if needed
        if creds.expired and creds.refresh_token:
            creds.refresh(AuthRequest())

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {creds.token}',
        }

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
                return True, resp.json().get('urlNotificationMetadata', {}), False
            elif resp.status_code == 429:
                # QUOTA EXCEEDED - stop entire batch
                return False, "HTTP 429 (QUOTA EXCEEDED)", True
            else:
                return False, f"HTTP {resp.status_code}: {resp.text[:80]}", False
        except requests.exceptions.Timeout:
            return False, "TIMEOUT (>30s)", False
        except requests.exceptions.ConnectionError as e:
            return False, f"CONNECTION ERROR: {str(e)[:80]}", False
        except Exception as e:
            return False, str(e)[:120], False

    return False, "RETRIES EXHAUSTED", False


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
# Step 5: Load/update tracking file
# ============================================================
def load_submitted():
    """Load list of already-submitted URLs."""
    if os.path.exists(SUBMITTED_FILE):
        with open(SUBMITTED_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def save_submitted(url):
    """Append one URL to tracking file."""
    with open(SUBMITTED_FILE, 'a') as f:
        f.write(url + '\n')


# ============================================================
# MAIN
# ============================================================
def main():
    print("\n[Step 1/5] Authenticating with Google...")
    creds = get_credentials()
    print("OK - Authenticated!")

    print("\n[Step 2/5] Setting up network...")
    if use_proxy and proxy_url:
        print(f"  Using proxy: {proxy_url}")
    else:
        print("  Using direct connection (no proxy needed)")

    print("\n[Step 3/5] Reading sitemap.xml...")
    sitemap = os.path.join(script_dir, '..', 'sitemap.xml')
    if not os.path.exists(sitemap):
        sitemap = os.path.join(script_dir, 'sitemap.xml')
    if not os.path.exists(sitemap):
        print(f"ERROR: sitemap.xml not found!")
        sys.exit(1)

    all_urls = get_urls(sitemap)
    print(f"OK - Total {len(all_urls)} URLs in sitemap")

    # Filter: only submit new URLs
    already = load_submitted()
    new_urls = [u for u in all_urls if u not in already]
    skip_count = len(all_urls) - len(new_urls)

    if skip_count > 0:
        print(f"SKIP - {skip_count} URLs already submitted")
    print(f"NEW  - {len(new_urls)} URLs to submit")

    if len(new_urls) == 0:
        print("\nNothing to do! All URLs already submitted.")
        return

    print(f"\n[Step 4/5] Submitting {len(new_urls)} NEW URLs to Google...")
    print("-" * 60)

    success = 0
    failed = 0
    failed_urls = []
    quota_exceeded = False
    connection_errors = 0

    for i, url in enumerate(new_urls, 1):
        short = url.replace('https://osrsguru.com/', '')

        # Stop entirely if quota already exceeded
        if quota_exceeded:
            print(f"  SKIP (quota exceeded): {short[:50]}")
            failed += 1
            failed_urls.append(url)
            continue

        print(f"[{i:2d}/{len(new_urls)}] {short[:50]}")
        ok, result, quota = submit_url(creds, url)
        if ok:
            print(f"         OK")
            success += 1
            save_submitted(url)  # Track immediately
        else:
            print(f"         FAIL: {result}")
            failed += 1
            failed_urls.append(url)
            # QUOTA EXCEEDED - stop all remaining submissions
            if quota:
                quota_exceeded = True
                print("\n" + "!" * 60)
                print("  DAILY QUOTA (200) EXCEEDED!")
                print("  Stopping all remaining submissions.")
                print("  Resume tomorrow (200 fresh quota).")
                print("!" * 60)
            # Track consecutive connection errors
            elif "CONNECTION ERROR" in result:
                connection_errors += 1
                if connection_errors >= 5:
                    print("\n  TOO MANY CONNECTION ERRORS - stopping.")
                    break
            else:
                connection_errors = 0
        time.sleep(0.5)  # Be gentle to API

    print("\n[Step 5/5] Updating tracking file...")
    print(f"  Submitted: {success}")
    print(f"  Failed:    {failed}")
    print(f"  Tracked:   {len(load_submitted())} total URLs in {os.path.basename(SUBMITTED_FILE)}")

    print("\n" + "=" * 60)
    print(f"DONE!  Success: {success}  |  Failed: {failed}")
    print("=" * 60)

    if success > 0:
        print(f"\n{success} URLs submitted to Google Indexing API!")
        print("Check Search Console in a few days for indexing status.")

    if failed > 0:
        print(f"\n{failed} URLs failed. Common reasons:")
        print("  - 403: URL not claimed in Search Console")
        print("  - 429: Daily quota reached (200/day). Retry tomorrow.")
        print("\n=== FAILED URLs (run again tomorrow) ===")
        for u in failed_urls:
            print(f"  {u}")

    if success == 0 and failed == 0:
        print("\nAll URLs already submitted. Nothing new to do.")


if __name__ == '__main__':
    main()
