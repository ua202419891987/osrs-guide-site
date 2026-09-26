#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject AdSense Auto-Ads head script (ca-pub-8532760886171435) into HTML pages missing it.
Only inserts the <head> client script (site uses Auto Ads). Skips:
 - pages already containing 'ca-pub'
 - pages with 'noindex' (redirect/stub pages)
 - backup files
Dry run with: python scripts/inject_adsense.py --dry
"""
import os, glob, sys, re

ROOT = r'C:/Users/Lenovo/osrs-guide-site'
CLIENT = 'ca-pub-8532760886171435'
HEAD_SCRIPT = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
               '?client=%s" crossorigin="anonymous"></script>' % CLIENT)
DRY = '--dry' in sys.argv

def all_html():
    out = []
    out += glob.glob(os.path.join(ROOT, '*.html'))
    out += glob.glob(os.path.join(ROOT, 'guides', '**', '*.html'), recursive=True)
    return [f.replace('\\', '/') for f in out if 'backup' not in f.lower()]

def main():
    files = all_html()
    todo, skip_have, skip_noindex, skip_nohead = [], 0, 0, 0
    for f in files:
        s = open(f, encoding='utf-8', errors='ignore').read()
        if CLIENT in s:
            skip_have += 1; continue
        if 'noindex' in s.lower():
            skip_noindex += 1; continue
        if '</head>' not in s.lower():
            skip_nohead += 1; continue
        todo.append(f)
    print('总HTML: %d | 已有广告:%d | noindex跳过:%d | 无</head>跳过:%d | 将注入:%d'
          % (len(files), skip_have, skip_noindex, skip_nohead, len(todo)))
    if DRY:
        for f in todo[:20]:
            print('  +', f.replace(ROOT + '/', ''))
        if len(todo) > 20: print('  ... 共%d' % len(todo))
        return
    n = 0
    for f in todo:
        s = open(f, encoding='utf-8').read()
        if HEAD_SCRIPT in s:
            continue
        s = s.replace('</head>', HEAD_SCRIPT + '\n</head>', 1)
        open(f, 'w', encoding='utf-8').write(s)
        n += 1
    print('已注入: %d 个页面' % n)

if __name__ == '__main__':
    main()
