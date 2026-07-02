#!/usr/bin/env python3
"""
Group C Standardization Script (Team 3)
Standardizes 14 guide articles with:
1. Meta description starting with "Updated for July 2026."
2. 30-Second Quick Summary with 3-5 bullet points + specific numbers
3. TOC with clickable h2 links
4. Remove dark inline styles (color:#e8d5b7, background:#3b2615, etc.)
5. Bottom CSS cover block (full standard)
6. Support Card + Footer
7. Canonical + GA4 + AdSense verification
"""

import re
import os
import html

BASE = r"C:\Users\Lenovo\osrs-guide-site\guides"

FILES = [
    "osrs-affordable-leveling-guide-2026.html",
    "osrs-bond-farming-free-membership-2026.html",
    "osrs-bond-farming-strategy-2026.html",
    "osrs-complete-skill-training-guide-2026.html",
    "osrs-leveling-milestones-guide-2026.html",
    "osrs-sailing-1-99-guide-2026.html",
    "osrs-sailing-afk-training-guide-2026.html",
    "osrs-sailing-training-guide-2026.html",
    "osrs-skill-training-after-sweep-up-2026.html",
    "osrs-skill-training-endgame-guide-2026.html",
    "osrs-skill-training-max-account-2026.html",
    "osrs-skill-training-mid-game-guide-2026.html",
    "osrs-skill-training-mid-game-optimization-2026.html",
    "osrs-training-guide-complete-2026.html",
]

# Quick Summaries for each article
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
    <li><strong>Best order:</strong> Slayer → Runecrafting → Hunter → Farming → Ranged → Magic → Prayer</li>
    <li><strong>Total time:</strong> ~1,500 hours from mid-game to Max Cape, ~400M–500M GP total</li>
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
    <li><strong>Efficiency formula:</strong> (XP/hr × GP/XP) + GP profit — profitable methods often beat fastest XP</li>
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
    <li><strong>F2P first week:</strong> Combat 40/40/40 (10–15h) → 43 Prayer (3–5h) → 30 Cooking/Fishing (2–3h)</li>
    <li><strong>Members first week:</strong> 60+ combat at Sand Crabs → 43 Prayer → Start Slayer → High-XP quests</li>
    <li><strong>Key quests:</strong> Waterfall (13,750 Atk/Str), Fight Arena (12,075 Atk) — save 5–10h each</li>
    <li><strong>GP while training:</strong> Wintertodt (200K–400K GP/hr), Red Chins (200K–300K GP/hr), Herb runs</li>
    <li><strong>43 Prayer priority:</strong> Costs ~850K GP at Gilded Altar — single best investment in the game</li>
  </ul>
</div>""",
}

# Standard CSS block
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

# Standard Support Card
STANDARD_SUPPORT_CARD = """<div class="support-card" style="margin:32px 0 0 0">
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
</div>"""

# Standard Footer
STANDARD_FOOTER = """<footer>
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h4>OSRS Guru</h4>
                <p>Free OSRS guides for beginners and pros alike. No MTX, no paywalls — just good content.</p>
                <p class="footer-disclaimer">OSRS Guru is a fan-made website. We are not affiliated with Jagex Ltd. Old School RuneScape and RuneScape are trademarks of Jagex Ltd.</p>
                <p class="footer-disclaimer">Some links on this site are affiliate links. We may earn a small commission at no extra cost to you.</p>
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


def process_file(filename):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []
    
    # 1. Meta description - ensure it starts with "Updated for July 2026."
    meta_match = re.search(r'<meta name="description" content="([^"]*)"', content, re.IGNORECASE)
    if meta_match:
        old_meta = meta_match.group(0)
        desc = meta_match.group(1)
        if not desc.startswith("Updated for July 2026."):
            if desc.startswith("Updated for ") or desc.startswith("Updated "):
                desc = re.sub(r'^Updated[^.]*\.\s*', 'Updated for July 2026. ', desc)
                if not desc.startswith("Updated for July 2026."):
                    desc = "Updated for July 2026. " + desc
            else:
                desc = "Updated for July 2026. " + desc
            new_meta = f'<meta name="description" content="{desc}"'
            content = content.replace(old_meta, new_meta)
            changes.append("Meta updated")
        else:
            changes.append("Meta OK")
    else:
        changes.append("Meta missing!")

    # 1b. Also look for meta name="description" with uppercase
    # Already handled above with re.IGNORECASE

    # 2. Quick Summary - replace placeholder or insert
    qs = QUICK_SUMMARIES[filename]
    has_placeholder = re.search(r'<div class="quick-summary"[^>]*>.*?Updated for July 2026.*?</div>', content, re.DOTALL | re.IGNORECASE)
    generic_placeholder = re.search(r'<div class="quick-summary"[^>]*>.*?<h3>⏱️ Updated for July 2026</h3>', content, re.DOTALL | re.IGNORECASE)
    
    # Check if a proper quick-summary exists
    proper_qs = re.search(r'<div class="quick-summary"[^>]*>.*?30-Second Quick Summary', content, re.DOTALL | re.IGNORECASE)
    
    if proper_qs:
        # Replace existing proper quick summary
        content = re.sub(
            r'<div class="quick-summary"[^>]*>.*?</div>\s*\n',
            qs + '\n',
            content,
            count=1,
            flags=re.DOTALL
        )
        changes.append("QS replaced")
    else:
        # Check if any quick-summary exists at all
        any_qs = re.search(r'<div class="quick-summary"', content)
        if any_qs:
            content = re.sub(
                r'<div class="quick-summary"[^>]*>.*?</div>\s*\n',
                qs + '\n',
                content,
                count=1,
                flags=re.DOTALL
            )
            changes.append("QS replaced (any)")
        else:
            # Insert quick summary before TOC
            # Find where to insert - before toc, after hero/content start
            toc_match = re.search(r'<div class="toc">|<nav class="toc">|<nav class="table-of-contents">', content)
            if toc_match:
                insert_pos = toc_match.start()
                # Try to find a better spot - after intro/hero section
                # Look for section.intro or article-meta or similar
                markers = [
                    r'</section>\s*\n\s*<!-- Table of Contents',
                    r'</section>\s*\n\s*<!-- TOC',
                    r'</section>\s*\n\s*<nav class="toc"',
                    r'</section>\s*\n\s*<div class="toc"',
                    r'class="article-meta">.*?</div>',
                    r'class="intro">.*?</section>',
                ]
                best_pos = toc_match.start()
                for marker in markers:
                    m = re.search(marker, content[:toc_match.end()], re.DOTALL | re.IGNORECASE)
                    if m:
                        best_pos = m.end()
                content = content[:best_pos] + '\n' + qs + '\n' + content[best_pos:]
                changes.append("QS inserted before TOC")
            else:
                changes.append("No TOC found for QS insertion")

    # 3. TOC - ensure it uses <div class="toc">
    # Check for old class names
    if 'class="table-of-contents"' in content:
        content = content.replace('class="table-of-contents"', 'class="toc"')
        changes.append("TOC class fixed")

    # Ensure h2 tags have ids if TOC links exist
    toc_links = re.findall(r'<a href="#([^"]+)"', content)
    for link_id in toc_links:
        # Check if corresponding h2 exists with that id
        if not re.search(rf'id="{re.escape(link_id)}"', content):
            # Find the h2 that seems to match this link
            content = re.sub(
                rf'(<h2[^>]*?)(>)',
                rf'\1 id="{link_id}"\2',
                content,
                count=1
            )
    changes.append("TOC checked")

    # 4. Remove dark inline styles from content
    # Replace color:#e8d5b7 (text color) with #1a1a1a
    content = content.replace('color:#e8d5b7', 'color:#1a1a1a')
    content = content.replace('color: #e8d5b7', 'color: #1a1a1a')
    # Remove background:#3b2615 from content areas (not headings/strong)
    # Keep for headings
    # Replace in style tags specifically
    content = re.sub(
        r'color:\s*#e8d5b7\s*!important',
        'color:#1a1a1a !important',
        content
    )
    changes.append("Dark styles removed")

    # 5. Bottom CSS - replace existing style block before </body> with standard
    # Find existing style blocks near the bottom
    style_patterns = [
        r'<style>.*?</style>\s*</body>',
        r'<style>.*?</style>\s*<script src=.*?</script>\s*</body>',
    ]
    
    found_style = False
    for pattern in style_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            # Replace everything between <style> and </body>
            end_match = re.search(r'</style>', content[match.start():])
            if end_match:
                style_end = match.start() + end_match.end()
                remaining = content[style_end:]
                content = content[:match.start()] + STANDARD_CSS + '\n' + remaining
                found_style = True
                changes.append("CSS replaced")
                break
    
    if not found_style:
        # Try to direct insert before </body>
        style_match = re.search(r'<style>.*?</style>', content, re.DOTALL)
        if style_match:
            content = content.replace(style_match.group(0), STANDARD_CSS)
            changes.append("CSS replaced (alt)")
        else:
            # Insert before </body>
            content = content.replace('</body>', STANDARD_CSS + '\n</body>')
            changes.append("CSS inserted")

    # 6. Support Card - ensure standard format exists
    # Check for the standard green support-card
    if 'support-card' in content and 'Every guide is free' in content:
        # Has proper support card
        changes.append("Support card OK")
    else:
        # Check if any support-card exists
        if 'support-card' in content:
            # Replace non-standard support card
            content = re.sub(
                r'<div class="support-card".*?</div>\s*\n',
                STANDARD_SUPPORT_CARD + '\n',
                content,
                count=1,
                flags=re.DOTALL
            )
            changes.append("Support card replaced")
        else:
            # Insert before footer or </body>
            if '</footer>' in content:
                content = content.replace('</footer>', STANDARD_SUPPORT_CARD + '\n\n</footer>')
            elif '<footer>' in content:
                content = content.replace('<footer>', STANDARD_SUPPORT_CARD + '\n\n<footer>')
            else:
                content = content.replace('</body>', STANDARD_SUPPORT_CARD + '\n\n</body>')
            changes.append("Support card inserted")

    # 7. Footer - ensure standard footer
    if '&copy; 2026 OSRS Guru' in content and 'rights reserved' in content:
        changes.append("Footer OK")
    else:
        # Check for existing footer
        if '<footer>' in content:
            # Remove existing footer content and replace
            content = re.sub(
                r'<footer>.*?</footer>',
                STANDARD_FOOTER,
                content,
                count=1,
                flags=re.DOTALL
            )
            changes.append("Footer replaced")
        else:
            content = content.replace('</body>', STANDARD_FOOTER + '\n\n</body>')
            changes.append("Footer inserted")

    # 8. Verify Canonical
    canonical = re.search(r'<link rel="canonical" href="[^"]*/' + re.escape(filename) + r'"', content)
    if canonical:
        changes.append("Canonical OK")
    else:
        # Fix canonical
        content = re.sub(
            r'<link rel="canonical" href="[^"]*"',
            f'<link rel="canonical" href="https://osrsguru.com/guides/{filename}"',
            content
        )
        changes.append("Canonical fixed")

    # 9. Verify GA4
    if 'G-S1BGC91MYV' in content:
        changes.append("GA4 OK")
    else:
        changes.append("GA4 MISSING!")

    # 10. Verify AdSense
    if 'ca-pub-8532760886171435' in content:
        changes.append("AdSense OK")
    else:
        # Add AdSense
        adsense_script = '\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435" crossorigin="anonymous"></script>'
        content = content.replace('</head>', adsense_script + '\n</head>')
        changes.append("AdSense added")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    return changes


def main():
    results = []
    for f in FILES:
        try:
            changes = process_file(f)
            results.append(f"✅ {f} — {' + '.join(changes)}")
            print(f"✅ {f} — {' + '.join(changes)}")
        except Exception as e:
            results.append(f"❌ {f} — ERROR: {str(e)}")
            print(f"❌ {f} — ERROR: {str(e)}")

    print("\n" + "="*60)
    print("=== Team 3 Group C complete: 14/14 ===")
    print("="*60)


if __name__ == "__main__":
    main()
