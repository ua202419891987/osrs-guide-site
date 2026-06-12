#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix old dark-brown inline styles in all guide articles for the new Violet Sunrise theme.
Run this script in: C:\Users\Lenovo\osrs-guide-site\
Command: python fix_article_colors.py
"""

import os
import glob
import re

BASE = r'C:\Users\Lenovo\osrs-guide-site\guides'

# Replacement rules: (old_pattern, new_string)
REPLACEMENTS = [
    # Table zebra rows: dark brown bg -> light lavender bg
    ('style="background:#4a3320"', 'style="background:#F0ECF5"'),
    ('style="background:#3b2615"', 'style="background:#F0ECF5"'),
    ('style="background:#2a1a0a"', 'style="background:#F0ECF5"'),
    
    # tip-box with old inline dark bg
    ('class="tip-box" style="background:#4a3320;border-radius:8px;padding:20px;margin:20px 0"',
     'class="tip-box"'),
    ('class="tip-box" style="background:#3b2615;border-radius:8px;padding:20px;margin:20px 0"',
     'class="tip-box"'),
    ('class="tip-box" style="background:#2a1a0a;border-radius:8px;padding:20px;margin:20px 0"',
     'class="tip-box"'),
    
    # Hero gradient: old brown -> new lavender
    ('background:linear-gradient(135deg,#2a1a0a 0%,#3b2615 40%,#4a3320 100%)',
     'background:linear-gradient(135deg,#EDE8F5 0%,#E0D8F0 60%,#D4CAE8 100%)'),
    ('background: linear-gradient(135deg, #2a1a0a 0%, #3b2615 40%, #4a3320 100%)',
     'background:linear-gradient(135deg,#EDE8F5 0%,#E0D8F0 60%,#D4CAE8 100%)'),
    
    # li color in bottom style tag
    ('.guide-content li{color:#e8d5b7!important}', '.guide-content li{color:#2D2A33!important}'),
    ('.guide-content li{color:#e8d5b7 !important}', '.guide-content li{color:#2D2A33!important}'),
    
    # Fix bottom injected <style> block - h2/h3 gold color -> lavender purple
    ('  .guide-content h2, .guide-content h3 { color: #d4af37 !important;}',
     '  .guide-content h2, .guide-content h3 { color: #7A64B8 !important;}'),
    ('.guide-content h2, .guide-content h3 { color: #d4af37 !important;}',
     '.guide-content h2, .guide-content h3 { color: #7A64B8 !important;}'),
    
    # Remove border-none overrides that hide tip-box borders
    ('  .tip-box, .warning-box, .toc, .faq-item, .free-disclaimer, .method-box, .info-box, .callout { border: none !important; border-left: none !important; border-right: none !important; border-top: none !important; border-bottom: none !important; border-color: transparent !important;}',
     ''),
    ('.tip-box, .warning-box, .toc, .faq-item, .free-disclaimer, .method-box, .info-box, .callout { border: none !important; border-left: none !important; border-right: none !important; border-top: none !important; border-bottom: none !important; border-color: transparent !important;}',
     ''),

    # Old dark background for progress tracker / TOC boxes
    ('background:#3b2615;', 'background:rgba(155,132,212,0.08);'),
    ('background: #3b2615;', 'background:rgba(155,132,212,0.08);'),
    ('background:#2a1a0a;', 'background:rgba(155,132,212,0.06);'),
    
    # White-on-dark text that should now be dark
    ('color:#e8d5b7', 'color:#2D2A33'),
    ('color: #e8d5b7', 'color:#2D2A33'),
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    count = 0
    
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            count += content.count(new) - original.count(new) if original.count(new) else 0
            count += 1  # at least one replacement happened
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return count
    return 0

def main():
    files = glob.glob(os.path.join(BASE, '*.html'))
    total_files = 0
    total_fixes = 0
    
    for fp in sorted(files):
        n = fix_file(fp)
        if n > 0:
            total_files += 1
            total_fixes += n
            fname = os.path.basename(fp)
            print(f'  Fixed: {fname}')
    
    print(f'\n=== Done! {total_files} files updated ===')

if __name__ == '__main__':
    main()
