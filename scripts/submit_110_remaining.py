#!/usr/bin/env python3
"""
Google Indexing API — 提交剩余110篇URL（排除10篇试运行）
基于 2026-06-23 失败报告，排除 Viggora/Training/Hunter 系列
"""
import os, sys, json, time, socket, webbrowser, threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# ========== CONFIG ==========
CLIENT_SECRET_PATH = Path(__file__).parent / "client_secret.json"
TOKEN_PATH = Path(__file__).parent / "token.json"
REDIRECT_URI = 'http://localhost:8888'
REDIRECT_PORT = 8888
BATCH_SIZE = 10
BATCH_DELAY = 2
PROXY_HOST = '127.0.0.1'
PROXY_PORTS = [7897, 7890, 10808, 10809, 8888, 9999]
MAX_PER_RUN = 200

# ========== 110 URLs (120失败 - 10试运行) ==========
URLS = [
    "https://osrsguru.com/guides/osrs-efficient-training-routes-beginners-2026.html",
    "https://osrsguru.com/guides/osrs-fighter-torso-barbarian-assault-guide-2026.html",
    "https://osrsguru.com/guides/osrs-fire-cape-jad-guide-2026.html",
    "https://osrsguru.com/guides/osrs-fire-cape-to-infernal-progression-2026.html",
    "https://osrsguru.com/guides/osrs-first-100m-gp-mid-level-2026.html",
    "https://osrsguru.com/guides/osrs-gauntlet-meta-changes-2026.html",
    "https://osrsguru.com/guides/osrs-gear-upgrade-priority-order-2026.html",
    "https://osrsguru.com/guides/osrs-goraik-quest-guide-2026.html",
    "https://osrsguru.com/guides/osrs-goraik-rewards-worth-it-2026.html",
    "https://osrsguru.com/guides/osrs-guardians-of-the-rift-guide-2026.html",
    "https://osrsguru.com/guides/osrs-herb-run-mastery-guide-2026.html",
    "https://osrsguru.com/guides/osrs-khopesh-guide-2026.html",
    "https://osrsguru.com/guides/osrs-khopesh-vs-alternative-weapons-2026.html",
    "https://osrsguru.com/guides/osrs-maxing-99-order-guide-2026.html",
    "https://osrsguru.com/guides/osrs-mid-level-bossing-ladder-2026.html",
    "https://osrsguru.com/guides/osrs-mid-to-high-progression-roadmap-2026.html",
    "https://osrsguru.com/guides/osrs-money-making-tier-list-2026.html",
    "https://osrsguru.com/guides/osrs-nex-guide-2026.html",
    "https://osrsguru.com/guides/osrs-nightmare-phosanis-guide-2026.html",
    "https://osrsguru.com/guides/osrs-optimal-leveling-guide-2026.html",
    "https://osrsguru.com/guides/osrs-pest-control-void-guide-2026.html",
    "https://osrsguru.com/guides/osrs-phantom-muspah-guide-2026.html",
    "https://osrsguru.com/guides/osrs-poh-optimal-layout-guide-2026.html",
    "https://osrsguru.com/guides/osrs-raid-entry-requirements-2026.html",
    "https://osrsguru.com/guides/osrs-royal-titans-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-1-99-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-afk-training-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-money-making-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-ship-crew-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sailing-wyrmscraig-guide-2026.html",
    "https://osrsguru.com/guides/osrs-skills-progression-path-2026.html",
    "https://osrsguru.com/guides/osrs-slayer-70-to-95-money-makers-2026.html",
    "https://osrsguru.com/guides/osrs-slayer-block-skip-list-2026.html",
    "https://osrsguru.com/guides/osrs-summer-sweep-up-2026-account-guide.html",
    "https://osrsguru.com/guides/osrs-summer-sweep-up-2026-guide.html",
    "https://osrsguru.com/guides/osrs-tempoross-guide-2026.html",
    "https://osrsguru.com/guides/osrs-theatre-of-blood-guide-2026.html",
    "https://osrsguru.com/guides/osrs-toa-solo-beginner-guide-2026.html",
    "https://osrsguru.com/guides/osrs-wintertodt-complete-guide-2026.html",
    "https://osrsguru.com/zh/index.html",
    "https://osrsguru.com/zh/money-making.html",
    "https://osrsguru.com/zh/skill-training.html",
    "https://osrsguru.com/zh/quest-guides.html",
    "https://osrsguru.com/zh/boss-guides.html",
    "https://osrsguru.com/guides/osrs-kalphite-queen-kq-beginner-guide-2026.html",
    "https://osrsguru.com/guides/osrs-runelite-setup-guide-2026.html",
    "https://osrsguru.com/guides/osrs-range-training-1-99-guide-2026.html",
    "https://osrsguru.com/guides/osrs-cerberus-boss-guide-2026.html",
    "https://osrsguru.com/guides/osrs-sarachnis-solo-guide-2026.html",
    "https://osrsguru.com/guides/osrs-mobile-membership-guide-2026.html",
    "https://osrsguru.com/guides/osrs-regional-worlds-guide-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-beginner-complete-guide-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-beginner-fast-track-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-mid-game-guide-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-mid-game-optimization-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-endgame-guide-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-max-account-2026.html",
    "https://osrsguru.com/guides/osrs-money-making-summer-sweep-up-2026.html",
    "https://osrsguru.com/guides/osrs-money-making-under-1m-investment-2026.html",
    "https://osrsguru.com/guides/osrs-slayer-beginner-first-master-guide-2026.html",
    "https://osrsguru.com/guides/osrs-slayer-low-level-money-makers-2026.html",
    "https://osrsguru.com/guides/osrs-combat-achievements-easy-walkthrough-2026.html",
    "https://osrsguru.com/guides/osrs-ghommal-hilt-fast-guide-2026.html",
    "https://osrsguru.com/guides/osrs-first-boss-progression-roadmap-2026.html",
    "https://osrsguru.com/guides/osrs-obor-bryophyta-f2p-boss-guide-2026.html",
    "https://osrsguru.com/guides/osrs-returning-player-catch-up-guide-2026.html",
    "https://osrsguru.com/guides/osrs-returning-player-fast-track-2026.html",
    "https://osrsguru.com/guides/osrs-diary-priority-order-beginner-2026.html",
    "https://osrsguru.com/guides/osrs-diary-easy-medium-complete-guide-2026.html",
    "https://osrsguru.com/guides/osrs-skill-training-after-sweep-up-2026.html",
    "https://osrsguru.com/guides/osrs-top-10-skills-to-train-first-2026.html",
    "https://osrsguru.com/guides/osrs-blood-moon-rises-prep-checklist-detailed-2026.html",
    "https://osrsguru.com/guides/osrs-best-quests-per-skill-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-coop-multiplayer-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-money-farming-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-meta-build-tier-list-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-endgame-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-pvp-arena-guide-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-hidden-secrets-easter-eggs-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-best-settings-performance-2026.html",
    "https://osrsguru.com/guides/crimson-desert/crimson-desert-patch-notes-analysis-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-coop-multiplayer-guide-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-resource-farming-guide-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-meta-build-tier-list-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-endgame-guide-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-ship-pvp-combat-guide-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-treasure-map-secrets-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-performance-optimization-2026.html",
    "https://osrsguru.com/guides/windrose/windrose-early-access-update-guide-2026.html",
    "https://osrsguru.com/guides/osrs-slayer-money-making-guide-2026.html",
    "https://osrsguru.com/guides/osrs-boss-profit-comparison-2026.html",
    "https://osrsguru.com/guides/osrs-flipping-guide-beginners-2026.html",
    "https://osrsguru.com/guides/osrs-mid-game-money-making-roadmap-2026.html",
    "https://osrsguru.com/guides/osrs-afk-money-making-ultimate-guide-2026.html",
    "https://osrsguru.com/guides/osrs-daily-weekly-money-routine-2026.html",
    "https://osrsguru.com/guides/osrs-quest-unlocked-money-methods-2026.html",
    "https://osrsguru.com/guides/osrs-wilderness-money-making-2026.html",
    "https://osrsguru.com/guides/osrs-ironman-p2p-money-making-2026.html",
    "https://osrsguru.com/guides/osrs-skilling-money-post-sailing-2026.html",
    "https://osrsguru.com/guides/osrs-combat-money-making-non-boss-2026.html",
    "https://osrsguru.com/guides/osrs-how-to-spend-gp-wisely-2026.html",
    "https://osrsguru.com/guides/osrs-f2p-to-member-first-10-things-2026.html",
    "https://osrsguru.com/guides/osrs-f2p-money-making-first-bond-2026.html",
    "https://osrsguru.com/guides/osrs-f2p-quests-before-membership-2026.html",
    "https://osrsguru.com/guides/osrs-cheapest-membership-2026.html",
    "https://osrsguru.com/guides/osrs-cancel-membership-refund-2026.html",
    "https://osrsguru.com/guides/osrs-members-exclusive-skills-worth-it-2026.html",
    "https://osrsguru.com/guides/osrs-members-vs-f2p-comparison-2026.html",
    "https://osrsguru.com/guides/osrs-bond-farming-free-membership-2026.html",
    "https://osrsguru.com/guides/osrs-ironman-membership-guide-2026.html",
]

# 以下10篇排除不推送（Viggora/Training/Hunter 试运行）:
# - osrs-viggora-guide-2026.html
# - osrs-viggora-chainmace-guide-2026.html
# - osrs-curse-of-the-empty-lord-quest-2026.html
# - osrs-training-guide-complete-2026.html
# - osrs-fastest-leveling-guide-2026.html
# - osrs-leveling-milestones-guide-2026.html
# - osrs-f2p-leveling-guide-2026.html
# - osrs-1-99-hunter-guide-2026.html
# - osrs-fastest-hunter-training-2026.html
# - osrs-best-money-making-methods-2026.html

# ========== OAUTH CALLBACK SERVER ==========
oauth_code = None
oauth_error = None
server_started = threading.Event()

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
            html = '<html><body><h2>✅ 授权成功！</h2><p>可以关闭此窗口了。</p></body></html>'
        elif 'error' in params:
            oauth_error = params.get('error_description', params['error'])[0]
            html = f'<html><body><h2>❌ 授权失败</h2><p>{oauth_error}</p></body></html>'
        else:
            html = '<html><body><h2>等待授权...</h2></body></html>'
        self.wfile.write(html.encode('utf-8'))
        threading.Thread(target=self.server.shutdown).start()
    def log_message(self, format, *args):
        pass

def find_proxy():
    for port in PROXY_PORTS:
        try:
            s = socket.create_connection((PROXY_HOST, port), timeout=3)
            s.close()
            proxies = {'http': f'http://{PROXY_HOST}:{port}', 'https': f'http://{PROXY_HOST}:{port}'}
            r = requests.get('https://www.googleapis.com/', proxies=proxies, timeout=8)
            if r.status_code < 500:
                print(f'[✓] 代理找到: {PROXY_HOST}:{port}')
                return proxies
        except Exception:
            continue
    print('[⚠] 未找到代理，尝试直连...')
    return None

def get_access_token(proxies):
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, 'r') as f:
            td = json.load(f)
        if td.get('expires_at', 0) > time.time() + 300:
            print('[✓] 使用已保存的 OAuth token')
            return td['access_token']
        else:
            print('[i] 已保存的 token 过期，重新授权...')

    if not CLIENT_SECRET_PATH.exists():
        print(f'\n❌ 找不到: {CLIENT_SECRET_PATH}')
        print('请将 client_secret.json 放到 scripts/ 目录下')
        sys.exit(1)

    with open(CLIENT_SECRET_PATH, 'r') as f:
        cc = json.load(f)
    client_id = cc['installed']['client_id']
    client_secret = cc['installed']['client_secret']

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
    print('正在打开浏览器进行 Google 授权...')
    print('请在弹出窗口中点击"允许"')
    print('=' * 60)

    st = threading.Thread(target=lambda: (
        server_started.set(),
        HTTPServer(('localhost', REDIRECT_PORT), OAuthCallbackHandler).handle_request()
    ), daemon=True)
    st.start()
    server_started.wait(timeout=5)
    time.sleep(0.5)
    webbrowser.open(auth_url)
    st.join(timeout=130)

    if oauth_code is None:
        print('❌ 未收到授权码，请重试')
        sys.exit(1)

    print('[i] 正在用授权码换取 access token...')
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': client_id, 'client_secret': client_secret,
        'code': oauth_code, 'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }, proxies=proxies, timeout=30)
    if r.status_code != 200:
        print(f'❌ Token 交换失败: {r.text}')
        sys.exit(1)

    tokens = r.json()
    tokens['expires_at'] = time.time() + tokens.get('expires_in', 3600)
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tokens, f)
    print('[✓] OAuth token 已保存！')
    return tokens['access_token']

def main():
    print('=' * 60)
    print('  Google Indexing API — 110篇 URL 批量提交')
    print(f'  总 URL 数: {len(URLS)}')
    print(f'  每日配额: {MAX_PER_RUN}')
    print('=' * 60)

    proxies = find_proxy()
    access_token = get_access_token(proxies)

    api_url = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

    success, failed_403, failed_other = 0, 0, 0
    submitted_file = Path(__file__).parent / "submitted_110.txt"

    print(f'\n开始提交 {min(len(URLS), MAX_PER_RUN)} 篇...\n')

    for i, url in enumerate(URLS[:MAX_PER_RUN]):
        payload = json.dumps({'url': url, 'type': 'URL_UPDATED'})
        short = url.replace('https://osrsguru.com/', '')
        prefix = f'[{i+1:3d}/{min(len(URLS), MAX_PER_RUN)}]'

        try:
            r = requests.post(api_url, headers=headers, data=payload, proxies=proxies, timeout=30)
            if r.status_code == 200:
                success += 1
                print(f'{prefix} ✅ {short}')
                with open(submitted_file, 'a') as f:
                    f.write(url + '\n')
            elif r.status_code == 403:
                failed_403 += 1
                print(f'{prefix} ⏭ 403 {short}')
            elif r.status_code == 429:
                failed_other += 1
                print(f'{prefix} 🚨 429 配额用完！')
                print('\n⚠️ 每日配额已用完，剩余 URL 下次继续')
                break
            else:
                failed_other += 1
                print(f'{prefix} ❌ {r.status_code} {short}')
        except Exception as e:
            failed_other += 1
            print(f'{prefix} ⚡ {type(e).__name__}: {str(e)[:50]}')

        time.sleep(0.6)

    print(f'\n{"=" * 60}')
    print(f'  完成！✅ 成功: {success}  ⏭ 跳过(403): {failed_403}  ❌ 失败: {failed_other}')
    print(f'  剩余未提交: {max(0, len(URLS) - success - failed_403 - failed_other)}')
    print(f'{"=" * 60}')

if __name__ == '__main__':
    main()
