#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为OSRS攻略HTML文件添加M+格式（中文H1+导语+章节标题中文翻译）"""

import re
import sys

GUIDES_DIR = "C:/Users/Lenovo/osrs-guide-site/zh/guides"

# ============================================================
# 配置文件：每个文件的 中文H1 / 导语 / H2翻译 / H3翻译
# ============================================================

# Combat Achievements 已处理完成，这里从其他8个文件开始

FILE_CONFIGS = {
    "max-cape-route-2026.html": {
        "cn_h1": "OSRS 最大技能披风高效路线2026 — 从新手到满级创纪录时间",
        "cn_summary": "最全面的OSRS最大技能披风路线图！本指南覆盖最优任务顺序、技能优先级别、各等级段最佳训练方法、铁人模式差异、每日和每周例行任务安排。从教程岛到最大技能披风，一站式全攻略。",
        "h2": {
            "Overall Strategy & Philosophy": "整体策略与理念",
            "Prerequisites \u2014 What You Need Before Starting": "前置条件 — 开始前需要准备什么",
            "Optimal Quest Order for Maximum XP Rewards": "最优任务顺序获取最大经验奖励",
            "Skill Priority Order \u2014 Which Skills to Train When": "技能优先顺序 — 何时训练哪些技能",
            "Combat Skills Training Route (Attack/Strength/Defence/Ranged/Magic)": "战斗技能训练路线（攻击/力量/防御/远程/魔法）",
            "Prayer Training Route": "祈祷技能训练路线",
            "All 23 Skills \u2014 Best Methods by Level Bracket": "全部23种技能 — 各等级段最佳方法",
            "AFK vs Active Training Balance": "挂机与主动训练平衡",
            "Money-Making Interspersed Strategy": "穿插赚钱策略",
            "Ironman Differences \u2014 What Changes": "铁人模式差异 — 什么变了",
            "Estimated Timeframes & Milestones": "预估时间与里程碑",
            "Daily & Weekly Routines for Maximum Efficiency": "每日和每周例行任务最大化效率",
            "Related Guides": "相关指南",
        },
        "h3": {
            "Account Setup": "账号设置",
            "Essential Unlocks (Do These First)": "必需解锁（先做这些）",
            "Phase 1: No Requirements (Start Here)": "阶段1：无要求（从这里开始）",
            "Phase 2: Mid-Game Quests (Combat ~40-60)": "阶段2：中局任务（战斗等级约40-60）",
            "Phase 3: Late-Game Quests (Combat ~70+)": "阶段3：后期任务（战斗等级约70+）",
            "Recommended Priority Order": "推荐优先顺序",
            "Attack & Strength (Levels 1-99)": "攻击与力量（1-99级）",
            "Ranged (Levels 1-99)": "远程（1-99级）",
            "Magic (Levels 1-99)": "魔法（1-99级）",
            "1. Agility": "1. 敏捷",
            "2. Herblore": "2. 草药学",
            "3. Thieving": "3. 偷窃",
            "4. Hunter": "4. 猎人",
            "5. Construction": "5. 建造",
            "AFK-Friendly Skills (Train While Doing Other Things)": "适合挂机的技能（边做其他事边训练）",
            "Active-Focus Skills (Require Attention)": "需要专注的技能（需要注意力）",
            "Balanced Daily Schedule (Example)": "平衡的每日安排（示例）",
            "Early Game Money (First 200 Hours)": "早期赚钱（前200小时）",
            "Mid Game Money (200-1000 Hours in)": "中期赚钱（200-1000小时）",
            "Late Game Money (1000+ Hours in)": "后期赚钱（1000+小时）",
            "Key Differences": "关键差异",
            "Ironman-Specific Strategy Changes": "铁人模式特有策略变化",
            "Daily Routines (Do Every Day)": "每日例行任务（每天做）",
            "Weekly Routines (Do Every Week)": "每周例行任务（每周做）",
            "Sample Weekly Schedule (Efficient Main)": "示例每周安排（高效主号）",
        }
    },
    "osrs-1-99-crafting-guide-2026.html": {
        "cn_h1": "OSRS 1-99 制作技能指南2026 — 快速、便宜与铁人模式方法",
        "cn_summary": "完整OSRS 1-99制作技能训练指南！全面对比玻璃吹制、战斗法杖、珠宝制作、龙皮 crafting 等所有方法，包含经验速率、成本分析以及铁人模式专属策略。无论你是追求最快速度、最低成本还是利润最大化，这里都有适合你的路线。",
        "h2": {
            "1. Crafting Overview & Core Mechanics": "1. 制作技能概述与核心机制",
            "2. Quest & Achievement XP Rewards": "2. 任务与成就经验奖励",
            "3. Glassblowing \u2014 Best Ironman Method (120K XP/hr)": "3. 玻璃吹制 — 最佳铁人模式方法（每小时12万经验）",
            "4. Battlestaves \u2014 Profitable Training (100K-180K XP/hr)": "4. 战斗法杖 — 可赚钱的训练（每小时10-18万经验）",
            "5. Jewelry Crafting \u2014 Semi-AFK Method (30K-80K XP/hr)": "5. 珠宝制作 — 半挂机方法（每小时3-8万经验）",
            "6. Dragonhide Crafting \u2014 Fastest XP (250K-350K XP/hr)": "6. 龙皮制作 — 最快经验（每小时25-35万经验）",
            "7. Gem Cutting \u2014 Beginner Friendly (50K-100K XP/hr)": "7. 宝石切割 — 新手友好（每小时5-10万经验）",
            "8. Other Methods \u2014 Pottery, Leather, Spinning": "8. 其他方法 — 陶器、皮革、纺线",
            "9. All Methods Comparison Table": "9. 所有方法对比表",
            "10. Ironman 1-99 Crafting Strategy": "10. 铁人模式1-99制作技能策略",
            "11. Level Milestones & Key Unlocks": "11. 等级里程碑与关键解锁",
            "12. Cost & Profit Analysis": "12. 成本与利润分析",
            "13. Pro Tips for Maximum Efficiency": "13. 最大化效率的专业技巧",
            "14. FAQ": "14. 常见问题解答",
            "Related Guides": "相关指南",
        },
        "h3": {
            "Why Train Crafting?": "为什么要训练制作技能？",
            "Core Training Categories": "核心训练类别",
            "How to Get Raw Materials": "如何获取原材料",
            "Superglass Make Method (77 Magic Required)": "超级玻璃制造方法（需要77级魔法）",
            "Glassblowing XP Table": "玻璃吹制经验表",
            "Battlestaff Profit Calculator": "战斗法杖利润计算器",
            "Optimal Battlestaff Training Route": "最优战斗法杖训练路线",
            "XP Per Jewelry Item": "每件珠宝经验",
            "AFK Jewelry Crafting Setup": "挂机珠宝制作设置",
            "Dragonhide XP Table": "龙皮经验表",
            "Optimal Strategy": "最优策略",
            "Where to Craft": "在哪里制作",
            "Gem Cutting XP Table": "宝石切割经验表",
            "Pottery (1-20)": "陶器（1-20级）",
            "Leather Crafting (1-46)": "皮革制作（1-46级）",
            "Spinning (1-10)": "纺线（1-10级）",
            "Early Game (1-46)": "前期（1-46级）",
            "Mid Game (46-87) \u2014 Giant Seaweed + Superglass Make": "中期（46-87级）— 巨型海藻+超级玻璃制造",
            "Late Game (87-99)": "后期（87-99级）",
            "Ironman Material Requirements to 99": "铁人模式冲99级所需材料",
            "Budget Route to 99 (~5M GP)": "预算路线冲99（约500万GP）",
            "Fast Route to 99 (~50M GP)": "快速路线冲99（约5000万GP）",
            "Profit-Focused Route (~20M GP)": "利润导向路线（约2000万GP）",
            "Q: How long does 1-99 Crafting take?": "问：1-99制作技能需要多长时间？",
            "Q: What\u2019s the best method for Ironman?": "问：铁人模式的最佳方法是什么？",
            "Q: Is Crafting expensive to train?": "问：训练制作技能贵吗？",
            "Q: When should I stop glassblowing and switch to something faster?": "问：什么时候应该停止玻璃吹制转用更快的方法？",
            "Q: What\u2019s the best Crafting item for profit?": "问：最佳赚钱的制作物品是什么？",
            "Q: Can I train Crafting on F2P?": "问：我可以在免费模式下训练制作技能吗？",
            "Q: Do I need Crafting for any important quests?": "问：制作技能对重要任务有必要吗？",
        }
    },
    "osrs-1-99-hitpoints-guide-2026.html": {
        "cn_h1": "OSRS 1-99 生命值技能指南2026 — 训练方法与升级路线",
        "cn_summary": "完整OSRS生命值技能训练指南！生命值是所有战斗技能的基础，本指南详细解析被动升级机制、最快主动训练方法、AFK挂机方案以及铁人模式专属策略。包含各等级段经验速率和实用技巧。",
        "h2": {
            "Why Hitpoints Is Different": "为什么生命值不同",
            "Passive Hitpoints Training (The Default Method)": "被动生命值训练（默认方法）",
            "Active Hitpoints Training (Faster Methods)": "主动生命值训练（更快方法）",
            "Hitpoints XP Rates Comparison": "生命值经验速率对比",
            "Hitpoints Training by Account Type": "按账号类型的生命值训练",
            "Hitpoints Milestones & Unlocks": "生命值里程碑与解锁",
            "Related Guides": "相关指南",
        },
        "h3": {
            "What Makes Hitpoints Unique": "生命值的独特之处",
            "Why Train Hitpoints Actively?": "为什么主动训练生命值？",
            "Combat Training (Most Efficient)": "战斗训练（最高效）",
            "Slayer (Recommended Method)": "杀戮任务（推荐方法）",
            "Bossing (Best High-Level Method)": "BOSS战（最佳高级方法）",
            "Splashing / Bursting (Magic XP + HP)": "溅射/爆发（魔法经验+生命值）",
            "Cannon Training (Ranged + HP)": "大炮训练（远程+生命值）",
            "Nightmare Zone (AFK HP Training)": "梦魇空间（挂机生命值训练）",
            "Pest Control (Mini-Game)": "害虫控制（小游戏）",
            "Chinning (Ranged + HP, Very Fast)": "奇宁（远程+生命值，非常快）",
            "Bursting/Barraging (Magic + HP)": "爆发/弹幕（魔法+生命值）",
            "Main Accounts": "主账号",
            "Ironman Accounts": "铁人模式账号",
            "Pure / PK Accounts": "纯净/PK账号",
            "Key HP Milestones": "关键生命值里程碑",
        }
    },
    "osrs-1-99-hitpoints-training-guide-2026.html": {
        "cn_h1": "OSRS 1-99 生命值训练指南2026 — 最快升级路线与方法对比",
        "cn_summary": "最详细的OSRS生命值训练路线指南！从1到99级，涵盖所有主流训练方法包括梦魇空间挂机、爆发训练、斯拉任务等，附精确经验速率、GP成本分析和各账号类型推荐方案。",
        "h2": {
            "Why Hitpoints Training Matters": "为什么生命值训练很重要",
            "Passive Hitpoints Gain from Combat": "从战斗中获得被动生命值",
            "Active Hitpoints Training Methods": "主动生命值训练方法",
            "Method Comparison Table (All Methods)": "方法对比表（所有方法）",
            "Best Hitpoints Training by Account Type": "按账号类型最佳生命值训练",
            "Recommended Leveling Roadmap": "推荐升级路线图",
            "Related Guides": "相关指南",
        },
        "h3": {
            "Why You Should Care About HP Training": "为什么你该关注生命值训练",
            "HP Training vs Other Combat Skills": "生命值训练 vs 其他战斗技能",
            "Standard Combat Training (1-99)": "标准战斗训练（1-99级）",
            "Nightmare Zone (AFK Method)": "梦魇空间（挂机方法）",
            "Bursting / Barraging Slayer Tasks": "爆发/弹幕杀戮任务",
            "Chinning (Ranged + HP Combo)": "奇宁（远程+生命值组合）",
            "Pest Control (Low-Intensity Mini-Game)": "害虫控制（低强度小游戏）",
            "Splashing (Cheap Magic + HP)": "溅射（便宜的魔法+生命值）",
            "Cannon Slayer (Ranged + HP)": "大炮杀戮（远程+生命值）",
            "Main Account (Efficient Route)": "主账号（高效路线）",
            "Ironman Account": "铁人模式账号",
            "Pure / Low-Level Account": "纯净/低等级账号",
            "Level 1-50 (Early Game)": "1-50级（前期）",
            "Level 50-80 (Mid Game)": "50-80级（中期）",
            "Level 80-99 (Late Game)": "80-99级（后期）",
        }
    },
    "osrs-1-99-hunter-guide-2026.html": {
        "cn_h1": "OSRS 1-99 猎人技能指南2026 — 最快方法、经验速率与利润",
        "cn_summary": "猎人技能是OSRS中最赚钱的技能之一，同时也是最快的99级技能之一！本完整指南覆盖从一号铜尾鸟到黑色奇奇帕蛙的每个等级范围，包含经验速率、利润分析、挂机替代方案以及各玩法风格的装备配置。",
        "h2": {
            "\u2460 \U0001f48e Why Train Hunter? (Profit + Diary Requirements)": "\u2460 为什么要训练猎人？（利润+日志要求）",
            "\u2461 \U0001f6e1\ufe0f Hunter Gear & Setup Checklist": "\u2461 猎人装备与设置清单",
            "\u2462 \U0001f331 Levels 1-9: Starting Out (Copper Longtail)": "\u2462 1-9级：开始（铜尾鸟）",
            "\u2463 \U0001f426 Levels 9-43: Early Methods (Wagtail/Ruby Harvest/Ferret/Lizard)": "\u2463 9-43级：早期方法（鹡鸰/红宝石收获/雪貂/蜥蜴）",
            "\u2464 \U0001f985 Levels 43-53: Falconry (Fast & Fun)": "\u2464 43-53级：鹰猎（快速且有趣）",
            "\u2465 \U0001f42d Levels 53-63: Grey Chinchompas (First Profit)": "\u2465 53-63级：灰色奇奇帕蛙（第一次赚钱）",
            "\u2466 \U0001f98a Levels 63-80: Red Chinchompas (Big Money)": "\u2466 63-80级：红色奇奇帕蛙（大钱）",
            "\u2467 \U0001f3ae 3-Tick Hunter Manipulation \u2014 Step-by-Step Guide": "\u2467 3刻猎人操作 — 分步指南",
            "\u2468 \u2b1b Levels 80-99: Black Chinchompas vs Herbiboar vs Bird Houses": "\u2468 80-99级：黑色奇奇帕蛙 vs 草药野猪 vs 鸟屋",
            "\u2469 \U0001f3af Hunter Rumours Complete Guide (2025 Update)": "\u2469 猎人传闻完整指南（2025更新）",
            "\u246a \U0001f4ca XP Rates & Profit Comparison Table": "\u246a 经验速率与利润对比表",
            "\u246b \U0001f504 Alternative Methods (AFK/Ironman/Mobile)": "\u246b 替代方法（挂机/铁人/手机）",
            "\u246c \U0001f3a3 Drift Net Fishing \u2014 Dual Skill Training (44H + 47F)": "\u246c 漂流网捕鱼 — 双技能训练（44猎人+47钓鱼）",
            "\u246d \u2753 FAQ": "\u246d 常见问题解答",
            "\u246e \U0001f3c6 Final Tips": "\u246e 最终建议",
        },
        "h3": {
            "\U0001f4b0 Massive Profit Potential": "巨大利润潜力",
            "\U0001f4dc Achievement Diary Requirements": "成就日志要求",
            "\u26a1 Fastest 99 \u2014 Where Hunter Ranks": "最快的99级 — 猎人排名",
            "\U0001f455 Weight-Reducing Gear (Mandatory)": "减重装备（必选）",
            "\U0001f9f0 Essential Hunter Tools": "必备猎人工具",
            "\U0001f5fa\ufe0f Important Teleports": "重要传送点",
            "\U0001f426 Method 1: Crimson Swifts (Levels 1\u20139)": "方法1：红速鸟（1-9级）",
            "\U0001f5fa\ufe0f Alternative: Varrock Museum Quiz (Skip Levels 1\u20139)": "替代方案：Varrock博物馆问答（跳过1-9级）",
            "\U0001f426 Method 1: Tropical Wagtails (Levels 9\u201319)": "方法1：热带鹡鸰（9-19级）",
            "\U0001f98b Method 2: Ruby Harvest (Levels 15\u201329)": "方法2：红宝石收获（15-29级）",
            "\U0001f9f0 Method 3: Ferrets (Levels 27\u201343, Falconry Prep)": "方法3：雪貂（27-43级，鹰猎准备）",
            "\U0001f98e Method 4: Salamanders (Levels 29\u201343)": "方法4：蜥蜴（29-43级）",
            "\U0001f3af How Falconry Works": "鹰猎如何运作",
            "\U0001f3af Falconry XP Rates": "鹰猎经验速率",
            "\U0001f4a1 Tips for Falconry": "鹰猎技巧",
            "\U0001f42d Grey Chinchompa Strategy": "灰色奇奇帕蛙策略",
            "\U0001f4b0 Profit Analysis": "利润分析",
            "\U0001f98a Red Chinchompa Strategy": "红色奇奇帕蛙策略",
            "\U0001f4b5 Profit Maximization": "利润最大化",
            "\U0001f3ae What Is 3-Tick Manipulation?": "什么是3刻操作？",
            "\U0001f3ae Step-by-Step 3-Tick Chinchompa Method": "分步3刻奇奇帕蛙方法",
            "\u26a0\ufe0f Difficulty Warning": "难度警告",
            "\u2b1b Black Chinchompas (73+ Hunter, Wilderness)": "黑色奇奇帕蛙（73+猎人，荒野）",
            "\U0001f427 Herbiboar (80+ Hunter, Fossil Island)": "草药野猪（80+猎人，化石岛）",
            "\U0001f426 Bird Houses (Passive XP)": "鸟屋（被动经验）",
            "\U0001f3af What Are Hunter Rumours?": "什么是猎人传闻？",
            "\U0001f3af How Hunter Rumours Work": "猎人传闻如何运作",
            "\U0001f4b0 Rewards & Benefits": "奖励与收益",
            "\U0001f4ca XP Rates & Profit Table": "经验速率与利润表",
            "\U0001f504 AFK Methods": "挂机方法",
            "\U0001f4f1 Mobile-Friendly Methods": "手机友好方法",
            "\U0001f9d1\u200d\U0001f3ed Ironman-Specific Strategies": "铁人模式专属策略",
            "\U0001f3a3 How Drift Net Fishing Works": "漂流网捕鱼如何运作",
            "\U0001f3a3 Requirements & Setup": "要求与设置",
            "\U0001f3a3 XP Rates & Strategy": "经验速率与策略",
            "\U0001f3c6 Final Pro Tips": "最终专业建议",
        }
    },
    "osrs-1-99-hunter-guide-afk-method.html": {
        "cn_h1": "OSRS 猎人技能挂机方法指南 — 低强度训练方案",
        "cn_summary": "寻找OSRS猎人技能的低强度训练方法？本指南专门介绍各种挂机/半挂机猎人训练方案，包括鸟屋被动经验、箱式陷阱设置、漂流网捕鱼双技能训练等。适合边看视频边玩或多账号操作的玩家。",
        "h2": {
            "AFK Hunter Methods Overview": "挂机猎人方法概述",
            "Bird House Runs (Best Passive XP)": "鸟屋跑（最佳被动经验）",
            "Box Trap AFK Methods": "箱式陷阱挂机方法",
            "Drift Net Fishing (Dual Skill AFK)": "漂流网捕鱼（双技能挂机）",
            "Herbiboar (Semi-AFK)": "草药野猪（半挂机）",
            "AFK Method Comparison Table": "挂机方法对比表",
            "Related Guides": "相关指南",
        },
        "h3": {
            "Why Go AFK for Hunter?": "为什么选择猎人挂机？",
            "AFK vs Active XP Rates": "挂机 vs 主动经验速率",
            "Bird House Mechanics": "鸟屋机制",
            "Optimal Bird House Route": "最优鸟屋路线",
            "Bird House XP & Profit": "鸟屋经验与利润",
            "Grey Chinchompas (Semi-AFK)": "灰色奇奇帕蛙（半挂机）",
            "Red Chinchompas (Low Intensity)": "红色奇奇帕蛙（低强度）",
            "Drift Net Setup": "漂流网设置",
            "Drift Net Strategy": "漂流网策略",
            "Herbiboar Route Guide": "草药野猪路线指南",
            "Herbiboar XP Rates": "草药野猪经验速率",
            "Quick Comparison": "快速对比",
            "Best AFK Method by Playstyle": "按玩法推荐最佳挂机方法",
        }
    },
    "osrs-1-99-magic-training-cheap-guide-2026.html": {
        "cn_h1": "OSRS 1-99 魔法训练省钱指南2026 — 低成本升级路线",
        "cn_summary": "想省钱练魔法技能？本指南专注OSRS最便宜的魔法训练方法！从溅射法到爆发训练，从高精炼到战斗法杖附魔，覆盖所有低成本的1-99升级路线。包含每10万经验的GP成本对比，帮助精打细算的玩家找到最划算的方案。",
        "h2": {
            "Why Train Magic on a Budget?": "为什么要省钱训练魔法？",
            "Cheapest Magic Training Methods (Lowest GP/XP)": "最便宜的魔法训练方法（最低GP/经验比）",
            "Mid-Range Cost Methods": "中等成本方法",
            "Expensive but Fast Methods (For Reference)": "昂贵但快速的方法（供参考）",
            "Method Cost Comparison Table": "方法成本对比表",
            "Best Budget Route to 99": "最佳省钱路线冲99",
            "Magic Training by Account Type": "按账号类型的魔法训练",
            "Related Guides": "相关指南",
        },
        "h3": {
            "What Makes a Method \u2018Cheap\u2019?": "什么方法算'便宜'？",
            "Budget vs Fast: The Trade-Off": "省钱 vs 快速：权衡取舍",
            "Splashing (Level 1-99, ~0 GP/hr)": "溅射（1-99级，约0 GP/小时）",
            "Curse/Alchemy (Level 1-99, Profitable)": "诅咒/高精炼（1-99级，可赚钱）",
            "Bolt Enchanting (Level 4-99, Profitable)": "箭矢附魔（4-99级，可赚钱）",
            "Superglass Make (Level 77-99, Profitable)": "超级玻璃制造（77-99级，可赚钱）",
            "String Jewelry (Level 7-99, Cheap)": "串珠宝（7-99级，便宜）",
            "Plank Make (Level 86-99, Profitable)": "木板制造（86-99级，可赚钱）",
            "Bursting Dust Devils (Level 55-99)": "爆发沙尘恶魔（55-99级）",
            "Barraging Slayer Tasks (Level 70-99)": "弹幕杀戮任务（70-99级）",
            "High-Level Alchemy (Level 55-99)": "高等级炼金术（55-99级）",
            "Stun/Alching (Level 80-99)": "眩晕/炼金（80-99级）",
            "String Jewelry (Level 80-99)": "串珠宝（80-99级）",
            "Telegrab (Level 33-99)": "远程抓取（33-99级）",
            "Complete Cost Table 1-99": "完整成本表1-99",
            "Budget Route (0-10M GP Total)": "预算路线（总计0-1000万GP）",
            "Balanced Route (10-50M GP Total)": "平衡路线（总计1000万-5000万GP）",
            "Main Account": "主账号",
            "Ironman Account": "铁人模式账号",
            "Pure Account": "纯净账号",
        }
    },
    "osrs-1-99-mining-guide-beginner-2026.html": {
        "cn_h1": "OSRS 1-99 采矿指南新手版2026 — 初学者友好训练路线",
        "cn_summary": "专为OSRS初学者打造的采矿技能1-99完整指南！从入门级铜锡矿到高级母矿脉，涵盖AFK友好方法、升级路线、装备推荐和赚钱技巧。包含各等级段最佳矿脉选择、经验速率对比和铁人模式策略。",
        "h2": {
            "Why Train Mining?": "为什么要训练采矿？",
            "Mining Quick-Start Guide (Levels 1-15)": "采矿快速入门指南（1-15级）",
            "Iron & Silver Power Mining (Levels 15-30)": "铁与银快速采矿（15-30级）",
            "Motherlode Mine (Levels 30-99, AFK Method)": "母矿脉（30-99级，挂机方法）",
            "Blast Mining (Levels 75-99, Fast XP)": "爆破采矿（75-99级，快速经验）",
            "Gem Rocks (Alternative Method)": "宝石矿（替代方法）",
            "Volcanic Mine (Group Mining, High XP)": "火山矿（组队采矿，高经验）",
            "Mining XP Rates Comparison Table": "采矿经验速率对比表",
            "Best Mining Route by Account Type": "按账号类型最佳采矿路线",
            "Mining Gear & Equipment Guide": "采矿装备指南",
            "Related Guides": "相关指南",
        },
        "h3": {
            "Mining Level Milestones & Unlocks": "采矿等级里程碑与解锁",
            "Key Mining Terminology": "关键采矿术语",
            "Why You Should Start Mining Early": "为什么你应该早期开始采矿",
            "Method 1: Copper & Tin (Levels 1-15)": "方法1：铜与锡（1-15级）",
            "Method 2: Quest XP (Fast Track)": "方法2：任务经验（快速通道）",
            "Iron Power Mining Setup": "铁快速采矿设置",
            "Motherlode Mine Basics": "母矿脉基础",
            "Motherlode Mine Strategy": "母矿脉策略",
            "Motherlode Mine Rewards": "母矿脉奖励",
            "Blast Mining Setup": "爆破采矿设置",
            "Blast Mining Strategy": "爆破采矿策略",
            "Gem Rock Locations": "宝石矿位置",
            "Gem Mining Strategy": "宝石采矿策略",
            "Volcanic Mine Requirements": "火山矿要求",
            "Volcanic Mine Strategy": "火山矿策略",
            "Best for Main Accounts (Fastest XP)": "主账号最佳（最快经验）",
            "Best for Ironman Accounts": "铁人模式账号最佳",
            "Best for AFK/Passive Play": "挂机/被动玩法最佳",
            "Pickaxes by Level": "按等级的镐子",
            "Graceful Outfit (Weight Reduction)": "优雅套装（减重）",
            "Varrock Armor (Bonus Ore)": "Varrock护甲（额外矿石）",
            "Prospector Kit (Motherlode Mine)": "探矿者套装（母矿脉）",
        }
    },
}


def process_file(filename):
    """处理单个HTML文件，添加M+格式"""
    filepath = GUIDES_DIR + "/" + filename
    config = FILE_CONFIGS[filename]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 在guide-hero区域、原有英文H1之前，加中文H1
    cn_h1_html = '<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">' + config["cn_h1"] + '</h1>'
    cn_summary_html = '<p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">' + config["cn_summary"] + '</p>'

    hero_h1 = re.search(r'(<section class="guide-hero">.*?)(<h1\b)', content, re.DOTALL)
    if hero_h1:
        insert_point = hero_h1.start(2)
        insert_block = cn_h1_html + '\n            ' + cn_summary_html + '\n            '
        content = content[:insert_point] + insert_block + content[insert_point:]
        print("  [OK] 已插入中文H1和导语")
    else:
        print("  [WARN] 未找到guide-hero中的H1")

    # 2. 给所有H2标题加（中文翻译）
    h2_count = 0
    for eng_title, cn_title in config["h2"].items():
        escaped_eng = re.escape(eng_title)
        pattern = re.compile(r'(<h2[^>]*>)' + escaped_eng + r'(</h2>)')
        def make_repl(en=eng_title, cn=cn_title):
            return lambda m: m.group(1) + en + '\uff08' + cn + '\uff09' + m.group(2)
        new_content = pattern.sub(make_repl(), content)
        if new_content != content:
            h2_count += 1
            content = new_content
        else:
            print("  [H2-] 未匹配: " + eng_title[:50])

    # 3. 给所有H3标题加（中文翻译）
    h3_count = 0
    for eng_title, cn_title in config["h3"].items():
        escaped_eng = re.escape(eng_title)
        pattern = re.compile(r'(<h3[^>]*>)' + escaped_eng + r'(</h3>)')
        def make_repl(en=eng_title, cn=cn_title):
            return lambda m: m.group(1) + en + '\uff08' + cn + '\uff09' + m.group(2)
        new_content = pattern.sub(make_repl(), content)
        if new_content != content:
            h3_count += 1
            content = new_content

    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("  [OK] " + filename + ": H1已加, " + str(h2_count) + "个H2翻译, " + str(h3_count) + "个H3翻译")
    return h2_count, h3_count


def main():
    total_h2 = 0
    total_h3 = 0
    for filename in FILE_CONFIGS:
        print("\n>>> " + filename)
        h2c, h3c = process_file(filename)
        total_h2 += h2c
        total_h3 += h3c
    print("\n=== 全部处理完成！共处理 " + str(len(FILE_CONFIGS)) + " 个文件 ===")
    print("总计添加 H2 翻译: " + str(total_h2) + " 个")
    print("总计添加 H3 翻译: " + str(total_h3) + " 个")

if __name__ == "__main__":
    main()
