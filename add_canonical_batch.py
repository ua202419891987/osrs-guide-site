#!/usr/bin/env python3
"""
Batch add canonical tags to OSRS Guru guide HTML files.
Adds <link rel="canonical" href="..."> after <meta name="keywords" ...>
"""

import os
import re

GUIDES_DIR = "C:/Users/Lenovo/osrs-guide-site/guides"
BASE_URL = "https://osrsguru.com/guides"

def add_canonical_to_file(filepath):
    """Add canonical tag to a single HTML file if missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has canonical tag
    if 'rel="canonical"' in content:
        return False
    
    filename = os.path.basename(filepath)
    canonical_url = f"{BASE_URL}/{filename}"
    
    # Pattern to match <meta name="keywords" ...> tag (handles various formats)
    # Insert canonical link after this tag
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">'
    
    # Try to insert after <meta name="keywords" ...>
    # Match the entire meta keywords tag (handles single or double quotes, with or without closing slash)
    pattern = r'(<meta name=["\']keywords["\'][^>]*>)'
    
    if re.search(pattern, content):
        # Insert canonical tag after the keywords meta tag
        new_content = re.sub(pattern, r'\1\n' + canonical_tag, content, count=1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    else:
        print(f"  WARNING: Could not find keywords meta tag in {filename}")
        return False

def main():
    added = 0
    skipped = 0
    errors = 0
    
    print("Starting canonical tag batch addition...")
    print(f"Scanning: {GUIDES_DIR}\n")
    
    for filename in sorted(os.listdir(GUIDES_DIR)):
        if not filename.endswith('.html'):
            continue
        
        filepath = os.path.join(GUIDES_DIR, filename)
        
        try:
            if add_canonical_to_file(filepath):
                print(f"  ADDED: {filename}")
                added += 1
            else:
                if 'rel="canonical"' in open(filepath, 'r', encoding='utf-8').read():
                    # Already has canonical
                    skipped += 1
                else:
                    errors += 1
        except Exception as e:
            print(f"  ERROR: {filename} - {e}")
            errors += 1
    
    print(f"\nDone!")
    print(f"  Added: {added} files")
    print(f"  Skipped (already had canonical): {skipped} files")
    print(f"  Errors: {errors} files")
    
    # Verify
    print("\nVerifying...")
    missing = []
    for filename in sorted(os.listdir(GUIDES_DIR)):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(GUIDES_DIR, filename)
        if 'rel="canonical"' not in open(filepath, 'r', encoding='utf-8').read():
            missing.append(filename)
    
    if missing:
        print(f"  Still missing canonical: {len(missing)} files")
        for f in missing[:10]:
            print(f"    - {f}")
    else:
        print("  All files now have canonical tags!")

if __name__ == "__main__":
    main()
