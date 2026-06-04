#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSRS Guru - GA4 可视化流量仪表盘生成器 v2
- 使用 GA4 Data API 拉取真实数据
- 生成自包含 HTML 仪表盘（Chart.js CDN）
- 用于第二阶段收费决策的数据支撑
"""

import os
import sys
import json
import time
import datetime

# ============================================================
# 配置
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token_ga4.json")
SECRET_FILE = os.path.join(SCRIPT_DIR, "client_secret.json")
OUTPUT_HTML = os.path.join(SCRIPT_DIR, "..", "ga4_dashboard.html")

# GA4 Property ID（从 Measurement ID 推导）
# 如果不知道，脚本会自动查找
# 手动填写格式：PROPERTY_ID = "123456789"
PROPERTY_ID = "539696958"  # 手动指定（从 GA4 媒体资源详情页获取）

# 代理设置
CLASH_PORT = "7897"
os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{CLASH_PORT}'
os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{CLASH_PORT}'

# ============================================================
# Step 1: 认证
# ============================================================
def get_credentials():
    import json
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            # 尝试 JSON 格式（to_json() 保存的格式）
            with open(TOKEN_FILE, 'r') as f:
                creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)
        except Exception as e:
            print(f"  [Warn] Token 格式异常，重新授权: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[Auth] Refreshing token...")
            creds.refresh(Request())
        else:
            print("\n" + "=" * 60)
            print("  GA4 授权需要 - 浏览器将打开")
            print("  请登录与 GA4 关联的 Google 账号")
            print("=" * 60)
            flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print("[OK] Token saved")

    return creds

# ============================================================
# Step 2: API 请求辅助
# ============================================================
def api_post(creds, url, body):
    import requests
    proxies = {
        'http': f'http://127.0.0.1:{CLASH_PORT}',
        'https': f'http://127.0.0.1:{CLASH_PORT}',
    }
    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json',
    }
    resp = requests.post(url, json=body, headers=headers,
                        proxies=proxies, timeout=30)
    resp.raise_for_status()
    return resp.json()

def api_get(creds, url):
    import requests
    proxies = {
        'http': f'http://127.0.0.1:{CLASH_PORT}',
        'https': f'http://127.0.0.1:{CLASH_PORT}',
    }
    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
    headers = {'Authorization': f'Bearer {creds.token}'}
    resp = requests.get(url, headers=headers, proxies=proxies, timeout=30)
    resp.raise_for_status()
    return resp.json()

# ============================================================
# Step 3: 查找 GA4 Property ID
# ============================================================
def find_property_id(creds):
    print("[GA4] 查找 GA4 属性...")
    summaries = api_get(creds, "https://analyticsadmin.googleapis.com/v1beta/accountSummaries")
    for summary in summaries.get('accountSummaries', []):
        account_name = summary.get('displayName', '')
        for prop in summary.get('propertySummaries', []):
            prop_name = prop.get('displayName', '')
            prop_id = prop.get('property', '').replace('properties/', '')
            print(f"  Found: {account_name} / {prop_name} (ID: {prop_id})")
            # 优先匹配 osrsguru
            if 'osrs' in prop_name.lower() or 'guru' in prop_name.lower():
                return prop_id
    # 没匹配到就返回第一个
    for summary in summaries.get('accountSummaries', []):
        for prop in summary.get('propertySummaries', []):
            return prop.get('property', '').replace('properties/', '')
    return None

# ============================================================
# Step 4: 拉取所有数据
# ============================================================
def fetch_all_data(creds, property_id):
    BASE = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    date_ranges = [{"startDate": "30daysAgo", "endDate": "today"}]
    date_ranges7 = [{"startDate": "7daysAgo", "endDate": "today"}]

    data = {}

    # --- 4.1 概览指标（30天）---
    print("[Data] 拉取概览指标...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "metrics": [
            {"name": "activeUsers"},
            {"name": "newUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "averageSessionDuration"},
            {"name": "bounceRate"},
            {"name": "engagedSessions"},
        ],
    })
    row = r.get('rows', [{}])[0]
    m = {k['name']: k for k in row.get('metricValues', [])}
    data['summary'] = {
        'users': int(m.get('activeUsers', {}).get('value', 0)),
        'new_users': int(m.get('newUsers', {}).get('value', 0)),
        'sessions': int(m.get('sessions', {}).get('value', 0)),
        'pageviews': int(m.get('screenPageViews', {}).get('value', 0)),
        'avg_duration': float(m.get('averageSessionDuration', {}).get('value', 0)),
        'bounce_rate': float(m.get('bounceRate', {}).get('value', 0)),
        'engaged_sessions': int(m.get('engagedSessions', {}).get('value', 0)),
    }

    # --- 4.2 每日流量（30天）---
    print("[Data] 拉取每日流量...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "dimensions": [{"name": "date"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "screenPageViews"},
            {"name": "sessions"},
        ],
        "orderBys": [{"dimension": {"dimensionName": "date"}}],
    })
    daily = []
    for row in r.get('rows', []):
        d = row['dimensionValues'][0]['value']
        u = int(row['metricValues'][0]['value'])
        v = int(row['metricValues'][1]['value'])
        s = int(row['metricValues'][2]['value'])
        daily.append({'date': f"{d[0:4]}-{d[4:6]}-{d[6:]}", 'users': u, 'pageviews': v, 'sessions': s})
    data['daily'] = daily

    # --- 4.3 热门页面 Top 20 ---
    print("[Data] 拉取热门页面...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "dimensions": [{"name": "pagePath"}, {"name": "pageTitle"}],
        "metrics": [{"name": "screenPageViews"}],
        "limit": "20",
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
    })
    pages = []
    for row in r.get('rows', []):
        path = row['dimensionValues'][0]['value']
        title = row['dimensionValues'][1]['value'][:50]
        pv = int(row['metricValues'][0]['value'])
        pages.append({'path': path, 'title': title, 'pageviews': pv})
    data['top_pages'] = pages

    # --- 4.4 流量来源 ---
    print("[Data] 拉取流量来源...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "dimensions": [{"name": "sessionSourceMedium"}],
        "metrics": [{"name": "activeUsers"}],
        "limit": "10",
        "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    })
    sources = []
    for row in r.get('rows', []):
        src = row['dimensionValues'][0]['value']
        u = int(row['metricValues'][0]['value'])
        sources.append({'source': src, 'users': u})
    data['sources'] = sources

    # --- 4.5 国家分布 ---
    print("[Data] 拉取国家分布...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "dimensions": [{"name": "country"}],
        "metrics": [{"name": "activeUsers"}],
        "limit": "10",
        "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    })
    countries = []
    for row in r.get('rows', []):
        c = row['dimensionValues'][0]['value']
        u = int(row['metricValues'][0]['value'])
        countries.append({'country': c, 'users': u})
    data['countries'] = countries

    # --- 4.6 设备类型 ---
    print("[Data] 拉取设备类型...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "dimensions": [{"name": "deviceCategory"}],
        "metrics": [{"name": "activeUsers"}],
        "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    })
    devices = []
    for row in r.get('rows', []):
        d = row['dimensionValues'][0]['value']
        u = int(row['metricValues'][0]['value'])
        devices.append({'device': d, 'users': u})
    data['devices'] = devices

    # --- 4.7 页面停留时间 Top 10 ---
    print("[Data] 拉取页面平均参与度...")
    r = api_post(creds, BASE, {
        "dateRanges": date_ranges,
        "dimensions": [{"name": "pagePath"}],
        "metrics": [{"name": "averageSessionDuration"}, {"name": "screenPageViews"}],
        "limit": "10",
        "orderBys": [{"metric": {"metricName": "averageSessionDuration"}, "desc": True}],
    })
    engagement = []
    for row in r.get('rows', []):
        path = row['dimensionValues'][0]['value']
        dur = float(row['metricValues'][0]['value'])
        pv = int(row['metricValues'][1]['value'])
        engagement.append({'path': path, 'avg_duration': dur, 'pageviews': pv})
    data['engagement'] = engagement

    # --- 4.8 近 7 天 vs 前 7 天对比 ---
    print("[Data] 拉取增长率数据...")
    r_now = api_post(creds, BASE, {
        "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}],
    })
    r_prev = api_post(creds, BASE, {
        "dateRanges": [{"startDate": "14daysAgo", "endDate": "8daysAgo"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}],
    })
    now_users = int(r_now['rows'][0]['metricValues'][0]['value']) if r_now.get('rows') else 0
    now_pv = int(r_now['rows'][0]['metricValues'][1]['value']) if r_now.get('rows') else 0
    prev_users = int(r_prev['rows'][0]['metricValues'][0]['value']) if r_prev.get('rows') else 0
    prev_pv = int(r_prev['rows'][0]['metricValues'][1]['value']) if r_prev.get('rows') else 0
    data['growth'] = {
        'users_now': now_users, 'users_prev': prev_users,
        'pv_now': now_pv, 'pv_prev': prev_pv,
        'users_growth': round((now_users - prev_users) / max(prev_users, 1) * 100, 1),
        'pv_growth': round((now_pv - prev_pv) / max(prev_users, 1) * 100, 1),
    }

    return data

# ============================================================
# Step 5: 生成 HTML 仪表盘
# ============================================================
def generate_html(data, output_path):
    import html
    s = data['summary']
    daily = data['daily']
    pages = data['top_pages']
    sources = data['sources']
    countries = data['countries']
    devices = data['devices']
    engagement = data['engagement']
    growth = data['growth']

    # 格式化时长
    avg_dur = int(s['avg_duration'])
    dur_str = f"{avg_dur // 60}:{avg_dur % 60:02d}"

    # 每日数据（最近 14 天）
    daily_14 = daily[-14:] if len(daily) >= 14 else daily
    daily_labels = [d['date'] for d in daily_14]
    daily_users = [d['users'] for d in daily_14]
    daily_pv = [d['pageviews'] for d in daily_14]

    # 热门页面列表 HTML
    pages_html = ""
    for i, p in enumerate(pages[:15], 1):
        pages_html += f"<tr><td>{i}</td><td class='left'>{html.escape(p['title'])}</td><td>{html.escape(p['path'])}</td><td>{p['pageviews']:,}</td></tr>\n"

    # 流量来源列表
    sources_html = ""
    for s2 in sources:
        sources_html += f"<tr><td>{html.escape(s2['source'])}</td><td>{s2['users']:,}</td><td>{round(s2['users']/max(s['users'],1)*100,1)}%</td></tr>\n"

    # 国家列表
    countries_html = ""
    for c in countries:
        countries_html += f"<tr><td>{html.escape(c['country'])}</td><td>{c['users']:,}</td><td>{round(c['users']/max(s['users'],1)*100,1)}%</td></tr>\n"

    # 参与度列表
    eng_html = ""
    for e in engagement[:10]:
        mins = int(e['avg_duration'] // 60)
        secs = int(e['avg_duration'] % 60)
        eng_html += f"<tr><td class='left'>{html.escape(e['path'])}</td><td>{mins}:{secs:02d}</td><td>{e['pageviews']:,}</td></tr>\n"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OSRS Guru - GA4 流量仪表盘</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #0f0f0f;
    color: #e0e0e0;
    padding: 20px;
  }}
  h1 {{
    color: #f0c040;
    font-size: 24px;
    margin-bottom: 4px;
  }}
  .subtitle {{
    color: #888;
    font-size: 13px;
    margin-bottom: 24px;
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .card {{
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
  }}
  .card h3 {{
    color: #888;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}
  .card .num {{
    font-size: 32px;
    font-weight: 700;
    color: #f0c040;
  }}
  .card .sub {{
    font-size: 12px;
    color: #888;
    margin-top: 4px;
  }}
  .card .growth {{
    font-size: 13px;
    margin-top: 6px;
    color: #4caf50;
  }}
  .card .growth.negative {{ color: #f44336; }}
  .chart-row {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
  }}
  .chart-box {{
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    border-radius: 10px;
    padding: 20px;
  }}
  .chart-box h2 {{
    color: #f0c040;
    font-size: 16px;
    margin-bottom: 16px;
  }}
  .table-box {{
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 24px;
    overflow-x: auto;
  }}
  .table-box h2 {{
    color: #f0c040;
    font-size: 16px;
    margin-bottom: 16px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  th {{
    background: #2d2d4a;
    color: #f0c040;
    padding: 8px 12px;
    text-align: right;
    font-size: 11px;
    text-transform: uppercase;
  }}
  th.left, td.left {{
    text-align: left;
  }}
  td {{
    padding: 8px 12px;
    border-bottom: 1px solid #2d2d4a;
    text-align: right;
  }}
  tr:hover {{ background: #2d2d4a44; }}
  .badge {{
    display: inline-block;
    background: #f0c04022;
    color: #f0c040;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    margin-left: 6px;
  }}
  .insight {{
    background: #1a1a2e;
    border-left: 3px solid #f0c040;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin-bottom: 24px;
  }}
  .insight h2 {{
    color: #f0c040;
    font-size: 16px;
    margin-bottom: 12px;
  }}
  .insight ul {{
    list-style: none;
    padding: 0;
  }}
  .insight li {{
    padding: 6px 0;
    color: #ccc;
    font-size: 14px;
  }}
  .insight li::before {{
    content: '→ ';
    color: #f0c040;
  }}
  @media (max-width: 900px) {{
    .chart-row {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<h1>📊 OSRS Guru - GA4 流量仪表盘</h1>
<p class="subtitle">过去 30 天数据 | 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} CST</p>

<!-- KPI 卡片 -->
<div class="grid">
  <div class="card">
    <h3>活跃用户</h3>
    <div class="num">{s['users']:,}</div>
    <div class="sub">30天</div>
    <div class="growth {'negative' if growth['users_growth'] < 0 else ''}">{'↓' if growth['users_growth'] < 0 else '↑'} {abs(growth['users_growth'])}% vs 前7天</div>
  </div>
  <div class="card">
    <h3>页面浏览</h3>
    <div class="num">{s['pageviews']:,}</div>
    <div class="sub">30天</div>
    <div class="growth {'negative' if growth['pv_growth'] < 0 else ''}">{'↓' if growth['pv_growth'] < 0 else '↑'} {abs(growth['pv_growth'])}% vs 前7天</div>
  </div>
  <div class="card">
    <h3>新用户</h3>
    <div class="num">{s['new_users']:,}</div>
    <div class="sub">占比 {round(s['new_users']/max(s['users'],1)*100,1)}%</div>
  </div>
  <div class="card">
    <h3>会话数</h3>
    <div class="num">{s['sessions']:,}</div>
    <div class="sub">平均时长 {dur_str}</div>
  </div>
  <div class="card">
    <h3>互动会话</h3>
    <div class="num">{s['engaged_sessions']:,}</div>
    <div class="sub">占比 {round(s['engaged_sessions']/max(s['sessions'],1)*100,1)}%</div>
  </div>
</div>

<!-- 洞察建议 -->
<div class="insight">
  <h2>💡 第二阶段决策建议</h2>
  <ul>
    <li><b>最高流量页面:</b> {html.escape(pages[0]['title'] if pages else '暂无数据')} ({pages[0]['pageviews'] if pages else 0} PV) — <b>优先做成付费深度版</b></li>
    <li><b>流量来源:</b> {html.escape(sources[0]['source'] if sources else '暂无数据')} 占 {round(sources[0]['users']/max(s['users'],1)*100,1) if sources else 0}% — {'考虑 SEO 优化' if 'google' in (sources[0]['source'] if sources else '').lower() else '考虑社交媒体推广'}</li>
    <li><b>用户停留:</b> 平均 {dur_str} — {'内容吸引力强，可考虑高级会员' if s['avg_duration'] > 60 else '需增加内容深度，提升停留时间'}</li>
    <li><b>新用户占比:</b> {round(s['new_users']/max(s['users'],1)*100,1)}% — {'增长健康' if s['new_users']/max(s['users'],1) > 0.5 else '需加强新用户获取'}</li>
  </ul>
</div>

<!-- 图表行 -->
<div class="chart-row">
  <div class="chart-box">
    <h2>📈 每日流量趋势（最近 14 天）</h2>
    <canvas id="dailyChart"></canvas>
  </div>
  <div class="chart-box">
    <h2>📱 设备分布</h2>
    <canvas id="deviceChart"></canvas>
  </div>
</div>

<div class="chart-row">
  <div class="chart-box">
    <h2>🌍 访客国家分布</h2>
    <canvas id="countryChart"></canvas>
  </div>
  <div class="chart-box">
    <h2>🔗 流量来源</h2>
    <canvas id="sourceChart"></canvas>
  </div>
</div>

<!-- 数据表格 -->
<div class="table-box">
  <h2>🏆 热门页面 Top 15</h2>
  <table>
    <tr><th>#</th><th class="left">页面标题</th><th class="left">路径</th><th>PV</th></tr>
    {pages_html}
  </table>
</div>

<div class="table-box">
  <h2>⏱️ 页面平均停留时间 Top 10</h2>
  <table>
    <tr><th class="left">页面路径</th><th>平均停留</th><th>PV</th></tr>
    {eng_html}
  </table>
</div>

<div class="table-box">
  <h2>🔗 流量来源明细</h2>
  <table>
    <tr><th class="left">来源 / 媒介</th><th>用户数</th><th>占比</th></tr>
    {sources_html}
  </table>
</div>

<div class="table-box">
  <h2>🌍 国家分布</h2>
  <table>
    <tr><th class="left">国家</th><th>用户数</th><th>占比</th></tr>
    {countries_html}
  </table>
</div>

<script>
// 每日流量趋势
new Chart(document.getElementById('dailyChart'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(daily_labels)},
    datasets: [{{
      label: '用户数',
      data: {json.dumps(daily_users)},
      borderColor: '#f0c040',
      backgroundColor: '#f0c04022',
      fill: true,
      tension: 0.4,
      yAxisID: 'y',
    }}, {{
      label: '页面浏览',
      data: {json.dumps(daily_pv)},
      borderColor: '#4caf50',
      backgroundColor: '#4caf5022',
      fill: true,
      tension: 0.4,
      yAxisID: 'y1',
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }} }},
    scales: {{
      x: {{ ticks: {{ color: '#888', maxTicksLimit: 10 }} }},
      y: {{ position: 'left', ticks: {{ color: '#f0c040' }}, grid: {{ color: '#2d2d4a' }} }},
      y1: {{ position: 'right', ticks: {{ color: '#4caf50' }}, grid: {{ display: false }} }},
    }}
  }}
}});

// 设备分布
new Chart(document.getElementById('deviceChart'), {{
  type: 'doughnut',
  data: {{
    labels: {json.dumps([d['device'] for d in devices])},
    datasets: [{{
      data: {json.dumps([d['users'] for d in devices])},
      backgroundColor: ['#f0c040', '#4caf50', '#2196f3', '#ff9800'],
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#ccc' }} }} }}
  }}
}});

// 国家分布
new Chart(document.getElementById('countryChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps([c['country'] for c in countries[:8]])},
    datasets: [{{
      label: '用户数',
      data: {json.dumps([c['users'] for c in countries[:8]])},
      backgroundColor: '#f0c040cc',
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: {{ color: '#888' }} }},
      y: {{ ticks: {{ color: '#888' }}, grid: {{ color: '#2d2d4a' }} }},
    }}
  }}
}});

// 流量来源
new Chart(document.getElementById('sourceChart'), {{
  type: 'pie',
  data: {{
    labels: {json.dumps([s2['source'][:20] for s2 in sources])},
    datasets: [{{
      data: {json.dumps([s2['users'] for s2 in sources])},
      backgroundColor: ['#f0c040', '#4caf50', '#2196f3', '#ff9800', '#e91e63', '#9c27b0', '#00bcd4', '#8bc34a', '#ff5722', '#607d8b'],
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#ccc', font: {{ size: 11 }} }} }} }}
  }}
}});
</script>

</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n[OK] 仪表盘已生成: {output_path}")
    return output_path

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("  OSRS Guru - GA4 可视化流量仪表盘生成器 v2")
    print("=" * 60)

    if not os.path.exists(SECRET_FILE):
        print(f"[ERROR] client_secret.json 不存在: {SECRET_FILE}")
        sys.exit(1)

    # 认证
    print("\n[1/4] 认证 GA4...")
    creds = get_credentials()
    print("  OK - 认证成功")

    # 使用预设 Property ID（跳过 Admin API 调用）
    print("\n[2/4] 使用 GA4 Property ID...")
    prop_id = PROPERTY_ID
    if not prop_id:
        print("[ERROR] PROPERTY_ID 未配置")
        sys.exit(1)
    print(f"  OK - Property ID: {prop_id}")

    # 拉取数据
    print("\n[3/4] 拉取 GA4 数据（可能需要 1-2 分钟）...")
    data = fetch_all_data(creds, prop_id)
    print(f"  OK - 已拉取 {len(data['daily'])} 天数据, {len(data['top_pages'])} 个页面")

    # 生成 HTML
    print("\n[4/4] 生成可视化仪表盘...")
    output = generate_html(data, OUTPUT_HTML)

    print("\n" + "=" * 60)
    print(f"  ✅ 完成！")
    print(f"  打开以下文件查看仪表盘:")
    print(f"  file:///{output.replace(chr(92), '/')}")
    print("=" * 60)

if __name__ == '__main__':
    main()
