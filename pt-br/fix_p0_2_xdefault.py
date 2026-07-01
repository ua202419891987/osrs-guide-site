#!/usr/bin/env python3
"""Fix P0-2 x-default hreflang: change from pt-br URLs to en URLs"""

import os

BASE = r"C:\Users\Lenovo\osrs-guide-site\pt-br"

xdefault_fixes = {
    "chefes.html": (
        'hreflang="x-default" href="https://osrsguru.com/pt-br/boss-guides.html"',
        'hreflang="x-default" href="https://osrsguru.com/boss-guides.html"',
    ),
    "habilidades.html": (
        'hreflang="x-default" href="https://osrsguru.com/pt-br/skill-training.html"',
        'hreflang="x-default" href="https://osrsguru.com/skill-training.html"',
    ),
    "iniciante.html": (
        'hreflang="x-default" href="https://osrsguru.com/pt-br/beginner.html"',
        'hreflang="x-default" href="https://osrsguru.com/beginner.html"',
    ),
    "lucro.html": (
        'hreflang="x-default" href="https://osrsguru.com/pt-br/money-making.html"',
        'hreflang="x-default" href="https://osrsguru.com/money-making.html"',
    ),
    "membros.html": (
        'hreflang="x-default" href="https://osrsguru.com/pt-br/membership.html"',
        'hreflang="x-default" href="https://osrsguru.com/membership.html"',
    ),
    "missoes.html": (
        'hreflang="x-default" href="https://osrsguru.com/pt-br/quest-guides.html"',
        'hreflang="x-default" href="https://osrsguru.com/quest-guides.html"',
    ),
}

count = 0
for fname, (old, new) in xdefault_fixes.items():
    fp = os.path.join(BASE, fname)
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"  修复 {fname}: x-default → en URL")
    else:
        print(f"  [警告] {fname}: 未找到旧的 x-default 字符串")

print(f"\nP0-2 x-default: 修复 {count}/6 个 hub 页面")
