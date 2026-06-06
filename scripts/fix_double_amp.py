import os

fixed = 0
for root, dirs, files in os.walk('.'):
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        if '&amp;amp;return=' not in content and '&amp;amp;business=' not in content:
            continue
        new_content = content.replace('&amp;amp;return=', '&amp;return=').replace('&amp;amp;business=', '&amp;business=')
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        fixed += 1
        print(f'[FIXED] {fp}')

print(f'\nTotal fixed: {fixed}')
