#!/usr/bin/env python3
"""
Process 15 OSRS guide files for Group 2.
Adds Chinese translations while preserving English source, support card, PayPal, footer, CSS.
"""

import re
import os

BASE = "c:/Users/Lenovo/osrs-guide-site"

# Files to process
FILES = [
    "osrs-gear-inflation-guide-2026.html",
    "osrs-grand-exchange-flipping-guide-2026.html",
    "osrs-grand-exchange-guide-2026.html",
    "osrs-herb-run-mastery-guide-2026.html",
    "osrs-herb-runs-profit-2026.html",
    "osrs-how-to-make-money-with-crafting-low-level.html",
    "osrs-how-to-make-money-with-zulrah.html",
    "osrs-hunter-money-making-guide-2026.html",
    "osrs-inflation-gear-prices-2026.html",
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-ironman-p2p-money-making-2026.html",
    "osrs-killing-green-dragons-money-per-hour.html",
    "osrs-low-effort-money-making-beginners.html",
    "osrs-low-level-skilling-money-makers-2026.html",
    "osrs-mid-game-money-making-roadmap-2026.html",
]

# ========== TRANSLATION DATA ==========

# Each file gets: cn_title, cn_summary, cn_toc_items, cn_h2, cn_h3, cn_quick

def t(text):
    """Mark English text that needs Chinese appended"""
    return text

# File 16: osrs-gear-inflation-guide-2026.html
DATA_16 = {
    "cn_title": "OSRS 2026装备通胀指南 — 价格趋势、买卖时机",
    "cn_summary": "2026年OSRS经济正经历显著通胀，金币购买力持续下降，而超稀有物品价格屡创新高。本文深入分析了Twisted Bow、Scythe of Vitur、Tumeken's Shadow等顶级装备的价格走势，揭示了通胀的五大成因，并提供了一套清晰的买入卖出策略，帮助您在高通胀环境中做出明智的装备投资决策。",
    "cn_hero_add": True,
    "toc_items": {
        "Why OSRS Has Inflation in 2026": "为什么2026年OSRS会出现通胀",
        "Mega-Rare Price Table (Current Prices)": "超级稀有物品价格表（当前价格）",
        "3rd Age & Ultra-Rare Items": "第三时代与超稀有物品",
        "Mid-Tier Gear & Consumables": "中档装备与消耗品",
        "Five Key Causes of Inflation": "通胀的五个关键原因",
        "When to Buy: Best Timing Strategy": "何时买入：最佳时机策略",
        "When to Sell: Profit-Taking Strategy": "何时卖出：获利了结策略",
        "Account Value & GP Purchasing Power": "账户价值与金币购买力",
        "Gear Inflation FAQs": "装备通胀常见问题",
    },
    "h2_map": {
        "1. Why OSRS Has Inflation in 2026": "1. 为什么2026年OSRS会出现通胀（Why OSRS Has Inflation in 2026）",
        "2. Mega-Rare Price Table (Current Prices)": "2. 超级稀有物品价格表（Mega-Rare Price Table）",
        "3. 3rd Age & Ultra-Rare Items": "3. 第三时代与超稀有物品（3rd Age & Ultra-Rare Items）",
        "4. Mid-Tier Gear & Consumables": "4. 中档装备与消耗品（Mid-Tier Gear & Consumables）",
        "5. Five Key Causes of Inflation": "5. 通胀的五个关键原因（Five Key Causes of Inflation）",
        "6. When to Buy: Best Timing Strategy": "6. 何时买入：最佳时机策略（When to Buy: Best Timing Strategy）",
        "7. When to Sell: Profit-Taking Strategy": "7. 何时卖出：获利了结策略（When to Sell: Profit-Taking Strategy）",
        "8. Account Value & GP Purchasing Power": "8. 账户价值与金币购买力（Account Value & GP Purchasing Power）",
        "9. Gear Inflation FAQs": "9. 装备通胀常见问题（Gear Inflation FAQs）",
        "① Table of Contents": "① 目录（Table of Contents）",
    },
    "h3_map": {
        "📈 What's Driving Mega-Rare Prices Up?": "📈 超级稀有物品价格为何上涨？（What's Driving Mega-Rare Prices Up?）",
        "🛡️ Elysian Spirit Shield": "🛡️  Elysean Spirit Shield（Elysian Spirit Shield）",
        "📊 GP to USD Rate": "📊 金币兑美元汇率（GP to USD Rate）",
        "🔒 Hard Currency: Skills & Achievements": "🔒 硬通货：技能与成就（Hard Currency: Skills & Achievements）",
    },
    "quick_preview": [
        ("🎯 What is it?", "分析2026年OSRS装备价格通胀情况——哪些装备现在该买，哪些该等。"),
        ("📋 Requirements", "无要求，只需有GP用于投资"),
        ("💰 Profit", "视情况而定——策略性买入/储蓄可节省数百万GP"),
        ("💡 Pro Tip", "远程装备（Armadyl、Pegasian）通胀最快——如果需要，尽早买入。"),
    ],
    "quick_summary": None,
}

# File 17: osrs-grand-exchange-flipping-guide-2026.html
DATA_17 = {
    "cn_title": "OSRS 2026大交易所倒卖指南 — 新手完整赚钱教程",
    "cn_summary": "零属性、零任务、零风险。从1万GP起步，一步步扩展到大交易所在被动收入。本指南全面涵盖从首次利润检查到高级多物品倒卖策略，帮助您在大交易所实现稳定盈利。",
    "cn_hero_add": True,
    "toc_items": {
        "How GE Flipping Works": "大交易所倒卖原理",
        "Getting Started: Setting Up Your Account": "入门：设置你的账户",
        "Margin Checking: The Core Skill": "利润检查：核心技能",
        "8 Best Beginner Flipping Items": "8个最佳新手倒卖物品",
        "Advanced Flipping Strategies": "高级倒卖策略",
        "GE Tax & Profit Calculation": "大交易所税费与利润计算",
        "Scaling Up: 10K to 50M+ Capital": "规模扩展：从1万到5000万+本金",
        "Common Flipping Mistakes": "常见倒卖错误",
        "Flipping FAQ": "倒卖常见问题",
    },
    "h2_map": {
        "① How GE Flipping Works": "① 大交易所倒卖原理（How GE Flipping Works）",
        "② Getting Started: Setting Up Your Account": "② 入门：设置你的账户（Getting Started）",
        "③ Margin Checking: The Core Skill": "③ 利润检查：核心技能（Margin Checking）",
        "④ 8 Best Beginner Flipping Items": "④ 8个最佳新手倒卖物品（Best Beginner Flipping Items）",
        "⑤ Advanced Flipping Strategies": "⑤ 高级倒卖策略（Advanced Flipping Strategies）",
        "⑥ GE Tax & Profit Calculation": "⑥ 大交易所税费与利润计算（GE Tax & Profit Calculation）",
        "⑦ Scaling Up: 10K to 50M+ Capital": "⑦ 规模扩展：从1万到5000万+本金（Scaling Up）",
        "⑧ Common Flipping Mistakes": "⑧ 常见倒卖错误（Common Flipping Mistakes）",
        "⑨ Flipping FAQ": "⑨ 倒卖常见问题（Flipping FAQ）",
        "⚡ Quick Summary": "⚡ 快速摘要",
    },
    "h3_map": {
        "💰 What is Flipping? A Simple Definition": "💰 什么是倒卖？简单定义（What is Flipping?）",
        "🛒 Why Flipping Works for Beginners": "🛒 为什么倒卖适合新手（Why Flipping Works for Beginners）",
    },
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>零需求（Zero requirements）</strong> — 一个3级账户只要有1万GP就能立即开始倒卖",
        "📌 <strong>每天1万-300万+GP（10K-3M+ GP/day）</strong> 被动收入，本金从1万到5000万+按比例增长",
        "📌 <strong>最佳入门物品（Best starter items）</strong>: 炮弹、自然符文、火符文——交易量大，成交快",
        "📌 <strong>4小时购买限制（4-hour buy limits）</strong> — 跨8个不同物品使用8个GE格子以最大化容量",
        "📌 <strong>1% GE税（1% GE tax）</strong> — 纯利润 = （售价 × 数量 × 0.99） − 成本价",
    ],
}

# File 18: osrs-grand-exchange-guide-2026.html
DATA_18 = {
    "cn_title": "OSRS 2026大交易所指南 — 超越买卖",
    "cn_summary": "大交易所（GE）是OSRS的中央市场——游戏中的每件物品都在这里买卖。本指南全面介绍GE的工作原理、购买限制、价格图表解读技巧，以及7个常见的交易错误，帮助您避免损失数百万GP。",
    "cn_hero_add": True,
    "toc_items": {
        "How the GE Actually Works": "大交易所实际工作原理",
        "Buying Smart — Instant vs Offer": "聪明购买——即时购买与挂单",
        "Selling for Maximum Profit": "最大化利润的卖出策略",
        "Buy Limits Explained": "购买限制详解",
        "Reading GE Graphs": "阅读大交易所价格图表",
        "Flipping Basics (Make Money!)": "倒卖基础知识（赚钱！）",
        "Common GE Mistakes Costing Millions": "常见大交易所错误让你损失数百万",
        "GE FAQ": "大交易所常见问题",
    },
    "h2_map": {
        "① How the GE Actually Works": "① 大交易所实际工作原理（How the GE Actually Works）",
        "② Buying Smart — Instant vs Offer": "② 聪明购买——即时购买与挂单（Buying Smart）",
        "③ Selling for Maximum Profit": "③ 最大化利润的卖出策略（Selling for Maximum Profit）",
        "④ Buy Limits Explained": "④ 购买限制详解（Buy Limits Explained）",
        "⑤ Reading GE Graphs": "⑤ 阅读大交易所价格图表（Reading GE Graphs）",
        "⑥ Flipping Basics (Make Money!)": "⑥ 倒卖基础知识（Flipping Basics）",
        "⑦ Common GE Mistakes Costing Millions": "⑦ 常见大交易所错误让你损失数百万（Common GE Mistakes）",
        "⑧ GE FAQ": "⑧ 大交易所常见问题（GE FAQ）",
        "⚡ Quick Jump": "⚡ 快速跳转",
        "OSRS Grand Exchange Guide 2026": "OSRS 2026大交易所指南",
    },
    "h3_map": {
        "🔍 Price Matching Explained": "🔍 价格匹配机制解析（Price Matching Explained）",
        "💡 Pro Tip: Volume Matters More Than Price": "💡 专业提示：交易量比价格更重要（Volume Matters More Than Price）",
    },
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>会员8+8个格子（8 buy + 8 sell slots）</strong> — F2P为3+3，中央自动匹配市场",
        "📌 <strong>1% GE税（1% GE tax）</strong> — 所有销售征收（上限1000万GP），始终计算净利润",
        "📌 <strong>每件物品4小时购买限制（4-hour buy limits）</strong> — 倒卖8种不同物品以最大化容量",
        "📌 <strong>倒卖基础（Flipping basics）</strong>: 以即时卖出价买入，以即时买入价卖出——差额即利润",
        "📌 <strong>阅读GE图表（Read GE graphs）</strong> — 发现趋势，避免倒卖30天走势向下的物品",
    ],
}

# File 19: osrs-herb-run-mastery-guide-2026.html
DATA_19 = {
    "cn_title": "OSRS 2026草药跑精通指南 — 最佳利润、地块与路线",
    "cn_summary": "草药跑是OSRS中最被忽视的赚钱方法之一。5分钟即可获得15万-80万GP利润。本指南将教您从32级 Farming 开始，掌握9地块最优路线，选择合适的草药种子，实现被动日入数百万。",
    "cn_hero_add": False,  # This file has a hero-image style, not standard hero
    "toc_items": {
        "Why Herb Runs Are the Best Passive GP in OSRS": "为什么草药跑是OSRS最佳被动收入",
        "Requirements & Unlocks You Need First": "先决条件与必要解锁",
        "Best Herbs to Plant by Level (Profit Calc)": "按等级的最佳种植草药（利润计算）",
        "All 9 Herb Patches — Unlock Priority": "全部9个草药地块——解锁优先级",
        "The Optimal 9-Patch Route (Step by Step)": "最优9地块路线（分步指南）",
        "Maximizing Profit — Compost, Secateurs & Diary Perks": "最大化利润——堆肥、剪刀与日记奖励",
        "FAQ": "常见问题",
        "Final Tips": "最终建议",
    },
    "h2_map": {
        "1. Why Herb Runs Are the Best Passive GP in OSRS": "1. 为什么草药跑是OSRS最佳被动收入（Why Herb Runs Are Best Passive GP）",
        "2. Requirements & Unlocks You Need First": "2. 先决条件与必要解锁（Requirements & Unlocks）",
        "3. Best Herbs to Plant by Level (Profit Calc)": "3. 按等级的最佳种植草药（Best Herbs by Level）",
        "4. All 9 Herb Patches — Unlock Priority": "4. 全部9个草药地块——解锁优先级（All 9 Herb Patches）",
        "5. The Optimal 9-Patch Route (Step by Step)": "5. 最优9地块路线（Optimal 9-Patch Route）",
        "6. Maximizing Profit — Compost, Secateurs & Diary Perks": "6. 最大化利润——堆肥、剪刀与日记奖励（Maximizing Profit）",
        "7. FAQ": "7. 常见问题（FAQ）",
        "8. Final Tips": "8. 最终建议（Final Tips）",
        "Table of Contents": "目录（Table of Contents）",
    },
    "h3_map": {},
    "quick_preview": [
        ("🎯 What is it?", "精通OSRS草药跑——优化路线、种子选择、利润计算和农场合同，以实现最大GP收益。"),
        ("📋 Requirements", "32+ Farming，拥有草药地块访问权限（需完成任务）"),
        ("💰 Profit", "每次5分钟的草药跑可获得40万-80万GP"),
        ("💡 Pro Tip", "Ranarr和Toadflax种子提供最佳利润成本比。"),
    ],
    "quick_summary": None,
}

# File 20: osrs-herb-runs-profit-2026.html
DATA_20 = {
    "cn_title": "OSRS 2026草药跑利润指南 | 每次跑的最佳草药与GP",
    "cn_summary": "2026年最佳OSRS草药跑利润指南——Snapdragon、Ranarr和Toadflax的每地块GP收益。包含9个地块位置、最优路线、成本与利润对比表以及等级要求。",
    "cn_hero_add": True,
    "toc_items": {
        "Why Herb Runs Matter More Than Ever": "为什么草药跑比以往更重要",
        "Best Herbs for Profit — Full Comparison": "最佳利润草药——全面对比",
        "All 9 Herb Patch Locations": "全部9个草药地块位置",
        "The Optimal 9-Patch Route": "最优9地块路线",
        "Cost vs. Profit — Detailed Breakdown": "成本与利润——详细分析",
        "Daily Profit Schedule": "每日利润时间表",
        "Tool & Item Requirements": "工具与物品需求",
        "FAQ — Herb Run Profit": "常见问题——草药跑利润",
    },
    "h2_map": {
        "1. Why Herb Runs Matter More Than Ever": "1. 为什么草药跑比以往更重要（Why Herb Runs Matter More Than Ever）",
        "2. Best Herbs for Profit — Full Comparison": "2. 最佳利润草药——全面对比（Best Herbs for Profit）",
        "3. All 9 Herb Patch Locations": "3. 全部9个草药地块位置（All 9 Herb Patch Locations）",
        "4. The Optimal 9-Patch Route": "4. 最优9地块路线（The Optimal 9-Patch Route）",
        "5. Cost vs. Profit — Detailed Breakdown": "5. 成本与利润——详细分析（Cost vs. Profit）",
        "6. Daily Profit Schedule": "6. 每日利润时间表（Daily Profit Schedule）",
        "7. Tool & Item Requirements": "7. 工具与物品需求（Tool & Item Requirements）",
        "8. FAQ — Herb Run Profit": "8. 常见问题——草药跑利润（Herb Run Profit FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>9个可用地块（9 patches available）</strong> — 会员全部可使用，F2P 2个",
        "📌 <strong>最佳利润草药（Best profit herbs）</strong>: Snapdragon（每次约8万GP）、Ranarr（约6.5万GP）、Toadflax（约4.5万GP）",
        "📌 <strong>每日5次跑（5 runs/day）</strong> = 5分钟/次，日利润可达40万-200万GP",
        "📌 <strong>必备物品（Must-have items）</strong>: 魔法剪刀（+10%产量）、无尽堆肥桶、超级堆肥",
        "📌 <strong>最低要求（Minimum req）</strong>: 32 Farming + Fairy Tale I（魔法剪刀）",
    ],
}

# File 21: osrs-how-to-make-money-with-crafting-low-level.html
DATA_21 = {
    "cn_title": "OSRS 2026低等级制作赚钱攻略 — 最佳利润方法",
    "cn_summary": "将低等级制作技能转化为真金白银。本文全面解析战斗法杖、龙皮护体、宝石切割和玻璃吹制等方法的利润空间，并配有三级装备配置方案，助您在制作之路上赚钱。",
    "cn_hero_add": True,
    "toc_items": {
        "Uncut Gem Cutting -- Best Entry-Level Profit (Level 1+)": "1. 未切割宝石切割——最佳入门级利润（1级+）",
        "Battlestaves -- Best Consistent Mid-Level Money Maker (Level 30+)": "2. 战斗法杖——最佳稳定中级赚钱方法（30级+）",
        "Dragonhide Bodies -- Best XP + Profit Combo (Level 63+)": "3. 龙皮护体——最佳经验+利润组合（63级+）",
        "Sapphire Rings & Gem Jewellery (Level 20+)": "4. 蓝宝石戒指与宝石首饰（20级+）",
        "Glassblowing -- Budget Method (Level 12+)": "5. 玻璃吹制——预算方法（12级+）",
        "3-Tier Gear Setup for Efficient Crafting": "6. 高效制作的三级装备配置",
        "Advanced Tips & Efficiency": "7. 高级技巧与效率优化",
        "Common Mistakes": "8. 常见错误",
        "Frequently Asked Questions": "9. 常见问题",
    },
    "h2_map": {
        "1. Uncut Gem Cutting -- Best Entry-Level Profit (Level 1+)": "1. 未切割宝石切割——最佳入门级利润（Uncut Gem Cutting）",
        "2. Battlestaves -- Best Consistent Mid-Level Money Maker (Level 30+)": "2. 战斗法杖——最佳稳定中级赚钱方法（Battlestaves）",
        "3. Dragonhide Bodies -- Best XP + Profit Combo (Level 63+)": "3. 龙皮护体——最佳经验+利润组合（Dragonhide Bodies）",
        "4. Sapphire Rings & Gem Jewellery (Level 20+)": "4. 蓝宝石戒指与宝石首饰（Sapphire Rings & Gem Jewellery）",
        "5. Glassblowing -- Budget Method (Level 12+)": "5. 玻璃吹制——预算方法（Glassblowing）",
        "6. 3-Tier Gear Setup for Efficient Crafting": "6. 高效制作的三级装备配置（3-Tier Gear Setup）",
        "7. Advanced Tips & Efficiency": "7. 高级技巧与效率优化（Advanced Tips & Efficiency）",
        "8. Common Mistakes": "8. 常见错误（Common Mistakes）",
        "9. Frequently Asked Questions": "9. 常见问题（Frequently Asked Questions）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>未切割宝石（Uncut gems）</strong> — 1级即可开始，蓝宝石/祖母绿每颗利润约400GP，每小时最多切3000颗",
        "📌 <strong>战斗法杖（Battlestaves）</strong> — 58级制作时，每根利润约100K，Varrock日记级别越高，每日库存越多",
        "📌 <strong>龙皮护体（Dragonhide bodies）</strong> — 71级制作，每小时210经验+约180万-100万GP利润",
        "📌 <strong>玻璃吹制（Glassblowing）</strong> — 12级即可开始，每颗光球利润100-400GP",
        "📌 <strong>蓝宝石戒指（Sapphire rings）</strong> — 20级制作，每枚戒指利润约500-800GP",
    ],
}

# File 22: osrs-how-to-make-money-with-zulrah.html
DATA_22 = {
    "cn_title": "OSRS 2026 Zulrah赚钱攻略 — GP/击杀、轮换与预算装备",
    "cn_summary": "掌握Zulrah每小时赚取200-500万GP的完整攻略。包含每次击杀的GP收益分析、预算装备配置（800-1200万GP）、轮换记忆技巧和拾取效率优化。",
    "cn_hero_add": True,
    "toc_items": {
        "Why Zulrah Is Still a Top Money Maker": "为什么Zulrah仍然是顶级赚钱方法",
        "GP Per Kill & Hour Breakdown": "每次击杀与每小时GP收益分析",
        "Requirements & Stat Recommendations": "要求与属性建议",
        "Budget Gear Setup (8-12M GP)": "预算装备配置（800-1200万GP）",
        "Zulrah Rotations Made Easy": "Zulrah轮换机制简化指南",
        "Inventory & Looting Strategy": "背包与拾取策略",
        "Profit Calculation — Real Numbers": "利润计算——真实数据",
        "Transitioning to Endgame Gear": "过渡到终局装备",
        "Common Mistakes": "常见错误",
        "FAQ — Zulrah Money Making": "常见问题——Zulrah赚钱",
    },
    "h2_map": {
        "① Why Zulrah Is Still a Top Money Maker": "① 为什么Zulrah仍然是顶级赚钱方法（Why Zulrah Is Still a Top Money Maker）",
        "② GP Per Kill & Hour Breakdown": "② 每次击杀与每小时GP收益分析（GP Per Kill & Hour Breakdown）",
        "③ Requirements & Stat Recommendations": "③ 要求与属性建议（Requirements & Stat Recommendations）",
        "④ Budget Gear Setup (8-12M GP)": "④ 预算装备配置（Budget Gear Setup）",
        "⑤ Zulrah Rotations Made Easy": "⑤ Zulrah轮换机制简化指南（Zulrah Rotations Made Easy）",
        "⑥ Inventory & Looting Strategy": "⑥ 背包与拾取策略（Inventory & Looting Strategy）",
        "⑦ Profit Calculation — Real Numbers": "⑦ 利润计算——真实数据（Profit Calculation）",
        "⑧ Transitioning to Endgame Gear": "⑧ 过渡到终局装备（Transitioning to Endgame Gear）",
        "⑨ Common Mistakes": "⑨ 常见错误（Common Mistakes）",
        "⑩ FAQ — Zulrah Money Making": "⑩ 常见问题——Zulrah赚钱（Zulrah Money Making FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>每小时200-500万GP（2-5M GP/hr）</strong> — 取决于击杀速率和经验水平",
        "📌 <strong>预算装备约800-1200万GP（Budget gear ~8-12M）</strong> — Trident of the Seas + Toxic Blowpipe",
        "📌 <strong>每次击杀约4万-10万GP（40K-100K GP/kill）</strong> — 包括独特掉落和鳞片",
        "📌 <strong>要求（Requirements）</strong>: 75+魔法、75+远程、43+祈祷、完成Regicide任务",
        "📌 <strong>建议（Pro tip）</strong>: 使用RuneLite Zulrah Helper插件——先学一种轮换模式",
    ],
}

# File 23: osrs-hunter-money-making-guide-2026.html
DATA_23 = {
    "cn_title": "OSRS 2026猎人赚钱攻略 — 黑鼬、红鼬与草药野猪",
    "cn_summary": "黑鼬（73+猎人）每小时180万-600万+GP，红鼬（63+猎人）每小时200万GP，草药野猪（80+猎人）每小时15万GP+草药经验。包含陷阱数量、PK生存技巧、装备配置和全面GP对比。",
    "cn_hero_add": True,
    "toc_items": {
        "Black Chinchompas (73+ Hunter)": "黑鼬（73+猎人）",
        "Red Chinchompas (63+ Hunter)": "红鼬（63+猎人）",
        "Herbiboar (80+ Hunter)": "草药野猪（80+猎人）",
        "Carnivorous Chinchompas (63+ Hunter)": "食肉鼬（63+猎人）",
        "Impling Hunting": "小精灵狩猎",
        "Hunter GP Comparison Table": "猎人GP对比表",
        "Trap Counts & Location Guide": "陷阱数量与位置指南",
        "Gear Setup for Hunter": "猎人装备配置",
        "PK Survival Guide for Wilderness Hunter": "野外猎人PK生存指南",
        "FAQ — Hunter Money Making": "常见问题——猎人赚钱",
    },
    "h2_map": {
        "① Black Chinchompas (73+ Hunter)": "① 黑鼬（Black Chinchompas）",
        "② Red Chinchompas (63+ Hunter)": "② 红鼬（Red Chinchompas）",
        "③ Herbiboar (80+ Hunter)": "③ 草药野猪（Herbiboar）",
        "④ Carnivorous Chinchompas (63+ Hunter)": "④ 食肉鼬（Carnivorous Chinchompas）",
        "⑤ Impling Hunting": "⑤ 小精灵狩猎（Impling Hunting）",
        "⑥ Hunter GP Comparison Table": "⑥ 猎人GP对比表（Hunter GP Comparison Table）",
        "⑦ Trap Counts & Location Guide": "⑦ 陷阱数量与位置指南（Trap Counts & Location Guide）",
        "⑧ Gear Setup for Hunter": "⑧ 猎人装备配置（Gear Setup for Hunter）",
        "⑨ PK Survival Guide for Wilderness Hunter": "⑨ 野外猎人PK生存指南（PK Survival Guide）",
        "⑩ FAQ — Hunter Money Making": "⑩ 常见问题——猎人赚钱（Hunter Money Making FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>最佳GP（Best GP）</strong>: 黑鼬每小时180万-600万+GP（73+猎人，野外，有PK风险）",
        "📌 <strong>安全选项（Safe option）</strong>: 红鼬每小时200万GP（63+猎人，Feldip Hills，无PK风险）",
        "📌 <strong>铁人模式最佳（Best for Ironmen）</strong>: 草药野猪每小时采收100-140株草药（80+猎人）",
        "📌 <strong>最大陷阱数（Max traps）</strong>: 80级野外可达6个陷阱（80+猎人在野外+1）",
        "📌 <strong>GP/XP平衡（GP/XP balance）</strong>: 食肉鼬每小时70万-250万GP（63+猎人），同时训练远程",
    ],
}

# File 24: osrs-inflation-gear-prices-2026.html
DATA_24 = {
    "cn_title": "OSRS 2026装备通胀 — 价格、趋势与明智投资",
    "cn_summary": "2026年夏季清扫活动从根本上重塑了OSRS的装备市场。部分物品价格上涨50%以上，而其他物品暴跌。债券价格徘徊在约1260万GP，通胀逐渐上升。本文详解每项重大价格变动，并提供可操作购买建议。",
    "cn_hero_add": True,
    "toc_items": {
        "OSRS Market Overview — June 2026": "OSRS市场概览——2026年6月",
        "Summer Sweep-Up Impact — Winners & Losers": "夏季清扫影响——赢家与输家",
        "Items That Rose (The Winners)": "价格上涨的物品（赢家）",
        "Items That Fell (The Losers)": "价格下跌的物品（输家）",
        "Bond Price Analysis — Current ~12.6M & Trajectory": "债券价格分析——当前约1260万GP及走势",
        "What's Driving Inflation in 2026?": "2026年通胀的驱动因素",
        "Smart Buying Guide — What to Buy & When": "明智购买指南——买什么、何时买",
        "FAQs — Gear Inflation & Investment": "常见问题——装备通胀与投资",
    },
    "h2_map": {
        "① 📈 OSRS Market Overview — June 2026": "① OSRS市场概览——2026年6月（OSRS Market Overview）",
        "② 🌞 Summer Sweep-Up Impact — Winners & Losers": "② 夏季清扫影响——赢家与输家（Summer Sweep-Up Impact）",
        "③ 📈 Items That Rose (The Winners)": "③ 价格上涨的物品（Items That Rose）",
        "④ 📉 Items That Fell (The Losers)": "④ 价格下跌的物品（Items That Fell）",
        "⑤ 💰 Bond Price Analysis — Current ~12.6M & Trajectory": "⑤ 债券价格分析——当前约1260万GP及走势（Bond Price Analysis）",
        "⑥ 🔍 What's Driving Inflation in 2026?": "⑥ 2026年通胀的驱动因素（What's Driving Inflation in 2026?）",
        "⑦ 📋 Smart Buying Guide — What to Buy & When": "⑦ 明智购买指南——买什么、何时买（Smart Buying Guide）",
        "❓ FAQs — Gear Inflation & Investment": "❓ 常见问题——装备通胀与投资（FAQs）",
    },
    "h3_map": {
        "1.1 📊 Key Market Indicators": "1.1 关键市场指标（Key Market Indicators）",
        "1.2 🎯 The Big Picture": "1.2 大局观（The Big Picture）",
        "2.1 📊 Market Reaction Timeline": "2.1 市场反应时间线（Market Reaction Timeline）",
        "2.2 Category Breakdown": "2.2 分类解析（Category Breakdown）",
        "3.1 🩸 Sanguinesti Staff — The Biggest Winner": "3.1 Sanguinesti法杖——最大赢家（The Biggest Winner）",
        "4.1 🔥 Burning Claws — Biggest Loser": "4.1 燃烧之爪——最大输家（Biggest Loser）",
    },
    "quick_preview": [
        ("🎯 What is it?", "2026年夏季清扫后OSRS装备价格变动分析——哪些装备价格上涨、哪些下跌及原因。"),
        ("📋 Requirements", "无要求，仅需关注市场动态"),
        ("💰 Profit", "视情况而定——正确时机买卖可节省数百万GP"),
        ("💡 Pro Tip", "Sanguinesti法杖涨价30-45%——尽早购买被增强的装备。"),
    ],
    "quick_summary": [
        "📌 <strong>Sanguinesti法杖+30-45%</strong>，Inquisitor套装+36-62%——夏季清扫创造了明确的赢家",
        "📌 <strong>债券价格预测（Bond price forecast）:</strong> 2026年第四季度达1350-1450万GP——如需会员，现在购买债券",
        "📌 <strong>明智购买指南（Smart buying guide）</strong>: 在价格进一步上涨前购买什么，在下跌前卖出什么",
        "📌 <strong>当前债券价格约1260万GP（~12.6M GP）</strong> 反映6个月内约7-8%的金币通胀率",
        "📌 <strong>避免长期持有GP（Avoid long-term GP holds）</strong> — 转换为物品或债券以保值",
    ],
}

# File 25: osrs-ironman-money-making-f2p-2026.html
DATA_25 = {
    "cn_title": "OSRS 2026铁人模式F2P赚钱攻略 — 最佳方法指南",
    "cn_summary": "2026年OSRS铁人模式F2P赚钱完整指南——从奶牛到符文矿石。8种按GP/小时排名的方法，涵盖牛皮、巨人之山、大恶魔和符文矿开采。",
    "cn_hero_add": True,
    "toc_items": {
        "Cowhides: The Classic Starter": "牛皮：经典起步方法",
        "Hill Giants & Big Bones": "山丘巨人与大骨头",
        "Greater Demons & Rune Mediums": "大恶魔与符文中型盔甲",
        "Ogress Warriors & Shamans": "食人魔战士与萨满",
        "Mining Iron Ore": "铁矿石开采",
        "Mining Silver & Gold": "银矿与金矿开采",
        "Rune Essence Mining": "符文精华开采",
        "Telegrabbing Wines of Zamorak": "远程抓取Zamorak之酒",
        "Method Comparison Table": "方法对比表",
        "F2P Ironman Money Making FAQ": "F2P铁人模式赚钱常见问题",
    },
    "h2_map": {
        "1. Cowhides: The Classic Starter": "1. 牛皮：经典起步方法（Cowhides: The Classic Starter）",
        "2. Hill Giants & Big Bones": "2. 山丘巨人与大骨头（Hill Giants & Big Bones）",
        "3. Greater Demons & Rune Mediums": "3. 大恶魔与符文中型盔甲（Greater Demons & Rune Mediums）",
        "4. Ogress Warriors & Shamans": "4. 食人魔战士与萨满（Ogress Warriors & Shamans）",
        "5. Mining Iron Ore": "5. 铁矿石开采（Mining Iron Ore）",
        "6. Mining Silver & Gold": "6. 银矿与金矿开采（Mining Silver & Gold）",
        "7. Rune Essence Mining": "7. 符文精华开采（Rune Essence Mining）",
        "8. Telegrabbing Wines of Zamorak": "8. 远程抓取Zamorak之酒（Telegrabbing Wines of Zamorak）",
        "9. Method Comparison Table": "9. 方法对比表（Method Comparison Table）",
        "10. F2P Ironman Money Making FAQ": "10. F2P铁人模式赚钱常见问题（FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>最佳起步（Best starter）</strong>: 杀牛卖牛皮——每小时4-7万GP，同时训练战斗属性",
        "📌 <strong>最佳中期（Best mid-game）</strong>: 山丘巨人掉落的巨骨（每根约2K GP）和大恶魔掉落的符文中型盔甲",
        "📌 <strong>最佳技能方法（Best skilling）</strong>: 铁矿石开采（每小时8万+GP）或在矿区开采银/金矿",
        "📌 <strong>有风险的高收益（High risk, high reward）</strong>: 远程抓取Zamorak之酒——有PK风险",
        "📌 <strong>铁人模式注意（Ironman note）</strong>: 不能使用GE——所有GP必须来自商店销售和掉落",
    ],
}

# File 26: osrs-ironman-p2p-money-making-2026.html
DATA_26 = {
    "cn_title": "OSRS 2026铁人模式P2P赚钱指南 — 9种方法（属性40-70）",
    "cn_summary": "为属性40-70的铁人模式玩家打造的9种赚钱方法排名，每小时10万-180万GP——敏捷金字塔、盗窃、战斗掉落高等级炼金、战斗法杖、每日GP例行任务。无需大交易所。",
    "cn_hero_add": True,
    "toc_items": {
        "Agility Pyramid — 100K GP/hr": "敏捷金字塔——每小时10万GP",
        "Thieving — Blackjacking & Pickpocketing": "盗窃——黑杰克与扒窃",
        "Slayer Alchs — Battlestaves & Rune Items": "战斗掉落炼金——战斗法杖与符文物品",
        "Battlestaves — Daily Shop Run": "战斗法杖——每日商店采购",
        "Giants' Foundry — Smithing for GP": "巨人铸造厂——锻造赚钱",
        "Birdhouse Runs — Passive Hunter/Farming": "鸟屋跑——被动猎人/农场经验",
        "Herb Runs — Passive Income": "草药跑——被动收入",
        "Daily GP Routine — Stacking Methods": "每日GP例行任务——叠加方法",
        "Nature Rune Strategy": "自然符文策略",
        "FAQ — Ironman P2P Money Making": "常见问题——铁人模式P2P赚钱",
    },
    "h2_map": {
        "1. Agility Pyramid — 100K GP/hr": "1. 敏捷金字塔（Agility Pyramid）",
        "2. Thieving — Blackjacking & Pickpocketing": "2. 盗窃——黑杰克与扒窃（Thieving）",
        "3. Slayer Alchs — Battlestaves & Rune Items": "3. 战斗掉落炼金——战斗法杖与符文物品（Slayer Alchs）",
        "4. Battlestaves — Daily Shop Run": "4. 战斗法杖——每日商店采购（Battlestaves）",
        "5. Giants' Foundry — Smithing for GP": "5. 巨人铸造厂——锻造赚钱（Giants' Foundry）",
        "6. Birdhouse Runs — Passive Hunter/Farming": "6. 鸟屋跑——被动猎人/农场经验（Birdhouse Runs）",
        "7. Herb Runs — Passive Income": "7. 草药跑——被动收入（Herb Runs）",
        "8. Daily GP Routine — Stacking Methods": "8. 每日GP例行任务——叠加方法（Daily GP Routine）",
        "9. Nature Rune Strategy": "9. 自然符文策略（Nature Rune Strategy）",
        "10. FAQ — Ironman P2P Money Making": "10. 常见问题——铁人模式P2P赚钱（FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>最佳前期（Best early）</strong>: 敏捷金字塔每小时10万GP（30+敏捷，无风险）",
        "📌 <strong>最佳中级（Best mid）</strong>: 盗窃每小时180万GP（70+盗窃，Ardougne Knight）",
        "📌 <strong>最佳被动收入（Best passive）</strong>: 战斗法杖每日商店采购（需要Varrock日记）",
        "📌 <strong>铁人模式特有（Ironman unique）</strong>: 自然符文策略——在商店购买自然符文用于炼金",
        "📌 <strong>每日叠加（Daily stack）</strong>: 组合所有方法每天可获得50万-100万+GP",
    ],
}

# File 27: osrs-killing-green-dragons-money-per-hour.html
DATA_27 = {
    "cn_title": "OSRS 2026杀绿龙每小时赚钱指南 — 每小时180万GP野外攻略",
    "cn_summary": "在野外击杀绿龙每小时赚取40万-80万GP。最佳位置、预算装备配置、拾取袋策略和PK生存技巧，附GP/小时收益分析。",
    "cn_hero_add": True,
    "toc_items": {
        "Green Dragons GP Per Hour Analysis": "绿龙每小时GP收益分析",
        "Best Locations for Green Dragons": "绿龙最佳击杀位置",
        "Budget Gear Setup (20K-100K)": "预算装备配置（2万-10万GP）",
        "Looting Bag Strategy": "拾取袋策略",
        "Anti-PK Survival Guide": "反PK生存指南",
        "GP Per Hour Comparison Table": "每小时GP对比表",
        "Transition to Blue & Red Dragons": "过渡到蓝龙与红龙",
        "FAQ — Green Dragon Money Making": "常见问题——绿龙赚钱",
    },
    "h2_map": {
        "① Green Dragons GP Per Hour Analysis": "① 绿龙每小时GP收益分析（Green Dragons GP Per Hour）",
        "② Best Locations for Green Dragons": "② 绿龙最佳击杀位置（Best Locations）",
        "③ Budget Gear Setup (20K-100K)": "③ 预算装备配置（Budget Gear Setup）",
        "④ Looting Bag Strategy": "④ 拾取袋策略（Looting Bag Strategy）",
        "⑤ Anti-PK Survival Guide": "⑤ 反PK生存指南（Anti-PK Survival Guide）",
        "⑥ GP Per Hour Comparison Table": "⑥ 每小时GP对比表（GP Per Hour Comparison）",
        "⑦ Transition to Blue & Red Dragons": "⑦ 过渡到蓝龙与红龙（Transition to Blue & Red Dragons）",
        "⑧ FAQ — Green Dragon Money Making": "⑧ 常见问题——绿龙赚钱（FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>每小时40万-80万GP（400K-800K GP/hr）</strong> — 取决于战斗属性和效率",
        "📌 <strong>最佳位置（Best location）</strong>: 东部绿龙区（野外17-19级）——20级以下，可随时传送",
        "📌 <strong>预算装备（Budget gear）</strong>: 2-10万GP即可——低成本装备，丢失不心疼",
        "📌 <strong>关键物品（Key item）</strong>: 拾取袋——每次行程容量翻倍，大幅提高有效GP/小时",
        "📌 <strong>安全提示（Safety tip）</strong>: 保持在20级以下野外以自由传送——看到小白点立即传送",
    ],
}

# File 28: osrs-low-effort-money-making-beginners.html
DATA_28 = {
    "cn_title": "OSRS 2026新手低付出赚钱攻略 — 10种方法，无需高属性",
    "cn_summary": "2026年10种最佳低付出OSRS赚钱方法——每小时5万-180万GP，零需求。包括亚麻纺线、鞣制皮革、GE倒卖、Snape草采集等经过验证的方法。",
    "cn_hero_add": True,
    "toc_items": {
        "Picking & Spinning Flax (Members)": "1. 采摘与纺织亚麻（会员）",
        "Tanning Hides at Al Kharid (Members)": "2. 在Al Kharid鞣制皮革（会员）",
        "Grand Exchange Flipping (No Stats Needed)": "3. 大交易所倒卖（无需属性）",
        "Collecting Snape Grass (Members)": "4. 采集Snape草（会员）",
        "Killing Cows -- Classic Early Game (F2P + Members)": "5. 杀牛——经典前期方法（F2P+会员）",
        "Wines of Zamorak via Telegrab (Members)": "6. 远程抓取Zamorak之酒（会员）",
        "Looting in the Wilderness (F2P + Members)": "7. 野外拾取（F2P+会员）",
        "Mort Myre Fungi (Members)": "8. Mort Myre真菌（会员）",
        "Cannonball Smithing (F2P Option)": "9. 炮弹锻造（F2P可选）",
        "Collecting Red Spider's Eggs (Members)": "10. 收集红蜘蛛卵（会员）",
        "Full Method Comparison Table": "11. 全部方法对比表",
        "Pro Tips for Beginner Money Makers": "12. 新手赚钱专业技巧",
        "Common Mistakes": "13. 常见错误",
        "Frequently Asked Questions": "14. 常见问题",
    },
    "h2_map": {
        "1. Picking & Spinning Flax (Members)": "1. 采摘与纺织亚麻（Picking & Spinning Flax）",
        "2. Tanning Hides at Al Kharid (Members)": "2. 在Al Kharid鞣制皮革（Tanning Hides）",
        "3. Grand Exchange Flipping (No Stats Needed)": "3. 大交易所倒卖（GE Flipping）",
        "4. Collecting Snape Grass (Members)": "4. 采集Snape草（Collecting Snape Grass）",
        "5. Killing Cows -- Classic Early Game (F2P + Members)": "5. 杀牛——经典前期方法（Killing Cows）",
        "6. Wines of Zamorak via Telegrab (Members)": "6. 远程抓取Zamorak之酒（Wines of Zamorak）",
        "7. Looting in the Wilderness (F2P + Members)": "7. 野外拾取（Looting in the Wilderness）",
        "8. Mort Myre Fungi (Members)": "8. Mort Myre真菌（Mort Myre Fungi）",
        "9. Cannonball Smithing (F2P Option)": "9. 炮弹锻造（Cannonball Smithing）",
        "10. Collecting Red Spider's Eggs (Members)": "10. 收集红蜘蛛卵（Red Spider's Eggs）",
        "11. Full Method Comparison Table": "11. 全部方法对比表（Full Method Comparison）",
        "12. Pro Tips for Beginner Money Makers": "12. 新手赚钱专业技巧（Pro Tips）",
        "13. Common Mistakes": "13. 常见错误（Common Mistakes）",
        "14. Frequently Asked Questions": "14. 常见问题（Frequently Asked Questions）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>最佳零需求（Best Zero-Req）</strong>: 亚麻纺线——只需10级制作，每小时10-12万GP",
        "📌 <strong>F2P可选（F2P Options）</strong>: 杀牛卖牛皮（每小时4-7万GP）和GE倒卖在免费世界可用",
        "📌 <strong>最省心（Most AFK）</strong>: 炮弹锻造（每2.5分钟处理一背包）和GE倒卖",
        "📌 <strong>风险提示（Risk Note）</strong>: Chaos Temple的Zamorak之酒有PK风险——使用Ice Dungeon替代",
        "📌 <strong>目标（Goal）</strong>: 休闲游戏10-20小时赚取第一个100万GP；积累本金，不要花在装备上",
    ],
}

# File 29: osrs-low-level-skilling-money-makers-2026.html
DATA_29 = {
    "cn_title": "OSRS 2026低等级技能赚钱攻略 — 被动GP指南",
    "cn_summary": "您不需要高战斗等级或昂贵装备也能在OSRS中赚钱。技能是被动、安全且从1级起就能盈利的。本指南涵盖从1-60级的每种F2P和会员技能赚钱方法，附确切GP/小时收益和需求。",
    "cn_hero_add": True,
    "toc_items": {
        "Mining — Iron Ore & Silver": "采矿——铁矿石和银矿",
        "Woodcutting — Yew & Magic Logs": "伐木——紫杉和魔法原木",
        "Fishing — Lobsters & Swordfish": "钓鱼——龙虾和剑鱼",
        "Cooking — Wine & Food": "烹饪——葡萄酒和食物",
        "Herblore — Unfinished Potions": "草药学——半成品药水",
        "Smithing — Cannonballs & Dart Tips": "锻造——炮弹和飞镖尖",
        "Crafting — Battlestaves": "制作——战斗法杖",
        "Full Comparison Table": "完整对比表",
        "Tips for Maximizing Profit": "利润最大化技巧",
    },
    "h2_map": {
        "1. Mining — Iron Ore & Silver": "1. 采矿——铁矿石和银矿（Mining）",
        "2. Woodcutting — Yew & Magic Logs": "2. 伐木——紫杉和魔法原木（Woodcutting）",
        "3. Fishing — Lobsters & Swordfish": "3. 钓鱼——龙虾和剑鱼（Fishing）",
        "4. Cooking — Wine & Food": "4. 烹饪——葡萄酒和食物（Cooking）",
        "5. Herblore — Unfinished Potions": "5. 草药学——半成品药水（Herblore）",
        "6. Smithing — Cannonballs & Dart Tips": "6. 锻造——炮弹和飞镖尖（Smithing）",
        "7. Crafting — Battlestaves": "7. 制作——战斗法杖（Crafting）",
        "8. Full Comparison Table": "8. 完整对比表（Full Comparison Table）",
        "9. Tips for Maximizing Profit": "9. 利润最大化技巧（Tips for Maximizing Profit）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>7种盈利技能（7 profitable skills）</strong> 从1级起——采矿、伐木、钓鱼、烹饪、草药学、锻造、制作",
        "📌 <strong>最佳低级方法（Best low-level method）</strong>: 锻造炮弹每小时11万+GP（35级锻造，可AFK）",
        "📌 <strong>F2P友好（F2P-friendly）</strong>: 开采铁矿石（每小时8万+GP）、砍伐橡木原木（每小时3万+GP）、钓龙虾（每小时4万+GP）",
        "📌 <strong>会员强力方法（P2P power methods）</strong>: 草药学半成品药水（每小时180万+GP）、鞣制皮革（每小时15万+GP）",
        "📌 <strong>无需战斗（No combat required）</strong> — 所有方法安全、被动，适合新账号",
    ],
}

# File 30: osrs-mid-game-money-making-roadmap-2026.html
DATA_30 = {
    "cn_title": "OSRS 2026中期游戏赚钱路线图 — 15种方法（180万-300万GP/小时）",
    "cn_summary": "为战斗等级60-100的OSRS玩家打造的完整中期赚钱路线图。涵盖15种详细方法，按GP/小时、需求和付出程度排名，帮助玩家从新手方法过渡到终局Boss战。",
    "cn_hero_add": True,
    "toc_items": {
        "Demonic Gorillas (3M GP/hr)": "恶魔大猩猩（每小时300万GP）",
        "Zulrah Entry (2.5M GP/hr)": "Zulrah入门（每小时250万GP）",
        "Vorkath Entry (2M GP/hr)": "Vorkath入门（每小时200万GP）",
        "Barrows (1.8M GP/hr)": "Barrows（每小时180万GP）",
        "Blast Furnace (2.5M GP/hr)": "高炉锻造（每小时250万GP）",
        "Slayer (1.8M-M GP/hr)": "战斗任务（每小时180万+GP）",
        "Herb Runs (660K/day Passive)": "草药跑（每日66万被动收入）",
        "Birdhouse Runs (Passive)": "鸟屋跑（被动收入）",
        "Giant's Foundry": "巨人铸造厂",
        "Flipping / Merchanting": "倒卖/交易",
        "Daily GP Routine": "每日GP例行任务",
        "Gear Priority Roadmap": "装备优先级路线图",
        "Endgame Transition Path": "终局过渡路径",
        "Common Mid-Game Mistakes": "中期常见错误",
        "FAQ — Mid-Game Money Making": "常见问题——中期赚钱",
    },
    "h2_map": {
        "1. Demonic Gorillas (3M GP/hr)": "1. 恶魔大猩猩（Demonic Gorillas）",
        "2. Zulrah Entry (2.5M GP/hr)": "2. Zulrah入门（Zulrah Entry）",
        "3. Vorkath Entry (2M GP/hr)": "3. Vorkath入门（Vorkath Entry）",
        "4. Barrows (1.8M GP/hr)": "4. Barrows（每小时180万GP）",
        "5. Blast Furnace (2.5M GP/hr)": "5. 高炉锻造（Blast Furnace）",
        "6. Slayer (1.8M-M GP/hr)": "6. 战斗任务（Slayer）",
        "7. Herb Runs (660K/day)": "7. 草药跑（Herb Runs）",
        "8. Birdhouse Runs (Passive)": "8. 鸟屋跑（Birdhouse Runs）",
        "9. Giant's Foundry": "9. 巨人铸造厂（Giant's Foundry）",
        "10. Flipping / Merchanting": "10. 倒卖/交易（Flipping）",
        "11. Daily GP Routine": "11. 每日GP例行任务（Daily GP Routine）",
        "12. Gear Priority Roadmap": "12. 装备优先级路线图（Gear Priority Roadmap）",
        "13. Endgame Transition Path": "13. 终局过渡路径（Endgame Transition Path）",
        "14. Common Mid-Game Mistakes": "14. 中期常见错误（Common Mid-Game Mistakes）",
        "15. FAQ — Mid-Game Money Making": "15. 常见问题——中期赚钱（FAQ）",
    },
    "h3_map": {},
    "quick_preview": None,
    "quick_summary": [
        "📌 <strong>15种方法排名（15 methods ranked）</strong> — 战斗60-100最佳区间，从新手到终局过渡",
        "📌 <strong>最佳中期战斗（Best mid-game combat）</strong>: 恶魔大猩猩每小时300万GP，Zulrah入门每小时250万GP，Vorkath入门每小时200万GP",
        "📌 <strong>最佳中期技能（Best skilling mid-game）</strong>: 高炉锻造每小时250万GP，草药跑每日66万被动收入",
        "📌 <strong>装备优先级路线图（Gear priority roadmap）</strong>: 从500万GP预算到5000万+终局装备的升级顺序",
        "📌 <strong>终局过渡（Endgame transition）</strong>: 从中期到Chambers of Xeric和终局Boss战的分步路径",
    ],
}

ALL_DATA = {
    "osrs-gear-inflation-guide-2026.html": DATA_16,
    "osrs-grand-exchange-flipping-guide-2026.html": DATA_17,
    "osrs-grand-exchange-guide-2026.html": DATA_18,
    "osrs-herb-run-mastery-guide-2026.html": DATA_19,
    "osrs-herb-runs-profit-2026.html": DATA_20,
    "osrs-how-to-make-money-with-crafting-low-level.html": DATA_21,
    "osrs-how-to-make-money-with-zulrah.html": DATA_22,
    "osrs-hunter-money-making-guide-2026.html": DATA_23,
    "osrs-inflation-gear-prices-2026.html": DATA_24,
    "osrs-ironman-money-making-f2p-2026.html": DATA_25,
    "osrs-ironman-p2p-money-making-2026.html": DATA_26,
    "osrs-killing-green-dragons-money-per-hour.html": DATA_27,
    "osrs-low-effort-money-making-beginners.html": DATA_28,
    "osrs-low-level-skilling-money-makers-2026.html": DATA_29,
    "osrs-mid-game-money-making-roadmap-2026.html": DATA_30,
}


def process_file(filename):
    """Process a single file: add Chinese translations"""
    filepath = os.path.join(BASE, "guides", filename)
    outpath = os.path.join(BASE, "zh", "guides", filename)
    data = ALL_DATA[filename]

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Change lang
    html = html.replace('lang="en"', 'lang="zh-Hans"')

    # 2. Change title to Chinese
    cn_title = data["cn_title"]
    html = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{cn_title}</title>',
        html
    )

    # 3. Update canonical to zh path
    html = re.sub(
        r'href="https://osrsguru\.com/guides/' + re.escape(filename) + r'"',
        f'href="https://osrsguru.com/zh/guides/{filename}"',
        html
    )
    # Also update og:url
    html = re.sub(
        r'<meta property="og:url" content="https://osrsguru\.com/guides/' + re.escape(filename) + r'">',
        f'<meta property="og:url" content="https://osrsguru.com/zh/guides/{filename}">',
        html
    )

    # 4. Update CSS paths (guides/ -> zh/guides/, so ../css/ -> ../../css/)
    # But only if the file is in zh/guides/
    html = re.sub(
        r'href="\.\./css/style\.css"',
        'href="../../css/style.css"',
        html
    )
    # Also fix paths like href="../js/features.js" -> href="../../js/features.js"
    html = re.sub(
        r'<script src="\.\./js/',
        '<script src="../../js/',
        html
    )

    # 5. Fix breadcrumb paths and nav links
    # Change href="../" to href="../../"
    # But be careful: some ../ are already correct for zh/guides/ depth
    # From zh/guides/, ../ goes to zh/, ../../ goes to root
    
    # Fix header nav links
    html = html.replace('href="../index.html"', 'href="../../index.html"')
    html = html.replace('href="../skill-training.html"', 'href="../../skill-training.html"')
    html = html.replace('href="../money-making.html"', 'href="../../money-making.html"')
    html = html.replace('href="../boss-guides.html"', 'href="../../boss-guides.html"')
    html = html.replace('href="../quest-guides.html"', 'href="../../quest-guides.html"')
    html = html.replace('href="../updates.html"', 'href="../../updates.html"')
    html = html.replace('href="../bosses.html"', 'href="../../bosses.html"')
    html = html.replace('href="../money.html"', 'href="../../money.html"')
    html = html.replace('href="../quests.html"', 'href="../../quests.html"')
    html = html.replace('href="../skills.html"', 'href="../../skills.html"')
    html = html.replace('href="../zh/"', 'href="../../zh/"')
    html = html.replace('href="../zh/index.html"', 'href="../../zh/index.html"')
    html = html.replace('href="../chinese.html"', 'href="../../chinese.html"')
    
    # Fix breadcrumb links
    html = re.sub(r'href="\.\./index\.html#([^"]*)"', r'href="../../index.html#\1"', html)
    
    # Fix other ../ directory references in links
    html = re.sub(r'href="\.\./guides/', 'href="../../guides/', html)

    # 6. Add cn-title and cn-summary in the hero section
    if data.get("cn_hero_add", True):
        # Find the h1 inside .guide-hero
        cn_title_text = data["cn_title"]
        # Insert cn-title class on h1 and add cn-summary paragraph
        
        # Pattern: <h1>...</h1> followed by <p class="subtitle">...</p>
        # We need to add cn-title (as separate h1) and cn-summary before the English h1
        
        # First, find the h1 in hero section
        hero_pattern = r'(<section class="guide-hero">.*?<div class="container">.*?)(<h1[^>]*>)(.*?)(</h1>)'
        def add_cn_title(m):
            prefix = m.group(1)
            h1_open = m.group(2)
            h1_text = m.group(3)
            h1_close = m.group(4)
            
            # Insert cn-title and cn-summary
            cn_block = f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title_text}</h1>\n            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{data["cn_summary"]}</p>\n            '
            
            return prefix + cn_block + h1_open + h1_text + h1_close
        
        html = re.sub(hero_pattern, add_cn_title, html, count=1, flags=re.DOTALL)

    # 7. Translate TOC items: add （中文翻译） after each TOC link text
    toc_map = data.get("toc_items", {})
    if toc_map:
        for en_text, cn_text in toc_map.items():
            escaped = re.escape(en_text)
            pattern = re.compile(r'(<a href="[^"]*">)' + escaped + r'(</a>)')
            html = pattern.sub(lambda m: m.group(1) + en_text + '（' + cn_text + '）' + m.group(2), html)

    # 8. Translate h2 headings
    h2_map = data.get("h2_map", {})
    if h2_map:
        for en_text, cn_text in h2_map.items():
            escaped = re.escape(en_text)
            pattern = re.compile(r'(<h2[^>]*>)' + escaped + r'(</h2>)')
            html = pattern.sub(lambda m: m.group(1) + cn_text + m.group(2), html)

    # 9. Translate h3 headings (but not in TOC, tip boxes, support card, etc.)
    h3_map = data.get("h3_map", {})
    if h3_map:
        for en_text, cn_text in h3_map.items():
            escaped = re.escape(en_text)
            pattern = re.compile(r'(<h3[^>]*>)' + escaped + r'(</h3>)')
            html = pattern.sub(lambda m: m.group(1) + cn_text + m.group(2), html)

    # 10. Handle Quick Summary / Quick Preview
    qs = data.get("quick_summary")
    qp = data.get("quick_preview")
    
    if qs:
        # Find the quick-summary section and replace its contents
        # Look for: <h3 ...>⏱️ Quick Summary — 30-Second Read</h3>
        # Replace with Chinese heading
        html = re.sub(
            r'<h3[^>]*>⏱️ Quick Summary[^<]*</h3>',
            '<h3 style="color:#2D2A33;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30秒快速预览</h3>',
            html
        )
        # Also handle "⏱️ Quick Summary &mdash; 30-Second Read"
        html = re.sub(
            r'<h3[^>]*>⏱️ Quick Summary[^<]*</h3>',
            '<h3 style="color:#2D2A33;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30秒快速预览</h3>',
            html
        )
        
        # Replace bullet list items in quick-summary divs
        # Find the <ul> inside a quick-summary div and replace its content
        def replace_qs_list(m):
            div_start = m.group(1)
            return div_start + '\n' + '\n'.join(f'                    <li>{item}</li>' for item in qs) + '\n                '
        
        html = re.sub(
            r'(<div class="quick-summary"[^>]*>.*?<ul[^>]*>).*?(</ul>)',
            lambda m: m.group(1) + '\n' + '\n'.join(f'                    <li>{item}</li>' for item in qs) + '\n                ' + m.group(2),
            html,
            flags=re.DOTALL
        )
        
        # If no quick-summary exists yet, add one after the hero section
        if not re.search(r'class="quick-summary"', html):
            # Add after hero section, before TOC
            qs_html = '\n            <div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">\n'
            qs_html += '                <h3 style="color:#2D2A33;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ 30秒快速预览</h3>\n'
            qs_html += '                <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">\n'
            for item in qs:
                qs_html += f'                    <li>{item}</li>\n'
            qs_html += '                </ul>\n            </div>\n'
            
            # Insert after hero section (before <main>)
            html = re.sub(
                r'(</section>\s*<main)',
                qs_html + r'\1',
                html
            )
    
    if qp:
        # Find the quick-preview section and replace card contents
        # The quick-preview has a grid with 4 cards: What is it?, Requirements, Profit, Pro Tip
        
        # Replace the heading
        html = re.sub(
            r'<span[^>]*>&#x26A1; 30-SECOND QUICK PREVIEW</span>',
            '<span style="background:#9B84D4;color:#fff;font-size:.75rem;font-weight:700;padding:4px 12px;border-radius:20px;">⚡ 30秒快速预览</span>',
            html
        )
        
        # Replace card contents
        for i, (en_label, cn_desc) in enumerate(qp):
            # Match card with this label
            # Pattern: <strong ...>EN_LABEL</strong>\n      <p ...>EN_DESC</p>
            pattern = r'(<strong[^>]*>' + re.escape(en_label) + r'</strong>)\s*<p[^>]*>[^<]*</p>'
            replacement = r'\1' + f'\n      <p style="color:#2D2A33;margin:4px 0 0;font-size:.85rem;line-height:1.4;">{cn_desc}</p>'
            html = re.sub(pattern, replacement, html)
        
        # If no quick-preview exists, add one
        if not re.search(r'class="quick-preview"', html):
            qp_html = '\n            <div class="quick-preview" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:12px;padding:20px 24px;margin:24px auto;max-width:780px;">\n'
            qp_html += '  <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">\n'
            qp_html += '    <span style="background:#9B84D4;color:#fff;font-size:.75rem;font-weight:700;padding:4px 12px;border-radius:20px;">⚡ 30秒快速预览</span>\n'
            qp_html += '  </div>\n'
            qp_html += '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;">\n'
            
            labels = ["🎯 这是什么？", "📋 要求", "💰 利润", "💡 专业提示"]
            for i, (en_label, cn_desc) in enumerate(qp):
                label = labels[i] if i < len(labels) else en_label
                qp_html += f'    <div style="background:#fff;border:1px solid #D4CDE0;border-radius:8px;padding:10px 14px;">\n'
                qp_html += f'      <strong style="color:#9B84D4;font-size:.82rem;">{label}</strong>\n'
                qp_html += f'      <p style="color:#2D2A33;margin:4px 0 0;font-size:.85rem;line-height:1.4;">{cn_desc}</p>\n'
                qp_html += '    </div>\n'
            
            qp_html += '  </div>\n</div>\n'
            
            # Insert after hero section
            html = re.sub(
                r'(</section>\s*<main)',
                qp_html + r'\1',
                html
            )

    # 11. Update JSON-LD headline to Chinese
    html = re.sub(
        r'"headline": "([^"]+)"',
        f'"headline": "{cn_title}"',
        html
    )

    # 12. Fix json-ld mainEntityOfPage URLs
    html = re.sub(
        r'"mainEntityOfPage": "https://osrsguru\.com/guides/' + re.escape(filename) + r'"',
        f'"mainEntityOfPage": "https://osrsguru.com/zh/guides/{filename}"',
        html
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    # Write output
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ {filename}")


def main():
    for filename in FILES:
        try:
            process_file(filename)
        except Exception as e:
            import traceback
            print(f"❌ {filename}: {e}")
            traceback.print_exc()
    
    print(f"\n🎉 Processed {len(FILES)} files.")


if __name__ == "__main__":
    main()
