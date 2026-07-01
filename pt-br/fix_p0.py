#!/usr/bin/env python3
"""
P0 修复脚本 – pt-br 巴西站所有 P0 问题一次性修复
Python 3.13.12
运行路径: C:/Users/Lenovo/osrs-guide-site/pt-br/
"""

import os
import re
import glob

BASE = r"C:\Users\Lenovo\osrs-guide-site\pt-br"
GUIDES_DIR = os.path.join(BASE, "guides")

# ============================================================
# P0-1: 201 篇 guides 缺完整 hreflang
# 当前只有一行 pt-br hreflang (或没有)，替换为 4 行完整 hreflang
# ============================================================
def fix_p0_1():
    guide_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    count = 0

    for fp in guide_files:
        fname = os.path.basename(fp)
        with open(fp, "r", encoding="utf-8") as f:
            original = f.read()

        # 目标: 4 行完整 hreflang
        target_block = (
            f'<link rel="alternate" hreflang="en" href="https://osrsguru.com/guides/{fname}">\n'
            f'<link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/guides/{fname}">\n'
            f'<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/guides/{fname}">\n'
            f'<link rel="alternate" hreflang="x-default" href="https://osrsguru.com/guides/{fname}">'
        )

        old = original

        # 匹配任意连续 hreflang 行（1~N 行），替换为 4 行完整 hreflang
        # 模式: 一行或多行 <link rel="alternate" hreflang=... href=...>
        # 允许行间有空白（空格/换行）
        hreflang_line = r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>'
        block_re = re.compile(
            hreflang_line + r'(\s*\n\s*' + hreflang_line + r')*'
        )

        m = block_re.search(original)
        if m:
            # 有现有 hreflang → 替换整个连续块
            original = original[:m.start()] + target_block + "\n" + original[m.end():]
            count += 1
        else:
            # 完全没有任何 hreflang → 插在 </head> 之前
            head_close = original.find("</head>")
            if head_close >= 0:
                original = original[:head_close] + "\n" + target_block + "\n" + original[head_close:]
                count += 1

        if original != old:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(original)

    print(f"  P0-1: 修复 {count} 篇 guides hreflang (4行完整)")

# ============================================================
# P0-2: 8 个 hub 页面 hreflang 错误
# ============================================================
def fix_p0_2():
    hub_fixes = {
        # 文件名          : (错误的 en hreflang 片段, 正确的 en hreflang 片段)
        "chefes.html": (
            'hreflang="en" href="https://osrsguru.com/pt-br/boss-guides.html"',
            'hreflang="en" href="https://osrsguru.com/boss-guides.html"',
        ),
        "habilidades.html": (
            'hreflang="en" href="https://osrsguru.com/pt-br/skill-training.html"',
            'hreflang="en" href="https://osrsguru.com/skill-training.html"',
        ),
        "iniciante.html": (
            'hreflang="en" href="https://osrsguru.com/pt-br/beginner.html"',
            'hreflang="en" href="https://osrsguru.com/beginner.html"',
        ),
        "lucro.html": (
            'hreflang="en" href="https://osrsguru.com/pt-br/money-making.html"',
            'hreflang="en" href="https://osrsguru.com/money-making.html"',
        ),
        "membros.html": (
            'hreflang="en" href="https://osrsguru.com/pt-br/membership.html"',
            'hreflang="en" href="https://osrsguru.com/membership.html"',
        ),
        "missoes.html": (
            'hreflang="en" href="https://osrsguru.com/pt-br/quest-guides.html"',
            'hreflang="en" href="https://osrsguru.com/quest-guides.html"',
        ),
        # atualizacoes: pt-br hreflang 用了英文名 → 改为 pt-br 文件名
        "atualizacoes-mensais.html": (
            'hreflang="pt-br" href="https://osrsguru.com/pt-br/monthly-updates.html"',
            'hreflang="pt-br" href="https://osrsguru.com/pt-br/atualizacoes-mensais.html"',
        ),
        "atualizacoes-semanais.html": (
            'hreflang="pt-br" href="https://osrsguru.com/pt-br/weekly-updates.html"',
            'hreflang="pt-br" href="https://osrsguru.com/pt-br/atualizacoes-semanais.html"',
        ),
    }

    count = 0
    for fname, (old_str, new_str) in hub_fixes.items():
        fp = os.path.join(BASE, fname)
        if not os.path.isfile(fp):
            print(f"    [警告] 文件不存在: {fname}")
            continue

        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        if old_str in content:
            content = content.replace(old_str, new_str)
            count += 1
        else:
            print(f"    [警告] 未找到目标字符串: {fname} -> {old_str[:60]}...")
            continue

        # x-default 修复: 对于前 6 个文件，将 x-default 从 pt-br URL 改为 en URL
        if fname not in ("atualizacoes-mensais.html", "atualizacoes-semanais.html"):
            # 提取正确的 en URL（去除 /pt-br 前缀）
            en_url = new_str.split('href="')[1].rstrip('"')
            # 获取此文件的正确 en path
            en_path = en_url.replace("https://osrsguru.com", "")
            old_x_default = 'hreflang="x-default" href="https://osrsguru.com/pt-br' + en_path[1:] + '"'
            new_x_default = f'hreflang="x-default" href="https://osrsguru.com{en_path}"'

            if old_x_default in content:
                content = content.replace(old_x_default, new_x_default)

        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  P0-2: 修复 {count} 个 hub 页面 hreflang")

# ============================================================
# P0-3: comunidade.html 缺 hreflang
# ============================================================
def fix_p0_3():
    fp = os.path.join(BASE, "comunidade.html")
    if not os.path.isfile(fp):
        print("  P0-3: [警告] comunidade.html 不存在")
        return

    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    hreflang_block = (
        '<link rel="alternate" hreflang="en" href="https://osrsguru.com/community.html">\n'
        '<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/comunidade.html">\n'
        '<link rel="alternate" hreflang="x-default" href="https://osrsguru.com/community.html">'
    )

    if 'rel="alternate"' in content:
        print("  P0-3: comunidade.html 已有 hreflang，跳过")
        return

    head_close = content.find("</head>")
    if head_close >= 0:
        content = content[:head_close] + "\n" + hreflang_block + "\n" + content[head_close:]
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print("  P0-3: 修复 1 个页面 (comunidade.html 添加 hreflang)")
    else:
        print("  P0-3: [错误] 未找到 </head>")

# ============================================================
# P0-4: 194 篇 guides 导航标签英文 → 葡语
# 注意：只替换 <a ...>标签内容</a> 中的显示文字
# ============================================================
def fix_p0_4():
    label_map = {
        ">Home<": ">Início<",
        ">Money<": ">Lucro<",
        ">Bosses<": ">Chefes<",
        ">Quests<": ">Missões<",
        ">Skills<": ">Habilidades<",
        ">Updates<": ">Atualizações<",
        ">Chinese<": ">Chinês<",
    }

    guide_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    count = 0

    for fp in guide_files:
        with open(fp, "r", encoding="utf-8") as f:
            original = f.read()

        modified = original
        changed = False
        for en_label, pt_label in label_map.items():
            if en_label in modified:
                modified = modified.replace(en_label, pt_label)
                changed = True

        if changed:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(modified)
            count += 1

    print(f"  P0-4: 修复 {count} 篇 guides 导航标签 (英文→葡语)")

# ============================================================
# P0-5: ~20 篇 guides 导航链接文件名错误
# href="../boss-guides.html" → href="../chefes.html" 等
# ============================================================
def fix_p0_5():
    href_map = {
        'href="../boss-guides.html"': 'href="../chefes.html"',
        'href="../money-making.html"': 'href="../lucro.html"',
        'href="../quest-guides.html"': 'href="../missoes.html"',
        'href="../skill-training.html"': 'href="../habilidades.html"',
        'href="../monthly-updates.html"': 'href="../atualizacoes-mensais.html"',
    }

    guide_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    count = 0

    for fp in guide_files:
        with open(fp, "r", encoding="utf-8") as f:
            original = f.read()

        modified = original
        changed = False
        for old_href, new_href in href_map.items():
            if old_href in modified:
                modified = modified.replace(old_href, new_href)
                changed = True

        if changed:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(modified)
            count += 1

    print(f"  P0-5: 修复 {count} 篇 guides 导航链接文件名")

# ============================================================
# P0-6: 2 个文件面包屑 "中文版" → "Versão Chinesa"
# ============================================================
def fix_p0_6():
    files = [
        "guides/vault-of-ralos-raid-guide-2026.html",
        "guides/osrs-hunter-training-guide-2026.html",
    ]

    count = 0
    for rel_path in files:
        fp = os.path.join(BASE, rel_path)
        if not os.path.isfile(fp):
            print(f"    [警告] 文件不存在: {rel_path}")
            continue

        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        # 只替换 >中文版< 这样的链接文字
        old_text = ">中文版<"
        new_text = ">Versão Chinesa<"

        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
        else:
            print(f"    [警告] 未找到 '中文版': {rel_path}")

    print(f"  P0-6: 修复 {count} 个文件面包屑 (中文版→Versão Chinesa)")


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("pt-br P0 修复脚本")
    print(f"工作目录: {BASE}")
    print("=" * 60)

    print("\n[P0-1] 修复 guides hreflang (201篇)...")
    fix_p0_1()

    print("\n[P0-2] 修复 hub 页面 hreflang (8个)...")
    fix_p0_2()

    print("\n[P0-3] 修复 comunidade.html hreflang...")
    fix_p0_3()

    print("\n[P0-4] 修复 guides 导航标签 (英文→葡语)...")
    fix_p0_4()

    print("\n[P0-5] 修复 guides 导航链接文件名...")
    fix_p0_5()

    print("\n[P0-6] 修复面包屑 (中文版→Versão Chinesa)...")
    fix_p0_6()

    print("\n" + "=" * 60)
    print("所有 P0 修复完成!")
    print("=" * 60)
