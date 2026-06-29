"""
Fix 12 articles:
1. Remove old dark quick-summary block (inside guide-content)
2. Insert new light quick-summary BEFORE guide-content / AFTER hero section
3. Use Crimson Desert style (light background, purple accent)
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

articles = {
    'wyrmscraig-activities': 'osrs-wyrmscraig-activities-guide-2026.html',
    'wyrmscraig-rewards': 'osrs-wyrmscraig-rewards-ranking-2026.html',
    'bank-tags-beginners': 'osrs-bank-tags-beginners-guide-2026.html',
    'bank-tags-layout': 'osrs-bank-tags-layout-guide-2026.html',
    'trouver-system': 'osrs-trouver-system-rework-guide-2026.html',
    'trouver-parchment': 'osrs-trouver-parchment-complete-guide-2026.html',
    'fractured-prep': 'osrs-fractured-archive-prep-guide-2026.html',
    'fractured-rewards': 'osrs-fractured-archive-rewards-analysis-2026.html',
    'ge-max-cash': 'osrs-ge-max-cash-guide-2026.html',
    'inflation': 'osrs-inflation-gear-prices-2026.html',
    'jagex-migration': 'osrs-jagex-account-migration-guide-2026.html',
    'jagex-faq': 'osrs-jagex-account-faq-2026.html',
}

# New light-style Quick Summary block (inserted before <main class="guide-content">)
new_summary_html = '''    <!-- Quick Summary -->
    <div class="quick-summary" style="background:#faf8f5;border:1px solid #e0d5c0;border-left:4px solid #d4af37;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
        <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ Quick Summary &mdash; 30-Second Read</h3>
        <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
            <li>BULLET_1</li>
            <li>BULLET_2</li>
            <li>BULLET_3</li>
        </ul>
    </div>
'''

summaries = {
    'wyrmscraig-activities': [
        '<strong>62 Sailing</strong> + <strong>85+ Combat</strong> required to reach Wyrmscraig Island',
        'Includes: Fallen From Grace quest, repeatable boss, Mortimer Slayer Master with task-choice system',
        'Two new training methods: Golem Crafting (Crafting) &amp; Goat Hunting (Hunter) + Sunstone gathering profit',
    ],
    'wyrmscraig-rewards': [
        '<strong>9 unique rewards</strong> ranked S/A/B/C &mdash; based on the Jagex official proposal',
        '<strong>S-Tier:</strong> Hallowfell (80-150M), Ornate Pipe &mdash; must-grind for PvM and skilling',
        '<strong>A-Tier:</strong> Weather Charms, Rough Basalt upgrades &mdash; solid value for specific activities',
    ],
    'bank-tags-beginners': [
        'Bank Tags launched <strong>June 17, 2026</strong> &mdash; official client + mobile, up to 20 custom tags',
        'Create your first tag in <strong>60 seconds</strong>: tap the + button, name it, drag items in',
        'Layout Plugin adds presets &mdash; auto-copy your gear into any tag with one click',
    ],
    'bank-tags-layout': [
        '5 pro layout templates included: <strong>PvM, Skilling, Slayer, Raids, Daily</strong>',
        'Combine Bank Tags + Layout Plugin for one-click gear presets &mdash; game-changing for bossing',
        'Community tools: RuneTags.com &amp; BankLayouts.com for sharing and importing layouts',
    ],
    'trouver-system': [
        '<strong>Trouver Parchment is now permanent</strong> &mdash; apply once, never re-apply on death',
        'Three-tier system: Tier 1 (never lost), Tier 2 (damaged, repairable), Tier 3 (Trouver required)',
        'Graceful, Fire Cape, and key items no longer permanently lost &mdash; repair cost <strong>500K</strong> above lvl 20',
    ],
    'trouver-parchment': [
        'Complete old vs new system comparison from the <strong>June 17, 2026</strong> wilderness update',
        'Full Tier 1/2/3 classification table &mdash; see exactly which items are safe in the wildy',
        'Cost analysis: one-time ~500K lock vs old per-death consumption &mdash; saves millions for frequent PKers',
    ],
    'fractured-prep': [
        'Requires <strong>base 80+ stats</strong>, all 3 combat styles proficient, bank of <strong>300M+</strong>',
        'Three gear setups: Budget (300-800M), Mid (800M-3B), Best-in-Slot (3B+) &mdash; full item lists included',
        'Team size: 2-8 players with dynamic scaling &mdash; practice mode confirmed for individual bosses',
    ],
    'fractured-rewards': [
        'First rewards proposal for <strong>Raids 4</strong> &mdash; 6 unique rewards decoded and analyzed',
        '<strong>Ascension Crossbows</strong> (2-tick ranged) and <strong>Hybrid Armour</strong> (+16 Prayer) are meta-defining',
        '<strong>TzHaar-Ket Breaker</strong> (crush megaraire) could shake up Corp / Tekton meta',
    ],
    'ge-max-cash': [
        '<strong>2.147B GE limit removed</strong> &mdash; Platinum Tokens allow trading any amount',
        'Rares, 3rd age, Partyhats no longer restricted to street trades &mdash; full market transparency restored',
        'Dev blog published <strong>June 15, 2026</strong> &mdash; the biggest GE change in OSRS history',
    ],
    'inflation': [
        '<strong>Sanguinesti Staff +30-45%</strong>, Inquisitor +36-62% &mdash; Summer Sweep-Up created clear winners',
        '<strong>Bond price forecast:</strong> 13.5-14.5M by Q4 2026 &mdash; buy bonds now if you need membership',
        'Smart buying guide: what to buy before prices rise further, what to sell before they drop',
    ],
    'jagex-migration': [
        '<strong>85% of players already migrated</strong> &mdash; deadline November/December 2026',
        '10-minute upgrade: modern passwords, authenticator 2FA, backup codes, 90-day sessions',
        'Perks: <strong>20 extra bank slots</strong> + Fancier Boots per character &mdash; no more recovery question anxiety',
    ],
    'jagex-faq': [
        '<strong>RuneLite fully compatible</strong> &mdash; all plugins, HDOS, and GPU rendering work fine',
        'Manage up to <strong>20 characters</strong> under one Jagex Account &mdash; switch with one click in launcher',
        'Migration is <strong>irreversible</strong> &mdash; characters, stats, items all carry over intact',
    ],
}

guides_dir = r'C:\Users\Lenovo\osrs-guide-site\guides'

# Pattern to match the old dark-style quick-summary block
old_summary_re = re.compile(
    r'\n\s*<div class="quick-summary"[^>]*>.*?</div>\s*\n',
    re.DOTALL
)

for key, fname in articles.items():
    path = os.path.join(guides_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    
    # 1. REMOVE old quick-summary if it exists
    new_content, count = old_summary_re.subn('\n', content)
    if count > 0:
        content = new_content
        changes += 1
        print(f'✅ [{key}] Old summary removed')
    else:
        print(f'⚠️ [{key}] No old summary found to remove')
    
    # 2. INSERT new quick-summary BEFORE <main class="guide-content">
    # Build the summary HTML with this article's bullets
    bullets = summaries[key]
    summary_html = new_summary_html.replace('BULLET_1', bullets[0])
    summary_html = summary_html.replace('BULLET_2', bullets[1])
    summary_html = summary_html.replace('BULLET_3', bullets[2])
    
    # Insert after hero section's </section> and before <main class="guide-content">
    # Pattern: hero section ends with </section>\n, then <main class="guide-content">
    insert_target = '</section>\n\n    <main class="guide-content"'
    if insert_target in content:
        content = content.replace(
            insert_target,
            '</section>\n' + summary_html + '\n    <main class="guide-content"',
            1
        )
        changes += 1
        print(f'✅ [{key}] New summary inserted before guide-content')
    else:
        print(f'❌ [{key}] Could not find insertion point')
    
    if changes > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  → {fname} saved\n')
    else:
        print(f'⚠️ [{key}] No changes\n')

print(f'\n=== Done ===')
