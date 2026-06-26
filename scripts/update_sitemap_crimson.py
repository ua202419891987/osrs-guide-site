#!/usr/bin/env python3
"""更新 sitemap.xml — 替换 8 个旧 Crimson Desert 条目为全部 43 个"""
import re, os

SITEMAP = r"C:\Users\Lenovo\osrs-guide-site\sitemap.xml"

# 全部 42 篇攻略 + index.html，字母排序
FILES = [
    "crimson-desert-1-10-update-guide-2026.html",
    "crimson-desert-abyss-artifacts-farming-guide-2026.html",
    "crimson-desert-beginner-mistakes-guide-2026.html",
    "crimson-desert-best-settings-performance-2026.html",
    "crimson-desert-best-skills-unlock-first-guide-2026.html",
    "crimson-desert-boss-guide-2026.html",
    "crimson-desert-camp-farm-guide-2026.html",
    "crimson-desert-camp-system-starter-guide-2026.html",
    "crimson-desert-combat-guide-2026.html",
    "crimson-desert-controls-keybindings-guide-2026.html",
    "crimson-desert-cooking-alchemy-recipes-guide-2026.html",
    "crimson-desert-coop-multiplayer-guide-2026.html",
    "crimson-desert-crafting-upgrade-guide-2026.html",
    "crimson-desert-damiane-companion-guide-2026.html",
    "crimson-desert-endgame-guide-2026.html",
    "crimson-desert-first-2-hours-checklist-guide-2026.html",
    "crimson-desert-first-boss-staglord-prep-guide-2026.html",
    "crimson-desert-fishing-guide-2026.html",
    "crimson-desert-hidden-secrets-easter-eggs-2026.html",
    "crimson-desert-inventory-backpack-guide-2026.html",
    "crimson-desert-known-bugs-fixes-guide-2026.html",
    "crimson-desert-matthias-boss-guide-2026.html",
    "crimson-desert-meta-build-tier-list-2026.html",
    "crimson-desert-mini-games-guide-2026.html",
    "crimson-desert-money-farming-guide-2026.html",
    "crimson-desert-mounts-pets-guide-2026.html",
    "crimson-desert-new-player-guide-2026.html",
    "crimson-desert-parry-timing-dodge-guide-2026.html",
    "crimson-desert-patch-notes-analysis-2026.html",
    "crimson-desert-pre-boss-gear-checklist-guide-2026.html",
    "crimson-desert-pvp-arena-guide-2026.html",
    "crimson-desert-quest-walkthrough-2026.html",
    "crimson-desert-resource-farming-guide-2026.html",
    "crimson-desert-resource-gathering-routes-guide-2026.html",
    "crimson-desert-roadmap-dlc-guide-2026.html",
    "crimson-desert-skills-builds-guide-2026.html",
    "crimson-desert-staglord-boss-strategy-guide-2026.html",
    "crimson-desert-stamina-management-guide-2026.html",
    "crimson-desert-tenebrum-boss-guide-2026.html",
    "crimson-desert-treasure-map-locations-guide-2026.html",
    "crimson-desert-weapon-combos-beginner-guide-2026.html",
    "crimson-desert-weapons-gear-guide-2026.html",
    "index.html",
]

BASE = "https://osrsguru.com/guides/crimson-desert"
TODAY = "2026-06-25"

with open(SITEMAP, "r", encoding="utf-8") as f:
    content = f.read()

# 匹配旧 Crimson Desert 区块 —— 从第一个到最后一个
old_start = content.index('<url><loc>https://osrsguru.com/guides/crimson-desert/')
# 找到最后一个 Crimson Desert 条目的结束位置
old_end_marker = 'crimson-desert-patch-notes-analysis-2026.html</loc>'
old_end = content.index(old_end_marker) + len(old_end_marker) + len('</url>\n')

# 构建新条目
new_entries = []
for f in FILES:
    priority = "0.80" if f == "index.html" else "0.85"
    new_entries.append(
        f'  <url><loc>{BASE}/{f}</loc>'
        f'<lastmod>{TODAY}</lastmod>'
        f'<priority>{priority}</priority>'
        f'<changefreq>weekly</changefreq></url>'
    )

new_block = "\n".join(new_entries) + "\n"
new_content = content[:old_start] + new_block + content[old_end:]

with open(SITEMAP, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"✅ sitemap.xml 已更新")
print(f"   旧条目: 8 个 Crimson Desert")
print(f"   新条目: {len(FILES)} 个（42 篇攻略 + index.html）")
print(f"   lastmod: {TODAY}")

# 验证
with open(SITEMAP, "r", encoding="utf-8") as f:
    verify = f.read()
count = verify.count("crimson-desert")
print(f"   验证: sitemap 中现有 {count} 个 crimson-desert 条目")
