#!/usr/bin/env python3
"""
检查整个网站是否有断链（404 错误）
"""

import os
import re
import urllib.request
from urllib.parse import urljoin, urlparse
from urllib.error import HTTPError, URLError

def check_link(base_url, link):
    """检查单个链接是否有效"""
    # 跳过锚点链接 (#) 和外部链接 (http)
    if link.startswith('#'):
        return True, 'anchor'
    
    if link.startswith('http'):
        # 外部链接，跳过（或可选检查）
        return True, 'external'
    
    # 构建完整 URL
    full_url = urljoin(base_url, link)
    
    # 检查本地文件是否存在
    # 将 URL 路径转换为本地文件路径
    parsed = urlparse(full_url)
    path = parsed.path
    
    # 移除开头的 /
    if path.startswith('/'):
        path = path[1:]
    
    # 如果路径为空，默认为 index.html
    if not path:
        path = 'index.html'
    
    # 检查文件是否存在
    if os.path.exists(path):
        return True, 'file exists'
    else:
        return False, f'file not found: {path}'

def check_html_file(file_path, base_url):
    """检查单个 HTML 文件中的所有链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找所有 href 和 src 链接
        links = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', content)
        
        broken_links = []
        
        for link in links:
            is_valid, msg = check_link(base_url, link)
            if not is_valid:
                broken_links.append((link, msg))
        
        return broken_links
            
    except Exception as e:
        print(f"❌ 错误: {file_path} - {e}")
        return []

def main():
    base_url = "http://localhost:8080/"
    
    print("=== 检查整个网站的断链 ===\n")
    
    all_broken_links = []
    
    # 1. 检查根目录的 HTML 文件
    print("📂 检查根目录 HTML 文件...\n")
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            file_path = filename
            print(f"检查: {file_path}")
            broken_links = check_html_file(file_path, base_url)
            if broken_links:
                print(f"  ⚠️  发现 {len(broken_links)} 个断链:")
                for link, msg in broken_links:
                    print(f"    - {link} ({msg})")
                    all_broken_links.append((file_path, link, msg))
            else:
                print(f"  ✅ 无断链")
            print()
    
    # 2. 检查 guides/ 目录中的 HTML 文件
    print("\n📂 检查 guides/ 目录中的 HTML 文件...\n")
    guides_dir = 'guides'
    if os.path.exists(guides_dir):
        for filename in os.listdir(guides_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(guides_dir, filename)
                print(f"检查: {file_path}")
                broken_links = check_html_file(file_path, base_url)
                if broken_links:
                    print(f"  ⚠️  发现 {len(broken_links)} 个断链:")
                    for link, msg in broken_links:
                        print(f"    - {link} ({msg})")
                        all_broken_links.append((file_path, link, msg))
                else:
                    print(f"  ✅ 无断链")
                print()
    
    # 3. 总结
    print("\n=== 检查完成 ===\n")
    if all_broken_links:
        print(f"⚠️  总共发现 {len(all_broken_links)} 个断链:")
        for file_path, link, msg in all_broken_links:
            print(f"  - {file_path}: {link} ({msg})")
    else:
        print("🎉 太好了！没有发现断链！")

if __name__ == "__main__":
    main()
