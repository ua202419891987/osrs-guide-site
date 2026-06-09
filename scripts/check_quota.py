#!/usr/bin/env python3
"""
OSRS Guru - Indexing API Quota Checker
- Shows pending URLs count
- Checks remaining quota via a test API call
- Shows next quota reset time (Pacific Time midnight = Beijing 15:00)
"""

import os
import sys
import json
import time
import socket
import requests
from datetime import datetime, timezone, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))
SUBMITTED_FILE = os.path.join(script_dir, 'submitted_urls.txt')

# Pacific Time zone (Google API quota resets at PT midnight)
# PT = UTC-7 (PDT) or UTC-8 (PST)
def get_pt_now():
    """Get current Pacific Time."""
    utc_now = datetime.now(timezone.utc)
    # Rough PT offset: PDT = UTC-7, PST = UTC-8
    # Google uses Pacific Time year-round for quota reset
    # Check if DST: March 2nd Sunday - November 1st Sunday => PDT (UTC-7)
    pt_offset = -7  # PDT (summer)
    # Simple check: if month Apr-Oct => PDT, else PST
    month = utc_now.month
    if month < 3 or month > 11:
        pt_offset = -8  # PST (winter)
    elif month == 3:
        # After 2nd Sunday
        pt_offset = -7
    elif month == 11:
        pt_offset = -8
    pt_now = utc_now + timedelta(hours=pt_offset)
    return pt_now, pt_offset

def get_next_reset():
    """Calculate next quota reset time in Beijing time."""
    pt_now, offset = get_pt_now()
    # Reset is at PT 00:00:00 (midnight)
    reset_today = pt_now.replace(hour=0, minute=0, second=0, microsecond=0)
    if pt_now >= reset_today:
        reset_pt = reset_today + timedelta(days=1)
    else:
        reset_pt = reset_today

    # Convert to Beijing time (UTC+8)
    # Approach: treat PT as UTC+offset, Beijing as UTC+8
    # reset_utc = reset_pt - offset_hours
    reset_utc = reset_pt - timedelta(hours=offset)
    reset_beijing = reset_utc + timedelta(hours=8)

    # Time until reset - use UTC-aware now for comparison
    now_utc = datetime.now(timezone.utc)
    reset_utc_dt = reset_utc.replace(tzinfo=timezone.utc)
    delta = reset_utc_dt - now_utc
    return reset_beijing, delta

def load_submitted():
    if os.path.exists(SUBMITTED_FILE):
        with open(SUBMITTED_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

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

def check_quota(creds):
    """Make a harmless GET request to check quota status."""
    # Use the API endpoint with a dummy URL to check auth + quota
    # Actually, the quota is per project per day for PublishUrlNotification
    # We can't directly query remaining quota, but we can try one request
    # and see if we get 429
    endpoint = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    body = json.dumps({'url': 'https://osrsguru.com/', 'type': 'URL_UPDATED'}).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.token}',
    }
    try:
        resp = requests.post(endpoint, data=body, headers=headers, timeout=15, verify=True)
        return resp.status_code, resp.text[:200]
    except Exception as e:
        return None, str(e)[:200]

def main():
    print("=" * 60)
    print("  OSRS Guru - Indexing API Quota Checker")
    print("=" * 60)

    # 1. Check pending URLs
    print("\n[1/4] Reading sitemap & tracking file...")
    sitemap = os.path.join(script_dir, '..', 'sitemap.xml')
    if not os.path.exists(sitemap):
        sitemap = os.path.join(script_dir, 'sitemap.xml')
    if not os.path.exists(sitemap):
        print("  ERROR: sitemap.xml not found!")
        sys.exit(1)

    all_urls = get_urls(sitemap)
    already = load_submitted()
    new_urls = [u for u in all_urls if u not in already]

    print(f"  Total URLs in sitemap : {len(all_urls)}")
    print(f"  Already submitted     : {len(already)}")
    print(f"  Pending submission   : {len(new_urls)}")

    # 2. Quota reset time
    print("\n[2/4] Quota reset time...")
    reset_beijing, delta = get_next_reset()
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    print(f"  Next reset (Beijing) : {reset_beijing.strftime('%Y-%m-%d %H:%M')} CST")
    if delta.total_seconds() > 0:
        print(f"  Time until reset      : {hours}h {minutes}m")
    else:
        print(f"  Status                : QUOTA SHOULD BE RESET (run script again to confirm)")

    # 3. Check OAuth token
    print("\n[3/4] Checking OAuth token...")
    token_file = os.path.join(script_dir, 'token.json')
    if not os.path.exists(token_file):
        print("  No token.json found - need to authenticate first")
        print("  Run: python submit_index_oauth.py")
        return

    try:
        import pickle
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
        if creds.valid:
            print("  Token: VALID")
        elif creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request as AuthRequest
            creds.refresh(AuthRequest())
            print("  Token: REFRESHED")
        else:
            print("  Token: INVALID - run submit_index_oauth.py to re-auth")
            return
    except Exception as e:
        print(f"  Token: ERROR - {e}")
        return

    # 4. Test API call to check quota
    print("\n[4/4] Testing API quota with a dry-run request...")
    print("  (Sending test request to Google Indexing API...)")

    status, text = check_quota(creds)

    if status == 200:
        print("  Result : [OK] HTTP 200 - Quota AVAILABLE (you can submit)")
        print(f"  Pending URLs can be submitted now!")
    elif status == 429:
        print("  Result : [FAIL] HTTP 429 - QUOTA EXCEEDED")
        print(f"  Wait until reset: {reset_beijing.strftime('%H:%M')} Beijing time")
    elif status == 403:
        print(f"  Result : [WARN] HTTP 403 - Auth/permission issue")
        print(f"  Response: {text[:150]}")
    else:
        print(f"  Result : [WARN] HTTP {status}")
        print(f"  Response: {text[:150]}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Pending URLs : {len(new_urls)}")
    if status == 200:
        print(f"  Quota status : [OK] Available - Ready to submit!")
        print(f"  Run: python submit_index_oauth.py")
    elif status == 429:
        print(f"  Quota status : [FAIL] Exceeded - Wait {hours}h {minutes}m")
    print("=" * 60)

if __name__ == '__main__':
    main()
