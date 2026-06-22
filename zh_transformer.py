#!/usr/bin/env python3
"""v3 translation pre-processor: mechanical transformations for OSRS Guru Chinese site."""

import os, re, glob

SRC = "guides"
DST = "zh/guides"
FILES = sorted(glob.glob(f"{SRC}/*.html"))

# Already done files (skip these, they've been manually processed)
done = [os.path.basename(f) for f in glob.glob(f"{DST}/*.html")]
skip = set(done)

COLOR_MAP = {
    '#d4af37': '#333',
    '#e8d5b7': '#1a1a1a',
    '#e0d5c0': '#aaa',
    '#4a3320': '#1a1a1a',
    'var(--gold)': '#333',
    'var(--text-secondary)': '#555',
}

ZH_NAV = """    <header class="site-header">
        <div class="header-inner">
            <a href="../../index.html" class="logo">OSRS<span>Guru</span></a>
            <nav class="main-nav">
                <a href="../../skill-training.html">技能训练</a>
                <a href="../../money-making.html">赚钱方法</a>
                <a href="../../boss-guides.html">Boss攻略</a>
                <a href="../../quest-guides.html">任务指南</a>
            </nav>
        </div>
    </header>"""

ZH_FOOTER = """    <footer>
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2026 OSRS Guru. All rights reserved. Old School RuneScape is a trademark of Jagex Ltd. This site is not affiliated with Jagex.</p>
            </div>
        </div>
    </footer>

<!-- Copyright & Anti-Scraping Notice -->
<div class="copyright-protection" style="background:#faf8f5;border:1px solid #e0d5c0;border-left:3px solid #d4af37;border-radius:4px;padding:10px 16px;margin:16px auto;max-width:780px">
    <p style="color:#1a1a1a;margin:0;font-size:0.78rem;line-height:1.55;">&copy; 2026 <strong>OSRS Guru (osrsguru.com)</strong>. All rights reserved. 本文受版权法保护，未经授权禁止爬取、抓取、自动转载及用于AI训练数据提取。 | Content created under <a href="https://legal.jagex.com/docs/policies/fan-content-policy" target="_blank" rel="noopener" style="color:#3b2615;">Jagex Fan Content Policy</a>. Wiki content under <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener" style="color:#3b2615;">CC BY-SA 3.0</a>. Not affiliated with Jagex Ltd.</p>
</div>"""

ZH_FOOTER_PART = ZH_FOOTER.split('<!-- Copyright')[0]
ZH_COPYRIGHT = '\n'.join(ZH_FOOTER.split('\n')[-10:])

count = 0
for path in FILES:
    fname = os.path.basename(path)
    if fname in skip:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1) lang
    html = html.replace('<html lang="en">', '<html lang="zh">')

    # 2) Path fixes
    html = html.replace('../css/style.css', '../../css/style.css')
    html = html.replace('../js/features.js', '../../js/features.js')
    html = html.replace('../js/ai-qa-widget.js', '../../js/ai-qa-widget.js')

    # 3) Canonical
    html = re.sub(
        r'<link rel="canonical" href="https://osrsguru\.com/guides/([^"]+)"',
        r'<link rel="canonical" href="https://osrsguru.com/zh/guides/\1"',
        html
    )

    # 4) Add hreflang alternates after canonical
    if '<link rel="alternate" hreflang="en"' not in html:
        canon_match = re.search(r'<link rel="canonical".*?>', html)
        if canon_match:
            hreflang_block = f'\n    <link rel="alternate" hreflang="en" href="https://osrsguru.com/guides/{fname}">\n    <link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/guides/{fname}">'
            html = html.replace(canon_match.group(0), canon_match.group(0) + hreflang_block)

    # 5) Color fixes
    html = re.sub(r'color:\s*#d4af37', 'color:#333', html)
    html = re.sub(r'color:\s*#e8d5b7', 'color:#1a1a1a', html)
    for old, new in COLOR_MAP.items():
        html = html.replace(old, new)

    # 6) Replace header
    html = re.sub(r'<header[^>]*>.*?</header>', ZH_NAV, html, flags=re.DOTALL)

    # 7) Replace footer (careful - match from <footer to </footer>)
    html = re.sub(r'<footer[^>]*>.*?</footer>\s*$', '', html, flags=re.DOTALL)
    html = html.rstrip() + '\n\n' + ZH_FOOTER + '\n'

    # 8) Remove old copyright notices
    html = re.sub(r'<!-- Copyright.*?-->.*?</div>', '', html, flags=re.DOTALL)

    # 9) Ensure black text color
    if 'guide-content li{color:#1a1a1a!important}' not in html:
        html = html.replace('</body>', '\n<style>.guide-content li{color:#1a1a1a!important}</style>\n</body>')

    # Write
    out_path = os.path.join(DST, fname)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    count += 1

print(f"Mechanical transform done: {count} files")
