#!/usr/bin/env python3
"""
Second pass: Fix Chinese translations inside parentheses that have
duplicate emoji/numbering prefixes matching the English text.
Example: "① 🏗️ Essential for Smithing（① 🏗️ 锻造必需）" 
     -->  "① 🏗️ Essential for Smithing（锻造必需）"
"""

import re
import glob

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\zh\guides"

# Pattern to match emoji/number prefixes that commonly appear at start of text
PREFIX_RE = re.compile(
    r'^[①-⑩⛏🪨🎯⚒📍🎽💰📈💎💵🌋💜🏆🏅💊⚡❓🗡🎮⚔🛡✨🙏🔐🏦🗺📜🔑🏃🥇🥈🥉📊'
    r'](?:\uFE0F)?\s*'
)

def clean_duplicate_prefixes(content):
    """Remove duplicate emoji/number prefixes from Chinese parentheses text."""
    # Pattern: EnglishText(EmojiPrefix Chinese)
    # Match: non-greedy text, then (Chinese)
    
    def fix_match(m):
        full = m.group(0)
        before_paren = m.group(1)  # English text before (
        chinese = m.group(2)       # Chinese content inside ()
        
        # Check if the Chinese starts with a prefix that matches the end of English text
        m_eng_prefix = PREFIX_RE.match(before_paren)
        m_chn_prefix = PREFIX_RE.match(chinese)
        
        if m_eng_prefix and m_chn_prefix:
            eng_pre = m_eng_prefix.group().strip()
            chn_pre = m_chn_prefix.group().strip()
            if eng_pre == chn_pre:
                # Strip the prefix from Chinese
                cleaned = chinese[len(m_chn_prefix.group()):]
                return f"{before_paren}（{cleaned}）"
        return full
    
    # Pattern: English Text before （Chinese inside）
    pattern = re.compile(r'([^>（]+?)（([^）]+)）')
    return pattern.sub(fix_match, content)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = clean_duplicate_prefixes(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  FIXED {os.path.basename(filepath)}")
        return 1
    return 0


import os

def main():
    files = sorted(glob.glob(os.path.join(BASE_DIR, "osrs-*.html")))
    fixed = 0
    for fp in files:
        fixed += process_file(fp)
    print(f"Fixed {fixed} files")


if __name__ == "__main__":
    main()
