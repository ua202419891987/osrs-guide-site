#!/usr/bin/env python3
import re, sys, os

BASE = "C:/Users/Lenovo/osrs-guide-site/guides"

def get_qs(filename):
    qs = {
        "osrs-bond-farming-free-membership-2026.html": """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">&#9201;&#65039; 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Keep OSRS membership active forever without spending real money:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Bond cost:</strong> ~5.2M GP per 14 days = ~370K GP/day</li>
    <li><strong>F2P first bond:</strong> Ogress Warriors (40+ combat) at 220K GP/hr &#8212; ~24 hours to 5.2M GP</li>
    <li><strong>Early member:</strong> Wintertodt at 200K&#8211;400K GP/hr + Green Dragons at 400K&#8211;600K GP/hr</li>
    <li><strong>Sustained:</strong> Zulrah/Vorkath at 1.5M&#8211;2.5M GP/hr &#8212; bond in 2&#8211;3 hours</li>
    <li><strong>Passive income:</strong> Bird house runs (100K&#8211;200K GP/day) + herb runs (200K&#8211;400K GP/day)</li>
  </ul>
</div>""",
    }
    if filename in qs:
        return qs[filename]
    return None

for fn in sys.argv[1:]:
    path = os.path.join(BASE, fn)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Meta
    m = re.search(r'<meta name="description" content="([^"]*)"', content, re.I)
    if m and not m.group(1).startswith("Updated for July 2026."):
        d = m.group(1)
        d = re.sub(r'^Updated[^.]*\.\s*', '', d)
        content = content.replace(m.group(0), f'<meta name="description" content="Updated for July 2026. {d}"')

    # 2. Quick Summary
    if '30-Second Quick Summary' not in content:
        qs_html = get_qs(fn)
        if qs_html:
            t = re.search(r'<(div|nav) class="(toc|table-of-contents)">', content)
            if t:
                content = content[:t.start()] + '\n' + qs_html + '\n' + content[t.start():]

    # 3. TOC
    content = content.replace('class="table-of-contents"', 'class="toc"')

    # 4. Dark style fix
    content = content.replace('color:#e8d5b7', 'color:#1a1a1a')

    # 5. CSS
    content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
    css = """<style>
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
    content = content.replace('</body>', css + '\n</body>')

    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {fn}")
