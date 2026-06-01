#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修正OSRS攻略HTML文件的问题
问题1: nav链接路径错误（缺少/guides/前缀）
问题2: canonical链接还是占位符
问题3: 英文拼写错误（can't, doesn't等）
"""

import os
import re

# 要修正的10篇文件
files = [
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-low-effort-money-making-for-beginners.html",
    "osrs-how-to-make-gold-with-fishing-2026.html",
    "osrs-f2p-money-making-no-stats-required.html",
    "osrs-passive-money-making-while-offline.html",
    "osrs-cheap-flipping-methods-for-new-players.html",
    "osrs-hunter-money-making-guide-2026.html",
    "osrs-how-to-make-money-with-crafting-low-level.html",
    "osrs-wintertodt-money-making-per-hour.html",
    "osrs-chambers-of-xeric-loot-profit-guide.html"
]

# 真实域名
REAL_DOMAIN = "https://osrsguide.com"

def fix_file(filename):
    filepath = os.path.join("/c/Users/Lenovo/osrs-guide-site/guides", filename)
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filename}")
        return False
    
    # 读取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_applied = []
    
    # 问题1: 修正nav链接路径
    patterns = [
        (r'href="\.\./money-making\.html"', 'href="../guides/money-making.html"'),
        (r'href="\.\./skill-training\.html"', 'href="../guides/skill-training.html"'),
        (r'href="\.\./quest-guide\.html"', 'href="../guides/quest-guide.html"'),
        (r'href="\.\./boss-killing\.html"', 'href="../guides/boss-killing.html"')
    ]
    
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            fixes_applied.append("nav链接路径")
            content = new_content
            break  # 只报告一次
    
    # 问题2: 修正canonical链接
    if 'https://yourdomain.com' in content:
        content = content.replace('https://yourdomain.com', REAL_DOMAIN)
        fixes_applied.append("canonical链接")
    
    # 问题3: 修正拼写错误
    spelling_fixes = [
        (r"does't", "doesn't"),
        (r"won't", "won't"),
        (r"don't", "don't"),
        (r"can't", "can't"),  # 确保正确
        (r"it's", "it's"),
        (r"you're", "you're"),
        (r"they're", "they're"),
        (r"that's", "that's"),
        (r"overpriced", "overpriced"),  # 修正拼写
    ]
    
    for wrong, correct in spelling_fixes:
        if re.search(wrong, content, re.IGNORECASE):
            content = re.sub(wrong, correct, content, flags=re.IGNORECASE)
            if "拼写" not in str(fixes_applied):
                fixes_applied.append("拼写错误")
    
    # 保存文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} - 已修正: {', '.join(set(fixes_applied))}")
        return True
    else:
        print(f"⚠️  {filename} - 无需修正")
        return False

def main():
    print("🔧 开始批量修正HTML文件...\n")
    
    fixed_count = 0
    for filename in files:
        if fix_file(filename):
            fixed_count += 1
    
    print(f"\n🎉 完成！共修正 {fixed_count}/{len(files)} 个文件")

if __name__ == "__main__":
    main()
