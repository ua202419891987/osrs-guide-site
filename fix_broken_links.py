#!/usr/bin/env python3
"""Fix 11 broken internal links found across OSRS guide files."""

import os
import re

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

# Mapping: broken_filename → correct_filename
FIXES = {
    "osrs-1-99-herblore-guide-2026.html": "osrs-low-cost-1-99-herblore-guide.html",
    "osrs-farming-1-99-guide-2026.html": "osrs-farming-guide-1-99-2026.html",
    "osrs-fastest-99-atack-strength-defence.html": "osrs-fastest-99-attack-strength-defence.html",
    "osrs-monetization-guide-2026.html": "osrs-best-money-making-methods-2026.html",
    "osrs-low-efort-money-making-for-beginers.html": "osrs-low-effort-money-making-for-beginners.html",
    "osrs-low-effort-money-making-for-beginers.html": "osrs-low-effort-money-making-for-beginners.html",
    "osrs-1-99-fishing-afk-method.html": "osrs-how-to-get-99-fishing-afk-method.html",
    "osrs-youtube-short-guide-2026.html": "osrs-youtube-shorts-guide-2026.html",
}

print("="*60)
print("Fixing broken internal links...")
print("="*60)

total_fixes = 0

for filename in os.listdir(GUIDES_DIR):
    if not filename.endswith(".html"):
        continue

    filepath = os.path.join(GUIDES_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for broken, correct in FIXES.items():
        if broken in content:
            content = content.replace(broken, correct)
            print(f"  [FIX] {filename}: {broken} -> {correct}")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        total_fixes += 1

print(f"\nFixed {total_fixes} files.")
print("Done!")
