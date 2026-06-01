#!/usr/bin/env python3
"""
批量修复 money-making.html 中的错误链接
根据实际文件名更新所有链接
"""

import os
import re

# 文件名映射表（错误的链接 → 正确的文件名）
FILE_MAPPING = {
    'osrs-f2p-money-making-2026.html': 'osrs-f2p-ironman-money-making-early-game.html',
    'osrs-p2p-money-making-for-beginners.html': 'osrs-p2p-money-making-for-beginners.html',  # 需要确认
    'osrs-ironman-money-making-f2p-2026.html': 'osrs-ironman-money-making-f2p-2026.html',  # 正确
    'osrs-crafting-for-profit-2026.html': 'osrs-crafting-for-profit-2026.html',  # 需要确认
    'osrs-farming-for-profit-2026.html': 'osrs-farming-for-profit-2026.html',  # 需要确认
    'osrs-slayer-money-making-early-game.html': 'osrs-slayer-money-making-early-game.html',  # 需要确认
    'osrs-hunter-money-making-guide-2026.html': 'osrs-hunter-money-making-guide-2026.html',  # 正确
    'osrs-fishing-for-profit-2026.html': 'osrs-fishing-for-profit-2026.html',  # 需要确认
    'osrs-woodcutting-for-profit-2026.html': 'osrs-woodcutting-for-profit-2026.html',  # 需要确认
    'osrs-mining-for-profit-2026.html': 'osrs-mining-for-profit-2026.html',  # 需要确认
    'osrs-thieving-for-profit-2026.html': 'osrs-thieving-for-profit-2026.html',  # 需要确认
    'osrs-pvm-for-profit-2026.html': 'osrs-pvm-for-profit-2026.html',  # 需要确认
    'osrs-flipping-guide-for-beginners.html': 'osrs-cheap-flipping-methods-for-new-players.html',  # 可能正确
    'osrs-barrows-for-profit-guide.html': 'osrs-barrows-for-profit-guide.html',  # 需要确认
    'osrs-zulrah-for-profit-2026.html': 'osrs-zulrah-for-profit-2026.html'  # 需要确认
}

def find_correct_filename(wrong_filename, guides_dir):
    """根据实际文件名模糊匹配正确的文件名"""
    # 移除路径和扩展名
    wrong_base = os.path.splitext(os.path.basename(wrong_filename))[0]
    
    # 获取所有实际文件名
    actual_files = [f for f in os.listdir(guides_dir) if f.endswith('.html')]
    
    # 尝试精确匹配
    if wrong_filename in actual_files:
        return wrong_filename
    
    # 尝试模糊匹配（提取关键词）
    keywords = wrong_base.replace('osrs-', '').replace('-guide', '').replace('-for-', ' ').split('-')
    
    best_match = None
    best_score = 0
    
    for actual_file in actual_files:
        actual_base = os.path.splitext(actual_file)[0]
        score = 0
        
        # 计算关键词匹配数
        for keyword in keywords:
            if keyword in actual_base:
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = actual_file
    
    return best_match

def fix_money_making_links(file_path, guides_dir):
    """修复 money-making.html 中的错误链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到所有 guides/ 开头的链接
    links = re.findall(r'href="guides/([^"]+)"', content)
    
    fixed_count = 0
    error_count = 0
    
    print(f"找到 {len(links)} 个链接")
    print()
    
    for link in links:
        wrong_path = f"guides/{link}"
        
        # 检查文件是否存在
        if os.path.exists(os.path.join(guides_dir, link)):
            print(f"✅ {link} - 文件存在")
            continue
        
        # 文件不存在，尝试找到正确的文件名
        correct_file = find_correct_filename(link, guides_dir)
        
        if correct_file:
            correct_path = f"guides/{correct_file}"
            old_link = f'href="guides/{link}"'
            new_link = f'href="guides/{correct_file}"'
            
            content = content.replace(old_link, new_link)
            print(f"🔧 修复: {link} → {correct_file}")
            fixed_count += 1
        else:
            print(f"❌ 无法修复: {link} - 找不到匹配的文件")
            error_count += 1
        print()
    
    # 保存修复后的文件
    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成！共修复 {fixed_count} 个链接，{error_count} 个错误")
    else:
        print(f"✅ 无需修复！所有链接都正确")
    
    return fixed_count, error_count

def main():
    """主函数"""
    base_dir = "C:/Users/Lenovo/osrs-guide-site/"
    money_making_file = os.path.join(base_dir, "money-making.html")
    guides_dir = os.path.join(base_dir, "guides/")
    
    print("=" * 60)
    print("批量修复 money-making.html 中的错误链接")
    print("=" * 60)
    print()
    
    if not os.path.exists(money_making_file):
        print(f"❌ 文件不存在: {money_making_file}")
        return
    
    if not os.path.exists(guides_dir):
        print(f"❌ 目录不存在: {guides_dir}")
        return
    
    fixed, errors = fix_money_making_links(money_making_file, guides_dir)
    
    print()
    print("=" * 60)
    print("验证修复结果...")
    print("=" * 60)
    print()
    
    # 验证修复结果
    with open(money_making_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    links = re.findall(r'href="guides/([^"]+)"', content)
    still_broken = 0
    
    for link in links:
        if not os.path.exists(os.path.join(guides_dir, link)):
            print(f"❌ 仍错误的链接: {link}")
            still_broken += 1
    
    if still_broken == 0:
        print("✅ 所有链接都已修复！")
    else:
        print(f"⚠️  仍有 {still_broken} 个错误链接")

if __name__ == "__main__":
    main()
