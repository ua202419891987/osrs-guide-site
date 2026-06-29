#!/usr/bin/env python3
"""Batch update 24 Crimson Desert articles: Quick Summary + Progress Bar + Mobile"""
import re, os, glob

CD_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides\crimson-desert"

# Quick Summary content per article (keyed by filename)
QUICK_SUMMARIES = {
    "crimson-desert-weapon-enhancement-guide-2026.html": [
        "⚔️ Refining from +1 to +10 is 100% deterministic — no RNG, no gear destruction",
        "🔧 Find all 5 blacksmith NPCs across Pywel with unique services at each location",
        "💎 Abyss Gear socket system adds custom passives — best cores are Destruction, Spirit Siphon, Critical Rate",
        "🫙 Kuku Pot crafting unlocks unique weapons, elemental armor, and utility backpacks",
    ],
    "crimson-desert-enhancement-materials-guide-2026.html": [
        "⛏️ Iron Ore (Hernand cliffs) to Bloodstone (Rocca's Hill) — every material with farming locations",
        "📊 Full material table per refinement tier from +1 (cheap) to +10 (rare Aeserion Scales)",
        "💡 Save-scum ore nodes by reloading near mining spots — farm 200+ Iron Ore in 15 min",
        "🔄 Abyss Artifacts are shared between refining and skill tree — plan allocation carefully",
    ],
    "crimson-desert-abyss-sanctum-guide-2026.html": [
        "🏛️ Abyss Sanctum is the main endgame dungeon — unlock via witch questline after Chapter 10",
        "🗺️ 6 sanctum floors with unique puzzles, combat challenges, and environmental hazards",
        "👹 Antumbra boss fight has 4 phases — dodge dark projectiles, destroy orbs, expose the core",
        "🎁 Rewards include boss weapons with unique extractable Abyss Cores and endgame gear",
    ],
    "crimson-desert-sanctum-rewards-guide-2026.html": [
        "💰 Full loot table for all 6 Abyss Sanctum floors — weapons, cores, artifacts, and materials",
        "🗡️ Boss weapon extraction turns signature abilities into equippable Abyss Cores",
        "⏫ Gear progression: Sanctum weapons → mid-game gear → craftable endgame sets",
        "🔄 Repeatable farming: each sanctum run resets, allowing unlimited loot collection",
    ],
    "crimson-desert-mid-game-gear-guide-2026.html": [
        "🔧 Best mid-game weapons: Crimson Set (2H axe), Reforged weapons from blacksmiths",
        "🛡️ Armor priority: Howling Hill gear set → Demeniss crafted → Abyss-socketed endgame",
        "💰 Silver management: prioritize socket slots (105 silver max) over cosmetic upgrades",
        "📈 Stat priorities: ATK > Crit Rate > Spirit Siphon > Stamina Siphon for general PvE",
    ],
    "crimson-desert-mid-gear-locations-guide-2026.html": [
        "🗺️ Every mid-game weapon and armor piece with exact NPC/vendor/drop location",
        "🔨 Blacksmith Turnali (Hernand) gives first upgradeable gear via quest rewards",
        "🏪 Witch vendors in each region sell Abyss Cores — check every crystal icon on your map",
        "🎯 Boss drops: unique weapons from world bosses like Crowcaller and Hornbreaker",
    ],
    "crimson-desert-post-game-guide-2026.html": [
        "🏆 Abyss Sanctum grinding, world boss rotations, and hidden boss encounters",
        "🌟 Achievement hunting: 50+ trophies with missable warnings and recommended order",
        "🔄 New Game+ carries over gear, skills, and Kuku Pot — harder enemies, better rewards",
        "🔍 Every region has post-game secrets: sealed artifacts, treasure maps, and NPC quests",
    ],
    "crimson-desert-post-game-secrets-guide-2026.html": [
        "🔍 Hidden bosses not marked on the map — special spawn conditions and unique loot",
        "📜 Missable NPC quests that disappear after certain story chapters",
        "🥚 Easter eggs: developer references, hidden cutscenes, and tribute locations",
        "💎 Secret areas: invisible platforms, breakable walls, and underwater caves with rare loot",
    ],
    "crimson-desert-kliff-build-guide-2026.html": [
        "🗡️ Kliff is the Blader class — high mobility, Spin Slash burst damage, and aerial combos",
        "⭐ Best skills: Spin Slash (max first) → Dash Attack → Aerial Strike → Whirlwind",
        "💎 Abyss Cores: Destruction + Critical Rate + Spirit Siphon for optimal DPS",
        "🔧 Weapon: Crimson Greatsword (mid-game) → Boss weapons (endgame) for best results",
    ],
    "crimson-desert-kliff-combos-guide-2026.html": [
        "💥 Core combo: Spin Slash cancel → Dash Attack → Aerial Strike → Whirlwind finisher",
        "⚡ Momentum stacking: maintain max stacks by chaining light attacks between skills",
        "👹 Boss rotation: parry → Spin Slash ×3 → Dodge → Aerial combo → retreat",
        "🎯 Frame-perfect tips: animation cancel with dodge, wall-bounce setups for extra damage",
    ],
    "crimson-desert-oongka-build-guide-2026.html": [
        "🪓 Oongka is the Berserker — dual-wield axes, Rage mechanic, and devastating AoE attacks",
        "⚡ Build Rage with light attacks, spend on heavy attacks — maintain 70%+ Rage for max DPS",
        "💎 Abyss Cores: Destruction + Momentum + Attack Speed for the best berserker setup",
        "🔧 Best weapons: Twin Axes (early) → Blood Axes (mid) → Legendary boss weapons (end)",
    ],
    "crimson-desert-oongka-dual-wield-guide-2026.html": [
        "🗡️ Dual-wield pairing: two one-handed axes for speed, or axe + mace for balance",
        "🔥 Rage System: 0-100 bar — fill with light attacks (fast), spend with heavy attacks (big damage)",
        "⚡ Rage Mode at 100%: all attacks enhanced, special moves unlocked, massive AoE potential",
        "💡 Best synergy: Rage Mode → Whirlwind → Ground Slam → repeat for area clear",
    ],
    "crimson-desert-damiane-build-guide-2026.html": [
        "🛡️ Damiane is the Sentinel — sword + shield tank with party support and crowd control",
        "⭐ Best skills: Shield Bash → Guard Break → Rally Cry → Iron Wall for balanced tank/support",
        "💎 Abyss Cores: Life Transference + Stamina Siphon + Spirit Siphon for survival",
        "🔧 Gear: Defender Set (early) → Guardian Set (mid) → Abyss-enhanced (endgame)",
    ],
    "crimson-desert-damiane-shield-guide-2026.html": [
        "🔰 Perfect parry timing: block 0.3s before hit for full parry — stuns enemies, opens counter",
        "🛡️ Shield bash combo: Parry → Shield Bash → Heavy Strike → Aerial Slam for big damage",
        "💪 Aggro management: Rally Cry draws nearby enemies, Iron Wall reduces incoming damage by 40%",
        "🎯 Survival setup: Life Transference core + Stamina Siphon + defensive food buffs = near-immortal",
    ],
    "crimson-desert-conversion-mechanics-guide-2026.html": [
        "🔄 Conversion Rate determines how much Kiln rewards you get from camp provisions",
        "📊 Higher conversion = more materials per provision — affects crafting, cooking, and upgrades",
        "🏕️ Boost conversion by upgrading camp facilities, assigning NPCs, and using specific recipes",
        "💡 Max efficiency: prioritize Kiln upgrades → assign skill-appropriate NPCs → craft in bulk",
    ],
    "crimson-desert-conversion-farming-guide-2026.html": [
        "🌾 Best camp setup: max-tier Kiln + high-skill NPCs = 40-60% conversion bonus",
        "📋 Kiln recipes ranked by efficiency: Leatherworking > Smelting > Cooking > Alchemy",
        "⏰ Daily routine: collect provisions → queue Kiln crafts → collect output → repeat",
        "💰 Profit calculation: convert low-tier materials into high-tier — ores→ingots, hides→leather",
    ],
    "crimson-desert-achievements-guide-2026.html": [
        "🏅 50+ achievements in Crimson Desert — combat, exploration, crafting, and story categories",
        "⚠️ Missable achievements: 8 tied to specific chapter choices — save before key decisions",
        "📋 Recommended order: Story first → Combat → Exploration → Crafting → Completionist",
        "🔧 Tools: in-game tracker shows progress per achievement category — check regularly",
    ],
    "crimson-desert-achievement-speedrun-guide-2026.html": [
        "⚡ Fastest route: main story → combat achievements → exploration → cleanup in post-game",
        "🎯 Missable checks: 8 achievements require specific choices — create save files at chapter 5, 8, 10",
        "⏱️ Time saves: skip optional dialogues, fast-travel between regions, farm combat achievements in arena",
        "🏆 Completion target: 40-50 hours for all achievements using optimized route",
    ],
    "crimson-desert-abyss-core-guide-2026.html": [
        "💎 Abyss Cores add passive bonuses via socket slots — up to 5 sockets on two-handed weapons",
        "📊 8 core types ranked: Destruction > Critical Rate > Spirit Siphon > Momentum > others",
        "🔄 Synthesis: combine 2 same-rank cores for 1 higher-rank — blueprint required",
        "💡 Extraction is free — swap loadouts between bossing (Malicebane) and farming (Siphon) freely",
    ],
    "crimson-desert-core-farming-guide-2026.html": [
        "⛏️ Best core farming: Sealed Artifact challenges give Abyss Cells + cores simultaneously",
        "🗺️ Core drop locations: world bosses (rare), elite enemies (common), Sanctum floors (guaranteed)",
        "📊 Drop rates: common cores from regular enemies (~5%), rare cores from bosses (~20%)",
        "🔄 Efficient route: Sanctum run → world boss rotation → artifact challenges → restart",
    ],
    "crimson-desert-card-game-guide-2026.html": [
        "🃏 Card game is a collectible card mini-game with NPC opponents across Pywel",
        "📖 Rules: each card has ATK/HP/cost — reduce opponent HP to 0 to win, earn rewards",
        "🧠 Deck strategy: balance low-cost (early pressure) and high-cost (finishers) cards",
        "🎁 Rewards include rare materials, Abyss Cells, and unique cosmetic items",
    ],
    "crimson-desert-card-collection-guide-2026.html": [
        "📚 All card locations: each NPC opponent requires specific deck to challenge and unlock",
        "🗺️ Card NPCs: 14+ opponents across Hernand, Demeniss, Pailune, Delesyia, and endgame zones",
        "⚠️ Missable: 3 card NPCs disappear after main story — collect before Chapter 10",
        "🏆 Completion: post-game cleanup mode lets you find remaining opponents via map markers",
    ],
    "crimson-desert-kuku-guide-2026.html": [
        "🫙 Kuku Pot is a Dwarven crafting station unlocked in Chapter 4 (Mysterious Pot quest)",
        "🔧 Craft categories: elemental spears, utility backpacks, elemental armor, special boots, laser helmet",
        "⚙️ Upgrade to Enhanced Kuku Pot (1 Abyss Cell) before endgame for advanced recipes",
        "💡 Craft priority: Fire Spear (permanent) → Watcher Pack → Elemental Armor → Rocket Pack",
    ],
    "crimson-desert-kuku-evolution-guide-2026.html": [
        "🔄 Optimal upgrade order: Kuku Spear > Kuku Backpack > Elemental Armor > Kuku Boots > Helmet",
        "📊 Material planning: each branch requires Abyss Cells + specific resources + blueprints",
        "💎 Best value: elemental spears (infinite durability) and Rocket Pack (flight utility)",
        "⚠️ Warning: upgraded items can't complete base-item challenges — finish challenges first",
    ],
}

PROGRESS_BAR_HTML = '''    <div class="cd-reading-progress" id="cdReadingProgress"><div class="cd-progress-fill" id="cdProgressFill"></div></div>'''

PROGRESS_BAR_CSS = '''
        /* Reading Progress Bar */
        .cd-reading-progress{position:fixed;top:0;left:0;width:100%;height:4px;background:rgba(122,100,184,0.12);z-index:99999;pointer-events:none;box-shadow:0 1px 3px rgba(0,0,0,0.06)}
        .cd-reading-progress .cd-progress-fill{height:100%;width:0%;background:linear-gradient(90deg,#7a64b8,#b8a4e8,#e0d8f0);transition:width .15s ease-out;border-radius:0 2px 2px 0}
        /* Mobile hero improvements */
        @media(max-width:768px){
            .guide-hero h1{font-size:1.6rem !important;line-height:1.3}
            .guide-hero .subtitle{font-size:1rem !important}
            .guide-hero .breadcrumb{font-size:.8rem !important}
            .toc{padding:1rem !important}
            .toc ol li{font-size:.9rem !important}
            .nav-links{overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}
        }'''

PROGRESS_BAR_JS = '''    <script>
    (function(){var p=document.getElementById('cdProgressFill');if(!p)return;var u=function(){var e=document.documentElement,t=e.scrollTop,n=e.scrollHeight-e.clientHeight;p.style.width=n>0?Math.min(t/n*100,100)+'%':'0%'};window.addEventListener('scroll',u,{passive:true});window.addEventListener('resize',u,{passive:true});u()})();
    </script>'''

def make_quick_summary_html(bullets):
    items = "\n".join(f"                <li>{b}</li>" for b in bullets)
    return f'''    <!-- Quick Summary -->
    <div class="quick-summary" style="background:#faf8fc;border:1px solid #e0d8f0;border-left:4px solid #7a64b8;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem 0 2rem;font-size:1rem">
        <h3 style="color:#7a64b8;font-size:1.15rem;margin:0 0 .8rem">⏱️ Quick Summary — 30-Second Read</h3>
        <ul style="margin:0;padding-left:1.2rem;list-style:none">
{items}
        </ul>
    </div>'''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # 1. Add Quick Summary between hero section and <main class="guide-content">
    # Find the pattern: </section> (end of hero) followed by <main
    if filename in QUICK_SUMMARIES:
        qs_html = make_quick_summary_html(QUICK_SUMMARIES[filename])
        # Insert after the hero section's closing </section> and before <main>
        content = content.replace(
            '    </section>\n\n    <main class="guide-content">',
            f'    </section>\n{qs_html}\n    <main class="guide-content">'
        )
        print(f"  + Quick Summary added")
    else:
        print(f"  ! No Quick Summary definition found for {filename}")
    
    # 2. Add progress bar HTML right after <body>
    if '<div class="cd-reading-progress"' not in content:
        content = content.replace(
            '<body>\n    <header>',
            f'<body>\n{PROGRESS_BAR_HTML}\n    <header>'
        )
        print(f"  + Progress bar HTML added")
    
    # 3. Add progress bar CSS to the <style> block (before </style>)
    if '/* Reading Progress Bar */' not in content:
        content = content.replace(
            '</style>\n</head>',
            f'{PROGRESS_BAR_CSS}\n    </style>\n</head>'
        )
        print(f"  + Progress bar CSS added")
    
    # 4. Add progress bar JS before </body>
    if "'scroll',u" not in content:
        content = content.replace(
            '</body>',
            f'{PROGRESS_BAR_JS}\n</body>'
        )
        print(f"  + Progress bar JS added")
    
    # 5. Remove old .progress-widget{display:none} if it exists (no longer needed)
    content = content.replace(
        '        .progress-widget{display:none !important}\n',
        ''
    )
    content = content.replace(
        '        .progress-widget{display:none !important}',
        ''
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved {filename}")

def main():
    files = sorted(glob.glob(os.path.join(CD_DIR, "crimson-desert-*-guide-2026.html")))
    # Filter to only our 24 new articles (those with Quick Summary definitions)
    target_files = [f for f in files if os.path.basename(f) in QUICK_SUMMARIES]
    
    print(f"Found {len(target_files)} articles to process\n")
    for i, fp in enumerate(target_files, 1):
        fn = os.path.basename(fp)
        print(f"[{i:02d}/24] {fn}")
        process_file(fp)
        print()
    
    print(f"\n=== Done! Processed {len(target_files)} articles ===")

if __name__ == "__main__":
    main()
