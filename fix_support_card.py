import re
import os

guides = [
    'guides/osrs-interface-controls-beginner-guide-2026.html',
    'guides/osrs-combat-triangle-explained-2026.html',
    'guides/osrs-skills-overview-beginner-2026.html',
    'guides/osrs-bank-inventory-management-2026.html',
    'guides/osrs-maps-travel-guide-2026.html',
]

base = r'C:\Users\Lenovo\osrs-guide-site'

for g in guides:
    path = os.path.join(base, g)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the support card block
    support_match = re.search(r'(\s+)(<!-- SUPPORT CARD -->.*?)(\s+)(<!-- RELATED GUIDES -->)', content, re.DOTALL)
    if not support_match:
        print(f'❌ {g}: pattern not found')
        continue

    indent_before_support = support_match.group(1)
    support_block = support_match.group(2)
    indent_between = support_match.group(3)
    related_start = support_match.group(4)

    # Remove support block from current position (and the whitespace after it)
    content_without_support = content.replace(
        indent_before_support + support_block + indent_between,
        indent_between,
        1
    )

    # Now find where RELATED GUIDES block ends (before </div> closing container or before footer)
    related_pattern = r'(\s+)(<!-- RELATED GUIDES -->.*?)(\s+)(</div>\s*</main>|<footer)'
    related_match = re.search(related_pattern, content_without_support, re.DOTALL)
    if not related_match:
        print(f'❌ {g}: related guides end not found')
        continue

    indent_before_related = related_match.group(1)
    related_block = related_match.group(2)
    indent_after_related = related_match.group(3)
    closing_tag = related_match.group(4)

    # Insert support block between related guides and closing tag
    new_content = content_without_support.replace(
        indent_before_related + related_block + indent_after_related + closing_tag,
        indent_before_related + related_block + indent_after_related + '\n' + indent_before_related + support_block + '\n' + closing_tag,
        1
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'✅ {g}: support card moved to bottom')

print('Done!')
