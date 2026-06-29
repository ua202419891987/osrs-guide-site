import os
import re
import sys

# Fix Windows console encoding for Chinese characters
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

print("=" * 80)
print("IMAGE & VIEWPORT CHECK FOR 12 NEW ARTICLES")
print("=" * 80)

issues = []

for article in articles:
    fpath = os.path.join(guides_dir, article)
    if not os.path.exists(fpath):
        print(f"\n❌ FILE NOT FOUND: {article}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n{'='*60}")
    print(f"📄 {article}")
    print(f"{'='*60}")
    
    # Check viewport
    if 'viewport' in content:
        print("✅ viewport meta tag: PRESENT")
    else:
        print("❌ viewport meta tag: MISSING")
        issues.append(f"{article}: missing viewport meta tag")
    
    # Check images
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', content)
    figures = re.findall(r'<figcaption>(.*?)</figcaption>', content, re.DOTALL)
    
    print(f"   Images found: {len(imgs)}")
    for i, src in enumerate(imgs):
        # Check if it's a Jagex CDN URL
        if 'cdn.runescape.com' in src:
            # Check for placeholder URL (2025-00-00)
            if '2025-00-00' in src:
                print(f"   ⚠️  Image {i+1}: PLACEHOLDER URL (2025-00-00) — {src[-40:]}")
                issues.append(f"{article}: image {i+1} has placeholder URL")
            else:
                print(f"   ✅ Image {i+1}: Jagex CDN — {src[-40:]}")
        elif src.startswith('http'):
            print(f"   ⚠️  Image {i+1}: External URL — {src[:60]}")
            issues.append(f"{article}: image {i+1} is external URL")
        elif src.startswith('../images/'):
            print(f"   ✅ Image {i+1}: Local file — {src}")
        else:
            print(f"   ❓ Image {i+1}: {src[:60]}")
    
    # Check figcaption has Source attribution
    for i, cap in enumerate(figures):
        if 'Source:' in cap or 'source:' in cap:
            print(f"   ✅ Figcaption {i+1}: Has 'Source:' attribution")
        else:
            print(f"   ⚠️  Figcaption {i+1}: No 'Source:' attribution — {cap.strip()[:50]}")
    
    # Check CSS path
    css_match = re.search(r'href="([^"]*style\.css)"', content)
    if css_match:
        css_path = css_match.group(1)
        if css_path == '../css/style.css':
            print("✅ CSS path: correct (../css/style.css)")
        else:
            print(f"❌ CSS path: WRONG ({css_path})")
            issues.append(f"{article}: wrong CSS path")
    else:
        print("❌ CSS path: NOT FOUND")

print(f"\n{'='*80}")
print(f"SUMMARY: {len(issues)} issues found")
for issue in issues:
    print(f"  - {issue}")
print(f"{'='*80}")
