#!/usr/bin/env python3
"""Batch update all guide articles for light violet theme"""
import os
import glob

# Define replacements
REPLACEMENTS = [
    # Hero gradient (dark brown → light lavender)
    ('linear-gradient(135deg,#2a1a0a 0%,#3b2615 40%,#4a3320 100%)',
     'linear-gradient(135deg,#EDE8F5 0%,#E0D8F0 40%,#D8D0E8 100%)'),
    
    ('linear-gradient(135deg, #2a1a0a 0%, #3b2615 40%, #4a3320 100%)',
     'linear-gradient(135deg, #EDE8F5 0%, #E0D8F0 40%, #D8D0E8 100%)'),
    
    # tip-box / cta-box / callout backgrounds (dark brown → light lavender)
    ('background:#3b2615', 'background:#F0ECF5'),
    ('background: #3b2615', 'background: #F0ECF5'),
    ('background-color:#3b2615', 'background-color:#F0ECF5'),
    
    # Some articles use slightly different dark colors for boxes
    ('background:#2a1a0a', 'background:#EDE8F5'),
    ('background: #2a1a0a', 'background: #EDE8F5'),
    
    # Bottom li style (light cream → dark text)
    ('.guide-content li{color:#e8d5b7!important}', '.guide-content li{color:#2D2A33!important}'),
    ('.guide-content li {color:#e8d5b7!important}', '.guide-content li {color:#2D2A33!important}'),
    
    # Other inline text colors that would be invisible on light bg
    ('color:#e8d5b7', 'color:#2D2A33'),
    ('color: #e8d5b7', 'color: #2D2A33'),
    ('color:#e8d9bc', 'color:#2D2A33'),
    ('color: #e8d9bc', 'color: #2D2A33'),
    
    # Table / section backgrounds
    ('background:rgba(59,39,22,', 'background:rgba(240,236,245,'),
    ('background:rgba(74,51,32,', 'background:rgba(232,228,242,'),
    
    # Border colors
    ('border-color:#3b2615', 'border-color:#D4CDE0'),
    ('border:1px solid #3b2615', 'border:1px solid #D4CDE0'),
]

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    count = 0
    
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            count += 1
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return count
    return 0

if __name__ == '__main__':
    base = r'C:\Users\Lenovo\osrs-guide-site\guides'
    files = glob.glob(os.path.join(base, '*.html'))
    
    total_replacements = 0
    updated_files = 0
    
    for filepath in files:
        n = update_file(filepath)
        if n > 0:
            updated_files += 1
            total_replacements += n
            print(f'  {os.path.basename(filepath)}: {n} replacements')
    
    print(f'\n=== Done! {updated_files} files updated, {total_replacements} total replacements ===')
