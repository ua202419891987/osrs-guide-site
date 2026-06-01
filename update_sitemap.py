#!/usr/bin/env python3
"""
sitemap.xml 自动更新脚本
读取guides/目录下所有HTML文件，自动生成完整的sitemap.xml
"""

import os
from pathlib import Path
from datetime import datetime

# ========== 配置区域 ==========
GUIDES_DIR = Path("C:/Users/Lenovo/osrs-guide-site/guides")
OUTPUT_SITEMAP = Path("C:/Users/Lenovo/osrs-guide-site/sitemap.xml")
DOMAIN = "https://fyy19891987202481.github.io"  # 替换为你的域名
# ================================


def get_all_html_files() -> list:
    """获取guides目录下所有HTML文件（排除分类汇总页）"""
    exclude_files = {
        "money-making.html",
        "skill-training.html",
        "quest-guide.html",
        "boss-killing.html",
        "index.html"
    }
    
    html_files = []
    for f in GUIDES_DIR.glob("*.html"):
        if f.name.lower() not in exclude_files:
            html_files.append(f.name)
    
    html_files.sort()  # 按文件名排序
    return html_files


def generate_sitemap_xml(html_files: list) -> str:
    """生成完整的sitemap.xml内容"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # XML头部
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- 首页 -->
  <url>
    <loc>{DOMAIN}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
'''
    
    # 分类页
    category_pages = [
        ("money-making.html", "0.9"),
        ("skill-training.html", "0.9"),
        ("quest-guide.html", "0.9"),
        ("boss-killing.html", "0.9"),
    ]
    
    for page, priority in category_pages:
        if (GUIDES_DIR / page).exists():
            xml_content += f'  <url><loc>{DOMAIN}/guides/{page}</loc><changefreq>weekly</changefreq><priority>{priority}</priority></url>\n'
    
    # 所有攻略页
    for filename in html_files:
        url = f"{DOMAIN}/guides/{filename}"
        xml_content += f'  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    
    # XML尾部
    xml_content += '</urlset>\n'
    
    return xml_content


def main():
    print("🚀 sitemap.xml 自动更新脚本启动...")
    print(f"📁 扫描目录: {GUIDES_DIR}")
    
    # 获取所有HTML文件
    html_files = get_all_html_files()
    print(f"📊 找到 {len(html_files)} 个攻略页面")
    
    if len(html_files) == 0:
        print("⚠️  没有找到任何攻略HTML文件！请检查guides/目录。")
        return
    
    # 生成sitemap.xml
    xml_content = generate_sitemap_xml(html_files)
    
    # 保存文件
    try:
        OUTPUT_SITEMAP.write_text(xml_content, encoding="utf-8")
        print(f"✅ sitemap.xml 已更新！")
        print(f"   📁 保存位置: {OUTPUT_SITEMAP}")
        print(f"   📊 包含URL数量: {len(html_files) + 5} 个（首页+4个分类页+{len(html_files)}个攻略页）")
        
        # 显示前5个URL
        print(f"\n📋 前5个攻略页URL预览：")
        for i, filename in enumerate(html_files[:5], 1):
            print(f"   {i}. {DOMAIN}/guides/{filename}")
        
        if len(html_files) > 5:
            print(f"   ... 还有 {len(html_files) - 5} 个页面")
            
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return
    
    print(f"\n📋 下一步：")
    print(f"   1. 检查sitemap.xml内容是否正确")
    print(f"   2. 提交到Google Search Console")
    print(f"   3. 等待谷歌收录（3-7天）")


if __name__ == "__main__":
    main()