#!/usr/bin/env python
"""
Google Indexing API - Submit URLs for re-indexing
Uses OAuth 2.0 Desktop App flow (not service accounts)
Optimized for users in China with proxy support.
"""
import os
import sys
import json
import time
import socket
import requests

# ========== CONFIGURATION ==========
SITEMAP_PATH = r'C:\Users\Lenovo\osrs-guide-site\sitemap.xml'
TOKEN_PATH = r'C:\Users\Lenovo\osrs-guide-site\scripts\token.json'
CLIENT_SECRET_PATH = r'C:\Users\Lenovo\osrs-guide-site\scripts\client_secret.json'
BATCH_SIZE = 10  # URLs per batch (avoid 429 rate limit)
BATCH_DELAY = 2  # seconds between batches

# Proxy settings (auto-detect or set manually)
PROXY_HOST = '127.0.0.1'
PROXY_PORTS = [7897, 7890, 10808, 10809, 8888, 9999]

# ========== PROXY DETECTION ==========
def find_proxy():
    """Auto-detect working proxy port."""
    for port in PROXY_PORTS:
        try:
            s = socket.create_connection((PROXY_HOST, port), timeout=3)
            s.close()
            proxies = {
                'http': f'http://{PROXY_HOST}:{port}',
                'https': f'http://{PROXY_HOST}:{port}',
            }
            # Test if it actually works
            r = requests.get('https://www.googleapis.com/', proxies=proxies, timeout=8)
            if r.status_code < 500:
                print(f'[OK] Proxy found: {PROXY_HOST}:{port}')
                return proxies
        except Exception:
            continue
    print('[WARN] No working proxy found, trying direct connection...')
    return None

# ========== OAUTH AUTHENTICATION ==========
def get_access_token(proxies):
    """Get OAuth access token (load from file or do browser auth)."""
    # Try loading saved token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            token_data = json.load(f)
        # Check if expired
        if token_data.get('expires_at', 0) > time.time() + 300:
            print('[OK] Using saved OAuth token')
            return token_data['access_token']
    
    # Need to do OAuth flow
    if not os.path.exists(CLIENT_SECRET_PATH):
        print('=' * 60)
        print('ERROR: client_secret.json not found!')
        print('=' * 60)
        print('Please follow these steps:')
        print('1. Go to https://console.cloud.google.com/')
        print('2. Enable "Indexing API" and "Google Search Console API"')
        print('3. Create OAuth 2.0 Client ID (Desktop app)')
        print('4. Download JSON and save as:')
        print(f'   {CLIENT_SECRET_PATH}')
        print('5. Add your email as test user in OAuth consent screen')
        print('6. Run this script again')
        print('=' * 60)
        sys.exit(1)
    
    with open(CLIENT_SECRET_PATH, 'r') as f:
        client_config = json.load(f)
    
    client_id = client_config['installed']['client_id']
    client_secret = client_config['installed']['client_secret']
    
    # Manual OAuth flow instructions
    print('=' * 60)
    print('OAuth Setup Required (one-time only)')
    print('=' * 60)
    print(f'1. Open this URL in browser:')
    print(f'   https://accounts.google.com/o/oauth2/auth?')
    print(f'   client_id={client_id}')
    print(f'   &redirect_uri=http://localhost:8888')
    print(f'   &response_type=code')
    print(f'   &scope=https://www.googleapis.com/auth/indexing')
    print(f'   &access_type=offline')
    print(f'   &prompt=consent')
    print()
    print('2. After authorization, you will be redirected to localhost')
    print('3. Copy the "code=" parameter from the URL')
    print('4. Paste it here:')
    print('=' * 60)
    
    auth_code = input('Enter authorization code: ').strip()
    
    # Exchange code for tokens
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': 'http://localhost:8888',
        'grant_type': 'authorization_code',
    }
    
    r = requests.post(token_url, data=token_data, proxies=proxies, timeout=30)
    if r.status_code != 200:
        print(f'[ERROR] Token exchange failed: {r.text}')
        sys.exit(1)
    
    tokens = r.json()
    tokens['expires_at'] = time.time() + tokens.get('expires_in', 3600)
    
    # Save token
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tokens, f)
    
    print('[OK] OAuth token saved!')
    return tokens['access_token']

# ========== URL SUBMISSION ==========
def submit_urls(access_token, proxies):
    """Submit URLs from sitemap.xml to Google Indexing API."""
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    for url_elem in root.findall('ns:url', ns):
        loc = url_elem.find('ns:loc', ns)
        if loc is not None:
            urls.append(loc.text)
    
    print(f'\n[INFO] Found {len(urls)} URLs in sitemap')
    print(f'[INFO] Submitting in batches of {BATCH_SIZE}...\n')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    api_url = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for url in batch:
            body = {
                'url': url,
                'type': 'URL_UPDATED'
            }
            
            try:
                r = requests.post(api_url, headers=headers, json=body, proxies=proxies, timeout=30)
                
                if r.status_code == 200:
                    result = r.json()
                    notify_time = result.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime', 'unknown')
                    print(f'  [OK] {url} -> indexed at {notify_time[:19] if len(notify_time) > 19 else notify_time}')
                    success_count += 1
                elif r.status_code == 403:
                    print(f'  [SKIP] {url} -> 403 (not verified in Search Console)')
                    skipped_count += 1
                elif r.status_code == 429:
                    print(f'  [RATE] {url} -> 429 rate limited, waiting 60s...')
                    time.sleep(60)
                    # Retry once
                    r = requests.post(api_url, headers=headers, json=body, proxies=proxies, timeout=30)
                    if r.status_code == 200:
                        print(f'  [OK] {url} -> indexed (retry)')
                        success_count += 1
                    else:
                        print(f'  [FAIL] {url} -> {r.status_code}')
                        error_count += 1
                else:
                    print(f'  [FAIL] {url} -> {r.status_code}: {r.text[:100]}')
                    error_count += 1
                    
            except requests.exceptions.Timeout:
                print(f'  [TIMEOUT] {url} -> request timed out')
                error_count += 1
            except Exception as e:
                print(f'  [ERROR] {url} -> {str(e)}')
                error_count += 1
        
        if i + BATCH_SIZE < len(urls):
            time.sleep(BATCH_DELAY)
    
    print(f'\n{"=" * 60}')
    print(f'RESULTS: {success_count} success, {skipped_count} skipped, {error_count} errors')
    print(f'{"=" * 60}')
    
    return success_count, skipped_count, error_count

# ========== MAIN ==========
if __name__ == '__main__':
    print('=' * 60)
    print('Google Indexing API - URL Submission Tool')
    print('=' * 60)
    
    # Step 1: Find proxy
    proxies = find_proxy()
    
    # Step 2: Get OAuth token
    access_token = get_access_token(proxies)
    
    # Step 3: Submit URLs
    submit_urls(access_token, proxies)
