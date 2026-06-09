#!/usr/bin/env python3
"""
OSRS Guru - Related Guides 批量修复（极简版）
只做一件事：用字符串替换，修复 Related Guides 区块
用法：python3 fix_rg_simple.py --dry-run
      python3 fix_rg_simple.py
"""

import sys
from pathlib import Path

GUIDES_DIR = Path(__file__).parent / "guides"

# 每篇文章的推荐 Related Guides（按优先级）
MAP = {
    "osrs-1-99-hitpoints-guide-2026.html": [
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-1-99-magic-training-cheap-guide-2026.html",
        "slayer-1-99-guide-2026.html",
        "osrs-combat-training-beginner-2026.html",
    ],
    "osrs-money-making-beginner-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-questing-beginner-guide-2026.html",
        "osrs-gear-beginner-guide-2026.html",
        "osrs-new-player-guide-2026.html",
    ],
    "osrs-combat-training-beginner-2026.html": [
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-1-99-hitpoints-guide-2026.html",
        "osrs-1-99-magic-training-cheap-guide-2026.html",
        "slayer-1-99-guide-2026.html",
    ],
    "osrs-new-player-guide-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-money-making-beginner-2026.html",
        "osrs-questing-beginner-guide-2026.html",
        "osrs-gear-beginner-guide-2026.html",
    ],
    "slayer-1-99-guide-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-1-99-hitpoints-guide-2026.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-questing-beginner-guide-2026.html",
    ],
    "osrs-questing-beginner-guide-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-money-making-beginner-2026.html",
        "slayer-1-99-guide-2026.html",
        "osrs-new-player-guide-2026.html",
    ],
    "osrs-gear-beginner-guide-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-1-99-magic-training-cheap-guide-2026.html",
        "osrs-bank-inventory-management-2026.html",
    ],
    "osrs-fastest-99-attack-strength-defence.html": [
        "osrs-1-99-hitpoints-guide-2026.html",
        "osrs-combat-training-beginner-2026.html",
        "osrs-1-99-magic-training-cheap-guide-2026.html",
        "slayer-1-99-guide-2026.html",
    ],
    "osrs-1-99-magic-training-cheap-guide-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-1-99-hitpoints-guide-2026.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "slayer-1-99-guide-2026.html",
    ],
    "osrs-bank-inventory-management-2026.html": [
        "osrs-gear-beginner-guide-2026.html",
        "osrs-combat-training-beginner-2026.html",
        "osrs-money-making-beginner-2026.html",
        "osrs-new-player-guide-2026.html",
    ],
}

# 生成 Related Guides HTML 区块
def make_block(file_list):
    lines = [
        '            <!-- Related Guides -->',
        '            <section class="related-guides">',
        '                <h2>Related Guides</h2>',
        '                <ul>',
    ]
    for fname in file_list:
        fpath = GUIDES_DIR / fname
        if not fpath.exists():
            continue
        # 从文件读取标题
        try:
            c = fpath.read_text(encoding="utf-8")
            import re
            m = re.search(r"<h1[^>]*>(.*?)</h1>", c, re.DOTALL)
            title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else fname
        except Exception:
            title = fname.replace("-", " ").replace(".html", "")
        # 简化标题
        for suffix in ["(2026)", "– Complete", "– Best", "Guide "]:
            title = title.replace(suffix, "")
        title = title.strip()
        lines.append(f'                    <li><a href="{fname}">{title}</a></li>')
    lines += [
        '                </ul>',
        '            </section>',
    ]
    return "\n".join(lines)

def fix_file(filepath, dry_run):
    name = filepath.name
    if name not in MAP:
        return False

    content = filepath.read_text(encoding="utf-8")
    new_block = make_block(MAP[name])

    # 查找并替换 Related Guides 区块
    # 方法：找到 <!-- Related Guides --> 直到下一个 </section>
    start_tag = "<!-- Related Guides -->"
    if start_tag not in content:
        print(f"  [SKIP] No Related Guides block found: {name}")
        return False

    idx_start = content.index(start_tag)
    # 从 idx_start 开始找 </section>
    idx_end = content.index("</section>", idx_start) + len("</section>")

    new_content = content[:idx_start] + new_block + content[idx_end:]

    if new_content == content:
        print(f"  [SKIP] No change needed: {name}")
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would update: {name}")
    else:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [OK] Updated: {name}")
    return True

def main():
    dry_run = "--dry-run" in sys.argv
    mode = "DRY-RUN" if dry_run else "EXECUTE"
    print(f"[START] Mode: {mode}")
    print(f"[INFO] Mapping has {len(MAP)} articles")
    print("=" * 60)

    updated = 0
    skipped = 0
    for fname in sorted(MAP.keys()):
        fpath = GUIDES_DIR / fname
        if not fpath.exists():
            print(f"[WARN] File not found: {fname}")
            skipped += 1
            continue
        print(f"\n  Processing: {fname}")
        changed = fix_file(fpath, dry_run)
        if changed:
            updated += 1
        else:
            skipped += 1

    print("\n" + "=" * 60)
    print(f"[DONE] Updated: {updated}, Skipped: {skipped}")
    if dry_run:
        print("\n[INFO] Remove --dry-run to apply changes")

if __name__ == "__main__":
    main()
