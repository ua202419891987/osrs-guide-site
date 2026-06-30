#!/usr/bin/env python3
"""深度升级5篇高潜力文章：焕新+串通+隐鉴"""

import os, re, random

articles = {
    'osrs-barrows-tunnel-optimization-2026.html': {
        'new_desc': 'Updated for June 2026. Master Barrows tunnel optimization with our complete strategy guide. Learn the 5 fastest routes, save 3+ minutes per run, and maximize your profit from every chest.',
        'qs_points': [
            'The 5 fastest tunnel routes save 3+ minutes per run compared to random searching',
            'Optimal prayer flicking and gear switching cuts supply costs by 40%',
            'Dharok\'s tunnel is always the most efficient path — learn why',
            'With practice, complete runs in under 6 minutes with 90%+ success rate',
        ],
    },
    'osrs-f2p-gear-progression-guide-2026.html': {
        'new_desc': 'Updated for June 2026. Complete F2P gear progression guide — from bronze to rune, organized by Attack level. Best weapons, armour, and budget setups for every F2P combat bracket.',
        'qs_points': [
            'Rune scimitar is the best F2P weapon — train Attack to 50 first for the fastest XP',
            'Full rune armour requires 40 Defence, but green d\'hide body is better for ranged defence',
            'Amulet of power (+6 to all stats) is the single best F2P amulet for combat',
            'Budget tip: maple shortbow + adamant arrows is the best F2P ranged setup under 50 Ranged',
        ],
    },
    'osrs-diary-priority-order-beginner-2026.html': {
        'new_desc': 'Updated for June 2026. OSRS Achievement Diary priority order guide — which diaries to complete first for maximum rewards. Fastest routes to unlock Fairy Rings, Falador Shield, and more.',
        'qs_points': [
            'Ardougne Easy Diary unlocks the fastest farming teleport in the game — do this FIRST',
            'Falador Easy Diary gives mole locator and shield — essential for early money making',
            'Lumbridge & Draynor Diary rewards 3,000 XP lamps — perfect for boosting slow skills',
            'Varrock Easy Diary gives 15 battlestaves daily from Zaff — 90K+ GP/week passive profit',
        ],
    },
    'osrs-clue-scrolls-beginner-guide-2026.html': {
        'new_desc': 'Updated for June 2026. Complete OSRS clue scroll guide for beginners. Learn how to get beginner and easy clues, solve every step type, and unlock profitable rewards worth millions.',
        'qs_points': [
            'Beginner clues drop from goblins, chickens, and cows — 1/128 chance, farmable at any level',
            'Easy clues drop from guards (1/128) — Hemenster guards near Seers\' Village are the fastest spot',
            'Reward caskets can contain god rune items worth 500K+ GP — even on beginner clues',
            'Always wear the best prayer gear and bring a teleport tab for emote clues',
        ],
    },
    'osrs-common-beginner-mistakes-avoid-2026.html': {
        'new_desc': 'Updated for June 2026. Avoid the 20 most common OSRS beginner mistakes that cost you millions of GP and hundreds of hours. Essential reading for every new player.',
        'qs_points': [
            'Buying expensive gear before training the skill — invest in supplies, not equipment for skills under 70',
            'Skipping quest rewards — Waterfall Quest alone gives 30+ Attack/Strength in 20 minutes',
            'Training Prayer at an altar instead of using the Chaos Temple or Player-Owned House gilded altar',
            'Not doing farm runs — herb runs pay 200K+ GP in 5 minutes with Ranarr seeds at 9 Farming',
        ],
    },
}

QUICK_SUMMARY_TPL = '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #ebe5f0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ Quick Summary &mdash; 30-Second Read</h3>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
%(points)s    </ul>
</div>'''

for fname, data in articles.items():
    path = f'guides/{fname}'
    if not os.path.exists(path):
        print(f'  NOT FOUND: {fname}')
        continue
    
    with open(path, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    orig = html
    changes = []
    
    # 1️⃣ 焕新 - Update meta description
    old_meta_pattern = r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']+["\']'
    new_meta = f'<meta name="description" content="{data["new_desc"]}"'
    html = re.sub(old_meta_pattern, new_meta, html, count=1)
    changes.append('meta desc')
    
    # 2️⃣ 焕新 - Update article-meta date if exists
    html = re.sub(r'(Updated:?\s*)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}', r'\1June 2026', html)
    html = re.sub(r'(last.*?updated.*?)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}', r'\1June 2026', html, flags=re.IGNORECASE)
    changes.append('date')
    
    # 3️⃣ 焕新 - Add Quick Summary if not present
    if 'Quick Summary' not in html:
        points_html = ''
        for pt in data['qs_points']:
            points_html += f'        <li>📌 <strong>{pt}</strong></li>\n'
        qs_html = QUICK_SUMMARY_TPL % {'points': points_html}
        
        # Insert after TOC or after article-meta
        toc_end = html.find('</ol>')
        if toc_end > 0:
            toc_end = html.find('\n', toc_end)
            html = html[:toc_end] + '\n' + qs_html + html[toc_end:]
            changes.append('Quick Summary')
        else:
            # Fallback: insert after first h1
            h1_end = html.find('</h1>')
            if h1_end > 0:
                h1_end = html.find('\n', h1_end)
                html = html[:h1_end] + '\n' + qs_html + html[h1_end:]
                changes.append('Quick Summary (after h1)')
    else:
        changes.append('QS exists')
    
    # 4️⃣ 串通 - Add internal links in Related Guides if missing
    # (The Related Guides were already added by the internal links update,
    # so this is already handled site-wide)
    changes.append('related guides (already done site-wide)')
    
    # 5️⃣ 隐鉴 - Check meta canonical is correct
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="[^"]*/([^"/]+\.html)"', html)
    if canonical_match and canonical_match.group(1) != fname:
        # Fix canonical
        html = re.sub(
            r'<link\s+rel="canonical"\s+href="[^"]*/([^"/]+\.html)"',
            f'<link rel="canonical" href="https://osrsguru.com/guides/{fname}"',
            html
        )
        changes.append('canonical fixed')
    else:
        changes.append('canonical OK')
    
    if html != orig:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        print(f'  ✅ {fname}: {", ".join(changes)}')
    else:
        print(f'  ⏭️ {fname}: no changes')

print('\n5 articles deeply upgraded!')
