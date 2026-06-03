import os
import glob

old_id = 'G-5I86091MYV'
new_id = 'G-14978162960'
fixed = 0

for filepath in glob.glob('**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_id in content:
        new_content = content.replace(old_id, new_id)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f'Fixed: {filepath}')

print(f'\nTotal files fixed: {fixed}')
