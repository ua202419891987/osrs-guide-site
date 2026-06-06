"""
Batch script: Add "Support on PayPal 💳" button below amount buttons
in ALL files that have support-amount-custom but don't have "Support on PayPal" text.
"""
import os
import re

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"
ROOT_DIR = r"C:\Users\Lenovo\osrs-guide-site"

# The PayPal button HTML to insert after </div> of support-amounts
PAYPAL_BTN = """<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;business=1530398390@qq.com&amp;item_name=Support+OSRSGuru+-+Buy+me+a+pack+of+gum&amp;currency_code=USD&amp;no_shipping=1&amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-btn paypal-btn" style="margin-top:12px;display:inline-block">Support on PayPal &#128179;</a>"""

# Pattern: find support-amount-custom line, then its closing </div>
# We match: ...support-amount-custom...Custom...</a> then \n + whitespace* + </div> (the amounts div close)
# Then insert the button between that </div> and whatever comes next

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has "Support on PayPal" in support context
    if 'Support on PayPal' in content and 'support-btn' in content:
        # Check if it's the actual support button (not just a next link)
        if 'class="support-btn paypal-btn"' in content and 'Support on PayPal' in content:
            return 'SKIP_ALREADY'

    # Skip if no support-amount-custom
    if 'support-amount-custom' not in content:
        return 'SKIP_NO_AMOUNTS'

    # Pattern: match from support-amount-custom to the end of its parent div
    # The structure is: <div class="support-amounts">...<a ...class="support-amount-custom">...</a>\n\s*</div>
    # We want to insert AFTER this </div>

    # Find the last occurrence of support-amount-custom and its closing div
    pattern = r'(class="support-amount-custom"[^>]*>[^<]*</a>)\s*\n(\s*)(</div>)'
    
    match = None
    for m in re.finditer(pattern, content):
        match = m
    
    if not match:
        return 'NO_MATCH'

    indent = match.group(2)  # indentation before </div>
    insert_pos = match.end()
    
    new_content = content[:insert_pos] + '\n' + indent + PAYPAL_BTN + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return 'OK'


results = {'OK': 0, 'SKIP_ALREADY': 0, 'SKIP_NO_AMOUNTS': 0, 'NO_MATCH': 0, 'ERROR': 0}

# Process root HTML files
for fname in os.listdir(ROOT_DIR):
    if fname.endswith('.html'):
        filepath = os.path.join(ROOT_DIR, fname)
        try:
            status = process_file(filepath)
            results[status] += 1
            print(f"[{status}] {fname}")
        except Exception as e:
            results['ERROR'] += 1
            print(f"[ERROR] {fname}: {e}")

# Process guide files
for fname in os.listdir(GUIDES_DIR):
    if fname.endswith('.html'):
        filepath = os.path.join(GUIDES_DIR, fname)
        try:
            status = process_file(filepath)
            results[status] += 1
            print(f"[{status}] guides/{fname}")
        except Exception as e:
            results['ERROR'] += 1
            print(f"[ERROR] guides/{fname}: {e}")

print(f"\n{'='*50}")
print(f"RESULTS:")
for k, v in sorted(results.items()):
    print(f"  {k}: {v}")
