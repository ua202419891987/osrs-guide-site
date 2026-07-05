# -*- coding: utf-8 -*-
"""
Google Search Console 排名查询工具
查询 osrsguru.com 最近 7 天的谷歌搜索排名数据
显示哪些页面排名靠前、关键词表现、位置和点击量

用法: python scripts/check_ranking.py
"""

import os
import sys
import json
import datetime

import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# --- 配置 ---
SITE_URL = "sc_domain:osrsguru.com"  # 或 "https://osrsguru.com/"
DAYS_BACK = 7          # 查询最近几天
TOP_RESULTS = 30       # 显示前多少条

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(SCRIPT_DIR, "client_secret.json")
# 使用 Search Console 专用的 token 文件（与 GA4 的区分开）
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token_sc.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "..", "ranking_report.txt")

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# --- 代理配置（根据你的 Clash 端口调整）---
HTTP_PROXY = "http://127.0.0.1:7897"
HTTPS_PROXY = "http://127.0.0.1:7897"


def setup_proxy():
    """设置代理环境变量"""
    os.environ['HTTP_PROXY'] = HTTP_PROXY
    os.environ['HTTPS_PROXY'] = HTTPS_PROXY
    print(f"[代理] HTTP_PROXY={HTTP_PROXY}")


def get_auth():
    """获取或刷新 OAuth 凭证"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[信息] 令牌已过期，尝试刷新...")
            try:
                creds.refresh(Request())
                print("[OK] 令牌刷新成功")
            except Exception as e:
                print(f"[错误] 令牌刷新失败: {e}")
                creds = None

        if not creds or not creds.valid:
            print("\n" + "=" * 60)
            print("  需要 Google 账号授权")
            print("  浏览器将自动打开，请登录关联了 Search Console 的 Google 账号")
            print("  (如果浏览器没打开，请手动复制 CMD 里的链接)")
            print("=" * 60 + "\n")

            flow = InstalledAppFlow.from_client_secrets_file(
                SECRET_FILE, SCOPES,
                redirect_uri="http://localhost:8080/"
            )
            creds = flow.run_local_server(
                port=8080,
                host="localhost",
                authorization_prompt_message="授权链接：{url}",
                success_message="授权完成，可以关闭此窗口。"
            )

        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print(f"[OK] 令牌已保存 -> {TOKEN_FILE}")

    return creds


def query_search_console(creds, start_date, end_date, row_limit=25):
    """
    使用 requests 直接调用 Search Console API（带显式代理）
    会尝试 domain property 和 url prefix property 两种格式
    """
    # 检查 token 是否过期，过期则刷新
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            print("[OK] 令牌自动刷新")
        except Exception as e:
            print(f"[错误] 刷新失败: {e}")

    access_token = creds.token

    # 尝试两种 site property 格式
    import urllib.parse
    candidates = [
        "sc-domain:osrsguru.com",
        "https://osrsguru.com/",
        "https://www.osrsguru.com/"
    ]

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    body = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page', 'query'],
        'rowLimit': row_limit,
        'orderBy': [
            {'fieldName': 'impressions', 'sortOrder': 'DESC'}
        ],
        'dataState': 'final'
    }

    proxies = {
        'http': HTTP_PROXY,
        'https': HTTPS_PROXY
    }

    last_error = None
    for site_url in candidates:
        encoded_site = urllib.parse.quote(site_url, safe='')
        url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"

        try:
            print(f"[请求] 尝试 siteUrl: {site_url}")
            r = requests.post(url, headers=headers, json=body, proxies=proxies, timeout=30)
            r.raise_for_status()
            print(f"[OK] siteUrl 成功: {site_url}")
            return r.json().get('rows', [])
        except requests.exceptions.HTTPError as e:
            last_error = e
            error_text = e.response.text
            print(f"[尝试失败] {site_url} -> {error_text[:200]}")
            # 如果是 403/404 说明 property 不存在，继续试下一个
            # 如果是 400 且与 property 格式有关，也继续试
            if e.response.status_code == 404:
                continue
            # 400 可能有很多种原因，如果是因为 siteUrl 不存在，继续试下一个
            if e.response.status_code == 400 and 'siteUrl' in error_text:
                continue
        except requests.exceptions.ProxyError as e:
            print(f"[错误] 代理连接失败: {e}")
            print("[提示] 请检查 HTTP_PROXY 端口是否和你 Clash 实际端口一致")
            return []
        except requests.exceptions.Timeout as e:
            print(f"[错误] 请求超时: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[错误] 请求失败: {e}")
            return []

    print(f"\n[错误] 所有 siteUrl 格式都失败")
    if last_error and hasattr(last_error, 'response'):
        print(f"[最后错误] {last_error.response.text[:500]}")
    print("\n可能原因：")
    print("1. 该 Google 账号的 Search Console 里没有添加 osrsguru.com")
    print("2. Search Console 里添加的是其他格式（如 http:// 或非 www）")
    print("3. 数据还没生成（新网站可能需要几天）")
    return []


def format_report(rows, start_date, end_date):
    """格式化排名数据为可读报告"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  OSRS Guru — Google 搜索排名报告")
    lines.append(f"  日期范围: {start_date} 至 {end_date}")
    lines.append(f"  查询时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)
    lines.append("")

    if not rows:
        lines.append("  ❌ 暂无数据")
        lines.append("  可能原因：")
        lines.append("  · Search Console 中还未收录该网站数据")
        lines.append("  · API 尚未启用（需在 Google Cloud 控制台启用 Search Console API）")
        lines.append("  · OAuth 授权的账号未绑定该网站 Search Console")
        lines.append("")
        return "\n".join(lines)

    # 按页面分组聚合
    page_stats = {}
    for row in rows:
        page_url = row['keys'][0]
        keyword = row['keys'][1]
        clicks = row['clicks']
        impressions = row['impressions']
        position = round(row['position'], 1)

        if page_url not in page_stats:
            page_stats[page_url] = {
                'clicks': 0,
                'impressions': 0,
                'total_position': 0,
                'position_count': 0,
                'queries': []
            }

        ps = page_stats[page_url]
        ps['clicks'] += clicks
        ps['impressions'] += impressions
        ps['total_position'] += position * impressions  # 加权平均
        ps['position_count'] += impressions
        ps['queries'].append({
            'keyword': keyword,
            'clicks': clicks,
            'impressions': impressions,
            'position': position
        })

    # 计算加权平均排名
    for url, ps in page_stats.items():
        if ps['position_count'] > 0:
            ps['avg_position'] = round(ps['total_position'] / ps['position_count'], 1)
        else:
            ps['avg_position'] = 999
        # 截取页面路径
        site_part = "osrsguru.com"
        idx = url.find(site_part)
        if idx > 0:
            ps['short_url'] = url[idx:]
        else:
            ps['short_url'] = url

    # 按点击量降序排列
    sorted_pages = sorted(
        page_stats.items(),
        key=lambda x: x[1]['clicks'],
        reverse=True
    )

    lines.append(f"📊 总展示次数: {sum(ps['impressions'] for _, ps in sorted_pages):,}")
    lines.append(f"🖱️  总点击次数: {sum(ps['clicks'] for _, ps in sorted_pages):,}")
    lines.append(f"📄 总页面数: {len(sorted_pages)}")
    lines.append("")

    # 表格头
    lines.append("-" * 70)
    lines.append(f"{'排名':>6} {'点击':>6} {'展示':>8} {'平均排名':>8}  页面路径")
    lines.append("-" * 70)

    for i, (url, ps) in enumerate(sorted_pages[:TOP_RESULTS], 1):
        short = ps['short_url']
        # 如果太长截断
        if len(short) > 50:
            short = short[:47] + "..."

        lines.append(
            f"{i:>4}. {ps['clicks']:>6} {ps['impressions']:>8} "
            f"{ps['avg_position']:>8.1f}  {short}"
        )

    lines.append("-" * 70)
    lines.append("")

    # 显示前 5 页面的具体关键词
    lines.append("📌 排名靠前页面的热门关键词")
    lines.append("=" * 70)

    for i, (url, ps) in enumerate(sorted_pages[:5], 1):
        short = ps['short_url']
        if len(short) > 55:
            short = short[:52] + "..."
        lines.append(f"\n{i}. {short}")
        lines.append(f"   总点击: {ps['clicks']}  |  总展示: {ps['impressions']:,}  |  平均排名: #{ps['avg_position']}")
        lines.append(f"   热门关键词:")

        # 按点击量排列关键词
        sorted_queries = sorted(ps['queries'], key=lambda q: q['clicks'], reverse=True)[:5]
        for q in sorted_queries:
            ranking_badge = "🟢" if q['position'] <= 10 else ("🟡" if q['position'] <= 30 else "🔴")
            lines.append(f"     {ranking_badge} #{q['position']:>4.1f}  {q['clicks']:>4}次点击  {q['impressions']:>5}次展示  「{q['keyword']}」")

    lines.append("")
    lines.append("=" * 70)
    lines.append("  图例：🟢 排名前10  🟡 排名11-30  🔴 排名30+")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_and_show(report_text):
    """保存报告并显示"""
    # 保存文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\n[OK] 报告已保存至: {OUTPUT_FILE}")

    # 直接打印
    print("\n" + report_text)


def main():
    print("=" * 60)
    print("  OSRS Guru — Google Search Console 排名查询")
    print("=" * 60)
    print(f"  网站: {SITE_URL}")
    print(f"  查询周期: 最近 {DAYS_BACK} 天")

    try:
        # 1. 设置代理
        setup_proxy()

        # 2. 获取凭证
        print("\n[1/3] 正在获取 Google API 授权...")
        creds = get_auth()

        # 3. 计算日期
        today = datetime.date.today()
        start_date = (today - datetime.timedelta(days=DAYS_BACK)).strftime("%Y-%m-%d")
        end_date = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        # 4. 查询数据
        print(f"[2/3] 正在查询 {start_date} ~ {end_date} 的数据...")
        rows = query_search_console(creds, start_date, end_date, row_limit=200)

        # 5. 生成报告
        print(f"[3/3] 正在生成报告...")
        report = format_report(rows, start_date, end_date)

        # 6. 保存并显示
        save_and_show(report)

    except ImportError as e:
        print(f"\n❌ 缺少依赖库: {e}")
        print("\n请先安装依赖:")
        print("  pip install requests google-auth-oauthlib google-auth")

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("\n常见解决方法:")
        print("1. 打开 https://console.cloud.google.com/apis/library/searchconsole.googleapis.com")
        print("   确认 'Search Console API' 已启用")
        print("2. 打开 https://console.cloud.google.com/apis/credentials")
        print("   检查 OAuth consent screen 中已添加测试用户: 1530398390@qq.com")
        print("3. 确认该 Google 账号已在 Search Console 中添加了 osrsguru.com")


if __name__ == "__main__":
    main()
