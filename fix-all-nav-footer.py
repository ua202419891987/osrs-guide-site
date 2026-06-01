#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复：删除所有导航栏和页脚中的错误链接
直接删除整个错误的导航栏和页脚，替换为正确的
"""

import os
import re

# 攻略文章目录
guides_dir = "C:/Users/Lenovo/osrs-guide-site/guides/"

# 获取所有 HTML 文件
html_files = [f for f in os.listdir(guides_dir) if f.endswith('.html') and f != 'TEMPLATE-high-quality.html']

print(f"找到 {len(html_files)} 个攻略文章文件")

fixed_count = 0

# 正确的导航栏 HTML
correct_nav = '''        <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../money-making.html">Money Making</a></li>
                    <li><a href="../skill-training.html">Skill Training</a></li>
                    <li><a href="../quest-guide.html">Quest Guide</a></li>
                    <li><a href="../boss-killing.html">Boss Guides</a></li>
                </ul>
            </nav>'''

# 正确的页脚 HTML  
correct_footer = '''                <div class="footer-col">
                    <h4>Categories</h4>
                    <ul>
                        <li><a href="../money-making.html">Money Making</a></li>
                        <li><a href="../skill-training.html">Skill Training</a></li>
                        <li><a href="../quest-guide.html">Quest Guides</a></li>
                        <li><a href="../boss-killing.html">Boss Guides</a></li>
                    </ul>
                </div>'''

for filename in html_files:
    filepath = os.path.join(guides_dir, filename)
    
    # 读取文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 替换导航栏（匹配 <nav> 到 </nav> 之间的所有内容）
    nav_pattern = r'<nav>.*?</nav>'
    content = re.sub(nav_pattern, correct_nav, content, flags=re.DOTALL)
    
    # 2. 替换页脚中的 Categories 部分
    footer_pattern = r'<div class="footer-col">\s*<h4>Categories</h4>.*?</div>'
    content = re.sub(footer_pattern, correct_footer, content, flags=re.DOTALL)
    
    # 3. 如果有修改，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"✅ 已修复: {filename}")

print(f"\n📊 总计修复了 {fixed_count} 个文件")
print("✅ 所有导航栏和页脚已替换为正确的链接")
