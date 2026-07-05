#!/usr/bin/env python3
"""
Process 7 Chinese beginner guides for Group 3.
Each file: copy EN content, modify lang/title/canonical, add cn-title/cn-summary,
translate TOC items, headings, and quick-preview-box.
"""

import re
import os

EN_DIR = "C:/Users/Lenovo/osrs-guide-site/guides"
ZH_DIR = "C:/Users/Lenovo/osrs-guide-site/zh/guides"

files = [
    # (filename, cn_title_suffix, cn_title_short, cn_summary, toc_translations, h2_translations, h3_translations, has_quick_box)
    (
        "osrs-fastest-99-cooking-f2p.html",
        "OSRS F2P最快烹饪99级攻略",
        "OSRS F2P最快烹饪99级 — 葡萄酒、卡兰布万鱼与经济方法",
        "最全面的OSRS烹饪升级指南。覆盖F2P和会员所有方法，从1级到99级，包括最快的葡萄酒/卡兰布万鱼方法、F2P专属路线以及节省GP的实用技巧。",
        {
            "1. XP Rates Comparison (All Methods)": "1. XP Rates Comparison (All Methods)（XP速率对比：所有方法）",
            "2. Fastest Members Route: 1-99 in 30-35 Hours": "2. Fastest Members Route: 1-99 in 30-35 Hours（最快会员路线：1-99需30-35小时）",
            "3. F2P-Only Route to 99 Cooking": "3. F2P-Only Route to 99 Cooking（纯F2P路线到99烹饪）",
            "4. Profitable Cooking Methods": "4. Profitable Cooking Methods（可盈利的烹饪方法）",
            "5. Best Cooking Locations & Equipment": "5. Best Cooking Locations & Equipment（最佳烹饪地点与装备）",
            "6. Common Mistakes & Pro Tips": "6. Common Mistakes & Pro Tips（常见错误与专业技巧）",
            "7. Frequently Asked Questions": "7. Frequently Asked Questions（常见问题解答）",
        },
        {
            "1. XP Rates Comparison (All Methods)": "1. XP Rates Comparison (All Methods)（XP速率对比：所有方法）",
            "2. Fastest Members Route: 1-99 in 30-35 Hours": "2. Fastest Members Route: 1-99 in 30-35 Hours（最快会员路线：1-99需30-35小时）",
            "3. F2P-Only Route to 99 Cooking": "3. F2P-Only Route to 99 Cooking（纯F2P路线到99烹饪）",
            "4. Profitable Cooking Methods": "4. Profitable Cooking Methods（可盈利的烹饪方法）",
            "5. Best Cooking Locations & Equipment": "5. Best Cooking Locations & Equipment（最佳烹饪地点与装备）",
            "6. Common Mistakes & Pro Tips": "6. Common Mistakes & Pro Tips（常见错误与专业技巧）",
            "7. Frequently Asked Questions": "7. Frequently Asked Questions（常见问题解答）",
        },
        {
            "Karambwan 1-Tick Cooking Technique:": "Karambwan 1-Tick Cooking Technique:（卡兰布万1-tick烹饪技巧）",
            "Wines of Zamorak — Fastest F2P Method:": "Wines of Zamorak — Fastest F2P Method:（萨莫拉克之酒——最快F2P方法）",
        },
        True
    ),
    (
        "osrs-first-boss-progression-roadmap-2026.html",
        "OSRS新手Boss进度路线图2026",
        "OSRS新手Boss进度路线图 — 从L3到L70的必经之路",
        "完整的OSRS Boss进度路线图。从战斗等级3到70，详细介绍10个新手必打的Boss，包括Giant Mole, Obor, Barrows, Zulrah, Vorkath。装备方案、利润评估和安全打法一应俱全。",
        {
            "Why Bossing Matters Even at Low Levels": "Why Bossing Matters Even at Low Levels（为什么低等级也要打Boss）",
            "Your First 10 Bosses — Complete Progression Map": "Your First 10 Bosses — Complete Progression Map（你的第一批10个Boss——完整进度图）",
            "Boss 1: Giant Mole (F2P Accessible)": "Boss 1: Giant Mole (F2P Accessible)（Boss 1: 巨鼹鼠 - F2P可打）",
            "Boss 2: Obor (F2P)": "Boss 2: Obor (F2P)（Boss 2: 奥博尔 - F2P）",
            "Boss 3: Bryophyta (F2P)": "Boss 3: Bryophyta (F2P)（Boss 3: 布赖欧菲塔 - F2P）",
            "Boss 4: Barrows (Members)": "Boss 4: Barrows (Members)（Boss 4: 巴罗斯 - 会员）",
            "Boss 5: Sarachnis (Members)": "Boss 5: Sarachnis (Members)（Boss 5: 萨拉奇尼斯 - 会员）",
            "Boss 6: Giant Roc (Members)": "Boss 6: Giant Roc (Members)（Boss 6: 巨鹏 - 会员）",
            "Boss 7: King Black Dragon (Members)": "Boss 7: King Black Dragon (Members)（Boss 7: 黑龙王 - 会员）",
            "Boss 8: Zulrah (Members)": "Boss 8: Zulrah (Members)（Boss 8: 祖拉 - 会员）",
            "Boss 9: Vorkath (Members)": "Boss 9: Vorkath (Members)（Boss 9: 沃卡什 - 会员）",
            "Boss 10: Chambers of Xeric (Members)": "Boss 10: Chambers of Xeric (Members)（Boss 10: 泽里克密室 - 会员）",
            "Gear Progression Path": "Gear Progression Path（装备进阶路线）",
            "Essential Supplies & Consumables": "Essential Supplies & Consumables（必备物资与消耗品）",
            "Common Beginner Mistakes & How to Avoid": "Common Beginner Mistakes & How to Avoid（新手常见错误及避免方法）",
            "After Level 70: What's Next?": "After Level 70: What's Next?（70级之后：下一步做什么？）",
            "Quick Reference Table & FAQ": "Quick Reference Table & FAQ（快速参考与常见问题）",
        },
        {
            "1. Why Bossing Matters Even at Low Levels": "1. Why Bossing Matters Even at Low Levels（1. 为什么低等级也要打Boss）",
            "2. Your First 10 Bosses — Complete Progression Map": "2. Your First 10 Bosses — Complete Progression Map（2. 你的第一批10个Boss——完整进度图）",
            "3. Boss 1: Giant Mole (F2P Accessible, Combat 30+)": "3. Boss 1: Giant Mole (F2P Accessible, Combat 30+)（3. Boss 1: 巨鼹鼠 - F2P可打，战斗30+）",
            "4. Boss 2: Obor (F2P, Combat 35+)": "4. Boss 2: Obor (F2P, Combat 35+)（4. Boss 2: 奥博尔 - F2P，战斗35+）",
            "5. Boss 3: Bryophyta (F2P, Combat 40+)": "5. Boss 3: Bryophyta (F2P, Combat 40+)（5. Boss 3: 布赖欧菲塔 - F2P，战斗40+）",
            "10. Gear Progression Path (L3→70)": "10. Gear Progression Path (L3→70)（10. 装备进阶路线 L3→70）",
            "11. Essential Supplies & Consumables": "11. Essential Supplies & Consumables（11. 必备物资与消耗品）",
            "12. Common Beginner Mistakes & How to Avoid": "12. Common Beginner Mistakes & How to Avoid（12. 新手常见错误及避免方法）",
            "13. After Level 70: What's Next?": "13. After Level 70: What's Next?（13. 70级之后：下一步做什么？）",
            "14. Quick Reference Table & FAQ": "14. Quick Reference Table & FAQ（14. 快速参考与常见问题）",
        },
        {
            "🎯 What This Roadmap Will Give You": "🎯 What This Roadmap Will Give You（🎯 这个路线图能给你什么）",
            "📍 Location & Requirements": "📍 Location & Requirements（📍 位置与要求）",
            "⚔️ Budget Gear Setup (<100K GP Total)": "⚔️ Budget Gear Setup (<100K GP Total)（⚔️ 预算装备方案 <10万GP）",
            "⚔️ Optimal Gear Setup (<1M GP, Members Only)": "⚔️ Optimal Gear Setup (<1M GP, Members Only)（⚔️ 最佳装备方案 <100万GP，仅会员）",
            "🧠 Fight Strategy — Step by Step": "🧠 Fight Strategy — Step by Step（🧠 战斗策略——逐步分解）",
            "💎 Loot & Profit per Kill": "💎 Loot & Profit per Kill（💎 掉落与每次击杀收益）",
            "🎯 Goals for This Boss": "🎯 Goals for This Boss（🎯 这个Boss的目标）",
            "📍 Location & How to Access": "📍 Location & How to Access（📍 位置与进入方法）",
            "⚔️ Gear Setup (Same as Giant Mole, + Better Weapon)": "⚔️ Gear Setup (Same as Giant Mole, + Better Weapon)（⚔️ 装备方案 - 同巨鼹鼠 + 更好武器）",
            "🧠 Fight Strategy": "🧠 Fight Strategy（🧠 战斗策略）",
            "💎 Loot & Profit": "💎 Loot & Profit（💎 掉落与收益）",
            "📍 Location & Access": "📍 Location & Access（📍 位置与进入）",
            "🧠 Fight Strategy": "🧠 Fight Strategy（🧠 战斗策略）",
            "💎 Loot": "💎 Loot（💎 掉落）",
            "🍖 Food Tier 1 (Bosses 1–3, F2P)": "🍖 Food Tier 1 (Bosses 1–3, F2P)（🍖 食物1级 - Boss 1-3，F2P）",
            "🧪 Potions Tier 1 (Members Only, Bosses 4+)": "🧪 Potions Tier 1 (Members Only, Bosses 4+)（🧪 药水1级 - 仅会员，Boss 4+）",
            "🎯 Recommended Next Steps": "🎯 Recommended Next Steps（🎯 推荐下一步）",
        },
        True
    ),
    (
        "osrs-flipping-guide-beginners-2026.html",
        "OSRS交易所倒卖新手指南2026",
        "OSRS交易所倒卖新手指南 — 10万变100万GP的秘诀",
        "完整的OSRS Grand Exchange倒卖新手指南。从10万GP起步，教你发现高利润物品、掌握7%日回报率、正确使用买入限额，逐步建立倒卖资金池到百万级别。",
        {
            "🎯 Why Flipping Pays": "🎯 Why Flipping Pays（🎯 为什么倒卖赚钱）",
            "📊 How It Works": "📊 How It Works（📊 如何运作）",
            "🔍 Find Items": "🔍 Find Items（🔍 寻找物品）",
            "📋 Step-by-Step": "📋 Step-by-Step（📋 分步攻略）",
            "💰 Under 1M GP": "💰 Under 1M GP（💰 低于100万GP）",
            "💰 1M-10M GP": "💰 1M-10M GP（💰 100万-1000万GP）",
            "⚠️ Avoid Mistakes": "⚠️ Avoid Mistakes（⚠️ 避免错误）",
            "❓ FAQ": "❓ FAQ（❓ 常见问题）",
        },
        {
            "🎯 Why Flipping Pays: 7% Daily ROI (Zero Requirements)": "🎯 Why Flipping Pays: 7% Daily ROI (Zero Requirements)（🎯 为什么倒卖赚钱：7%日回报率，零要求）",
            "📊 How GE Flipping Works: Spread + 4h Buy Limit": "📊 How GE Flipping Works: Spread + 4h Buy Limit（📊 交易所倒卖如何运作：差价 + 4小时买入限额）",
            "🔍 How to Find Items to Flip (3 Methods)": "🔍 How to Find Items to Flip (3 Methods)（🔍 如何寻找倒卖物品 - 3种方法）",
            "📋 Step-by-Step Strategy: 100K → 1M GP": "📋 Step-by-Step Strategy: 100K → 1M GP（📋 分步策略：10万→100万GP）",
            "💰 10 Best Items to Flip: 1M-10M GP": "💰 10 Best Items to Flip: 1M-10M GP（💰 倒卖最佳10件物品：100万-1000万GP）",
            "⚠️ 6 Common Mistakes That Cost GP": "⚠️ 6 Common Mistakes That Cost GP（⚠️ 6个浪费GP的常见错误）",
            "❓ FAQ + Advanced Tips": "❓ FAQ + Advanced Tips（❓ 常见问题 + 进阶技巧）",
        },
        {
            "📐 The Buy-Sell Spread (Your Profit)": "📐 The Buy-Sell Spread (Your Profit)（📐 买卖差价 - 你的利润）",
            "⏱️ The 4-Hour Buy Limit — Capacity Cap": "⏱️ The 4-Hour Buy Limit — Capacity Cap（⏱️ 4小时买入限额——容量上限）",
            "📊 GE Tax — The 1% You Must Account For": "📊 GE Tax — The 1% You Must Account For（📊 交易所税——必须计算的1%）",
            "1️⃣ Method: Manual Margin Check (Most Accurate)": "1️⃣ Method: Manual Margin Check (Most Accurate)（1️⃣ 方法：手动检查差价 - 最准确）",
            "2️⃣ Method: Use Price Tracking Tools": "2️⃣ Method: Use Price Tracking Tools（2️⃣ 方法：使用价格追踪工具）",
            "3️⃣ Method: Follow Content Cycles": "3️⃣ Method: Follow Content Cycles（3️⃣ 方法：跟随内容周期）",
            "📋 The 5-Step Flip Cycle": "📋 The 5-Step Flip Cycle（📋 5步倒卖循环）",
            "🎯 Your First Flip — Walkthrough": "🎯 Your First Flip — Walkthrough（🎯 你的第一次倒卖——手把手教程）",
            "📈 Scaling Strategy for 1M-10M Flippers": "📈 Scaling Strategy for 1M-10M Flippers（📈 100万-1000万资金策略）",
            "1️⃣ Mistake: Overinvesting in One Item": "1️⃣ Mistake: Overinvesting in One Item（1️⃣ 错误：过度投资单一物品）",
            "2️⃣ Mistake: Flipping Low-Volume Items": "2️⃣ Mistake: Flipping Low-Volume Items（2️⃣ 错误：倒卖低交易量物品）",
            "3️⃣ Mistake: Ignoring GE Tax": "3️⃣ Mistake: Ignoring GE Tax（3️⃣ 错误：忽视交易所税）",
            "4️⃣ Mistake: Canceling Offers Too Quickly": "4️⃣ Mistake: Canceling Offers Too Quickly（4️⃣ 错误：过早取消订单）",
            "5️⃣ Mistake: Panic Selling During Dip": "5️⃣ Mistake: Panic Selling During Dip（5️⃣ 错误：恐慌性抛售）",
            "6️⃣ Mistake: Flipping After Game Updates": "6️⃣ Mistake: Flipping After Game Updates（6️⃣ 错误：游戏更新后倒卖）",
        },
        True
    ),
    (
        "osrs-how-to-beat-zulrah-beginners-rotation.html",
        "OSRS祖拉新手攻略 — 完整轮换指南2026",
        "OSRS祖拉新手攻略 — 完整轮换与打法指南",
        "最新的OSRS Zulrah新手攻略。详细解析4种轮换模式、预算装备搭配、Jad阶段生存技巧，以及如何从Zulrah获得每小时100-400万GP的稳定收入。",
        {
            "Requirements & Recommended Stats": "Requirements & Recommended Stats（要求与推荐属性）",
            "Budget Gear Setup (~8-10M Total)": "Budget Gear Setup (~8-10M Total)（预算装备方案 - 总价约800-1000万GP）",
            "The 4 Zulrah Rotations — How to Identify Each": "The 4 Zulrah Rotations — How to Identify Each（4种Zulrah轮换——如何识别每种）",
            "Phase-by-Phase Survival Guide": "Phase-by-Phase Survival Guide（分阶段生存指南）",
            "Inventory Setup for Learning Zulrah": "Inventory Setup for Learning Zulrah（学习Zulrah的背包配置）",
            "Zulrah Loot & Profit Analysis (2026)": "Zulrah Loot & Profit Analysis (2026)（Zulrah掉落与收益分析 2026）",
            "Common Mistakes Beginners Make": "Common Mistakes Beginners Make（新手常犯错误）",
            "Frequently Asked Questions": "Frequently Asked Questions（常见问题解答）",
        },
        {
            "1. Requirements & Recommended Stats": "1. Requirements & Recommended Stats（1. 要求与推荐属性）",
            "2. Budget Gear Setup (~8-10M Total)": "2. Budget Gear Setup (~8-10M Total)（2. 预算装备方案 - 总价约800-1000万GP）",
            "3. The 4 Zulrah Rotations — How to Identify Each": "3. The 4 Zulrah Rotations — How to Identify Each（3. 4种Zulrah轮换——如何识别每种）",
            "4. Phase-by-Phase Survival Guide": "4. Phase-by-Phase Survival Guide（4. 分阶段生存指南）",
            "5. Inventory Setup for Learning Zulrah": "5. Inventory Setup for Learning Zulrah（5. 学习Zulrah的背包配置）",
            "6. Zulrah Loot & Profit Analysis (2026)": "6. Zulrah Loot & Profit Analysis (2026)（6. Zulrah掉落与收益分析 2026）",
            "7. Common Mistakes Beginners Make": "7. Common Mistakes Beginners Make（7. 新手常犯错误）",
            "8. Frequently Asked Questions": "8. Frequently Asked Questions（8. 常见问题解答）",
        },
        {
            "Green Phase (Mage Attacks — Use Ranged)": "Green Phase (Mage Attacks — Use Ranged)（绿色阶段 - 魔法攻击，使用远程）",
            "Blue/Tanzanite Phase (Range Attacks — Use Magic)": "Blue/Tanzanite Phase (Range Attacks — Use Magic)（蓝色/坦桑石阶段 - 远程攻击，使用魔法）",
            "Red/Melee Phase — DO NOT ATTACK": "Red/Melee Phase — DO NOT ATTACK（红色/近战阶段——不要攻击）",
            "Jad Phase (Rotation 3 Only) — Prayer Switching Required": "Jad Phase (Rotation 3 Only) — Prayer Switching Required（Jad阶段 - 仅轮换3，需要切换祈祷）",
        },
        False  # Special warning box instead of quick-summary
    ),
    (
        "osrs-how-to-solo-god-wars-boss-for-beginners.html",
        "OSRS新手单人战神地牢Boss攻略",
        "OSRS新手单人战神地牢Boss攻略 — Bandos和Armadyl指南",
        "完整的新手单人攻略GWD（God Wars Dungeon）Boss指南。从Bandos开始，详细介绍装备配置、击杀数获取、背包规划以及800K-200万GP/小时的收益分析。",
        {
            "God Wars Dungeon — The Basics": "God Wars Dungeon — The Basics（战神地牢——基础知识）",
            "Getting Kill Count Efficiently": "Getting Kill Count Efficiently（高效获取击杀数）",
            "Soloing General Graardor (Bandos) — Budget to Best Gear": "Soloing General Graardor (Bandos) — Budget to Best Gear（单人Graardor将军/Bandos——从预算到顶级装备）",
            "Bandos Solo Strategy — Step by Step": "Bandos Solo Strategy — Step by Step（Bandos单人策略——逐步分解）",
            "Soloing Kree'arra (Armadyl) — Budget to Best Gear": "Soloing Kree'arra (Armadyl) — Budget to Best Gear（单人Kree'arra/Armadyl——从预算到顶级装备）",
            "Bandos vs Armadyl — Profit Comparison": "Bandos vs Armadyl — Profit Comparison（Bandos vs Armadyl——收益对比）",
            "Trip Inventory Setup": "Trip Inventory Setup（出装背包配置）",
            "Common Mistakes at GWD": "Common Mistakes at GWD（GWD常见错误）",
            "Frequently Asked Questions": "Frequently Asked Questions（常见问题解答）",
        },
        {
            "1. God Wars Dungeon — The Basics": "1. God Wars Dungeon — The Basics（1. 战神地牢——基础知识）",
            "2. Getting Kill Count Efficiently": "2. Getting Kill Count Efficiently（2. 高效获取击杀数）",
            "3. Soloing General Graardor (Bandos) — Budget to Best Gear": "3. Soloing General Graardor (Bandos) — Budget to Best Gear（3. 单人Graardor将军/Bandos——从预算到顶级装备）",
            "4. Bandos Solo Strategy — Step by Step": "4. Bandos Solo Strategy — Step by Step（4. Bandos单人策略——逐步分解）",
            "5. Soloing Kree'arra (Armadyl) — Budget to Best Gear": "5. Soloing Kree'arra (Armadyl) — Budget to Best Gear（5. 单人Kree'arra/Armadyl——从预算到顶级装备）",
            "6. Bandos vs Armadyl — Profit Comparison": "6. Bandos vs Armadyl — Profit Comparison（6. Bandos vs Armadyl——收益对比）",
            "7. Trip Inventory Setup": "7. Trip Inventory Setup（7. 出装背包配置）",
            "8. Common Mistakes at GWD": "8. Common Mistakes at GWD（8. GWD常见错误）",
            "9. Frequently Asked Questions": "9. Frequently Asked Questions（9. 常见问题解答）",
        },
        {},
        False
    ),
    (
        "osrs-how-to-train-prayer-cheap-f2p.html",
        "OSRS F2P最便宜祈祷训练指南2026",
        "OSRS F2P最便宜祈祷训练指南 — 大骨头、Ectofuntus与成本分析",
        "最新的F2P祈祷省钱训练方法。从Hill Giants免费获得大骨头，使用Ectofuntus获得4倍经验值。对比所有骨头类型、详细成本分析到99级，以及重要的祈祷等级里程碑。",
        {
            "Prayer Training Methods — XP Multipliers": "Prayer Training Methods — XP Multipliers（祈祷训练方法——经验倍率）",
            "F2P Bone Types & XP Values": "F2P Bone Types & XP Values（F2P骨头类型与经验值）",
            "The Ectofuntus — Step by Step": "The Ectofuntus — Step by Step（Ectofuntus——逐步教程）",
            "Farming Big Bones from Hill Giants (Free Method)": "Farming Big Bones from Hill Giants (Free Method)（从Hill Giants刷大骨头 - 免费方法）",
            "Cost to 99 Prayer — F2P Methods Comparison": "Cost to 99 Prayer — F2P Methods Comparison（99祈祷成本——F2P方法对比）",
            "Important Prayer Level Milestones": "Important Prayer Level Milestones（重要祈祷等级里程碑）",
            "Money-Saving Tips": "Money-Saving Tips（省钱技巧）",
            "Frequently Asked Questions": "Frequently Asked Questions（常见问题解答）",
        },
        {
            "1. Prayer Training Methods — XP Multipliers": "1. Prayer Training Methods — XP Multipliers（1. 祈祷训练方法——经验倍率）",
            "2. F2P Bone Types & XP Values": "2. F2P Bone Types & XP Values（2. F2P骨头类型与经验值）",
            "3. The Ectofuntus — Step by Step": "3. The Ectofuntus — Step by Step（3. Ectofuntus——逐步教程）",
            "4. Farming Big Bones from Hill Giants (Free Method)": "4. Farming Big Bones from Hill Giants (Free Method)（4. 从Hill Giants刷大骨头 - 免费方法）",
            "5. Cost to 99 Prayer — F2P Methods Comparison": "5. Cost to 99 Prayer — F2P Methods Comparison（5. 99祈祷成本——F2P方法对比）",
            "6. Important Prayer Level Milestones": "6. Important Prayer Level Milestones（6. 重要祈祷等级里程碑）",
            "7. Money-Saving Tips": "7. Money-Saving Tips（7. 省钱技巧）",
            "8. Frequently Asked Questions": "8. Frequently Asked Questions（8. 常见问题解答）",
        },
        {},
        True
    ),
    (
        "osrs-ironman-money-making-f2p-2026.html",
        "OSRS铁人模式F2P赚钱指南2026",
        "OSRS铁人模式F2P赚钱指南 — 最佳方法详解",
        "完整的F2P铁人模式赚钱指南。8种方法按照GP/小时排序，涵盖Cowhide、Hill Giants、Greater Demons和Rune Mining。适合不同阶段的铁人玩家参考。",
        {
            "Why F2P Ironman \"Money Making\" Is Different": "Why F2P Ironman \"Money Making\" Is Different（为什么F2P铁人模式的\"赚钱\"不一样）",
            "Early Game Methods (Total Level Under 500)": "Early Game Methods (Total Level Under 500)（前期方法 - 总等级500以下）",
            "Mid Game Methods (Total Level 500-1000)": "Mid Game Methods (Total Level 500-1000)（中期方法 - 总等级500-1000）",
            "Late Game Methods (Combat Level 80+, High Skills)": "Late Game Methods (Combat Level 80+, High Skills)（后期方法 - 战斗80+，高技能）",
            "Passive Methods While Training": "Passive Methods While Training（训练中的被动方法）",
            "Priority Order for F2P Ironman Progress": "Priority Order for F2P Ironman Progress（F2P铁人模式优先级顺序）",
            "Related Guides You Might Like": "Related Guides You Might Like（你可能喜欢的相关指南）",
        },
        {
            "Why F2P Ironman \"Money Making\" Is Different": "Why F2P Ironman \"Money Making\" Is Different（为什么F2P铁人模式的\"赚钱\"不一样）",
            "Early Game Methods (Total Level Under 500)": "Early Game Methods (Total Level Under 500)（前期方法 - 总等级500以下）",
            "Mid Game Methods (Total Level 500-1000)": "Mid Game Methods (Total Level 500-1000)（中期方法 - 总等级500-1000）",
            "Late Game Methods (Combat Level 80+, High Skills)": "Late Game Methods (Combat Level 80+, High Skills)（后期方法 - 战斗80+，高技能）",
            "Passive Methods While Training": "Passive Methods While Training（训练中的被动方法）",
            "Priority Order for F2P Ironman Progress": "Priority Order for F2P Ironman Progress（F2P铁人模式优先级顺序）",
        },
        {
            "1. Killing Cows — Cowhide & Bones (Level 1+ Combat)": "1. Killing Cows — Cowhide & Bones (Level 1+ Combat)（1. 杀牛 - 牛皮与骨头，战斗1+）",
            "2. Mining Iron Ore — Smithing & Bank Filler (Level 15 Mining)": "2. Mining Iron Ore — Smithing & Bank Filler (Level 15 Mining)（2. 挖铁矿 - 锻造与银行填充，挖矿15）",
            "3. Fishing Shrimp and Anchovies (Level 1-40 Fishing)": "3. Fishing Shrimp and Anchovies (Level 1-40 Fishing)（3. 钓鱼虾与凤尾鱼，钓鱼1-40）",
            "4. Killing Hill Giants — Limpwurt Roots & Big Bones (Level 40+ Combat)": "4. Killing Hill Giants — Limpwurt Roots & Big Bones (Level 40+ Combat)（4. 杀Hill Giants - Limpwurt根与大骨头，战斗40+）",
            "5. Crafting Gold Jewelry — Coins from NPC Shops (Level 40 Crafting)": "5. Crafting Gold Jewelry — Coins from NPC Shops (Level 40 Crafting)（5. 制作金首饰 - NPC商店换金币，制作40）",
            "6. Mining Coal — Smithing Fuel & GP (Level 30 Mining)": "6. Mining Coal — Smithing Fuel & GP (Level 30 Mining)（6. 挖煤 - 锻造燃料与金币，挖矿30）",
            "7. Killing Greater Demons — Rune Full Helm & Key Halves": "7. Killing Greater Demons — Rune Full Helm & Key Halves（7. 杀大恶魔 - Rune全盔与钥匙碎片）",
            "8. Rune Rock Mining — Highest Tier F2P Ore (Level 85 Mining)": "8. Rune Rock Mining — Highest Tier F2P Ore (Level 85 Mining)（8. 挖Rune矿 - F2P最高级矿石，挖矿85）",
            "Alchemy on the Go": "Alchemy on the Go（随身高炼）",
            "Collecting Noted Resources from Spawn Points": "Collecting Noted Resources from Spawn Points（从刷新点收集已备注资源）",
        },
        True
    ),
]


def process_file(filename, cn_title_suffix, cn_title_short, cn_summary, toc_trans, h2_trans, h3_trans, has_quick_box):
    en_path = os.path.join(EN_DIR, filename)
    zh_path = os.path.join(ZH_DIR, filename)

    # Read English file
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()

    # Read existing Chinese file (for title and canonical URL)
    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_html_old = f.read()

    # Extract Chinese title from old zh file (the <title> tag)
    title_match = re.search(r'<title>(.*?)</title>', zh_html_old)
    cn_title = title_match.group(1) if title_match else ""

    # Extract canonical URL from old zh file
    canon_match = re.search(r'<link rel="canonical" href="([^"]+)"', zh_html_old)
    cn_canonical = canon_match.group(1) if canon_match else f"https://osrsguru.com/zh/guides/{filename}"

    # Build new zh HTML from English
    html = en_html

    # Step 1: Change lang
    html = html.replace('<html lang="en">', '<html lang="zh-Hans">')

    # Step 2: Change canonical URL to zh version  
    # The English canonical points to ../guides/... vs the zh one points to ../zh/guides/...
    # Replace the canonical href pattern
    en_canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if en_canon:
        old_canon = en_canon.group(1)
        # Build zh canonical based on the old zh file
        html = html.replace(old_canon, cn_canonical)

    # Step 3: Change OG URL to zh version
    og_url_pattern = re.compile(r'(<meta property="og:url" content=")([^"]+)(")')
    def replace_og_url(m):
        prefix = m.group(1)
        url = m.group(2)
        suffix = m.group(3)
        # Determine the zh URL from canonical
        zh_url = cn_canonical
        return f'{prefix}{zh_url}{suffix}'
    html = og_url_pattern.sub(replace_og_url, html)

    # Step 4: In the hero section, before the English h1, add cn-title and cn-summary
    # Find the first <h1> in the guide-hero section
    hero_h1_pattern = re.compile(r'(<section class="guide-hero">.*?)(<h1[^>]*>.*?</h1>)', re.DOTALL)
    
    def add_cn_before_h1(m):
        before = m.group(1)
        h1_tag = m.group(2)
        cn_block = f'''
           <h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title_suffix}</h1>
            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>
            {h1_tag}'''
        return before + cn_block
    
    # Also handle the osrs-first-boss-progression file which has different hero structure
    if "first-boss-progression" in filename:
        # This file uses <section class="guide-hero"> with direct content
        hero_pattern = re.compile(r'(<section class="guide-hero">.*?)(<h1[^>]*>.*?</h1>)', re.DOTALL)
        html = hero_pattern.sub(add_cn_before_h1, html)
    elif "ironman" in filename:
        # Ironman file has different hero structure with class="article-hero" and h1 has class="article-title"
        hero_pattern = re.compile(r'(<section class="article-hero">.*?)(<h1[^>]*>.*?</h1>)', re.DOTALL)
        html = hero_pattern.sub(add_cn_before_h1, html)
    else:
        html = hero_h1_pattern.sub(add_cn_before_h1, html)

    # Step 5: Translate TOC items
    # Pattern: <a href="#xxx">Title</a> 
    for orig, trans in toc_trans.items():
        escaped = re.escape(orig)
        # Match the TOC link pattern - use lambda to avoid backreference issues
        pattern = re.compile(r'(<a href="#[^"]*">)\s*' + escaped + r'\s*(</a>)')
        html = pattern.sub(lambda m: m.group(1) + trans + m.group(2), html)

    # Step 6: Translate h2 headings
    for orig, trans in h2_trans.items():
        escaped = re.escape(orig)
        pattern = re.compile(r'(<h2[^>]*>)\s*' + escaped + r'\s*(</h2>)')
        html = pattern.sub(lambda m, t=trans: m.group(1) + t + m.group(2), html)

    # Step 7: Translate h3 headings
    for orig, trans in h3_trans.items():
        escaped = re.escape(orig)
        pattern = re.compile(r'(<h3[^>]*>)\s*' + escaped + r'\s*(</h3>)')
        html = pattern.sub(lambda m, t=trans: m.group(1) + t + m.group(2), html)

    # Step 8: Handle quick-preview-box (quick-summary) English to Chinese
    if has_quick_box:
        # Translate the text content of quick-summary divs
        # The translation patterns vary per file - we'll handle specific patterns for each
        if "cooking" in filename:
            html = html.replace(
                "Cooking is the easiest first 99. Pick the method that matches your membership status:",
                "烹饪是最容易达到的99级。选择适合你的会员状态的方法："
            )
            html = html.replace(
                "<strong>Fastest members:</strong> Karambwans (1-tick) — 950K+ XP/hr, 30–35 hours to 99",
                "<strong>最快会员方法：</strong>卡兰布万鱼（1-tick）— 95万+经验/小时，30-35小时到99级"
            )
            html = html.replace(
                "<strong>Fastest F2P:</strong> Wines of Zamorak — 400K+ XP/hr, 60–80 hours to 99",
                "<strong>最快F2P方法：</strong>萨莫拉克之酒 — 40万+经验/小时，60-80小时到99级"
            )
            html = html.replace(
                "<strong>Typical cost:</strong> 10–30M members; 5–10M F2P with wines",
                "<strong>典型成本：</strong>会员1000-3000万；F2P葡萄酒法500-1000万"
            )
            html = html.replace(
                "<strong>Cape perk:</strong> 0% burn rate on all food forever",
                "<strong>披风效果：</strong>所有食物永久0%烧焦率"
            )
            html = html.replace(
                "⏱️ 30-Second Quick Summary",
                "⏱️ 30秒快速摘要"
            )
        elif "first-boss" in filename:
            html = html.replace(
                "<strong>10 bosses in progression order</strong> — from Giant Mole (Combat 30, F2P) to Vorkath (Combat 70+, 2M-4M GP/hr)",
                "<strong>按顺序排列的10个Boss</strong> — 从巨鼹鼠（战斗30，F2P）到沃卡什（战斗70+，200-400万GP/小时）"
            )
            html = html.replace(
                "<strong>Start bossing at Combat 30</strong> — Giant Mole earns 200K-400K GP/hr, Obor drops Rune items worth 100K+",
                "<strong>战斗30级开始打Boss</strong> — 巨鼹鼠每小时20-40万GP，奥博尔掉落价值10万+的Rune装备"
            )
            html = html.replace(
                "<strong>Members breakpoint:</strong> Barrows at Combat 50+ — 500K-1M GP/hr with Iban's Staff, minimal gear needed",
                "<strong>会员转折点：</strong>战斗50+打巴罗斯 — 使用Iban法杖每小时50-100万GP，装备要求低"
            )
            html = html.replace(
                "<strong>Zulrah at Combat 65+:</strong> 500K-3M GP/hr, unlocks mid-game wealth — learn rotations in 10-20 attempts",
                "<strong>战斗65+打祖拉：</strong>每小时50-300万GP，解锁中期财富 — 10-20次尝试学会轮换"
            )
            html = html.replace(
                "<strong>Gear priority:</strong> Iban's Staff → Rune Crossbow → Toxic Trident → Blowpipe — upgrade in that order",
                "<strong>装备优先级：</strong>Iban法杖 → Rune弩 → Toxic三叉戟 → Blowpipe — 按此顺序升级"
            )
            html = html.replace("⏱️ Quick Summary &mdash; 30-Second Read", "⏱️ 快速摘要 — 30秒阅读")
        elif "flipping" in filename:
            html = html.replace(
                "<strong>Start with just 100K GP</strong> — fire runes, feathers, and cannonballs have 1-15 GP margins and 10K+ buy limits",
                "<strong>只需10万GP起步</strong> — 火符文、羽毛和炮弹有1-15GP的差价和1万+的买入限额"
            )
            html = html.replace(
                "<strong>Target 7% daily ROI</strong> — 100K → 1M GP in ~13 days with consistent checking every 4 hours",
                "<strong>目标7%日回报率</strong> — 每4小时检查一次，约13天将10万变成100万GP"
            )
            html = html.replace(
                "<strong>20+ best flip items ranked</strong> — from under 1M GP to 10M+ GP capital brackets",
                "<strong>20+个最佳倒卖物品排名</strong> — 从低于100万到1000万+GP资金档位"
            )
            html = html.replace(
                "<strong>Margin checking takes 30 seconds</strong> — buy 1 at +20%, sell 1 at -20%, the difference is your margin",
                "<strong>差价检查只需30秒</strong> — 以+20%买入1个，以-20%卖出1个，差额就是你的差价"
            )
            html = html.replace(
                "<strong>Scale up fast:</strong> flip multiple items simultaneously — buy limits are per-item, not per-account",
                "<strong>快速扩大规模：</strong>同时倒卖多种物品 — 买入限额按物品计算，不按账号"
            )
            html = html.replace("⏱️ Quick Summary &mdash; 30-Second Read", "⏱️ 快速摘要 — 30秒阅读")
        elif "prayer" in filename:
            html = html.replace(
                "Prayer is expensive, but F2P players can train it cheaply with the right bone strategy:",
                "祈祷训练很昂贵，但F2P玩家可以用正确的骨头策略省钱训练："
            )
            html = html.replace(
                "<strong>Cheapest F2P method:</strong> Big Bones at the Ectofuntus — 4x XP (60 XP per bone)",
                "<strong>最便宜的F2P方法：</strong>在Ectofuntus使用大骨头 — 4倍经验（每根60经验）"
            )
            html = html.replace(
                "<strong>Free option:</strong> Kill Hill Giants in Edgeville Dungeon for Big Bones",
                "<strong>免费选择：</strong>在Edgeville地牢杀Hill Giants获得大骨头"
            )
            html = html.replace(
                "<strong>Cost to 99:</strong> ~39M via Ectofuntus vs ~156M by burying Big Bones",
                "<strong>到99级成本：</strong>使用Ectofuntus约3900万 vs 直接埋大骨头约1.56亿"
            )
            html = html.replace(
                "<strong>Key milestone:</strong> Level 43 for Protect from Melee",
                "<strong>关键里程碑：</strong>43级解锁近战保护祈祷"
            )
        elif "ironman" in filename:
            html = html.replace(
                "<strong>Ironman F2P is Different:</strong> No GE access — wealth = stockpiled resources, not GP",
                "<strong>铁人模式F2P不同：</strong>无法使用交易所 — 财富=囤积的资源，不是金币"
            )
            html = html.replace(
                "<strong>Early Game:</strong> Cows for cowhides + bones → Crafting & Prayer XP combined",
                "<strong>前期：</strong>杀牛获得牛皮+骨头 → 制作和祈祷经验双收"
            )
            html = html.replace(
                "<strong>Mid Game:</strong> Hill Giants for big bones + limpwurt roots (~15K-25K GP/hr in drops)",
                "<strong>中期：</strong>Hill Giants刷大骨头+Limpwurt根（掉落约1.5-2.5万GP/小时）"
            )
            html = html.replace(
                "<strong>Late Game:</strong> Greater Demons (rune helm drop) and rune rock mining (55K-110K GP/hr)",
                "<strong>后期：</strong>大恶魔（Rune头盔掉落）和挖Rune矿（5.5-11万GP/小时）"
            )
            html = html.replace(
                "<strong>Key Tip:</strong> Go members at combat 60+ for 3-5x faster progression",
                "<strong>关键提示：</strong>战斗60+后转会员可获得3-5倍更快的进度"
            )

    # Write the result
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Processed: {filename}")


# Process all 7 files
for file_data in files:
    filename = file_data[0]
    print(f"\nProcessing {filename}...")
    process_file(*file_data)

print("\n🎉 All 7 files processed successfully!")
