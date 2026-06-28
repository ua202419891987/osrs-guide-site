#!/usr/bin/env python3
"""
批量给OSRS攻略文章添加M+格式：
1. guide-hero区加中文H1
2. 加中文导语
3. 所有H2/H3标题加（中文翻译）
"""

import re
import os

BASE = r"C:\Users\Lenovo\osrs-guide-site\zh\guides"
OUT = r"C:\Users\Lenovo\WorkBuddy\2026-06-28-07-19-44\mplus_output"

# ===== 每篇文章的中文H1标题和中文导语 =====
DATA = {
    "blood-moon-rises-quest-guide-2026.html": {
        "cn_title": "OSRS 血月崛起任务攻略（2026版）",
        "cn_summary": "Myreque系列终章——血月化身Boss战多阶段机制、谜题解法、完整通关流程。包含所有技能要求、装备推荐、战利品和后续内容详解。"
    },
    "new-boss-loot-guide-2026.html": {
        "cn_title": "OSRS 2026新Boss击杀与掉落攻略",
        "cn_summary": "2026年全部新Boss机制详解。Moolord（牛魔王）的掉落表、单人/团队策略、GP/小时收益分析和宠物掉率。从入门到精通。"
    },
    "osrs-blood-moon-rises-prep-checklist-detailed-2026.html": {
        "cn_title": "OSRS 血月崛起前置准备完整清单（2026版）",
        "cn_summary": "最全面的血月崛起Grandmaster任务前置准备指南。包含全部前置任务清单、推荐属性等级、装备配置、物品采购清单（含GE价格）和4周筹备时间表。"
    },
    "osrs-bond-vs-subscription-2026.html": {
        "cn_title": "OSRS 绑定券 vs 订阅会员（2026版）——哪个更划算？",
        "cn_summary": "2026年绑定券涨至约520万GP，订阅涨至14.99美元/月。通过GP/小时计算、盈亏分析和玩家类型匹配，帮你决定用真金白银还是游戏币续费。"
    },
    "osrs-cancel-membership-refund-2026.html": {
        "cn_title": "OSRS 取消会员与退款指南（2026版政策）",
        "cn_summary": "完整取消OSRS会员自动续费、向Jagex申请退款的详细步骤指南。涵盖各平台取消方式、退款政策解读、取消后账号状态变化及省钱替代方案。"
    },
    "osrs-chambers-of-xeric-loot-profit-guide.html": {
        "cn_title": "OSRS 沙力克密室战利品与收益攻略（2026版）",
        "cn_summary": "沙力克密室（Raids 1）是OSRS中最赚钱的活动之一。扭曲弓价值超过11亿GP，普通战利品也能提供稳定收入。本文详解完整掉落表、点数系统及单人/组队每小时收益分析。"
    },
    "osrs-cheapest-membership-2026.html": {
        "cn_title": "OSRS 最便宜会员获取方式（2026版·合法途径）",
        "cn_summary": "2026年OSRS会员费用上涨后，逐一对比所有合法支付方式：月付/季付/年付、绑定券、第三方零售平台和购买时机策略。提供每账号每年最省钱的完整方案。"
    },
    "osrs-combat-achievements-easy-walkthrough-2026.html": {
        "cn_title": "OSRS 简易战斗成就完全通关攻略（全部35项任务·2026版）",
        "cn_summary": "最完整的35项Easy级战斗成就（CA）指南。每项任务精确说明：要求、分步完成方法、推荐装备和技巧。包含Ghommal's Hilt 1（+5%伤害）解锁路线和进阶Medium级准备。"
    },
    "osrs-corrupted-gauntlet-guide-2026.html": {
        "cn_title": "OSRS 腐化Gauntlet攻略（2026版）——低配装方案与策略",
        "cn_summary": "零成本投入，每小时500万GP。Tier 1和Tier 2护甲准备策略、Hunllef Boss机制详解、祷告切换技巧和完整掉落分析。无需满属性或顶级装备。"
    },
    "osrs-curse-of-the-empty-lord-quest-2026.html": {
        "cn_title": "OSRS 空之诅咒迷你任务攻略——找到Viggora获取幽灵长袍",
        "cn_summary": "空之诅咒迷你任务完整攻略：三个Viggora刷新坐标、幽灵长袍全套属性、Zaros背叛剧情故事。15-30分钟即可完成，获得OSRS最稀有幻化套装之一。"
    },
    "osrs-desert-treasure-quest-guide-low-level.html": {
        "cn_title": "OSRS 沙漠宝藏低等级攻略（2026版）——Boss打法与古代魔法解锁",
        "cn_summary": "为低等级玩家量身定做的沙漠宝藏攻略。Dessous、Kamil、Fareed和Damis四个Boss的取巧打法、安全点位、最低属性要求，以及古代魔法（Ancient Magicks）解锁后的实战价值。"
    },
    "osrs-diary-easy-medium-complete-guide-2026.html": {
        "cn_title": "OSRS 简易与中等成就日记全区域通关攻略（2026版）",
        "cn_summary": "完成OSRS全部12个区域的Easy和Medium级成就日记。每项任务精确解决方案、最优路线规划和必备物品清单。从Lumbridge到Varlamore全覆盖。"
    },
    "osrs-diary-priority-order-beginner-2026.html": {
        "cn_title": "OSRS 成就日记优先顺序指南——新手必做的10个日记（2026版）",
        "cn_summary": "数据驱动的成就日记优先顺序排名。按奖励价值、时间投入和对新手/中期的实用性，选出了最具性价比的10个日记。别在低价值日记上浪费时间。"
    }
}

# ===== H2/H3中文翻译映射 =====
H2_H3_TRANSLATIONS = {
    # blood-moon-rises-quest-guide-2026.html
    "Quest Overview & Lore": "任务概述与背景故事",
    "Quest Lore (Spoiler-Free)": "任务背景（无剧透）",
    "Quest Details": "任务详情",
    "Quest Requirements (Skills, Quests, Items)": "任务要求（技能、前置任务、物品）",
    "Skill Requirements": "技能要求",
    "Quest Requirements": "前置任务要求",
    "Item Requirements (Bring These!)": "物品要求（务必携带）",
    "Step-by-Step Walkthrough (Spoiler-Light)": "分步通关攻略（低剧透）",
    "Step 1: Speak to Veliaf Hurtz": "第一步：与Veliaf Hurtz对话",
    "Step 2: Investigate the Blood Moon Temple": "第二步：调查血月神殿",
    "Step 3: Solve the Blood Moon Puzzle": "第三步：解开血月谜题",
    "Step 4: Defeat the Blood Moon Avatar (Phase 1)": "第四步：击败血月化身（第一阶段）",
    "Step 5: The Collapsing Temple (Agility Puzzle)": "第五步：坍塌神殿（敏捷谜题）",
    "Step 6: Final Showdown (Phase 2)": "第六步：最终决战（第二阶段）",
    "Step 7: Claim Your Rewards": "第七步：领取奖励",
    "Boss Fight Strategies (All Phases)": "Boss战斗策略（所有阶段）",
    "Phase 1: The Avatar's First Form (HP 1000-700)": "第一阶段：化身初形（HP 1000-700）",
    "Phase 2: The Avatar's True Form (HP 700-0)": "第二阶段：化身真身（HP 700-0）",
    "Recommended Gear for Boss Fight": "Boss战推荐装备",
    "Puzzle Solutions": "谜题解法",
    "Puzzle 1: The Lunar Altar Alignment": "谜题1：月坛对齐",
    "Puzzle 2: The Collapsing Temple (Agility)": "谜题2：坍塌神殿（敏捷）",
    "Puzzle 3: The Blood Moon Seal (Memory Game)": "谜题3：血月封印（记忆游戏）",
    "Quest Rewards (XP, Gear, Unlocks)": "任务奖励（经验、装备、解锁内容）",
    "XP Rewards": "经验奖励",
    "GP Reward": "金币奖励",
    "New Gear & Items": "新装备与物品",
    "Unlocks & Access": "解锁内容与权限",
    "Post-Quest Content & Unlocks": "任务后内容与解锁",
    "Blood Moon Island": "血月岛",
    "Myreque Shop Upgrades": "Myreque商店升级",
    "New Slayer Tasks (Blood Moon Creatures)": "新杀戮任务（血月生物）",
    "Post-Quest Miniquest: \"The Blood Moon Legacy\"": "任务后迷你任务：\"血月遗产\"",
    "Ironman-Specific Tips": "铁人模式专属技巧",
    "Ironman Preparation": "铁人模式准备",
    "Ironman Gear Progression (for Quest)": "铁人模式装备进阶（任务用）",
    "Common Mistakes & How to Avoid Them": "常见错误与避免方法",
    "Mistake 1: Not Bringing a Blisterwood Weapon": "错误1：未携带Blisterwood武器",
    "Mistake 2: Running Out of Prayer Potions": "错误2：祷告药水用完",
    "Mistake 3: Failing the Agility Puzzle (Collapsing Temple)": "错误3：敏捷谜题失败（坍塌神殿）",
    "Mistake 4: Not Wearing Anti-Poison": "错误4：未携带解毒剂",
    "Mistake 5: Forgetting to Upgrade Blisterwood Staff to Sword": "错误5：忘记升级Blisterwood法杖为剑",
    "Frequently Asked Questions": "常见问题",
    
    # new-boss-loot-guide-2026.html  
    "2026 New Bosses Overview": "2026年新Boss概览",
    "Moolord — The Bovine Terror": "Moolord——牛魔王恐怖",
    "Location & Access": "位置与入口",
    "Boss Stats": "Boss属性",
    "Gear Requirements": "装备要求",
    "Budget Setup (2M—10M GP)": "经济配置（200万-1000万GP）",
    "Mid-Game Setup (20M—100M GP)": "中期配置（2000万-1亿GP）",
    "High-End Setup (500M+ GP)": "高端配置（5亿+ GP）",
    "Kill Mechanics & Phases": "击杀机制与阶段",
    "Phase 1: The Graze (100%—66% HP)": "第一阶段：放牧（100%-66% HP）",
    "Phase 2: The电荷 (66%—33% HP)": "第二阶段：蓄能（66%-33% HP）",
    "Phase 3: The Stampede (33%—0% HP)": "第三阶段：狂奔（33%-0% HP）",
    "Special Mechanic: The Golden Calf": "特殊机制：金色牛犊",
    "Solo vs Team Strategies": "单人 vs 团队策略",
    "Solo Strategy": "单人策略",
    "Team Strategy (2—5 players)": "团队策略（2-5人）",
    "Drop Tables & GP Values": "掉落表与GP价值",
    "Unique Drops": "独特掉落",
    "Standard Drops": "标准掉落",
    "Drop Rate Calculations": "掉率计算",
    "Money-Making Potential (GP/hr)": "赚钱潜力（GP/小时）",
    "GP/hr by Gear Level": "按装备等级的GP/小时",
    "Pet Drops & Drop Rates": "宠物掉落与掉率",
    "Pet Drop Rate Modifiers": "宠物掉率修正",
    "Ironman Strategies": "铁人模式策略",
    "Gear Progression for Ironmen": "铁人装备进阶路线",
    "Ironman-Specific Tips": "铁人模式专属技巧",
    "Ironman Expected Loot Value": "铁人预期掉落价值",

    # osrs-cheapest-membership-2026.html
    "① 💳 All Legal Ways to Buy Membership (Full Price List)": "① 所有合法会员购买方式（完整价目表）",
    "1.1 📋 Complete Price List (USD, as of June 2026)": "1.1 完整价格表（美元，2026年6月）",
    "1.2 🔄 Recurring vs One-Time (Game Pass)": "1.2 循环订阅 vs 一次性购买（Game Pass）",
    "1.3 🎮 What About Premier Club? (Historical Context)": "1.3 Premier Club呢？（历史背景）",
    "1.4 🌐 RS3 vs OSRS Membership: Do You Need Both?": "1.4 RS3 vs OSRS会员：两者都需要吗？",
    "② 📊 Monthly vs Quarterly vs Yearly — The Math": "② 月付 vs 季付 vs 年付——算笔账",
    "2.1 🧮 Yearly Cost Comparison (1 Account)": "2.1 年度费用对比（1个账号）",
    "2.2 💸 Breakeven Point: When Does Annual Beat Monthly?": "2.2 盈亏平衡点：年付何时优于月付？",
    "2.3 🔁 Can You Stack Multiple Game Passes?": "2.3 可以叠加多个Game Pass吗？",
    "2.4 📅 Monthly Recurring: The \"Cancel After First Month\" Trick": "2.4 月循环：\"首月后取消\"技巧",
    "③ 📜 Bonds: The In-Game Currency Route": "③ 绑定券：游戏币渠道",
    "3.1 💰 How Much GP Do You Need for a Bond?": "3.1 一个绑定券需要多少GP？",
    "3.2 📈 Is Buying Bonds with Real Money Ever Worth It?": "3.2 用真钱买绑定券划算吗？",
    "3.3 🎯 Who Should Use Bonds (and Who Shouldn't)": "3.3 谁应该用绑定券（谁不应该）",
    "3.4 🔄 Bond-to-GP-to-Membership: The Cycle": "3.4 绑定券→GP→会员的循环",
    "④ 🛒 Third-Party Retailers (Legitimate Ones Only)": "④ 第三方零售商（仅合法途径）",
    "4.1 🏷️ Authorized Retailers Comparison": "4.1 授权零售商对比",
    "4.2 🛡️ Are Third-Party Codes Safe?": "4.2 第三方兑换码安全吗？",
    "4.3 🌍 Regional Code Differences": "4.3 区域码差异",
    "4.4 ⚠️ Retailers to Avoid": "4.4 应避免的零售商",
    "⑤ ⏰ Timing Your Purchase — When Is Cheapest?": "⑤ 把握购买时机——何时最便宜？",
    "5.1 📅 Annual Sale Calendar": "5.1 年度促销日历",
    "5.2 🎯 The \"Buy Once, Play for Years\" Strategy": "5.2 \"一次购买，多年畅玩\"策略",
    "5.3 🚫 When NOT to Buy": "5.3 何时不买",
    "⑥ 🌍 Regional Pricing & VPN Considerations": "⑥ 区域定价与VPN考量",
    "6.1 🌐 Regional Price Differences (Approximate)": "6.1 区域价格差异（近似值）",
    "6.2 ⚠️ VPN Purchasing: Risk Assessment": "6.2 VPN购买：风险评估",
    "6.3 ✅ Safer Alternative: Regional Gift Cards": "6.3 更安全的替代：区域礼品卡",
    "⑦ 🏆 The Ultimate Money-Saving Strategy": "⑦ 终极省钱策略",
    "7.1 🥇 The #1 Cheapest Method (Step by Step)": "7.1 最省钱方法（分步详解）",
    "7.2 💰 Total Savings Calculation": "7.2 总节省金额计算",
    "7.3 🔄 Alternative: The Bond Hybrid": "7.3 替代方案：绑定券混合模式",
    "⑧ ⚠️ Scams to Avoid (Important!)": "⑧ 应避免的骗局（重要！）",
    "8.1 🚫 Common Scam Types": "8.1 常见骗局类型",
    "8.2 🛡️ Golden Rules for Safe Purchasing": "8.2 安全购买黄金法则",
    "⑨ ❓ FAQ — Cheapest OSRS Membership": "⑨ 常见问题——最便宜OSRS会员",
    "9.1 ❓ Is it legal to buy OSRS membership from CDKeys?": "9.1 从CDKeys购买OSRS会员合法吗？",
    "9.2 ❓ Can I get banned for using a VPN to buy cheaper membership?": "9.2 用VPN买便宜会员会被封号吗？",
    "9.3 ❓ What's the absolute cheapest way to get membership?": "9.3 最便宜的会员方式是什么？",
    "9.4 ❓ Can I share membership between OSRS and RS3?": "9.4 OSRS和RS3可以共享会员吗？",
    "9.5 ❓ Do bonds ever go on sale?": "9.5 绑定券会打折吗？",
    "9.6 ❓ Can I refund a membership purchase?": "9.6 可以退会员费吗？",
    "9.7 ❓ Is it cheaper to buy multiple months at once?": "9.7 一次性购买多个月更便宜吗？",
    "⑩ 💡 Final Tips & Recommendations": "⑩ 终极建议与推荐",
    "10.1 📋 Quick Summary": "10.1 快速总结",
    "10.2 🎯 Decision Matrix by Player Type": "10.2 按玩家类型的决策矩阵",
    "10.3 🔗 Related Guides": "10.3 相关攻略",

    # osrs-bond-vs-subscription-2026.html
    "1. 🎟️ What is an OSRS Bond?": "1. 什么是OSRS绑定券？",
    "2. 💰 Bond vs Subscription — Price Comparison": "2. 绑定券 vs 订阅——价格对比",
    "① 📊 Cost Comparison Table": "费用对比表",
    "② ⏱️ Time Investment — The Real Cost of Bonds": "时间投入——绑定券的真实成本",
    "3. ⛏️ GP Farming Calculator — Can You Afford a Bond?": "3. GP赚取计算器——你买得起绑定券吗？",
    "① 🧮 Bond Farming Calculator": "绑定券赚取计算器",
    "② 🎯 Best F2P Methods (No Membership Needed)": "最佳免费玩家方法（无需会员）",
    "③ 🏆 Best Members Methods (Much Faster)": "最佳会员方法（快得多）",
    "4. 📊 Break-Even Analysis — When Bond Wins": "4. 盈亏平衡分析——绑定券何时划算",
    "① 💵 The $14.99 Threshold": "14.99美元门槛",
    "② 🔄 When Bonds Make Sense (The 3 Scenarios)": "绑定券划算的3种场景",
    "③ ❌ When Subscription Wins (The 3 Scenarios)": "订阅胜出的3种场景",
    "5. ✅ Who Should Use Bonds (Not Subscribe)": "5. 谁应该用绑定券（而非订阅）",
    "6. ✅ Who Should Subscribe (Not Bond)": "6. 谁应该订阅（而非绑定券）",
    "7. ❓ FAQs — OSRS Bonds vs Subscriptions 2026": "7. 常见问题——绑定券 vs 订阅 2026",

    # osrs-cancel-membership-refund-2026.html
    "① 🤔 Before You Cancel — Consider These First": "① 取消前请三思",
    "1.1 🎯 Why Do You Want to Cancel?": "1.1 为什么要取消？",
    "1.2 ⏰ The Timing Matters": "1.2 时机很重要",
    "② 🔧 How to Cancel Auto-Renewal (Step-by-Step)": "② 如何取消自动续费（分步指南）",
    "2.1 💻 Method 1: Jagex Website (Recommended)": "2.1 方法1：Jagex官网（推荐）",
    "2.2 📱 Method 2: In-Game (Quick Method)": "2.2 方法2：游戏内取消（快速）",
    "2.3 🎮 Method 3: Platform-Specific (Steam, iOS, Android, Console)": "2.3 方法3：各平台取消（Steam、iOS、安卓、主机）",
    "③ 💰 Jagex Refund Policy 2026 — What You Need to Know": "③ Jagex退款政策2026——须知事项",
    "3.1 📜 The Official Policy": "3.1 官方政策",
    "3.2 ⏱️ Time Windows That Matter": "3.2 关键时间窗口",
    "3.3 🌍 Regional Differences": "3.3 地区差异",
    "④ 📋 How to Request a Refund": "④ 如何申请退款",
    "4.1 📧 Step 1: Gather Your Information": "4.1 第一步：收集信息",
    "4.2 ✉️ Step 2: Submit a Support Ticket": "4.2 第二步：提交支持工单",
    "4.3 ⏳ Step 3: Wait & Follow Up": "4.3 第三步：等待与跟进",
    "⑤ 📦 What Happens After Cancellation": "⑤ 取消后会发生什么",
    "5.1 🗓️ Your Membership Period Continues Until Expiry": "5.1 会员有效期持续至到期",
    "5.2 🎒 What Happens to Your Items & Bank?": "5.2 物品和银行会怎样？",
    "5.3 🌍 What You Can & Can't Do as F2P": "5.3 作为F2P能做和不能做的事",
    "⑥ 💡 Alternatives to Cancelling (Save Money Instead)": "⑥ 取消的替代方案（省钱）",
    "6.1 💎 Switch to Bond-Based Membership": "6.1 改用绑定券会员",
    "6.2 📆 Take a Structured Break (The \"Pause\" Strategy)": "6.2 有计划地休息（\"暂停\"策略）",
    "6.3 👥 Switch to Ironman Mode": "6.3 切换到铁人模式",
    "⑦ 🔄 Re-subscribing Later — Best Practices": "⑦ 日后重新订阅——最佳实践",
    "7.1 🔑 When to Re-subscribe": "7.1 何时重新订阅",
    "7.2 💰 Smart Re-subscription Tips": "7.2 聪明的重新订阅技巧",
    "⑧ ❓ FAQs — Cancellation & Refunds": "⑧ 常见问题——取消与退款",

    # osrs-combat-achievements-easy-walkthrough-2026.html
    "1. What Are Combat Achievements?": "1. 什么是战斗成就？",
    "📊 The Six Tiers of Combat Achievements": "战斗成就的六个等级",
    "🎁 Why Combat Achievements Matter": "战斗成就为何重要",
    "📱 How to Access Your Combat Achievements": "如何查看战斗成就",
    "2. Easy Combat Achievements — Complete List (All 35 Tasks)": "2. 简易战斗成就完整列表（全部35项）",
    "🗡️ Category 1: General Combat Tasks (10 Tasks)": "类别1：通用战斗任务（10项）",
    "Task 1: Deal 100 Damage to a Single Monster": "任务1：对单个怪物造成100伤害",
    "Task 2: Deal 500 Damage to a Single Monster": "任务2：对单个怪物造成500伤害",
    "Task 3: Deal 1,000 Damage to a Single Monster": "任务3：对单个怪物造成1000伤害",
    "Task 4: Kill 10 Monsters": "任务4：击杀10只怪物",
    "Task 5: Kill 50 Monsters": "任务5：击杀50只怪物",
    "Task 6: Kill 100 Monsters": "任务6：击杀100只怪物",
    "Task 7: Deal 50 Damage with a Single Hit": "任务7：单次攻击造成50伤害",
    "Task 8: Deal 100 Damage with a Single Hit": "任务8：单次攻击造成100伤害",
    "Task 9: Cast 50 Spells": "任务9：施放50次法术",
    "Task 10: Eat 50 Pieces of Food": "任务10：吃50份食物",
    "🏹 Category 2: Style-Specific Tasks (8 Tasks)": "类别2：风格专属任务（8项）",
    "Task 11: Kill a Monster with Melee Only": "任务11：仅用近战击杀怪物",
    "Task 12: Kill a Monster with Ranged Only": "任务12：仅用远程击杀怪物",
    "Task 13: Kill a Monster with Magic Only": "任务13：仅用魔法击杀怪物",
    "Task 14: Kill 10 Monsters with Melee": "任务14：用近战击杀10只怪物",
    "Task 15: Kill 10 Monsters with Ranged": "任务15：用远程击杀10只怪物",
    "Task 16: Kill 10 Monsters with Magic": "任务16：用魔法击杀10只怪物",
    "Task 17: Attack a Monster Using All Three Combat Styles in One Fight": "任务17：在一场战斗中用三种战斗风格攻击怪物",
    "Task 18: Complete a Slayer Task Using Only One Combat Style": "任务18：仅用一种战斗风格完成杀戮任务",
    "👑 Category 3: Boss-Related Tasks (7 Tasks)": "类别3：Boss相关任务（7项）",
    "Task 19: Kill the Giant Mole (1 Kill)": "任务19：击杀巨型鼹鼠（1次）",
    "Task 20: Kill Barrows Brother (Any Brother, 1 Kill)": "任务20：击杀Barrows兄弟（任意1次）",
    "Task 21: Kill the King Black Dragon (1 Kill)": "任务21：击杀黑龙王（1次）",
    "Task 22: Kill the Kraken (1 Kill)": "任务22：击杀海怪（1次）",
    "Task 23: Kill Skotizo (1 Kill)": "任务23：击杀Skotizo（1次）",
    "Task 24: Complete a Barrows Brother Encounter (Kill All 6 Brothers)": "任务24：完成一次Barrows全程（击杀全部6位兄弟）",
    "Task 25: Kill a Boss While Wearing a Full Set of Rune Armor": "任务25：穿全套符文盔甲击杀Boss",
    "⚔️ Category 4: Slayer Tasks (5 Tasks)": "类别4：杀戮任务（5项）",
    "Task 26: Complete a Slayer Task Assigned by Turael": "任务26：完成Turael分配的杀戮任务",
    "Task 27: Complete a Slayer Task Assigned by Mazchna": "任务27：完成Mazchna分配的杀戮任务",
    "Task 28: Kill 10 Slayer Creatures While on a Slayer Task": "任务28：在杀戮任务中击杀10只怪物",
    "Task 29: Use a Slayer Item on a Slayer Creature": "任务29：对杀戮怪物使用专属道具",
    "Task 30: Complete 5 Slayer Tasks in a Row (Consecutive)": "任务30：连续完成5个杀戮任务",
    "🏆 Category 5: PvM Milestones (5 Tasks)": "类别5：PvM里程碑（5项）",
    "Task 31: Kill 5 Bosses (Any Bosses, Cumulative)": "任务31：击杀5个Boss（累计）",
    "Task 32: Deal 50 Damage to a Boss Using Ranged": "任务32：用远程对Boss造成50伤害",
    "Task 33: Deal 50 Damage to a Boss Using Magic": "任务33：用魔法对Boss造成50伤害",
    "Task 34: Kill a Boss Without Taking Any Damage": "任务34：不受伤害击杀Boss",
    "Task 35: Open a Barrows Chest (Loot the Chest After Killing All Brothers)": "任务35：打开Barrows宝箱",
    "3. Optimal Completion Order": "3. 最佳完成顺序",
    "📋 Phase 1: Natural Completion (0 Extra Time)": "第一阶段：自然完成（无需额外时间）",
    "📋 Phase 2: Quick Wins (1–2 Hours Total)": "第二阶段：快速任务（共1-2小时）",
    "📋 Phase 3: Boss Tasks (2–5 Hours Total)": "第三阶段：Boss任务（共2-5小时）",
    "📋 Phase 4: The Long Grind (Tasks 30 + 8 + 100 Damage)": "第四阶段：耗时任务（任务30+8+100伤害）",
    "⏱️ Total Estimated Time to Complete All 35 Easy Tasks": "完成全部35项任务的预计总时间",
    "4. Ghommal's Hilt Guide — Rewards & Usage": "4. Ghommal's Hilt指南——奖励与使用",
    "🏆 Ghommal's Hilt 1: Full Stats & Effect": "Ghommal's Hilt 1：完整属性与效果",
    "⚔️ How the +5% Damage Boost Works (In Detail)": "+5%伤害加成详解",
    "🎨 Gilded Spear Upgrade": "镀金长矛升级",
    "📈 Upgrade Path: Hilt 1 → Hilt 2 → Hilt 3...": "升级路线",
    "🎯 Best Ways to Use Ghommal's Hilt 1": "Ghommal's Hilt 1的最佳使用方式",
    "5. Preparing for Medium Tier": "5. 准备Medium级",
    "📊 Medium Tier: What to Expect": "Medium级：期待什么",
    "🛡️ Gear You'll Need for Medium (Shopping List)": "Medium级所需装备（购物清单）",
    "📝 Prerequisites to Unlock Before Starting Medium": "开始Medium前的先决条件",
    "🎯 Medium Tier: First 5 Tasks to Tackle": "Medium级：前5个任务",
    "6. FAQ & Quick Reference Table": "6. 常见问题与快速参考表",
    
    # osrs-corrupted-gauntlet-guide-2026.html
    "1. How the Gauntlet Works": "1. Gauntlet运作方式",
    "2. Tier 1 Prep (Fast — Experienced)": "2. Tier 1准备（快速——适合老手）",
    "3. Tier 2 Prep (Safe — Beginners)": "3. Tier 2准备（安全——适合新手）",
    "4. Hunllef Boss Mechanics": "4. Hunllef Boss机制",
    "5. Tornado Survival Formula": "5. 龙卷风生存法则",
    "6. Profit & Drops": "6. 收益与掉落",
    "7. FAQ": "7. 常见问题",

    # osrs-curse-of-the-empty-lord-quest-2026.html
    "① 📖 Mini-Quest Overview & Requirements": "① 迷你任务概览与要求",
    "1.1 🔑 Requirements": "1.1 要求",
    "1.2 📋 Item Checklist": "1.2 物品清单",
    "1.3 ⏱️ Estimated Time": "1.3 预计时间",
    "② 🗡️ The Lore — Zaros, Zamorak & the Betrayal": "② 背景故事——Zaros、Zamorak与背叛",
    "2.1 🏛️ The Zarosian Empire": "2.1 Zaros帝国",
    "2.2 ⚔️ Zamorak's Rebellion": "2.2 Zamorak的叛乱",
    "2.3 🧟 Viggora's Curse": "2.3 Viggora的诅咒",
    "③ 🧭 Step-by-Step Walkthrough": "③ 分步通关攻略",
    "3.1 📌 Step 1 — Get a Ghostly Robes Piece": "3.1 第一步：获取一件幽灵长袍",
    "3.2 📌 Step 2 — Equip the Ring of Visibility": "3.2 第二步：装备可见之戒",
    "3.3 📌 Step 3 — Find and Talk to Viggora": "3.3 第三步：找到并与Viggora对话",
    "3.4 📌 Step 4 — Collect the Remaining Pieces (Optional)": "3.4 第四步：收集剩余部件（可选）",
    "④ 👻 Viggora NPC Locations (All Three)": "④ Viggora NPC位置（全部三处）",
    "4.1 🗡️ Edgeville Dungeon (Fastest Route)": "4.1 Edgeville地牢（最快路线）",
    "4.2 🏚️ Slayer Tower (Morytania Route)": "4.2 杀戮塔（Morytania路线）",
    "4.3 🏰 Rogues' Castle (Wilderness Route — Most Dangerous)": "4.3 盗贼城堡（荒野路线——最危险）",
    "4.4 📊 Which Location Should You Pick?": "4.4 应该选哪个位置？",
    "⑤ 🧥 Ghostly Robes — Full Set & Stats": "⑤ 幽灵长袍——全套与属性",
    "5.1 📊 Full Set Stats": "5.1 全套属性",
    "5.2 ✨ The Translucent Effect": "5.2 半透明效果",
    "5.3 🏆 Is It Worth Doing?": "5.3 值得做吗？",
    "⑥ 💡 Tips, Troubleshooting & Common Mistakes": "⑥ 技巧、故障排除与常见错误",
    "6.1 ❌ Common Mistakes": "6.1 常见错误",
    "6.2 🔧 Troubleshooting": "6.2 故障排除",
    "6.3 🎯 Speedrunning Tips": "6.3 速通技巧",
    "⑦ ❓ FAQs — Curse of the Empty Lord Mini-Quest": "⑦ 常见问题——空之诅咒迷你任务",

    # osrs-desert-treasure-quest-guide-low-level.html
    "1. Quest & Skill Requirements": "1. 任务与技能要求",
    "2. Pre-Quest Inventory & Gear Setup for Low Levels": "2. 低等级玩家的前置背包与装备配置",
    "3. Boss 1: Dessous the Vampire — Air Magic & Safe-Spot": "3. Boss 1：吸血鬼Dessous——风系魔法与安全点位",
    "4. Boss 2: Kamil the Ice Troll King — Stat Drain & Freeze": "4. Boss 2：冰巨魔之王Kamil——属性吸取与冰冻",
    "5. Boss 3: Fareed the Fire Warrior — Water Magic & Ice Gloves": "5. Boss 3：火焰战士Fareed——水系魔法与冰手套",
    "6. Boss 4: Damis the Shadow Hound — Prayer Drain Nightmare": "6. Boss 4：暗影猎犬Damis——祷告汲取噩梦",
    "7. Ancient Magicks Spellbook — What You Unlock": "7. 古代魔法书——解锁内容",
    "8. Common Mistakes That End Runs": "8. 导致失败的常见错误",
    "9. Frequently Asked Questions": "9. 常见问题",

    # osrs-chambers-of-xeric-loot-profit-guide.html
    "1. Entry Requirements & Recommended Stats（入场要求与推荐属性）": "1. 入场要求与推荐属性",
    "2. How the CoX Points & Loot System Works（CoX点数与战利品系统运作方式）": "2. CoX点数与战利品系统运作方式",
    "3. Unique Drop Table — All Items & Values（独特掉落表——所有物品与价值）": "3. 独特掉落表——所有物品与价值",
    "4. Common Loot — What You Get Every Raid（普通战利品——每次副本的收益）": "4. 普通战利品——每次副本的收益",
    "5. Profit Per Hour Analysis（每小时收益分析）": "5. 每小时收益分析",
    "6. CoX Profit Tips（CoX收益技巧）": "6. CoX收益技巧",
    "7. Frequently Asked Questions（常见问题）": "7. 常见问题",

    # osrs-diary-easy-medium-complete-guide-2026.html
    "1. Achievement Diaries Overview": "1. 成就日记概览",
    "All Regions & Diary Tiers": "全部区域与日记等级",
    "Rewards Structure": "奖励结构",
    "Should You Complete Easy Before Medium?": "应该先完成Easy再做Medium吗？",
    "2. Complete Easy Diaries Walkthrough (All Regions)": "2. 全区域Easy日记攻略",
    "🏠 Lumbridge & Draynor Easy Diary": "Lumbridge & Draynor Easy日记",
    "All Tasks & Solutions": "全部任务与解法",
    "Common Stuck Points & Solutions": "常见卡关点与解法",
    "Optimized Route (One Trip, No Backtracking)": "优化路线（一次性完成，无需折返）",
    "🏰 Varrock Easy Diary": "Varrock Easy日记",
    "Pro Tips for Varrock Easy": "Varrock Easy技巧",
    "🛡️ Falador Easy Diary": "Falador Easy日记",
    "⚔️ Wilderness Easy Diary": "荒野Easy日记",
    "Recommended Order (Minimize Risk)": "推荐顺序（最小化风险）",
    "🏔️ Kandarin Easy Diary": "Kandarin Easy日记",
    "Kandarin Easy Pro Route": "Kandarin Easy专业路线",
    "🏘️ Ardougne Easy Diary": "Ardougne Easy日记",
    "Reward Highlight": "奖励亮点",
    "🏜️ Desert Easy Diary": "沙漠Easy日记",
    "🗺️ Kourend & Kebos Easy Diary": "Kourend & Kebos Easy日记",
    "🌙 Morytania Easy Diary": "Morytania Easy日记",
    "🏹 Western Provinces Easy Diary": "Western Provinces Easy日记",
    "🌄 Varlamore Easy Diary (NEW 2024)": "Varlamore Easy日记（2024新区域）",
    "3. Complete Medium Diaries Walkthrough (All Regions)": "3. 全区域Medium日记攻略",
    "Medium Diary Completion Order (Recommended)": "Medium日记完成顺序（推荐）",
    "4. Essential Items Checklist": "4. 必备物品清单",
    "🎒 Teleportation Items (Bring These Always)": "传送物品（始终携带）",
    "🍖 Food & Consumables": "食物与消耗品",
    "🛠️ Tools & Equipment": "工具与装备",
    "💰 Budget Estimate (All Easy + Medium Diaries)": "预算估算（全部Easy+Medium日记）",
    "5. Time Management Strategy": "5. 时间管理策略",
    "📅 4-Week Completion Plan": "4周完成计划",
    "🎮 During-Gameplay Integration (The Lazy Way)": "游戏内整合（懒人法）",
    "⏰ Optimal Session Structure": "最佳游戏时段结构",
    "6. After E/M Diaries: Preparing for Hard": "6. 完成E/M日记后：为Hard做准备",
    "🎯 Preparing for Hard Diaries": "准备Hard日记",
    "🏆 Which Hard Diaries to Prioritize First": "优先做哪些Hard日记",
    "📊 Account Power Check (After E/M Diaries)": "账号实力检查（完成E/M日记后）",
    "7. FAQ & Troubleshooting": "7. 常见问题与故障排除",

    # osrs-diary-priority-order-beginner-2026.html
    "🎯 Why Achievement Diaries Matter for New Players": "成就日记对新玩家的价值",
    "📋 The 10 Best Diaries for Beginners (Ranked)": "最适合新手的10个日记（排名）",
    "🥇 #1: Lumbridge & Draynor Diary — Explorer's Ring": "第1名：Lumbridge & Draynor日记——探险家之戒",
    "🥈 #2: Ardougne Diary — Ardougne Cloak": "第2名：Ardougne日记——Ardougne斗篷",
    "🥉 #3: Varrock Diary — Varrock Armor": "第3名：Varrock日记——Varrock盔甲",
    "#4: Falador Diary — Falador Shield": "第4名：Falador日记——Falador盾牌",
    "#5: Kandarin Diary — Kandarin Headgear": "第5名：Kandarin日记——Kandarin头饰",
    "#6: Desert Diary — Desert Amulet": "第6名：沙漠日记——沙漠护身符",
    "#7: Morytania Diary — Morytania Legs": "第7名：Morytania日记——Morytania护腿",
    "#8: Wilderness Diary — Wilderness Sword": "第8名：荒野日记——荒野之剑",
    "#9: Kourend & Kebos Diary — Kourend Headgear": "第9名：Kourend & Kebos日记——Kourend头饰",
    "#10: Western Provinces Diary — Western Banner": "第10名：Western Provinces日记——Western旗帜",
    "📊 Quick Comparison Table": "快速对比表",
    "⚠️ Which Diaries to Skip (For Now)": "应跳过（暂时）的日记",
    "🏆 Your Diary Priority Roadmap": "你的日记优先级路线图",
}

# ===== 添加中文标题和导语 =====
def add_chinese_header(content, filename):
    """在guide-hero区添加中文H1和导语"""
    cn = DATA[filename]
    cn_h1 = cn["cn_title"]
    cn_summary = cn["cn_summary"]
    
    # 在 <h1> 标签前添加中文H1
    # 注意：有些文件已经有中文H1（如chambers-of-xeric），需要判断
    h1_pattern = r'(<h1[^>]*>)'
    
    # 在英文H1前添加中文H1
    cn_h1_html = f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_h1}</h1>\n            '
    
    # 在英文H1之后、subtitle之后添加中文导语
    # 找到subtitle后的第一个</div>（guide-hero container的结束）
    
    # 策略：在英文H1后添加中文H1（如果还没有的话）
    if 'class="cn-title"' not in content:
        content = re.sub(
            r'(<h1[^>]*>.*?</h1>)',
            cn_h1_html + r'\1',
            content,
            count=1
        )
    
    # 添加中文导语 - 在subtitle后面
    cn_summary_html = f'\n            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>'
    
    if 'class="cn-summary"' not in content:
        content = re.sub(
            r'(<p class="subtitle">.*?</p>)',
            r'\1' + cn_summary_html,
            content,
            count=1
        )
    
    return content

# ===== 给H2/H3加中文翻译 =====
def add_h2_h3_translations(content):
    """给所有H2和H3标签添加中文翻译"""
    
    def translate_h(match):
        tag = match.group(1)  # h2 or h3
        attrs = match.group(2) or ''
        text = match.group(3)
        
        # 不处理已有中文翻译的标题（包含中文括号的）
        if '（' in text or '\u3000' in text or 'chinese' in attrs.lower():
            return match.group(0)
        
        # 检查翻译字典
        if text in H2_H3_TRANSLATIONS:
            cn = H2_H3_TRANSLATIONS[text]
            return f'<{tag}{attrs}>{text}（{cn}）</{tag}>'
        
        return match.group(0)
    
    # 匹配 <h2>...</h2> 或 <h3>...</h3>，考虑属性
    content = re.sub(
        r'<(h[23])([^>]*)>(.*?)</\1>',
        translate_h,
        content
    )
    
    return content

# ===== 处理所有文件 =====
def process_all():
    os.makedirs(OUT, exist_ok=True)
    for filename, cn_data in DATA.items():
        filepath = os.path.join(BASE, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. 添加中文标题和导语
        content = add_chinese_header(content, filename)
        
        # 2. 添加H2/H3中文翻译
        content = add_h2_h3_translations(content)
        
        if content != original:
            outpath = os.path.join(OUT, filename)
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] {filename} -> {outpath}")
        else:
            print(f"[SKIP] {filename}")
    
    print("All files processed!")

if __name__ == "__main__":
    process_all()
