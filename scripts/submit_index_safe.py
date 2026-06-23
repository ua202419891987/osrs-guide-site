#!/usr/bin/env python3
"""
Google Indexing API - Safe Submit Script
预检 + 自动刷新 Token + 配额检查 + 批量提交
确保每次运行都成功，不浪费配额
"""

import json
import time
import requests
import re
import sys
import os

# ============ 配置 ============
CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")
SUBMITTED_FILE = os.path.join(os.path.dirname(__file__), "submitted_urls.txt")
SITEMAP_FILE = r"C:\Users\Lenovo\osrs-guide-site\sitemap.xml"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
BATCH_SIZE = 10
BATCH_DELAY = 2  # 秒
TOKEN_REFRESH_MARGIN = 600  # Token 剩余 10 分钟就刷新
# ==================================


def log(msg, level="INFO"):
    """带时间戳的日志"""
    timestamp = time.strftime("%H:%M:%S")
    prefix = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌"}[level]
    print(f"[{timestamp}] {prefix} {msg}")


def load_credentials():
    """加载 OAuth 凭据"""
    with open(CLIENT_SECRET_FILE, "r") as f:
        return json.load(f)


def load_token():
    """加载 Token"""
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)


def save_token(token):
    """保存 Token"""
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f)
    log(f"Token 已保存（有效期至 {time.strftime('%H:%M:%S', time.localtime(token['expires_at']))}）", "OK")


def is_token_valid(token):
    """检查 Token 是否有效（剩余时间 > 刷新边界）"""
    if not token:
        return False
    expires_at = token.get("expires_at", 0)
    remaining = expires_at - time.time()
    return remaining > TOKEN_REFRESH_MARGIN


def refresh_token(credentials, token):
    """刷新 Token"""
    log("Token 即将过期，正在刷新...", "WARN")
    client_id = credentials["installed"]["client_id"]
    client_secret = credentials["installed"]["client_secret"]
    refresh_token = token.get("refresh_token")

    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        proxies=PROXY,
        timeout=30,
    )

    if r.status_code != 200:
        log(f"刷新失败: {r.text}", "ERROR")
        return None

    new_tokens = r.json()
    new_tokens["refresh_token"] = refresh_token  # 保留 refresh_token
    new_tokens["expires_at"] = time.time() + new_tokens.get("expires_in", 3600)
    return new_tokens


def ensure_valid_token():
    """确保 Token 有效，无效则刷新"""
    log("检查 Token 状态...")
    credentials = load_credentials()
    token = load_token()

    if not token or not is_token_valid(token):
        if token:
            log("Token 即将过期或已过期，正在刷新...", "WARN")
            new_token = refresh_token(credentials, token)
            if new_token:
                save_token(new_token)
                token = new_token
            else:
                log("自动刷新失败，需要重新授权", "ERROR")
                return None
        else:
            log("Token 不存在，需要授权", "ERROR")
            return None
    else:
        remaining = token["expires_at"] - time.time()
        log(f"Token 有效（剩余 {int(remaining / 60)} 分钟）", "OK")

    return token


def check_quota(token):
    """检查今日配额（提交 1 个测试 URL）"""
    log("检查今日配额...")
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json",
    }
    body = {"url": "https://osrsguru.com/", "type": "URL_UPDATED"}

    r = requests.post(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        headers=headers,
        json=body,
        proxies=PROXY,
        timeout=30,
    )

    if r.status_code == 200:
        log("配额正常（200 次/天）", "OK")
        return True
    elif r.status_code == 429:
        log("今日配额已耗尽（429）", "ERROR")
        reset_time = time.strftime("%Y-%m-%d 08:00:00", time.localtime(time.time() + 3600 * 2))
        log(f"配额将在（北京时间）{reset_time} 重置", "INFO")
        return False
    else:
        log(f"配额检查失败: {r.status_code} {r.text[:100]}", "ERROR")
        return False


def parse_sitemap():
    """解析 sitemap.xml"""
    log("解析 sitemap.xml...")
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    urls = re.findall(r"<loc>([^<]+)</loc>", content)
    log(f"找到 {len(urls)} 个 URL", "OK")
    return urls


def load_submitted():
    """加载已提交的 URL"""
    if not os.path.exists(SUBMITTED_FILE):
        return set()
    with open(SUBMITTED_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())


def submit_urls(token, urls_to_submit):
    """批量提交 URL"""
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json",
    }
    api_url = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    success = skipped = error = 0
    log(f"开始提交 {len(urls_to_submit)} 个 URL...", "INFO")

    for i, url in enumerate(urls_to_submit):
        # 每 10 个检查一次 Token 是否快过期
        if i % 10 == 0:
            token = ensure_valid_token()
            if not token:
                log("Token 失效且无法刷新，停止提交", "ERROR")
                break
            headers["Authorization"] = f"Bearer {token['access_token']}"

        body = {"url": url, "type": "URL_UPDATED"}
        try:
            r = requests.post(api_url, headers=headers, json=body, proxies=PROXY, timeout=30)

            if r.status_code == 200:
                success += 1
                with open(SUBMITTED_FILE, "a") as f:
                    f.write(url + "\n")
                if (i + 1) % 10 == 0:
                    log(f"进度: {i + 1}/{len(urls_to_submit)} (成功 {success})", "INFO")

            elif r.status_code == 429:
                log(f"配额耗尽！已提交 {success} 个", "ERROR")
                break

            elif r.status_code == 403:
                skipped += 1
                # 403 通常是已索引，跳过

            else:
                error += 1
                log(f"失败: {url[:50]}... -> {r.status_code}", "WARN")

        except Exception as e:
            error += 1
            log(f"异常: {url[:50]}... -> {e}", "WARN")

        # 每批间隔
        if (i + 1) % BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY)

    return success, skipped, error


def main():
    log("=" * 50, "INFO")
    log("Google Indexing API - 安全提交脚本", "INFO")
    log("=" * 50, "INFO")

    # 第 1 步：确保 Token 有效
    token = ensure_valid_token()
    if not token:
        log("无法获取有效 Token，请运行 submit_index_oauth.py 重新授权", "ERROR")
        sys.exit(1)

    # 第 2 步：检查配额
    if not check_quota(token):
        log("配额检查失败，停止提交", "ERROR")
        sys.exit(1)

    # 第 3 步：解析 sitemap + 已提交列表
    all_urls = parse_sitemap()
    submitted = load_submitted()
    unsubmitted = [u for u in all_urls if u not in submitted]

    log(f"已提交: {len(submitted)} | 待提交: {len(unsubmitted)}", "INFO")

    if not unsubmitted:
        log("所有 URL 已提交完毕！", "OK")
        sys.exit(0)

    # 第 4 步：提交
    log("=" * 50, "INFO")
    success, skipped, error = submit_urls(token, unsubmitted)

    # 第 5 步：结果统计
    log("=" * 50, "INFO")
    log(f"提交完成！", "INFO")
    log(f"  成功: {success}", "OK")
    log(f"  跳过: {skipped}", "INFO")
    log(f"  失败: {error}", "WARN")
    log(f"  总计: {len(submitted) + success}/{len(all_urls)}", "INFO")
    log("=" * 50, "INFO")


if __name__ == "__main__":
    main()
