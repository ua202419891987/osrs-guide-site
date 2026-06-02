import os, glob

old_id = 'G-S1B0C91MYV'
new_id = 'G-5I86091MYV'
root = r'C:\Users\Lenovo\osrs-guide-site'
count = 0

for html_file in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_id in content:
        content = content.replace(old_id, new_id)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f'Updated: {html_file}')

print(f'\nTotal: {count} files updated. GA tracking ID: {old_id} -> {new_id}')
