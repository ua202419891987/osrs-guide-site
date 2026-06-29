"""
Batch update 12 articles:
1. Insert 30-Second Quick Summary after Quick Verdict
2. Add reading progress bar (HTML + CSS + JS)
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Mapping: key -> (filename, [summary bullets])
articles = {
    'wyrmscraig-activities': (
        'osrs-wyrmscraig-activities-guide-2026.html',
        [
            'Requires <strong>62 Sailing</strong> + <strong>85+ Combat</strong> to access Wyrmscraig Island',
            'New content: Fallen From Grace quest, repeatable Fire Cape-tier boss, Mortimer Slayer Master with task-choice system',
            'Two new training methods: Golem Crafting (Crafting) and Goat Hunting (Hunter) + Sunstone gathering for profit'
        ]
    ),
    'wyrmscraig-rewards': (
        'osrs-wyrmscraig-rewards-ranking-2026.html',
        [
            '<strong>9 unique rewards</strong> ranked S/A/B/C — based on Jagex official rewards proposal',
            '<strong>S-Tier:</strong> Hallowfell (80-150M), Ornate Pipe — must-grind for PvM and skilling',
            '<strong>A-Tier:</strong> Weather Charms, Rough Basalt upgrades — strong value for specific activities'
        ]
    ),
    'bank-tags-beginners': (
        'osrs-bank-tags-beginners-guide-2026.html',
        [
            'Bank Tags released on <strong>June 17, 2026</strong> — official client + mobile, up to 20 custom tags',
            'Create your first tag in <strong>60 seconds</strong>: tap +, name it, drag items in',
            'Layout Plugin adds presets — auto-copy your current gear into any tag with one click'
        ]
    ),
    'bank-tags-layout': (
        'osrs-bank-tags-layout-guide-2026.html',
        [
            '5 pro layout templates included: <strong>PvM, Skilling, Slayer, Raids, Daily</strong>',
            'Combine Bank Tags + Layout Plugin for one-click gear presets — game-changing for bossing',
            'Community tools at RuneTags.com and BankLayouts.com for sharing and importing layouts'
        ]
    ),
    'trouver-system': (
        'osrs-trouver-system-rework-guide-2026.html',
        [
            '<strong>Trouver Parchment is now permanent</strong> — apply once, never re-apply on death',
            'Three-tier system: Tier 1 (never lost), Tier 2 (damaged, repairable at Perdu), Tier 3 (Trouver required, permanent)',
            'Graceful, Fire Cape, and other key items no longer permanently lost in wildy — repair cost <strong>500K</strong> above level 20'
        ]
    ),
    'trouver-parchment': (
        'osrs-trouver-parchment-complete-guide-2026.html',
        [
            'Complete breakdown of <strong>old vs new</strong> Trouver Parchment system from June 17, 2026 update',
            'Full Tier 1/2/3 item classification table — see exactly what is safe and what needs a parchment',
            'Cost analysis: one-time ~500K lock vs old per-death consumption — saves millions for regular wildy goers'
        ]
    ),
    'fractured-prep': (
        'osrs-fractured-archive-prep-guide-2026.html',
        [
            'Requires <strong>base 80+ stats</strong>, all 3 combat styles, and a bank of <strong>300M+</strong>',
            'Three gear tiers: Budget (300-800M), Mid (800M-3B), Best-in-Slot (3B+) — with exact item lists',
            'Team composition: 2-8 players, dynamic scaling. Practice mode confirmed — practice individual bosses'
        ]
    ),
    'fractured-rewards': (
        'osrs-fractured-archive-rewards-analysis-2026.html',
        [
            '<strong>First rewards proposal</strong> for Raids 4 — 6 unique rewards decoded and analyzed',
            '<strong>Ascension Crossbows</strong> (2-tick ranged) and <strong>Hybrid Armour</strong> (+16 Prayer) are meta-defining',
            '<strong>TzHaar-Ket Breaker</strong> (crush megaraire) could shake up the Corp / Tekton meta'
        ]
    ),
    'ge-max-cash': (
        'osrs-ge-max-cash-guide-2026.html',
        [
            '<strong>2.147B GE limit removed</strong> — Platinum Tokens now allow trading up to any amount',
            'Rares, 3rd age, and Partyhats no longer restricted to street trades — full market transparency',
            'Dev blog published <strong>June 15, 2026</strong> — the biggest GE change in OSRS history'
        ]
    ),
    'inflation': (
        'osrs-inflation-gear-prices-2026.html',
        [
            '<strong>Sanguinesti Staff +30-45%</strong>, Inquisitor +36-62% — Summer Sweep-Up created clear winners',
            '<strong>Bond price forecast</strong>: 13.5-14.5M by Q4 2026 — buy bonds now if you need membership',
            'Smart buying guide: what to buy before prices rise further, what to sell before they drop'
        ]
    ),
    'jagex-migration': (
        'osrs-jagex-account-migration-guide-2026.html',
        [
            '<strong>85% of players already migrated</strong> — deadline is November/December 2026',
            '10-minute upgrade: modern password rules, authenticator 2FA, backup codes, 90-day session persistence',
            'Perks: <strong>20 extra bank slots</strong> + Fancier Boots per character — and no more recovery question anxiety'
        ]
    ),
    'jagex-faq': (
        'osrs-jagex-account-faq-2026.html',
        [
            '<strong>RuneLite fully compatible</strong> after migration — all plugins, HDOS, and GPU rendering work fine',
            'Manage up to <strong>20 characters</strong> under one Jagex Account — switch with one click in the launcher',
            'Migration is <strong>irreversible</strong> — but your characters, stats, and items all carry over intact'
        ]
    ),
}

# The Quick Summary HTML template
summary_template = '''            <div class="quick-summary" style="background:#2a1a0a;border:1px solid #4a3320;border-left:3px solid #d4af37;border-radius:6px;padding:14px 18px;margin:18px 0;">
                <strong style="color:#d4af37;font-size:.92rem;">⚡ 30-Second Summary</strong>
                <ul style="margin:8px 0 0 0;padding-left:18px;color:#e8d5b7;font-size:.85rem;line-height:1.7;">
                    <li>{}</li>
                    <li>{}</li>
                    <li>{}</li>
                </ul>
            </div>'''

# Progress bar HTML (insert after <body>)
progress_html = '''<div id="reading-progress" style="position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#d4af37,#f0d68a);z-index:99999;width:0%;transition:width .1s ease-out;"></div>'''

# Progress bar JS (insert before </body>)
progress_js = '''<script>
// Reading progress bar
window.addEventListener('scroll', function(){
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    document.getElementById('reading-progress').style.width = (winScroll/height)*100 + '%';
});
</script>'''

guides_dir = r'C:\Users\Lenovo\osrs-guide-site\guides'
updated_summary = 0
updated_progress = 0

for key, (fname, bullets) in articles.items():
    path = os.path.join(guides_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    
    # 1. Insert Quick Summary after Quick Verdict's closing </div>
    quick_verdict_end = '</div>\n\n            <!-- SECTION'
    summary_block = '\n' + summary_template.format(*bullets) + '\n\n            <!-- SECTION'
    
    # Try alternative pattern if first doesn't match
    if quick_verdict_end in content:
        content = content.replace(quick_verdict_end, summary_block, 1)
        changes += 1
        print(f'✅ [{key}] Summary inserted')
    else:
        # Try with different spacing
        quick_verdict_end2 = '</div>\n\n        <!-- SECTION'
        summary_block2 = '\n' + summary_template.format(*bullets) + '\n\n        <!-- SECTION'
        if quick_verdict_end2 in content:
            content = content.replace(quick_verdict_end2, summary_block2, 1)
            changes += 1
            print(f'✅ [{key}] Summary inserted (variant 2)')
        else:
            print(f'❌ [{key}] Could not find Quick Verdict end')
    
    # 2. Add progress bar HTML after <body>
    progress_insert = progress_html + '\n'
    body_tag = '<body'
    body_end = '>'
    
    body_match = re.search(r'(<body[^>]*>)', content)
    if body_match:
        pos = body_match.end()
        content = content[:pos] + '\n' + progress_html + content[pos:]
        changes += 1
        print(f'✅ [{key}] Progress bar HTML added')
    
    # 3. Add progress bar JS before </body>
    if '</body>' in content:
        content = content.replace('</body>', progress_js + '\n</body>', 1)
        changes += 1
        print(f'✅ [{key}] Progress bar JS added')
    
    if changes > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_summary += 1
        print(f'  → {fname} ({changes} changes)\n')
    else:
        print(f'⚠️ [{key}] No changes applied\n')

print(f'\n=== Done: {updated_summary}/12 articles updated ===')
