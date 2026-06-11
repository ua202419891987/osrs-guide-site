#!/usr/bin/env python3
"""Fix article styles to match medieval brown theme."""
import glob, re, os

targets = [
    "guides/osrs-summer-sweep-up-2026-guide.html",
    "guides/osrs-gauntlet-meta-changes-2026.html",
    "guides/osrs-sailing-wyrmscraig-guide-2026.html",
]

replacements = [
    # Red borders -> gold/dark brown
    ("border: 2px solid #e74c3c", "border: 2px solid #d4af37"),
    ("border-left:4px solid #e74c3c", "border-left:4px solid #d4af37"),
    ("border-color:#e74c3c", "border-color:#d4af37"),
    # Red text -> gold
    ("color: #e74c3c", "color: #d4af37"),
    ("color:#e74c3c", "color:#d4af37"),
    # Red backgrounds -> dark brown
    ("background:#e74c3c", "background:#8b4513"),
    ("background: #e74c3c", "background: #8b4513"),
    # Nerf tag red -> dark brown
    (".tag-nerf { background: #e74c3c", ".tag-nerf { background: #8b4513"),
    # Gradient backgrounds that are too dark red -> use theme colors
    ("background: linear-gradient(135deg, #2d1810 0%, #1a0e08 100%)", "background: linear-gradient(135deg, #3b2615 0%, #2a1810 100%)"),
    ("background:linear-gradient(135deg,#2d1810 0%,#1a0e08 100%)", "background:linear-gradient(135deg,#3b2615 0%,#2a1810 100%)"),
    # TOC nav dark -> theme
    ("background: #1a0e08", "background: #2a1810"),
]

for rel_path in targets:
    path = os.path.join("C:\\Users\\Lenovo\\osrs-guide-site", rel_path)
    if not os.path.exists(path):
        print(f"SKIP: {rel_path} not found")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"FIXED: {rel_path}")
    else:
        print(f"OK: {rel_path} (no changes)")

print("Done.")
