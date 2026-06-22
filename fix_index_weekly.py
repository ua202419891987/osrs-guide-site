#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复首页index.html的Weekly Updates卡片：
1. 更新预览文字（从第367-368行）
2. 更新计数（从第370行：9 → 11）
"""

import re

filepath = r"C:\Users\Lenovo\osrs-guide-site\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复1：更新预览文字
old_preview = """          <span>⚔️ Viggora Chainmace</span>
          <span>🦌 1-99 Hunter Guide</span>
          <span>🎯 Complete Training Roadmap</span>"""

new_preview = """          <span>⚔️ Viggora Chainmace</span>
          <span>🦌 Hunter P1 Upgraded</span>
          <span>🎯 Ironman Cape Analysis</span>"""

if old_preview in content:
    content = content.replace(old_preview, new_preview)
    print("✅ 预览文字已更新")
else:
    print("⚠️ 未找到预览文字，尝试模糊匹配...")
    # 模糊匹配（忽略空格差异）
    if "🦌 1-99 Hunter Guide" in content:
        content = content.replace("🦌 1-99 Hunter Guide", "🦌 Hunter P1 Upgraded")
        print("✅ 已模糊修复预览文字1")
    if "🎯 Complete Training Roadmap" in content:
        content = content.replace("🎯 Complete Training Roadmap", "🎯 Ironman Cape Analysis")
        print("✅ 已模糊修复预览文字2")

# 修复2：更新计数
old_count = '<span class="game-cat-count">9 New This Week</span>'
new_count = '<span class="game-cat-count">11 New This Week</span>'

if old_count in content:
    content = content.replace(old_count, new_count)
    print("✅ 计数已更新：9 → 11")
else:
    print("⚠️ 未找到计数，尝试模糊匹配...")
    if "9 New This Week" in content:
        content = content.replace("9 New This Week", "11 New This Week")
        print("✅ 已模糊修复计数")

# 保存
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 首页index.html已更新！")
print("📝 修改内容：")
print("  1. Weekly Updates卡片预览文字 → Hunter P1 Upgraded + Ironman Cape Analysis")
print("  2. 计数 → 9 New This Week → 11 New This Week")
