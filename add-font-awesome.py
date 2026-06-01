#!/usr/bin/env python3
"""
在所有 HTML 文件中引入 Font Awesome，并替换 Emoji 为 Font Awesome 图标
"""

import os
import re
import glob

def add_font_awesome(html_file):
    """在 <head> 中添加 Font Awesome CDN"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有 Font Awesome
        if 'font-awesome' in content.lower() or 'fontawesome' in content.lower():
            # print(f"⏭️  跳过 (已有 Font Awesome): {html_file}")
            return False
        
        # 在 </head> 前插入 Font Awesome CDN
        fa_cdn = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n'
        
        # 找到 </head> 位置
        head_end = content.find('</head>')
        if head_end == -1:
            # 如果没有 </head>，尝试在 <head> 末尾添加
            head_start = content.find('<head>')
            if head_start == -1:
                print(f"⚠️  找不到 <head>: {html_file}")
                return False
            # 在 <head> 标签后添加
            insert_pos = head_start + len('<head>')
            new_content = content[:insert_pos] + '\n' + fa_cdn + content[insert_pos:]
        else:
            # 在 </head> 前添加
            new_content = content[:head_end] + fa_cdn + content[head_end:]
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已添加 Font Awesome: {html_file}")
        return True
            
    except Exception as e:
        print(f"❌ 错误: {html_file} - {e}")
        return False

def replace_emojis_with_fa(html_file):
    """替换 Emoji 为 Font Awesome 图标"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Emoji → Font Awesome 映射表
        emoji_map = {
            '💰': '<i class="fas fa-coins"></i>',
            '🗡️': '<i class="fas fa-skull-crossbones"></i>',
            '🛡️': '<i class="fas fa-shield-alt"></i>',
            '📜': '<i class="fas fa-scroll"></i>',
            '🏆': '<i class="fas fa-trophy"></i>',
            '⚔️': '<i class="fas fa-sword"></i>',
            '🧭': '<i class="fas fa-compass"></i>',
            '🎯': '<i class="fas fa-bullseye"></i>',
            '📦': '<i class="fas fa-box"></i>',
            '🏹': '<i class="fas fa-bow-arrow"></i>',
            '🧙': '<i class="fas fa-hat-wizard"></i>',
            '🐉': '<i class="fas fa-dragon"></i>',
            '💎': '<i class="fas fa-gem"></i>',
        }
        
        original_content = content
        
        # 替换 Emoji
        for emoji, fa_icon in emoji_map.items():
            content = content.replace(emoji, fa_icon)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已替换 Emoji: {html_file}")
            return True
        else:
            # print(f"⏭️  跳过 (无 Emoji): {html_file}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {html_file} - {e}")
        return False

def main():
    added_fa_count = 0
    replaced_emoji_count = 0
    total_count = 0
    
    # 1. 处理根目录的 HTML 文件
    print("=== 处理根目录 HTML 文件 ===\n")
    for html_file in glob.glob("*.html"):
        total_count += 1
        
        # 添加 Font Awesome
        if add_font_awesome(html_file):
            added_fa_count += 1
        
        # 替换 Emoji
        if replace_emojis_with_fa(html_file):
            replaced_emoji_count += 1
    
    # 2. 处理 guides/ 目录中的 HTML 文件
    print("\n=== 处理 guides/ 目录中的 HTML 文件 ===\n")
    for html_file in glob.glob("guides/*.html"):
        total_count += 1
        
        # 添加 Font Awesome
        if add_font_awesome(html_file):
            added_fa_count += 1
        
        # 替换 Emoji
        if replace_emojis_with_fa(html_file):
            replaced_emoji_count += 1
    
    print(f"\n=== 完成 ===")
    print(f"总文件数: {total_count}")
    print(f"已添加 Font Awesome: {added_fa_count}")
    print(f"已替换 Emoji: {replaced_emoji_count}")

if __name__ == "__main__":
    main()
