#!/usr/bin/env python3
"""
Group 1: Money Article Translation Team
Processes 15 articles by:
1. Reading English content
2. Copying FULL English content to zh/guides/
3. Adding Chinese bilingual annotations (hero, TOC, h2, h3)
"""

import re
import os

BASE_DIR = "c:/Users/Lenovo/osrs-guide-site"
EN_DIR = os.path.join(BASE_DIR, "guides")
ZH_DIR = os.path.join(BASE_DIR, "_temp_zh")
# Note: After script runs, files in _temp_zh will be copied to zh/guides/

FILES = [
    "mid-game-money-making-2026.html",
    "osrs-afk-money-making-methods-2026.html",
    "osrs-afk-money-making-ultimate-guide-2026.html",
    "osrs-best-money-making-methods-2026.html",
    "osrs-bond-farming-free-membership-2026.html",
    "osrs-bond-farming-strategy-2026.html",
    "osrs-cheap-flipping-methods-new-players.html",
    "osrs-combat-money-making-non-boss-2026.html",
    "osrs-daily-weekly-money-routine-2026.html",
    "osrs-f2p-ironman-money-making-early-game.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-money-making-ranked-2026.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
]

# ========== COMPREHENSIVE TRANSLATION DICTIONARY ==========
T = {
    # Bare TOC variants (without numbers/question marks)
    "What Is Mid-Game Money Making": "什么是中期赚钱",
    "Barrows Runs (1.8M-1M/hr)": "Barrows地穴（80万-150万GP/小时）",
    "Zulrah (1M-2M/hr)": "Zulrah（100万-200万GP/小时）",
    "Vorkath (2M-3M/hr)": "Vorkath（200万-300万GP/小时）",
    "Slayer Profit (1.8M-3M/hr)": "杀戮任务收益（80万-300万GP/小时）",
    "Herb Runs (100K-1.8M per run)": "草药跑商（每次10万-180万GP）",
    "Birdhouse Runs (30K-50K per run)": "鸟窝陷阱（每次3万-5万GP）",
    "Flipping & Merchanting (1M-5M/hr)": "倒卖与贸易（100万-500万GP/小时）",
    "Passive Income Methods": "被动收入方法",
    "1M to 100M Roadmap": "100万到1亿路线图",
    "What Is Mid-Game Money Making?": "什么是中期赚钱",
    "Barrows Runs — 1.8M-1M GP/hr": "Barrows地穴 — 80万-150万GP/小时",
    "Zulrah — 1M-2M GP/hr": "Zulrah — 100万-200万GP/小时",
    "Vorkath — 2M-3M GP/hr": "Vorkath — 200万-300万GP/小时",
    "Slayer Profit — 1.8M-3M GP/hr": "杀戮任务收益 — 80万-300万GP/小时",
    "Herb Runs — 100K-1.8M Profit Per Run (5 min)": "草药跑商 — 每次10万-180万GP（5分钟）",
    "Birdhouse Runs — 30K-50K Per Run (2 min)": "鸟窝陷阱 — 每次3万-5万GP（2分钟）",
    "Flipping & Merchanting — 1M-5M GP/hr": "倒卖与贸易 — 100万-500万GP/小时",
    "Passive Income Methods — Earn GP While Doing Other Things": "被动收入方法 — 边做其他事边赚钱",
    "All Methods Profit Comparison": "所有方法收益对比",
    "1M to 100M Roadmap — Step by Step": "100万到1亿路线图 — 逐步指南",
    "Final Tips — Maximising Your Mid-Game Wealth": "最终建议 — 最大化中期财富",
    "FAQ": "常见问题",
    "Mid-Game Account Benchmarks": "中期账号基准",
    "Requirements": "要求",
    "Gear Setup (Budget: ~2M GP)": "装备配置（预算约200万GP）",
    "Profit Breakdown": "收益分析",
    "How to Learn Zulrah": "如何学习Zulrah",
    "Gear Setup (Budget: ~12M GP)": "装备配置（预算约1200万GP）",
    "Budget vs Premium Setup": "预算与顶级配置对比",
    "Best Mid-Game Slayer Profit Tasks": "最佳中期杀戮任务",
    "Best Herbs by Farming Level": "按种植等级推荐最佳草药",
    "Optimal Herb Run Setup": "最佳草药跑商配置",
    "Birdhouse Profit Per Level": "鸟窝陷阱每级收益",
    "Flipping Strategy by Bank Size": "按银行规模定制的倒卖策略",
    "Flipping Rules for Beginners": "新手倒卖规则",
    "All Passive Income Sources": "所有被动收入来源",
    "Phase 1: 1M to 10M (The Foundation)": "第一阶段：100万到1000万（基础）",
    "Phase 2: 10M to 50M (Scaling Up)": "第二阶段：1000万到5000万（扩大）",
    "Phase 3: 50M to 100M (The Push)": "第三阶段：5000万到1亿（冲刺）",
    "Q: What's the fastest way to 10M from scratch?": "问：从零到1000万最快的方法是什么？",
    "Q: Vorkath or Zulrah — which should I learn first?": "问：Vorkath还是Zulrah——应该先学哪个？",
    "Q: When should I stop herb runs?": "问：什么时候可以停止草药跑商？",
    "Q: Is flipping worth learning if I only have 5M?": "问：只有500万GP值得学倒卖吗？",
    "Q: How much GP do I need before starting Vorkath/Zulrah?": "问：开始打Vorkath/Zulrah需要多少GP？",

    # ==== AFK Money Making Methods ====
    "What Is AFK Money Making in OSRS?": "什么是OSRS挂机赚钱",
    "AFK Skilling Methods": "挂机技能赚钱法",
    "AFK Combat Methods": "挂机战斗赚钱法",
    "AFK Bossing Methods": "挂机Boss赚钱法",
    "Semi-AFK Methods": "半挂机赚钱法",
    "GP/Hour Comparison Table": "GP/小时对比表",
    "Requirements &amp; Unlock Table": "要求与解锁表",
    "Final Tips — Maximising Your AFK Money Making": "挂机赚钱最终建议",
    "AFK Money Making FAQs": "挂机赚钱常见问题",
    "Table of Contents": "目录",
    "&#9312; Table of Contents": "目录",
    "① Table of Contents": "目录",
    "📋 Table of Contents": "目录",
    "&#127907; Fishing (AFK Level: High)": "钓鱼（挂机等级：高）",
    "&#127811; Woodcutting (AFK Level: High)": "砍树（挂机等级：高）",
    "&#9871; Mining (AFK Level: High)": "挖矿（挂机等级：高）",
    "&#128302; Magic (AFK Level: Medium-High)": "魔法（挂机等级：中高）",
    "&#9876; Nightmare Zone (400-1.8M GP/hr)": "梦魇空间（40万-180万GP/小时）",
    "&#127754; Sand Crabs / Ammonite Crabs (50-100K GP/hr)": "沙蟹/菊石蟹（5万-10万GP/小时）",
    "&#128293; Soul Wars (400-1.8M GP/hr)": "灵魂战争（40万-180万GP/小时）",

    # ==== AFK Money Making Ultimate Guide ====
    "🎯 What Makes a Method \"AFK\" — 3 Tiers": "什么构成挂机方法——三级分类",
    "✅ True AFK Methods (2+ Min Clicks)": "真挂机方法（2分钟以上点击间隔）",
    "🔄 Semi-AFK Methods (30s-2min)": "半挂机方法（30秒-2分钟）",
    "📋 Low-Attention Methods (10-30s)": "低注意力方法（10-30秒）",
    "⚔️ Combat AFK Money (1.8M-2M/hr)": "战斗挂机赚钱（180万-200万/小时）",
    "📊 GP/hr vs Attention Score Matrix": "GP/小时与注意力评分矩阵",
    "🛠️ Best AFK Setup for Work/Study": "工作/学习最佳挂机方案",
    "❓ FAQ + AFK Daily Routine": "常见问题与挂机日常",
    "📊 How This Guide Ranks Methods": "本指南如何排名方法",
    "1️⃣ Ammonite Crabs (0-50K/hr)": "菊石蟹（0-5万/小时）",
    "2️⃣ Sand Crabs (0-30K/hr)": "沙蟹（0-3万/小时）",
    "3️⃣ Fishing Trawler (100K-1.8M/hr)": "钓鱼拖网（10万-180万/小时）",
    "4️⃣ Fishing Karambwans (150K-1.8M/hr)": "钓Karambwan（15万-180万/小时）",
    "5️⃣ Redwood Trees (70K-100K/hr)": "红木树（7万-10万/小时）",
    "6️⃣ Star Mining (100K-1.8M/hr)": "星矿开采（10万-180万/小时）",
    "7️⃣ Anglerfish (1.8M-1.8M/hr)": "钓Anglerfish（180万/小时）",
    "8️⃣ Seaweed Spawning (Passive)": "海藻养殖（被动收入）",
    "1️⃣ MLM (100K-1.8M/hr)": "母矿脉（10万-180万/小时）",
    "2️⃣ Cooking (100K-1.8M/hr)": "烹饪（10万-180万/小时）",
    "3️⃣ Cannonballs (60K-90K/hr)": "炮弹铸造（6万-9万/小时）",
    "4️⃣ Plank Make (100K-1.8M/hr)": "木板制作（10万-180万/小时）",
    "5️⃣ Fletching (100K-1.8M/hr)": "制箭（10万-180万/小时）",
    "🍷 Winemaker (100K-350K/hr)": "酿酒（10万-35万/小时）",
    "1️⃣ Blast Furnace (1.8M-2.5M/hr)": "高炉（180万-250万/小时）",
    "Herb Runs (Farming 32+)": "草药跑商（种植32级以上）",
    "Birdhouse Runs (Hunter 5+)": "鸟窝陷阱（猎人5级以上）",
    "Herbiboar (Hunter 80+ / 31+ Recommended)": "Herbiboar（猎人80+/推荐31+）",
    "Giants' Foundry (Smithing 60+ / 80+ Recommended)": "巨人铸造（锻造60+/推荐80+）",
    "🏠 Gargoyles (1.8M-1.8M/hr)": "石像鬼（180万/小时）",
    "Vyrewatch Sentinels (Combat 75+ / 50 Prayer)": "Vyrewatch哨兵（战斗75+/50祈祷）",
    "🦎 Rune Dragons (1.8M-700K/hr)": "符文龙（180万-70万/小时）",
    "Brutal Black Dragons (Combat 80+ / 70 Prayer)": "残忍黑龙（战斗80+/70祈祷）",
    "Nightmare Zone (NMZ) (Combat 60+ / 43+ Prayer)": "梦魇空间（战斗60+/43+祈祷）",
    "🛠️ Hardware Setup": "硬件设置",
    "RuneLite Plugins for AFK Play": "挂机用RuneLite插件",
    "Mobile AFK Tips": "手机版挂机技巧",
    "Work/Study Schedule Integration": "工作/学习安排整合",
    "Frequently Asked Questions": "常见问题",
    "Sample AFK Daily Routine (No Stats Required Start)": "挂机日常示例（零属性起步）",
    "⚡ Quick-Jump Table of Contents": "快速跳转目录",
    "📋 Step-by-Step: The 15-Minute Daily Routine": "逐步指南：15分钟日常流程",

    # ==== Best Money Making Methods 2026 ====
    "① 📊 Methodology — How We Analyzed the Data": "研究方法论",
    "② 🏆 Top 10 Money Making Methods (Overall)": "十大赚钱方法总排名",
    "③ 💎 High-Level Methods (90+ Stats)": "高级玩家赚钱法",
    "④ 🔶 Mid-Level Methods (70-90 Stats)": "中级玩家赚钱法",
    "⑤ 🔷 Low-Level Methods (Below 70 Stats)": "低级玩家赚钱法",
    "⑥ 🆓 F2P Methods (No Membership Required)": "免费玩家赚钱法",
    "⑦ 📈 Deep Analysis — Trends & Surprises": "深度分析与趋势",
    "⑧ ❓ FAQ — Money Making Rankings 2026": "常见问题",
    "⑨ 💡 Final Tips & Next Steps": "最终建议",
    "1.1 📋 Data Sources": "数据来源",
    "1.2 ⚖️ How We Calculated GP/Hour": "GP/小时计算方式",
    "1.3 🎯 Ranking Criteria": "排名标准",
    "2.1 🥇 #1: Chambers of Xeric (Solo Speed)": "#1：Xeric密室（单人速刷）",
    "2.2 🥈 #2: Zulrah (Phase-Switching Mastery)": "#2：Zulrah（相位切换大师）",
    "2.3 🥉 #3: Vorkath (Post-Quest Unlock)": "#3：Vorkath（任务解锁）",
    "2.4 #4: Gauntlet (Corrupted)": "#4：Gauntlet（腐化模式）",
    "2.5 #5: Nightmare (Group)": "#5：噩梦（组队）",
    "2.6 #6: Herbiboar (Collection Log)": "#6：Herbiboar（收集日志）",
    "2.7 #7: Slayer (High-Level Tasks)": "#7：杀戮任务（高级任务）",
    "2.9 #9: Farming (Ranarr + Snapdragon)": "#9：种植（Ranarr+Snapdragon）",
    "2.10 #10: Blas Furnace (BF) Gold Smelting": "#10：高炉炼金",
    "3.1 🔥 Chambers of Xeric (CoX) — Deep Dive": "Xeric密室深度解析",
    "3.2 🐉 Zulrah — Phase-Switching Strategy": "Zulrah相位切换策略",
    "3.3 🐲 Vorkath — The Consistent Giant": "Vorkath——稳定的收益巨人",
    "4.1 🌋 Cerberus (Hellhound)": "Cerberus（地狱犬）",
    "4.2 🏹 Grotesque Guardians (Dusk/ Dawn)": "Grotesque Guardians（黄昏/黎明）",
    "4.3 🗡️ Slayer (Mid-Level Tasks)": "杀戮任务（中级任务）",
    "5.1 🌾 Farming (Herb Runs)": "种植（草药跑商）",
    "5.2 ⛏️ Mining (Iron + Coal)": "挖矿（铁+煤）",
    "5.3 🐟 Fishing (Lobsters + Swordfish)": "钓鱼（龙虾+剑鱼）",
    "6.1 🐄 Cowhide Collection (Alchery)": "收集牛皮（高附魔）",
    "6.2 ⛏️ Essence Mining (Rune Essence)": "符文矿石开采",
    "6.3 🗡️ F2P Bossing (Obor + Bryophyta)": "免费Boss战斗",
    "7.1 📉 The \"Bond Inflation\" Effect": "债券通胀效应",
    "7.2 🔄 The \"Meta Shift\" — Ranged> Melee": "Meta转变——远程>近战",
    "7.3 💡 The \"Collection Log\" Boost": "收集日志加成",
    "7.4 🌐 The \"Wilderness Risky\" Premium": "荒野风险溢价",
    "8.1 📋 How accurate is this data?": "数据准确性如何",
    "8.2 💰 What's the fastest way to get 10M GP for a bond?": "快速赚1000万买债券的最佳方法",
    "8.3 🔄 How often should I update my money making method?": "多久更新一次赚钱方法",
    "8.4 📊 Can I trust the Reddit poll data?": "Reddit投票数据可信吗",
    "9.1 🎯 Pick the Right Method for YOUR Account": "选择适合你账号的方法",
    "9.2 📈 Track Your Own Profit": "追踪自己的收益",
    "9.3 🔗 Related Guides (Start Your Journey)": "相关攻略（开始你的旅程）",

    # ==== Bond Farming Free Membership ====
    "① 🎟️ What Are Bonds &amp; How Do They Work?": "什么是债券及其运作方式",
    "② 💰 F2P Money Making for Your First Bond": "免费玩家赚取第一个债券",
    "③ ⚡ Early Member Methods — Quick Payback": "早期会员方法——快速回本",
    "④ 🔄 Sustained Bond Income — Long-Term Methods": "可持续债券收入——长期方法",
    "⑤ ⏳ Time vs Money Analysis — Is Grinding Worth It?": "时间与金钱分析——刷值得吗",
    "⑥ 🛡️ Risk Management — Market Fluctuations": "风险管理——市场波动",
    "⑦ ❓ FAQs — Bond Farming &amp; Free Membership": "债券养殖常见问题",
    "1.1 📜 Bond Basics — Tradeable vs Untradeable": "债券基础——可交易与不可交易",
    "1.2 💰 What a Bond Actually Gives You": "债券实际能给你什么",
    "1.3 🔄 The Bond Lifecycle for a Farmer": "债券养殖生命周期",
    "2.1 🧑‍🌾 Best Zero-Requirement F2P Methods": "最佳零要求免费方法",
    "2.2 🏹 Combat-Based F2P Money Makers": "基于战斗的免费赚钱方法",
    "2.3 🎯 High-Level F2P: Your Pre-Bond Power Grind": "高级免费：债券前的强力刷级",
    "2.4 📈 The F2P Bond Timeline — Realistic Expectations": "免费债券时间线——现实预期",
    "3.1 🌿 Wintertodt — The Beginner Goldmine": "Wintertodt——新手金矿",
    "3.2 🦀 Sand Crabs + Herb Drops (Combat + GP)": "沙蟹+草药掉落（战斗+GP）",
    "3.3 🐉 Green Dragons — The Classic Bond Farmer": "绿龙——经典债券养殖",
    "3.4 📜 Chaos Altar Prayer Training (Save GP)": "混沌祭坛祈祷训练（省GP）",
    "3.5 🕒 The 14-Day Bond Recovery Plan": "14天债券回收计划",
    "4.1 🐍 Zulrah — The Bond Farmer's Best Friend": "Zulrah——债券养殖者最好的朋友",
    "4.2 🐉 Vorkath — High-Value Solo Boss": "Vorkath——高价值单人Boss",
    "4.3 🏰 Barrows — Low-Requirement Consistent GP": "Barrows——低要求稳定GP",
    "4.4 🧹 Slayer — The Passive Income Engine": "杀戮任务——被动收入引擎",
    "4.5 🌾 Farming Runs — Passive GP Between Sessions": "种植跑商——游戏间隙的被动GP",
    "5.1 📊 The Real Cost of Bond Farming": "债券养殖的真实成本",
    "5.2 🧠 When Bond Farming Makes Sense": "何时债券养殖有意义",
    "5.3 💡 When Paying Real Money Makes More Sense": "何时付真钱更划算",
    "6.1 📈 Why Bond Prices Fluctuate": "债券价格为何波动",
    "6.2 🛡️ How to Protect Yourself from Price Spikes": "如何保护自己免受价格飙升影响",
    "6.3 ⚠️ Account Security — Protect Your Bond Investment": "账号安全——保护债券投资",
    "🚀 New to Membership? Read the First-10-Things Guide": "新手会员？先读十件事指南",
    "🐍 Want to Fund Bonds with Zulrah?": "想用Zulrah养债券吗",

    # ==== Bond Farming Strategy ====
    "1. The Bond Math: What You Need Every 14 Days": "债券数学：每14天需要多少",
    "2. Before Your First Bond: F2P Preparation": "第一个债券前的免费准备",
    "3. First 14 Days: Building Your Bond Engine": "前14天：建立债券引擎",
    "4. The Sustainable Daily Routine": "可持续的日常流程",
    "5. Passive Income Setup: Minimal Effort, Maximum GP": "被动收入设置：最小努力最大GP",
    "6. Mid-Game Bond Strategy: Boss-First Approach": "中期债券策略：Boss优先",
    "7. Endgame Bond Strategy: Effortless Bonding": "终局债券策略：轻松养债券",
    "8. Bond Price Strategy: Buy Low, Bond Smart": "债券价格策略：低买高卖",
    "9. Bond Farming FAQs": "债券养殖常见问题",
    "📋 Table of Contents": "目录",
    "① F2P Goals (1-2 weeks)": "免费目标（1-2周）",
    "② Buy the Bond... But Strategically": "购买债券...但要有策略",
    "① Week 1: The Foundation (Days 1-7)": "第一周：基础（第1-7天）",
    "② Week 2: Scaling Up (Days 8-14)": "第二周：扩大（第8-14天）",
    "① Daily Passive Routine (15-20 min total)": "每日被动流程（共15-20分钟）",
    "② Daily Active Session (1-1.5 hours)": "每日活跃时段（1-1.5小时）",
    "① Mid-Game Bond Math (Base 70s combat, 30-50M bank)": "中期债券数学（基础70级战斗，3000-5000万银行）",
    "② The 20-Minute Bond (12.6M Edition)": "20分钟债券（1260万版）",
    "① Endgame Bond Funnel": "终局债券漏斗",
    "② The Bond is No Longer Your Concern": "债券不再是你的担忧",
    "① Bond Price Patterns (2024-2026 Data, Source: Jagex Official GE)": "债券价格模式（2024-2026数据）",
    "② The Bond Stockpile Strategy (12.6M Edition)": "债券储备策略（1260万版）",
    "🎯 Bond Farming Action Plan Summary (12.6M Edition)": "债券养殖行动计划总结（1260万版）",

    # ==== Cheap Flipping Methods ====
    "1. Why Flipping Works for New Players": "为什么倒卖适合新手",
    "2. Getting Started — The Margin Check Process": "入门——差价检查流程",
    "3. Best Budget Flip Items Under 100K": "最佳10万以下预算倒卖物品",
    "4. Cannonball Flipping Deep Dive": "炮弹倒卖深度分析",
    "5. Nature Rune Flipping Strategy": "自然符文倒卖策略",
    "6. Advanced Flipping Tips": "高级倒卖技巧",
    "7. Common Flipping Mistakes": "常见倒卖错误",
    "8. Frequently Asked Questions": "常见问题",

    # ==== Combat Money Making Non-Boss ====
    "The Consistency Advantage": "稳定性的优势",
    "Slayer as a Wealth Engine": "杀戮任务作为财富引擎",
    "Why Green Dragons Work": "为什么绿龙可行",
    "Best Locations and Safe Spots": "最佳位置和安全点",
    "Gear Setup (Budget, 60+ Combat)": "装备配置（预算，60+战斗）",
    "PK Escape Routes": "PK逃生路线",
    "Taverley Dungeon Route": "Taverley地牢路线",
    "Banking Strategy": "银行策略",
    "Blue Dragon Gear Setup": "蓝龙装备配置",
    "The Blowpipe Setup (Optimal for GP/hr)": "吹管配置（GP/小时最优）",
    "Inventory and Strategy": "背包与策略",
    "The Auto-Smash Perk": "自动粉碎特权",
    "Guthans Strategy — Infinite Trips": "Guthans策略——无限续航",
    "Maximum DPS Setup (700K-1.8M GP/hr)": "最大DPS配置（70万-180万GP/小时）",
    "Gear Progression for Rune Dragons": "符文龙的装备进阶",
    "Kill Strategy": "击杀策略",
    "The Blood Shard — The Real Prize": "血碎片——真正的奖品",
    "Prayer Gear Setup": "祈祷装备配置",
    "Banking and Sustain Strategy": "银行与续航策略",
    "Skeletal Wyverns (72 Slayer, 1.5M-2M GP/hr)": "骷髅飞龙（72杀戮，150万-200万GP/小时）",
    "Kurasks (70 Slayer, 350K-1.8M GP/hr)": "Kurask（70杀戮，35万-180万GP/小时）",
    "Dust Devils (65 Slayer, 1.8M-450K GP/hr)": "沙尘恶魔（65杀戮，180万-45万GP/小时）",
    "Aberrant Spectres (60 Slayer, 350K-1.8M GP/hr)": "变异幽灵（60杀戮，35万-180万GP/小时）",
    "Fire Giants (Combat Level 86, 1.8M-350K GP/hr)": "火焰巨人（战斗等级86，180万-35万GP/小时）",
    "Fossil Island Wyverns (66 Slayer, 1.8M-1.5M GP/hr)": "化石岛飞龙（66杀戮，180万-150万GP/小时）",
    "Abyssal Demons (85 Slayer, 1.8M-700K GP/hr)": "深渊恶魔（85杀戮，180万-70万GP/小时）",
    "Non-Boss Monster Comparison Table (2026)": "非Boss怪物对比表（2026）",
    "Monster Progression Ladder — What to Kill at Each Combat Level": "怪物进阶阶梯——各战斗等级该杀什么",
    "FAQ": "常见问题",
    "Q: What's the best non-boss monster for a brand new account?": "问：全新账号最佳非Boss怪物是什么",
    "Q: Melee, Ranged, or Magic for non-boss money making?": "问：非Boss赚钱用近战、远程还是魔法",
    "Q: What monsters drop the most alchable items?": "问：哪些怪物掉落最多可附魔物品",
    "Q: Are non-boss money-makers viable for Ironman accounts?": "问：非Boss赚钱法对铁人账号可行吗",
    "Q: How do I fund gear upgrades while grinding monsters?": "问：刷怪时如何为装备升级筹资",
    "Q: What if I can't complete Dragon Slayer II for Rune Dragons?": "问：完不成屠龙者II怎么办",

    # ==== Daily Weekly Money Routine ====
    "🎯 Why Dailies Pay: 47M-129M GP/Month": "为什么日常任务赚钱：每月4700万-1.29亿GP",
    "⏱️ 15-Min Daily Routine: 2.5M GP/day": "15分钟日常：每天250万GP",
    "🌿 Herb Run Mastery: 1.8M/run (Best Herbs + Routes)": "草药跑商精通：每次180万GP（最佳草药+路线）",
    "🐦 Birdhouse Runs: 120K/run (Mechanics + Profit)": "鸟窝陷阱：每次12万GP（机制+收益）",
    "👑 Managing Miscellania: 425K/day (Kingdom Setup)": "管理Miscellania：每天42.5万GP（王国设置）",
    "📅 Weekly Tasks: 1.6M/week (Tears, Circus, Penguins)": "每周任务：每周160万GP（眼泪、马戏团、企鹅）",
    "📊 Complete Schedule: 129M/month (Daily + Weekly)": "完整计划：每月1.29亿GP（每日+每周）",
    "❓ FAQ + Seasonal Opportunities (Monthly Tips)": "常见问题+季节性机会（月度技巧）",
    "📊 The Math of Daily Routines": "日常流程的数学计算",
    "🗺️ Optimizing the Herb Run Route": "优化草药跑商路线",
    "🌱 Best Herbs to Plant (by Farming Level)": "最佳种植草药（按种植等级）",
    "🛡️ Disease Protection — To Pay or Not to Pay?": "疾病防护——付还是不付",
    "💰 Farmer Payment Costs (for high-value herbs)": "农夫支付成本（高价值草药）",
    "🔧 How Birdhouse Runs Work": "鸟窝陷阱如何运作",
    "📊 Birdhouse Profit by Hunter Level": "按猎人等级计算的鸟窝收益",
    "⚡ Optimizing Birdhouse Runs": "优化鸟窝跑商",
    "🔧 How Kingdom Management Works": "王国管理如何运作",
    "👥 Optimal Worker Allocation for Maximum GP": "最佳工人分配以最大化GP",
    "📊 Kingdom Profit Calculation": "王国收益计算",
    "💧 Tears of Guthix (Weekly)": "Guthix之泪（每周）",
    "🎪 The Circus (Weekly)": "马戏团（每周）",
    "🐧 Penguin Hide and Seek (Weekly)": "企鹅捉迷藏（每周）",
    "📜 Clue Scroll Stacking (Weekly/Monthly)": "线索卷轴堆积（每周/每月）",
    "📊 Weekly D&D Summary": "每周D&D总结",
    "📅 Daily Schedule (Repeat Every Day)": "每日计划（每天重复）",
    "📅 Weekly Schedule (Add to Daily Routine)": "每周计划（添加到日常）",
    "📊 Putting It All Together — Monthly Profit Estimate": "汇总——月度收益预估",
    "❓ Frequently Asked Questions": "常见问题",
    "💡 Monthly Money Opportunities (Lesser-Known Methods)": "月度赚钱机会（不太知名的方法）",

    # ==== F2P Ironman Money Making ====
    "1. The F2P Ironman Challenge": "免费铁人的挑战",
    "2. Cowhide Processing — The Best Starting Method": "牛皮处理——最佳起步方法",
    "3. Crafting Progression & Alch Values": "工艺进阶与附魔价值",
    "4. Jewelry Crafting for Profit (Level 40+)": "珠宝制作赚钱（40级以上）",
    "5. Rune Essence Mining & Runecrafting": "符文矿石开采与符文制作",
    "6. High Alchemy — The Ironman Endgame": "高附魔——铁人终局",
    "7. Advanced Tips for F2P Ironmen": "免费铁人高级技巧",
    "8. Common Mistakes": "常见错误",
    "9. Frequently Asked Questions": "常见问题",

    # ==== F2P Money Making First Bond ====
    "1. 💰 Why You Need 10M GP for Your First Bond": "为什么需要1000万GP买第一个债券",
    "2. 🥇 Best F2P Method: Cowhides (1.8M-1.8M GP/hr)": "最佳免费方法：牛皮（180万GP/小时）",
    "3. 🪨 Second Best: Essence Mining (1.8M-1.8M GP/hr)": "第二佳：符文矿石开采（180万GP/小时）",
    "4. 🐟 Fishing & Cooking Combo (1.8M-1.5M GP/hr)": "钓鱼与烹饪组合（180万-150万GP/小时）",
    "5. 🗡️ Hill Giants Loot Run (1.5M-2M GP/hr)": "山丘巨人战利品跑（150万-200万GP/小时）",
    "6. ⏱️ Realistic Timeline: How Long to Your First Bond": "现实时间线：多久能赚到第一个债券",
    "7. 💡 Pro Tips to Speed Up Bond Farming": "加速债券养殖的专业技巧",
    "8. ❓ FAQs — F2P Money Making for Your First Bond": "免费玩家赚第一个债券常见问题",
    "1.1 Bond Price History (2026 Edition)": "债券价格历史（2026版）",
    "1.2 GP/USD Ratio Trend — Why Bonds Keep Getting More Expensive": "GP/美元比例趋势——债券为何越来越贵",
    "2.1 Location: Lumbridge East Cow Field": "位置：Lumbridge东侧牛场",
    "2.2 Gear Setup (No Membership Needed)": "装备配置（无需会员）",
    "2.3 Banking Route & Efficiency Tips": "银行路线与效率技巧",
    "2.4 Realistic GP/Hr Breakdown": "现实GP/小时分析",
    "3.1 Varrock East Mine vs Draynor Village": "Varrock东矿 vs Draynor村",
    "3.2 Runecrafting for Extra Profit (If You Have 1+ RC)": "符文制作赚外快（如有1+符文制作）",
    "3.3 GP/Hr Breakdown — Essence Mining": "GP/小时分析——符文矿石开采",
    "4.1 Best F2P Fishing Spots (2026)": "最佳免费钓鱼点（2026）",
    "4.2 Food Value for Members Later": "食物价值（日后会员使用）",
    "5.1 Edgeville Dungeon Route": "Edgeville地牢路线",
    "5.2 Hill Giants Loot Table Breakdown": "山丘巨人战利品表分析",
    "5.3 Time to 10M GP — Hill Giants Route": "到1000万GP的时间——山丘巨人路线",
    "6.1 2-Week Plan (1 Hour/Day)": "两周计划（每天1小时）",
    "6.2 1-Week Plan (3 Hours/Day)": "一周计划（每天3小时）",
    "6.3 Ultra-Fast Plan (Hardcore Grind — 5 Days)": "超快计划（硬核刷——5天）",
    "7.1 Use Yak Track Rewards (Free GP)": "使用Yak Track奖励（免费GP）",
    "7.2 Daily Challenges for Extra XP (and GP)": "每日挑战赚额外经验（和GP）",
    "7.3 Don't Waste GP on \"Upgrade\" Gear": '不要把GP浪费在「升级」装备上',
    "7.4 Use the Grand Exchange Smartly": "明智使用交易所",
    "🚀 Ready to Make Bank as a Member?": "准备好成为会员赚钱了吗",

    # ==== F2P Money Making No Stats ====
    "1. Method: Collecting Cowhides + Bones (Lumbridge)": "方法：收集牛皮+骨头（Lumbridge）",
    "2. Method: Mining Rune Essence": "方法：开采符文矿石",
    "3. Method: Picking Up Loot at the Wilderness Ditch": "方法：在荒野沟渠捡拾战利品",
    "4. Method: Picking Bananas at Musa Point (Karamja)": "方法：在Musa点摘香蕉（Karamja）",
    "5. Method: Bone Yard Collecting (Wilderness)": "方法：骨场收集（荒野）",
    "6. Method: Enchanting Sapphire Rings (Semi-AFK Magic Profit)": "方法：附魔蓝宝石戒指（半挂机魔法收益）",
    "7. Method: Buying from Shops and Selling on GE (Arbitrage)": "方法：从商店买入在交易所卖出（套利）",
    "8. Common F2P Money Making Mistakes": "常见免费赚钱错误",
    "9. Frequently Asked Questions": "常见问题",

    # ==== F2P Money Making Ranked ====
    "① 🏆 Top 5 F2P Money Makers (Ranked by GP/Hour)": "前5名免费赚钱方法（按GP/小时排名）",
    "② 📊 Complete F2P GP/Hour Ranking (All 18 Methods)": "完整免费GP/小时排名（全部18种方法）",
    "③ 🔍 Detailed Strategy for Top 10 Methods": "前10名方法的详细策略",
    "④ ✨ High Alchemy — The F2P Profit Multiplier": "高附魔——免费玩家的收益倍增器",
    "⑤ 💰 Bond Math — How Long to Earn a Bond in F2P?": "债券数学——免费玩家赚债券要多久",
    "⑥ ❓ FAQ — F2P Money Making GP/Hour": "免费赚钱GP/小时常见问题",
    "⑦ 💡 Final Tips for F2P Money Making": "免费赚钱最终建议",
    "🥇 1. Ogress Warriors (Corsair Cove) — 120K-1.8M GP/Hour": "食人魔战士（Corsair Cove）——12万-180万GP/小时",
    "🥈 2. Swordfish Fishing (Karamja Dock) — 80K-120K GP/Hour": "剑鱼钓鱼（Karamja码头）——8万-12万GP/小时",
    "🥉 3. Yew Log Cutting (Edgeville) — 60K-90K GP/Hour": "紫杉木砍伐（Edgeville）——6万-9万GP/小时",
    "🥊 4. High Alchemy While Skilling — +50K-150K GP/Hour": "练技能时高附魔——+5万-15万GP/小时",
    "🥋 5. Nature Runecrafting (44 Runecrafting) — 100K-180K GP/Hour": "自然符文制作（44符文制作）——10万-18万GP/小时",
    "3.1 🔥 Ogress Warriors — Complete Strategy": "食人魔战士——完整策略",
    "3.2 🎣 Swordfish Fishing — Complete Strategy": "剑鱼钓鱼——完整策略",
    "3.3 🌿 Nature Runecrafting — Complete Strategy": "自然符文制作——完整策略",
    "3.4 🪓 Yew Log Cutting — Complete Strategy": "紫杉木砍伐——完整策略",
    "3.5 🐄 Cowhide Collecting — New Player Friendly": "牛皮收集——新手友好",
    "4.1 📊 How High Alchemy Works": "高附魔如何运作",
    "4.2 💰 Buying Items to High Alchemy (The \"Flip\")": "购买物品进行高附魔（倒卖）",
    "⚔️ Ready to Start Bossing with Your F2P GP?": "准备好用免费GP开始打Boss了吗",
    "💰 Want Faster Profit? Go Members After Your First Bond": "想要更快收益？第一个债券后就成为会员",

    # ==== Farming Herb Runs ====
    "🌿 1. Why Farming Herb Runs Are the Best Passive Income": "为什么草药跑商是最佳被动收入",
    "📋 2. Requirements to Start Herb Runs": "开始草药跑商的要求",
    "🌱 3. Best Herbs to Plant (Profit per Run)": "最佳种植草药（每次收益）",
    "🗺️ 4. All Herb Patch Locations (Map Route)": "所有草药地块位置（地图路线）",
    "🚶 5. Step-by-Step Herb Run (5 Minutes)": "逐步草药跑商（5分钟）",
    "📊 6. Profit Calculator — How Much You Make": "收益计算器——你能赚多少",
    "⚡ 7. 5 Tips to Maximize Farming Profit": "最大化种植收益的5个技巧",
    "❓ 8. FAQ": "常见问题",
    "⚡ Quick Jump": "快速跳转",
    "① Why Ranarr Weed Is the Best Mid-Game Herb": "为什么Ranarr Weed是最佳中期草药",
    "① Optimal Herb Run Route (9 Patches)": "最佳草药跑商路线（9个地块）",
    "🎯 What To Do After Your First Herb Run": "第一次草药跑商后该做什么",

    # ==== Flipping Guide Beginners ====
    "🎯 Why Flipping Pays: 7% Daily ROI (Zero Requirements)": "为什么倒卖赚钱：每日7%回报率（零要求）",
    "📊 How GE Flipping Works: Spread + 4h Buy Limit": "交易所倒卖如何运作：差价+4小时购买限制",
    "🔍 How to Find Items to Flip (3 Methods)": "如何找到倒卖物品（3种方法）",
    "📋 Step-by-Step Strategy: 100K → 1M GP": "逐步策略：10万→100万GP",
    "💰 10 Best Items to Flip: 1M-10M GP": "10种最佳倒卖物品：100万-1000万GP",
    "⚠️ 6 Common Mistakes That Cost GP": "6个浪费GP的常见错误",
    "❓ FAQ + Advanced Tips": "常见问题+高级技巧",
    "① Table of Contents": "目录",
    "② 📊 Flipping Profit Progression — What to Expect": "倒卖收益进阶——预期",
    "③ 📐 The Buy-Sell Spread (Your Profit)": "买卖价差（你的利润）",
    "④ ⏱️ The 4-Hour Buy Limit — Capacity Cap": "4小时购买限制——容量上限",
    "⑤ 📊 GE Tax — The 1% You Must Account For": "交易所税——必须考虑的1%",
    "⑥ 1️⃣ Method: Manual Margin Check (Most Accurate)": "方法：手动差价检查（最准确）",
    "⑦ 2️⃣ Method: Use Price Tracking Tools": "方法：使用价格追踪工具",
    "⑧ 3️⃣ Method: Follow Content Cycles": "方法：跟随内容周期",
    "⑨ 📋 The 5-Step Flip Cycle": "5步倒卖周期",
    "🎯 Your First Flip — Walkthrough": "你的第一次倒卖——实战演练",
    "⑩ 💰 10 Best Items: Under 1M GP": "10种最佳物品：100万GP以下",
    "💰 Best Starter Trio (Under 350K Capital)": "最佳新手三件套（35万本金以下）",
    "📈 Scaling Strategy for 1M-10M Flippers": "100万-1000万倒卖者的扩大策略",
    "1️⃣ Mistake: Overinvesting in One Item": "错误：过度投资单一物品",
    "2️⃣ Mistake: Flipping Low-Volume Items": "错误：倒卖低成交量物品",
    "3️⃣ Mistake: Ignoring GE Tax": "错误：忽略交易所税",
    "4️⃣ Mistake: Canceling Offers Too Quickly": "错误：过快取消订单",
    "5️⃣ Mistake: Panic Selling During Dip": "错误：下跌时恐慌抛售",
    "6️⃣ Mistake: Flipping After Game Updates": "错误：游戏更新后倒卖",
    "❓ Q: How much GP to start flipping?": "问：倒卖需要多少GP起步",
    "❓ Q: How fast do GE offers fill?": "问：交易所订单多久成交",
    "❓ Q: Can I make money while training?": "问：训练技能时也能赚钱吗",
    "❓ Q: What's the best item to flip?": "问：最佳的倒卖物品是什么",
    "❓ Q: What are \"limit stacking\" & \"overnight\"?": '问：什么是「限额堆积」和「隔夜」',
    "❓ Q: How to avoid losing GP on flips?": "问：如何避免倒卖亏损",
    "📊 The Flipping Pyramid — Final Words": "倒卖金字塔——最后的话",
}

# ===== ARTICLE METADATA =====
FILE_META = {
    "mid-game-money-making-2026.html": (
        "OSRS 中期赚钱攻略 2026 — 从100万到1亿GP的完整路线图",
        "本指南专为有70-90级属性的中期玩家设计，涵盖Barrows、Zulrah、Vorkath等高效赚钱方法。通过草药跑商、鸟窝陷阱等被动收入策略，帮助你从100万稳步增长到1亿GP。所有数据基于2026年7月最新市场价格。"
    ),
    "osrs-afk-money-making-methods-2026.html": (
        "OSRS 2026 十大挂机赚钱方法排名 — GP/小时与注意力评分",
        "精选10种OSRS挂机赚钱方法，按GP/小时和注意力需求双重评分。从魔法弦琴到夜之兽，从挖矿到钓鱼，找到最适合你在工作/学习时玩的赚钱方式。数据基于2026年7月最新GE价格。"
    ),
    "osrs-afk-money-making-ultimate-guide-2026.html": (
        "OSRS 2026 挂机赚钱终极指南：20+种方法（每小时10万-200万GP）",
        "最完整的OSRS挂机赚钱指南，涵盖20+种方法，按GP/小时和注意力评分双重排序。从真挂机（2分钟+点击间隔）到低注意力方法，详细分析每个方法的收益、要求和最佳练级路线。附有注意力评分矩阵和工作/学习最佳挂机方案。"
    ),
    "osrs-best-money-making-methods-2026.html": (
        "OSRS 2026 最佳赚钱方法 — GP/小时排名（数据分析）",
        "基于10,847个数据点，通过RuneLite插件统计、Reddit社区调查和GE价格追踪，为您呈现2026年最准确的OSRS赚钱方法排名。完整排名包含高、中、低等级及免费玩家的分类分析。"
    ),
    "osrs-bond-farming-free-membership-2026.html": (
        "OSRS 2026 债券养殖攻略 — 免费获得会员资格的完整指南",
        "学习如何通过游戏内赚钱来持续购买会员债券，再也不需要花真钱。本指南提供从免费玩家开始的完整债券养殖策略，包括最佳赚钱方法、14天加速计划和会员资格维持技巧。"
    ),
    "osrs-bond-farming-strategy-2026.html": (
        "OSRS 2026 债券养殖策略 — 高效会员资格管理",
        "掌握OSRS债券养殖的完整策略，从购买第一个债券到永久维持会员资格。涵盖债券经济分析、最佳赚钱效率方法、14天冲刺计划和避免债券陷阱的实用技巧。"
    ),
    "osrs-cheap-flipping-methods-new-players.html": (
        "OSRS 2026 新手低成本倒卖指南 — 100万GP起步的翻转策略",
        "即使只有100万GP，你也可以通过交易所倒卖赚钱！本指南教会新手玩家低价买入、高价卖出的核心技巧，推荐适合小资金的倒卖物品清单，以及如何逐步扩大利润的完整策略。"
    ),
    "osrs-combat-money-making-non-boss-2026.html": (
        "OSRS 2026 战斗赚钱指南 — 9种非Boss方法（每小时高达300万GP）",
        "不想打Boss但想通过战斗赚钱？本指南精选9种最优的非Boss战斗赚钱方法，从Gargoyles到Nightmare Zone，涵盖各种战斗等级和装备需求。附有完整的GP/小时排名和要求对照表。"
    ),
    "osrs-daily-weekly-money-routine-2026.html": (
        "OSRS 2026 每日每周赚钱计划 — 被动收入最大化路线图",
        "建立高效的每日和每周赚钱计划，最大化被动收入。从草药跑商到鸟窝陷阱，从战斗任务到倒卖操作，安排最优的日常赚钱流程。每天只需30-60分钟，即可稳定获得100万+GP。"
    ),
    "osrs-f2p-ironman-money-making-early-game.html": (
        "OSRS 2026 免费铁人前期赚钱攻略 — 零会员的自给自足指南",
        "专为免费铁人玩家设计的前期赚钱指南，涵盖不需要会员资格的自给自足赚钱方法。从收集牛皮带到大骨头，从采矿到钓鱼，详细分析每种方法对铁人账号的实用性和效率。"
    ),
    "osrs-f2p-money-making-first-bond-2026.html": (
        "OSRS 2026 免费玩家赚钱指南 — 赚取你的第一个会员债券",
        "完全免费玩家如何赚到850万GP购买第一个会员债券？本指南提供从0开始的完整路线图，包括最佳免费赚钱方法排名、效率技巧和时间预估。无需任何技能要求即可开始赚钱。"
    ),
    "osrs-f2p-money-making-no-stats.html": (
        "OSRS 2026 零属性赚钱指南 — 不需要技能的GP赚取方法",
        "刚建号没有任何技能等级？没问题！本指南列出所有不需要任何技能要求的免费赚钱方法，从最基础的收集物品到简单的战斗掉落，让你从第一天就开始积累财富。"
    ),
    "osrs-f2p-money-making-ranked-2026.html": (
        "OSRS 2026 免费玩家赚钱方法GP/小时排名",
        "完整的OSRS免费玩家赚钱指南，每种方法都有精确的GP/小时数据。从最佳到最差排名所有免费赚钱方式，包括详细的收益分析、属性要求和装备推荐。助你免费玩家也能高效赚GP。"
    ),
    "osrs-farming-herb-runs-beginner-guide-2026.html": (
        "OSRS 2026 草药跑商新手指南 — 被动收入从零开始",
        "草药跑商是OSRS最稳定的被动收入来源之一。本指南从零开始教新手玩家如何设置和优化草药跑商路线，推荐最佳种植草药、所需等级和装备要求，以及如何将每次跑商利润最大化。"
    ),
    "osrs-flipping-guide-beginners-2026.html": (
        "OSRS 2026 倒卖指南新手篇 — 交易所赚钱完整教程",
        "从零开始学习OSRS交易所倒卖的艺术！本指南涵盖倒卖基础知识、最佳倒卖物品推荐、市场分析工具使用和风险控制策略。无论你有多少本金，都能找到适合自己的倒卖方法。"
    ),
}


def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def extract_chinese_meta(zh_content):
    meta = {}
    if zh_content:
        m = re.search(r'<html\s+lang="([^"]+)"', zh_content)
        meta["html_lang"] = m.group(1) if m else "zh-Hans"
        m = re.search(r"<title>([^<]+)</title>", zh_content)
        meta["title"] = m.group(1).strip() if m else ""
        # Check for Chinese canonical already
        m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', zh_content)
        meta["canonical"] = m.group(1) if m else ""
        meta["hreflangs"] = re.findall(
            r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>',
            zh_content,
        )
        m = re.search(
            r"(<script type=\"application/ld\+json\">.*?</script>)",
            zh_content,
            re.DOTALL,
        )
        meta["ldjson"] = m.group(1) if m else ""
    return meta


def translate_text(text):
    """Look up Chinese translation for a heading/title."""
    text = text.strip()
    # Try exact match
    if text in T:
        return T[text]
    # Try stripping trailing punctuation
    text_clean = re.sub(r'[?.!]+$', '', text).strip()
    if text_clean in T:
        return T[text_clean]
    # Try without leading numbers
    text_clean2 = re.sub(r'^\d+\.\s*', '', text)
    if text_clean2 in T:
        return T[text_clean2]
    # Try without leading numbers and trailing punctuation
    text_clean3 = re.sub(r'^\d+\.\s*', '', text_clean)
    if text_clean3 in T:
        return T[text_clean3]
    # Try removing extra whitespace
    text_norm = re.sub(r'\s+', ' ', text)
    if text_norm in T:
        return T[text_norm]
    return None


def process_file(html_file):
    en_path = os.path.join(EN_DIR, html_file)
    zh_path = os.path.join(ZH_DIR, html_file)

    en_content = read_file(en_path)
    if en_content is None:
        return f"ERROR: English file not found: {en_path}"

    zh_content = read_file(zh_path)

    cn_title_text, cn_summary_text = FILE_META.get(html_file, ("", ""))

    content = en_content

    # 1. Change html lang
    content = re.sub(r'<html\s+lang="en"', '<html lang="zh-Hans"', content)

    # 2. Replace title
    content = re.sub(
        r"<title>[^<]+</title>",
        f"<title>{cn_title_text}</title>",
        content,
    )

    # 3. Replace canonical URL - handle both en and already-zh cases
    content = re.sub(
        r'(<link\s+rel="canonical"\s+href="https://osrsguru\.com/)guides/',
        r'\1zh/guides/',
        content,
    )

    # 4. Add hreflang tags after canonical
    hreflang_block = (
        '\n    <link rel="alternate" hreflang="en" href="https://osrsguru.com/guides/'
        + html_file
        + '">\n    <link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/guides/'
        + html_file
        + '">\n    <link rel="alternate" hreflang="x-default" href="https://osrsguru.com/zh/guides/'
        + html_file
        + '">'
    )

    # Insert hreflang after canonical, but avoid duplication
    if 'hreflang="zh"' not in content:
        content = re.sub(
            r'(<link\s+rel="canonical"[^>]*>)',
            r"\1" + hreflang_block,
            content,
        )

    # 5. Add Chinese hero title and summary in hero section
    hero_insert = f'''            <h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title_text}</h1>
            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary_text}</p>
'''

    # Insert after breadcrumb, before h1
    content = re.sub(
        r'(<p class="breadcrumb">.*?</p>\s*)<h1',
        r"\1" + hero_insert + "<h1",
        content,
        flags=re.DOTALL,
    )

    # 6. Process TOC items - add Chinese annotation after English text
    def process_toc(match):
        before = match.group(1)
        text = match.group(2)
        after = match.group(3)
        cn = translate_text(text)
        if cn:
            return f'{before}{text}（{cn}）{after}'
        return match.group(0)

    content = re.sub(
        r'(<a\s+href="#[^"]*">)([^<]+?)(</a>)',
        process_toc,
        content,
    )

    # 7. Process h2 headings
    def process_h2(match):
        text = match.group(1)
        cn = translate_text(text)
        if cn:
            return f'<h2>{text}（{cn}）</h2>'
        return f"<h2>{text}</h2>"

    content = re.sub(r"<h2>([^<]+?)</h2>", process_h2, content)

    # 8. Process h3 headings
    def process_h3(match):
        text = match.group(1)
        # Skip content inside support card, related guides, footer
        cn = translate_text(text)
        if cn:
            return f'<h3>{text}（{cn}）</h3>'
        return f"<h3>{text}</h3>"

    content = re.sub(r"<h3>([^<]+?)</h3>", process_h3, content)

    # 9. Update ld+json headline if present
    content = re.sub(
        r'"headline"\s*:\s*"[^"]*"',
        f'"headline": "{cn_title_text}"',
        content,
    )

    # Write the result
    write_file(zh_path, content)
    return f"OK: {html_file}"


def main():
    os.makedirs(ZH_DIR, exist_ok=True)
    results = []
    for i, fname in enumerate(FILES, 1):
        print(f"[{i}/15] Processing {fname}...")
        result = process_file(fname)
        print(f"  -> {result}")
        results.append(result)

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    for r in results:
        status = "OK" if r.startswith("OK") else "FAIL"
        print(f"  [{status}] {r}")


if __name__ == "__main__":
    main()
