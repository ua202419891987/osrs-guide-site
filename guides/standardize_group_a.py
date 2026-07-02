#!/usr/bin/env python3
"""
Team 2: Standardize 14 Group A skill training guide articles.
Per-file: Meta+30s+TOC+CSS+Support+Footer
"""
import re
import os

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"
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

STANDARD_CSS_BLOCK = '''<style>
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
</style>'''

# ===== Quick Summaries for each article =====
QUICK_SUMMARIES = {
    "osrs-1-99-crafting-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP:</strong> Dragonhide bodies at 250K–350K XP/hr (expensive, ~6M-8M GP/hr)</li>
    <li><strong>Best Ironman:</strong> Giant seaweed glassblowing at ~120K XP/hr, profitable</li>
    <li><strong>Best profit:</strong> Battlestaves at 100K–180K XP/hr, 500K-2M GP/hr profit</li>
    <li><strong>Budget to 99:</strong> Glassblowing unpowered orbs (46-87) + light orbs (87-99), ~7M profit</li>
    <li><strong>Fast route to 99:</strong> Dragonhide bodies, 35-40 hours, ~50M-80M total cost</li>
  </ul>
</div>''',

    "osrs-1-99-hitpoints-training-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Hitpoints is passive:</strong> 1.33 HP XP per damage dealt — train combat, get HP</li>
    <li><strong>Fastest HP XP:</strong> Chinchompas at Maniacal Monkeys — 100K-200K HP XP/hr</li>
    <li><strong>Best AFK:</strong> Nightmare Zone with absorption potions — ~25K HP XP/hr, 20-min AFK</li>
    <li><strong>Slayer is optimal:</strong> Train combat + Slayer + HP simultaneously for best efficiency</li>
    <li><strong>99 HP Cape:</strong> 2x natural HP regen (4 HP/min), +4 prayer bonus</li>
  </ul>
</div>''',

    "osrs-1-99-hunter-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP (1-99):</strong> Black chinchompas at 200K-600K XP/hr — expensive but best</li>
    <li><strong>Best profit:</strong> Herbiboar (level 80+) at 50K-80K XP/hr + 500K-1M GP/hr in herbs</li>
    <li><strong>Most AFK:</strong> Bird houses (level 5+) — 2-min runs every 50 min, 5K-15K XP/hr passive</li>
    <li><strong>Budget training:</strong> Falconry/Swamp lizards at 30K-60K XP/hr, low cost</li>
    <li><strong>Time to 99:</strong> ~50-60 hours with black chins, ~120+ hours with budget methods</li>
  </ul>
</div>''',

    "osrs-1-99-magic-training-cheap-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Cheapest to 99:</strong> Splashing at ~10-15M GP total, ~350 hrs (overnight AFK)</li>
    <li><strong>Profit method:</strong> Enchanting jewelry — can profit 20-50M GP while training to 99</li>
    <li><strong>Best AFK:</strong> Lunar spells (Tan Leather/String Jewelry) at 50K-65K XP/hr, low cost</li>
    <li><strong>Lunar path (70-99):</strong> Lunar Diplomacy quest → Tan Leather/String Jewelry/Plank Make</li>
    <li><strong>High Alch warning:</strong> 150-180M GP to 99 — 10-15x more expensive than splashing</li>
  </ul>
</div>''',

    "osrs-1-99-thieving-guide-ironman.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP:</strong> Pyramid Plunder at 280K+ XP/hr (level 91+), 40-60 hours to 99</li>
    <li><strong>Best AFK:</strong> Ardougne Knights at 250K XP/hr, 10-15M GP earned to 99</li>
    <li><strong>GP earned 1-99:</strong> 10-15M GP (with Rogues' Outfit doubling coin drops)</li>
    <li><strong>Key unlock:</strong> Rogues' Outfit (50 Thieving+Agility) — mandatory for GP farming</li>
    <li><strong>Master Farmers:</strong> Start at 38 for ranarr/snapdragon seeds — bank 200+ ranarr seeds</li>
  </ul>
</div>''',

    "osrs-agility-training-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP:</strong> Hallowed Sepulchre (62+) at 50K-105K XP/hr, 180-200 hrs to 99</li>
    <li><strong>GP earned 1-99 (rooftops):</strong> 15-20M GP from Marks of Grace → Amylase crystals</li>
    <li><strong>Sepulchre profit:</strong> 1M+ GP/hr, rare Ring of Endurance worth ~6M GP</li>
    <li><strong>Graceful outfit:</strong> Farm Canifis (40+) for full set before progressing</li>
    <li><strong>Brimhaven Arena:</strong> 30K XP/hr at level 20 — 3x faster than Draynor rooftop</li>
  </ul>
</div>''',

    "osrs-blast-furnace-smithing-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP:</strong> Gold bars + goldsmith gauntlets at 140K-170K XP/hr</li>
    <li><strong>Profit:</strong> Most bar types are profitable — earn 300K-600K GP/hr while training</li>
    <li><strong>Half coal cost:</strong> Steel needs 1 coal (not 2), mithril 2 (not 4), adamant 3 (not 6)</li>
    <li><strong>Gold to 99 profit:</strong> ~33M GP profit from 40-99 with goldsmith gauntlets</li>
    <li><strong>Iron method:</strong> Iron bars need NO coal at Blast Furnace — cheapest training option</li>
  </ul>
</div>''',

    "osrs-cheapest-99-runecrafting-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Free method:</strong> Guardians of the Rift (GOTR) — zero cost, 30K-70K XP/hr</li>
    <li><strong>Cheapest direct:</strong> Lava runes at ~8-9M GP total to 99, 55K-72K XP/hr</li>
    <li><strong>ZMI Altar:</strong> ~20M GP total to 99, 40K-55K XP/hr, beginner-friendly</li>
    <li><strong>Key unlocks:</strong> Colossal Pouch (85 RC, 40 essence) from GOTR, Magic Imbue from Lunar</li>
    <li><strong>Time to 99:</strong> ~200 hrs (lava runes), ~290 hrs (GOTR), ~270 hrs (ZMI)</li>
  </ul>
</div>''',

    "osrs-construction-1-99-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP:</strong> Mahogany Tables at 950K+ XP/hr, ~155M GP total cost</li>
    <li><strong>Best balance:</strong> Oak Larders at 450K XP/hr, ~30M GP total — community standard</li>
    <li><strong>Cheapest AFK:</strong> Oak Dungeon Doors at 300K XP/hr, ~15M GP total</li>
    <li><strong>Myth. Cape Rack:</strong> ~380K XP/hr, ~25M GP, requires Dragon Slayer II</li>
    <li><strong>Budget (74-99):</strong> Oak Doors with Demon Butler, ~30 hours semi-AFK</li>
  </ul>
</div>''',

    "osrs-1-99-hitpoints-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Hitpoints is passive:</strong> 1.33 HP XP per damage dealt — train combat, get HP</li>
    <li><strong>Fastest HP XP:</strong> Chinchompas at Maniacal Monkeys — 100K-200K HP XP/hr</li>
    <li><strong>Best AFK:</strong> Nightmare Zone with absorption potions — ~25K HP XP/hr, 20-min AFK</li>
    <li><strong>Slayer is optimal:</strong> Train combat + Slayer + HP simultaneously for best efficiency</li>
    <li><strong>99 HP Cape:</strong> 2x natural HP regen (4 HP/min), +4 prayer bonus</li>
  </ul>
</div>''',

    "osrs-1-99-prayer-guide-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>43 Prayer (Protect from Melee)</strong> is the #1 priority — 100% damage reduction</li>
    <li><strong>Gilded Altar (W330):</strong> 300K XP/hr, safe, ~12 GP/XP with dragon bones</li>
    <li><strong>Chaos Altar:</strong> 50% bone save = ~6 GP/XP best value — saves ~77M GP to 99</li>
    <li><strong>Do quests first:</strong> Restless Ghost + Priest in Peril + Holy Grail = ~55K free XP</li>
    <li><strong>Time to 99:</strong> ~43 hrs (dragon bones Gilded), ~26 hrs (superior dragon bones)</li>
  </ul>
</div>''',

    "osrs-1-99-prayer-guide-all-methods-2026.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>43 Prayer (Protect from Melee)</strong> is essential — do quests first for ~44 free</li>
    <li><strong>Gilded Altar (W330):</strong> 300K XP/hr, ~12 GP/XP, completely safe</li>
    <li><strong>Chaos Altar:</strong> 3.5x + 50% bone save = ~6 GP/XP, saves ~77M GP to 99</li>
    <li><strong>Best for Ironmen:</strong> Ectofuntus at 4x XP (slow but safe) or Chaos Altar at 7x effective</li>
    <li><strong>Summer Sweep-Up 2026:</strong> Buffed Arceuus Offering to 3.5x, new Wyrmscraig Altar</li>
  </ul>
</div>''',

    "osrs-ironman-1-99-smithing-guide.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Fastest XP:</strong> Gold bars + Goldsmith Gauntlets at Blast Furnace — 300K+ XP/hr</li>
    <li><strong>Quest skip:</strong> The Knight's Sword gives 12,725 XP — level 29 instant start</li>
    <li><strong>Best gold ore:</strong> Arzinian Mine (Between a Rock) — 2,000 gold ore/hr</li>
    <li><strong>Early (15-40):</strong> Iron bars at Blast Furnace — no coal needed, 62.5K XP/hr</li>
    <li><strong>Late game:</strong> Gold bars from 40-99, ~300K XP/hr with self-mined ore</li>
  </ul>
</div>''',

    "osrs-low-cost-1-99-herblore-guide.html": '''<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
  <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30-Second Quick Summary</h3>
  <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
    <li>📌 <strong>Best value:</strong> Ranging potions (72+) at 162.5 XP each, ~3-5 GP/XP</li>
    <li><strong>Cheapest path 1-99:</strong> ~50M GP total using low-cost potions at each level</li>
    <li><strong>Early (1-38):</strong> Serum 207, Strength/Energy potions — minimal cost</li>
    <li><strong>Mid (38-72):</strong> Superantipoison (106.3 XP) and Prayer potions — sell to recoup costs</li>
    <li><strong>Use Zahur:</strong> 200 GP/herb to clean in Nardah — massive time savings</li>
  </ul>
</div>''',
}

# ===== New Meta Descriptions =====
META_DESCRIPTIONS = {
    "osrs-1-99-crafting-guide-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Crafting guide comparing glassblowing (120K XP/hr), battlestaves (100K-180K XP/hr), dragonhide (350K XP/hr), and jewelry crafting. Ironman-friendly giant seaweed methods included."',
    "osrs-1-99-hitpoints-training-guide-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Hitpoints guide — passive training through combat. Best methods include chinchompas (200K HP XP/hr), NMZ AFK (25K HP XP/hr), and Slayer for optimal efficiency."',
    "osrs-1-99-hunter-guide-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Hunter guide with all training methods. Black chinchompas (600K XP/hr), Herbiboar profit (500K GP/hr), bird house runs (passive), and more."',
    "osrs-1-99-magic-training-cheap-guide-2026.html": 'content="Updated for July 2026. Cheap OSRS Magic training from 1-99. Splashing for 10-15M GP total, profitable enchanting, Lunar spells (50K-65K XP/hr), and budget alternatives to High Alch."',
    "osrs-1-99-thieving-guide-ironman.html": 'content="Updated for July 2026. Complete OSRS Ironman 1-99 Thieving guide. Pyramid Plunder (280K XP/hr), Ardougne Knights (250K XP/hr), Master Farmers for 200+ ranarr seeds, and 10-15M GP profit."',
    "osrs-agility-training-guide-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Agility guide. Hallowed Sepulchre (105K XP/hr), rooftop courses, Marks of Grace farming (15-20M GP to 99), graceful outfit guide, and Brimhaven Arena."',
    "osrs-blast-furnace-smithing-guide-2026.html": 'content="Updated for July 2026. Complete OSRS Blast Furnace Smithing guide. Gold bars (170K XP/hr), profitable bar smelting, half coal cost, goldsmith gauntlets, coal bag strategy, and Ironman methods."',
    "osrs-cheapest-99-runecrafting-2026.html": 'content="Updated for July 2026. Cheapest OSRS Runecrafting 1-99 guide. GOTR (0 GP, 70K XP/hr), lava runes (8-9M GP to 99), ZMI (20M GP to 99). Colossal Pouch, Magic Imbue, and full cost breakdowns."',
    "osrs-construction-1-99-guide-2026.html": 'content="Updated for July 2026. Complete OSRS Construction 1-99 guide. Mahogany Tables (950K XP/hr, 155M GP), Oak Larders (450K XP/hr, 30M GP), Oak Dungeon Doors (300K XP/hr, 15M GP). POH layout guide."',
    "osrs-1-99-hitpoints-guide-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Hitpoints guide. Passive training through combat — chinchompas (200K HP XP/hr), NMZ AFK (25K HP XP/hr), Slayer efficiency. Ironman strategies included."',
    "osrs-1-99-prayer-guide-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Prayer guide. Gilded Altar (300K XP/hr, safe), Chaos Altar (6 GP/XP — saves 77M GP), Ectofuntus (4x XP), ensouled heads. Full cost breakdowns."',
    "osrs-1-99-prayer-guide-all-methods-2026.html": 'content="Updated for July 2026. Complete OSRS 1-99 Prayer guide — all methods. Gilded Altar (300K XP/hr), Chaos Altar (6 GP/XP budget), Ectofuntus (4x XP, Ironman), ensouled heads. Summer Sweep-Up 2026 updates."',
    "osrs-ironman-1-99-smithing-guide.html": 'content="Updated for July 2026. Complete OSRS Ironman 1-99 Smithing guide. Blast Furnace gold bars (300K XP/hr), Knight Sword quest skip, Arzinian Mine gold ore, iron bar training, and anvil methods."',
    "osrs-low-cost-1-99-herblore-guide.html": 'content="Updated for July 2026. Complete OSRS low-cost Herblore guide 1-99. Ranging potions (3-5 GP/XP), cheapest path ~50M GP total, superantipoison, prayer potions, Ironman herb sourcing guide."',
}

SUPPORT_CARD = '''<div class="support-card" style="margin:32px 0 0 0">
    <div class="support-inner">
        <span class="support-icon">🔓</span>
        <div class="support-text">
            <h3>Every guide is free — this one stays free either way.</h3>
            <p>No paywalls, no subscriptions. But the <strong>Early Access Guide Pack</strong> gives you more:</p>
            <p style="margin:6px 0 0 0;line-height:1.7">
                📚 <strong>10 Beginner Guides</strong> — zero to mid-game in one pack<br>
                ⭐ <strong>5 Premium Picks</strong> — our most popular expert deep-dives<br>
                ⏰ <strong>3-Day Early Access</strong> — read new guides before everyone else<br>
                🔄 <strong>3 New Guides Every Month</strong> — and each one fuels us to write faster
            </p>
            <p style="font-size:14px;margin:12px 0 0 0;opacity:0.85">✅ Your purchase includes instant access to everything above</p>
            <div class="support-amounts">
                <a href="https://www.paypal.com/paypalme/osrsguru/1.9" target="_blank" rel="noopener" class="support-amount-btn recommended">$1.90 — Get the Early Access Guide Pack 👑</a>
            </div>
            <p style="font-size:14px;margin:6px 0 0 0;opacity:0.85">Every guide stays free for everyone, always — no strings attached. 🤝</p>
        </div>
    </div>
</div>'''

FOOTER = '''<footer>
    <div class="container">
        <p>&copy; 2026 OSRSGuru.com — Not affiliated with Jagex Ltd.</p>
    </div>
</footer>'''

def process_file(filename):
    filepath = os.path.join(GUIDES_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []

    # 1. Meta Description - update to start with "Updated for July 2026."
    if filename in META_DESCRIPTIONS:
        new_meta = META_DESCRIPTIONS[filename]
        # Replace existing meta description
        pattern = r'<meta name="description" content="[^"]*"'
        if re.search(pattern, html):
            html = re.sub(pattern, f'<meta name="description" {new_meta}', html)
            changes.append("Meta updated")

    # 2. Remove dark inline styles
    html = html.replace('color:#e8d5b7', 'color:#1a1a1a')
    html = re.sub(r'background:#3b2615(?![^}]*?color)', 'background:#fff', html)
    html = re.sub(r'border-left:4px\s*solid\s*#d4af37', 'border-left:0', html)

    # 3. 30-Second Quick Summary - insert at top of content area, before TOC
    if filename in QUICK_SUMMARIES:
        qs = QUICK_SUMMARIES[filename]

        # Check if quick-summary already exists
        has_qs = 'quick-summary' in html and ('Quick Summary' in html or '30-Second' in html or 'Quick Summary' in html)

        if has_qs:
            # Replace existing inline style one
            html = re.sub(
                r'<div class="quick-summary"[^>]*>.*?</div>\s*',
                qs + '\n',
                html,
                flags=re.DOTALL
            )
            changes.append("Quick summary replaced")
        else:
            # Need to insert one - find a good location
            # Strategy: Insert after guide-header/guide-hero area, before TOC
            # Pattern 1: Magic/ironman/smithing/herblore use guide-header template
            m = re.search(r'(</div>\s*<!-- Section 1:|<section[^>]*id="overview"[^>]*>|<p class="guide-intro">.*?</p>|<span class="tag[^>]*>.*?</span>\s*</div>)', html)
            if not m:
                # Try after hero section subtitle
                m = re.search(r'(<p class="subtitle">.*?</p>|<p class="hero-subtitle".*?</p>|<div class="article-meta".*?</div>\s*</div>\s*</section>)', html)
            if m:
                pos = m.end()
                # Check we're before TOC
                toc_pos = html.find('class="toc"')
                if toc_pos > 0 and pos < toc_pos:
                    html = html[:pos] + '\n' + qs + '\n' + html[pos:]
                    changes.append("Quick summary inserted")
                else:
                    # Insert before TOC
                    html = html.replace('<div class="toc">', qs + '\n<div class="toc">', 1)
                    changes.append("Quick summary inserted before TOC")
            else:
                # Fallback: insert after <div class="container">
                html = html.replace('<div class="container">', '<div class="container">\n' + qs, 1)
                changes.append("Quick summary inserted (fallback)")

    # 4. Ensure TOC exists with proper class
    has_toc = re.search(r'class="[^"]*\btoc\b[^"]*"', html)
    if not has_toc:
        # Try to find table-of-contents and rename
        html = html.replace('class="table-of-contents"', 'class="toc"')
        html = html.replace('class="toc-list"', 'class="toc"')
        has_toc = re.search(r'class="[^"]*\btoc\b[^"]*"', html)
    if has_toc:
        changes.append("TOC verified")
    else:
        # Generate TOC from h2 tags
        h2s = re.findall(r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>', html)
        if h2s:
            toc_html = '<div class="toc">\n  <h3>Table of Contents</h3>\n  <ol>\n'
            for i, (h2_id, h2_text) in enumerate(h2s, 1):
                clean_text = re.sub(r'<[^>]+>', '', h2_text)
                toc_html += f'    <li><a href="#{h2_id}">{i}. {clean_text}</a></li>\n'
            toc_html += '  </ol>\n</div>'
            # Insert after quick-summary
            qs_match = re.search(r'</div>\s*(<!-- .*?-->\s*)?<div class="toc"', html)
            if qs_match:
                html = html[:qs_match.start()] + toc_html + '\n' + html[qs_match.start():]
            else:
                # Insert before first h2
                html = html.replace('<h2', toc_html + '\n<h2', 1)
            changes.append("TOC generated from h2s")

    # 5. Add h2 ids if missing (for TOC links)
    h2s_no_id = re.findall(r'<h2>(?!.*?id=)(.*?)</h2>', html)
    for h2_text in h2s_no_id:
        clean = re.sub(r'<[^>]+>', '', h2_text)
        h2_id = re.sub(r'[^a-zA-Z0-9]+', '-', clean.lower()).strip('-')[:50]
        html = html.replace(f'<h2>{h2_text}</h2>', f'<h2 id="{h2_id}">{h2_text}</h2>', 1)

    # 6. Replace or add bottom CSS block
    # Remove existing <style> blocks near </body>
    pattern_style_block = r'<style>(.*?)</style>\s*'
    html = re.sub(pattern_style_block, '', html, flags=re.DOTALL)

    # Inject standard CSS before </body>
    html = html.replace('</body>', STANDARD_CSS_BLOCK + '\n</body>')
    changes.append("CSS block replaced/added")

    # 7. Support Card - check if exists and add standard green one if missing
    has_support_card = 'support-card' in html
    if has_support_card:
        # Check if it's the old format (needs replacement)
        if 'Green' not in html and 'support-inner' not in html:
            # Already has correct format
            pass
        changes.append("Support card present")
    else:
        # Insert before footer or </main>
        if '</main>' in html:
            html = html.replace('</main>', SUPPORT_CARD + '\n</main>')
            changes.append("Support card added")
        elif '<footer' in html:
            html = html.replace('<footer', SUPPORT_CARD + '\n<footer', 1)
            changes.append("Support card added")
        else:
            html = html.replace('</body>', SUPPORT_CARD + '\n</body>')
            changes.append("Support card added (before body close)")

    # 8. Footer - check if exists
    has_footer = '<footer' in html
    if not has_footer:
        html = html.replace('</body>', FOOTER + '\n</body>')
        changes.append("Footer added")
    else:
        changes.append("Footer present")

    # 9. Verify canonical
    if filename in html or filename.replace('.html', '') in html:
        changes.append("Canonical OK")
    else:
        # Try to add/update canonical
        canonical_match = re.search(r'<link rel="canonical"[^>]*>', html)
        if canonical_match:
            old_canonical = canonical_match.group(0)
            new_canonical = f'<link rel="canonical" href="https://osrsguru.com/guides/{filename}">'
            html = html.replace(old_canonical, new_canonical)
            changes.append("Canonical corrected")

    # 10. Verify GA4 and AdSense
    ga4_ok = 'G-S1BGC91MYV' in html
    adsense_ok = 'ca-pub-8532760886171435' in html
    if ga4_ok:
        changes.append("GA4 OK")
    if adsense_ok:
        changes.append("AdSense OK")

    # Write if changed
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {filename} — {' | '.join(changes)}")
        return True
    else:
        print(f"  ⏭️  {filename} — No changes needed")
        return False

def main():
    success = 0
    for fname in FILES:
        print(f"Processing: {fname}")
        try:
            if process_file(fname):
                success += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}")

    print(f"\n=== Team 2 Group A complete: {success}/{len(FILES)} ===")

if __name__ == '__main__':
    main()
