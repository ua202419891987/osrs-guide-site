#!/usr/bin/env python3
"""
Batch fix 14 OSRS Group B guide articles.
Performs all P0 checklist fixes.
"""
import re
import os

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"
files = [
    "osrs-1-99-hunter-guide-afk-method.html",
    "osrs-fastest-1-99-crafting-guide-2026.html",
    "osrs-fastest-99-attack-strength-defence.html",
    "osrs-fastest-99-cooking-f2p.html",
    "osrs-fastest-hunter-training-2026.html",
    "osrs-fastest-leveling-guide-2026.html",
    "osrs-how-to-get-99-agility-fast-2026.html",
    "osrs-how-to-get-99-fishing-afk-method.html",
    "osrs-how-to-train-prayer-cheap-f2p.html",
    "osrs-hunter-training-guide-2026.html",
    "osrs-mahogany-homes-construction-guide-2026.html",
    "osrs-maxing-99-order-guide-2026.html",
    "osrs-optimal-leveling-guide-2026.html",
    "osrs-range-training-1-99-guide-2026.html",
]

NEW_HEADER = '''   <nav class="main-nav">
    <a href="../index.html">Home</a>
    <a href="../boss-guides.html">Bosses</a>
    <a href="../money-making.html">Money</a>
    <a href="../quest-guides.html">Quests</a>
    <a href="../skill-training.html">Skills</a>
    <a href="../osrs-best-updates-2026-ranked.html">Updates</a>
    <a href="../osrs-chinese-guide-2026.html">Chinese</a>
   </nav>'''

MOBILE_CSS = '''
@media (max-width:768px){.guide-content .quick-summary{padding:1rem!important;margin:1rem auto!important}.guide-content .toc{padding:1rem!important;margin:1rem auto!important}.guide-content table{font-size:.85rem}.guide-content h2{font-size:1.2rem}.guide-content h3{font-size:1.05rem}.article-meta{font-size:12px!important}.support-card{padding:16px!important}.copyright-protection{padding:.8rem!important;font-size:.75rem!important}.guide-content ul,.guide-content ol{padding-left:1.2rem}}
@media (max-width:640px){.guide-content table{font-size:.78rem}.guide-content td,.guide-content th{padding:4px!important}.guide-content .article-grid{grid-template-columns:1fr!important}}
</style>'''

def fix_file(filepath):
    basename = os.path.basename(filepath)
    fixes_applied = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # 1. Fix header: replace 4-item nav with 7-item nav
    # Match any nav class="main-nav" with its children
    nav_pattern = r'(<nav class="main-nav">)(.*?)(</nav>)'
    
    def replace_header(match):
        return NEW_HEADER
    
    html = re.sub(nav_pattern, replace_header, html, count=1, flags=re.DOTALL)
    if html != original:
        fixes_applied.append("header-7items")
    
    # 2. Replace placeholder quick-summary with real 30-second summary
    quick_summary_fixes = {
        "osrs-fastest-99-attack-strength-defence.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Fastest way to 99 Attack/Strength/Defence: NMZ and sand crabs for early levels, then Nightmare Zone (NMZ) for AFK, and Slayer for profit while training.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Fastest XP:</strong> Nightmare Zone (NMZ) — 70K\u2013100K XP/hr, fully AFK with absorption potions</li>
     <li>\U0001f4cc <strong>Early game:</strong> Sand crabs (1\u201340) or Rock crabs \u2014 20K\u201350K XP/hr, zero cost</li>
     <li>\U0001f4cc <strong>Mid-game:</strong> Ammonite crabs (40\u201370) \u2014 40K\u201365K XP/hr, better drops</li>
     <li>\U0001f4cc <strong>Estimated cost:</strong> 0\u20132M GP (NMZ absorbs) \u2014 free with Sand/Ammonite crabs</li>
    </ul>
   </div>''',
        "osrs-fastest-99-cooking-f2p.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Fastest way to 99 Cooking in F2P OSRS: trout/salmon (1\u201340), then lobster/anchovy pizza (40\u201399) for profit, or wines (35\u201399) for fastest XP.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Fastest XP:</strong> Wine-making (35+) \u2014 150K\u2013250K XP/hr, slight loss per batch</li>
     <li>\U0001f4cc <strong>Most profitable:</strong> Lobster cooking (40+) \u2014 40K\u201375K XP/hr, 50K\u2013150K GP/hr profit</li>
     <li>\U0001f4cc <strong>AFK-friendly:</strong> Trout/Salmon at Barbarian Village \u2014 25K\u201345K XP/hr</li>
     <li>\U0001f4cc <strong>Estimated cost:</strong> Free to 10M GP profit depending on method</li>
    </ul>
   </div>''',
        "osrs-fastest-hunter-training-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Fastest way to 99 Hunter in OSRS: 3-tick Black salamanders (67\u201380) for max XP, then Herbiboar (80\u201399) for profit + great XP, with Maniacal monkeys for AFK training.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Fastest XP:</strong> 3-tick Black salamanders \u2014 100K\u2013180K XP/hr (advanced)</li>
     <li>\U0001f4cc <strong>Best overall:</strong> Herbiboar (80+) \u2014 140K\u2013180K XP/hr + 500K\u20131M GP/hr</li>
     <li>\U0001f4cc <strong>AFK method:</strong> Maniacal Monkeys (60+) \u2014 60K\u2013110K XP/hr, 1\u20132 min AFK</li>
     <li>\U0001f4cc <strong>Estimated time:</strong> 35\u201350 hours active play</li>
    </ul>
   </div>''',
        "osrs-fastest-leveling-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Fastest 1\u201399 leveling route in OSRS for a new account: quest rush to skip early levels, then efficient skill training to unlock endgame content as fast as possible.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Start:</strong> Quest rush (Waterfall Quest, Fight Arena, Tree Gnome Village) \u2014 10\u201330 combat levels in 1 hour</li>
     <li>\U0001f4cc <strong>Combat:</strong> Sand crabs (1\u201340) \u2192 NMZ (40\u201370) \u2192 Slayer (70\u201399)</li>
     <li>\U0001f4cc <strong>Non-combat:</strong> Birdhouse runs + herb runs for passive gains</li>
     <li>\U0001f4cc <strong>Estimated time to base 70s:</strong> 100\u2013150 hours</li>
    </ul>
   </div>''',
        "osrs-how-to-get-99-agility-fast-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Fastest way to 99 Agility in OSRS: rooftop courses from 1\u201399, then Hallowed Sepulchre (52+) for best XP and profit, or Ardougne rooftop (70+) for AFK with graceful marks.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Best XP:</strong> Hallowed Sepulchre (92 Agility + 82) \u2014 90K\u2013130K XP/hr + 1\u20132M GP/hr</li>
     <li>\U0001f4cc <strong>AFK method:</strong> Ardougne rooftop (70+) \u2014 55K\u201365K XP/hr, low attention</li>
     <li>\U0001f4cc <strong>Early game:</strong> Gnome Stronghold (1) \u2192 Draynor (10) \u2192 Al Kharid (20) \u2192 Varrock (30)</li>
     <li>\U0001f4cc <strong>Estimated time:</strong> 200\u2013300 hours rooftops, 150\u2013200 hours Sepulchre</li>
    </ul>
   </div>''',
        "osrs-how-to-get-99-fishing-afk-method.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Most AFK-friendly path to 99 Fishing in OSRS: fly fishing (1\u201358), then barbarian fishing (58\u201399) for best XP, or monkfish/anglerfish for profit while AFK.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>AFK XP:</strong> Barbarian Fishing (58+) \u2014 35K\u201365K XP/hr, click every 1\u20132 min</li>
     <li>\U0001f4cc <strong>Profit AFK:</strong> Monkfish (62+) \u2014 30K\u201340K XP/hr + 200K\u2013400K GP/hr</li>
     <li>\U0001f4cc <strong>Ultra AFK:</strong> Anglerfish (82+) \u2014 20K\u201330K XP/hr + 300K\u2013500K GP/hr</li>
     <li>\U0001f4cc <strong>Estimated time:</strong> 200\u2013300 hours to 99</li>
    </ul>
   </div>''',
        "osrs-how-to-train-prayer-cheap-f2p.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Cheapest way to train Prayer in F2P OSRS: bury big bones at hill giants or use the Chaos Temple (Wilderness) for 50% bone saving chance, then switch to hydra/dragon bones.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Cheapest XP:</strong> Big bones at Chaos Temple (Wilderness) \u2014 50% save chance, ~25K XP/hr</li>
     <li>\U0001f4cc <strong>F2P best:</strong> Hydra bones at Wilderness Chaos Altar \u2014 ~60K XP/hr with 50% save</li>
     <li>\U0001f4cc <strong>Passive method:</strong> Bury bones while training combat at hill/cave giants</li>
     <li>\U0001f4cc <strong>Estimated cost 1\u201343:</strong> 100K\u2013500K GP with big bones</li>
    </ul>
   </div>''',
        "osrs-hunter-training-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Complete OSRS Hunter training guide for 2026: birdhouse runs for passive XP, salamanders for active mid-level training, and Herbiboar for best endgame XP and profit.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Passive:</strong> Birdhouse runs (every 50 min) \u2014 40K\u201360K XP/run, profitable</li>
     <li>\U0001f4cc <strong>Best XP:</strong> Herbiboar (80+) \u2014 140K\u2013180K XP/hr, profitable</li>
     <li>\U0001f4cc <strong>AFK:</strong> Maniacal Monkeys (60+) \u2014 60K\u2013110K XP/hr, 1\u20132 min AFK</li>
     <li>\U0001f4cc <strong>Estimated time:</strong> 40\u201360 hours active + passive birdhouses</li>
    </ul>
   </div>''',
        "osrs-mahogany-homes-construction-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Mahogany Homes is the most cost-efficient Construction training method in OSRS, offering 80\u2013150K XP/hr at half the cost of traditional larders/mythical capes.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Cost saving:</strong> 50\u201360% cheaper than larders or mythical capes</li>
     <li>\U0001f4cc <strong>Fastest supplies:</strong> Mahogany planks \u2014 120K\u2013150K XP/hr, ~6\u20138 GP/XP</li>
     <li>\U0001f4cc <strong>Budget:</strong> Oak planks \u2014 80K\u2013110K XP/hr, ~4\u20135 GP/XP</li>
     <li>\U0001f4cc <strong>Estimated cost 1\u201399:</strong> 30\u201350M with mahogany, 15\u201325M with oak</li>
    </ul>
   </div>''',
        "osrs-maxing-99-order-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Optimal 99 order for maxing in OSRS 2026: train profitable skills first to fund expensive ones, and prioritize skills that unlock money-making methods.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Start with:</strong> Slayer + Farming (profitable skills that fund others)</li>
     <li>\U0001f4cc <strong>Do early:</strong> Hunter (birdhouses), Fishing, Woodcutting (AFK + profit)</li>
     <li>\U0001f4cc <strong>Leave for last:</strong> Construction, Herblore, Prayer (expensive skills)</li>
     <li>\U0001f4cc <strong>Estimated cost to max:</strong> 500M\u20131B GP (efficient order)</li>
    </ul>
   </div>''',
        "osrs-optimal-leveling-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Optimal leveling guide for OSRS in 2026: quest rush for fast early levels, then a skill priority order that maximizes account progression and money-making potential.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>First:</strong> Quest rush (Waterfall, Fight Arena, MM1) for 40+ combat stats in hours</li>
     <li>\U0001f4cc <strong>Early skills:</strong> Agility (Graceful) \u2192 Farming (herb runs) \u2192 Hunter (birdhouses)</li>
     <li>\U0001f4cc <strong>Mid-game:</strong> Slayer (combat + money) \u2192 Range/Magic for bossing</li>
     <li>\U0001f4cc <strong>Time to Quest Cape:</strong> ~150\u2013200 hours with optimal order</li>
    </ul>
   </div>''',
        "osrs-range-training-1-99-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">\u23f1\ufe0f 30-Second Quick Summary</h3>
    <p style="margin:0 0 .6rem;color:#2D2A33;font-size:.92rem;">Fastest way to 99 Ranged in OSRS 2026: Maniacal Monkeys (60+) or Nightmare Zone for AFK, Red Chins for fastest XP, and Slayer for profitable progression.</p>
    <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
     <li>\U0001f4cc <strong>Fastest XP:</strong> Red Chinchompas at Maniacal Monkeys \u2014 200K\u2013400K XP/hr (costly)</li>
     <li>\U0001f4cc <strong>AFK method:</strong> Nightmare Zone (NMZ) with MSB/Rune Crossbow \u2014 60K\u201390K XP/hr</li>
     <li>\U0001f4cc <strong>Profitable:</strong> Slayer with Range \u2014 30K\u201370K XP/hr + profit from tasks</li>
     <li>\U0001f4cc <strong>Estimated cost (chins):</strong> 40\u201380M GP for 1\u201399</li>
    </ul>
   </div>''',
    }
    
    # Also handle the already-existing quick-summary in files that have them
    # For files that don't have a proper quick-summary, add one
    
    for fn, qs_html in quick_summary_fixes.items():
        if basename == fn:
            # Find and replace the existing quick-summary block
            # Pattern: match from <div class="quick-summary" to closing </div>
            qs_pattern = r'<div class="quick-summary"[^>]*>.*?</div>\s*'
            # Use DOTALL for multi-line matching, but be careful not to be too greedy
            if re.search(r'<div class="quick-summary"[^>]*>', html, re.DOTALL):
                # Find the exact quick-summary block
                start = html.find('<div class="quick-summary"')
                if start >= 0:
                    # Find the matching closing div
                    depth = 0
                    end = start
                    for i in range(start, len(html)):
                        if html[i:i+3] == '<di' and 'quick-summary' not in html[i:i+50]:
                            # Nested div opening
                            pass
                        if html[i:i+6] == '</div>':
                            # Check if this is the quick-summary closing
                            # We need to count the quick-summary div's own closing
                            # Since the quick-summary has no nested divs, the first </div> after it is its close
                            end = i + 6
                            break
                    
                    if end > start:
                        html = html[:start] + qs_html + '\n\n' + html[end:]
                        fixes_applied.append("quick-summary-replaced")
                        print(f"  Replaced quick-summary placeholder")
    # For files that have NO quick-summary at all
    if re.search(r'class="quick-summary"', html) is None:
        # Add quick-summary after <div class="container"> for these files
        if basename == "osrs-maxing-99-order-guide-2026.html":
            new_qs = quick_summary_fixes["osrs-maxing-99-order-guide-2026.html"]
            html = html.replace('<div class="container">', '<div class="container">\n' + new_qs + '\n', 1)
            fixes_applied.append("quick-summary-added")
        elif basename == "osrs-optimal-leveling-guide-2026.html":
            new_qs = quick_summary_fixes["osrs-optimal-leveling-guide-2026.html"]
            html = html.replace('<div class="container">', '<div class="container">\n' + new_qs + '\n', 1)
            fixes_applied.append("quick-summary-added")
        elif basename == "osrs-range-training-1-99-guide-2026.html":
            new_qs = quick_summary_fixes["osrs-range-training-1-99-guide-2026.html"]
            html = html.replace('<div class="container">', '<div class="container">\n' + new_qs + '\n', 1)
            fixes_applied.append("quick-summary-added")
    
    # 3. Add article-meta with "Updated for July 2026" if missing
    if 'article-meta' not in html and 'Updated for July 2026' not in html:
        # Add after h1 in hero section - find the pattern
        meta_pattern = r'(<section class="guide-hero">.*?<h1>.*?</h1>)\s*'
        meta_html = r'\1\n            <div class="article-meta" style="margin-top:12px;color:#2D2A33;font-size:14px">\n             <span>\U0001f4c5 Published: June 2026</span> &nbsp;|&nbsp;\n             <span>\u23f1\ufe0f 10 min read</span> &nbsp;|&nbsp;\n             <span>\u270d\ufe0f OSRS Guru</span> &nbsp;|&nbsp;\n             <span>\U0001f504 Updated for July 2026</span>\n            </div>'
        
        # Since Python re can't handle the lookbehind well, let's do it differently
        if '<section class="guide-hero">' in html and '<h1>' in html:
            # Find the position after h1 closing tag within hero
            hero_start = html.find('<section class="guide-hero">')
            h1_pos = html.find('</h1>', hero_start)
            if h1_pos > 0:
                h1_end = h1_pos + 5
                # Check what follows
                next_section = html.find('</section>', h1_end)
                if next_section > 0 and next_section - h1_end < 200:
                    insert_pos = next_section
                    meta_insert = '\n            <div class="article-meta" style="margin-top:12px;color:#2D2A33;font-size:14px">\n             <span>\U0001f4c5 Published: June 2026</span> &nbsp;|&nbsp;\n             <span>\u23f1\ufe0f 10 min read</span> &nbsp;|&nbsp;\n             <span>\u270d\ufe0f OSRS Guru</span> &nbsp;|&nbsp;\n             <span>\U0001f504 Updated for July 2026</span>\n            </div>\n'
                    # Check if next_section actually closes the hero section
                    if html[insert_pos:insert_pos+11] == '</section>':
                        html = html[:insert_pos] + meta_insert + html[insert_pos:]
                        fixes_applied.append("article-meta-added")
    
    # 4. Add @media queries to bottom CSS if missing
    if 'max-width:768px' not in html:
        html = html.replace('</style>', MOBILE_CSS, 1)
        fixes_applied.append("media-queries-added")
    
    # 5. Add TOC where missing 
    # Check files that need TOC
    files_needing_toc = [
        "osrs-1-99-hunter-guide-afk-method.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-fastest-99-cooking-f2p.html",
        "osrs-how-to-get-99-agility-fast-2026.html",
        "osrs-how-to-get-99-fishing-afk-method.html",
        "osrs-how-to-train-prayer-cheap-f2p.html",
    ]
    
    if basename in files_needing_toc and 'class="toc"' not in html:
        # Add simple TOC after quick-summary
        toc_html = '\n   <div class="toc" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">\n    <h3 style="color:#b8860b;font-size:1rem;margin:0 0 .6rem;font-weight:700;">\U0001f4d6 Table of Contents</h3>\n    <ul style="margin:0;padding-left:1.2rem;font-size:.9rem;line-height:2;list-style:none;">\n     <li><a href="#section1" style="color:#4a4a6a;">1. Main Overview</a></li>\n     <li><a href="#faq" style="color:#4a4a6a;">FAQ</a></li>\n    </ul>\n   </div>\n'
        # Insert after quick-summary or before first h2
        qs_end = html.find('</div>', html.find('class="quick-summary"'))
        if qs_end > 0:
            # Find the next </div> after quick-summary - that's the closing of the quick-summary div
            close1 = html.find('</div>', html.find('class="quick-summary"'))
            close2 = html.find('</div>', close1 + 6)
            insert_after = close2 + 6 if close2 > close1 else close1 + 6
            html = html[:insert_after] + '\n' + toc_html + html[insert_after:]
            fixes_applied.append("toc-added")
    
    # 6. Add support-card if missing
    files_needing_support = [
        "osrs-1-99-hunter-guide-afk-method.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-fastest-99-cooking-f2p.html",
        "osrs-how-to-train-prayer-cheap-f2p.html",
    ]
    
    support_card = '''\n    <div class="support-card" style="background:#e8f5e9;border:1px solid #a5d6a7;border-radius:12px;padding:24px;margin:24px 0;text-align:center;">\n     <h3 style="margin:0 0 8px;color:#2e7d32;font-size:1.1rem;">\U0001f49a Support OSRS Guru</h3>\n     <p style="margin:0 0 12px;color:#1b5e20;font-size:.95rem;">Enjoying this guide? Support us via PayPal to keep the site ad-light and updated for 2026!</p>\n     <form action="https://www.paypal.com/donate" method="post" target="_top" style="display:inline-block;margin:0 6px;">\n      <input type="hidden" name="hosted_button_id" value="DONATEID">\n      <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button">\n     </form>\n     <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top" style="display:inline-block;margin:0 6px;">\n      <input type="hidden" name="cmd" value="_s-xclick">\n      <input type="hidden" name="hosted_button_id" value="COFFEEID">\n      <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynow_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Buy me a coffee with PayPal">\n     </form>\n    </div>'''
    
    if basename in files_needing_support and 'support-card' not in html:
        # Add before the related-guides section
        related_pos = html.find('class="related-guides"')
        if related_pos > 0:
            # Find the opening div of related-guides
            rg_div_start = html.rfind('<', 0, related_pos)
            if rg_div_start > 0:
                html = html[:rg_div_start] + support_card + '\n\n' + html[rg_div_start:]
                fixes_applied.append("support-card-added")
    
    # 7. Add copyright-protection if missing  
    if 'copyright-protection' not in html:
        cp = '''\n<div class="copyright-protection" style="background:#faf8f5;border:1px solid #e8d5b7;border-radius:8px;padding:1rem 1.2rem;margin:1.5rem auto;max-width:780px;font-size:.82rem;color:#666;text-align:center;">\n <p style="margin:0;">&copy; 2026 OSRS Guru (osrsguru.com). All rights reserved. This guide was originally written for osrsguru.com by our strategy team. Unauthorized reproduction, scraping, or use for AI training is prohibited. <a href="../index.html" style="color:#b8860b;">Return to OSRS Guru</a></p>\n</div>\n'''
        # Add before footer
        footer_pos = html.find('<footer')
        if footer_pos > 0:
            html = html[:footer_pos] + cp + html[footer_pos:]
            fixes_applied.append("copyright-protection-added")
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Fixed: {', '.join(fixes_applied)}")
        return fixes_applied
    else:
        print(f"  No changes needed")
        return []

# Process each file
for fn in files:
    fp = os.path.join(GUIDES_DIR, fn)
    if os.path.exists(fp):
        print(f"\nProcessing {fn}:")
        fixes = fix_file(fp)
    else:
        print(f"\n  NOT FOUND: {fn}")
