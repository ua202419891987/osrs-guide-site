#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为OSRS技能训练文章添加M+中文格式"""

import re
import os

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\zh\guides"

# =========================================================
# 每篇文章的中文标题、导语 和 H2/H3 翻译映射
# =========================================================

file_data = {
    # =========================================================
    # 1. Prayer Guide 2026
    # =========================================================
    "osrs-1-99-prayer-guide-2026.html": {
        "cn_title": "OSRS 祷告技能训练：1-99 全方法对比（2026版）",
        "cn_summary": "本指南详细对比金边祭坛、混乱祭坛、厄克特方塔等所有祷告训练方法，涵盖各类骨头经验表、任务奖励、成本分析及钢铁侠模式策略，助你高效达成99级祷告。",
        "h_translations": {
            "Table of Contents": "目录",
            "1. Prayer Overview & Core Mechanics": "祷告概述与核心机制（祷告概述与核心机制）",
            "How Prayer Training Works": "祷告训练工作原理（祷告训练工作原理）",
            "Why Train Prayer?": "为何要训练祷告？（为何要训练祷告？）",
            "2. Complete Bone & Ashes XP Table": "完整骨头与灰烬经验表（完整骨头与灰烬经验表）",
            "3. Quest XP Rewards": "任务经验奖励（任务经验奖励）",
            "4. Gilded Altar — Best for Main Accounts (3.5x XP)": "金边祭坛 — 主账号最佳选择（3.5倍经验）",
            "Setup Requirements": "设置要求（设置要求）",
            "How to Use World 330 (Free, No Construction)": "如何使用世界330（免费，无需建筑）",
            "XP Rates & Costs": "经验率与成本（经验率与成本）",
            "5. Chaos Altar — Wilderness Risk, Big Savings (3.5x + Bone Save)": "混乱祭坛 — 荒野风险，大幅节省（3.5倍+保留骨头）",
            "Setup": "设置（设置）",
            "Risk Management": "风险管理（风险管理）",
            "Chaos Altar vs Gilded Altar — Cost Comparison": "混乱祭坛 vs 金边祭坛 — 成本对比",
            "6. Ectofuntus — No Risk, 4x XP (Ironman Friendly)": "厄克特方塔 — 无风险，4倍经验（适合钢铁侠）",
            "How It Works": "运作方式（运作方式）",
            "When to Use Ectofuntus": "何时使用厄克特方塔（何时使用厄克特方塔）",
            "7. Ensouled Heads — Combat + Prayer Training (50K-120K XP/hr)": "注入灵魂的头颅 — 战斗+祷告训练（5万-12万经验/小时）",
            "Ensouled Heads XP Table": "注入灵魂的头颅经验表",
            "8. Other Methods — Passive Prayer XP": "其他方法 — 被动祷告经验（其他方法 — 被动祷告经验）",
            "Bone Crusher (Morytania Hard Diary)": "碎骨器（莫里塔尼亚困难日记）",
            "Ash Sanctifier ( Kourend Hard Diary)": "灰烬净化器（库伦德困难日记）",
            "Offering Spells (Arceuus Spellbook)": "献祭法术（阿尔塞乌斯法术书）",
            "9. All Methods Comparison Table": "所有方法对比表（所有方法对比表）",
            "10. Ironman 1-99 Prayer Strategy": "钢铁侠1-99祷告策略（钢铁侠1-99祷告策略）",
            "Early Game (1-43)": "前期（1-43级）（前期（1-43级））",
            "Mid Game (43-70) — Green Dragons": "中期（43-70级）— 绿龙（中期（43-70级）— 绿龙）",
            "Late Game (70-99) — PvM Bones": "后期（70-99级）— PvM骨头（后期（70-99级）— PvM骨头）",
            "Passive Ironman Prayer XP": "钢铁侠被动祷告经验（钢铁侠被动祷告经验）",
            "11. Bone Gathering Methods (Main Accounts)": "骨头收集方法（主账号）（骨头收集方法（主账号））",
            "12. Cost Analysis — Bones Needed to 99": "成本分析 — 升到99级所需骨头（成本分析 — 升到99级所需骨头）",
            "Dragon Bones (Gilded Altar — 3.5x, 252 XP each)": "龙骨（金边祭坛 — 3.5倍，每个252经验）",
            "Chaos Altar Savings (50% bone save)": "混乱祭坛节省（50%保留骨头）",
            "13. Level Milestones & Prayer Unlocks": "等级里程碑与祷告解锁（等级里程碑与祷告解锁）",
            "14. Pro Tips for Maximum Efficiency": "极限效率专业技巧（极限效率专业技巧）",
            "15. FAQ": "常见问题（常见问题）",
            "Q: How long does 1-99 Prayer take?": "问：1-99祷告需要多长时间？",
            "Q: What's the cheapest GP/XP for Prayer?": "问：祷告最便宜的GP/XP是多少？",
            "Q: Is Chaos Altar safe?": "问：混乱祭坛安全吗？",
            "Q: What Prayer level should I aim for?": "问：我应该瞄准多少级祷告？",
            "Q: Best Prayer training for Ironman?": "问：钢铁侠最佳祷告训练方式？",
            "Q: Can I train Prayer on F2P?": "问：F2P可以训练祷告吗？",
            "Q: Are ensouled heads worth it?": "问：注入灵魂的头颅值得用吗？",
            "Related Guides": "相关指南",
            "Every guide is free — this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 2. Prayer Guide All Methods 2026
    # =========================================================
    "osrs-1-99-prayer-guide-all-methods-2026.html": {
        "cn_title": "OSRS 祷告技能训练：1-99 全方法指南（2026版）",
        "cn_summary": "全面介绍OSRS祷告技能训练的所有方法，包括金边祭坛（最快）、混乱祭坛（最省）、厄克特方塔（安全）及瓦尔拉莫尔新方法，附完整成本对比和经验值表格。",
        "h_translations": {
            "How Prayer XP Works": "祷告经验值运作方式（祷告经验值运作方式）",
            "Bone Types &amp; XP Values (All Methods)": "骨头类型与经验值（所有方法）",
            "F2P Route (Levels 1\u201343+)": "F2P路线（1-43+级）（F2P路线（1-43+级））",
            "Recommended F2P Path": "推荐的F2P路径（推荐的F2P路径）",
            "F2P Cost to Level 43": "F2P升到43级成本（F2P升到43级成本）",
            "Members Fastest Route \u2014 Gilded Altar": "会员最快路线 — 金边祭坛（会员最快路线 — 金边祭坛）",
            "Gilded Altar Setup Guide": "金边祭坛设置指南（金边祭坛设置指南）",
            "Dragon Bones on Gilded Altar \u2014 The Standard Method": "金边祭坛用龙骨 — 标准方法",
            "New 2026 Meta: Varlamore Prayer Methods": "2026新主流：瓦尔拉莫尔祷告方法",
            "Varlamore Bone Offering (Post-Children of the Sun)": "瓦尔拉莫尔骨头献祭（日之子任务后）",
            "Ensouled Heads (Combat-Based Prayer XP)": "注入灵魂的头颅（基于战斗的祷告经验）",
            "Full Cost Comparison to 99 Prayer": "99级祷告完整成本对比（99级祷告完整成本对比）",
            "Essential Prayer Milestones": "重要祷告里程碑（重要祷告里程碑）",
            "Prayer Training Tips": "祷告训练技巧（祷告训练技巧）",
        }
    },

    # =========================================================
    # 3. Thieving Guide Ironman
    # =========================================================
    "osrs-1-99-thieving-guide-ironman.html": {
        "cn_title": "OSRS 钢铁侠偷窃技能训练：1-99 全指南（2026版）",
        "cn_summary": "专为钢铁侠账号打造的偷窃技能完整训练指南，涵盖金字塔掠夺、阿多格奈骑士、大师农夫等所有方法，附种子收益、金币产出及关键解锁攻略。",
        "h_translations": {
            "\U0001f4b0 Ironman Thieving \u2014 Quick Reference": "钢铁侠偷窃 — 快速参考",
            "1. Why Ironmen Need Thieving": "1. 钢铁侠为何需要偷窃（钢铁侠为何需要偷窃）",
            "2. Levels 1-55: Early Game Thieving Progression": "2. 1-55级：前期偷窃进展",
            "3. Levels 55-99: Pyramid Plunder (Fastest XP)": "3. 55-99级：金字塔掠夺（最快经验）",
            "Pyramid Plunder Run Strategy": "金字塔掠夺策略（金字塔掠夺策略）",
            "4. Alternative: Ardougne Knights (Best AFK, Level 55+)": "4. 替代方案：阿多格奈骑士（最佳挂机，55+级）",
            "5. Key Ironman Rewards & Unlocks": "5. 钢铁侠关键奖励与解锁",
            "6. Common Mistakes Ironmen Make": "6. 钢铁侠常犯错误（钢铁侠常犯错误）",
            "7. Frequently Asked Questions": "7. 常见问题（常见问题）",
            "\U0001f3af Thieving Cape \u2014 Ironman Achievement": "偷窃披风 — 钢铁侠成就",
            "\U0001f4da Related Guides": "相关指南",
            "Related Guides": "相关指南",
            "Every guide is free \u2014 this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 4. Woodcutting Guide Early Game
    # =========================================================
    "osrs-1-99-woodcutting-guide-early-game.html": {
        "cn_title": "OSRS 伐木技能训练：新手1-99全指南（2026版）",
        "cn_summary": "从F2P到会员的伐木技能完整升级路线，涵盖橡树、柳树、柚木、桃花心木到红木的最佳训练方法，附斧头等级表、经验速率对比及装备推荐。",
        "h_translations": {
            "\U0001f7f5 Woodcutting 1-99 -- Quick Reference": "伐木1-99 -- 快速参考",
            "1. Axe Upgrades -- Always Use the Best Available": "1. 斧头升级 — 始终使用最佳（斧头升级 — 始终使用最佳）",
            "2. F2P Woodcutting Route (1-99)": "2. F2P伐木路线（1-99级）（F2P伐木路线（1-99级））",
            "3. Members Woodcutting Route (1-99)": "3. 会员伐木路线（1-99级）（会员伐木路线（1-99级））",
            "Teak Trees -- The Fastest Method": "柚木 — 最快方法（柚木 — 最快方法）",
            "Mahogany Trees on Ape Atoll": "猿猴岛的桃花心木（猿猴岛的桃花心木）",
            "4. Redwood Trees -- Best AFK Method (90-99)": "4. 红木 — 最佳挂机方法（90-99级）（红木 — 最佳挂机方法（90-99级））",
            "5. 3-Tier Gear &amp; Inventory Setup": "5. 三级装备与背包设置",
            "6. Advanced Tips for Maximum Efficiency": "6. 极限效率进阶技巧（极限效率进阶技巧）",
            "7. Common Mistakes": "7. 常见错误（常见错误）",
            "8. Frequently Asked Questions": "8. 常见问题（常见问题）",
            "\U0001f7f5 The Path to 99 -- You've Got This": "通往99之路 — 你可以的",
            "\U0001f4da Related Guides": "相关指南",
            "Related Guides": "相关指南",
            "Every guide is free \u2014 this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 5. Agility Training Guide 2026
    # =========================================================
    "osrs-agility-training-guide-2026.html": {
        "cn_title": "OSRS 敏捷技能训练：1-99 最快经验与屋顶路线（2026版）",
        "cn_summary": "2026年OSRS敏捷技能完整训练指南，涵盖屋顶路线、圣殿墓穴（最高经验率）、布林哈文竞技场、荒野路线等所有方法，附准确的经验/小时和金币/小时数据。",
        "h_translations": {
            "\U0001f4cb Table of Contents": "目录",
            "1. Why Train Agility?": "1. 为何训练敏捷？（为何训练敏捷？）",
            "2. Essential Items & Gear": "2. 必备物品与装备（必备物品与装备）",
            "\U0001f392 Mandatory Items": "必带物品（必带物品）",
            "\u2694\ufe0f Wilderness Course Gear (Risk Protection)": "荒野路线装备（风险防护）",
            "\u26ea Hallowed Sepulchre Gear": "圣殿墓穴装备（圣殿墓穴装备）",
            "3. Fastest 1-99 Route Overview": "3. 最快1-99路线概览（最快1-99路线概览）",
            "4. Rooftop Courses \u2014 Complete Data": "4. 屋顶路线 — 完整数据（屋顶路线 — 完整数据）",
            "\U0001f5fa\ufe0f Rooftop Course Diary Bonuses": "屋顶路线日记加成（屋顶路线日记加成）",
            "\u23f1\ufe0f Marks of Grace \u2192 GP Conversion": "恩典印记 → 金币转换（恩典印记 → 金币转换）",
            "5. Brimhaven Agility Arena": "5. 布林哈文敏捷竞技场（布林哈文敏捷竞技场）",
            "\U0001f3f7\ufe0f Arena Ticket Rewards": "竞技场门票奖励（竞技场门票奖励）",
            "\U0001f43f\ufe0f Giant Squirrel Pet Rate": "巨松鼠宠物概率（巨松鼠宠物概率）",
            "6. Wilderness Agility Course": "6. 荒野敏捷路线（荒野敏捷路线）",
            "\U0001f6e1\ufe0f Anti-PK Strategy": "反PK策略（反PK策略）",
            "\U0001f4b0 Loot Breakdown": "战利品详解（战利品详解）",
            "7. Hallowed Sepulchre \u2014 Fastest XP in the Game": "7. 圣殿墓穴 — 游戏中最快经验（圣殿墓穴 — 游戏中最快经验）",
            "\U0001f4cb Requirements": "要求（要求）",
            "\U0001f4ca Floor-by-Floor XP Rates": "逐层经验率（逐层经验率）",
            "\U0001f3ae Trap Types & How to Beat Them": "陷阱类型与应对方法（陷阱类型与应对方法）",
            "\U0001f381 Hallowed Sepulchre Rewards": "圣殿墓穴奖励（圣殿墓穴奖励）",
            "\U0001f6d2 Reward Shop Purchase Order": "奖励商店购买顺序（奖励商店购买顺序）",
            "8. Alternative & AFK Methods": "8. 替代与挂机方法（替代与挂机方法）",
            "\U0001f3f0 Prifddinas Agility Course (Level 75)": "普里夫迪纳斯敏捷路线（75级）",
            "\U0001f412 Ape Atoll Course (Level 48)": "猿猴岛路线（48级）",
            "\U0001f409 Colossal Wyrm Course (Level 50/62)": "巨型蠕虫路线（50/62级）",
            "\U0001f41f Barbarian Fishing (Passive Agility XP)": "野蛮人钓鱼（被动敏捷经验）",
            "\U0001f3e0 POH Agility (Most AFK)": "玩家房屋敏捷（最挂机友好）",
            "9. Marks of Grace & Graceful Outfit Guide": "9. 恩典印记与优雅套装指南",
            "\U0001f48e What Are Marks of Grace?": "什么是恩典印记？",
            "\U0001f457 Graceful Outfit \u2014 Full Set": "优雅套装 — 完整套装",
            "\U0001f3a8 Graceful Recolours": "优雅套装换色（优雅套装换色）",
            "\U0001f4cd Optimal Mark Farming Strategy": "最优印记收集策略（最优印记收集策略）",
            "10. Key Shortcuts Unlocked by Level": "10. 各等级解锁的关键捷径（各等级解锁的关键捷径）",
            "11. FAQ": "11. 常见问题（常见问题）",
            "12. Final Tips": "12. 最终建议（最终建议）",
            "\U0001f4da Related Guides": "相关指南",
            "Every guide is free — this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 6. All Skills Overview Guide 2026
    # =========================================================
    "osrs-all-skills-overview-guide-2026.html": {
        "cn_title": "OSRS 全技能概览：新手完整参考指南（2026版）",
        "cn_summary": "全面介绍OSRS所有23项技能的分类、训练方法和实际应用。从战斗技能到生产技能再到辅助技能，助你规划最佳升级路径，节省上百小时游戏时间。",
        "h_translations": {
            "Table of Contents": "目录",
            "Understanding Skill Categories": "了解技能分类（了解技能分类）",
            "The Three Pillar System": "三大支柱体系（三大支柱体系）",
            "Combat Skills (11 total)": "战斗技能（共11项）",
            "Production Skills (9 total)": "生产技能（共9项）",
            "Gathering & Support Skills (3 total)": "采集与辅助技能（共3项）",
            "Combat Skills Overview": "战斗技能概述（战斗技能概述）",
            "Attack Skill": "攻击技能（攻击技能）",
            "Strength Skill": "力量技能（力量技能）",
            "Defence Skill": "防御技能（防御技能）",
            "Hitpoints (HP) Skill": "生命值技能（生命值技能）",
            "Ranged Skill": "远程技能（远程技能）",
            "Magic Skill": "魔法技能（魔法技能）",
            "Prayer Skill": "祷告技能（祷告技能）",
            "Slayer Skill": "杀戮技能（杀戮技能）",
            "Production & Crafting Skills": "生产与制造技能（生产与制造技能）",
            "Cooking Skill": "烹饪技能（烹饪技能）",
            "Fishing Skill": "钓鱼技能（钓鱼技能）",
            "Woodcutting Skill": "伐木技能（伐木技能）",
            "Mining Skill": "采矿技能（采矿技能）",
            "Smithing Skill": "锻造技能（锻造技能）",
            "Crafting Skill": "工艺技能（工艺技能）",
            "Herblore Skill": "草药技能（草药技能）",
            "Fletching Skill": "制箭技能（制箭技能）",
            "Construction Skill": "建筑技能（建筑技能）",
            "Runecrafting Skill": "符文制作技能（符文制作技能）",
            "Support & Utility Skills": "辅助与实用技能（辅助与实用技能）",
            "Agility Skill": "敏捷技能（敏捷技能）",
            "Thieving Skill": "偷窃技能（偷窃技能）",
            "Firemaking Skill": "生火技能（生火技能）",
            "Recommended Skill Progression for Beginners": "新手推荐技能进展（新手推荐技能进展）",
            "Priority 1: Early Combat (Levels 1-40)": "优先级1：早期战斗（1-40级）",
            "Priority 2: Mid-Level Combat (Levels 40-70)": "优先级2：中级战斗（40-70级）",
            "Priority 3: Essential Support Skills (Concurrent)": "优先级3：必备辅助技能（并行）",
            "Priority 4: Money-Making Skills (Post-70 Combat)": "优先级4：赚钱技能（70级战斗后）",
            "Priority 5: Late-Game Specialization (99 Goals)": "优先级5：后期专精（99级目标）",
            "Recommended Early-Game Skill Order": "推荐的早期技能顺序（推荐的早期技能顺序）",
            "Real-World Skill Applications & Gold-Making Potential": "技能实际应用与赚钱潜力（技能实际应用与赚钱潜力）",
            "Combat-Focused Progression": "战斗专注型进展（战斗专注型进展）",
            "Production-Focused Progression": "生产专注型进展（生产专注型进展）",
            "Hybrid Progression": "混合型进展（混合型进展）",
            "Gathering-Focused Progression": "采集专注型进展（采集专注型进展）",
            "Quest & Achievement Progression": "任务与成就进展（任务与成就进展）",
            "Smart Profit Rotation Strategy": "智能利润轮换策略（智能利润轮换策略）",
            "F2P vs P2P Skill Access Comparison": "F2P与会员技能访问对比（F2P与会员技能访问对比）",
            "Final Tips for Skill Mastery": "技能精通最终建议（技能精通最终建议）",
            "Continue Your OSRS Journey": "继续你的OSRS之旅（继续你的OSRS之旅）",
            "Frequently Asked Questions": "常见问题（常见问题）",
            "What's the fastest skill to train to 99?": "哪项技能最快升到99？",
            "Which skill should I train first?": "应该先训练哪项技能？",
            "Are all 23 skills essential?": "所有23项技能都必需吗？",
            "How long does it take to reach 99 in each skill?": "每项技能升到99需要多长时间？",
            "What's the most profitable skill to train?": "最赚钱的技能是什么？",
            "Should I train all skills to 99?": "应该把所有技能升到99吗？",
            "Related Guides": "相关指南",
            "Every guide is free — this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 7. Best Quests Per Skill 2026
    # =========================================================
    "osrs-best-quests-per-skill-2026.html": {
        "cn_title": "OSRS 各技能最佳任务参考：完整任务奖励指南（2026版）",
        "cn_summary": "按技能分类的终极任务参考指南，列出每项OSRS任务对应的技能经验奖励。快速找出训练任意技能的最佳任务，包括战斗风格任务、赚钱任务及最优任务顺序。",
        "h_translations": {
            "Table of Contents": "目录",
            "1. Why Quest = Fastest Skill Training": "1. 为什么任务=最快技能训练（为什么任务=最快技能训练）",
            "\U0001f4ca Quest XP vs Grinding XP: The Numbers": "任务经验 vs 刷怪经验：数据对比",
            "\U0001f9ee The Math: When Quests Beat Grinding": "数学计算：任务何时优于刷怪",
            "2. Best Quests By Combat Style": "2. 按战斗风格的最佳任务（按战斗风格的最佳任务）",
            "\u2694\ufe0f Melee (Attack + Strength + Defence + Hitpoints)": "近战（攻击+力量+防御+生命值）",
            "\U0001f3f9 Ranged": "远程（远程）",
            "\U0001f52e Magic": "魔法（魔法）",
            "\U0001f64f Prayer": "祷告（祷告）",
            "\u2764\ufe0f Hitpoints": "生命值（生命值）",
            "3. Best Quests For Gathering Skills": "3. 采集技能的最佳任务（采集技能的最佳任务）",
            "\u26cf\ufe0f Mining": "采矿（采矿）",
            "\U0001f3a3 Fishing": "钓鱼（钓鱼）",
            "\U0001fa93 Woodcutting": "伐木（伐木）",
            "\U0001f331 Farming": "种植（种植）",
            "\U0001f3f9 Hunter": "狩猎（狩猎）",
            "4. Best Quests For Support Skills": "4. 辅助技能的最佳任务（辅助技能的最佳任务）",
            "\U0001f3c3 Agility": "敏捷（敏捷）",
            "\U0001f5e1\ufe0f Thieving": "偷窃（偷窃）",
            "\U0001f300 Runecraft": "符文制作（符文制作）",
            "\U0001f33f Herblore": "草药（草药）",
            "\U0001f528 Other Support Skills (Brief)": "其他辅助技能（简述）",
            "5. Best Money-Making Quest Unlocks": "5. 最佳赚钱任务解锁（最佳赚钱任务解锁）",
            "\U0001f4b0 Quests That Unlock Direct GP Rewards": "解锁直接金币奖励的任务",
            "\U0001f4b0 Quests That Unlock GP/h Methods (Indirect)": "解锁金币/小时方法的任务（间接）",
            "6. Multi-Skill Powerhouse Quests": "6. 多技能强力任务（多技能强力任务）",
            "\U0001f3c6 Top 10 Multi-Skill Quests (Ranked by Total XP Given)": "十大多技能任务（按总经验排名）",
            "7. Quest Difficulty vs Reward Analysis": "7. 任务难度与奖励分析（任务难度与奖励分析）",
            "\U0001f947 S-Tier Quests (Easy + High XP = Must Do FIRST)": "S级任务（简单+高经验=优先完成）",
            "\U0001f948 A-Tier Quests (Medium Difficulty + Good XP)": "A级任务（中等难度+不错经验）",
            "\U0001f949 B-Tier Quests (Harder + Moderate XP)": "B级任务（较难+中等经验）",
            "\U0001faaa C-Tier Quests (Hard + Low XP = Skip Unless Needed)": "C级任务（困难+低经验=非必需跳过）",
            "8. Complete Quick Reference Tables": "8. 完整快速参考表（完整快速参考表）",
            "\U0001f4ca By Skill (All Skills, Top 5 Quests Each)": "按技能（所有技能，每项前5个任务）",
            "\U0001f4ca By Total XP (All Quests Ranked)": "按总经验（所有任务排名）",
            "9. FAQ — Quest Training Questions": "9. 常见问题 — 任务训练问题",
            "\U0001f3af Your Quest Training Plan": "你的任务训练计划",
            "\U0001f4da Related Guides": "相关指南",
            "Every guide is free — this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 8. Cheapest 99 Runecrafting 2026
    # =========================================================
    "osrs-cheapest-99-runecrafting-2026.html": {
        "cn_title": "OSRS 最省钱的99级符文制作训练指南（2026版）",
        "cn_summary": "介绍三种最省钱的99级符文制作路线：熔岩符文（约800万金币）、ZMI（约2000万金币）和裂隙守护者（零成本），附完整经验速率、装备配置和成本分析。",
        "h_translations": {
            "\U0001f4d6 Runecrafting 1-99 -- Quick Reference": "符文制作1-99 -- 快速参考",
            "1. Quest Unlocks &amp; Pouches (Do These First)": "1. 任务解锁与袋子（优先完成）",
            "Essence Pouches": "精华袋子（精华袋子）",
            "2. Lava Runes -- The Cheapest Direct Method": "2. 熔岩符文 — 最省钱的直接方法",
            "Lava Runes Step-by-Step Process": "熔岩符文逐步流程（熔岩符文逐步流程）",
            "3-Tier Gear Setup for Lava Runes": "熔岩符文三级装备设置（熔岩符文三级装备设置）",
            "3. Guardians of the Rift (GOTR) -- The Zero-Cost Method": "3. 裂隙守护者（GOTR）— 零成本方法",
            "4. ZMI Altar -- Best XP, Moderate Cost": "4. ZMI祭坛 — 最佳经验，中等成本",
            "5. Full Method Comparison": "5. 全部方法对比（全部方法对比）",
            "Lava Runes Total Cost Breakdown to 99": "熔岩符文到99级总成本分解",
            "6. Early Level Progression (1-23)": "6. 早期等级进展（1-23级）",
            "7. Advanced Tips": "7. 进阶技巧（进阶技巧）",
            "8. Common Mistakes": "8. 常见错误（常见错误）",
            "9. Frequently Asked Questions": "9. 常见问题（常见问题）",
            "\U0001f4d6 Runecrafting -- The Marathon Skill": "符文制作 — 马拉松技能",
            "\U0001f4da Related Guides": "相关指南",
            "Related Guides": "相关指南",
            "Every guide is free — this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },

    # =========================================================
    # 9. Combat Training Beginner 2026
    # =========================================================
    "osrs-combat-training-beginner-2026.html": {
        "cn_title": "OSRS 战斗技能训练：新手1-99全指南（2026版）",
        "cn_summary": "从打哥布林到终局Boss战的完整战斗技能训练路线图，涵盖近战、远程、魔法三种战斗风格的精确训练地点、经验速率和装备推荐，专为2026年新玩家设计。",
        "h_translations": {
            "\u2460 Table of Contents": "目录",
            "1. Combat Basics \u2014 Understanding the Combat Triangle": "1. 战斗基础 — 理解战斗三角（战斗基础 — 理解战斗三角）",
            "\u2461 How Combat Level Is Calculated": "战斗等级如何计算（战斗等级如何计算）",
            "\u2462 Understanding Attack Speed (Ticks)": "理解攻击速度（游戏刻）（理解攻击速度（游戏刻））",
            "2. Core Training Principles Every Beginner Must Know": "2. 每个新手必须知道的核心训练原则",
            "\u2463 Principle 1: Attack > Strength > Defence Priority": "原则1：攻击 > 力量 > 防御优先级",
            "\u2464 Principle 2: Safe-Spotting = Free Training": "原则2：安全点位 = 免费训练",
            "\u2465 Principle 3: Aggressive Monsters Save you Time": "原则3：攻击性怪物节省时间",
            "\u2466 Principle 4: Quests Give Free Combat XP": "原则4：任务提供免费战斗经验",
            "3. Melee Training: Complete 1\u201370 Step-by-Step Route": "3. 近战训练：1-70级完整逐步路线",
            "\u2467 Step 1: Levels 1\u201310 (Chickens & Cows)": "步骤1：1-10级（鸡和牛）",
            "\u2468 Step 2: Levels 10\u201320 (Al-Kharid Warriors \u2014 F2P Option)": "步骤2：10-20级（阿尔卡里德战士 — F2P选项）",
            "\u2469 Step 3: Levels 20\u201340 (Barbarians or Stronghold of Security)": "步骤3：20-40级（野蛮人或安全堡垒）",
            "Step 4: Levels 40\u201360 (Flesh Crawlers or Hill Giants)": "步骤4：40-60级（血肉爬行者或丘陵巨人）",
            "Step 5: Levels 60\u201370 (Experiments or Rock Crabs)": "步骤5：60-70级（实验体或岩蟹）",
            "4. Melee Training: 70\u201399 Efficient Routes": "4. 近战训练：70-99级高效路线",
            "Method A: Slayer (Best Overall, 70\u201399)": "方法A：杀戮任务（综合最佳，70-99级）",
            "Method B: Nightmare Zone (NMZ) \u2014 AFK 99": "方法B：噩梦区（NMZ）— 挂机到99",
            "Method C: Manual Grinding (Fastest XP)": "方法C：手动刷怪（最快经验）",
            "5. Ranged Training: Complete 1\u201399 Route": "5. 远程训练：1-99级完整路线",
            "Levels 1\u201330: Chickens & Cows with Shortbow": "1-30级：用短弓打鸡和牛",
            "Levels 30\u201360: Rock Crabs (Members) or Ogress Warriors (F2P)": "30-60级：岩蟹（会员）或食人魔战士（F2P）",
            "Levels 60\u201370: Chinning or Slayer": "60-70级：使用 Chinchompa 或杀戮任务",
            "Levels 70\u201399: Slayer with Ranged": "70-99级：远程杀戮任务（远程杀戮任务）",
            "6. Magic Training: Complete 1\u201399 Route": "6. 魔法训练：1-99级完整路线",
            "Levels 1\u20137: Imp Catcher Quest (Instant XP)": "1-7级：小恶魔抓捕任务（即时经验）",
            "Levels 7\u201325: Splashing (AFK Method)": "7-25级：溅射（挂机方法）",
            "Levels 25\u201355: Superheat Item (Smithing XP + Money)": "25-55级：超高温物品（锻造经验+赚钱）",
            "Level 55+: High Level Alchemy (Passive Income)": "55+级：高级炼金术（被动收入）",
            "Levels 55\u201399: Combat Magic (Bursts/Barrages)": "55-99级：战斗魔法（爆发/弹幕法术）",
            "7. Complete 1\u201370 Combat Training Route Table (Step-by-Step)": "7. 1-70级战斗训练路线表（逐步）",
            "Melee Training Route (Attack / Strength / Defence)": "近战训练路线（攻击/力量/防御）",
            "Ranged Training Route": "远程训练路线（远程训练路线）",
            "Magic Training Route": "魔法训练路线（魔法训练路线）",
            "8. Best Monsters by Combat Level (Quick Reference)": "8. 按战斗等级的最佳怪物（快速参考）",
            "9. Gear Upgrade Milestones (Budget to Endgame)": "9. 装备升级里程碑（从经济到终局）",
            "\u2694\ufe0f Melee Gear Progression": "近战装备进展（近战装备进展）",
            "\U0001f3f9 Ranged Gear Progression": "远程装备进展（远程装备进展）",
            "\u2728 Magic Gear Progression": "魔法装备进展（魔法装备进展）",
            "10. When & How to Start Slayer \u2014 The Best Combat Training Method": "10. 何时及如何开始杀戮任务 — 最佳战斗训练方法",
            "Which Slayer Master to Use (by Combat Level)": "使用哪位杀戮大师（按战斗等级）",
            "How to Start Slayer (Step-by-Step)": "如何开始杀戮任务（逐步）",
            "11. Advanced Combat Training Methods (70+ Combat)": "11. 进阶战斗训练方法（70+战斗等级）",
            "Nightmare Zone (NMZ) \u2014 AFK Melee 60k\u201380k XP/hr": "噩梦区（NMZ）— 挂机近战6万-8万经验/小时",
            "Bursting/Barraging \u2014 Magic 100k\u2013300k XP/hr": "爆发/弹幕 — 魔法10万-30万经验/小时",
            "Chinning \u2014 Ranged 200k\u2013300k XP/hr": "Chinchompa — 远程20万-30万经验/小时",
            "Cannon \u2014 +30% XP Boost (Costs GP)": "加农炮 — +30%经验加成（消耗金币）",
            "12. Combat Training FAQs \u2014 15 Questions Every Beginner Asks": "12. 战斗训练常见问题 — 每个新手都会问的15个问题",
            "Final Tips \u2014 Combat Training for Beginners": "最终建议 — 新手战斗训练",
            "\U0001f5e1\ufe0f What to Do After This Guide": "看完本指南后做什么",
            "\U0001f4da Related Guides": "相关指南",
            "Every guide is free — this one stays free either way.": "每篇指南都免费 — 这篇也是如此。",
        }
    },
}


def add_cn_format(filename, cn_title, cn_summary, h_translations):
    """为单个HTML文件添加M+中文格式"""
    filepath = os.path.join(GUIDES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  [SKIP] 文件不存在: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # --- 步骤1: 添加中文H1和导语 ---

    # 中文H1
    cn_h1_html = f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title}</h1>'

    # 中文导语
    cn_summary_html = f'<p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>'

    # 对于大多数文件，在guide-hero区域的英文H1前插入
    # 优先匹配 guide-hero 里的 <h1>
    # 对于 osrs-all-skills-overview-guide-2026.html，结构不同，在 <h1> 前插入
    # 对于 osrs-1-99-prayer-guide-all-methods-2026.html，在 <div class="guide-header"> 里的 <h1> 前插入

    hero_patterns = [
        # 旧结构: <section class="guide-hero"> ... <h1>...</h1>
        (r'(<section class="guide-hero">.*?)(<h1[^>]*>)', lambda m: m.group(1) + cn_h1_html + '\n            ' + m.group(2)),
        # ALL SKILLS 结构: <h1> 前无 hero-section，直接在 <article class="guide-content"> 里
        (r'(<article class="guide-content">.*?)(<h1[^>]*>)', lambda m: m.group(1) + cn_h1_html + '\n' + m.group(2)),
        # ALL METHODS 结构: <div class="guide-header"> ... <h1>...</h1>
        (r'(<div class="guide-header">.*?)(<h1[^>]*>)', lambda m: m.group(1) + cn_h1_html + '\n      ' + m.group(2)),
    ]

    for pattern, repl_fn in hero_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, repl_fn, content, flags=re.DOTALL)
            print(f"  [OK] 已添加中文H1")
            break
    else:
        print(f"  [WARN] 未找到匹配的H1插入位置")

    # 在中文H1之后插入中文导语
    cn_h1_pattern = r'(<h1 class="cn-title"[^>]*>.*?</h1>)'
    cn_h1_match = re.search(cn_h1_pattern, content, re.DOTALL)
    if cn_h1_match:
        content = content.replace(
            cn_h1_match.group(1),
            cn_h1_match.group(1) + '\n' + cn_summary_html
        )
        print(f"  [OK] 已添加中文导语")

    # --- 步骤2: 为H2/H3添加中文翻译 ---

    # 构建最长的匹配优先的排序
    sorted_headings = sorted(h_translations.keys(), key=len, reverse=True)

    for eng_text in sorted_headings:
        cn_text = h_translations[eng_text]

        # 处理 H2 和 H3，需要区分大小写且不匹配TOC/Related等内部
        # 匹配 <h2>内容</h2> 或 <h3>内容</h3>，但跳过已有 cn-title 的
        # 也跳过已经有中文括号翻译的
        def replace_heading(m):
            full_tag = m.group(0)
            tag_name = m.group(1)  # h2 or h3
            inner = m.group(2)

            # 跳过已经包含中文翻译的 (已经有中文括号的)
            if '（' in inner and '）' in inner:
                return full_tag

            # 跳过 support card 里的
            if 'Every guide is free' in inner:
                return full_tag

            # 替换
            new_inner = inner.replace(eng_text, cn_text)
            if new_inner != inner:
                return f'<{tag_name}>{new_inner}</{tag_name}>'
            return full_tag

        # 创建正则: 匹配该标题文本作为h2或h3的完整内容
        # 需要使用 re.escape 但保留 &amp; 等实体的匹配
        escaped_eng = re.escape(eng_text)
        # 对 &amp; 等实体做宽松匹配
        escaped_eng = escaped_eng.replace(r'\&amp\;', '&amp;')

        pattern = rf'(<h([23])(?: [^>]*)?>)' + re.escape(eng_text) + r'(\s*</h\2>)'
        new_content = re.sub(pattern, lambda m: f'<h{m.group(2)}{"" if m.group(1).endswith(">") and " " not in m.group(1)[3:-1] else m.group(1)[3:] if " " in m.group(1) else ""}>{cn_text}</h{m.group(2)}>', content)
        if new_content != content:
            content = new_content

    # 对带样式的标签也做替换
    for eng_text in sorted_headings:
        cn_text = h_translations[eng_text]
        # 匹配 <h2 style="...">内容</h2>
        for tag in ['h2', 'h3']:
            p = re.compile(rf'(<{tag}[^>]*>)' + re.escape(eng_text) + r'(\s*</' + tag + r'>)')
            content = p.sub(lambda m: m.group(1) + cn_text + m.group(2), content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [DONE] 文件已更新: {filename}")
        return True
    else:
        print(f"  [NOCHANGE] 无更改: {filename}")
        return False


def main():
    os.chdir(GUIDES_DIR)
    success = []
    failed = []

    for fname, data in file_data.items():
        print(f"\n处理文件: {fname}")
        try:
            ok = add_cn_format(fname, data["cn_title"], data["cn_summary"], data["h_translations"])
            if ok:
                success.append(fname)
            else:
                failed.append(fname)
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed.append(fname)

    print(f"\n{'='*50}")
    print(f"处理完成: 成功 {len(success)}, 失败 {len(failed)}")
    if success:
        print(f"已更新: {', '.join(success)}")
    if failed:
        print(f"失败: {', '.join(failed)}")

if __name__ == '__main__':
    main()
