#!/usr/bin/env python3
"""
Google Indexing API + Bing Webmaster API 自动提交脚本
用于向搜索引擎提交新URL或更新URL的索引请求

依赖: pip install google-auth google-api-python-client requests
"""

import json
import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

# Windows UTF-8 编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ============================================================
# 配置
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = SCRIPT_DIR / "index_config.json"

# 默认需要提交的URL（新增/更新的页面）
DEFAULT_URLS = [
    "https://osrsguru.com/guides/account-security-guide-2026.html",
    "https://osrsguru.com/guides/quest-cape-roadmap-2026.html",
    "https://osrsguru.com/guides/mid-game-money-making-2026.html",
    "https://osrsguru.com/guides/f2p-to-p2p-bond-guide-2026.html",
    "https://osrsguru.com/guides/slayer-1-99-guide-2026.html",
]


def load_config():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def submit_google(url, credentials_path):
    """
    提交单个URL到 Google Indexing API

    需要:
    - 服务账号 JSON 密钥文件路径
    - 该服务账号已在 Search Console 中添加为该站点的所有者
    """
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("❌ 缺少依赖库，请运行:")
        print("   pip install google-auth google-api-python-client")
        return False

    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/indexing"],
        )
        service = build("indexing", "v3", credentials=credentials)

        body = {
            "url": url,
            "type": "URL_UPDATED",  # 或 URL_NOTIFIED（仅通知，不请求抓取）
        }

        response = service.urlNotifications().publish(body=body).execute()
        result = response.get("urlNotificationMetadata", {})

        if result:
            notify_time = result.get("latestUpdate", {}).get("notifyTime", "")
            status = result.get("latestUpdate", {}).get("type", "UNKNOWN")
            print(f"  ✅ Google: {url}")
            print(f"     状态: {status} | 时间: {notify_time}")
            return True
        else:
            print(f"  ⚠️  Google: {url} - 响应异常: {response}")
            return False

    except json.decoder.JSONDecodeError as e:
        print(f"  ❌ Google: {url} - API返回非JSON响应（可能API未启用或权限不足）")
        return False
    except Exception as e:
        err_msg = str(e)
        if "Expecting ',' delimiter" in err_msg or "JSONDecodeError" in str(type(e)):
            print(f"  ❌ Google: {url} - API返回非JSON错误页 → 请确认已启用 Indexing API")
        else:
            print(f"  ❌ Google: {url} - {e}")
        return False


def submit_bing(urls, api_key, site_url="https://osrsguru.com"):
    """
    批量提交URL到 Bing Webmaster API

    需要:
    - Bing Webmaster Tools API Key
    - 站点已在 Bing Webmaster Tools 中验证
    """
    try:
        import requests
    except ImportError:
        print("❌ 缺少依赖库，请运行:")
        print("   pip install requests")
        return False

    endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={api_key}"

    body = {
        "siteUrl": site_url,
        "urlList": urls,
    }

    try:
        resp = requests.post(endpoint, json=body, timeout=30)
        if resp.status_code == 200:
            print(f"  ✅ Bing: 成功提交 {len(urls)} 个URL")
            return True
        elif resp.status_code == 202:
            print(f"  ⏳ Bing: {len(urls)} 个URL已接收，等待处理")
            return True
        else:
            print(f"  ❌ Bing: HTTP {resp.status_code} - {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Bing: {e}")
        return False


def submit_sitemap_ping(sitemap_url):
    """
    尝试通过 IndexNow 协议提交（Bing/Yandex 支持）
    这是 IndexNow 的替代方案
    """
    try:
        import requests
    except ImportError:
        print("❌ 需要 requests 库")
        return

    # IndexNow 协议
    indexnow_key = "81f6a2c3d4e5f6a7b8c9d0e1f2a3b4c5"  # 可自定义，需要放在站点根目录
    indexnow_endpoint = "https://api.indexnow.org/indexnow"

    # 提取站点域名
    from urllib.parse import urlparse

    site_host = urlparse(sitemap_url).netloc

    body = {
        "host": site_host,
        "key": indexnow_key,
        "keyLocation": f"https://{site_host}/{indexnow_key}.txt",
        "urlList": [],
    }

    # 注意：IndexNow 需要先将 key 文件放到站点根目录
    print(f"\n📢 IndexNow 协议说明:")
    print(f"   需将密钥文件放到: https://{site_host}/{indexnow_key}.txt")
    print(f"   文件内容: {indexnow_key}")
    print(f"   (暂时跳过 IndexNow，先用 API 路径)")


def main():
    parser = argparse.ArgumentParser(description="提交URL到 Google + Bing 搜索引擎索引")
    parser.add_argument(
        "--urls",
        nargs="*",
        help="要提交的URL列表（不指定则使用默认列表）",
    )
    parser.add_argument(
        "--sitemap",
        action="store_true",
        help="从 sitemap.xml 解析URL（优先本地文件，回退到线上）",
    )
    parser.add_argument(
        "--google-key",
        help="Google 服务账号 JSON 密钥文件路径",
        default=None,
    )
    parser.add_argument(
        "--bing-key",
        help="Bing Webmaster API Key",
        default=None,
    )
    parser.add_argument(
        "--config",
        help="显示当前配置",
        action="store_true",
    )
    parser.add_argument(
        "--dry-run",
        help="仅列出将要提交的URL，不实际提交",
        action="store_true",
    )
    args = parser.parse_args()

    config = load_config()

    # 确定密钥路径
    google_key = args.google_key or config.get("google_service_account_key")
    bing_key = args.bing_key or config.get("bing_api_key")
    site_url = config.get("site_url", "https://osrsguru.com")

    # 确定URL列表
    if args.urls:
        urls = args.urls
    elif args.sitemap:
        try:
            import requests
            from lxml import etree
            import io

            # 优先读取本地 sitemap（避免 GitHub Pages CDN 缓存延迟）
            local_sitemap = PROJECT_DIR / "sitemap.xml"
            if local_sitemap.exists():
                with open(local_sitemap, "rb") as f:
                    xml_content = f.read()
                print(f"📄 从本地 sitemap.xml 解析到 {xml_content.count(b'<loc>')} 个URL")
            else:
                sitemap_url = f"{site_url}/sitemap.xml"
                resp = requests.get(sitemap_url, timeout=30)
                xml_content = resp.content
                print(f"📄 从线上 sitemap 解析到 {xml_content.count(b'<loc>')} 个URL")

            tree = etree.fromstring(xml_content)
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = [loc.text for loc in tree.findall(".//sm:loc", ns)]
            print(f"   共 {len(urls)} 个URL")
        except ImportError:
            print("❌ 需要 lxml 库: pip install lxml requests")
            return
    else:
        urls = DEFAULT_URLS

    # 显示配置
    if args.config:
        print("=" * 60)
        print("📋 当前配置")
        print("=" * 60)
        print(f"站点URL: {site_url}")
        print(f"Google密钥: {'✅ 已配置' if google_key else '❌ 未配置'}")
        print(f"  → 路径: {google_key or 'N/A'}")
        print(f"Bing密钥: {'✅ 已配置' if bing_key else '❌ 未配置'}")
        print(f"  → Key: {'***' + bing_key[-4:] if bing_key else 'N/A'}")
        print(f"默认URL数: {len(DEFAULT_URLS)}")
        return

    # 输出计划
    print("=" * 60)
    print("🚀 搜索引擎索引提交")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"站点: {site_url}")
    print(f"待提交URL数: {len(urls)}")
    print("-" * 60)

    if args.dry_run:
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
        print(f"\n🔍 DRY RUN — 未实际提交")
        return

    # Google 提交
    if google_key and os.path.exists(google_key):
        print("\n[Google Indexing API]")
        success = 0
        fail = 0
        for i, url in enumerate(urls, 1):
            print(f"  [{i}/{len(urls)}]", end=" ")
            if submit_google(url, google_key):
                success += 1
            else:
                fail += 1
            time.sleep(1)  # 避免触发频率限制
        print(f"\n  Google 结果: ✅ {success} / ❌ {fail}")
    else:
        print("\n[Google] ⚠️ 跳过 — 未配置服务账号密钥")
        if not google_key:
            print("  请设置: python submit_index.py --google-key path/to/key.json")

    # Bing 提交
    if bing_key:
        print("\n[Bing Webmaster API]")
        submit_bing(urls, bing_key, site_url)
    else:
        print("\n[Bing] ⚠️ 跳过 — 未配置 API Key")
        print("  请设置: python submit_index.py --bing-key YOUR_API_KEY")

    # IndexNow（备选）
    submit_sitemap_ping(f"{site_url}/sitemap.xml")

    print("\n" + "=" * 60)
    print("✅ 提交完成")
    print("=" * 60)
    print("\n💡 提示:")
    print("  - Google 索引通常在几小时到几天内生效")
    print("  - 可在 Search Console 查看索引状态")
    print("  - 可用 --dry-run 先预览再执行")


if __name__ == "__main__":
    main()
