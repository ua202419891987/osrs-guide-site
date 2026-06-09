#!/usr/bin/env python3
"""
OSRS Guru 内链批量修复脚本 v2
功能：修复 Related Guides 区块（最可靠、最大 SEO 效果）
使用：python3 fix_related_guides.py --dry-run
      python3 fix_related_guides.py
"""

import re
import os
import sys
import argparse
from pathlib import Path

# ========== 每篇文章的 Related Guides 推荐 ==========
# key = 当前文章文件名，value = 推荐文章列表（按优先级排序）
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
    """从 HTML 文件中提取标题（h1 或 title）"""
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

def build_related_section(file_list):
    """根据文件名列表生成 Related Guides HTML 区块"""
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
        # 清理标题
        title = re.sub(r"\(2026\)|–.*|\|.*", "", title).strip()
        lines.append(f'                    <li><a href="{fname}">{title}</a></li>')
    lines.append('                </ul>')
    lines.append('            </section>')
    return "\n".join(lines)

def fix_related_guides_in_file(filepath, dry_run=False):
    """修复单个文件的 Related Guides 区块"""
    filename = filepath.name
    if filename not in RELATED_MAP:
        return False, "not_in_map"

    content = filepath.read_text(encoding="utf-8")
    recommended = RELATED_MAP[filename]

    # 检查是否已有 Related Guides 区块
    has_related = '<section class="related-guides">' in content or '<!-- Related Guides -->' in content

    # 检查现有链接
    existing = set(re.findall(r'<li><a href="([^"]+)"', content))
    to_add = [f for f in recommended if f not in existing and (GUIDES_DIR / f).exists()]

    new_block = build_related_section(recommended)

    if has_related:
        # 替换现有区块
        new_content = re.sub(
            r'(?<=<!-- Related Guides -->\s*<section class="related-guides">).*?(?=</section>\s*(?:<!--|<\/div>|<div class="inline-support-hint"|</main>))',
            new_block.split('<section class="related-guides">')[1].replace('</section>', '', 1).rsplit('</section>', 1)[0],
            content,
            flags=re.DOTALL
        )
        # 更安全的替换：直接替换整个区块
        new_content = re.sub(
            r'(<!-- Related Guides -->.*?</section>)',
            new_block,
            content,
            flags=re.DOTALL
        )
    else:
        # 在 support-card 或 inline-support-hint 前插入
        insert_before = r'(<div class="inline-support-hint"|<div class="support-card")'
        if re.search(insert_before, content):
            new_content = re.sub(
                insert_before,
                new_block + "\n\n            ",
                content,
                count=1
            )
        else:
            print(f"  [WARN] Could not find insertion point for {filename}")
            return False, "no_insert_point"

    if new_content == content and to_add == []:
        return False, "no_change"

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [OK] Updated Related Guides: {filename}")
        if to_add:
            print(f"       Added links: {to_add}")
    else:
        print(f"  [DRY-RUN] Would update: {filename}")
        if to_add:
            print(f"       Would add links: {to_add}")

    return True, "updated"

def main():
    parser = argparse.ArgumentParser(description="OSRS Guru Related Guides 批量修复")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不修改文件")
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

    mode = "DRY-RUN (no changes)" if args.dry_run else "EXECUTE (will modify files)"
    print(f"[START] Mode: {mode}")
    print(f"[INFO] Files to process: {len(files)}")
    print("=" * 60)

    updated = 0
    skipped = 0
    for f in sorted(files):
        print(f"\n  Processing: {f.name}")
        changed, reason = fix_related_guides_in_file(f, dry_run=args.dry_run)
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
