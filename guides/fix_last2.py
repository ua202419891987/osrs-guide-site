#!/usr/bin/env python3
"""Fix remaining 2 files: ironman smithing (QS+TOC) and cheapest runecrafting (TOC)."""
import re

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

def generate_toc(html):
    h2s = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', html)
    if not h2s:
        return None
    toc = '<div class="toc">\n  <h3>Table of Contents</h3>\n  <ol>\n'
    for i, (hid, ht) in enumerate(h2s, 1):
        clean = re.sub(r'<[^>]+>', '', ht)
        toc += '    <li><a href="#%s">%d. %s</a></li>\n' % (hid, i, clean)
    toc += '  </ol>\n</div>'
    return toc

# 1. Ironman Smithing - QS is only in CSS, need to insert real QS div + TOC
with open(GUIDES_DIR + '/osrs-ironman-1-99-smithing-guide.html', 'r', encoding='utf-8') as f:
    html = f.read()

QS_SMITH = """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li><strong>Fastest XP:</strong> Gold bars + Goldsmith Gauntlets at Blast Furnace - 300K+ XP/hr</li>
    <li><strong>Quest skip:</strong> The Knight's Sword gives 12,725 XP - level 29 instant start</li>
    <li><strong>Best gold ore:</strong> Arzinian Mine (Between a Rock) - 2,000 gold ore/hr</li>
    <li><strong>Early (15-40):</strong> Iron bars at Blast Furnace - no coal needed, 62.5K XP/hr</li>
    <li><strong>Late game:</strong> Gold bars from 40-99, ~300K XP/hr with self-mined ore</li>
  </ul>
</div>"""

# Insert QS after the guide-intro line
pos = html.find('<p class="guide-intro">')
if pos > 0:
    div_end = html.find('</div>', pos)
    div_end = html.find('</div>', div_end + 1) + 6
    html = html[:div_end] + '\n' + QS_SMITH + '\n' + html[div_end:]
    print("Ironman Smith: QS inserted")
else:
    # Try after tag line
    pos = html.find('class="tag"')
    if pos > 0:
        div_end = html.find('</div>', pos) + 6
        html = html[:div_end] + '\n' + QS_SMITH + '\n' + html[div_end:]
        print("Ironman Smith: QS inserted after tag")
    else:
        print("Ironman Smith: Could not find insertion point")

# Insert TOC after QS
toc = generate_toc(html)
if toc:
    qs_end = html.find('</div>', html.find('quick-summary'))
    qs_end = html.find('</div>', qs_end + 1) + 6
    html = html[:qs_end] + '\n' + toc + '\n' + html[qs_end:]
    print("Ironman Smith: TOC added")
else:
    print("Ironman Smith: No h2s found")

with open(GUIDES_DIR + '/osrs-ironman-1-99-smithing-guide.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Ironman Smith: Done")

# 2. Cheapest Runecrafting - need TOC
with open(GUIDES_DIR + '/osrs-cheapest-99-runecrafting-2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

toc = generate_toc(html)
if toc:
    # Insert TOC after QS
    qs_end = html.find('</div>', html.find('quick-summary'))
    qs_end = html.find('</div>', qs_end + 1) + 6
    html = html[:qs_end] + '\n' + toc + '\n' + html[qs_end:]
    print("Runecrafting: TOC added after QS")
else:
    print("Runecrafting: No h2s found")

with open(GUIDES_DIR + '/osrs-cheapest-99-runecrafting-2026.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Runecrafting: Done")

print("\n=== All fixes complete ===")
