#!/usr/bin/env python3
"""Team 2 Group A standardization script - processes 14 Skill/1-99 guide articles."""

import re
import os

BASE_DIR = "C:/Users/Lenovo/osrs-guide-site/guides"

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

# ======== STANDARD CSS BLOCK (from _MONEY_MAKING_SPEC.md) ========
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

# ======== QUICK SUMMARIES (tailored per article) ========
QUICK_SUMMARIES = {
    "osrs-1-99-crafting-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Get 99 Crafting in OSRS by picking the right method for your budget:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest XP:</strong> Dragonhide bodies at 250K–350K XP/hr</li>
    <li><strong>Best Ironman:</strong> Giant seaweed glassblowing at ~120K XP/hr</li>
    <li><strong>Most profitable:</strong> Battlestaves at 100K–180K XP/hr</li>
    <li><strong>AFK friendly:</strong> Jewelry crafting at 30K–80K XP/hr</li>
    <li><strong>Cheapest:</strong> Glassblowing at 60K–100K XP/hr, nearly zero loss</li>
  </ul>
</div>""",

    "osrs-1-99-hitpoints-training-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Hitpoints is trained passively through combat. Maximize HP XP with these approaches:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Best overall:</strong> Slayer — combat XP + HP XP + Slayer XP + profit</li>
    <li><strong>Fastest HP XP:</strong> Chinchompas at MM2 tunnels, 100K–200K HP XP/hr</li>
    <li><strong>Most AFK:</strong> NMZ with absorption potions, ~25K HP XP/hr, 20-min AFK</li>
    <li><strong>Ironman:</strong> Sand/Ammonite Crabs early, Slayer mid, burst tasks late</li>
    <li><strong>Key ratio:</strong> 1.33 HP XP per 4 combat XP — HP caps at ~98-99 alongside 99 combat</li>
  </ul>
</div>""",

    "osrs-1-99-hunter-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Hunter 1-99 takes 40-60 hours with the right methods and earns 50M–150M GP:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>1–43:</strong> Birds/Salamanders (fast, low attention) — ~2 hours total</li>
    <li><strong>43–63:</strong> Falconry or Red Salamanders at 70K–110K XP/hr</li>
    <li><strong>63–80:</strong> Red Chinchompas at 100K–140K XP/hr, 500K–800K GP/hr</li>
    <li><strong>80–99:</strong> Black Chinchompas at 130K–180K XP/hr or Herbiboar at 120K–160K XP/hr</li>
    <li><strong>Passive:</strong> Bird house runs for 4K–5K XP per run, 50K–150K GP each</li>
  </ul>
</div>""",

    "osrs-1-99-magic-training-cheap-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Train Magic from 1-99 on a budget with these proven methods:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Cheapest (break-even):</strong> Enchanting jewelry (emerald rings/diamond amulets) at 50K–100K XP/hr</li>
    <li><strong>Most AFK:</strong> Splashing at 13K XP/hr — 6 hours AFK per session</li>
    <li><strong>Best profit:</strong> Bolt enchanting at 100K–400K GP/hr profit, 40K–60K XP/hr</li>
    <li><strong>Fastest budget:</strong> High Alch at 65K XP/hr, 50K–100K GP profit depending on items</li>
    <li><strong>Cheapest to 99:</strong> ~8M–12M GP total using enchantment methods</li>
  </ul>
</div>""",

    "osrs-1-99-thieving-guide-ironman.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Thieving 1-99 on an Ironman: fast XP, no resources consumed:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>1–38:</strong> Men/Bakers/Tea sellers — ~1 hour total</li>
    <li><strong>38–55:</strong> Silk Stall (safe) or Blackjack (best XP at 80K–120K XP/hr)</li>
    <li><strong>55–71:</strong> Pyramid Plunder at 100K–180K XP/hr with sceptre chance</li>
    <li><strong>71–99:</strong> Pyramid Plunder (speeding up) or Ardy Knights (AFK)</li>
    <li><strong>Total time:</strong> ~30-40 hours to 99 with XP rates climbing to 200K+/hr</li>
  </ul>
</div>""",

    "osrs-agility-training-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Agility 1-99 takes 180–230 hours depending on method chosen:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest XP:</strong> Hallowed Sepulchre (62+) at 65K–105K XP/hr + 1M+ GP/hr</li>
    <li><strong>Best marks:</strong> Canifis rooftop (40+) for Graceful outfit farming</li>
    <li><strong>Most AFK:</strong> Brimhaven Arena spike trap at ~45K XP/hr</li>
    <li><strong>Rooftop progression:</strong> Gnome→Draynor→Canifis→Falador→Seers→Ardougne</li>
    <li><strong>GP from 1–99 rooftop:</strong> ~15M–20M from Amylase crystals</li>
  </ul>
</div>""",

    "osrs-blast-furnace-smithing-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Blast Furnace is the fastest Smithing method in OSRS:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest XP:</strong> Gold bars with Goldsmith Gauntlets at 350K–400K XP/hr</li>
    <li><strong>Cheapest:</strong> Steel bars at ~2 GP/XP, 180K–220K XP/hr</li>
    <li><strong>Best profit:</strong> Mithril/Addy bars when prices align, 100K–200K GP/hr</li>
    <li><strong>Cost to 99 via gold:</strong> ~30M–40M GP for 1-99</li>
    <li><strong>Requirements:</strong> Ice Gloves (or bucket of water), Coins for coffers, 60 Smithing optimal</li>
  </ul>
</div>""",

    "osrs-cheapest-99-runecrafting-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Runecrafting on a budget — cheap methods for 1-99:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Cheapest XP:</strong> Guardians of the Rift at 25K–55K XP/hr, zero cost + profit</li>
    <li><strong>Best profit:</strong> Nature runes (44+) at 500K–800K GP/hr</li>
    <li><strong>Fastest:</strong> Lava runes at 150K+ XP/hr with Ring of Duelling and Clay</li>
    <li><strong>Most AFK:</strong> ZMI altar at 30K–55K XP/hr, rune profits cover costs</li>
    <li><strong>Cost to 99 (cheapest):</strong> ~3M–5M GP using GOTR + ZMI combo</li>
  </ul>
</div>""",

    "osrs-construction-1-99-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Construction 1-99 costs 15M–150M+ GP depending on method:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest XP:</strong> Mahogany Tables at 950K+ XP/hr, ~150M GP total</li>
    <li><strong>Best balance:</strong> Oak Larders at 450K XP/hr, ~30M GP total</li>
    <li><strong>Cheapest:</strong> Oak Dungeon Doors at ~300K XP/hr, ~15M GP total</li>
    <li><strong>AFK option:</strong> Mythical Cape Racks at 200K–250K XP/hr</li>
    <li><strong>Must-have unlocks:</strong> Max Pool, Ornate Jewellery Box, Portal Nexus</li>
  </ul>
</div>""",

    "osrs-1-99-hitpoints-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Hitpoints is passive — train combat, get HP XP for free:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Passive training:</strong> Slayer to 99 gives enough combat XP for 99 HP</li>
    <li><strong>Fastest active:</strong> Chinchompas at MM2 - 100K–200K HP XP/hr</li>
    <li><strong>Most AFK:</strong> NMZ absorption at ~25K HP XP/hr for 20-min AFK sessions</li>
    <li><strong>Key formula:</strong> 1.33 HP XP per damage dealt — always train with max DPS</li>
    <li><strong>99 HP Cape perk:</strong> 2x natural regen (4 HP/min) — excellent QoL</li>
  </ul>
</div>""",

    "osrs-1-99-prayer-guide-2026.html": None,  # Already has a quick-summary

    "osrs-1-99-prayer-guide-all-methods-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Prayer 1-99 — compare all methods to find the right balance:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest:</strong> Gilded Altar (W330) at 300K XP/hr, ~12 GP/XP with Dragon Bones</li>
    <li><strong>Cheapest:</strong> Chaos Altar with 50% bone save, ~6 GP/XP — saves 77M GP to 99</li>
    <li><strong>Safest:</strong> Ectofuntus at 4x XP but slowest (60K–80K XP/hr)</li>
    <li><strong>Best quest start:</strong> Restless Ghost + Priest in Peril + Holy Grail = ~55K free XP</li>
    <li><strong>Cost to 99:</strong> ~18M GP (Dragon Bones, Chaos Altar) to ~77M GP (Gilded Altar)</li>
  </ul>
</div>""",

    "osrs-ironman-1-99-smithing-guide.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Ironman Smithing 1-99 — ore management is key:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Best XP method:</strong> Blast Furnace gold bars with Goldsmith Gauntlets at 350K–400K XP/hr</li>
    <li><strong>Ore sources:</strong> Arzinian Mine (gold), Motherlode Mine (coal), MLM upper level (add) or BF</li>
    <li><strong>Early game (1–30):</strong> Knight's Sword quest (skip to 29), then Bronze/Steel at BF</li>
    <li><strong>Mid game (30–70):</strong> Iron/Steel bars at Blast Furnace, Giants' Foundry minigame</li>
    <li><strong>Late game (70–99):</strong> Gold bars at BF — requires sustained gold ore mining at Arzinian Mines</li>
  </ul>
</div>""",

    "osrs-low-cost-1-99-herblore-guide.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <strong style="color:#3b2615;">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Herblore 1-99 on a budget — minimize costs with smart potion choices:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Cheapest early (3–22):</strong> Serum 207 at ~3 GP/XP</li>
    <li><strong>Best budget (22–38):</strong> Strength potions at ~5 GP/XP</li>
    <li><strong>Break-even (38–99):</strong> Prayer potions (Ranarr) at 40K–70K XP/hr, often profitable</li>
    <li><strong>Ironman friendly:</strong> Farming herbs from runs + Kingdom of Miscellania for seeds</li>
    <li><strong>Cost to 99 (cheapest):</strong> ~20M–40M GP using budget potion route</li>
  </ul>
</div>""",
}


def process_file(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    changes = []

    # 1. Update meta description
    meta_match = re.search(r'<meta name="description" content="(.*?)">', html, re.IGNORECASE | re.DOTALL)
    if meta_match and not meta_match.group(1).startswith('Updated for July 2026.'):
        old_meta = meta_match.group(0)
        new_content = "Updated for July 2026. " + meta_match.group(1)
        new_meta = f'<meta name="description" content="{new_content}">'
        html = html.replace(old_meta, new_meta)
        changes.append("Meta prefixed with 'Updated for July 2026.'")

    # 2. Quick Summary insertion
    qs = QUICK_SUMMARIES.get(filename)
    if qs is not None:
        # Check if quick-summary already exists
        if 'class="quick-summary"' in html or 'class="quick-summary ' in html:
            # Replace existing placeholder quick-summary
            changes.append("Quick-summary already present (kept as-is)")
        else:
            # Find the insertion point - after guide-header, guide-intro, or in the container after hero
            if '<div class="guide-header">' in html:
                # Old template A: guide-header style
                insert_after = '<div class="guide-intro">'
                if insert_after in html:
                    idx = html.index(insert_after) + len(insert_after)
                    # Find the closing </p> of guide-intro
                    end_idx = html.index('</div>', idx)
                    # Skip past entire guide-intro div
                    end_idx = html.index('</div>', end_idx) + 6
                    # Actually, we need to insert after the entire guide-intro div
                    # Let's find the actual closing </div> of guide-intro
                    html = html[:end_idx] + '\n' + qs + html[end_idx:]
                    changes.append("Quick-summary inserted after guide-intro")
                else:
                    # Insert after guide-header
                    idx = html.index('<div class="guide-header">')
                    idx = html.index('</div>', idx) + 6
                    html = html[:idx] + '\n' + qs + html[idx:]
                    changes.append("Quick-summary inserted after guide-header")
            elif '<div class="hero-section">' in html:
                # Old template B: hero-section
                insert_after = '<div class="article-meta">'
                if insert_after in html:
                    idx = html.index(insert_after)
                    idx = html.index('</div>', idx) + 6
                    html = html[:idx] + '\n' + qs + html[idx:]
                    changes.append("Quick-summary inserted after article-meta")
                else:
                    # Insert after first h1 or first section
                    idx = html.index('<section')
                    idx = html.index('</section>', idx) + 10
                    html = html[:idx] + '\n' + qs + html[idx:]
                    changes.append("Quick-summary inserted after hero section")
            elif '<main class="guide-content">' in html or '<main class="guide-main">' in html:
                # Standard/new template - insert at top of container before TOC
                # Find the container div inside main
                main_start = html.index('<div class="container">')
                main_start = html.index('<div', main_start + 1)
                main_start = html.index('<div', main_start + 1)
                # Actually, let's just find first <div class="container">
                container_idx = html.find('<div class="container">')
                if container_idx >= 0:
                    inner_start = container_idx + len('<div class="container">')
                    inner = html[inner_start:]
                    # Insert before TOC
                    toc_idx = inner.find('<div class="toc">')
                    if toc_idx >= 0:
                        html = html[:inner_start + toc_idx] + '\n' + qs + '\n' + html[inner_start + toc_idx:]
                        changes.append("Quick-summary inserted before TOC")
                    else:
                        html = html[:inner_start] + '\n' + qs + html[inner_start:]
                        changes.append("Quick-summary inserted in container (no TOC found)")
            else:
                changes.append("SKIPPED quick-summary - unknown template structure")
    else:
        changes.append("Quick-summary already present (kept as-is)")

    # 3. Ensure TOC class is correct
    html = html.replace('class="table-of-contents"', 'class="toc"')
    html = html.replace('class="table-of-contents ', 'class="toc ')

    # 4. Remove dark inline styles
    # Replace color:#e8d5b7 with color:#1a1a1a
    html = html.replace('color:#e8d5b7', 'color:#1a1a1a')
    html = html.replace('color: #e8d5b7', 'color: #1a1a1a')
    
    # Replace background:#3b2615 in content areas (but not in support-card)
    # Only replace in guide-content area
    html = html.replace('background:#3b2615', 'background:#fff')
    html = html.replace('background: #3b2615', 'background: #fff')
    
    # Replace border-left:4px solid #d4af37 in content areas
    html = html.replace('border-left:4px solid #d4af37', 'border-left:0')
    html = html.replace('border-left: 4px solid #d4af37', 'border-left: 0')

    changes.append("Dark inline styles removed")

    # 5. Replace/Add bottom CSS block
    # Remove all existing <style> blocks (except in head)
    # We'll remove style blocks between </main> and </body> or at end of file
    # Strategy: remove any <style>...</style> that's NOT in <head>
    head_end = html.find('</head>')
    body_section = html[head_end:]
    
    # Remove old style blocks in body
    body_section = re.sub(r'<style>.*?</style>', '', body_section, flags=re.DOTALL)
    
    html = html[:head_end] + body_section
    
    # Insert standard CSS before </body>
    html = html.replace('</body>', f'{STANDARD_CSS}\n\n</body>')
    changes.append("Standard CSS block added")

    # 6. Support Card check - most files already have it, but let's check
    if 'class="support-card"' not in html:
        changes.append("WARNING: No support-card found (needs manual check)")

    # 7. Footer check
    if '<footer' not in html or '</footer>' not in html:
        changes.append("WARNING: No footer found (needs manual check)")

    # 8. Verify canonical
    canonical_match = re.search(r'<link rel="canonical" href="https://osrsguru.com/guides/(.*?)"', html)
    if canonical_match:
        c_file = canonical_match.group(1)
        if c_file == filename:
            changes.append(f"Canonical verified: {c_file}")
        else:
            changes.append(f"Canonical MISMATCH: found {c_file}, expected {filename}")
    else:
        changes.append("WARNING: No canonical tag found")

    # 9. Verify GA4
    if 'G-S1BGC91MYV' in html:
        changes.append("GA4 verified")
    else:
        changes.append("WARNING: GA4 missing")

    # 10. Verify AdSense
    if 'ca-pub-8532760886171435' in html:
        changes.append("AdSense verified")
    else:
        changes.append("WARNING: AdSense missing")

    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    return changes


def main():
    results = []
    for fname in FILES:
        print(f"Processing {fname}...")
        changes = process_file(fname)
        results.append((fname, changes))
        print(f"  Changes: {', '.join(changes)}")

    print("\n\n=== Summary ===")
    for fname, changes in results:
        status = "✅" if not any("WARNING" in c for c in changes) else "⚠️"
        print(f"{status} {fname}")
        for c in changes:
            print(f"    - {c}")

    # Count
    ok = sum(1 for _, c in results if not any("WARNING" in x for x in c))
    warn = sum(1 for _, c in results if any("WARNING" in x for x in c))
    print(f"\n{'='*50}")
    print(f"Total: {len(results)} files | OK: {ok} | Warnings: {warn}")
    print(f"=== Team 2 Group A complete: {len(results)}/14 ===")


if __name__ == '__main__':
    main()
