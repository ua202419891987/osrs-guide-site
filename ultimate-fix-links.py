#!/usr/bin/env python3
"""
终极修复：批量修复 guides/ 目录中所有 HTML 文件的错误链接
通过扫描实际存在的文件，建立正确映射
"""

import os
import re
import glob

def get_actual_filename(guides_dir, target_name):
    """模糊匹配：根据目标文件名，找到实际存在的文件"""
    # 1. 精确匹配
    exact_path = os.path.join(guides_dir, target_name)
    if os.path.exists(exact_path):
        return target_name
    
    # 2. 模糊匹配（忽略大小写、空格、部分匹配）
    target_lower = target_name.lower().replace('-', ' ').replace('.html', '')
    
    best_match = None
    best_score = 0
    
    for filename in os.listdir(guides_dir):
        if not filename.endswith('.html') or filename == 'TEMPLATE.html':
            continue
        
        file_lower = filename.lower().replace('-', ' ').replace('.html', '')
        
        # 计算相似度（简单方法：公共单词数）
        target_words = set(target_lower.split())
        file_words = set(file_lower.split())
        common = target_words & file_words
        score = len(common)
        
        if score > best_score:
            best_score = score
            best_match = filename
    
    # 如果相似度 > 50%，认为是匹配
    if best_score >= len(target_lower.split()) * 0.5:
        return best_match
    
    return None

def fix_all_guide_links():
    """修复所有攻略文章中的相互链接"""
    guides_dir = "guides"
    
    # 获取所有实际存在的攻略文件
    actual_files = []
    for filename in os.listdir(guides_dir):
        if filename.endswith('.html') and filename != 'TEMPLATE.html':
            actual_files.append(filename)
    
    print(f"📂 找到 {len(actual_files)} 个实际攻略文件\n")
    
    fixed_count = 0
    total_count = 0
    
    # 遍历所有 HTML 文件
    for html_file in glob.glob(os.path.join(guides_dir, "*.html")):
        if 'TEMPLATE' in html_file:
            continue
        
        total_count += 1
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 查找所有攻略文章链接（href="guides/..." 或 href="../..."）
            links = re.findall(r'href=["\'](guides/[^"\']+|[^"\']*\.html)["\']', content)
            
            for link in links:
                # 提取文件名
                if link.startswith('guides/'):
                    filename = link.replace('guides/', '')
                else:
                    filename = os.path.basename(link)
                
                # 检查文件是否存在
                if filename in actual_files:
                    continue  # 文件存在，无需修复
                
                # 尝试模糊匹配
                matched_file = get_actual_filename(guides_dir, filename)
                
                if matched_file and matched_file != filename:
                    # 替换链接
                    old_link = f'href="{link}"'
                    if link.startswith('guides/'):
                        new_link = f'href="guides/{matched_file}"'
                    else:
                        new_link = f'href="{matched_file}"'
                    
                    content = content.replace(old_link, new_link)
                    print(f"  ✅ {os.path.basename(html_file)}: {filename} → {matched_file}")
                    fixed_count += 1
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
        except Exception as e:
            print(f"  ❌ 错误: {html_file} - {e}")
    
    print(f"\n✅ 修复完成：检查了 {total_count} 个文件，修复了 {fixed_count} 个链接")

def main():
    print("=== 终极修复：批量修复所有错误链接 ===\n")
    fix_all_guide_links()
    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
