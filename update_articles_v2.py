#!/usr/bin/env python3
"""Batch update all guide articles for light violet theme - robust version"""
import os
import sys

BASE = r'C:\Users\Lenovo\osrs-guide-site'

# Replacement rules (old, new, description)
RULES = [
    # Hero gradient - dark brown -> light lavender
    (
        'linear-gradient(135deg,#2a1a0a 0%,#3b2615 40%,#4a3320 100%)',
        'linear-gradient(135deg,#EDE8F5 0%,#E0D8F0 40%,#D8D0E8 100%)',
        'hero-gradient-1'
    ),
    (
        'linear-gradient(135deg, #2a1a0a 0%, #3b2615 40%, #4a3320 100%)',
        'linear-gradient(135deg, #EDE8F5 0%, #E0D8F0 40%, #D8D0E8 100%)',
        'hero-gradient-2'
    ),
    # tip-box / cta-box / callout background
    (
        'background:#3b2615',
        'background:#F0ECF5',
        'tip-box-bg-1'
    ),
    (
        'background: #3b2615',
        'background: #F0ECF5',
        'tip-box-bg-2'
    ),
    (
        'background-color:#3b2615',
        'background-color:#F0ECF5',
        'tip-box-bg-3'
    ),
    # Bottom li style - light cream -> dark text
    (
        '.guide-content li{color:#e8d5b7!important}',
        '.guide-content li{color:#2D2A33!important}',
        'li-color-1'
    ),
    (
        '.guide-content li {color:#e8d5b7!important}',
        '.guide-content li {color:#2D2A33!important}',
        'li-color-2'
    ),
    # Inline light text colors that become invisible on light bg
    (
        'color:#e8d5b7',
        'color:#2D2A33',
        'text-color-1'
    ),
    (
        'color: #e8d5b7',
        'color: #2D2A33',
        'text-color-2'
    ),
    (
        'color:#e8d9bc',
        'color:#2D2A33',
        'text-color-3'
    ),
    (
        'color: #e8d9bc',
        'color: #2D2A33',
        'text-color-4'
    ),
]

def update_file(filepath):
    """Update a single file, return number of replacements made"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return -1, str(e)

    original = content
    count = 0
    applied = []

    for old, new, desc in RULES:
        if old in content:
            content = content.replace(old, new)
            count += 1
            applied.append(desc)

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return count, ', '.join(applied)
        except PermissionError:
            # Try to write to a temp file then replace
            try:
                import tempfile
                fd, tmp = tempfile.mkstemp(suffix='.html', dir=os.path.dirname(filepath))
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(content)
                os.replace(tmp, filepath)
                return count, ', '.join(applied)
            except Exception as e2:
                return -2, f'{", ".join(applied)} | WRITE ERROR: {e2}'

    return 0, ''

def main():
    guides_dir = os.path.join(BASE, 'guides')
    files = [f for f in os.listdir(guides_dir) if f.endswith('.html')]

    total_files = 0
    total_replacements = 0
    errors = []
    skipped = []

    print(f'Scanning {len(files)} files in {guides_dir}...\n')

    for fname in sorted(files):
        filepath = os.path.join(guides_dir, fname)
        n, desc = update_file(filepath)
        if n > 0:
            total_files += 1
            total_replacements += n
            print(f'  ✓ {fname}: {n} fixes ({desc})')
        elif n == -1:
            errors.append(f'{fname}: READ ERROR')
        elif n == -2:
            errors.append(f'{fname}: {desc}')
        # n == 0: no changes needed, skip

    print(f'\n=== Done! ===')
    print(f'  Files updated: {total_files}')
    print(f'  Total replacements: {total_replacements}')

    if errors:
        print(f'\n=== Errors ({len(errors)}) ===')
        for e in errors[:10]:
            print(f'  ✗ {e}')
        if len(errors) > 10:
            print(f'  ... and {len(errors)-10} more')

if __name__ == '__main__':
    main()
