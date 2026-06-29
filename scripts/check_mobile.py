import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

guides_dir = "C:/Users/Lenovo/osrs-guide-site/guides"

articles = [
    "osrs-wyrmscraig-activities-guide-2026.html",
    "osrs-wyrmscraig-rewards-ranking-2026.html",
    "osrs-bank-tags-layout-guide-2026.html",
    "osrs-bank-tags-beginners-guide-2026.html",
    "osrs-trouver-system-rework-guide-2026.html",
    "osrs-trouver-parchment-complete-guide-2026.html",
    "osrs-fractured-archive-prep-guide-2026.html",
    "osrs-fractured-archive-rewards-analysis-2026.html",
    "osrs-ge-max-cash-guide-2026.html",
    "osrs-inflation-gear-prices-2026.html",
    "osrs-jagex-account-migration-guide-2026.html",
    "osrs-jagex-account-faq-2026.html",
]

print("=" * 70)
print("MOBILE RESPONSIVENESS CHECK")
print("=" * 70)

for article in articles:
    fpath = os.path.join(guides_dir, article)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check for tables (may cause horizontal scroll on mobile)
    tables = re.findall(r'<table', content)
    
    # Check for fixed width on images
    imgs_with_fixed_w = re.findall(r'<img[^>]*width="(\d+)"[^>]*>', content)
    
    # Check for inline styles with fixed widths
    fixed_containers = re.findall(r'style="[^"]*width\s*:\s*\d+px[^"]*"', content)
    
    # Check for pre/code blocks (may overflow)
    pre_blocks = re.findall(r'<pre|<code>', content)
    
    # Check for custom font sizes
    font_sizes_small = re.findall(r'font-size\s*:\s*([6789]|1[0-2])px', content)
    
    report = []
    if tables:
        report.append(f"  ⚠️  {len(tables)} table(s) — may need horizontal scroll wrapper on mobile")
    if imgs_with_fixed_w:
        report.append(f"  ⚠️  {len(imgs_with_fixed_w)} img(s) with fixed width={imgs_with_fixed_w} — check CSS overrides")
    if pre_blocks:
        report.append(f"  ℹ️  {len(pre_blocks)} code/pre block(s)")
    
    if report:
        print(f"\n📄 {article}")
        for r in report:
            print(r)
    else:
        pass  # All clean, skip output to keep it concise

# Now check the main CSS for mobile breakpoints
css_path = "C:/Users/Lenovo/osrs-guide-site/css/style.css"
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    print(f"\n{'='*70}")
    print("CSS MEDIA QUERY BREAKPOINTS")
    print(f"{'='*70}")
    
    media_queries = re.findall(r'@media[^{]*\{', css)
    for mq in media_queries:
        print(f"  {mq.strip()}")
    
    # Check if guide-content has mobile styles
    guide_styles = re.findall(r'\.guide-content\s*[^{]*\{[^}]*\}', css)
    for gs in guide_styles:
        gs_clean = gs.strip()[:120]
        print(f"\n  Guide Content: {gs_clean}")

print("\nDone!")
