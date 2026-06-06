"""
Batch script: Remove "Support on PayPal 💳" green button from ALL pages
Removes the redundant paypal-btn that was added below $3/$5/$10/Custom buttons
"""
import os
import re

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"
ROOT_DIR = r"C:\Users\Lenovo\osrs-guide-site"

# Pattern to match the green PayPal button (with variable return URL)
# Matches: <a ... class="support-btn paypal-btn" ...>Support on PayPal ...</a>
PAYPAL_BTN_PATTERN = re.compile(
    r'\s*<a\s+href="https://www\.paypal\.com/cgi-bin/webscr\?cmd=_xclick&amp;'
    r'business=1530398390@qq\.com&amp;item_name=Support\+OSRSGuru\+\-\+Buy\+me\+a\+pack\+of\+gum'
    r'&amp;currency_code=USD&amp;no_shipping=1&amp;return=[^"]*"\s+'
    r'target="_blank"\s+rel="noopener"\s+'
    r'class="support-btn paypal-btn"[^>]*>Support on PayPal[^<]*</a>',
    re.IGNORECASE
)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'class="support-btn paypal-btn"' not in content:
        return 'SKIP_NO_BTN'

    new_content, count = PAYPAL_BTN_PATTERN.subn('', content)

    if count == 0:
        return 'NO_MATCH'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return f'OK({count})'


results = {'OK': 0, 'SKIP_NO_BTN': 0, 'NO_MATCH': 0, 'ERROR': 0}
total_removed = 0

# Process root HTML files
for fname in sorted(os.listdir(ROOT_DIR)):
    if fname.endswith('.html'):
        filepath = os.path.join(ROOT_DIR, fname)
        try:
            status = process_file(filepath)
            results[status] = results.get(status, 0) + 1
            if status.startswith('OK'):
                total_removed += 1
            print(f"[{status}] {fname}")
        except Exception as e:
            results['ERROR'] += 1
            print(f"[ERROR] {fname}: {e}")

# Process guide files
for fname in sorted(os.listdir(GUIDES_DIR)):
    if fname.endswith('.html'):
        filepath = os.path.join(GUIDES_DIR, fname)
        try:
            status = process_file(filepath)
            results[status] = results.get(status, 0) + 1
            if status.startswith('OK'):
                total_removed += 1
            print(f"[{status}] guides/{fname}")
        except Exception as e:
            results['ERROR'] += 1
            print(f"[ERROR] guides/{fname}: {e}")

print(f"\n{'='*50}")
print(f"RESULTS:")
print(f"  Files modified (button removed): {total_removed}")
for k, v in sorted(results.items()):
    print(f"  {k}: {v}")
print(f"\nDone! Green PayPal button removed from {total_removed} file(s).")
