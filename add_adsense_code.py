#!/usr/bin/env python3
"""Add AdSense verification code to all HTML files."""

import os
import glob

ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435" crossorigin="anonymous"></script>'

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site"

html_files = glob.glob(os.path.join(BASE_DIR, "*.html")) + glob.glob(os.path.join(BASE_DIR, "guides", "*.html"))

modified = 0
skipped = 0

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has AdSense code
    if "adsbygoogle.js" in content or "ca-pub-8532760886171435" in content:
        skipped += 1
        continue

    # Insert AdSense code before </head>
    if "</head>" in content:
        new_content = content.replace("</head>", ADSENSE_CODE + "\n</head>", 1)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        modified += 1
        print(f"  ✅ Added: {os.path.basename(filepath)}")
    else:
        print(f"  ⚠️ No </head> found: {os.path.basename(filepath)}")

print(f"\nDone! Modified: {modified}, Skipped (already has code): {skipped}")
