#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试H2匹配 - 读取max-cape文件并打印H2标签内容"""
import re

filepath = "C:/Users/Lenovo/osrs-guide-site/zh/guides/max-cape-route-2026.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 打印所有H2标签行
for i, line in enumerate(content.split('\n')):
    if '<h2>' in line:
        print(f"Line {i+1}: {line.strip()}")

print("\n\n--- 测试正则匹配 ---")
eng_title = "Overall Strategy & Philosophy"
pattern = re.compile(r'(<h2[^>]*>)' + re.escape(eng_title) + r'(</h2>)')
matches = pattern.findall(content)
print(f"匹配 {eng_title}: {len(matches)} 个")
if matches:
    print(f"  完整匹配: {matches[0]}")
