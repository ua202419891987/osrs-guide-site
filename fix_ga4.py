import os, glob

old_id = 'G-5I86091MYV'
new_id = 'G-14978162960'
count = 0

base = os.path.dirname(os.path.abspath(__file__))
for f in glob.glob('**/*.html', recursive=True):
    fp = os.path.join(base, f)
    content = open(fp, 'r', encoding='utf-8').read()
    if old_id in content:
        open(fp, 'w', encoding='utf-8').write(content.replace(old_id, new_id))
        count += 1
        print(f'Fixed: {f}')

print(f'\nTotal fixed: {count} files')
