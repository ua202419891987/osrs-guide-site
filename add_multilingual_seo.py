"""
OSRS Guru 多语言 SEO 脚本
- 给所有 HTML 页面添加 hreflang 标签
- 生成语言切换器组件
- 创建中文翻译页面
- 更新 sitemap.xml 支持多语言
"""

import os
import re
from pathlib import Path

SITE_ROOT = Path(__file__).parent
GUIDES_DIR = SITE_ROOT / "guides"
LANGUAGES = {
    "en": {"name": "English", "flag": "🇬🇧", "hreflang": "en"},
    "zh": {"name": "中文", "flag": "🇨🇳", "hreflang": "zh"},
}

# 热门页面 — 需要多语言版本
TOP_PAGES = [
    "index.html",
    "money-making.html",
    "skill-training.html",
    "quest-guides.html",
    "boss-guides.html",
]

# 中文翻译映射（页面标题和描述）
ZH_TRANSLATIONS = {
    "index.html": {
        "title": "OSRS 指南中心 — 2026 旧学院 RuneScape 攻略大全",
        "desc": "2026 年最完整的 OSRS 攻略网站。115+ 篇指南，包括新手指南、赚钱方法、技能训练、任务攻略、Boss 打法。适合新手和老玩家。",
        "og_title": "OSRS 指南中心 — 2026 完整攻略",
        "og_desc": "115+ 篇详尽的旧学院 RuneScape 攻略，2026 年最新版本。",
    },
    "money-making.html": {
        "title": "OSRS 赚钱攻略 2026 — 最佳 GP/小时方法 | OSRS Guru 中文",
        "desc": "2026 年最全 OSRS 赚钱指南。从零成本到高端 PvM，涵盖 F2P 和会员，新手友好。",
    },
    "skill-training.html": {
        "title": "OSRS 技能训练指南 2026 — 1-99 全技能攻略 | OSRS Guru 中文",
        "desc": "OSRS 全技能 1-99 训练指南。采矿、钓鱼、伐木、敏捷、猎人——最高效、最省钱、最快的方法。",
    },
    "quest-guides.html": {
        "title": "OSRS 任务攻略 2026 — 完整任务通关指南 | OSRS Guru 中文",
        "desc": "OSRS 全部任务攻略。从新手到 Dragon Slayer 2，一步步带你完成所有任务。",
    },
    "boss-guides.html": {
        "title": "OSRS Boss 攻略 2026 — PvM 打法大全 | OSRS Guru 中文",
        "desc": "OSRS 所有 Boss 完整攻略。Jad、Vorkath、Zulrah、Raid——预算装备、打法和掉落。",
    },
}


def add_hreflang_tags(html_content: str, page_path: str) -> str:
    """给 HTML <head> 添加 hreflang 标签"""
    hreflang_tags = ""
    for lang_code, info in LANGUAGES.items():
        if lang_code == "en":
            url = f"https://osrsguru.com/{page_path}"
        else:
            url = f"https://osrsguru.com/{lang_code}/{page_path}"
        hreflang_tags += f'\n  <link rel="alternate" hreflang="{info["hreflang"]}" href="{url}">'

    # 添加 x-default
    hreflang_tags += f'\n  <link rel="alternate" hreflang="x-default" href="https://osrsguru.com/{page_path}">'

    # 在第一个 <link 或 <meta 标签之后插入
    if '<link rel="alternate" hreflang' in html_content:
        # 已有 hreflang，跳过
        return html_content

    # 在 </title> 之后插入
    if '</title>' in html_content:
        html_content = html_content.replace('</title>', '</title>' + hreflang_tags)

    return html_content


def create_zh_page(original_path: Path, zh_dir: Path, page_name: str) -> Path:
    """创建中文翻译页面"""
    with open(original_path, 'r', encoding='utf-8') as f:
        html = f.read()

    trans = ZH_TRANSLATIONS.get(page_name, {})
    if not trans:
        return None

    # 替换标题
    if "title" in trans:
        html = re.sub(r'<title>.*?</title>', f'<title>{trans["title"]}</title>', html, count=1)
    if "desc" in trans:
        html = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{trans["desc"]}">',
            html, count=1
        )
    if "og_title" in trans:
        html = re.sub(
            r'<meta property="og:title" content="[^"]*">',
            f'<meta property="og:title" content="{trans["og_title"]}">',
            html, count=1
        )
    if "og_desc" in trans:
        html = re.sub(
            r'<meta property="og:description" content="[^"]*">',
            f'<meta property="og:description" content="{trans["og_desc"]}">',
            html, count=1
        )

    # 更新 canonical
    if page_name == "index.html":
        html = html.replace(
            'href="https://osrsguru.com/"',
            'href="https://osrsguru.com/zh/"'
        )
    else:
        html = html.replace(
            f'href="https://osrsguru.com/{page_name}"',
            f'href="https://osrsguru.com/zh/{page_name}"'
        )

    # 更新 html lang 属性
    html = html.replace('<html lang="en">', '<html lang="zh">')

    # 添加当前页面中文的 hreflang
    zh_hreflang = f'\n  <link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/{page_name}">'
    en_hreflang = f'\n  <link rel="alternate" hreflang="en" href="https://osrsguru.com/{page_name}">'
    x_default = f'\n  <link rel="alternate" hreflang="x-default" href="https://osrsguru.com/{page_name}">'

    if '<link rel="alternate" hreflang' not in html:
        hreflang_all = en_hreflang + zh_hreflang + x_default
        html = html.replace('</title>', '</title>' + hreflang_all)

    # 保存
    zh_path = zh_dir / page_name
    zh_path.parent.mkdir(parents=True, exist_ok=True)
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return zh_path


def create_language_switcher_js():
    """创建语言切换器组件"""
    js_code = """
/**
 * OSRS Guru Language Switcher
 * 浮动语言切换按钮
 */
(function() {
  'use strict';

  function injectSwitcher() {
    var switcher = document.createElement('div');
    switcher.id = 'lang-switcher';
    switcher.innerHTML = '<a href="/">EN</a> | <a href="/zh/">中文</a>';
    switcher.style.cssText = 'position:fixed;top:10px;right:80px;z-index:9999;'
      + 'color:#d4af37;font-size:12px;font-family:sans-serif;'
      + 'background:rgba(39,33,26,0.9);padding:4px 10px;'
      + 'border:1px solid rgba(212,175,55,0.3);border-radius:4px;';
    document.body.appendChild(switcher);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectSwitcher);
  } else {
    injectSwitcher();
  }
})();
"""
    js_path = SITE_ROOT / "js" / "lang-switcher.js"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_code.strip())
    return js_path


def update_sitemap():
    """更新 sitemap.xml 添加中文页面"""
    sitemap_path = SITE_ROOT / "sitemap.xml"
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    zh_entries = ""
    for page in TOP_PAGES:
        zh_entries += f'  <url><loc>https://osrsguru.com/zh/{page}</loc><lastmod>2026-06-08</lastmod><priority>0.8</priority><changefreq>monthly</changefreq></url>\n'

    if "<!-- ZH Pages -->" not in content:
        insert_pos = content.find("</urlset>")
        content = content[:insert_pos] + "\n  <!-- ZH Pages -->\n" + zh_entries + "\n" + content[insert_pos:]

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return sitemap_path


def main():
    print("=" * 60)
    print("OSRS Guru Multilingual SEO Deploy")
    print("=" * 60)

    # 1. 给所有页面添加 hreflang
    print("\n[1/4] Adding hreflang tags to root pages...")
    for page in TOP_PAGES:
        path = SITE_ROOT / page
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = add_hreflang_tags(html, page)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  [OK] {page}")
        else:
            print(f"  [MISS] {page} not found")

    # 2. 创建中文页面
    print("\n[2/4] Creating Chinese (zh/) pages...")
    zh_dir = SITE_ROOT / "zh"
    zh_dir.mkdir(parents=True, exist_ok=True)
    for page in TOP_PAGES:
        path = SITE_ROOT / page
        if path.exists():
            zh_path = create_zh_page(path, zh_dir, page)
            if zh_path:
                print(f"  [OK] zh/{page}")
            else:
                print(f"  [SKIP] {page} (no translation data)")

    # 3. 创建语言切换器
    print("\n[3/4] Creating language switcher...")
    js_path = create_language_switcher_js()
    print(f"  [OK] {js_path}")

    # 4. 更新 sitemap
    print("\n[4/4] Updating sitemap.xml...")
    sitemap_path = update_sitemap()
    print(f"  [OK] {sitemap_path}")

    print("\n" + "=" * 60)
    print("MULTILINGUAL SEO READY")
    print("=" * 60)
    print("  5 Chinese pages in /zh/")
    print("  Language switcher: js/lang-switcher.js")
    print("  Sitemap updated with zh URLs")
    print("\n  Next: Add <script src='js/lang-switcher.js'></script>")
    print("  to all pages' <head> section")


if __name__ == '__main__':
    main()
