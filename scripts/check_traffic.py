# -*- coding: utf-8 -*-
"""
GA4 流量查询脚本 - 在 cmd 中运行
用法: python scripts/check_traffic.py
"""
import sys
import os
import json

# === 代理设置（可选，根据你的 Clash 端口调整）===
CLASH_PORT = "7897"
os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{CLASH_PORT}'
os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{CLASH_PORT}'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token_ga4.json")
SECRET_FILE = os.path.join(SCRIPT_DIR, "client_secret.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "..", "traffic_report.txt")

GA4_SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

def get_auth():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, GA4_SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[INFO] Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("\n" + "=" * 60)
            print("  需要 Google 账号授权 - 浏览器将自动打开")
            print("  请用你的 Google 账号登录（与 GA4 关联的账号）")
            print("=" * 60 + "\n")
            flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, GA4_SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print("[OK] Token saved to token_ga4.json")
    
    return creds

def api_call(session, url, body=None):
    """发送 GA4 REST API 请求（带代理）"""
    import requests
    proxies = {'http': f'http://127.0.0.1:{CLASH_PORT}', 'https': f'http://127.0.0.1:{CLASH_PORT}'}
    
    if body:
        r = session.post(url, json=body)
    else:
        r = session.get(url)
    r.raise_for_status()
    return r.json()

def main():
    from google.auth.transport.requests import AuthorizedSession
    
    print("=" * 60)
    print("  OSRS Guru (osrsguru.com) - GA4 流量报告")
    print("=" * 60)
    
    creds = get_auth()
    session = AuthorizedSession(creds)
    
    # 1. 获取 GA4 属性列表
    print("\n[1/4] 获取 GA4 属性列表...")
    summaries = api_call(session, 
        "https://analyticsadmin.googleapis.com/v1beta/accountSummaries")
    
    output_lines = []
    found = False
    
    for summary in summaries.get('accountSummaries', []):
        account = summary.get('displayName', 'Account')
        for prop in summary.get('propertySummaries', []):
            prop_name = prop.get('displayName', 'Unknown')
            prop_id = prop.get('property', '').replace('properties/', '')
            
            print(f"\n  账户: {account}")
            print(f"  属性: {prop_name} (ID: {prop_id})\n")
            output_lines.append(f"账户: {account}")
            output_lines.append(f"属性: {prop_name} (ID: {prop_id})")
            output_lines.append("")
            
            date_ranges = [{"startDate": "30daysAgo", "endDate": "today"}]
            
            # 2. 每日流量
            print("[2/4] 每日流量数据...")
            report = api_call(session,
                f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport",
                {
                    "dateRanges": date_ranges,
                    "dimensions": [{"name": "date"}],
                    "metrics": [
                        {"name": "activeUsers"},
                        {"name": "screenPageViews"},
                        {"name": "sessions"},
                    ],
                    "orderBys": [{"dimension": {"dimensionName": "date"}}],
                }
            )
            
            rows = report.get('rows', [])
            total_users = 0
            total_views = 0
            total_sessions = 0
            
            print(f"  {'日期':<12} {'用户':>6} {'PV':>6} {'会话':>5}")
            print(f"  {'-'*12} {'-'*6} {'-'*6} {'-'*5}")
            output_lines.append("每日流量:")
            
            for row in rows:
                d = row['dimensionValues'][0]['value']
                u = int(row['metricValues'][0]['value'])
                v = int(row['metricValues'][1]['value'])
                s = int(row['metricValues'][2]['value'])
                if u + v + s > 0:  # 跳过0数据日期
                    print(f"  {d[:4]}-{d[4:6]}-{d[6:]:<5} {u:>6} {v:>6} {s:>5}")
                    output_lines.append(f"  {d[:4]}-{d[4:6]}-{d[6:]:<5} {u:>6} {v:>6} {s:>5}")
                total_users += u
                total_views += v
                total_sessions += s
            
            print(f"\n  [30天合计] 用户: {total_users} | PV: {total_views} | 会话: {total_sessions}")
            output_lines.append(f"\n30天合计: 用户 {total_users} | PV {total_views} | 会话 {total_sessions}")
            
            # 3. 热门页面
            print("\n[3/4] 热门页面 Top 20...")
            pages = api_call(session,
                f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport",
                {
                    "dateRanges": date_ranges,
                    "dimensions": [{"name": "pagePath"}, {"name": "pageTitle"}],
                    "metrics": [{"name": "screenPageViews"}],
                    "limit": "20",
                    "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
                }
            )
            
            output_lines.append("\n热门页面 Top 20:")
            for i, row in enumerate(pages.get('rows', [])[:20], 1):
                path = row['dimensionValues'][0]['value']
                title = row['dimensionValues'][1]['value'][:40]
                pv = int(row['metricValues'][0]['value'])
                print(f"  {i:>2}. [{pv:>5}] {title}  -> {path}")
                output_lines.append(f"  {i:>2}. [{pv:>5}] {title}  -> {path}")
            
            # 4. 流量来源 + 国家
            print("\n[4/4] 流量来源...")
            
            # 来源
            sources = api_call(session,
                f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport",
                {
                    "dateRanges": date_ranges,
                    "dimensions": [{"name": "sessionSourceMedium"}],
                    "metrics": [{"name": "activeUsers"}],
                    "limit": "10",
                    "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
                }
            )
            
            output_lines.append("\n流量来源:")
            for row in sources.get('rows', []):
                src = row['dimensionValues'][0]['value']
                u = int(row['metricValues'][0]['value'])
                print(f"  {src}: {u} 用户")
                output_lines.append(f"  {src}: {u} 用户")
            
            # 国家
            countries = api_call(session,
                f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport",
                {
                    "dateRanges": date_ranges,
                    "dimensions": [{"name": "country"}],
                    "metrics": [{"name": "activeUsers"}],
                    "limit": "10",
                    "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
                }
            )
            
            output_lines.append("\n访客国家:")
            for row in countries.get('rows', []):
                c = row['dimensionValues'][0]['value']
                u = int(row['metricValues'][0]['value'])
                print(f"  {c}: {u} 用户")
                output_lines.append(f"  {c}: {u} 用户")
            
            found = True
            break
        if found:
            break
    
    # 保存报告
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    print(f"\n[OK] 报告已保存到: {OUTPUT_FILE}")
    
    print("\n" + "=" * 60)
    if total_users == 0:
        print("  [注意] 目前没有任何访问数据")
        print("  可能原因: GA4 刚安装 / 网站太新 / 数据延迟")
    else:
        print(f"  [总结] 30天: {total_users} 用户 | {total_views} PV")
    print("=" * 60)

if __name__ == "__main__":
    main()
