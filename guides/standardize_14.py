#!/usr/bin/env python3
"""Standardize 14 OSRS guide articles with meta, Quick Summary, CSS overlay, dates."""

import re
import os

GUIDES_DIR = r"c:\Users\Lenovo\osrs-guide-site\guides"

FILES = [
    "osrs-1-99-crafting-guide-2026.html",
    "osrs-1-99-hitpoints-training-guide-2026.html",
    "osrs-1-99-hunter-guide-2026.html",
    "osrs-1-99-magic-training-cheap-guide-2026.html",
    "osrs-1-99-thieving-guide-ironman.html",
    "osrs-agility-training-guide-2026.html",
    "osrs-blast-furnace-smithing-guide-2026.html",
    "osrs-cheapest-99-runecrafting-2026.html",
    "osrs-construction-1-99-guide-2026.html",
    "osrs-1-99-hitpoints-guide-2026.html",
    "osrs-1-99-prayer-guide-2026.html",
    "osrs-1-99-prayer-guide-all-methods-2026.html",
    "osrs-ironman-1-99-smithing-guide.html",
    "osrs-low-cost-1-99-herblore-guide.html",
]

# Standard CSS overlay block to insert before </body>
STANDARD_CSS = """<style>
.guide-content { color:#1a1a1a !important; }
.guide-content li,
.guide-content p,
.guide-content td,
.guide-content th,
.guide-content h3,
.guide-content h4 { color:#1a1a1a !important; }

.guide-content .tip-box,
.guide-content .method-box,
.guide-content .action-step,
.guide-content .quick-verdict,
.guide-content .faq-item,
.guide-content .warning-box,
.guide-content .info-box,
.guide-content .pro-tip-box,
.guide-content .note-box,
.guide-content .highlight-box,
.guide-content .strategy-box,
.guide-content .gear-box,
.guide-content .setup-box,
.guide-content .location-box,
.guide-content .next-steps,
.guide-content .bond-roadmap,
.guide-content .profit-box,
.guide-content .risk-box,
.guide-content .req-box { background:#fff !important; border:1px solid #e0d5c0 !important; }

.guide-content .tip-box p,
.guide-content .tip-box li,
.guide-content .method-box p,
.guide-content .method-box li,
.guide-content .faq-item p,
.guide-content .faq-item li,
.guide-content .quick-verdict p,
.guide-content .action-step p,
.guide-content .warning-box p,
.guide-content .warning-box li,
.guide-content .info-box p,
.guide-content .info-box li,
.guide-content .pro-tip-box p,
.guide-content .pro-tip-box li,
.guide-content .note-box p,
.guide-content .note-box li,
.guide-content .highlight-box p,
.guide-content .highlight-box li,
.guide-content .strategy-box p,
.guide-content .strategy-box li,
.guide-content .gear-box p,
.guide-content .gear-box li,
.guide-content .setup-box p,
.guide-content .setup-box li,
.guide-content .location-box p,
.guide-content .location-box li,
.guide-content .next-steps p,
.guide-content .next-steps li,
.guide-content .bond-roadmap p,
.guide-content .bond-roadmap li,
.guide-content .profit-box p,
.guide-content .profit-box li,
.guide-content .risk-box p,
.guide-content .risk-box li,
.guide-content .req-box p,
.guide-content .req-box li { color:#1a1a1a !important; }

.guide-content .faq-item h3,
.guide-content .faq-item h4,
.guide-content .method-box h3,
.guide-content .method-box h4,
.guide-content .quick-verdict h3,
.guide-content .action-step h4,
.guide-content .tip-box strong,
.guide-content .method-box strong,
.guide-content .warning-box strong,
.guide-content .info-box strong,
.guide-content .pro-tip-box strong,
.guide-content .note-box strong,
.guide-content .highlight-box strong,
.guide-content .strategy-box strong,
.guide-content .gear-box strong,
.guide-content .setup-box strong,
.guide-content .location-box strong,
.guide-content .next-steps strong,
.guide-content .bond-roadmap strong,
.guide-content .profit-box strong,
.guide-content .risk-box strong,
.guide-content .req-box strong { color:#3b2615 !important; }

.guide-content [style*="border-left:4px"],
.guide-content [style*="border-left: 4px"],
.guide-content [style*="border-left:3px"],
.guide-content [style*="border-left: 3px"],
.guide-content [style*="border-left:5px"],
.guide-content [style*="border-left: 5px"] { border-left:0 !important; }

.guide-content .related-guides .article-card { background:#f5f2f8 !important; border-color:#D4CDE0 !important; }
.guide-content .related-guides .article-card:hover { background:#f0ecf5 !important; border-color:#9B84D4 !important; }
.guide-content .toc { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }
.guide-content .quick-summary { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }

@media (max-width: 768px) {
    .guide-content table { font-size: 0.85rem; }
    .guide-content table thead tr th { padding: 8px 10px; font-size: 0.8rem; }
    .guide-content table tbody td { padding: 6px 10px; }
    .guide-content h2 { font-size: 1.4em; }
    .guide-content h3 { font-size: 1.15em; }
}
@media (max-width: 640px) {
    .guide-content table { display: block; overflow-x: auto; }
    .guide-content h2 { font-size: 1.25em; }
    .guide-content h3 { font-size: 1.05em; }
}
</style>"""

# Quick Summary HTML template
QS_TEMPLATE = """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
    <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
    <p style="margin:0;color:#2D2A33;font-size:.92rem;line-height:1.8;">{summary}</p>
</div>"""


def get_summary(filename, content):
    """Generate a summary based on article type."""
    name = filename.lower()
    if "crafting" in name and "ironman" not in name:
        return "Complete OSRS 1-99 Crafting guide covering glassblowing (120K XP/hr, best for Ironmen), battlestaves (profitable, 100-180K XP/hr), dragonhide crafting (fastest at 350K XP/hr), and all methods compared with cost analysis."
    elif "hitpoints-training" in name:
        return "Complete OSRS 1-99 Hitpoints training guide covering passive XP mechanics, best combat methods (NMZ, Slayer, chins), XP rates, Ironman strategies, and how to maximize HP gains alongside other combat skills."
    elif "hitpoints-guide" in name and "training" not in name:
        return "Complete OSRS 1-99 Hitpoints guide covering Melee, Ranged, and Magic methods, Nightmare Zone AFK training, Slayer as the best overall method, and Ironman-specific strategies for passive HP gains."
    elif "hunter" in name:
        return "Complete OSRS 1-99 Hunter guide covering fastest methods (chins, falconry, herbiboar), XP rates, profit analysis, bird house runs, and 3-tick manipulation for max XP/hr."
    elif "magic" in name:
        return "Complete OSRS 1-99 Magic training guide for budget players covering enchanting jewelry for profit, splashing AFK methods, Lunar spells, and low-cost alternatives to expensive High Alchemy."
    elif "thieving" in name:
        return "Complete OSRS 1-99 Thieving guide for Ironman accounts covering Pyramid Plunder (fastest XP), Ardougne Knights (best AFK), Master Farmers for seeds, and key rewards worth 10-15M GP."
    elif "agility" in name:
        return "Complete OSRS Agility training guide 1-99 covering rooftop courses, Hallowed Sepulchre (100K+ XP/hr), Brimhaven Arena, Wilderness course, Marks of Grace farming, and GP/hr for every level range."
    elif "blast-furnace" in name:
        return "Complete OSRS Blast Furnace Smithing guide covering all ore types, XP rates (140-170K XP/hr with gold), profit/loss per bar, Ice gloves method, gold smelting for profit, and Ironman strategies."
    elif "runecrafting" in name:
        return "Complete OSRS cheapest 99 Runecrafting guide covering Lava Runes (~8M total cost), ZMI (~20M), and Guardians of the Rift (zero cost), with full gear setups and cost breakdowns for each method."
    elif "construction" in name:
        return "Complete OSRS Construction 1-99 guide covering cheapest methods (Oak Dungeon Doors, ~15M GP), fastest XP (Mahogany Tables, 950K XP/hr), and the best balance (Oak Larders, 450K XP/hr, ~30M GP)."
    elif "prayer-all" in name or "prayer-guide-all" in name:
        return "Complete OSRS 1-99 Prayer guide covering all methods including Gilded Altar, Chaos Altar, Ectofuntus, Ensouled Heads, and Summer Sweep-Up 2026 changes with cost analysis for each bone type."
    elif "prayer" in name:
        return "Complete OSRS 1-99 Prayer guide covering Gilded Altar (300K XP/hr, safe), Chaos Altar (cheapest at ~6 GP/XP), Ectofuntus (4x XP), and Ensouled Heads with complete cost comparisons."
    elif "ironman" in name and "smithing" in name:
        return "Complete OSRS Ironman 1-99 Smithing guide covering Blast Furnace strategies, gold bar methods (300K+ XP/hr with gauntlets), ore sourcing as an Ironman, and anvil training routes."
    elif "herblore" in name:
        return "Complete OSRS Low Cost 1-99 Herblore guide covering cheapest potions at each level, ranging potions as the best value (3-5 GP/XP), Ironman herb sourcing, and cost-cutting tips."
    else:
        return "Complete OSRS 1-99 guide covering all training methods, XP rates, cost analysis, and Ironman strategies. Updated for July 2026."


def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    ops = []

    # 1. Update meta description - prepend "Updated for July 2026."
    meta_pattern = r'(<meta\s+name="description"\s+content=")([^"]+)(")'
    def update_meta(m):
        prefix = m.group(1)
        content = m.group(2)
        suffix = m.group(3)
        if not content.startswith("Updated for July 2026."):
            content = "Updated for July 2026. " + content
        return prefix + content + suffix
    html = re.sub(meta_pattern, update_meta, html, count=1)
    ops.append("MetaUpdated")

    # 2. Check for Quick Summary, add if missing
    has_qs = False
    # Check for any quick-summary, quick-verdict, or quick-answer class
    if re.search(r'class="[^"]*\bquick-summary\b[^"]*"', html, re.IGNORECASE):
        has_qs = True
    if re.search(r'class="[^"]*\bquick-verdict\b[^"]*"', html, re.IGNORECASE):
        has_qs = True
    if re.search(r'class="[^"]*\bquick-answer\b[^"]*"', html, re.IGNORECASE):
        has_qs = True

    if not has_qs:
        # Find the TOC div and insert Quick Summary before it
        summary = get_summary(filename, html)
        qs_html = QS_TEMPLATE.format(summary=summary)
        # Insert after first <div class="container"> that is inside <main class="guide-content">
        # Pattern: find the container right after guide-content starts
        toc_match = re.search(r'(<div\s+class="toc"[^>]*>)', html)
        if toc_match:
            insert_pos = toc_match.start()
            # Check if there's already content before TOC that should remain
            html = html[:insert_pos] + qs_html + "\n\n" + html[insert_pos:]
            ops.append("QSAdded")
        else:
            # No TOC found - try inserting after container div inside guide-content
            cont_match = re.search(r'(<main\s+class="guide-content"[^>]*>\s*<div\s+class="container"[^>]*>)', html)
            if cont_match:
                insert_pos = cont_match.end()
                html = html[:insert_pos] + "\n" + qs_html + "\n" + html[insert_pos:]
                ops.append("QSAdded")
            else:
                ops.append("QSNoTOC")
    else:
        ops.append("QSExists")

    # 3. Remove inline dark styles in body content
    # Remove color:#e8d5b7 etc. inline styles from paragraphs
    html = re.sub(r'\bcolor\s*:\s*#e8d5b7\b', 'color:#1a1a1a', html, flags=re.IGNORECASE)
    # Remove specific inline dark backgrounds
    html = re.sub(r'\bbackground\s*:\s*#3b2615\b', 'background:#fff', html, flags=re.IGNORECASE)
    html = re.sub(r'\bbackground\s*:\s*#2a1a0a\b', 'background:#fff', html, flags=re.IGNORECASE)
    # Remove border-left:4px solid #d4af37 inline (for copyright notices etc, it's fine - CSS handles it)
    ops.append("ColorsCleaned")

    # 4. Replace existing CSS block before </body> with standard one
    # Remove any existing style blocks that contain the P0 Standard patterns
    # Find all <style>...</style> before </body>
    def replace_css_block(html):
        # Find the last </style> before </body>
        body_close = html.rfind("</body>")
        if body_close == -1:
            return html
        
        # Get everything before </body>
        before_body = html[:body_close]
        
        # Remove all <style>...</style> blocks before </body>
        cleaned = re.sub(r'<style>.*?</style>\s*', '', before_body, flags=re.DOTALL)
        
        # Also remove double/triple empty lines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned + "\n" + STANDARD_CSS + "\n\n</body>"

    html = replace_css_block(html)
    ops.append("CSSReplaced")

    # 5. Update dates - convert June 2026 to July 2026
    # Match "June 2026" but not inside URLs or code
    html = html.replace("June 2026", "July 2026")
    html = html.replace("June 7, 2026", "July 7, 2026")
    html = html.replace("June 8, 2026", "July 8, 2026")
    html = html.replace("June 1, 2026", "July 1, 2026")
    html = html.replace("June 6, 2026", "July 6, 2026")
    html = html.replace("June 30, 2026", "July 30, 2026")
    ops.append("DatesUpdated")

    # 6. Verify canonical URL
    canonical_pattern = r'<link\s+rel="canonical"\s+href="https://osrsguru\.com/guides/' + re.escape(filename) + r'"'
    if re.search(canonical_pattern, html):
        ops.append("CanonicalVerified")
    else:
        ops.append("CanonicalCHECK")

    # Write to temp dir in /tmp
    temp_dir = "/tmp"
    temp_path = os.path.join(temp_dir, "osrs_" + filename)
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(html)

    return ops


# Main processing
results = []
for fname in FILES:
    fpath = os.path.join(GUIDES_DIR, fname)
    if not os.path.exists(fpath):
        results.append(f"❌ {fname} — NOT FOUND")
        continue
    ops = process_file(fpath)
    ops_str = " + ".join(ops)
    results.append(f"✅ {fname} — {ops_str}")
    print(f"✅ {fname} — {ops_str}")

print(f"\n=== Group A complete: {len(results)}/{len(FILES)} ===")
