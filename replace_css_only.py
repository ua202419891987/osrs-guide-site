#!/usr/bin/env python3
"""为所有30篇文章替换完整的CSS覆盖块"""

import re
import os

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

# 读取完整CSS块
with open(r"C:\Users\Lenovo\osrs-guide-site\css_override_complete.html", "r", encoding="utf-8") as f:
    CSS_COMPLETE = f.read().strip()

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

def replace_css_block(content):
    """替换<style>块为完整版"""
    # 查找 <style> 开始位置
    style_start = content.rfind("<style>")
    if style_start == -1:
        # 没有现有style块，在</body>前添加
        return content.replace("</body>", CSS_COMPLETE + "\n</body>")
    
    # 查找 </style> 结束位置
    style_end = content.find("</style>", style_start)
    if style_end == -1:
        return content  # 格式错误，不修改
    
    style_end += 8  # 包含 </style>
    
    # 替换整个 style 块
    new_content = content[:style_start] + CSS_COMPLETE + "\n" + content[style_end:]
    return new_content

def fix_file(filename):
    """修复单个文件的CSS块"""
    filepath = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ {filename}: 文件不存在")
        return False
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    new_content = replace_css_block(content)
    
    if new_content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ {filename}: CSS块已替换")
        return True
    else:
        print(f"⏭️ {filename}: CSS块无需修改")
        return False

def main():
    success = 0
    skipped = 0
    
    for f in FILES:
        if fix_file(f):
            success += 1
        else:
            skipped += 1
    
    print(f"\n{'='*60}")
    print(f"CSS块替换完成：{success+skipped}/{len(FILES)}")
    print(f"成功：{success} 篇，无需修改：{skipped} 篇")

if __name__ == "__main__":
    main()
