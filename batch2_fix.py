#!/usr/bin/env python3
"""Batch 2 of 10 articles: upgrade dormant articles"""

import os

batch2 = [
    'osrs-blowpipe-guide-2026.html',
    'osrs-boss-profit-comparison-2026.html',
    'osrs-clue-scrolls-beginner-guide-2026.html',
    'osrs-colosseum-fortis-guide-2026.html',
    'osrs-combat-training-beginner-2026.html',
    'osrs-common-beginner-mistakes-avoid-2026.html',
    'osrs-daily-weekly-reset-activities-guide-2026.html',
    'osrs-dangerous-pvp-rewards-guide-2026.html',
    'osrs-desert-treasure-quest-guide-low-level.html',
    'osrs-easy-clue-scroll-guide-2026.html',
]

NEW_CSS = '''<style>
.guide-content{color:#1a1a1a!important}
.guide-content li,.guide-content p,.guide-content td,.guide-content th,.guide-content h3,.guide-content h4{color:#1a1a1a!important}
.guide-content .tip-box,.guide-content .method-box,.guide-content .action-step,.guide-content .quick-verdict,.guide-content .faq-item{background:#fff!important;border-color:#e0d5c0!important}
.guide-content .tip-box p,.guide-content .tip-box li,.guide-content .method-box p,.guide-content .method-box li,.guide-content .faq-item p,.guide-content .faq-item li,.guide-content .quick-verdict p,.guide-content .action-step p{color:#1a1a1a!important}
.guide-content .faq-item h3,.guide-content .faq-item h4,.guide-content .method-box h3,.guide-content .method-box h4,.guide-content .quick-verdict h3,.guide-content .action-step h4,.guide-content .tip-box strong,.guide-content .method-box strong{color:#3b2615!important}
.guide-content .related-guides .article-card{background:#f5f2f8!important;border-color:#ebe5f0!important}
.guide-content .related-guides .article-card:hover{background:#f0ecf5!important;border-color:#D4CDE0!important}
</style>'''

OLD_CSS_SINGLE = '.guide-content li{color:#e8d5b7!important}'
AI_QA_SCRIPT = '<script src="../js/ai-qa-widget.js"></script>'

for f in batch2:
    path = f'guides/{f}'
    if not os.path.exists(path):
        print(f'  NOT FOUND: {f}')
        continue
    
    with open(path, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    orig = html
    
    if OLD_CSS_SINGLE in html:
        html = html.replace(OLD_CSS_SINGLE, NEW_CSS)
    
    if AI_QA_SCRIPT not in html:
        html = html.replace('</body>', f'    {AI_QA_SCRIPT}\n</body>')
    
    html = html.replace('OSRS <span>GuideHub</span>', 'OSRS <span>Guru</span>')
    html = html.replace('OSRSGuideHub', 'OSRS Guru')
    
    if html != orig:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        print(f'  ✅ {f}')
    else:
        print(f'  ⏭️ {f}')

print(f'\nBatch 2 done: {len(batch2)} articles')
