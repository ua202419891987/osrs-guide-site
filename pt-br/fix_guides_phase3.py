#!/usr/bin/env python3
"""
Phase 3: Fix remaining garbled/Chinese text in guide article bodies.
Handles: TOC headers with garbled Chinese, link descriptions with single CJK chars.
"""
import re
from pathlib import Path

BASE = Path(r'C:\Users\Lenovo\osrs-guide-site')
GUIDES = BASE / 'pt-br' / 'guides'

# TOC header text: garbled Chinese→Portuguese
TOC_GARBLED = {
    # These appear in <h3>Table of Contents(Ŀ¼)</h3> form
    # The Ŀ¼ is a corrupted version of 目录 (Table of Contents)
}

# Full TOC section regex pattern to replace
TOC_RE = re.compile(
    r'<h3>Table of Contents\([^)]+\)</h3>'
)

# Skill name replacements in article body
SKILL_CN2PT = {
    '��': '',
    'ħ': '',  # Latin h with stroke - corrupted data
    'С': '',  # Cyrillic - corrupted data
    'Сʱ': 'Hora',
    'Сʱ': '',
    'Ŀ¼': 'Índice',  # Replace (Ŀ¼) with proper Portuguese
    '目录': 'Índice',  # Proper Chinese for Table of Contents
    'Ŀ': '',
    '¼': '',
}

def fix_guide(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix TOC headers: Table of Contents(XXXX) → Table of Contents (Índice)
    content = re.sub(
        r'Table of Contents\([^)]*\)',
        'Table of Contents (Índice)',
        content
    )
    
    # Fix h2/h3 TOC entries with corrupted CJK in parentheses
    # Pattern: <h4>Attack / Strength / Defence (70→99)(xxxx)(yyyy)</h4>
    # Remove everything after the first closing paren if inside TOC
    content = re.sub(
        r'(<h[234]>[^(]+\([^)]+\))\([^)]+\)',
        r'\1',
        content
    )
    
    # Fix remaining corrupted CJK characters by removing them
    # These are garbled data that can't be displayed properly
    corrupted_ranges = [
        (0x013F, 0x0140),  # Ŀ/ŀ - Latin
        (0x00BC, 0x00BE),  # ¼½¾ - fractions
        (0x0400, 0x04FF),  # Cyrillic
        (0x0100, 0x024F),  # Latin Extended
    ]
    
    def is_corrupted(c):
        code = ord(c)
        # Single CJK chars that are left over
        if '\u4e00' <= c <= '\u9fff':
            return True
        for start, end in corrupted_ranges:
            if start <= code <= end:
                return True
        return False
    
    # Remove isolated corrupted characters (not part of complete words)
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        # Skip lines with mostly HTML
        if line.strip().startswith('<') and '>' in line:
            # But still clean inside text nodes
            # Only process lines with full text nodes
            text_outside_tags = re.sub(r'<[^>]+>', '▁▁▁', line)
            # Check if this text has corrupted chars
            if any(is_corrupted(c) for c in text_outside_tags):
                # Try to clean
                cleaned = ''
                in_tag = False
                for c in line:
                    if c == '<':
                        in_tag = True
                    elif c == '>':
                        in_tag = True
                        cleaned += c
                        in_tag = False
                        continue
                    
                    if not in_tag and is_corrupted(c):
                        continue  # Skip corrupted char
                    cleaned += c
                line = cleaned
        clean_lines.append(line)
    content = '\n'.join(clean_lines)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def count_cn(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return len([c for c in content if '\u4e00' <= c <= '\u9fff'])

if __name__ == '__main__':
    print("Phase 3: Guide article garbled text fix\n")
    fixed = 0
    total_before = 0
    total_after = 0
    
    for fpath in sorted(GUIDES.glob('*.html')):
        before = count_cn(fpath)
        total_before += before
        if before > 0:
            if fix_guide(fpath):
                after = count_cn(fpath)
                total_after += after
                fixed += 1
                if after > 0:
                    # Only print if significant change
                    if before - after > 5:
                        print(f"  [OK] {fpath.name}: {before} -> {after}")
    
    print(f"\n--- Summary ---")
    print(f"  Articles fixed: {fixed}")
    print(f"  Total before: {total_before}")
    print(f"  Total after: {total_after}")
    print(f"  Reduction: {total_before - total_after} chars")
    
    # Show remaining top offenders
    print(f"\n  Remaining CJK per article:")
    dirty = [(f.name, count_cn(f)) for f in sorted(GUIDES.glob('*.html')) if count_cn(f) > 0]
    for name, cnt in sorted(dirty, key=lambda x: -x[1])[:15]:
        print(f"  {name}: {cnt} chars")
    
    print("\nDone!")
