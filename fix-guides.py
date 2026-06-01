#!/usr/bin/env python3
"""
OSRS Guide Site - Batch Fix Script
Fixes all identified issues in guide HTML files.
"""

import os
import re
import shutil

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

# ============================================================
# FIX 1: Remove Chinese character remnants (8 places)
# ============================================================
CHINESE_FIXES = {
    "osrs-passive-money-making-while-offline.html": [
        ("activities that成熟 and give", "activities that mature and give"),
    ],
    "osrs-desert-treasure-quest-guide-for-low-level.html": [
        ("4 hidden强光", "4 hidden diamonds"),
    ],
    "osrs-cheapest-99-runecrafting-2026.html": [
        ("Kara规范", "Karamja"),
    ],
    "osrs-how-to-fight-corporeal-beast-loot-guide.html": [
        ("minimise damage from祝福", "minimise damage from its dark core attack"),
        ("Cor can hit 50+ with祝福", "Cor can hit 50+ with its dark core"),
    ],
    "osrs-how-to-get-graceful-outfit-full-guide.html": [
        ("the one with the榻榻米符号", "the house with the icon on the minimap"),
    ],
    "osrs-how-to-unlock-the-abyss-guide.html": [
        ("进人深渊", "enter the Abyss"),
    ],
    "osrs-f2p-ironman-money-making-early-game.html": [
        ("这些方法", "these methods"),
    ],
    "quest-guide.html": [
        ("攻略", "walkthrough"),
    ],
}

# ============================================================
# FIX 2: Fix factual errors
# ============================================================
FACTUAL_FIXES = {
    "osrs-passive-money-making-while-offline.html": [
        # "Galaxy/Stars" should be "Shooting Stars"
        ("Method 3: Galaxy/Stars (Level 10+ Mining, Dwarven Mine)", 
         "Method 3: Shooting Stars (Level 10+ Mining)"),
        ("Mining stars gives mining XP and stardust (sell to operator for GP). Stars respawn every 2 hours in random worlds.",
         "Shooting Stars fall across Gielinor every 2 hours. Mine the star for Stardust, which can be exchanged for items including coins, ores, and astral runes. Low effort and great Mining XP."),
        # "Raising Pets (Varrock Museum)" is factually wrong - pets can't be sold on GE
        ("Method 5: Raising Pets (Varrock Museum)", "Method 5: Managing Miscellania (Level 35+ Quest)"),
        ("After cleaning 200 specimens at Varrock Museum, you unlock fossil cleaning. The fossils can be traded for unique pets. Not directly profitable, but pets can be sold on GE for high prices if you get a rare one.",
         "After completing Throne of Miscellania (35+ Quest), you can assign subjects to gather resources. With 750K+ GP in the coffer and 100% approval, you can earn 50,000-150,000 GP/day passively. Check and refill the coffer every few days."),
    ],
    "osrs-how-to-fight-corporal-beast-loot-guide.html": [
        # Title says "Corporal Beast" - should be "Corporeal Beast"
        ("OSRS How to Fight Corporal Beast (Loot Guide) 2026", 
         "OSRS How to Fight Corporeal Beast (Loot Guide) 2026"),
        # "Decent into Darkness" doesn't exist as a quest
        ("Decent into Darkness", "Summertime in the Corp's Cave"),
    ],
    "osrs-how-to-rune-spinning-profit-2026.html": [
        # "While Quest RPeeding" - typo
        ("While Quest RPeeding", "While Getting Quest XP"),
        # Nav links point to wrong files
        ('href="osrs-f2p-ironman-money-making-early-game.html">Money Making', 
         'href="money-making.html">Money Making'),
        ('href="osrs-desert-treasure-quest-guide-for-low-level.html">Quest Guide',
         'href="quest-guide.html">Quest Guide'),
        ('href="osrs-how-to-solo-god-wars-boss-for-beginners.html">Boss Guides',
         'href="boss-killing.html">Boss Guides'),
        ('href="osrs-f2p-ironman-money-making-early-game.html">Money Making',
         'href="money-making.html">Money Making'),
        ('href="osrs-how-to-solo-god-wars-boss-for-beginners.html">Boss Guides',
         'href="boss-killing.html">Boss Guides'),
    ],
    "osrs-f2p-money-making-no-stats-required.html": [
        # Link to misspelled file
        ('href="osrs-low-effort-money-making-for-beginers.html"', 
         'href="osrs-low-effort-money-making-for-beginners.html"'),
    ],
    "osrs-passive-money-making-while-offline.html": [
        # Link to misspelled file
        ('href="osrs-low-effort-money-making-for-beginers.html"',
         'href="osrs-low-effort-money-making-for-beginners.html"'),
    ],
}

# ============================================================
# FIX 3: Delete duplicate files
# ============================================================
FILES_TO_DELETE = [
    "osrs-how-to-fight-corporal-beast-loot-guide.html",  # Misspelled, keep corporeal version
    "osrs-low-effort-money-making-for-beginers.html",     # Misspelled, keep beginners version
]

# ============================================================
# FIX 4: Fix canonical URLs (osrsguide.com -> ua202419891987.github.io/osrs-guide-site)
# ============================================================
CANONICAL_DOMAIN_OLD = "https://osrsguide.com"
CANONICAL_DOMAIN_NEW = "https://ua202419891987.github.io/osrs-guide-site"

# ============================================================
# FIX 5: Standardize nav for all guide files
# ============================================================
STANDARD_NAV = '''<nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="money-making.html">Money Making</a></li>
                    <li><a href="skill-training.html">Skill Training</a></li>
                    <li><a href="quest-guide.html">Quest Guide</a></li>
                    <li><a href="boss-killing.html">Boss Guides</a></li>
                </ul>
            </nav>'''

# Active nav variants for category pages
ACTIVE_NAV_MONEY = '''<nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="money-making.html" class="active">Money Making</a></li>
                    <li><a href="skill-training.html">Skill Training</a></li>
                    <li><a href="quest-guide.html">Quest Guide</a></li>
                    <li><a href="boss-killing.html">Boss Guides</a></li>
                </ul>
            </nav>'''

ACTIVE_NAV_SKILL = '''<nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="money-making.html">Money Making</a></li>
                    <li><a href="skill-training.html" class="active">Skill Training</a></li>
                    <li><a href="quest-guide.html">Quest Guide</a></li>
                    <li><a href="boss-killing.html">Boss Guides</a></li>
                </ul>
            </nav>'''

ACTIVE_NAV_QUEST = '''<nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="money-making.html">Money Making</a></li>
                    <li><a href="skill-training.html">Skill Training</a></li>
                    <li><a href="quest-guide.html" class="active">Quest Guide</a></li>
                    <li><a href="boss-killing.html">Boss Guides</a></li>
                </ul>
            </nav>'''

ACTIVE_NAV_BOSS = '''<nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="money-making.html">Money Making</a></li>
                    <li><a href="skill-training.html">Skill Training</a></li>
                    <li><a href="quest-guide.html">Quest Guide</a></li>
                    <li><a href="boss-killing.html" class="active">Boss Guides</a></li>
                </ul>
            </nav>'''


def get_active_nav_for_file(filename):
    """Determine which nav item should be active based on filename."""
    # Category pages
    if filename == "money-making.html":
        return ACTIVE_NAV_MONEY
    if filename == "skill-training.html":
        return ACTIVE_NAV_SKILL
    if filename == "quest-guide.html":
        return ACTIVE_NAV_QUEST
    if filename == "boss-killing.html":
        return ACTIVE_NAV_BOSS
    
    # Guide pages - determine active based on content keywords
    money_keywords = ["money", "profit", "gold", "flipping", "f2p", "ironman-money", "wintertodt", "passive", "low-effort", "spinning"]
    skill_keywords = ["1-99", "skill", "training", "agility", "cooking", "runecrafting", "smithing", "herblore", "woodcutting", "fishing", "hunter", "thieving", "prayer", "attack", "strength", "defence"]
    quest_keywords = ["quest", "desert-treasure", "lost-city", "fremennik", "monkey-madness", "dragon-slayer", "fairy-rings", "abyss", "rune-pouch", "dragon-defender", "graceful", "dinosaur", "fossil-island", "kourend"]
    boss_keywords = ["boss", "zulrah", "vorkath", "corporeal", "sarachnis", "hydra", "smoke-devil", "god-wars", "grotesque", "guardian", "green-dragons"]
    
    fname_lower = filename.lower()
    
    for kw in money_keywords:
        if kw in fname_lower:
            return ACTIVE_NAV_MONEY
    for kw in boss_keywords:
        if kw in fname_lower:
            return ACTIVE_NAV_BOSS
    for kw in quest_keywords:
        if kw in fname_lower:
            return ACTIVE_NAV_QUEST
    for kw in skill_keywords:
        if kw in fname_lower:
            return ACTIVE_NAV_SKILL
    
    return STANDARD_NAV


def fix_file(filepath, filename):
    """Apply all fixes to a single file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Fix 1: Chinese remnants
    if filename in CHINESE_FIXES:
        for old, new in CHINESE_FIXES[filename]:
            if old in content:
                content = content.replace(old, new)
                changes.append(f"  Fixed Chinese: '{old}' -> '{new}'")
    
    # Fix 2: Factual errors
    if filename in FACTUAL_FIXES:
        for old, new in FACTUAL_FIXES[filename]:
            if old in content:
                content = content.replace(old, new)
                changes.append(f"  Fixed factual: '{old}' -> '{new}'")
    
    # Fix 3: Fix canonical URLs
    if CANONICAL_DOMAIN_OLD in content:
        content = content.replace(CANONICAL_DOMAIN_OLD, CANONICAL_DOMAIN_NEW)
        changes.append(f"  Fixed canonical URLs: osrsguide.com -> github.io")
    
    # Fix 4: Fix nav - replace everything between <nav> and </nav>
    active_nav = get_active_nav_for_file(filename)
    nav_pattern = re.compile(r'<nav>.*?</nav>', re.DOTALL)
    if nav_pattern.search(content):
        old_nav = nav_pattern.search(content).group()
        new_nav = active_nav
        content = nav_pattern.sub(new_nav, content)
        if old_nav != new_nav:
            changes.append(f"  Fixed nav links to standard format")
    
    # Fix 5: Fix CSS path in category pages (css/style.css -> ../css/style.css)
    if 'href="css/style.css"' in content:
        content = content.replace('href="css/style.css"', 'href="../css/style.css"')
        changes.append(f"  Fixed CSS path: css/style.css -> ../css/style.css")
    
    # Fix 6: Fix links to misspelled files
    content = content.replace('osrs-how-to-fight-corporal-beast-loot-guide.html', 'osrs-how-to-fight-corporeal-beast-loot-guide.html')
    content = content.replace('osrs-low-effort-money-making-for-beginers.html', 'osrs-low-effort-money-making-for-beginners.html')
    
    # Fix 7: Fix category page guide links (guides/xxx.html -> xxx.html since we're already in guides/)
    if filename in ['boss-killing.html', 'money-making.html', 'quest-guide.html', 'skill-training.html']:
        content = re.sub(r'href="guides/', 'href="', content)
        changes.append(f"  Fixed category page links: removed 'guides/' prefix")
    
    # Fix 8: Fix wrong nav active states in old-format guide files
    # Some files have class="active" on wrong nav items
    # This is handled by the nav replacement above
    
    # Fix 9: Add Font Awesome CDN if missing
    if 'font-awesome' not in content and 'fontawesome' not in content:
        fa_link = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
        # Insert after the style.css link
        if '../css/style.css' in content:
            content = content.replace(
                'href="../css/style.css">',
                'href="../css/style.css">\n' + fa_link
            )
            changes.append(f"  Added Font Awesome CDN")
    
    # Fix 10: Fix footer links (some footers have wrong nav links too)
    # Footer nav should point to category pages with correct relative paths
    content = content.replace('href="../guides/money-making.html"', 'href="money-making.html"')
    content = content.replace('href="../guides/skill-training.html"', 'href="skill-training.html"')
    content = content.replace('href="../guides/quest-guide.html"', 'href="quest-guide.html"')
    content = content.replace('href="../guides/boss-killing.html"', 'href="boss-killing.html"')
    
    # Write back if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return []


def main():
    print("=" * 60)
    print("OSRS Guide Site - Batch Fix Script")
    print("=" * 60)
    
    all_changes = {}
    
    # Process all HTML files
    for filename in sorted(os.listdir(GUIDES_DIR)):
        if not filename.endswith('.html'):
            continue
        if filename in FILES_TO_DELETE:
            continue
            
        filepath = os.path.join(GUIDES_DIR, filename)
        changes = fix_file(filepath, filename)
        if changes:
            all_changes[filename] = changes
    
    # Delete duplicate files
    print("\n--- Deleting Duplicate Files ---")
    for filename in FILES_TO_DELETE:
        filepath = os.path.join(GUIDES_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  DELETED: {filename}")
    
    # Print summary
    print(f"\n--- Fix Summary ---")
    print(f"Files modified: {len(all_changes)}")
    total_fixes = sum(len(v) for v in all_changes.values())
    print(f"Total fixes applied: {total_fixes}")
    
    for filename, changes in sorted(all_changes.items()):
        print(f"\n{filename}:")
        for change in changes:
            print(change)


if __name__ == "__main__":
    main()
