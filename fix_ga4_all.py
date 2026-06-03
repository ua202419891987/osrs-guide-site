#!/usr/bin/env python3
"""Fix GA4 tracking code across all OSRS Guru HTML files."""
import os
import glob

SITE_DIR = r"C:\Users\Lenovo\osrs-guide-site"
OLD_ID = "G-14978162960"
NEW_ID = "G-S1BGC91MYV"

GA4_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S1BGC91MYV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-S1BGC91MYV');
</script>
"""

html_files = glob.glob(os.path.join(SITE_DIR, "**/*.html"), recursive=True)
fixed_wrong_id = 0
added_new = 0
skipped = 0

for path in html_files:
    # Skip Google verification file
    if "googlef2d4bacd14fcdb05" in path:
        skipped += 1
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Case 1: Has wrong ID — replace it
    if OLD_ID in content:
        content = content.replace(OLD_ID, NEW_ID)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        fixed_wrong_id += 1
        continue

    # Case 2: No GA4 code at all — inject before </head>
    if "googletagmanager" not in content:
        if "</head>" in content:
            content = content.replace("</head>", GA4_SNIPPET + "</head>")
        elif "</HEAD>" in content:
            content = content.replace("</HEAD>", GA4_SNIPPET + "</HEAD>")
        else:
            print(f"  ⚠️ No </head> found: {os.path.basename(path)}")
            skipped += 1
            continue

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        added_new += 1
        continue

    # Case 3: Already has correct ID — skip
    if NEW_ID in content:
        skipped += 1
        continue

    # Case 4: Has GA4 but neither old nor new ID (edge case)
    print(f"  ⚠️ Unknown GA4 state: {os.path.basename(path)}")
    skipped += 1

print(f"✅ Fixed wrong ID: {fixed_wrong_id} files")
print(f"✅ Added new GA4:  {added_new} files")
print(f"⏭️  Skipped:        {skipped} files")
print(f"📁 Total checked:  {len(html_files)} files")
