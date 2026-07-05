#!/usr/bin/env python3
"""
Batch update Chinese (zh/guides/) beginner guides:
1. Add cn-title and cn-summary to hero section
2. Add Chinese annotations to TOC items
3. Add Chinese annotations to h2/h3 headings
4. Copy 30S Quick Preview from English version
"""

import re
import os
import shutil

BASE = r"C:\Users\Lenovo\osrs-guide-site"

FILES = [
    "osrs-1-99-mining-guide-beginner-2026.html",
    "osrs-all-skills-overview-guide-2026.html",
    "osrs-cheap-flipping-methods-new-players.html",
    "osrs-combat-training-beginner-2026.html",
    "osrs-diary-priority-order-beginner-2026.html",
    "osrs-efficient-training-routes-beginners-2026.html",
    "osrs-f2p-combat-training-guide-2026.html",
    "osrs-f2p-ironman-money-making-early-game.html",
    "osrs-f2p-leveling-guide-2026.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-quests-before-membership-2026.html",
    "osrs-f2p-to-member-first-10-things-2026.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
    "osrs-fastest-99-cooking-f2p.html",
    "osrs-first-boss-progression-roadmap-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
    "osrs-how-to-beat-zulrah-beginners-rotation.html",
    "osrs-how-to-solo-god-wars-boss-for-beginners.html",
    "osrs-how-to-train-prayer-cheap-f2p.html",
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-low-effort-money-making-beginners.html",
    "osrs-members-vs-f2p-comparison-2026.html",
    "osrs-money-making-beginner-2026.html",
    "osrs-nmz-beginner-guide-2026.html",
    "osrs-obor-bryophyta-f2p-boss-guide-2026.html",
    "osrs-prayer-training-beginner-guide-2026.html",
    "osrs-skills-overview-beginner-2026.html",
    "osrs-skill-training-beginner-complete-guide-2026.html",
    "osrs-skill-training-beginner-fast-track-2026.html",
    "osrs-slayer-beginner-first-master-guide-2026.html",
    "osrs-slayer-beginner-guide-2026.html",
    "osrs-toa-solo-beginner-guide-2026.html",
    "osrs-top-10-skills-to-train-first-2026.html",
]


def get_h1_title(html):
    """Extract the first h1 title from HTML."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    if m:
        return m.group(1).strip()
    return None


def add_cn_hero(html, filename):
    """Add cn-title and cn-summary before first h1 if missing."""
    if 'cn-title' in html:
        return html  # Already has it
    
    h1_en = get_h1_title(html)
    if not h1_en:
        return html
    
    # Generate Chinese title from filename/English title
    cn_title_map = {
        "osrs-1-99-mining-guide-beginner-2026.html": "OSRS 采矿1-99完整指南 — 新手采矿训练攻略（2026版）",
        "osrs-all-skills-overview-guide-2026.html": "OSRS 全技能概览指南 — 新手完整参考（2026版）",
        "osrs-cheap-flipping-methods-new-players.html": "OSRS 低成本倒卖方法 — 新手赚金币入门（2026版）",
        "osrs-combat-training-beginner-2026.html": "OSRS 战斗训练指南 — 新手战斗技能提升（2026版）",
        "osrs-diary-priority-order-beginner-2026.html": "OSRS 成就日记优先级 — 新手最佳顺序（2026版）",
        "osrs-efficient-training-routes-beginners-2026.html": "OSRS 高效训练路线 — 新手分步指南（2026版）",
        "osrs-f2p-combat-training-guide-2026.html": "OSRS F2P战斗训练指南 — 免费玩家战斗升级（2026版）",
        "osrs-f2p-ironman-money-making-early-game.html": "OSRS F2P铁人早期赚钱 — 零成本起步（2026版）",
        "osrs-f2p-leveling-guide-2026.html": "OSRS F2P升级指南 — 免费玩家完整路线（2026版）",
        "osrs-f2p-money-making-first-bond-2026.html": "OSRS F2P赚钱买第一张Bond — 免费玩家指南（2026版）",
        "osrs-f2p-money-making-no-stats.html": "OSRS F2P零属性赚钱方法 — 无需任何技能等级",
        "osrs-f2p-quests-before-membership-2026.html": "OSRS 加入会员前必做F2P任务 — 新手任务清单（2026版）",
        "osrs-f2p-to-member-first-10-things-2026.html": "OSRS F2P转会员后必做的10件事 — 新手入门（2026版）",
        "osrs-farming-herb-runs-beginner-guide-2026.html": "OSRS  farming与草药种植 — 新手草药种植指南（2026版）",
        "osrs-fastest-99-cooking-f2p.html": "OSRS F2P最快烹饪99级 — 免费玩家烹饪全攻略",
        "osrs-first-boss-progression-roadmap-2026.html": "OSRS 首个Boss进阶路线图 — 新手Boss攻略（2026版）",
        "osrs-flipping-guide-beginners-2026.html": "OSRS 倒卖指南 — 新手交易所赚钱入门（2026版）",
        "osrs-how-to-beat-zulrah-beginners-rotation.html": "OSRS Zulrah击败指南 — 新手旋转模式攻略",
        "osrs-how-to-solo-god-wars-boss-for-beginners.html": "OSRS 单人God Wars Boss — 新手独立攻略",
        "osrs-how-to-train-prayer-cheap-f2p.html": "OSRS F2P廉价训练祷告 — 免费玩家祈祷升级",
        "osrs-ironman-money-making-f2p-2026.html": "OSRS 铁人模式F2P赚钱 — 免费铁人经济指南（2026版）",
        "osrs-low-effort-money-making-beginners.html": "OSRS 低投入赚钱方法 — 新手轻松赚金币",
        "osrs-members-vs-f2p-comparison-2026.html": "OSRS 会员vs免费对比 — 是否值得成为会员？（2026版）",
        "osrs-money-making-beginner-2026.html": "OSRS 新手赚钱指南 — 从零开始赚金币（2026版）",
        "osrs-nmz-beginner-guide-2026.html": "OSRS NMZ新手指南 — 梦魇地带训练攻略",
        "osrs-obor-bryophyta-f2p-boss-guide-2026.html": "OSRS F2P Boss指南 — Obor与Bryophyta攻略",
        "osrs-prayer-training-beginner-guide-2026.html": "OSRS 祷告训练新手指南 — 祈祷技能升级（2026版）",
        "osrs-skills-overview-beginner-2026.html": "OSRS 技能概览新手指南 — 全方位技能介绍（2026版）",
        "osrs-skill-training-beginner-complete-guide-2026.html": "OSRS 技能训练完整指南 — 新手全技能攻略（2026版）",
        "osrs-skill-training-beginner-fast-track-2026.html": "OSRS 技能训练快速通道 — 新手高效升级路线（2026版）",
        "osrs-slayer-beginner-first-master-guide-2026.html": "OSRS 杀戮新手入门 — 第一位大师指南",
        "osrs-slayer-beginner-guide-2026.html": "OSRS 杀戮技能新手指南 — Slayer入门全攻略（2026版）",
        "osrs-toa-solo-beginner-guide-2026.html": "OSRS TOA单人新手指南 — 废墟之墓入门攻略",
        "osrs-top-10-skills-to-train-first-2026.html": "OSRS 新手最优先训练的10个技能 — 高效开局（2026版）",
    }
    
    cn_title = cn_title_map.get(filename, f"OSRS {h1_en} — 中文攻略指南")
    
    # Summary map
    cn_summary_map = {
        "osrs-1-99-mining-guide-beginner-2026.html": "完整OSRS采矿1-99指南（2026版）：从锡/铜矿到紫水晶的多种方法，10K-70K经验/小时，50K-3M金币/小时利润，母亲矿脉AFK策略，从青铜到水晶镐子的完整升级路径。适合所有新老玩家。",
        "osrs-all-skills-overview-guide-2026.html": "2026年更新版：23个技能分为4大类别，每种技能提供3种训练方法（最快、最便宜、AFK）。从正确的5个技能开始，在通往满技能披风的路上节省100+小时。",
        "osrs-cheap-flipping-methods-new-players.html": "2026年更新：低成本倒卖方法，仅需10K金币起步。学习GE交易所的基础倒卖技巧，逐步积累财富。适合想从零开始学习经济系统的新手玩家。",
        "osrs-combat-training-beginner-2026.html": "完整OSRS战斗训练指南：从1级到99级，涵盖攻击、力量、防御、远程、魔法等战斗技能。包含最佳升级地点、装备推荐和经验数据对比。",
        "osrs-diary-priority-order-beginner-2026.html": "2026年成就日记优先级指南：从简单到精英，按最优顺序完成地区和任务成就，最大化奖励收益。",
        "osrs-efficient-training-routes-beginners-2026.html": "2026年高效训练路线：4周分步计划，从0级到战斗70+和10个关键技能目标，新手最佳成长路径。",
        "osrs-f2p-combat-training-guide-2026.html": "完整F2P战斗训练指南：了解免费玩家可用的最佳战斗训练方法、地点和装备选择，从新手到高手。",
        "osrs-f2p-ironman-money-making-early-game.html": "F2P铁人模式早期赚钱指南：零成本起步方法，利用有限资源最大化金币收入，为购买Bond做准备。",
        "osrs-f2p-leveling-guide-2026.html": "完整F2P升级路线（2026版）：免费玩家从1到99级的最佳技能训练路径，涵盖所有F2P可用技能。",
        "osrs-f2p-money-making-first-bond-2026.html": "2026年F2P赚钱买第一张会员Bond指南：一步步教你如何在免费版中赚够8.5M金币。",
        "osrs-f2p-money-making-no-stats.html": "无需任何技能等级的F2P赚钱方法：适合纯新手，零门槛起步赚取第一桶金。",
        "osrs-f2p-quests-before-membership-2026.html": "2026年加入会员前必做F2P任务清单：最大化免费版任务奖励，为会员生活做好充分准备。",
        "osrs-f2p-to-member-first-10-things-2026.html": "2026年F2P转会员后必做的10件事：最大化会员首日效率，快速适应会员生活。",
        "osrs-farming-herb-runs-beginner-guide-2026.html": "2026年Farming与草药种植新手指南：学习草药种植跑法、最佳种子选择、利润计算和1-99升级路线。",
        "osrs-fastest-99-cooking-f2p.html": "F2P最快烹饪99级攻略：免费玩家烹饪升级的最佳方法和最快路线，4-8小时达成99级。",
        "osrs-first-boss-progression-roadmap-2026.html": "2026年首个Boss进阶路线图：从低门槛Boss开始，逐步挑战更高难度，提升装备和技巧。",
        "osrs-flipping-guide-beginners-2026.html": "2026年倒卖指南：从基础到高级的GE交易所倒卖技巧，学习如何通过买卖差价赚取稳定利润。",
        "osrs-how-to-beat-zulrah-beginners-rotation.html": "Zulrah旋转模式新手攻略：详细图解Zulrah所有旋转模式的应对策略，适合初次挑战的玩家。",
        "osrs-how-to-solo-god-wars-boss-for-beginners.html": "单人God Wars Boss新手攻略：一步步教你如何独自挑战GWD四大Boss，包括装备推荐和战术详解。",
        "osrs-how-to-train-prayer-cheap-f2p.html": "F2P廉价训练祷告指南：免费玩家最经济的祷告升级方法，不花金币也能高效提升。",
        "osrs-ironman-money-making-f2p-2026.html": "2026年铁人模式F2P赚钱指南：铁人玩家在免费版中的经济策略和赚钱方法汇总。",
        "osrs-low-effort-money-making-beginners.html": "新手低投入赚钱方法汇总：不需要高强度操作，轻松稳定的金币收入来源。",
        "osrs-members-vs-f2p-comparison-2026.html": "2026年会员vs免费全面对比：分析两种模式在技能、内容、赚钱效率上的差异，帮你决定是否值得成为会员。",
        "osrs-money-making-beginner-2026.html": "2026年新手赚钱指南大全：从零开始的多种赚钱方法，适合不同等级和喜好的玩家。",
        "osrs-nmz-beginner-guide-2026.html": "NMZ（梦魇地带）新手完整指南：了解如何设置NMZ、选择Boss、最佳装备和训练策略。",
        "osrs-obor-bryophyta-f2p-boss-guide-2026.html": "F2P Boss挑战指南：Obor和Bryophyta的击败方法、掉落分析和准备工作。适合免费玩家。",
        "osrs-prayer-training-beginner-guide-2026.html": "2026年祷告训练新手指南：从1级到99级的完整祷告升级方法、骨类选择和最佳地点推荐。",
        "osrs-skills-overview-beginner-2026.html": "2026年OSRS全技能概览：了解所有23个技能的分类、训练方法和实际应用，为你的冒险之旅打基础。",
        "osrs-skill-training-beginner-complete-guide-2026.html": "2026年新手技能训练完整指南：涵盖所有核心技能的最佳训练方法、经验和金币数据对比。",
        "osrs-skill-training-beginner-fast-track-2026.html": "2026年技能训练快速通道指南：高效升级路线，帮助新玩家在最短时间内达到关键里程碑。",
        "osrs-slayer-beginner-first-master-guide-2026.html": "杀戮技能入门指南：从选择第一位杀戮大师开始，了解任务分配、装备和收益。",
        "osrs-slayer-beginner-guide-2026.html": "2026年杀戮技能新手完整指南：Slayer从1-99升级攻略、大师选择、任务推荐和赚钱技巧。",
        "osrs-toa-solo-beginner-guide-2026.html": "TOA（废墟之墓）单人新手指南：了解Boss机制、准备工作和通关策略，独立完成首次挑战。",
        "osrs-top-10-skills-to-train-first-2026.html": "2026年新手最需优先训练的10个技能：合理安排训练顺序，最大化效率和游戏体验。",
    }
    cn_summary = cn_summary_map.get(filename, f"完整指南帮助您了解{h1_en}的最佳方法和技巧。")
    
    # Insert cn-title and cn-summary before first h1
    cn_block = f'''            <h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title}</h1>
            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>
            <h1>{h1_en}</h1>'''
    
    # Replace first h1 with cn block
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', cn_block, html, count=1)
    return html


def fix_toc_items(html):
    """Add Chinese annotations to TOC items that lack them."""
    # Find TOC nav
    toc_match = re.search(r'<nav[^>]*class="toc"[^>]*>(.*?)</nav>', html, re.DOTALL)
    if not toc_match:
        # Try other TOC patterns
        toc_match = re.search(r'<div[^>]*class="toc"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not toc_match:
        return html
    
    toc_html = toc_match.group(0)
    new_toc = toc_html
    
    # For each li a in TOC, check if it has Chinese in parentheses
    li_pattern = re.findall(r'<li><a href="([^"]+)"[^>]*>([^<]+)</a></li>', toc_html)
    
    for href, text in li_pattern:
        # Check if already has Chinese in parens
        if '（' in text or '(' in text:
            continue
        # Add （中文翻译） placeholder
        new_toc = new_toc.replace(
            f'<a href="{href}">{text}</a>',
            f'<a href="{href}">{text}（中文翻译）</a>',
            1
        )
    
    html = html.replace(toc_html, new_toc)
    return html


def fix_headings(html):
    """Add Chinese annotations to h2/h3 in guide sections only, excluding support/footer areas."""
    # Skip headings containing these phrases (support card, footer, quick-preview, etc.)
    skip_texts = [
        'Support This Guide', 'Every guide is free', 'support-card',
        'References & Sources', 'copyright', 'All rights reserved',
        'Not affiliated with Jagex', '30秒快速预览',
    ]
    
    # Also use placeholder protection for known blocks
    protected_patterns = [
        (r'<div[^>]*class="support-card[^"]*"[^>]*>', r'</div>\s*</div>\s*</div>'),  # Not perfect but helps
    ]
    
    for level in ['h2', 'h3']:
        pattern = re.compile(rf'<{level}[^>]*>(.*?)</{level}>', re.DOTALL)
        for match in pattern.finditer(html):
            full = match.group(0)
            inner = match.group(1)
            # Skip if already has Chinese in parens
            if '（' in inner:
                continue
            # Skip if contains known non-guide phrases
            if any(skip in inner for skip in skip_texts):
                continue
            # Add （中文说明）
            new_inner = inner + '（中文说明）'
            new_full = full.replace(inner, new_inner)
            html = html.replace(full, new_full, 1)
    
    return html


def copy_quick_preview(en_html, zh_html):
    """Copy 30S Quick Preview box from English version if present."""
    # Check if zh already has a quick-preview box
    if '30秒快速预览' in zh_html:
        return zh_html
    
    qp_match = re.search(
        r'<div[^>]*class="quick-preview-box"[^>]*>.*?</div>',
        en_html, re.DOTALL
    )
    if not qp_match:
        # Check for quick-summary pattern too
        qp_match = re.search(
            r'<div[^>]*class="quick-summary"[^>]*>.*?</div>',
            en_html, re.DOTALL
        )
    if not qp_match:
        return zh_html
    
    qp_html = qp_match.group(0)
    # Change h3 label to Chinese - use a unique placeholder to prevent re-annotation
    qp_html = re.sub(
        r'<h3[^>]*>.*?</h3>',
        '<h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⚡ 30秒快速预览</h3>',
        qp_html
    )
    
    # Insert before first <section> in zh (that has an id)
    zh_html = re.sub(
        r'(<section[^>]*>)',
        qp_html + '\n\n            \\1',
        zh_html,
        count=1
    )
    return zh_html


def process_file(filename):
    en_path = os.path.join(BASE, "guides", filename)
    zh_path = os.path.join(BASE, "zh/guides", filename)
    
    if not os.path.exists(en_path):
        print(f"  SKIP: English file not found: {en_path}")
        return False
    if not os.path.exists(zh_path):
        print(f"  SKIP: Chinese file not found: {zh_path}")
        return False
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_html = f.read()
    
    changes = []
    
    # Step 0: Clean up any （中文说明） from protected areas and fix issues from previous runs
    # Remove （中文说明） from support card headings
    zh_html = re.sub(
        r'(<div[^>]*class="support-card[^"]*"[^>]*>.*?<h[23][^>]*>.*?)（中文说明）(.*?</h[23])',
        r'\1\2', zh_html, flags=re.DOTALL
    )
    # Remove （中文说明） from footer headings
    zh_html = re.sub(
        r'(<footer[^>]*>.*?<h[23][^>]*>.*?)（中文说明）(.*?</h[23])',
        r'\1\2', zh_html, flags=re.DOTALL
    )
    # Remove （中文说明） from quick-preview h3 
    zh_html = re.sub(
        r'(30秒快速预览)（中文说明）',
        r'\1', zh_html
    )
    # Remove duplicate quick preview boxes
    qp_count = zh_html.count('30秒快速预览')
    if qp_count > 1:
        # Keep only the first occurrence
        parts = zh_html.split('<div class="quick-summary"', 2)
        if len(parts) >= 3:
            # Find end of second quick-summary div
            second_start = parts[0] + '<div class="quick-summary"' + parts[1]
            remaining = '<div class="quick-summary"' + parts[2]
            # Find close of the second quick-summary
            close_match = re.search(r'</div>', remaining)
            if close_match:
                remaining = remaining[close_match.end():]
                zh_html = second_start + remaining
    
    # Step 1: Fix hero section
    old_zh2 = zh_html
    zh_html = add_cn_hero(zh_html, filename)
    if zh_html != old_zh2:
        changes.append("Added cn-title and cn-summary")
    
    # Step 2: Fix TOC items
    old_zh2 = zh_html
    zh_html = fix_toc_items(zh_html)
    if zh_html != old_zh2:
        changes.append("Updated TOC with Chinese annotations")
    
    # Step 3: Fix headings
    old_zh2 = zh_html
    zh_html = fix_headings(zh_html)
    if zh_html != old_zh2:
        changes.append("Updated headings with Chinese annotations")
    
    # Step 4: Copy quick preview
    old_zh2 = zh_html
    zh_html = copy_quick_preview(en_html, zh_html)
    if zh_html != old_zh2:
        changes.append("Copied Quick Preview box from English")
    
    if not changes:
        print(f"  NO CHANGES: {filename}")
        return True
    
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(zh_html)
    
    print(f"  CHANGED ({', '.join(changes)}): {filename}")
    return True


def main():
    total = len(FILES)
    changed = 0
    skipped = 0
    
    print(f"Processing {total} files...")
    print("=" * 60)
    
    for i, filename in enumerate(FILES, 1):
        print(f"[{i}/{total}] {filename}")
        result = process_file(filename)
        if result is False:
            skipped += 1
        print()
    
    print("=" * 60)
    print(f"Done! Processed {total} files.")


if __name__ == '__main__':
    main()
