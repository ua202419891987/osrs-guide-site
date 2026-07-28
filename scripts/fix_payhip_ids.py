#!/usr/bin/env python3
"""Fix PayHip product IDs: MVa5->MVtu5, qkkmVs->qjkmVs"""
import os, sys

ROOT = r"C:\Users\Lenovo\osrs-guide-site"
DRY = "--dry-run" in sys.argv

count = 0
for dirpath, _, filenames in os.walk(ROOT):
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        fpath = os.path.join(dirpath, fn)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        new_content = content.replace("payhip.com/b/MVa5", "payhip.com/b/MVtu5")
        new_content = new_content.replace("payhip.com/b/qkkmVs", "payhip.com/b/qjkmVs")

        if new_content != content:
            count += 1
            rel = os.path.relpath(fpath, ROOT)
            if not DRY:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
            print(f"  {'[DRY] ' if DRY else ''}Fixed: {rel}")

print(f"\n{'DRY-RUN: ' if DRY else ''}Total files fixed: {count}")
