#!/usr/bin/env python3
"""Fix remaining 4 files that need QS and/or TOC insertion."""
import re

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

QS_MAGIC = """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li><strong>Cheapest to 99:</strong> Splashing at ~10-15M GP total, ~350 hrs (overnight AFK)</li>
    <li><strong>Profit method:</strong> Enchanting jewelry - can profit 20-50M GP while training to 99</li>
    <li><strong>Best AFK:</strong> Lunar spells (Tan Leather/String Jewelry) at 50K-65K XP/hr, low cost</li>
    <li><strong>Lunar path (70-99):</strong> Lunar Diplomacy quest into Tan Leather/String Jewelry/Plank Make</li>
    <li><strong>High Alch warning:</strong> 150-180M GP to 99 - 10-15x more expensive than splashing</li>
  </ul>
</div>"""

QS_CONSTRUCTION = """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li><strong>Fastest XP:</strong> Mahogany Tables at 950K+ XP/hr, ~155M GP total cost</li>
    <li><strong>Best balance:</strong> Oak Larders at 450K XP/hr, ~30M GP total - community standard</li>
    <li><strong>Cheapest AFK:</strong> Oak Dungeon Doors at 300K XP/hr, ~15M GP total</li>
    <li><strong>Myth. Cape Rack:</strong> ~380K XP/hr, ~25M GP, requires Dragon Slayer II</li>
    <li><strong>Budget (74-99):</strong> Oak Doors with Demon Butler, ~30 hours semi-AFK</li>
  </ul>
</div>"""

QS_HERBLORE = """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li><strong>Best value:</strong> Ranging potions (72+) at 162.5 XP each, ~3-5 GP/XP</li>
    <li><strong>Cheapest path 1-99:</strong> ~50M GP total using low-cost potions at each level</li>
    <li><strong>Early (1-38):</strong> Serum 207, Strength/Energy potions - minimal cost</li>
    <li><strong>Mid (38-72):</strong> Superantipoison (106.3 XP) and Prayer potions - sell to recoup costs</li>
    <li><strong>Use Zahur:</strong> 200 GP/herb to clean in Nardah - massive time savings</li>
  </ul>
</div>"""

def generate_toc(html):
    """Generate TOC from h2 tags."""
    h2s = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', html)
    if not h2s:
        return None
    toc = '<div class="toc">\n  <h3>Table of Contents</h3>\n  <ol>\n'
    for i, (hid, ht) in enumerate(h2s, 1):
        clean = re.sub(r'<[^>]+>', '', ht)
        toc += '    <li><a href="#%s">%d. %s</a></li>\n' % (hid, i, clean)
    toc += '  </ol>\n</div>'
    return toc

# 1. Magic guide
with open(GUIDES_DIR + '/osrs-1-99-magic-training-cheap-guide-2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the CSS-only quick-summary selector with real QS div
# Find guide-header intro area to insert QS
pos = html.find('<p class="guide-intro">')
if pos > 0:
    # Find end of this div
    div_end = html.find('</div>', pos)
    div_end = html.find('</div>', div_end + 1) + 6
    html = html[:div_end] + '\n' + QS_MAGIC + '\n' + html[div_end:]
    print("Magic: QS inserted after guide-intro")
else:
    print("Magic: Could not find guide-intro")

# Add TOC after QS
toc = generate_toc(html)
if toc:
    qs_end = html.find('</div>', html.find('quick-summary'))
    qs_end = html.find('</div>', qs_end + 1) + 6
    html = html[:qs_end] + '\n' + toc + '\n' + html[qs_end:]
    print("Magic: TOC added")
else:
    print("Magic: No h2s found for TOC")

with open(GUIDES_DIR + '/osrs-1-99-magic-training-cheap-guide-2026.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Magic: Done")

# 2. Construction guide
with open(GUIDES_DIR + '/osrs-construction-1-99-guide-2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('<!-- QUICK VERDICT -->')
if pos > 0:
    html = html[:pos] + QS_CONSTRUCTION + '\n\n' + html[pos:]
    print("Construction: QS inserted before QUICK VERDICT")
else:
    print("Construction: Could not find QUICK VERDICT marker")

with open(GUIDES_DIR + '/osrs-construction-1-99-guide-2026.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Construction: Done")

# 3. Thieving guide - add TOC
with open(GUIDES_DIR + '/osrs-1-99-thieving-guide-ironman.html', 'r', encoding='utf-8') as f:
    html = f.read()

toc = generate_toc(html)
if toc:
    sec_pos = html.find('<section>')
    if sec_pos > 0:
        html = html[:sec_pos] + toc + '\n' + html[sec_pos:]
        print("Thieving: TOC added before first section")
    else:
        print("Thieving: No section tag found")
else:
    print("Thieving: No h2s found for TOC")

with open(GUIDES_DIR + '/osrs-1-99-thieving-guide-ironman.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Thieving: Done")

# 4. Herblore guide
with open(GUIDES_DIR + '/osrs-low-cost-1-99-herblore-guide.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('<p class="guide-intro">')
if pos > 0:
    div_end = html.find('</div>', pos)
    div_end = html.find('</div>', div_end + 1) + 6
    html = html[:div_end] + '\n' + QS_HERBLORE + '\n' + html[div_end:]
    print("Herblore: QS inserted after guide-intro")
else:
    print("Herblore: Could not find guide-intro")

toc = generate_toc(html)
if toc:
    qs_end = html.find('</div>', html.find('quick-summary'))
    qs_end = html.find('</div>', qs_end + 1) + 6
    html = html[:qs_end] + '\n' + toc + '\n' + html[qs_end:]
    print("Herblore: TOC added")
else:
    print("Herblore: No h2s found for TOC")

with open(GUIDES_DIR + '/osrs-low-cost-1-99-herblore-guide.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Herblore: Done")

print("\n=== All remaining fixes complete ===")
