#!/usr/bin/env python3
"""
批量修复 guides/ 目录中 HTML 文件里的错误攻略文章链接
"""

import os
import re
import glob

def fix_guide_links(html_file):
    """修复单个 HTML 文件中的攻略文章链接"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 攻略文件名映射表（错误 → 正确）
        guide_mapping = {
            'osrs-fastest-99-agility-guide-2026.html': 'osrs-how-to-get-99-agility-fast-2026.html',
            'osrs-low-gear-setup-for-vorkath-guide.html': 'osrs-low-gear-setup-for-vorkath-guide.html',
            'osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html': 'osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html',
            'osrs-how-to-solo-god-wars-boss-for-beginners.html': 'osrs-how-to-solo-god-wars-boss-for-beginners.html',
            'osrs-ironman-money-making-early-game.html': 'osrs-f2p-ironman-money-making-early-game.html',
            'osrs-how-to-get-dragon-defender-2026.html': 'osrs-how-to-get-dragon-defender-2026.html',
            'osrs-how-to-complete-lost-city-guide.html': 'osrs-how-to-complete-lost-city-guide.html',
            'osrs-how-to-unlock-fairy-rings-quick-guide.html': 'osrs-how-to-unlock-fairy-rings-quick-guide.html',
            'osrs-how-to-get-to-fossil-island-quick-guide.html': 'osrs-how-to-get-to-fossil-island-quick-guide.html',
            'osrs-cheapest-99-runecrafting-2026.html': 'osrs-cheapest-99-runecrafting-2026.html',
            'osrs-low-cost-1-99-herblore-guide.html': 'osrs-low-cost-1-99-herblore-guide.html',
            'osrs-how-to-get-cowhides-early-game-guide.html': 'osrs-f2p-ironman-money-making-early-game.html',
        }
        
        # 批量替换
        for wrong, correct in guide_mapping.items():
            content = content.replace(f'href="{wrong}"', f'href="{correct}"')
            content = content.replace(f'href="../{wrong}"', f'href="../{correct}"')
            content = content.replace(f'href="guides/{wrong}"', f'href="guides/{correct}"')
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复: {html_file}")
            return True
        else:
            # print(f"⏭️  跳过 (无需修复): {html_file}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {html_file} - {e}")
        return False

def main():
    fixed_count = 0
    total_count = 0
    
    # 处理 guides/ 目录中的 HTML 文件
    print("=== 修复 guides/ 目录中的攻略文章链接 ===\n")
    for html_file in glob.glob("guides/*.html"):
        total_count += 1
        if fix_guide_links(html_file):
            fixed_count += 1
    
    print(f"\n=== 修复完成 ===")
    print(f"总文件数: {total_count}")
    print(f"已修复: {fixed_count}")
    print(f"无需修复: {total_count - fixed_count}")

if __name__ == "__main__":
    main()
