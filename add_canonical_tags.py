#!/usr/bin/env python3
"""
Add canonical tags to all HTML pages in the OSRS Guru site.
Canonical URL format: https://osrsguru.com/path/to/file.html
"""

import os
import re
import glob

SITE_URL = "https://osrsguru.com"
GUIDES_DIR = "guides"
ROOT_FILES = [
    "index.html",
    "about.html",
    "privacy-policy.html",
    "money-making.html",
    "skill-training.html",
    "quest-guides.html",
    "boss-guides.html",
]

def add_canonical_to_file(filepath, canonical_url):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if canonical already exists
    if 'rel="canonical"' in content:
        print(f"  SKIP (already exists): {filepath}")
        return False

    # Insert canonical link after the </title> tag (inside <head>)
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'

    # Try to insert after </title>
    new_content = content.replace('</title>\n', '</title>\n' + canonical_tag, 1)

    if new_content == content:
        # Try after <meta name="description"
        new_content = content.replace('/>\n', '/>\n' + canonical_tag, 1)

    if new_content == content:
        print(f"  WARN (could not insert): {filepath}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ADDED: {canonical_url}")
    return True


def main():
    added = 0
    skipped = 0

    # Process root files
    print("=== Root files ===")
    for fname in ROOT_FILES:
        fpath = os.path.join(".", fname)
        if not os.path.exists(fpath):
            print(f"  NOT FOUND: {fpath}")
            continue
        url = f"{SITE_URL}/{fname}"
        if add_canonical_to_file(fpath, url):
            added += 1
        else:
            skipped += 1

    # Process guides/
    print("\n=== Guide pages ===")
    guide_files = sorted(glob.glob(os.path.join(GUIDES_DIR, "*.html")))
    for fpath in guide_files:
        fname = os.path.basename(fpath)
        url = f"{SITE_URL}/{GUIDES_DIR}/{fname}"
        if add_canonical_to_file(fpath, url):
            added += 1
        else:
            skipped += 1

    print(f"\nDone: {added} added, {skipped} skipped/existing")


if __name__ == "__main__":
    main()
