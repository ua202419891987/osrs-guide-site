#!/usr/bin/env python3
"""
Read a file, apply standardizations, output to stdout.
Usage: python _process_single.py <filename>
"""

import re
import sys
import os

BASE = "C:/Users/Lenovo/osrs-guide-site/guides"

QUICK_SUMMARIES = {
    "osrs-affordable-leveling-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Reach 99 in every skill on a budget with profit-making training methods:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Zero GP needed:</strong> Slayer, Mining, Farming, Runecrafting fund themselves at 200K–500K GP/hr</li>
    <li><strong>Cheapest 99s:</strong> Agility, Thieving, Firemaking cost 0 GP and take 10–35 hours each</li>
    <li><strong>Total budget:</strong> ~150M–300M GP for all 23 skills vs 600M–900M GP optimal</li>
    <li><strong>Best money-makers:</strong> Amethyst mining (92+) at 400K–600K GP/hr, Farming runs at 1M–3M/run</li>
    <li><strong>Quest XP:</strong> Complete Waterfall, Tree Gnome Village, Fight Arena first — saves 15–25 hours</li>
  </ul>
</div>""",

    "osrs-bond-farming-free-membership-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Keep OSRS membership active forever without spending real money:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Bond cost:</strong> ~5.2M GP per 14 days = ~370K GP/day</li>
    <li><strong>F2P first bond:</strong> Ogress Warriors (40+ combat) at 220K GP/hr — ~24 hours to 5.2M GP</li>
    <li><strong>Early member:</strong> Wintertodt at 200K–400K GP/hr + Green Dragons at 400K–600K GP/hr</li>
    <li><strong>Sustained:</strong> Zulrah/Vorkath at 1.5M–2.5M GP/hr — bond in 2–3 hours</li>
    <li><strong>Passive income:</strong> Bird house runs (100K–200K GP/day) + herb runs (200K–400K GP/day)</li>
  </ul>
</div>""",

    "osrs-bond-farming-strategy-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Sustained bond farming strategy for 12.6M GP bonds in 2026:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Daily target:</strong> ~900K GP/day (12.6M GP / 14 days)</li>
    <li><strong>Passive setup:</strong> Bird houses + herb runs + Miscellania = 300K–550K GP/day in 20 min</li>
    <li><strong>Active income:</strong> Mort Myre Fungi at 300K–400K GP/hr or tanning dragonhide at 400K–600K GP/hr</li>
    <li><strong>Mid-game bossing:</strong> Vorkath/Zulrah at 2M–3M GP/hr = 18–20 min/day for bond</li>
    <li><strong>Endgame:</strong> Single ToA purple drop can cover 4–12 months of membership</li>
  </ul>
</div>""",

    "osrs-complete-skill-training-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Complete 1–99 training reference for all 23 OSRS skills in 2026:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest 99s:</strong> Cooking (8h, ~72M GP), Fletching (27h, ~105M GP), Prayer (10–20h, 60–120M GP)</li>
    <li><strong>Free 99s:</strong> Agility (30–50h), Thieving (40–60h, profit), Runecrafting (80–120h, profit)</li>
    <li><strong>Combat:</strong> Train through Slayer — earns 50K–500K+ GP/hr while leveling all combat stats</li>
    <li><strong>Most expensive:</strong> Construction (70–130M GP), Herblore (80–150M GP), Crafting (60–130M GP)</li>
    <li><strong>Best AFK:</strong> Motherlode Mine (Mining), Tempoross (Fishing), Ardougne Knights (Thieving)</li>
  </ul>
</div>""",

    "osrs-leveling-milestones-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Every significant level unlock across all 23 OSRS skills:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>#1 milestone:</strong> 43 Prayer (Protect from Melee) — costs ~850K GP, opens all PvM</li>
    <li><strong>70 Attack:</strong> Abyssal Whip — the iconic melee weapon (~1.5M GP)</li>
    <li><strong>55 Magic:</strong> High Alchemy — the most important money-making spell</li>
    <li><strong>70 Agility:</strong> Saradomin GWD shortcut — essential for God Wars Dungeon</li>
    <li><strong>72 Slayer:</strong> Gargoyles — first consistent 500K+ GP/hr money-maker</li>
  </ul>
</div>""",

    "osrs-sailing-1-99-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Master OSRS Sailing from 1 to 99 with verified 2026 methods:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest route:</strong> Barracuda Trials — 70–80 hours to 99, up to 180K XP/hr at Gwenith Glide</li>
    <li><strong>AFK route:</strong> Shipwreck Salvaging — ~160 hours, earns 20M+ GP profit</li>
    <li><strong>Start:</strong> Complete Pandemonium quest (15 min, no requirements)</li>
    <li><strong>Cost:</strong> Only ~350K–500K GP for boat upgrades</li>
    <li><strong>Post-99:</strong> Doom of Mokhaiotl at 15M–23M GP/hr — highest GP/hr in the game</li>
  </ul>
</div>""",

    "osrs-sailing-afk-training-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">The most relaxed way to 99 Sailing — Shipwreck Salvaging mastery:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>AFK windows:</strong> 3–4 minutes per wreck — perfect for work, Netflix, or studying</li>
    <li><strong>Time to 99:</strong> ~160 hours pure AFK, or 100–120 hours hybrid with Barracuda Trials</li>
    <li><strong>Profit:</strong> 20M–50M+ GP from salvaged materials on the way to 99</li>
    <li><strong>Max XP:</strong> Dragon Hook (87+) at ~90K XP/hr and ~400K GP/hr</li>
    <li><strong>Crew:</strong> 3 Salvagers + 2 Lookouts on Sloop for optimal loot and wreck spawns</li>
  </ul>
</div>""",

    "osrs-sailing-training-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Complete Sailing training guide with five training methods in 2026:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest XP:</strong> Barracuda Trials at 200K+ XP/hr (Gwenith Glide, 72+)</li>
    <li><strong>Best AFK:</strong> Shipwreck Salvaging — 30K–100K XP/hr, 20M+ GP profit to 99</li>
    <li><strong>Budget cost:</strong> ~350K–500K GP for basic gear; premium upgrades up to 20–60M GP</li>
    <li><strong>One-time bonus:</strong> Sea Charting gives 691K free XP + permanent 2.5% XP boost</li>
    <li><strong>Total time:</strong> 70–80 hours (active) or 160–170 hours (AFK)</li>
  </ul>
</div>""",

    "osrs-skill-training-after-sweep-up-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Post-Summer Sweep-Up 2026 training changes — what got better and what got worse:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Biggest buff:</strong> Hunter — Mangrove Sifaka (43–53) at 32K XP/hr, Sunlight Moth (80+) at 95K XP/hr</li>
    <li><strong>Agility improved:</strong> New Oo'glog course (50–70) at 48K XP/hr, TzHaar (85+) at 72K XP/hr</li>
    <li><strong>Thieving:</strong> Pickpocket Dwarves (65+) at 62K XP/hr + profit, Elves (80+) at 90K XP/hr</li>
    <li><strong>Mining buff:</strong> Gem Rocks (45+) at 30K XP/hr + 150K–300K GP/hr profit</li>
    <li><strong>Smithing nerf:</strong> Blast Furnace reduced 3–6%, but early smithing (1–30) got 25–40% buff</li>
  </ul>
</div>""",

    "osrs-skill-training-endgame-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Training all 23 skills from level 70 to 99 — the definitive endgame guide:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Most expensive:</strong> Smithing (~230M GP), Herblore (~180M GP), Construction (~120M GP)</li>
    <li><strong>Free/profitable:</strong> Runecrafting (+40M GP), Hunter (+100M GP), Fishing (+50M GP)</li>
    <li><strong>Fastest methods:</strong> Cooking Anglerfish at 1.3M XP/hr, Smithing Blast Furnace at 300K XP/hr</li>
    <li><strong>Best order:</strong> Slayer to 93+ → Runecrafting 90+ → Hunter 99 → Farming 99</li>
    <li><strong>Total time:</strong> ~1,500 hours from mid-game to Max Cape, ~400M–500M GP total cost</li>
  </ul>
</div>""",

    "osrs-skill-training-max-account-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">The complete roadmap to 2277 total level and the Max Cape:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Total time:</strong> 1,200–1,500 hours efficient play, ~400M–500M GP total budget</li>
    <li><strong>5 phases:</strong> Combat First → Fast Skiller 99s → Slow Gathering → Expensive 99s → Clean-Up</li>
    <li><strong>Key synergy:</strong> Slayer trains 6 combat skills simultaneously while earning 200M–500M GP</li>
    <li><strong>Runecrafting first:</strong> 90+ RC (Soul runes) = 170K XP/hr + 40M GP profit — fund the rest</li>
    <li><strong>Big 4 expenses:</strong> Smithing (230M), Herblore (180M), Construction (120M), Fletching (105M)</li>
  </ul>
</div>""",

    "osrs-skill-training-mid-game-guide-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Optimal training methods for all 23 skills at levels 50–70:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Combat 50–70:</strong> Switch from Sand Crabs to Slayer — 40K–60K XP/hr plus 100K–400K GP/hr profit</li>
    <li><strong>Prayer 43–70:</strong> Dragon bones at Gilded Altar — ~300 XP/bone, ~18M GP total for 70</li>
    <li><strong>Hunter 50–70:</strong> Red Chinchompas at 60K–80K XP/hr and 250K–350K GP/hr profit</li>
    <li><strong>Farming:</strong> Herb runs (Ranarr/Snapdragon) at 200K–500K GP per 5-minute run</li>
    <li><strong>Construction:</strong> Portal Nexus (58) and Gilded Altar (47) — the two must-build POH upgrades</li>
  </ul>
</div>""",

    "osrs-skill-training-mid-game-optimization-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Maximize XP and GP per hour during your mid-game phase:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Efficiency formula:</strong> (XP/hr x GP/XP) + GP profit — profitable methods often beat fastest XP</li>
    <li><strong>Top optimizations:</strong> Portal Nexus (saves 5–10s per bank trip), Graceful outfit (-30% run drain)</li>
    <li><strong>Beginner tick manipulation:</strong> 3-tick mining (55K XP/hr vs 42K) and 1-tick banking setups</li>
    <li><strong>Inventory:</strong> Mushroom Potatoes (20 HP, ~400 GP) — best mid-game food value</li>
    <li><strong>Route optimization:</strong> Reduce bank distance from 30s to 10s = 66% more actions per hour</li>
  </ul>
</div>""",

    "osrs-training-guide-complete-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">The complete OSRS training roadmap from F2P to endgame:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>F2P first week:</strong> Combat 40/40/40 (10–15h) to 43 Prayer (3–5h) to 30 Cooking/Fishing (2–3h)</li>
    <li><strong>Members first week:</strong> 60+ combat at Sand Crabs to 43 Prayer to Start Slayer to High-XP quests</li>
    <li><strong>Key quests:</strong> Waterfall (13,750 Atk/Str), Fight Arena (12,075 Atk) — save 5–10h each</li>
    <li><strong>GP while training:</strong> Wintertodt (200K–400K GP/hr), Red Chins (200K–300K GP/hr), Herb runs</li>
    <li><strong>43 Prayer priority:</strong> Costs ~850K GP at Gilded Altar — single best investment in the game</li>
  </ul>
</div>""",
}

STANDARD_FOOTER = """<footer>
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h4>OSRS Guru</h4>
                <p>Free OSRS guides for beginners and pros alike. No MTX, no paywalls just good content.</p>
                <p class="footer-disclaimer">OSRS Guru is a fan-made website. We are not affiliated with Jagex Ltd. Old School RuneScape and RuneScape are trademarks of Jagex Ltd.</p>
            </div>
            <div class="footer-section">
                <h4>Guides</h4>
                <ul>
                    <li><a href="../skill-training.html">Skill Training</a></li>
                    <li><a href="../money-making.html">Money Making</a></li>
                    <li><a href="../boss-guides.html">Boss Guides</a></li>
                    <li><a href="../quest-guides.html">Quest Guides</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Legal</h4>
                <ul>
                    <li><a href="../privacy-policy.html">Privacy Policy</a></li>
                    <li><a href="../terms-of-service.html">Terms of Service</a></li>
                    <li><a href="../affiliate-disclosure.html">Affiliate Disclosure</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 OSRS Guru. All rights reserved. | Fan Content Policy: <a href="https://www.jagex.com/legal/fan-content-policy" target="_blank">Jagex Fan Content</a> | Wiki content licensed under <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank">CC BY-SA 3.0</a></p>
        </div>
    </div>
</footer>"""

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
.guide-content .req-box,
.guide-content .quick-answer,
.guide-content .quick-jump { background:#fff !important; border:1px solid #e0d5c0 !important; }

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

STANDARD_SUPPORT_CARD = """<div class="support-card" style="margin:32px 0 0 0">
    <div class="support-inner">
        <span class="support-icon">🔓</span>
        <div class="support-text">
            <h3>Every guide is free this one stays free either way.</h3>
            <p>No paywalls no subscriptions. But the <strong>Early Access Guide Pack</strong> gives you more:</p>
            <p style="margin:6px 0 0 0;line-height:1.7">
                <strong>10 Beginner Guides</strong> zero to mid-game in one pack<br>
                <strong>5 Premium Picks</strong> our most popular expert deep-dives<br>
                <strong>3-Day Early Access</strong> read new guides before everyone else<br>
                <strong>3 New Guides Every Month</strong> and each one fuels us to write faster
            </p>
            <p style="font-size:14px;margin:12px 0 0 0;opacity:0.85">Your purchase includes instant access to everything above</p>
            <div class="support-amounts">
                <a href="https://www.paypal.com/paypalme/osrsguru/1.9" target="_blank" rel="noopener" class="support-amount-btn recommended">$1.90 Get the Early Access Guide Pack</a>
            </div>
            <p style="font-size:14px;margin:6px 0 0 0;opacity:0.85">Every guide stays free for everyone always no strings attached.</p>
        </div>
    </div>
</div>"""

def process_file(filename):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []
    
    # 1. Meta description
    meta_match = re.search(r'<meta name="description" content="([^"]*)"', content, re.IGNORECASE)
    if meta_match:
        desc = meta_match.group(1)
        if not desc.startswith("Updated for July 2026."):
            if "Updated for" in desc:
                desc = re.sub(r'^Updated[^.]*\.\s*', '', desc)
            desc = "Updated for July 2026. " + desc
            old = meta_match.group(0)
            new = f'<meta name="description" content="{desc}"'
            content = content.replace(old, new)
            changes.append("Meta")

    # 2. Quick Summary
    qs = QUICK_SUMMARIES[filename]
    if '30-Second Quick Summary' in content:
        content = re.sub(r'<div class="quick-summary"[^>]*>.*?</div>\s*\n', qs + '\n', content, count=1, flags=re.DOTALL)
        changes.append("QS")
    else:
        toc_match = re.search(r'<(div|nav) class="(toc|table-of-contents)">', content)
        if toc_match:
            before = content[:toc_match.start()]
            after = content[toc_match.start():]
            content = before + '\n' + qs + '\n' + after
            changes.append("QS+insert")

    # 3. TOC normalization
    content = content.replace('class="table-of-contents"', 'class="toc"')
    content = content.replace('class="toc toc"', 'class="toc"')
    changes.append("TOC")

    # 4. Remove dark inline styles
    content = content.replace('color:#e8d5b7', 'color:#1a1a1a')
    content = content.replace('color: #e8d5b7', 'color: #1a1a1a')
    content = re.sub(r'color:\s*#e8d5b7\s*!important', 'color:#1a1a1a !important', content)
    changes.append("DarkFix")

    # 5. Bottom CSS - replace
    content = re.sub(r'<style>.*?</style>\s*', '', content, count=0, flags=re.DOTALL)
    # Insert CSS before </body>
    content = content.replace('</body>', STANDARD_CSS + '\n</body>')
    changes.append("CSS")

    # 6. Support card
    if 'support-card' in content:
        changes.append("SupCard")
    else:
        content = content.replace('</main>', STANDARD_SUPPORT_CARD + '\n</main>')
        changes.append("SupCard+")

    # 7. Footer
    if '&copy; 2026 OSRS Guru' in content or '(c) 2026 OSRS Guru' in content:
        changes.append("Footer")
    else:
        content = content.replace('</body>', STANDARD_FOOTER + '\n</body>')
        changes.append("Footer+")

    # 8 - 10. Verify scripts
    if 'G-S1BGC91MYV' in content: changes.append("GA4")
    else: changes.append("GA4-MISS")
    if 'ca-pub-8532760886171435' in content: changes.append("AdSense")
    else: changes.append("AdSense-MISS")
    
    canon = re.search(r'<link rel="canonical" href="[^"]*' + re.escape(filename) + r'"', content)
    if canon: changes.append("Canon")
    
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdout.write(content)

if __name__ == "__main__":
    process_file(sys.argv[1])
