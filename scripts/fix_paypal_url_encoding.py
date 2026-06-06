"""
Batch script: Fix double-encoded PayPal URLs
Replace &amp;amp; with &amp; in PayPal link parameters across ALL HTML files
"""
import os
import re

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"
ROOT_DIR = r"C:\Users\Lenovo\osrs-guide-site"

# Fix double-encoded &amp;amp; -> &amp; in PayPal URLs only
# This targets the specific PayPal URL pattern to avoid affecting other content
PAYPAL_DOUBLE_ENCODE_FIX = re.compile(
    r'(&amp;)amp;(business=|item_name=|amount=|currency_code=|no_shipping=1&amp;|return=)',
    re.IGNORECASE
)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has the problem
    if '&amp;amp;business=1530398390' not in content:
        return 'SKIP_CLEAN'

    new_content, count = PAYPAL_DOUBLE_ENCODE_FIX.subn(r'\1\2', content)

    if count == 0:
        return 'NO_MATCH'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return f'OK({count} fixes)'


results = {'OK': 0, 'SKIP_CLEAN': 0, 'NO_MATCH': 0, 'ERROR': 0}
total_fixed = 0

print("Fixing double-encoded PayPal URLs (&amp;amp; -> &amp;)...")
print("=" * 55)

# Process root HTML files
for fname in sorted(os.listdir(ROOT_DIR)):
    if fname.endswith('.html'):
        filepath = os.path.join(ROOT_DIR, fname)
        try:
            status = process_file(filepath)
            results[status] = results.get(status, 0) + 1
            if status.startswith('OK'):
                total_fixed += 1
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
                total_fixed += 1
            print(f"[{status}] guides/{fname}")
        except Exception as e:
            results['ERROR'] += 1
            print(f"[ERROR] guides/{fname}: {e}")

print(f"\n{'='*55}")
print(f"RESULTS:")
print(f"  Files fixed: {total_fixed}")
for k, v in sorted(results.items()):
    print(f"  {k}: {v}")
print(f"\nDone! All PayPal URLs should now work correctly.")
