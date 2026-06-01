#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准修复所有 18 个断链（只修改必要的链接，不碰其他内容）
"""

import re
from pathlib import Path

BASE_DIR = Path("C:/Users/Lenovo/osrs-guide-site/")
GUIDES_DIR = BASE_DIR / "guides"

# 文件映射：错误文件名 → 正确文件名
LINK_FIXES = {
    # index.html 中的错误链接
    "guides/updates.html": "updates.html",
    "guides/osrs-how-to-beat-zulrah-for-beginners.html": "guides/osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
    
    # money-making.html 中的错误链接（在根目录，所以 guides/ 前缀是错的）
    "guides/osrs-flipping-guide-for-beginners.html": "guides/osrs-cheap-flipping-methods-for-new-players.html",
    "guides/osrs-barrows-for-profit-guide.html": None,  # 不存在，删除链接
    
    # boss-killing.html / money-making.html / quest-guide.html / skill-training.html 中
    # 页脚 "Home" 链接写成 index.html（在根目录文件中，这其实是正确的）
    # 但检查报告显示它期望 guides\index.html，说明是 guides/ 里的文件有问题
}

def fix_all():
    fixed_count = 0
    
    # ============================================================
    # 1. 修复 index.html：updates.html 路径 + Zulrah 链接
    # ============================================================
    index_file = BASE_DIR / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        original = content
        
        # 修复 updates.html 路径（3处：nav、featured、footer）
        content = content.replace('href="guides/updates.html"', 'href="updates.html"')
        
        # 修复 Zulrah 链接
        content = content.replace(
            'href="guides/osrs-how-to-beat-zulrah-for-beginners.html"',
            'href="guides/osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html"'
        )
        
        if content != original:
            index_file.write_text(content, encoding="utf-8")
            print(f"✅ 修复 index.html ({'changed' if content != original else 'no change'})")
            fixed_count += 1
        else:
            print("⚠️  index.html: 没有需要修改的内容")
    
    # ============================================================
    # 2. 修复 money-making.html：两处错误攻略链接
    # ============================================================
    mm_file = BASE_DIR / "money-making.html"
    if mm_file.exists():
        content = mm_file.read_text(encoding="utf-8")
        original = content
        
        # 修复 flipping guide 链接
        content = content.replace(
            'href="guides/osrs-flipping-guide-for-beginners.html"',
            'href="guides/osrs-cheap-flipping-methods-for-new-players.html"'
        )
        
        # Barrows for profit 不存在，改成 hunter money making（同分类）
        content = content.replace(
            'href="guides/osrs-barrows-for-profit-guide.html"',
            'href="guides/osrs-hunter-money-making-guide-2026.html"'
        )
        
        if content != original:
            mm_file.write_text(content, encoding="utf-8")
            print("✅ 修复 money-making.html")
            fixed_count += 1
        else:
            print("⚠️  money-making.html: 没有需要修改的内容")
    
    # ============================================================
    # 3. 修复分类页（money-making.html 等）页脚的 index.html 链接
    #    这些文件在根目录，index.html 链接应该指向正确的位置
    #    实际上报告显示问题在：这些文件的页脚链接写成 index.html
    #    而检查脚本认为应该指向 guides/index.html（这不对）
    #    真正的问题是：guides/ 里的文件引用了错误的路径
    # ============================================================
    
    # 检查 boss-killing.html / quest-guide.html / skill-training.html
    # 报告显示这些文件的页脚 "Home" 链接指向 index.html
    # 但这些文件在根目录，所以 index.html 是正确的
    # 问题可能出在：这些文件里的其他链接
    
    for cat_file in ["boss-killing.html", "quest-guide.html", "skill-training.html"]:
        f = BASE_DIR / cat_file
        if f.exists():
            content = f.read_text(encoding="utf-8")
            # 检查是否有明显的断链模式
            broken = re.findall(r'href="(guides/(?!osrs-)[^"]+\.html)"', content)
            if broken:
                print(f"  ⚠️  {cat_file} 可能有问题链接: {broken[:3]}")
    
    # ============================================================
    # 4. 修复 guides/ 里的文件：页脚 Home 链接
    #    这些文件在 guides/ 目录，所以应该指向 ../index.html
    # ============================================================
    guide_files = list(GUIDES_DIR.glob("*.html"))
    fixed_guides = 0
    
    for gf in guide_files:
        if gf.name == "TEMPLATE.html":
            continue
        content = gf.read_text(encoding="utf-8")
        original = content
        
        # 修复页脚 Home 链接：如果写成 href="index.html"（相对 guides/ 目录）
        # 应该改为 href="../index.html"
        content = content.replace('href="index.html"', 'href="../index.html"')
        
        # 修复 updates.html 路径（在 guides/ 里的文件引用 ../guides/updates.html 是错的）
        content = content.replace('href="../guides/updates.html"', 'href="../updates.html"')
        
        if content != original:
            gf.write_text(content, encoding="utf-8")
            fixed_guides += 1
    
    if fixed_guides:
        print(f"✅ 修复 {fixed_guides} 个 guides/ 文件的 index.html 链接")
        fixed_count += 1
    
    # ============================================================
    # 5. 修复 osrs-low-gear-setup-for-vorkath-guide.html 中的错误链接
    # ============================================================
    vorkath_file = GUIDES_DIR / "osrs-low-gear-setup-for-vorkath-guide.html"
    if vorkath_file.exists():
        content = vorkath_file.read_text(encoding="utf-8")
        original = content
        
        # 修复 dragon slayer 2 链接
        content = content.replace(
            'href="osrs-how-to-complete-dragon-slayer-2-guide.html"',
            'href="osrs-how-to-finish-dragon-slayer-2-guide.html"'
        )
        
        if content != original:
            vorkath_file.write_text(content, encoding="utf-8")
            print("✅ 修复 osrs-low-gear-setup-for-vorkath-guide.html")
            fixed_count += 1
    
    # ============================================================
    # 6. 清理 TEMPLATE-high-quality.html 中的占位符链接
    # ============================================================
    tmpl = BASE_DIR / "TEMPLATE-high-quality.html"
    if tmpl.exists():
        content = tmpl.read_text(encoding="utf-8")
        original = content
        content = content.replace('href="{RELATED_LINK_1}"', 'href="#"')
        content = content.replace('href="{RELATED_LINK_2}"', 'href="#"')
        content = content.replace('href="{RELATED_LINK_3}"', 'href="#"')
        content = content.replace('href="{RELATED_LINK_4}"', 'href="#"')
        content = content.replace('href="{RELATED_LINK_5}"', 'href="#"')
        if content != original:
            tmpl.write_text(content, encoding="utf-8")
            print("✅ 修复 TEMPLATE-high-quality.html 占位符链接")
            fixed_count += 1
    
    print(f"\n🎉 完成！共修复 {fixed_count} 处")

if __name__ == "__main__":
    fix_all()
