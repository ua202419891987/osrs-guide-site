#!/usr/bin/env python3
"""
OSRS Guru Related Guides 批量修复脚本 v3
方法：纯字符串操作（无复杂regex），稳定可靠
使用：python3 fix_rg_v3.py --dry-run
      python3 fix_rg_v3.py
"""

import re
import os
import sys
import argparse
from pathlib import Path

# ========== 每篇文章的 Related Guides 推荐 ==========
RELATED_MAP = {
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
    "osrs-maps-travel-guide-2026.html": [
        "osrs-new-player-guide-2026.html",
        "osrs-questing-beginner-guide-2026.html",
        "osrs-combat-training-beginner-2026.html",
        "osrs-money-making-beginner-2026.html",
    ],
    "osrs-skills-overview-beginner-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-1-99-hitpoints-guide-2026.html",
        "osrs-1-99-magic-training-cheap-guide-2026.html",
        "slayer-1-99-guide-2026.html",
    ],
    "osrs-interface-controls-beginner-guide-2026.html": [
        "osrs-new-player-guide-2026.html",
        "osrs-combat-training-beginner-2026.html",
        "osrs-gear-beginner-guide-2026.html",
    ],
    "osrs-combat-triangle-explained-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-1-99-hitpoints-guide-2026.html",
    ],
    "osrs-safe-spots-beginner-2026.html": [
        "osrs-combat-training-beginner-2026.html",
        "slayer-1-99-guide-2026.html",
        "osrs-1-99-hitpoints-guide-2026.html",
    ],
}

GUIDES_DIR = Path(__file__).parent / "guides"

def get_title_from_file(filepath):
    try:
        content = filepath.read_text(encoding="utf-8")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
        if m:
            return re.sub(r"<[^>]+>", "", m.group(1)).strip()
        m = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return filepath.stem.replace("-", " ").title()

def build_related_html(file_list):
    """生成 Related Guides HTML 区块"""
    lines = []
    lines.append('            <!-- Related Guides -->')
    lines.append('            <section class="related-guides">')
    lines.append('                <h2>Related Guides</h2>')
    lines.append('                <ul>')
    for fname in file_list:
        fpath = GUIDES_DIR / fname
        if not fpath.exists():
            continue
        title = get_title_from_file(fpath)
        title = re.sub(r"\(2026\)|–.*|\|.*", "", title).strip()
        lines.append(f'                    <li><a href="{fname}">{title}</a></li>')
    lines.append('                </ul>')
    lines.append('            </section>')
    return "\n".join(lines)

def fix_file(filepath, dry_run=False):
    filename = filepath.name
    if filename not in RELATED_MAP:
        return False, "skip"

    content = filepath.read_text(encoding="utf-8")
    original = content
    new_block = build_related_html(RELATED_MAP[filename])

    # 方法1：替换已有的 Related Guides 区块
    marker_start = "<!-- Related Guides -->"
    if marker_start in content:
        idx_start = content.index(marker_start)
        # 找结束的 </section>
        idx_end = content.index("</section>", idx_start) + len("</section>")
        content = content[:idx_start] + new_block + content[idx_end:]
        print(f"  [OK] Replaced Related Guides: {filename}")
    else:
        # 方法2：在 inline-support-hint 或 support-card 前插入
        insert_markers = ['<div class="inline-support-hint">', '<div class="support-card"']
        inserted = False
        for marker in insert_markers:
            if marker in content:
                idx = content.index(marker)
                content = content[:idx] + new_block + "\n\n            " + content[idx:]
                print(f"  [OK] Inserted Related Guides: {filename}")
                inserted = True
                break
        if not inserted:
            print(f"  [WARN] No insert point found: {filename}")
            return False, "no_insert_point"

    if content != original:
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
            print(f"  [SAVED] {filename}")
        else:
            print(f"  [DRY-RUN] Would update: {filename}")
        return True, "updated"
    else:
        print(f"  [SKIP] No change: {filename}")
        return False, "no_change"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", type=str, help="只处理指定文件")
    args = parser.parse_args()

    if not GUIDES_DIR.exists():
        print(f"[ERROR] Directory not found: {GUIDES_DIR}")
        sys.exit(1)

    files = [f for f in GUIDES_DIR.glob("*.html") if f.name in RELATED_MAP]
    if args.file:
        files = [f for f in files if f.name == args.file]
        if not files:
            print(f"[ERROR] File not in mapping: {args.file}")
            sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else "EXECUTE"
    print(f"[START] Mode: {mode}")
    print(f"[INFO] Files to process: {len(files)}")
    print("=" * 60)

    updated = 0
    skipped = 0
    for f in sorted(files):
        print(f"\n  File: {f.name}")
        changed, reason = fix_file(f, dry_run=args.dry_run)
        if changed:
            updated += 1
        else:
            skipped += 1

    print("\n" + "=" * 60)
    print(f"[DONE] Updated: {updated}, Skipped: {skipped}")
    if args.dry_run:
        print("\n[INFO] Remove --dry-run to apply changes")

if __name__ == "__main__":
    main()
