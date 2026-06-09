#!/usr/bin/env python3
"""
OSRS Guru 内链批量修复脚本
功能：
  1. 根据关键词→文件名映射，在正文第一段/段落中自动加入上下文内链
  2. 修复 Related Guides 区块（移除无效项，添加有效链接）
  3. 支持 dry-run 模式预览修改

使用方法：
  python3 add_internal_links.py --dry-run    # 预览
  python3 add_internal_links.py               # 执行
"""

import re
import os
import sys
import argparse
from pathlib import Path
from html.parser import HTMLParser

# ========== 关键词 → 目标文件映射 ==========
# 当正文中出现这些关键词时，自动添加内链（只加第一次出现）
KEYWORD_MAP = {
    # 战斗/技能类
    "Slayer": "slayer-1-99-guide-2026.html",
    "slayer": "slayer-1-99-guide-2026.html",
    "combat training": "osrs-combat-training-beginner-2026.html",
    "combat": "osrs-combat-training-beginner-2026.html",
    "Attack": "osrs-fastest-99-attack-strength-defence.html",
    "Strength": "osrs-fastest-99-attack-strength-defence.html",
    "Defence": "osrs-fastest-99-attack-strength-defence.html",
    "Magic": "osrs-1-99-magic-training-cheap-guide-2026.html",
    "Ranged": "osrs-1-99-ranged-guide-2026.html",
    "Hitpoints": "osrs-1-99-hitpoints-guide-2026.html",
    "Hitpoint": "osrs-1-99-hitpoints-guide-2026.html",
    "quest": "osrs-questing-beginner-guide-2026.html",
    "Quest": "osrs-questing-beginner-guide-2026.html",
    "Waterfall Quest": "osrs-questing-beginner-guide-2026.html",
    "Nightmare Zone": "osrs-nightmare-phosanis-guide-2026.html",
    "NMZ": "osrs-nightmare-phosanis-guide-2026.html",
    # 赚钱/新手类
    "money making": "osrs-money-making-beginner-2026.html",
    "Money Making": "osrs-money-making-beginner-2026.html",
    "Grand Exchange": "osrs-money-making-beginner-2026.html",
    "GE": "osrs-money-making-beginner-2026.html",
    "beginner": "osrs-new-player-guide-2026.html",
    "Beginner": "osrs-new-player-guide-2026.html",
    "new player": "osrs-new-player-guide-2026.html",
    "New Player": "osrs-new-player-guide-2026.html",
    "Ironman": "osrs-ironman-money-making-f2p-2026.html",
    "ironman": "osrs-ironman-money-making-f2p-2026.html",
    # 装备/道具类
    "gear": "osrs-gear-beginner-guide-2026.html",
    "Gear": "osrs-gear-beginner-guide-2026.html",
    "Bank": "osrs-bank-inventory-management-2026.html",
    "bank": "osrs-bank-inventory-management-2026.html",
    "Inventory": "osrs-bank-inventory-management-2026.html",
    "inventory": "osrs-bank-inventory-management-2026.html",
}

# ========== 每篇文章的 Related Guides 推荐链接 ==========
# key = 当前文章文件名，value = 推荐的相关文章列表
RELATED_GUIDES = {
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
}

GUIDES_DIR = Path(__file__).parent / "guides"

def get_title_from_file(filepath):
    """从 HTML 文件中提取 <h1> 或 <title> 作为文章标题"""
    try:
        content = filepath.read_text(encoding="utf-8")
        # 优先找 h1
        m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
        if m:
            return re.sub(r"<[^>]+>", "", m.group(1)).strip()
        # 其次找 title
        m = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return filepath.stem.replace("-", " ").title()

def add_contextual_links(content, filename):
    """
    在正文段落中添加上下文内链。
    规则：
    1. 只在 <p> 标签内的文字添加（不碰 <h*>, <li>, <th>, <td> 里的）
    2. 每个关键词只加第一次出现
    3. 不破坏已有的 <a> 标签
    """
    # 找到 <main> 正文区域（在 guide-content 后的 <p> 标签）
    # 简单策略：找到第一个 <p> 标签后，在接下来的 3 个 <p> 里加链接
    links_added = set()  # 已添加的关键词，避免重复

    def replace_in_p(match):
        p_content = match.group(1)  # <p>...</p> 内部内容
        modified = p_content
        for keyword, target_file in KEYWORD_MAP.items():
            # 跳过：指向自己的链接
            if target_file == filename:
                continue
            # 跳过：已经加过的关键词
            if keyword in links_added:
                continue
            # 检查目标文件是否存在
            if not (GUIDES_DIR / target_file).exists():
                continue
            # 不在已有 <a> 标签内添加
            if f'<a href="{target_file}"' in modified:
                continue
            # 只替换第一个出现（不在标签内的）
            # 使用负向断言：不在 > 和 < 之间的（即不在标签内）
            pattern = r"(?<![>\"])" + re.escape(keyword) + r"(?![^<]*</a>)"
            # 更安全的做法：只替换不在 <a> 标签内的第一次出现
            # 简化：直接替换第一次出现，如果它不在 <a>...</a> 内
            def safe_replace(m):
                word = m.group(0)
                # 检查这个匹配是否在 <a> 标签内
                # 简化：只替换第一个不在标签内的
                return f'<a href="../guides/{target_file}" style="color:#d4af37;">{word}</a>'
            if keyword in modified and f'<a href="' not in modified.split(keyword)[0].split(">")[-1]:
                # 只在第一个 <p> 里加 1-2 个链接，避免过多
                if len(links_added) < 3:
                    modified = modified.replace(keyword, f'<a href="../guides/{target_file}" style="color:#d4af37;">{keyword}</a>', 1)
                    links_added.add(keyword)
        return "<p>" + modified + "</p>"

    # 只处理 guide-content 里的 <p> 标签（前 5 个）
    # 找到 guide-content 区域
    gc_match = re.search(r'(<main class="guide-content">.*?)(?=<div class="related-guides"|<div class="inline-support-hint"|<footer|</main>)', content, re.DOTALL)
    if not gc_match:
        return content, []

    prefix = content[:content.index(gc_match.group(1))]
    body = gc_match.group(1)
    suffix_start = content.index(gc_match.group(1)) + len(gc_match.group(1))
    suffix = content[suffix_start:]

    # 在 body 里找前 5 个 <p> 标签，加内链
    p_count = 0
    def process_p(m):
        nonlocal p_count
        if p_count >= 5:
            return m.group(0)
        p_count += 1
        return replace_in_p(m)

    new_body = re.sub(r"<p>(.*?)</p>", process_p, body, count=5, flags=re.DOTALL)
    added = list(links_added)
    return prefix + new_body + suffix, added

def fix_related_guides(content, filename):
    """
    修复 Related Guides 区块：
    1. 移除纯文本项（没有 <a> 标签的 <li>）
    2. 添加推荐的相关文章链接（如果还没有）
    """
    if filename not in RELATED_GUIDES:
        return content, []

    recommended = RELATED_GUIDES[filename]
    existing_links = set(re.findall(r'<li><a href="([^"]+)"', content))
    to_add = [f for f in recommended if f not in existing_links and (GUIDES_DIR / f).exists()]

    # 构建新的 Related Guides 区块
    related_section = """            <!-- Related Guides -->
            <section class="related-guides">
                <h2>Related Guides</h2>
                <ul>
"""
    for f in recommended:
        if not (GUIDES_DIR / f).exists():
            continue
        title = get_title_from_file(GUIDES_DIR / f)
        # 简化标题
        title = re.sub(r"\(2026\)|–.*|\|.*", "", title).strip()
        related_section += f'                    <li><a href="{f}">{title}</a></li>\n'
    related_section += """                </ul>
            </section>
"""

    # 替换旧的 Related Guides 区块
    new_content = re.sub(
        r'(\s*<!-- Related Guides -->.*?</section>\s*)(?=<div class="inline-support-hint"|</main>)',
        related_section,
        content,
        flags=re.DOTALL
    )
    if new_content == content:
        # 尝试另一种匹配
        new_content = re.sub(
            r'(<section class="related-guides">.*?</section>)',
            related_section.strip(),
            content,
            flags=re.DOTALL
        )
    return new_content, to_add

def process_file(filepath, dry_run=False):
    """处理单个文件"""
    filename = filepath.name
    print(f"\n📄 Processing: {filename}")
    results = {"contextual": [], "related": []}

    try:
        content = filepath.read_text(encoding="utf-8")
        original = content

        # Step 1: 添加正文上下文内链
        content, added = add_contextual_links(content, filename)
        results["contextual"] = added
        if added:
            print(f"  + Added contextual links: {added}")

        # Step 2: 修复 Related Guides
        content, added_rg = fix_related_guides(content, filename)
        results["related"] = added_rg
        if added_rg:
            print(f"  + Updated Related Guides: {added_rg}")

        # 写回文件
        if not dry_run and content != original:
            filepath.write_text(content, encoding="utf-8")
            print(f"  ✅ Saved: {filename}")
        elif content == original:
            print(f"  ⏭  No changes needed")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return results

def main():
    parser = argparse.ArgumentParser(description="OSRS Guru 内链批量修复脚本")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改文件")
    parser.add_argument("--file", type=str, help="只处理指定文件（文件名）")
    args = parser.parse_args()

    guides_dir = GUIDES_DIR
    if not guides_dir.exists():
        print(f"❌ Error: {guides_dir} not found!")
        sys.exit(1)

    files = list(guides_dir.glob("*.html"))
    if args.file:
        files = [f for f in files if f.name == args.file]
        if not files:
            print(f"❌ File not found: {args.file}")
            sys.exit(1)

    print(f"{'[DRY RUN] 预览模式 — 不修改文件' if args.dry_run else '[EXECUTE] 执行模式 — 将修改文件'}")
    print(f"[INFO] Found {len(files)} HTML files")
    print("=" * 60)

    total_contextual = 0
    total_related = 0
    for f in sorted(files):
        results = process_file(f, dry_run=args.dry_run)
        total_contextual += len(results["contextual"])
        total_related += len(results["related"])

    print("\n" + "=" * 60)
    print(f"✅ Done! Contextual links added: {total_contextual}")
    print(f"✅ Related Guides updated: {total_related}")
    if args.dry_run:
        print("\n💡 移除 --dry-run 参数来实际执行修改")

if __name__ == "__main__":
    main()
