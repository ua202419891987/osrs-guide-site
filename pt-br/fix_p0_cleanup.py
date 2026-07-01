#!/usr/bin/env python3
"""清理 P0-1 修复后仍有重复 hreflang 的文件"""

import os
import re
import glob

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\pt-br\guides"

def fix_duplicate_hreflangs():
    guide_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    total_fixed = 0

    for fp in guide_files:
        fname = os.path.basename(fp)
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        hreflang_count = len(re.findall(r'hreflang=', content))
        if hreflang_count == 4:
            continue  # 正确，跳过

        # 需要修复：移除 ALL hreflang 行（不管缩进），重新插入 4 行
        target_block = (
            f'<link rel="alternate" hreflang="en" href="https://osrsguru.com/guides/{fname}">\n'
            f'<link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/guides/{fname}">\n'
            f'<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/guides/{fname}">\n'
            f'<link rel="alternate" hreflang="x-default" href="https://osrsguru.com/guides/{fname}">'
        )

        # 删除所有 hreflang 行（含前后的空白换行）
        # 匹配: 可选的空白 + <link rel="alternate" hreflang=...> + 可选的换行
        original = content
        content = re.sub(
            r'[ \t]*<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"[^>]*>\s*\n?',
            '',
            content
        )

        # 检查清理后是否真的移除了所有 hreflang
        remaining = len(re.findall(r'hreflang=', content))
        if remaining > 0:
            print(f"  [警告] {fname}: 仍有 {remaining} 个 hreflang 残留，尝试更激进方式")
            # 逐行删除
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if 'rel="alternate"' in line and 'hreflang=' in line:
                    continue
                new_lines.append(line)
            content = '\n'.join(new_lines)

        # 插入新的 hreflang
        head_close = content.find("</head>")
        if head_close >= 0:
            # 找 </head> 前的最后一个位置，插入前确保换行正确
            # 清理前导空白行
            before = content[:head_close].rstrip()
            after = content[head_close:]
            content = before + "\n" + target_block + "\n" + after
        else:
            print(f"  [错误] {fname}: 未找到 </head>")
            continue

        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)

        # 验证
        new_count = len(re.findall(r'hreflang=', content))
        total_fixed += 1
        print(f"  修复 {fname}: {hreflang_count} → {new_count} 个 hreflang")

    print(f"\n总计修复 {total_fixed} 个文件的重複 hreflang")

if __name__ == "__main__":
    fix_duplicate_hreflangs()
