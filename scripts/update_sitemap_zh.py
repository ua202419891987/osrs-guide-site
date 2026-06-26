#!/usr/bin/env python3
"""更新 sitemap.xml — 添加所有 zh/ URL（163 guides + 9 root 页面）"""
import os, glob

SITEMAP = r"C:\Users\Lenovo\osrs-guide-site\sitemap.xml"
ZH_DIR = r"C:\Users\Lenovo\osrs-guide-site\zh"
TODAY = "2026-06-25"
BASE = "https://osrsguru.com"

with open(SITEMAP, "r", encoding="utf-8") as f:
    content = f.read()

# 找到插入点（在 </urlset> 之前）
insert_marker = "</urlset>"

# 生成所有 zh 页面条目
entries = []

# zh/ root pages
for f in sorted(glob.glob(os.path.join(ZH_DIR, "*.html"))):
    filename = os.path.basename(f)
    entries.append(
        f'  <url><loc>{BASE}/zh/{filename}</loc>'
        f'<lastmod>{TODAY}</lastmod>'
        f'<priority>0.80</priority>'
        f'<changefreq>weekly</changefreq></url>'
    )

# zh/guides/ pages
for f in sorted(glob.glob(os.path.join(ZH_DIR, "guides", "*.html"))):
    filename = os.path.basename(f)
    entries.append(
        f'  <url><loc>{BASE}/zh/guides/{filename}</loc>'
        f'<lastmod>{TODAY}</lastmod>'
        f'<priority>0.85</priority>'
        f'<changefreq>weekly</changefreq></url>'
    )

# 移除旧 zh/ 条目（5 个）
old_zh_urls = [
    "https://osrsguru.com/zh/index.html",
    "https://osrsguru.com/zh/money-making.html",
    "https://osrsguru.com/zh/skill-training.html",
    "https://osrsguru.com/zh/quest-guides.html",
    "https://osrsguru.com/zh/boss-guides.html",
]
for url in old_zh_urls:
    # 移除完整行（含换行）
    content = content.replace(f'  <url><loc>{url}</loc><lastmod>2026-06-22</lastmod><priority>0.8</priority><changefreq>monthly</changefreq></url>\n', '')

new_block = "\n".join(entries) + "\n"
content = content.replace("</urlset>", new_block + "</urlset>")

with open(SITEMAP, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ sitemap.xml 已更新")
print(f"   新增 zh/ root 页面: {len(glob.glob(os.path.join(ZH_DIR, '*.html')))} 个")
print(f"   新增 zh/guides/ 页面: {len(glob.glob(os.path.join(ZH_DIR, 'guides', '*.html')))} 个")
print(f"   总计 zh/ 条目: {content.count('/zh/')} 个")
print(f"   lastmod: {TODAY}")
