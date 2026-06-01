#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理攻略文章中的"相关攻略"链接
方案：删除整个"相关攻略"部分（因为链接大多指向不存在的文件）
"""

import os
import re

# 攻略文章目录
guides_dir = "C:/Users/Lenovo/osrs-guide-site/guides/"

# 获取所有 HTML 文件
html_files = [f for f in os.listdir(guides_dir) if f.endswith('.html') and f != 'TEMPLATE-high-quality.html']

print(f"找到 {len(html_files)} 个攻略文章文件")

fixed_count = 0

for filename in html_files:
    filepath = os.path.join(guides_dir, filename)
    
    # 读取文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 删除"Related Guides"部分（包括几种可能的标题）
    patterns = [
        r'<section class="related-guides">.*?</section>',
        r'<div class="related-guides">.*?</div>',
        r'<h3>Related Guides</h3>.*?</div>',
        r'<h3>📚 Related Guides</h3>.*?</section>',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 如果有修改，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"✅ 已删除相关攻略部分: {filename}")

print(f"\n📊 总计修复了 {fixed_count} 个文件")
print("\n💡 建议：相关攻略部分已删除，避免指向不存在的文件")
