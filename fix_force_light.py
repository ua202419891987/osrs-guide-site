import os, re

folders = [
    'C:/Users/Lenovo/osrs-guide-site/guides/crimson-desert',
    'C:/Users/Lenovo/osrs-guide-site/guides/windrose'
]

count = 0
for folder in folders:
    for f in sorted(os.listdir(folder)):
        if not f.endswith('.html'):
            continue
        path = os.path.join(folder, f)
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Find </style> tag position in <head>
        style_end = content.find('</style>')
        if style_end == -1:
            print('NO STYLE: ' + f)
            continue
        
        # Check if we already added the force-light rule
        if 'FORCE_LIGHT_BG' in content:
            print('SKIP (already fixed): ' + f)
            continue
        
        # Build the injection: FORCE LIGHT background on everything inside main
        # Remove old broken rules first
        inject = '''
        /* FORCE_LIGHT_BG: Entire content area must be LIGHT - only support-card stays green */
        main.guide-content{background:#F5F2F8!important}
        main.guide-content>.container{background:#F5F2F8!important}
        .guide-content h2,.guide-content h3,.guide-content p,
        .guide-content ul,.guide-content ol,.guide-content li,
        .guide-content table,.guide-content figure,
        .guide-content .tip-box,.guide-content .warn-box,
        .guide-content .action-step,.guide-content .method-box,
        .guide-content .faq-item{background:transparent!important}
'''
        
        new_content = content[:style_end] + inject + content[style_end:]
        
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        
        count += 1
        print('DONE: ' + f)

print('Total patched: ' + str(count) + ' files')
