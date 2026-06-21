"""
Fix CD/WR background: add style='background:transparent' to <main>
and wrap content in <article class='guide-content' with transparent bg.
This matches the OSRS article pattern (light background).
"""
import os
import re

folders = [
    'C:/Users/Lenovo/osrs-guide-site/guides/crimson-desert',
    'C:/Users/Lenovo/osrs-guide-site/guides/windrose',
]

count = 0
for folder in folders:
    for f in sorted(os.listdir(folder)):
        if not f.endswith('.html'):
            continue
        
        path = os.path.join(folder, f)
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # 1. Add style="background:transparent" to <main class="guide-content">
        old_main = '<main class="guide-content">'
        new_main = '<main class="guide-content" style="background:transparent">'
        
        if old_main in content:
            content = content.replace(old_main, new_main, 1)
        else:
            print('SKIP (no main tag found): ' + f)
            continue
        
        # 2. Remove the old FORCE light background rules we added before (they didn't work)
        old_force = '''        /* FORCE: Light theme background for content area */
        .guide-content{background:#F5F2F8 !important}
        body{background:#F5F2F8 !important}'''
        
        content = content.replace(old_force, '')
        
        # 3. Also force body transparent in case of any dark theme residue
        # Insert after the </style> in head - we'll add a small safety rule
        style_end = content.find('</style>')
        if style_end != -1:
            safety_rule = '\n        body{background:var(--bg-page,#F5F2F8)!important}\n'
            content = content[:style_end] + safety_rule + content[style_end:]
        
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(content)
        
        count += 1
        print('FIXED: ' + f)

print('Total fixed: ' + str(count) + ' files')
