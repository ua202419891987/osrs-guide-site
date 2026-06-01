#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准断链检查 - 只报告，不修改任何文件
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("C:/Users/Lenovo/osrs-guide-site/")
GUIDES_DIR = BASE_DIR / "guides"
IMAGES_DIR = BASE_DIR / "images"
GUIDES_IMAGES_DIR = BASE_DIR / "guides" / "images"

def check_all():
    broken = []
    checked = 0
    
    all_html = list(BASE_DIR.glob("*.html")) + list(GUIDES_DIR.glob("*.html"))
    
    for html_file in all_html:
        if html_file.name == "TEMPLATE.html":
            continue
        if not html_file.exists():
            continue
            
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        
        # 检查 href 链接
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        for href in hrefs:
            if href.startswith("http") or href.startswith("#") or href.startswith("mailto"):
                continue
            # 解析相对路径
            if href.startswith("../"):
                target = html_file.parent / href
            elif href.startswith("./"):
                target = html_file.parent / href[2:]
            elif "/" in href:
                target = BASE_DIR / href.lstrip("/")
            else:
                target = html_file.parent / href
            
            target = target.resolve()
            if not target.exists():
                broken.append({
                    "file": html_file.name,
                    "type": "link",
                    "value": href,
                    "target": str(target.relative_to(BASE_DIR))
                })
            checked += 1
        
        # 检查 img src
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        for src in imgs:
            if src.startswith("http"):
                continue
            if src.startswith("../"):
                target = (html_file.parent / src).resolve()
            elif src.startswith("./"):
                target = (html_file.parent / src[2:]).resolve()
            else:
                target = (BASE_DIR / src.lstrip("/")).resolve()
            
            if not target.exists():
                broken.append({
                    "file": html_file.name,
                    "type": "image",
                    "value": src,
                    "target": str(target.relative_to(BASE_DIR))
                })
            checked += 1
    
    print(f"检查了 {checked} 个链接/图片引用")
    print(f"发现 {len(broken)} 个断链\n")
    
    # 按类型分组
    link_broken = [b for b in broken if b["type"] == "link"]
    img_broken = [b for b in broken if b["type"] == "image"]
    
    print(f"❌ 断链（HTML 链接）: {len(link_broken)} 个")
    print(f"❌ 缺失图片: {len(img_broken)} 个\n")
    
    if link_broken:
        print("=" * 60)
        print("链接断链详情：")
        print("=" * 60)
        for b in link_broken[:30]:  # 只显示前30个
            print(f"  {b['file']} → {b['value']}")
            print(f"    期望文件: {b['target']}")
        if len(link_broken) > 30:
            print(f"  ... 还有 {len(link_broken)-30} 个")
        print()
    
    if img_broken:
        print("=" * 60)
        print("缺失图片详情：")
        print("=" * 60)
        seen = set()
        for b in img_broken:
            key = b['target']
            if key not in seen:
                seen.add(key)
                print(f"  {b['file']} → {b['value']}")
                print(f"    期望文件: {b['target']}")
        print()
    
    # 保存结果供后续使用
    with open(BASE_DIR / "broken-report.txt", "w", encoding="utf-8") as f:
        f.write(f"检查了 {checked} 个链接/图片引用\n")
        f.write(f"发现 {len(broken)} 个断链\n\n")
        f.write(f"断链（HTML 链接）: {len(link_broken)} 个\n")
        for b in link_broken:
            f.write(f"  {b['file']} → {b['value']} (期望: {b['target']})\n")
        f.write(f"\n缺失图片: {len(img_broken)} 个\n")
        seen = set()
        for b in img_broken:
            key = b['target']
            if key not in seen:
                seen.add(key)
                f.write(f"  {b['target']}\n")

    print("报告已保存到 broken-report.txt")

if __name__ == "__main__":
    check_all()
