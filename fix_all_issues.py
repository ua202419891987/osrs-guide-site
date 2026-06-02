import os, glob

root = r'C:\Users\Lenovo\osrs-guide-site'

# Fix 1: GA4 ID across ALL HTML files
old_ga = 'G-S1BGC91MVV'
new_ga = 'G-5I86091MYV'
ga_count = 0

for html_file in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_ga in content:
        content = content.replace(old_ga, new_ga)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        ga_count += 1
        print(f'[GA4] Fixed: {os.path.basename(html_file)}')

print(f'\n[GA4] Total: {ga_count} files updated ({old_ga} -> {new_ga})\n')

# Fix 2: Logo text across ALL HTML files
old_logo = 'OSRSGuides'
new_logo = 'OSRS Guru'
logo_count = 0

for html_file in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_logo in content:
        content = content.replace(old_logo, new_logo)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        logo_count += 1
        print(f'[Logo] Fixed: {os.path.basename(html_file)}')

print(f'\n[Logo] Total: {logo_count} files updated ({old_logo} -> {new_logo})\n')

# Fix 3: Wrong canonical domains in guide pages
wrong_domains = ['osrsguidehub.com', 'osrsguides.com']
canonical_count = 0

for html_file in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for wrong in wrong_domains:
        content = content.replace(f'https://{wrong}/', 'https://osrsguru.com/')
        content = content.replace(f'"{wrong}"', '"osrsguru.com"')
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        canonical_count += 1
        print(f'[Canonical] Fixed: {os.path.basename(html_file)}')

print(f'\n[Canonical] Total: {canonical_count} files updated (wrong domain -> osrsguru.com)\n')
print('='*60)
print(f'ALL FIXES COMPLETE!')
print(f'  GA4 IDs: {ga_count} files')
print(f'  Logo text: {logo_count} files')
print(f'  Canonical URLs: {canonical_count} files')
print('='*60)
