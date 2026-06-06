"""
Batch update all support cards across OSRS Guru site v2.
Handles BOTH structural variations of the old support card:
- Pattern A: paypal button INSIDE support-inner (after support-text)
- Pattern B: paypal button OUTSIDE support-inner (sibling)
"""

import os
import re

SITE_DIR = r"C:\Users\Lenovo\osrs-guide-site"

# Pattern A: button inside support-inner (after </div> of support-text)
PATTERN_A = re.compile(
    r'(?:<!--\s*S[sU]pport\s+C[aA]rd\s*-->\s*)?'   # optional comment
    r'<div\s+class="support-card"[^>]*>\s*'
    r'<div\s+class="support-inner">\s*'
    r'<span\s+class="support-icon">[^<]+</span>\s*'
    r'<div\s+class="support-text">\s*'
    r'<h3>[^<]+</h3>\s*'
    r'<p>[^<]+</p>\s*'
    r'</div>\s*'   # close support-text
    r'<a\s+href="[^"]*paypal[^"]*"[^>]*class="support-btn[^"]*"[^>]*>[^<]+</a>\s*'   # button inside inner
    r'</div>\s*</div>',   # close inner, close card
    re.IGNORECASE | re.DOTALL
)

# Pattern B: button outside support-inner (sibling, after support-inner closes)
PATTERN_B = re.compile(
    r'(?:<!--\s*S[sU]pport\s+C[aA]rd\s*-->\s*)?'   # optional comment
    r'<div\s+class="support-card"[^>]*>\s*'
    r'<div\s+class="support-inner">\s*'
    r'<span\s+class="support-icon">[^<]+</span>\s*'
    r'<div\s+class="support-text">\s*'
    r'<h3>[^<]+</h3>\s*'
    r'<p>[^<]+</p>\s*'
    r'</div>\s*'   # close support-text
    r'</div>\s*'   # close support-inner
    r'<a\s+href="[^"]*paypal[^"]*"[^>]*class="support-btn[^"]*"[^>]*>[^<]+</a>\s*'   # button sibling
    r'</div>',   # close card
    re.IGNORECASE | re.DOTALL
)

NEW_CARD = """<!-- Support Card -->
<div class="support-card" style="margin:32px 0 0 0">
    <div class="support-inner">
        <span class="support-icon">🌿</span>
        <div class="support-text">
            <h3>Buy me a pack of gum &mdash; let&apos;s be friends!</h3>
            <p>I&apos;m a game guide creator dedicated to helping OSRS players level up faster. Every donation goes directly into keeping this site updated with fresh content for the community. Support is always optional &mdash; pay what feels right.</p>
            <div class="support-amounts">
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;business=1530398390@qq.com&amp;item_name=Support+OSRSGuru&amp;amount=3&amp;currency_code=USD&amp;no_shipping=1&amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-btn">$3</a>
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;business=1530398390@qq.com&amp;item_name=Support+OSRSGuru&amp;amount=5&amp;currency_code=USD&amp;no_shipping=1&amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-btn recommended">$5 &#9733;</a>
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;business=1530398390@qq.com&amp;item_name=Support+OSRSGuru&amp;amount=10&amp;currency_code=USD&amp;no_shipping=1&amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-btn">$10</a>
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;business=1530398390@qq.com&amp;item_name=Support+OSRSGuru+-+Buy+me+a+pack+of+gum&amp;currency_code=USD&amp;no_shipping=1&amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-custom">Custom &#9998;</a>
            </div>
            <div class="support-alt-pay">
                <p>&#127468;&#127463; Chinese users prefer Alipay or WeChat? <a href="mailto:1530398390@qq.com?subject=OSRSGuru+Support" style="color:#d4af37;text-decoration:none;font-weight:600">Email me</a> for alternative payment.</p>
            </div>
        </div>
    </div>
</div>"""


def find_html_files(root_dir):
    skip_names = {
        'googlef2d4bacd14fcdb05.html',
        'ga4_dashboard.html',
        'medium-article-formatted.html',
    }
    html_files = []
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.html') and fname not in skip_names:
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)


def main():
    html_files = find_html_files(SITE_DIR)
    total = len(html_files)
    replaced_a = 0
    replaced_b = 0
    skipped = 0

    print(f"Scanning {total} HTML files...\n")

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            rel_path = os.path.relpath(filepath, SITE_DIR)

            if PATTERN_A.search(content):
                new_content = PATTERN_A.sub(NEW_CARD, content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [A] {rel_path}")
                replaced_a += 1
            elif PATTERN_B.search(content):
                new_content = PATTERN_B.sub(NEW_CARD, content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [B] {rel_path}")
                replaced_b += 1
            else:
                skipped += 1
        except Exception as e:
            rel_path = os.path.relpath(filepath, SITE_DIR)
            print(f"  [X] ERROR: {rel_path} - {e}")

    total_replaced = replaced_a + replaced_b
    print(f"\n{'='*55}")
    print(f"Done! Pattern A: {replaced_a} | Pattern B: {replaced_b}")
    print(f"Total updated: {total_replaced} | Skipped: {skipped}")


if __name__ == '__main__':
    main()
