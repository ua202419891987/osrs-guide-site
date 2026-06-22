#!/usr/bin/env python
"""
Google Indexing API - Submit URLs for re-indexing
Uses OAuth 2.0 Desktop App flow with AUTO browser authorization.
Optimized for users in China with proxy support.
"""
import os
import sys
import json
import time
import socket
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# ========== CONFIGURATION ==========
SITEMAP_PATH = r'C:\Users\Lenovo\osrs-guide-site\sitemap.xml'
TOKEN_PATH = r'C:\Users\Lenovo\osrs-guide-site\scripts\token.json'
CLIENT_SECRET_PATH = r'C:\Users\Lenovo\osrs-guide-site\scripts\client_secret.json'
REDIRECT_URI = 'http://localhost:8888'
REDIRECT_PORT = 8888
BATCH_SIZE = 10
BATCH_DELAY = 2

# Proxy settings (auto-detect or set manually)
PROXY_HOST = '127.0.0.1'
PROXY_PORTS = [7897, 7890, 10808, 10809, 8888, 9999]

# Global var for OAuth callback result
oauth_code = None
oauth_error = None
server_started = threading.Event()

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
            r = requests.get('https://www.googleapis.com/', proxies=proxies, timeout=8)
            if r.status_code < 500:
                print(f'[OK] Proxy found: {PROXY_HOST}:{port}')
                return proxies
        except Exception:
            continue
    print('[WARN] No working proxy found, trying direct connection...')
    return None

# ========== OAUTH CALLBACK SERVER ==========
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global oauth_code, oauth_error
        
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        if 'code' in params:
            oauth_code = params['code'][0]
            html = '<html><body><h2>Authorization Successful!</h2><p>You may close this window now.</p></body></html>'
        elif 'error' in params:
            oauth_error = params.get('error_description', params['error'])[0]
            html = f'<html><body><h2>Authorization Failed</h2><p>{oauth_error}</p></body></html>'
        else:
            html = '<html><body><h2>Waiting for authorization...</h2></body></html>'
        
        self.wfile.write(html.encode('utf-8'))
        
        # Signal to stop server
        threading.Thread(target=self.server.shutdown).start()
    
    def log_message(self, format, *args):
        pass  # Suppress HTTP server logs

def start_oauth_server():
    """Start local HTTP server and wait for OAuth callback."""
    global oauth_code, oauth_error
    
    oauth_code = None
    oauth_error = None
    
    server = HTTPServer(('localhost', REDIRECT_PORT), OAuthCallbackHandler)
    server.timeout = 120  # 2 minute timeout
    
    print('[INFO] Starting OAuth callback server on port 8888...')
    server_started.set()
    
    server.handle_request()  # Handle one request and return
    
    if oauth_code:
        print('[OK] Authorization code received!')
        return oauth_code
    elif oauth_error:
        raise Exception(f'OAuth error: {oauth_error}')
    else:
        raise Exception('OAuth timed out - no authorization code received')

# ========== OAUTH AUTHENTICATION ==========
def get_access_token(proxies):
    """Get OAuth access token (auto browser auth)."""
    # Try loading saved token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            token_data = json.load(f)
        if token_data.get('expires_at', 0) > time.time() + 300:
            print('[OK] Using saved OAuth token')
            return token_data['access_token']
        else:
            print('[INFO] Saved token expired, refreshing...')
    
    if not os.path.exists(CLIENT_SECRET_PATH):
        print('=' * 60)
        print('ERROR: client_secret.json not found!')
        print('=' * 60)
        print(f'Please place client_secret.json at:')
        print(f'  {CLIENT_SECRET_PATH}')
        print('=' * 60)
        sys.exit(1)
    
    with open(CLIENT_SECRET_PATH, 'r') as f:
        client_config = json.load(f)
    
    client_id = client_config['installed']['client_id']
    
    # Build auth URL
    auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        f'client_id={client_id}'
        f'&redirect_uri={REDIRECT_URI}'
        '&response_type=code'
        '&scope=https://www.googleapis.com/auth/indexing'
        '&access_type=offline'
        '&prompt=consent'
    )
    
    print('=' * 60)
    print('Opening browser for Google authorization...')
    print('Please allow access when prompted.')
    print('=' * 60)
    
    # Start OAuth server in background thread
    server_thread = threading.Thread(target=start_oauth_server, daemon=True)
    server_thread.start()
    
    # Wait for server to be ready
    server_started.wait(timeout=5)
    time.sleep(0.5)
    
    # Auto-open browser
    print('[INFO] Opening browser...')
    webbrowser.open(auth_url)
    
    # Wait for server to complete (max 130 seconds)
    server_thread.join(timeout=130)
    
    if oauth_code is None:
        print('[ERROR] No authorization code received. Please try again.')
        sys.exit(1)
    
    # Exchange code for tokens
    client_secret = client_config['installed']['client_secret']
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': oauth_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    print('[INFO] Exchanging code for access token...')
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
    
    # Step 2: Get OAuth token (auto browser flow)
    access_token = get_access_token(proxies)
    
    # Step 3: Submit URLs
    submit_urls(access_token, proxies)
