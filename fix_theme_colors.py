#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复文章中的红色/深色背景，统一为网站棕色主题
"""
import re, os

files = [
    "guides/osrs-blood-moon-rises-guide-2026.html",
    "guides/osrs-gauntlet-meta-changes-2026.html",
    "guides/osrs-sailing-wyrmscraig-guide-2026.html",
]

base = r"C:\Users\Lenovo\osrs-guide-site"

replacements = [
    # 深红色 → 棕色/金色
    (r'#8b0000', '#3b2615'),
    (r'#ff4444', '#d4af37'),
    # 深黑红渐变背景 → 去掉（用默认样式）
    (r'background:linear-gradient\(135deg,#2d1010,#1a0808\)', 'background:linear-gradient(135deg,#3b2615 0%,#2d1810 100%)'),
    (r'background:linear-gradient\(135deg,#2d1010 0%,#1a0808 100%\)', 'background:linear-gradient(135deg,#3b2615 0%,#2d1810 100%)'),
    # 深黑背景 → 半透明棕色
    (r'background:#1a0e08', 'background:rgba(59,38,21,0.4)'),
    (r'background: #1a0e08', 'background:rgba(59,38,21,0.4)'),
]

for f in files:
    path = os.path.join(base, f)
    if not os.path.exists(path):
        print(f"SKIP (not found): {f}")
        continue
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    original = content
    for old, new in replacements:
        content = re.sub(old, new, content)
    if content != original:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"FIXED: {f}")
    else:
        print(f"OK: {f} (no changes)")

print("\nDone!")
