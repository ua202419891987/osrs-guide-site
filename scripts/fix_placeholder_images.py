import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

guides_dir = "C:/Users/Lenovo/osrs-guide-site/guides"

articles = [
    "osrs-wyrmscraig-activities-guide-2026.html",
    "osrs-bank-tags-beginners-guide-2026.html",
    "osrs-trouver-parchment-complete-guide-2026.html",
    "osrs-jagex-account-migration-guide-2026.html",
    "osrs-fractured-archive-prep-guide-2026.html",
]

for article in articles:
    fpath = os.path.join(guides_dir, article)
    if not os.path.exists(fpath):
        print(f"FILE NOT FOUND: {article}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Match any <figure...> block containing placeholder URL, across multiple lines
    # Remove it and one trailing newline
    pattern = r'[ \t]*<figure class="guide-img">\s*<img[^>]*2025-00-00[^>]*>.*?</figure>\s*\n?'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Count how many were removed
    removed = len(re.findall(pattern, original, flags=re.DOTALL))
    
    # Clean up triple+ newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if removed > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED] {article}: removed {removed} placeholder figure block(s)")
    else:
        print(f"[CLEAN] {article}: no placeholder images found")

print("\nDone!")
