#!/usr/bin/env python3
"""诊断30篇文件的格式问题"""

import os

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

FILES = [
    "osrs-money-making-beginner-2026.html",
    "osrs-new-player-guide-2026.html",
    "osrs-slayer-beginner-guide-2026.html",
    "osrs-money-making-zero-req-2026.html",
    "osrs-1-99-prayer-guide-2026.html",
    "osrs-barrows-tunnel-optimization-2026.html",
    "osrs-f2p-gear-progression-guide-2026.html",
    "osrs-diary-priority-order-beginner-2026.html",
    "osrs-clue-scrolls-beginner-guide-2026.html",
    "osrs-common-beginner-mistakes-avoid-2026.html",
    "osrs-combat-training-beginner-2026.html",
    "osrs-prayer-training-beginner-guide-2026.html",
    "osrs-1-99-mining-guide-beginner-2026.html",
    "osrs-1-99-farming-guide-beginner-profit-2026.html",
    "osrs-1-99-woodcutting-guide-early-game.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
    "osrs-skill-training-beginner-complete-guide-2026.html",
    "osrs-skill-training-beginner-fast-track-2026.html",
    "osrs-efficient-training-routes-beginners-2026.html",
    "osrs-low-level-skilling-money-makers-2026.html",
    "osrs-f2p-combat-training-guide-2026.html",
    "osrs-f2p-leveling-guide-2026.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-quests-before-membership-2026.html",
    "osrs-f2p-slayer-guide-2026.html",
    "osrs-f2p-to-member-first-10-things-2026.html",
    "osrs-first-boss-progression-roadmap-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
    "osrs-gear-beginner-guide-2026.html",
]

for f in FILES:
    filepath = os.path.join(BASE_DIR, f)
    if not os.path.exists(filepath):
        print("FILE NOT FOUND: " + f)
        continue
    
    with open(filepath, "r", encoding="utf-8") as fp:
        content = fp.read()
    
    issues = []
    
    # Problem C1: 旧版结构
    if '<div class="container guide-content"' in content:
        issues.append("C1(div.container.guide-content)")
    if '<main class="guide-main guide-content"' in content:
        issues.append("C1(main.guide-main.guide-content)")
    
    # Problem C2: TOC 类名
    if 'class="table-of-contents"' in content or '<nav class="table-of-contents"' in content:
        issues.append("C2(table-of-contents)")
    
    # Problem A: Quick Summary 边框 #ebe5f0
    if "#ebe5f0" in content.lower() and "quick-summary" in content.lower():
        # 检查是否在 quick-summary 的 style 中
        import re
        qs_match = re.search(r'<div class="quick-summary"[^>]*style="[^"]*"', content, re.IGNORECASE)
        if qs_match and "#ebe5f0" in qs_match.group(0).lower():
            issues.append("A(QS边框#ebe5f0)")
    
    # Step 4: #ebe5f0 残留（在任何位置）
    if "#ebe5f0" in content or "#EBE5F0" in content:
        issues.append("Step4(#ebe5f0残留)")
    
    # Step 3: CSS 覆盖块
    has_css_block = False
    style_pos = content.rfind("<style>")
    if style_pos != -1:
        # 检查这个 <style> 是否包含 .guide-content 规则
        end_style = content.find("</style>", style_pos)
        if end_style != -1:
            style_content = content[style_pos:end_style]
            if ".guide-content" in style_content:
                has_css_block = True
    
    if not has_css_block:
        issues.append("Step3(缺失CSS覆盖)")
    
    # Problem B: border-left 内联样式
    if "border-left:4px" in content or "border-left: 4px" in content or "border-left:3px" in content:
        issues.append("B(border-left内联)")
    
    if issues:
        print(f + ": " + ", ".join(issues))
    else:
        print(f + ": OK (无需修改)")

print("\n诊断完成")
