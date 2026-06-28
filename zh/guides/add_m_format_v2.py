#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第2版：先清理原有cn-title/cn-summary，再添加正确的M+格式。
"""
import re, os

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\zh\guides"
OUT_DIR  = r"C:\Users\Lenovo\AppData\Local\Temp\osrs_m_format_v2"
os.makedirs(OUT_DIR, exist_ok=True)

CONFIG = {
    "blood-moon-rises-quest-guide-2026.html": {
        "cn_title": "OSRS 血月崛起任务攻略（2026版）",
        "cn_summary": "血月崛起（The Blood Moon Rises）是Myreque任务线的史诗终章。本文提供完整通关攻略，包括Boss阶段策略、谜题解法、奖励一览以及铁人模式技巧，助你顺利完成这一宗师级任务。",
        "h2_map": {
            "Quest Overview & Lore": "任务概述与背景故事",
            "Quest Requirements (Skills, Quests, Items)": "任务要求（技能、前置任务、物品）",
            "Step-by-Step Walkthrough (Spoiler-Light)": "分步通关攻略（轻度剧透）",
            "Boss Fight Strategies (All Phases)": "Boss战斗策略（全阶段）",
            "Puzzle Solutions": "谜题解法",
            "Quest Rewards (XP, Gear, Unlocks)": "任务奖励（经验、装备、解锁内容）",
            "Post-Quest Content & Unlocks": "任务后内容与解锁",
            "Ironman-Specific Tips": "铁人模式专属技巧",
            "Common Mistakes & How to Avoid Them": "常见错误及避免方法",
            "Frequently Asked Questions": "常见问题解答",
        },
        "h3_map": {
            "Quest Lore (Spoiler-Free)": "任务背景（无剧透）",
            "Quest Details": "任务详情",
            "Skill Requirements": "技能要求",
            "Quest Requirements": "前置任务要求",
            "Item Requirements (Bring These!)": "物品要求（请携带！）",
            "Step 1: Speak to Veliaf Hurtz": "步骤1：与Veliaf Hurtz对话",
            "Step 2: Investigate the Blood Moon Temple": "步骤2：调查血月神庙",
            "Step 3: Solve the Blood Moon Puzzle": "步骤3：解血月谜题",
            "Step 4: Defeat the Blood Moon Avatar (Phase 1)": "步骤4：击败血月化身（阶段1）",
            "Step 5: The Collapsing Temple (Agility Puzzle)": "步骤5：崩塌的神庙（敏捷谜题）",
            "Step 6: Final Showdown (Phase 2)": "步骤6：最终决战（阶段2）",
            "Step 7: Claim Your Rewards": "步骤7：领取奖励",
            "Phase 1: The Avatar's First Form (HP 1000-700)": "阶段1：化身的第一形态（HP 1000-700）",
            "Phase 2: The Avatar's True Form (HP 700-0)": "阶段2：化身的真身（HP 700-0）",
            "Recommended Gear for Boss Fight": "Boss战推荐装备",
            "Puzzle 1: The Lunar Altar Alignment": "谜题1：月神祭坛对齐",
            "Puzzle 2: The Collapsing Temple (Agility)": "谜题2：崩塌的神庙（敏捷）",
            "Puzzle 3: The Blood Moon Seal (Memory Game)": "谜题3：血月封印（记忆游戏）",
            "XP Rewards": "经验奖励",
            "GP Reward": "GP奖励",
            "New Gear & Items": "新装备与物品",
            "Unlocks & Access": "解锁与访问权限",
            "Blood Moon Island": "血月岛",
            "Myreque Shop Upgrades": "Myreque商店升级",
            "New Slayer Tasks (Blood Moon Creatures)": "新杀戮任务（血月生物）",
            "Post-Quest Miniquest: \"The Blood Moon Legacy\"": "任务后迷你任务：血月遗产",
            "Ironman Preparation": "铁人模式准备",
            "Ironman Gear Progression (for Quest)": "铁人模式装备进阶（任务用）",
            "Mistake 1: Not Bringing a Blisterwood Weapon": "错误1：未携带水银木武器",
            "Mistake 2: Running Out of Prayer Potions": "错误2：祈祷药水耗尽",
            "Mistake 3: Failing the Agility Puzzle (Collapsing Temple)": "错误3：敏捷谜题失败（崩塌神庙）",
            "Mistake 4: Not Wearing Anti-Poison": "错误4：未装备解毒",
            "Mistake 5: Forgetting to Upgrade Blisterwood Staff to Sword": "错误5：忘记将水银木杖升级为剑",
            "Related Guides": "相关攻略",
        }
    },
    "new-boss-loot-guide-2026.html": {
        "cn_title": "OSRS 2026新Boss击杀与掉落指南",
        "cn_summary": "全面解析2026年OSRS新增Boss的机制、掉落表和每小时收益。涵盖Moolord等新Boss的单人/团队策略、宠物掉落率及铁人模式技巧，助你最大化战斗收益。",
        "h2_map": {
            "2026 New Bosses Overview": "2026新Boss概览",
            "Moolord — The Bovine Terror": "Moolord — 牛头恐怖",
            "Gear Requirements": "装备要求",
            "Kill Mechanics & Phases": "击杀机制与阶段",
            "Solo vs Team Strategies": "单人vs团队策略",
            "Drop Tables & GP Values": "掉落表与GP价值",
            "Money-Making Potential (GP/hr)": "赚钱潜力（每小时收益）",
            "Pet Drops & Drop Rates": "宠物掉落与概率",
            "Ironman Strategies": "铁人模式策略",
        },
        "h3_map": {
            "Location & Access": "位置与入口",
        }
    },
    "osrs-blood-moon-rises-prep-checklist-detailed-2026.html": {
        "cn_title": "OSRS 血月崛起前置准备清单（2026版）",
        "cn_summary": "血月崛起（The Blood Moon Rises）将于2026年6月30日发布。本文提供最全面的前置准备指南——涵盖所有前置任务清单、推荐属性等级、装备配置、物品购物清单及四周准备时间表，确保你有备而战。",
        "h2_map": {
            "Blood Moon Rises — What We Know": "血月崛起 — 已知信息",
            "Complete Requirements Checklist": "完整前置要求清单",
            "Preparation Timeline (4-Week Plan)": "准备时间表（四周计划）",
            "Recommended Gear Setup": "推荐装备配置",
            "What Happens If You're Not Fully Prepared": "准备不足的后果",
            "Blood Moon Rewards Speculation": "血月奖励猜测",
            "Quick Checklist Summary & FAQ": "快速清单总结与常见问题",
        },
        "h3_map": {
            "Story Background (No Spoilers)": "故事背景（无剧透）",
            "Expected Difficulty": "预期难度等级",
            "Confirmed Rewards (From Jagex Teasers)": "已确认奖励（来自Jagex预告）",
        }
    },
    "osrs-bond-vs-subscription-2026.html": {
        "cn_title": "OSRS 绑定期与付费订阅对比（2026版）",
        "cn_summary": "2026年绑定期价格升至约520万GP，订阅费涨至$14.99/月。本文通过GP Farming计算器和盈亏平衡分析，帮你判断哪种方式更适合你的游戏风格。",
        "h2_map": {
            "What is an OSRS Bond?": "什么是OSRS绑定期？",
            "Bond vs Subscription — Price Comparison": "绑定期vs订阅 — 价格对比",
            "GP Farming Calculator — Can You Afford a Bond?": "GP Farming计算器 — 你能买得起绑定期吗？",
            "Break-Even Analysis — When Bond Wins": "盈亏平衡分析 — 何时绑定期更划算",
            "Who Should Use Bonds (Not Subscribe)": "谁应该使用绑定期（而非订阅）",
            "Who Should Subscribe (Not Bond)": "谁应该订阅（而非使用绑定期）",
            "FAQs": "常见问题解答",
        },
        "h3_map": {}
    },
    "osrs-cancel-membership-refund-2026.html": {
        "cn_title": "OSRS 取消会员与退款指南（2026政策）",
        "cn_summary": "想取消OSRS会员订阅？本文详细说明如何关闭自动续费、向Jagex申请退款、取消后的账户状态以及如果费用过高时的更省钱替代方案。",
        "h2_map": {
            "Before You Cancel — Consider These First": "取消前请三思",
            "How to Cancel Auto-Renewal (Step-by-Step)": "如何取消自动续费（分步指南）",
            "Jagex Refund Policy 2026 Explained": "Jagex 2026退款政策详解",
            "How to Request a Refund": "如何申请退款",
            "What Happens After Cancellation": "取消后会发生什么",
            "Alternatives to Cancelling (Save Money Instead)": "取消的替代方案（省钱更佳）",
            "Re-subscribing Later — Best Practices": "后续重新订阅 — 最佳实践",
            "FAQs — Cancellation & Refunds": "常见问题 — 取消与退款",
        },
        "h3_map": {
            "Why Do You Want to Cancel?": "你为什么想取消？",
            "The Timing Matters": "时机很重要",
        }
    },
    "osrs-chambers-of-xeric-loot-profit-guide.html": {
        "cn_title": "OSRS 沙力克密室战利品与收益攻略（2026版）",
        "cn_summary": "沙力克密室（Raids 1）是OSRS中最赚钱的活动之一。扭曲弓价值超过11亿GP，普通战利品也能提供稳定收入。本文详解完整掉落表、点数系统及单人/组队每小时收益分析。",
        "already_has_cn_title": True,
        "h2_map": {},
        "h3_map": {}
    },
    "osrs-cheapest-membership-2026.html": {
        "cn_title": "OSRS 最便宜会员获取方式（2026版·合法途径）",
        "cn_summary": "OSRS会员越来越贵——2026年涨价后月费更甚。本文比较所有合法途径：月/季/年订阅、绑定期、第三方零售商和购买时机，帮你找到最省钱的方法。",
        "h2_map": {
            "All Legal Ways to Buy Membership (Full Price List)": "所有合法购买会员的方式（完整价格表）",
            "Monthly vs Quarterly vs Yearly — The Math": "月费vs季度vs年度 — 数学计算",
            "Bonds: The In-Game Currency Route": "绑定期：游戏内货币途径",
            "Third-Party Retailers (Legitimate Ones Only)": "第三方零售商（仅合法渠道）",
            "Timing Your Purchase — When Is Cheapest?": "购买时机 — 什么时候最便宜？",
            "Regional Pricing & VPN Considerations": "区域定价与VPN考量",
            "The Ultimate Money-Saving Strategy": "终极省钱策略",
            "Scams to Avoid (Important!)": "需要避免的骗局（重要！）",
            "FAQ": "常见问题",
            "Final Tips": "最终建议",
        },
        "h3_map": {
            "Complete Price List (USD, as of June 2026)": "完整价格表（美元，2026年6月）",
        }
    },
    "osrs-combat-achievements-easy-walkthrough-2026.html": {
        "cn_title": "OSRS 战斗成就（简单）完整通关攻略（2026版）",
        "cn_summary": "战斗成就（CA）系统是OSRS最重要的PvM进阶体系之一。本文完整讲解全部35项简单级任务——精确要求、分步完成方法、推荐装备和专家技巧，助你解锁Ghommal's Hilt的+5%伤害加成。",
        "h2_map": {
            "What Are Combat Achievements?": "什么是战斗成就？",
            "Easy Combat Achievements — Complete List (All 35 Tasks)": "简单战斗成就 — 完整列表（全部35项）",
            "Optimal Completion Order": "最佳完成顺序",
            "Ghommal's Hilt Guide — Rewards & Usage": "Ghommal's Hilt指南 — 奖励与使用",
            "Preparing for Medium Tier": "为中级难度做准备",
            "FAQ & Quick Reference Table": "常见问题与快速参考表",
        },
        "h3_map": {
            "The Six Tiers of Combat Achievements": "战斗成就的六个难度等级",
            "Why Combat Achievements Matter": "为什么战斗成就很重要",
        }
    },
    "osrs-corrupted-gauntlet-guide-2026.html": {
        "cn_title": "OSRS 腐化Gauntlet完全攻略（2026版·预算配置）",
        "cn_summary": "无需满级属性或数十亿装备也能征服腐化Gauntlet。本文详解T1/T2护甲准备策略、Hunllef Boss机制、祈祷切换技巧，以及零成本实现约500万GP/小时收益的完整路径。",
        "h2_map": {
            "How the Gauntlet Works": "Gauntlet运作方式",
            "Tier 1 Prep (Fast — Experienced)": "T1准备（快速 — 高手向）",
            "Tier 2 Prep (Safe — Beginners)": "T2准备（稳健 — 新手向）",
            "Hunllef Boss Mechanics": "Hunllef Boss机制",
            "Tornado Survival Formula": "龙卷风生存法则",
            "Profit & Drops": "收益与掉落",
            "FAQ": "常见问题",
            "Best Zero-Risk Money Maker": "最佳零风险赚钱方式",
            "Related Guides": "相关攻略",
            "Related Guides（相关攻略）": "相关攻略",
        },
        "h3_map": {
            "CG — Quick Reference": "CG — 快速参考",
        }
    },
    "osrs-curse-of-the-empty-lord-quest-2026.html": {
        "cn_title": "OSRS 虚空领主诅咒迷你任务攻略（2026版）",
        "cn_summary": "虚空领主诅咒（Curse of the Empty Lord）是OSRS中最具氛围感的迷你任务之一。本文详细说明如何找到Viggora的三个出现位置、解锁幽灵长袍套装，并深入探索Zaros背叛的背景故事。",
        "h2_map": {
            "Mini-Quest Overview & Requirements": "迷你任务概述与要求",
            "The Lore — Zaros, Zamorak & the Betrayal": "背景故事 — Zaros、Zamorak与背叛",
            "Step-by-Step Walkthrough": "分步通关流程",
            "Viggora NPC Locations (All Three)": "Viggora NPC位置（全部三处）",
            "Ghostly Robes — Full Set & Stats": "幽灵长袍 — 完整套装与属性",
            "Tips, Troubleshooting & Common Mistakes": "技巧、故障排除与常见错误",
            "FAQs": "常见问题解答",
        },
        "h3_map": {
            "Requirements": "要求",
        }
    },
    "osrs-desert-treasure-quest-guide-low-level.html": {
        "cn_title": "OSRS 沙漠宝藏任务低级攻略（2026版）",
        "cn_summary": "沙漠宝藏（Desert Treasure）是解锁古代魔法的最关键任务。本文专为低等级玩家设计——提供最低要求、四大Boss（Dessous/Kamil/Fareed/Damis）的逃课打法与安全站位，助你以最低属性解锁全部古代魔法。",
        "h2_map": {
            "Quest & Skill Requirements": "任务与技能要求",
            "Pre-Quest Preparation": "任务前准备",
            "Step-by-Step Walkthrough": "分步通关流程",
            "Dessous (Vampyre) — Safe Spot Strategy": "Dessous（吸血鬼）— 安全站位策略",
            "Kamil (Ice Troll) — Direct Fight Strategy": "Kamil（冰巨魔）— 正面战斗策略",
            "Fareed (Fire Warrior) — Safe Spot Strategy": "Fareed（火战士）— 安全站位策略",
            "Damis (Shadow Hound) — Safe Spot & Prayer Strategy": "Damis（暗影猎犬）— 安全站位与祈祷策略",
            "Rewards: Ancient Magicks Spellbook": "奖励：古代魔法书",
            "FAQ — Desert Treasure Low Level": "常见问题 — 沙漠宝藏低级攻略",
        },
        "h3_map": {}
    },
    "osrs-diary-easy-medium-complete-guide-2026.html": {
        "cn_title": "OSRS 简易与中等成就日记完整攻略（2026版·全区域）",
        "cn_summary": "完成全部12个区域的简易和中等成就日记只需这一份攻略。每个区域的每项任务都有精确要求、物品清单和最优路线。附常用物品清单和时间管理策略，帮你最大化账号成长效率。",
        "h2_map": {
            "Achievement Diaries Overview": "成就日记概览",
            "Complete Easy Diaries Walkthrough (All Regions)": "简易日记完整攻略（全区域）",
            "Complete Medium Diaries Walkthrough (All Regions)": "中等日记完整攻略（全区域）",
            "Essential Items Checklist": "必备物品清单",
            "Time Management Strategy": "时间管理策略",
            "After E/M Diaries: Preparing for Hard": "完成简易/中等后：准备挑战困难",
            "FAQ & Troubleshooting": "常见问题与故障排除",
        },
        "h3_map": {
            "All Regions & Diary Tiers": "全部区域与日记等级",
            "Rewards Structure": "奖励结构",
        }
    },
    "osrs-diary-priority-order-beginner-2026.html": {
        "cn_title": "OSRS 成就日记优先级排序（2026版·新手必备）",
        "cn_summary": "并非所有成就日记都价值相等。有些解锁能省数百小时的游戏时间，有些仅提供无实用价值的外观奖励。本文通过数据驱动的方法按每小时回报率对所有日记进行排名，帮你优先完成最有价值的10个日记。",
        "h2_map": {
            "Why Diary Order Matters (Not All Diaries Are Equal)": "为什么日记顺序很重要（并非所有日记都等价）",
            "The Scoring System — How We Ranked Diaries": "评分系统 — 我们如何排名日记",
            "Top 10 Diaries — Detailed Breakdown": "十大日记 — 详细分析",
            "Optimal Completion Route (Efficiency Path)": "最优完成路线（效率路径）",
            "Diaries to Skip For Now": "暂时跳过的日记",
            "Quick Reference: All Diary Rewards Summary": "快速参考：全部日记奖励总结",
            "Diary Priority FAQ": "日记优先级常见问题",
        },
        "h3_map": {
            "Why Beginners Should NOT Start with Hard Diaries": "为什么新手不应从困难日记开始",
        }
    },
}


def clean_and_process(filepath, cfg):
    """
    1. 读取文件
    2. 移除guide-hero中已有的cn-title和cn-summary
    3. 在英文<h1>前添加正确的cn-title和cn-summary
    4. 添加H2/H3翻译
    5. 写入输出目录
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 先清理已经存在的cn-title和cn-summary
    # 匹配 guide-hero 区域内的 cn-title 和 cn-summary
    guide_hero_pattern = re.compile(
        r'(<section class="guide-hero">.*?)(<h1 class="cn-title"[^>]*>.*?</h1>\s*)(<p class="cn-summary"[^>]*>.*?</p>\s*)?',
        re.DOTALL
    )
    content = guide_hero_pattern.sub(r'\1', content)

    # 还要清理可能存在的单独cn-title
    content = re.sub(
        r'(?<=<section class="guide-hero">.*?)(<h1 class="cn-title"[^>]*>.*?</h1>\s*)(<p class="cn-summary"[^>]*>.*?</p>\s*)?',
        '', content
    )

    # 清理任何独立的cn-summary
    content = re.sub(r'<p class="cn-summary"[^>]*>.*?</p>\s*', '', content)

    # 现在添加正确的cn-title和cn-summary在英文<h1>前
    h1_pattern = re.compile(r'(<section class="guide-hero">.*?)(<h1[^>]*>)(.*?)(</h1>)', re.DOTALL)
    match = h1_pattern.search(content)
    if match:
        before_section = content[:match.start()]
        section_start = match.group(1)
        h1_open = match.group(2)
        h1_text = match.group(3)
        h1_close = match.group(4)
        after_h1 = content[match.end():]

        if not cfg.get("already_has_cn_title", False):
            cn_title_html = f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cfg["cn_title"]}</h1>\n            '
            cn_summary_html = f'<p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cfg["cn_summary"]}</p>\n            '
            new_section = section_start + cn_title_html + cn_summary_html + h1_open + h1_text + h1_close
            content = before_section + new_section + after_h1
            print(f"  [OK] 已添加中文H1和导语")

    # 添加H2翻译
    def process_headers(header_tag, header_map, content):
        pattern = re.compile(f'<{header_tag}[^>]*>(.*?)</{header_tag}>', re.DOTALL)
        def replacer(match):
            full = match.group(0)
            inner = match.group(1)
            text_only = re.sub(r'<[^>]+>', '', inner).strip()
            has_translation = bool(re.search(r'[（(][\u4e00-\u9fff\)）]', inner))
            if not has_translation and text_only in header_map:
                cn = header_map[text_only]
                new_inner = inner.rstrip() + f'（{cn}）'
                return full.replace(inner, new_inner)
            return full
        return pattern.sub(replacer, content)

    content = process_headers('h2', cfg.get("h2_map", {}), content)
    content = process_headers('h3', cfg.get("h3_map", {}), content)

    # 写入输出
    outpath = os.path.join(OUT_DIR, os.path.basename(filepath))
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [SAVED] -> {outpath}")


def main():
    files = list(CONFIG.keys())
    for fname in files:
        filepath = os.path.join(BASE_DIR, fname)
        print(f"\n{'='*60}")
        print(f"处理: {fname}")
        if fname in CONFIG:
            clean_and_process(filepath, CONFIG[fname])
        else:
            print(f"  [SKIP] 无配置")

    print(f"\n{'='*60}")
    print(f"全部完成！输出目录: {OUT_DIR}")

if __name__ == "__main__":
    main()
