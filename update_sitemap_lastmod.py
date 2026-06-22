#!/usr/bin/env python
# Update sitemap.xml lastmod dates for P0-upgraded articles (2026-06-22)
# Strategy: update ALL guide URLs with lastmod 2026-06-13 to 2026-06-22
# Also update URLs with 2026-06-14 or 2026-06-16 (recent updates)

import re

sitemap_path = r'C:\Users\Lenovo\osrs-guide-site\sitemap.xml'

with open(sitemap_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Track changes
changes = 0

# Pattern: match <lastmod>YYYY-MM-DD</lastmod> in guide URLs
# We want to update articles that were upgraded today (2026-06-22)
# Strategy: update ALL guide URLs with older dates to 2026-06-22
# But preserve pages that have 2026-06-21 or 2026-06-22 already

def replace_lastmod(match):
    global changes
    old_date = match.group(1)
    if old_date in ['2026-06-22', '2026-06-21']:
        return match.group(0)  # Keep already-updated dates
    changes += 1
    return f'<lastmod>2026-06-22</lastmod>'

# Replace lastmod dates in guide URLs (lines with /guides/ in the URL)
lines = content.split('\n')
new_lines = []
for line in lines:
    if '/guides/' in line and '<lastmod>' in line:
        new_line = re.sub(r'<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>', replace_lastmod, line)
        new_lines.append(new_line)
    else:
        new_lines.append(line)

new_content = '\n'.join(new_lines)

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Done! Updated {changes} lastmod dates to 2026-06-22')
print(f'Total lines: {len(new_lines)}')
