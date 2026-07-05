#!/usr/bin/env python3
"""
Fix two files missing cn-title: herb run mastery and ironman f2p
"""
import re, os

BASE = "c:/Users/Lenovo/osrs-guide-site"

# ========== Fix 1: osrs-herb-run-mastery-guide-2026.html ==========
f1 = "osrs-herb-run-mastery-guide-2026.html"
path1 = os.path.join(BASE, "zh", "guides", f1)

with open(path1, "r", encoding="utf-8") as f:
    html1 = f.read()

# Add cn-title/cn-summary before the h1 inside hero-image
cn_title1 = "OSRS 2026草药跑精通指南 — 最佳利润、地块与路线"
cn_summary1 = "草药跑是OSRS中最被忽视的赚钱方法之一。5分钟即可获得15万-80万GP利润。本指南将教您从32级 Farming 开始，掌握9地块最优路线，选择合适的草药种子，实现被动日入数百万。"

cn_block1 = (
    '<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">'
    + cn_title1
    + '</h1>\n      <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">'
    + cn_summary1
    + '</p>\n      '
)

# Insert before <h1 style="font-size:clamp...
html1 = re.sub(
    r'(<div class="hero-image"[^>]*>.*?<div[^>]* style="text-align:center[^>]*>)'
    r'(<h1[^>]*>)',
    lambda m: m.group(1) + '\n' + cn_block1 + m.group(2),
    html1,
    flags=re.DOTALL
)

with open(path1, "w", encoding="utf-8") as f:
    f.write(html1)

print(f"✅ Fixed {f1}")

# ========== Fix 2: osrs-ironman-money-making-f2p-2026.html ==========
f2 = "osrs-ironman-money-making-f2p-2026.html"
path2 = os.path.join(BASE, "zh", "guides", f2)

with open(path2, "r", encoding="utf-8") as f:
    html2 = f.read()

# Add cn-title/cn-summary before the h1 inside article-hero
cn_title2 = "OSRS 2026铁人模式F2P赚钱攻略 — 最佳方法指南"
cn_summary2 = "2026年OSRS铁人模式F2P赚钱完整指南——从奶牛到符文矿石。8种按GP/小时排名的方法，涵盖牛皮、巨人之山、大恶魔和符文矿开采。"

cn_block2 = (
    '<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">'
    + cn_title2
    + '</h1>\n    <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">'
    + cn_summary2
    + '</p>\n    '
)

# Insert before <h1 class="article-title">...
html2 = re.sub(
    r'(<section class="article-hero">.*?<div class="container">.*?)'
    r'(<h1[^>]* class="article-title"[^>]*>)',
    lambda m: m.group(1) + '\n' + cn_block2 + m.group(2),
    html2,
    flags=re.DOTALL
)

with open(path2, "w", encoding="utf-8") as f:
    f.write(html2)

print(f"✅ Fixed {f2}")
