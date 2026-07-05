#!/usr/bin/env python3
"""
Re-process osrs-mid-game-money-making-roadmap-2026.html for zh/guides/
"""
import re, os

BASE = "c:/Users/Lenovo/osrs-guide-site"
filename = "osrs-mid-game-money-making-roadmap-2026.html"
src = os.path.join(BASE, "guides", filename)
dst = os.path.join(BASE, "zh", "guides", filename)

with open(src, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Source size: {len(html)} bytes")

# 1. lang
html = html.replace('lang="en"', 'lang="zh-Hans"')

# 2. Title
html = re.sub(r'<title>[^<]+</title>',
    '<title>OSRS 2026中期游戏赚钱路线图 — 15种方法（180万-300万GP/小时）</title>', html)

# 3. Canonical
html = re.sub(r'href="https://osrsguru\.com/guides/' + re.escape(filename) + r'"',
    'href="https://osrsguru.com/zh/guides/' + filename + '"', html)

# 4. og:url
html = re.sub(r'<meta property="og:url" content="https://osrsguru\.com/guides/' + re.escape(filename) + r'">',
    '<meta property="og:url" content="https://osrsguru.com/zh/guides/' + filename + '">', html)

# 5. CSS path
html = html.replace('href="../css/style.css"', 'href="../../css/style.css"')

# 6. Nav/breadcrumb links
for oldp in ['href="../index.html"', 'href="../money-making.html"', 'href="../skilling.html"',
             'href="../bossing.html"', 'href="../guides.html"']:
    html = html.replace(oldp, oldp.replace('href="..', 'href="../..'))

# 7. hero section: add cn-title/cn-summary
cn_title = "OSRS 2026中期游戏赚钱路线图 — 15种方法（180万-300万GP/小时）"
cn_summary = "为战斗等级60-100的OSRS玩家打造的完整中期赚钱路线图。涵盖15种详细方法，按GP/小时、需求和付出程度排名，帮助玩家从新手方法过渡到终局Boss战。"

# Replace the hero h1: insert cn-title before it
# Pattern: find first <h1> inside <section class="guide-hero">
hero_pattern = re.compile(
    r'(<section class="guide-hero">.*?<div class="container">.*?)'
    r'(<h1[^>]*>)(.*?)(</h1>)',
    re.DOTALL
)

def add_cn(m):
    cn_block = (
        '<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">'
        + cn_title
        + '</h1>\n            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">'
        + cn_summary
        + '</p>\n            '
    )
    return m.group(1) + cn_block + m.group(2) + m.group(3) + m.group(4)

html = hero_pattern.sub(add_cn, html, count=1)

# 8. Quick Summary - translate heading
html = html.replace(
    '⏱️ Quick Summary — 30-Second Read',
    '⏱️ 30秒快速预览'
)

# 9. Quick Summary items - replace ul content
qs_items = [
    '📌 <strong>15种方法排名（15 methods ranked）</strong> — 战斗60-100最佳区间，从新手到终局过渡',
    '📌 <strong>最佳中期战斗（Best mid-game combat）</strong>: 恶魔大猩猩每小时300万GP，Zulrah入门每小时250万GP，Vorkath入门每小时200万GP',
    '📌 <strong>最佳中期技能（Best skilling mid-game）</strong>: 高炉锻造每小时250万GP，草药跑每日66万被动收入',
    '📌 <strong>装备优先级路线图（Gear priority roadmap）</strong>: 从500万GP预算到5000万+终局装备的升级顺序',
    '📌 <strong>终局过渡（Endgame transition）</strong>: 从中期到Chambers of Xeric和终局Boss战的分步路径',
]

qs_html_ul = '\n'.join(f'                    <li>{item}</li>' for item in qs_items)

# Replace the ul inside quick-summary
html = re.sub(
    r'(<div class="quick-summary"[^>]*>.*?<ul[^>]*>).*?(</ul>)',
    lambda m: m.group(1) + '\n' + qs_html_ul + '\n                ' + m.group(2),
    html,
    flags=re.DOTALL
)

# 10. TOC items - add Chinese translations
toc_map = {
    "Demonic Gorillas (3M GP/hr)": "恶魔大猩猩（每小时300万GP）",
    "Zulrah Entry (2.5M GP/hr)": "Zulrah入门（每小时250万GP）",
    "Vorkath Entry (2M GP/hr)": "Vorkath入门（每小时200万GP）",
    "Barrows (1.8M GP/hr)": "Barrows（每小时180万GP）",
    "Blast Furnace (2.5M GP/hr)": "高炉锻造（每小时250万GP）",
    "Slayer (1.8M-M GP/hr)": "战斗任务（每小时180万+GP）",
    "Herb Runs (660K/day Passive)": "草药跑（每日66万被动收入）",
    "Birdhouse Runs (Passive)": "鸟屋跑（被动收入）",
    "Giant's Foundry": "巨人铸造厂",
    "Flipping / Merchanting": "倒卖/交易",
    "Daily GP Routine": "每日GP例行任务",
    "Gear Priority Roadmap": "装备优先级路线图",
    "Endgame Transition Path": "终局过渡路径",
    "Common Mid-Game Mistakes": "中期常见错误",
    "FAQ — Mid-Game Money Making": "常见问题——中期赚钱",
}

for en_text, cn_text in toc_map.items():
    pattern = re.compile(r'(<a href="[^"]*">)' + re.escape(en_text) + r'(</a>)')
    html = pattern.sub(lambda m, et=en_text, ct=cn_text: m.group(1) + et + '（' + ct + '）' + m.group(2), html)

# 11. h2 headings
h2_map = {
    "1. Demonic Gorillas (3M GP/hr)": "1. 恶魔大猩猩（Demonic Gorillas）",
    "2. Zulrah Entry (2.5M GP/hr)": "2. Zulrah入门（Zulrah Entry）",
    "3. Vorkath Entry (2M GP/hr)": "3. Vorkath入门（Vorkath Entry）",
    "4. Barrows (1.8M GP/hr)": "4. Barrows（每小时180万GP）",
    "5. Blast Furnace (2.5M GP/hr)": "5. 高炉锻造（Blast Furnace）",
    "6. Slayer (1.8M-M GP/hr)": "6. 战斗任务（Slayer）",
    "7. Herb Runs (660K/day)": "7. 草药跑（Herb Runs）",
    "8. Birdhouse Runs (Passive)": "8. 鸟屋跑（Birdhouse Runs）",
    "9. Giant's Foundry": "9. 巨人铸造厂（Giant's Foundry）",
    "10. Flipping / Merchanting": "10. 倒卖/交易（Flipping）",
    "11. Daily GP Routine": "11. 每日GP例行任务（Daily GP Routine）",
    "12. Gear Priority Roadmap": "12. 装备优先级路线图（Gear Priority Roadmap）",
    "13. Endgame Transition Path": "13. 终局过渡路径（Endgame Transition Path）",
    "14. Common Mid-Game Mistakes": "14. 中期常见错误（Common Mid-Game Mistakes）",
    "15. FAQ — Mid-Game Money Making": "15. 常见问题——中期赚钱（FAQ）",
}

for en_text, cn_text in h2_map.items():
    pattern = re.compile(r'(<h2[^>]*>)' + re.escape(en_text) + r'(</h2>)')
    html = pattern.sub(lambda m, ct=cn_text: m.group(1) + ct + m.group(2), html)

# 12. JSON-LD headline
html = re.sub(r'"headline": "[^"]*"', '"headline": "' + cn_title + '"', html)

# 13. mainEntityOfPage
html = re.sub(r'"mainEntityOfPage": "https://osrsguru\.com/guides/' + re.escape(filename) + r'"',
    '"mainEntityOfPage": "https://osrsguru.com/zh/guides/' + filename + '"', html)

os.makedirs(os.path.dirname(dst), exist_ok=True)
with open(dst, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Output size: {len(html)} bytes")
print(f"✅ Done: {filename}")
