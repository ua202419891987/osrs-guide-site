"""Batch add AdSense code to HTML files that are missing it."""
import os
import re

ADSENSE_TAG = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435"
     crossorigin="anonymous"></script>'''

# Files to skip (not real site pages)
SKIP = [
    "googlef2d4bacd14fcdb05.html",
    "medium-article-formatted.html",
    "medium-osrs-money-making-2026.html",
]

BASE = r"C:\Users\Lenovo\osrs-guide-site"

# Get all .html files
added = 0
skipped_list = []
errors = []
total = 0

for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith(".html"):
            continue
        rel_path = os.path.relpath(os.path.join(root, f), BASE)

        # Skip non-site files
        if f in SKIP:
            skipped_list.append(f"skip: {rel_path}")
            continue

        filepath = os.path.join(root, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            content = fh.read()

        # Already has adsbygoogle? Skip
        if "adsbygoogle" in content:
            skipped_list.append(f"already: {rel_path}")
            continue

        total += 1
        # Strategy: insert after GA4 inline script, before the next tag
        # GA4 pattern: gtag('config', 'G-S1BGC91MYV');</script>
        pattern = re.compile(r"(gtag\('config', 'G-S1BGC91MYV'\);</script>)", re.DOTALL)
        match = pattern.search(content)
        if match:
            insert_pos = match.end()
            new_content = content[:insert_pos] + "\n" + ADSENSE_TAG + "\n" + content[insert_pos:]
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write(new_content)
            added += 1
            print("Added:", rel_path)
        else:
            errors.append(rel_path)

print()
print("=== Summary ===")
print("Added:", added)
if errors:
    print("Errors:", len(errors))
    for e in errors:
        print("  ERR:", e)
