#!/usr/bin/env python3
"""Batch replace Ko-fi links with PayPal _xclick buttons in all guide HTML files."""

import os
import re

# PayPal _xclick URL (your verified email)
PAYPAL_URL = (
    "https://www.paypal.com/cgi-bin/webscr"
    "?cmd=_xclick"
    "&business=1530398390@qq.com"
    "&item_name=Support+OSRSGuru+-+Buy+me+a+pack+of+gum"
    "&currency_code=USD"
    "&no_shipping=1"
    "&return=https://osrsguru.com"
)

# The old Ko-fi pattern to find and replace
OLD_A_PATTERN = re.compile(
    r'<a[^>]+href="https://ko-fi\.com/fyanchun"[^>]*class="support-btn"[^>]*>.*?</a>',
    re.DOTALL
)

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old = content
    # Replace Ko-fi <a> tag with PayPal button
    new_content = OLD_A_PATTERN.sub(
        f'<a href="{PAYPAL_URL}" target="_blank" rel="noopener" class="support-btn paypal-btn">Support on PayPal 💳</a>',
        content
    )

    if new_content != old:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ Updated: {os.path.relpath(filepath)}")
        return True
    return False


def main():
    guides_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guides')
    updated = 0
    skipped = 0

    for fname in sorted(os.listdir(guides_dir)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(guides_dir, fname)
        if replace_in_file(fpath):
            updated += 1
        else:
            skipped += 1

    print(f"\nDone: {updated} updated, {skipped} skipped (no Ko-fi link found)")


if __name__ == '__main__':
    main()
