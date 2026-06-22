#!/usr/bin/env python3
"""
OSRS Guru - 批量修复图片宽高属性（修复CLS问题）
用法：python fix_img_dimensions.py
"""

import os
import re
import glob

GUIDES_DIR = "C:/Users/Lenovo/osrs-guide-site/guides"

def fix_img_dimensions(content):
    """
    给所有<img>标签加上width和height属性（如果缺失）
    保留所有现有属性，只补充缺失的
    """
    # 正则：匹配<img 开头，捕获整个标签
    img_pattern = r'<img([^>]+?)>'
    
    def replace_img(match):
        img_tag = match.group(1)
        
        # 检查是否已有width和height
        has_width = 'width=' in img_tag
        has_height = 'height=' in img_tag
        
        # 如果都有，不修改
        if has_width and has_height:
            return f'<img{img_tag}>'
        
        # 如果缺width，加 width="500"
        if not has_width:
            # 在第一个属性前加width（或在末尾加）
            img_tag = ' width="500"' + img_tag
        
        # 如果缺height，加 height="300"
        if not has_height:
            # 找到width的位置，在后面加height
            if 'width="500"' in img_tag:
                img_tag = img_tag.replace(' width="500"', ' width="500" height="300"', 1)
            else:
                img_tag = img_tag + ' height="300"'
        
        return f'<img{img_tag}>'
    
    # 替换所有<img>标签
    fixed_content = re.sub(img_pattern, replace_img, content)
    return fixed_content

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = fix_img_dimensions(original_content)
        
        # 检查是否有修改
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, filepath
        else:
            return False, filepath
    except Exception as e:
        return None, f"{filepath} - ERROR: {str(e)}"

def main():
    print("Starting batch fix for image width/height attributes...")
    print(f"Directory: {GUIDES_DIR}\n")
    
    # 找出所有.html文件
    html_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    print(f"Found {len(html_files)} HTML files\n")
    
    fixed_count = 0
    error_count = 0
    
    for filepath in html_files:
        result, info = process_file(filepath)
        if result:
            print(f"✅ 修复：{os.path.basename(filepath)}")
            fixed_count += 1
        elif result is False:
            # 没修改，跳过
            pass
        else:
            print(f"❌ 错误：{info}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"✅ 完成！修复了 {fixed_count} 个文件")
    if error_count > 0:
        print(f"❌ 错误：{error_count} 个文件")
    print(f"{'='*50}\n")
    print("🎯 下一步：用Google PageSpeed Insights测试CLS分数")

if __name__ == "__main__":
    main()
