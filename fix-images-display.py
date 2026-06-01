#!/usr/bin/env python3
"""
移除所有 HTML 文件中的 style="display:none;" (img 标签)
让图片正常显示
"""

import os
import re
import glob

def fix_images_in_file(file_path):
    """修复单个文件中的图片显示问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除所有 <img> 标签中的 style="display:none;"
        # 匹配 style="display:none;" 或 style="display: none;"
        pattern = r'<img([^>]*?)style=["\']display:\s?none;?["\']([^>]*?)>'
        replacement = r'<img\1\2>'
        
        new_content = re.sub(pattern, replacement, content)
        
        # 也可以尝试更简单的匹配（直接删除 style 属性）
        pattern2 = r'\s+style=["\']display:\s?none;?["\']'
        new_content = re.sub(pattern2, '', new_content)
        
        # 如果内容有变化，写回文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已修复: {file_path}")
            return True
        else:
            # print(f"⏭️  跳过 (无需修复): {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {file_path} - {e}")
        return False

def main():
    fixed_count = 0
    total_count = 0
    
    # 1. 修复根目录的 HTML 文件
    print("=== 修复根目录 HTML 文件 ===\n")
    for html_file in glob.glob("*.html"):
        total_count += 1
        if fix_images_in_file(html_file):
            fixed_count += 1
    
    # 2. 修复 guides/ 目录中的 HTML 文件
    print("\n=== 修复 guides/ 目录中的 HTML 文件 ===\n")
    for html_file in glob.glob("guides/*.html"):
        total_count += 1
        if fix_images_in_file(html_file):
            fixed_count += 1
    
    print(f"\n=== 修复完成 ===")
    print(f"总文件数: {total_count}")
    print(f"已修复: {fixed_count}")
    print(f"无需修复: {total_count - fixed_count}")

if __name__ == "__main__":
    main()
