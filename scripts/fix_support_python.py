# -*- coding: utf-8 -*-
"""
Comprehensive Support Card Fixer - Python Version
Fixes all 3 issues in one pass:
  1. Remove Chinese/Alipay payment text from new-format cards
  2. Upgrade old "Support on PayPal" cards to new $3/$5/$10/Custom format
  3. Add inline support hint before Support Card in guide articles

Run: python fix_support_python.py
Or double-click: batch_update_support.bat
"""
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'guides')
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'new_card_template.txt')

# Load the new support card template
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    NEW_CARD = f.read()

INLINE_HINT = '''\n            <div class="inline-support-hint">
                <p>If this guide helped you on your OSRS journey, <strong>consider supporting the author</strong> below &mdash; it keeps this site free and updated for everyone. \u2764\ufe0f</p>
            </div>\n'''

# Regex patterns
PAT_CHINESE = re.compile(r'\s*<div class="support-alt-pay">.*?</div>\s*', re.DOTALL)
PAT_OLD_CARD = re.compile(
    r'<div\s+class="support-card"[^>]*>'     # opening div
    r'\s*<div\s+class="support-inner">'        # inner container
    r'\s*<span\s+class="support-icon">[^<]+</span>'
    r'\s*<div\s+class="support-text">'
    r'\s*<h3>[^<]+</h3>'
    r'\s*<p>[^<]+</p>'
    r'\s*</div>'                              # close support-text
    r'\s*<a\s+href="[^"]*paypal[^"]*"'         # old PayPal button
    r'[^>]*class="support-btn[^"]*"'
    r'[^>]*>[^<]+</a>'
    r'\s*</div>\s*</div>',                    # close both divs
    re.DOTALL
)
PAT_COMMENT = re.compile(r'(\s*)(<!--\s*Support Card\s*-->)', re.DOTALL)

def main():
    if not os.path.isdir(GUIDES_DIR):
        print(f"ERROR: Guides directory not found: {GUIDES_DIR}")
        return
    
    files = sorted([f for f in os.listdir(GUIDES_DIR) if f.endswith('.html')])
    
    cn = up = hi = ok = err = 0
    
    print("=" * 55)
    print("  SUPPORT CARD COMPREHENSIVE FIXER")
    print(f"  Target: {GUIDES_DIR} ({len(files)} files)")
    print("=" * 55)
    print()
    
    for filename in files:
        filepath = os.path.join(GUIDES_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        actions = []
        
        # Step 1: Remove Chinese payment text
        if 'Alipay' in content or 'WeChat' in content:
            new_content = PAT_CHINESE.sub('', content)
            if len(new_content) != len(content):
                content = new_content
                cn += 1
                changed = True
                actions.append('RM-CN')
        
        # Step 2: Upgrade old format cards
        if 'Support on PayPal' in content or 'class="support-btn"' in content:
            before_len = len(content)
            content = PAT_OLD_CARD.sub(NEW_CARD, content)
            if len(content) != before_len:
                up += 1
                changed = True
                actions.append('UPG')
        
        # Step 3: Add inline support hint
        if ('inline-support-hint' not in content 
            and ('Support Card' in content or 'support-card' in content)):
            new_content = PAT_COMMENT.sub(r'\1' + INLINE_HINT + r'\2', content)
            if 'inline-support-hint' in new_content:
                content = new_content
                hi += 1
                changed = True
                actions.append('HINT')
        
        # Write back if changed
        if changed:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  [OK] {filename:<50} {' '.join(actions)}")
            except PermissionError:
                err += 1
                print(f"  [ERR] {filename} - Permission denied")
            except Exception as e:
                err += 1
                print(f"  [ERR] {filename} - {e}")
        else:
            if 'support-amount-btn' in content and 'inline-support-hint' in content:
                ok += 1
            elif 'support-card' not in content and 'Support Card' not in content:
                pass  # skip silently - no support card
            else:
                print(f"  [??]  {filename} - needs review")
    
    print()
    print("=" * 55)
    print(f"  Chinese text removed : {cn}")
    print(f"  Old cards upgraded   : {up}")
    print(f"  Inline hints added   : {hi}")
    print(f"  Already correct      : {ok}")
    print(f"  Errors              : {err}")
    print("=" * 55)
    print("  DONE!")
    
if __name__ == '__main__':
    main()
