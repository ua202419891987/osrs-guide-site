#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复攻略文章中的导航栏链接
将所有错误的导航栏链接替换为正确的链接
"""

import os
import re

# 攻略文章目录
guides_dir = "C:/Users/Lenovo/osrs-guide-site/guides/"

# 错误的链接模式 → 正确的链接
replacements = [
    # 导航栏链接错误
    ('href="../guides/index.html"', 'href="../index.html"'),
    ('href="../guides/money-making.html"', 'href="../money-making.html"'),
    ('href="../guides/skill-training.html"', 'href="../skill-training.html"'),
    ('href="../guides/quest-guide.html"', 'href="../quest-guide.html"'),
    ('href="../guides/boss-killing.html"', 'href="../boss-killing.html"'),
    ('href="../guides/skilling.html"', 'href="../skill-training.html"'),
    ('href="../guides/questing.html"', 'href="../quest-guide.html"'),
    ('href="../guides/pvm.html"', 'href="../boss-killing.html"'),
    ('href="../guides/ironman.html"', 'href="../money-making.html"'),
    
    # 页脚链接错误
    ('href="../guides/money-making.html"', 'href="../money-making.html"'),
    ('href="../guides/skill-training.html"', 'href="../skill-training.html"'),
    ('href="../guides/quest-guide.html"', 'href="../quest-guide.html"'),
    ('href="../guides/boss-killing.html"', 'href="../boss-killing.html"'),
]

# 获取所有 HTML 文件
html_files = [f for f in os.listdir(guides_dir) if f.endswith('.html') and f != 'TEMPLATE-high-quality.html']

print(f"找到 {len(html_files)} 个攻略文章文件")

fixed_count = 0

for filename in html_files:
    filepath = os.path.join(guides_dir, filename)
    
    # 读取文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有错误链接
    original_content = content
    for wrong, correct in replacements:
        content = content.replace(wrong, correct)
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"✅ 已修复: {filename}")

print(f"\n📊 总计修复了 {fixed_count} 个文件")
