#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准替换所有 HTML 文件中的 Emoji 为 Font Awesome 图标
"""

from pathlib import Path
import re

BASE_DIR = Path("C:/Users/Lenovo/osrs-guide-site/")
GUIDES_DIR = BASE_DIR / "guides"

# Emoji → Font Awesome 映射
EMOJI_MAP = {
    "💰": '<i class="fas fa-coins"></i>',
    "🗡️": '<i class="fas fa-skull-crossbones"></i>',
    "⚔️": '<i class="fas fa-sword"></i>',  # 技能训练
    "🛡️": '<i class="fas fa-shield-alt"></i>',
    "📜": '<i class="fas fa-scroll"></i>',
    "🏆": '<i class="fas fa-trophy"></i>',
    "👹": '<i class="fas fa-dragon"></i>',  # Boss
    "🎯": '<i class="fas fa-bullseye"></i>',
    "⚡": '<i class="fas fa-bolt"></i>',
    "🔥": '<i class="fas fa-fire"></i>',
    "📦": '<i class="fas fa-box"></i>',
    "🏪": '<i class="fas fa-store"></i>',
    "💎": '<i class="fas fa-gem"></i>',
    "🪓": '<i class="fas fa-axe"></i>',  # 伐木
    "🎣": '<i class="fas fa-fish"></i>',
    "⛏️": '<i class="fas fa-pickaxe"></i>',
    "🧵": '<i class="fas fa-scissors"></i>',
    "🍳": '<i class="fas fa-egg"></i>',
    "🧪": '<i class="fas fa-flask"></i>',
    "📊": '<i class="fas fa-chart-bar"></i>',
    "🏃": '<i class="fas fa-running"></i>',
    "🐦": '<i class="fas fa-dove"></i>',  # 狩猎
    "🧙": '<i class="fas fa-hat-wizard"></i>',
    "🗝️": '<i class="fas fa-key"></i>',
    "🏰": '<i class="fas fa-chess-rook"></i>',
    "🚪": '<i class="fas fa-door-open"></i>',
    "📦": '<i class="fas fa-box-open"></i>',
    "✅": '<i class="fas fa-check-circle"></i>',
    "❌": '<i class="fas fa-times-circle"></i>',
    "⭐": '<i class="fas fa-star"></i>',
    "🔸": '<i class="fas fa-square"></i>',
    "🔹": '<i class="fas fa-square"></i>',
}

def remove_emojis():
    fixed = 0
    total_emojis = 0
    
    all_files = list(BASE_DIR.glob("*.html")) + list(GUIDES_DIR.glob("*.html"))
    
    for html_file in all_files:
        if "TEMPLATE" in html_file.name or "template" in html_file.name:
            continue
        
        content = html_file.read_text(encoding="utf-8")
        original = content
        
        # 替换已知 Emoji
        for emoji, fa_icon in EMOJI_MAP.items():
            if emoji in content:
                content = content.replace(emoji, fa_icon)
                total_emojis += 1
        
        # 用正则去掉剩余的 Emoji（Unicode 范围）
        # 匹配常见 Emoji Unicode 范围
        emoji_re = re.compile(
            r'[\U0001F000-\U0001FAFF'
            r'\U00002600-\U000027BF'
            r'\U0001F300-\U0001F9FF'
            r'\U0001FA00-\U0001FA6F'
            r'\U0001F910-\U0001F96B'
            r'\U0001F680-\U0001F6FF]+',
            re.UNICODE
        )
        remaining = emoji_re.findall(content)
        if remaining:
            print(f"  ⚠️  {html_file.name} 有未处理的 Emoji: {remaining[:3]}")
            # 用空格替换剩余 Emoji
            content = emoji_re.sub('', content)
        
        if content != original:
            html_file.write_text(content, encoding="utf-8")
            fixed += 1
    
    print(f"✅ 处理了 {total_emojis} 个已知 Emoji")
    print(f"✅ 修改了 {fixed} 个文件")
    return fixed

if __name__ == "__main__":
    print("=== 开始清理所有 Emoji ===\n")
    remove_emojis()
    print("\n🎉 完成！")
