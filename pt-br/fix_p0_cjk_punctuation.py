#!/usr/bin/env python3
"""P0: Replace all CJK punctuation with ASCII equivalents across entire pt-br/ site."""
import re
from pathlib import Path

PUNCT_MAP = {
    '\uff0c': ',',   # ，
    '\u3002': '.',   # 。
    '\u3001': ',',   # 、
    '\uff1a': ':',   # ：
    '\uff1f': '?',   # ？
    '\uff01': '!',   # ！
    '\uff1b': ';',   # ；
    '\uff08': '(',   # （
    '\uff09': ')',   # ）
    '\u300a': '"',   # 《
    '\u300b': '"',   # 》
    '\u300c': "'",   # 「
    '\u300d': "'",   # 」
    '\u3010': '[',   # 【
    '\u3011': ']',   # 】
}

BASE = Path(r'C:\Users\Lenovo\osrs-guide-site\pt-br')

total_files = 0
total_replacements = 0

for html_file in sorted(BASE.rglob('*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    for cjk, ascii_char in PUNCT_MAP.items():
        count = content.count(cjk)
        if count > 0:
            content = content.replace(cjk, ascii_char)
            changes += count

    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        total_replacements += changes
        rel = html_file.relative_to(BASE)
        print(f'  {rel}: {changes} replacements')

print(f'\nTotal: {total_files} files, {total_replacements} replacements')
