#!/usr/bin/env python3
"""
Group 2 of Team 3: Process 7 beginner guides.
Copy English content to zh/ files with Chinese translations.
"""
import re
import os

BASE = r"c:\Users\Lenovo\osrs-guide-site"
EN_DIR = os.path.join(BASE, "guides")
ZH_DIR = os.path.join(BASE, "zh/guides")

FILENAMES = [
    "osrs-f2p-ironman-money-making-early-game.html",
    "osrs-f2p-leveling-guide-2026.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-quests-before-membership-2026.html",
    "osrs-f2p-to-member-first-10-things-2026.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
]

# ========== PER-FILE DATA ==========

FILE_DATA = {
    # File 8
    "osrs-f2p-ironman-money-making-early-game.html": {
        "zh_title": "OSRS 赚钱攻略 — OSRS F2P Ironman Money Making Early Game 2026 — Cowhides, Crafting & Alching | OSRS Guru",
        "cn_h1": "OSRS F2P铁人早期赚钱 — 零成本起步（2026版）",
        "cn_summary": "F2P铁人模式早期赚钱指南：零成本起步方法，利用有限资源最大化金币收入，从牛皮加工到珠宝高抛，助你渡过铁人最艰难的阶段。",
        "toc_translations": {},
        "h2_translations": {
            "1. The F2P Ironman Challenge": "F2P铁人模式挑战",
            "2. Cowhide Processing — The Best Starting Method": "牛皮加工 — 最佳起步方法",
            "3. Crafting Progression & Alch Values": "制造升级路线与高抛价值",
            "4. Jewelry Crafting for Profit (Level 40+)": "珠宝制造赚钱（40级以上）",
            "5. Rune Essence Mining & Runecrafting": "符文精华开采与符文制作",
            "6. High Alchemy — The Ironman Endgame": "高抛 — 铁人模式的终极赚钱法",
            "7. Advanced Tips for F2P Ironmen": "F2P铁人进阶技巧",
            "8. Common Mistakes": "常见错误",
            "9. Frequently Asked Questions": "常见问题解答",
        },
        "h3_translations": {},
        "quick_summary_bullets": [],
    },
    # File 9
    "osrs-f2p-leveling-guide-2026.html": {
        "zh_title": "OSRS F2P技能训练 — OSRS F2P Leveling Guide 2026 — Max Your Free-to-Play Account Efficiently",
        "cn_h1": "OSRS F2P升级指南 — 高效提升免费账户（2026版）",
        "cn_summary": "完整F2P升级路线图，覆盖全部7个F2P技能的最佳训练地点和每小时经验值（5K-50K），包含3阶段计划表。教你何时从F2P转为付费会员，省下100+小时的无谓刷怪时间。",
        "toc_translations": {
            "🎯 Why Level a F2P Account First?": "为什么先练F2P账户？",
            "⚔️ Combat Leveling (Attack/Strength/Defence/Ranged/Magic)": "战斗技能升级",
            "🔧 Skilling Leveling (Fishing/Cooking/Woodcutting/Mining/Smithing/Crafting/Runecrafting)": "生产技能升级",
            "🗺️ Best F2P Training Spots Map": "最佳F2P训练地点地图",
            "📋 F2P Leveling Order — What to Train First": "F2P升级顺序 — 先练什么",
            "🚪 When to Switch to Members": "何时转为付费会员",
            "❓ FAQ": "常见问题",
            "💡 Final Tips": "最终建议",
        },
        "h2_translations": {
            "① 🎯 Why Level a F2P Account First?": "为什么先练F2P账户？",
            "② ⚔️ Combat Leveling (Attack/Strength/Defence/Ranged/Magic)": "战斗技能升级（攻击/力量/防御/远程/魔法）",
            "③ 🔧 F2P Skilling Leveling (All 7 Non-Combat Skills)": "F2P生产技能升级（全部7个非战斗技能）",
            "④ 🗺️ Best F2P Training Spots Map": "最佳F2P训练地点地图",
            "⑤ 📋 F2P Leveling Order — What to Train First": "F2P升级顺序 — 先练什么",
            "⑥ 🚪 When to Switch to Members": "何时转为付费会员",
            "⑦ ❓ FAQ — F2P Leveling Guide": "常见问题 — F2P升级指南",
            "⑧ 💡 Final Tips for F2P Leveling": "F2P升级最终建议",
        },
        "h3_translations": {
            "1.1 💰 Learn the Game Without Wasting Membership Days": "在不浪费会员天数的情况下学习游戏",
            "1.2 📊 This Is How Far F2P Can Actually Take You": "F2P实际上能走多远",
            "1.3 🏆 F2P Achievements Worth Going For": "值得追求的F2P成就",
            "2.1 🗡️ Melee (Attack/Strength/Defence) — Complete F2P Path": "近战（攻击/力量/防御）— 完整F2P路线",
            "2.2 🏹 Ranged — Best F2P Training": "远程 — 最佳F2P训练方法",
            "2.3 ✨ Magic — F2P Training Methods": "魔法 — F2P训练方法",
            "3.1 🎣 Fishing": "钓鱼",
            "3.2 🍳 Cooking": "烹饪",
            "3.3 🪓 Woodcutting": "砍树",
            "3.4 ⛏️ Mining": "采矿",
            "3.5 🔨 Smithing": "锻造",
            "3.6 🎨 Crafting": "制造",
            "3.7 🔮 Runecrafting": "符文制作",
            "4.1 🔥 Stronghold of Security (Barbarian Village)": "安全堡垒（野蛮人村）",
            "4.2 🦎 Corsair Cove (Best All-Round F2P Zone)": "海盗湾（最佳全能F2P区域）",
            "4.3 ⛰️ Crandor (Dragon Slayer Island)": "克兰多尔（屠龙者岛）",
            "5.1 🥇 Phase 1: The First 10 Hours (New Account)": "第一阶段：前10小时（新账户）",
            "5.2 🥈 Phase 2: The Mid-Game Foundation (10–40 Hours)": "第二阶段：中期基础（10-40小时）",
            "5.3 🥉 Phase 3: F2P Endgame (40–80+ Hours)": "第三阶段：F2P后期（40-80+小时）",
            "6.1 📉 Signs F2P Is Becoming Inefficient": "F2P变得低效的迹象",
            "6.2 💡 The Sweet Spot: Level 50s Across the Board": "最佳平衡点：全技能50级",
        },
    },
    # File 10
    "osrs-f2p-money-making-first-bond-2026.html": {
        "zh_title": "OSRS F2P 赚取第一个 Bond 指南 2026 | 最佳方法 | First Bond Money Making",
        "cn_h1": "OSRS F2P最佳赚钱方法 — 赚取你的第一张Bond（2026版）",
        "cn_summary": "完整F2P赚钱指南：牛皮收集、精华矿开采、钓鱼烹饪、山丘巨人刷宝等4种最佳方法，精确GP/小时数据，20-25小时赚够1000万GP购买你的第一张Bond。",
        "toc_translations": {
            "💰 Why You Need 10M GP for Your First Bond": "为什么需要1000万GP买第一张Bond",
            "🥇 Best F2P Method: Cowhides (500K-800K GP/hr)": "最佳F2P方法：牛皮（50-80万/小时）",
            "🪨 Second Best: Essence Mining (300K-500K GP/hr)": "次佳：精华矿开采（30-50万/小时）",
            "🐟 Fishing & Cooking Combo (400K-600K GP/hr)": "钓鱼与烹饪组合（40-60万/小时）",
            "🗡️ Hill Giants Loot Run (600K-900K GP/hr)": "山丘巨人刷宝（60-90万/小时）",
            "⏱️ Realistic Timeline: How Long to Your First Bond": "现实时间线：多久能赚到第一张Bond",
            "💡 Pro Tips to Speed Up Bond Farming": "加速赚取Bond的专业技巧",
            "❓ FAQs": "常见问题",
        },
        "h2_translations": {
            "1. 💰 Why You Need 10M GP for Your First Bond": "为什么需要1000万GP购买第一张Bond",
            "2. 🥇 Best F2P Method: Cowhides (500K-800K GP/hr)": "最佳F2P方法：牛皮（50-80万GP/小时）",
            "3. 🪨 Second Best: Essence Mining (300K-500K GP/hr)": "次佳方法：精华矿开采（30-50万GP/小时）",
            "4. 🐟 Fishing & Cooking Combo (400K-600K GP/hr)": "钓鱼与烹饪组合（40-60万GP/小时）",
            "5. 🗡️ Hill Giants Loot Run (600K-900K GP/hr)": "山丘巨人刷宝（60-90万GP/小时）",
            "6. ⏱️ Realistic Timeline: How Long to Your First Bond": "现实时间线：多久能赚到第一张Bond",
            "7. 💡 Pro Tips to Speed Up Bond Farming": "加速赚取Bond的专业技巧",
            "8. ❓ FAQs — F2P Money Making for Your First Bond": "常见问题 — F2P赚钱购买第一张Bond",
        },
        "h3_translations": {
            "1.1 Bond Price History (2026 Edition)": "Bond价格历史（2026版）",
            "1.2 GP/USD Ratio Trend — Why Bonds Keep Getting More Expensive": "GP/美元汇率趋势 — Bond为何越来越贵",
            "2.1 Location: Lumbridge East Cow Field": "位置：伦布里奇东部牛场",
            "2.2 Gear Setup (No Membership Needed)": "装备配置（无需会员）",
            "2.3 Banking Route & Efficiency Tips": "银行路线与效率技巧",
            "2.4 Realistic GP/Hr Breakdown": "实际GP/小时分析",
            "3.1 Varrock East Mine vs Draynor Village": "瓦罗克东矿 vs 德雷诺村",
            "3.2 Runecrafting for Extra Profit (If You Have 1+ RC)": "符文制作赚取额外利润",
            "3.3 GP/Hr Breakdown — Essence Mining": "GP/小时分析 — 精华矿开采",
            "4.1 Best F2P Fishing Spots (2026)": "最佳F2P钓鱼地点（2026）",
            "4.2 Food Value for Members Later": "为日后会员存粮的价值",
            "5.1 Edgeville Dungeon Route": "埃奇维尔地牢路线",
            "5.2 Hill Giants Loot Table Breakdown": "山丘巨人掉落表分析",
            "5.3 Time to 10M GP — Hill Giants Route": "赚取1000万GP所需时间",
            "6.1 2-Week Plan (1 Hour/Day)": "两周计划（每天1小时）",
            "6.2 1-Week Plan (3 Hours/Day)": "一周计划（每天3小时）",
            "6.3 Ultra-Fast Plan (Hardcore Grind — 5 Days)": "极速计划（硬核刷 — 5天）",
            "7.1 Use Yak Track Rewards (Free GP)": "利用Yak Track奖励（免费GP）",
            "7.2 Daily Challenges for Extra XP (and GP)": "每日挑战获取额外经验和GP",
            "7.3 Don't Waste GP on Upgrade Gear": "不要浪费GP升级装备",
            "7.4 Use the Grand Exchange Smartly": "聪明使用大交易所",
        },
    },
    # File 11
    "osrs-f2p-money-making-no-stats.html": {
        "zh_title": "OSRS 赚钱攻略 — OSRS F2P Money Making No Stats 2026 — 10+ Methods for Brand New Accounts | OSRS Guru",
        "cn_h1": "OSRS F2P零属性赚钱指南 — 新账号10+方法（2026版）",
        "cn_summary": "全新OSRS账号零属性零GP起步赚钱攻略：涵盖牛皮收集、精华矿开采、荒野捡垃圾、香蕉采摘、戒指附魔等10+种方法。15-25小时赚够100万GP，助你购买第一套装备。",
        "toc_translations": {},
        "h2_translations": {
            "1. Method: Collecting Cowhides + Bones (Lumbridge)": "方法一：收集牛皮+骨头（伦布里奇）",
            "2. Method: Mining Rune Essence": "方法二：开采符文精华",
            "3. Method: Picking Up Loot at the Wilderness Ditch": "方法三：在荒野沟渠捡拾战利品",
            "4. Method: Picking Bananas at Musa Point (Karamja)": "方法四：在穆萨点采摘香蕉（卡拉姆贾）",
            "5. Method: Bone Yard Collecting (Wilderness)": "方法五：荒野墓地收集骨头",
            "6. Method: Enchanting Sapphire Rings (Semi-AFK Magic Profit)": "方法六：附魔蓝宝石戒指（半挂机魔法赚钱）",
            "7. Method: Buying from Shops and Selling on GE (Arbitrage)": "方法七：从商店买入到大交易所卖出（套利）",
            "8. Common F2P Money Making Mistakes": "F2P赚钱常见错误",
            "9. Frequently Asked Questions": "常见问题解答",
        },
        "h3_translations": {},
        "quick_summary_bullets": [
            "📌 <strong>10+种零需求方法</strong> — 从牛皮收集（4-6万/小时）到荒野捡垃圾（8-12万/小时）",
            "📌 <strong>最佳安全方法：伦布里奇牛皮</strong> — 高峰期30秒装满背包，4-6万/小时",
            "📌 <strong>完成1个任务后最佳：符文精华开采</strong> — 需完成符文之谜（5分钟），3-5万/小时",
            "📌 <strong>100万GP时间线：15-25小时</strong> — 一个周末可完成，但不建议用此法赚Bond（180-300小时）",
            "📌 <strong>专业技巧：</strong> 蓝宝石戒指附魔7级魔法即可，5万+/小时 — 买蓝宝石戒指，附魔，转卖",
        ],
    },
    # File 12
    "osrs-f2p-quests-before-membership-2026.html": {
        "zh_title": "OSRS 任务攻略 — OSRS F2P Quests You Must Finish Before Becoming a Member in 2026",
        "cn_h1": "OSRS成为会员前必须完成的F2P任务（2026版）",
        "cn_summary": "完整列出全部18个OSRS F2P任务，包含6万+总经验奖励、难度评级、时间估算和3小时速通路线。在激活Bond或订阅前完成所有免费任务，避免浪费宝贵的会员天数。",
        "toc_translations": {
            "🎯 Why Finish F2P Quests Before Buying Membership": "为什么要在购买会员前完成F2P任务",
            "🗺️ Must-Do F2P Quest List (Priority Order)": "必做F2P任务清单（按优先级排序）",
            "📊 Reward Summary Table — All F2P Quest Rewards": "奖励汇总表 — 所有F2P任务奖励",
            "⚡ Fastest Route: Complete All F2P Quests in 3 Hours": "最快路线：3小时完成全部F2P任务",
            "🎁 Post-Quest: What to Do Immediately After Buying Membership": "任务后：购买会员后立即做什么",
            "💡 Common Mistakes to Avoid": "需要避免的常见错误",
            "❓ FAQ": "常见问题",
        },
        "h2_translations": {
            "1. 🎯 Why Finish F2P Quests Before Buying Membership": "为什么在购买会员前完成F2P任务",
            "2. 🗺️ Must-Do F2P Quest List (Priority Order)": "必做F2P任务清单（按优先级排序）",
            "3. 📊 Reward Summary Table — All F2P Quest Rewards": "奖励汇总表 — 所有F2P任务奖励",
            "4. ⚡ Fastest Route: Complete All F2P Quests in 3 Hours": "最快路线：3小时完成全部F2P任务",
            "5. 🎁 Post-Quest: What to Do Immediately After Buying Membership": "任务后：购买会员后立即做什么",
            "6. 💡 Common Mistakes to Avoid": "需要避免的常见错误",
            "7. ❓ FAQ — F2P Quests Before Membership": "常见问题 — 会员前F2P任务",
        },
        "h3_translations": {
            "1.1 ⏱️ Every Minute of Membership Costs GP or Real Money": "会员的每一分钟都花费GP或真钱",
            "1.2 📈 F2P Quests Give You a Level Head Start": "F2P任务给你等级优势",
            "1.3 🎫 Quest Points Are Required for Members Quests": "会员任务需要任务点数",
            "1.4 🛡️ Unlock Essential Items and Areas": "解锁关键物品和区域",
            "2.1 🍳 Cook's Assistant — ★ Essential (Top Priority)": "厨师助手 — ★ 必不可少（最高优先级）",
            "2.2 ⛏️ Doric's Quest — ★ Essential": "多里克的差事 — ★ 必不可少",
            "2.3 👻 The Restless Ghost — ★ Essential": "不安分的幽灵 — ★ 必不可少",
            "2.4 🧪 Witch's Potion — ★ Essential": "女巫的药水 — ★ 必不可少",
            "2.5 🐑 Sheep Shearer — ★ Essential": "剪羊毛 — ★ 必不可少",
            "2.6 👺 Goblin Diplomacy — ★ High Priority": "哥布林外交 — ★ 高优先级",
            "2.7 🐔 Ernest the Chicken — ★ High Priority": "厄内斯特鸡 — ★ 高优先级",
            "2.8 🔍 Misthalin Mystery — ★ Medium Priority": "米斯萨林之谜 — ★ 中优先级",
            "2.9 📋 Other F2P Quests Worth Completing": "其他值得完成的F2P任务",
            "4.1 📍 Phase 1 — Lumbridge Cluster (~40 minutes)": "第一阶段 — 伦布里奇集群（约40分钟）",
            "4.2 📍 Phase 2 — Draynor & Falador (~45 minutes)": "第二阶段 — 德雷诺与法尔多（约45分钟）",
            "4.3 📍 Phase 3 — Rimmington & Port Sarim (~35 minutes)": "第三阶段 — 里明顿与萨里姆港（约35分钟）",
            "4.4 📍 Phase 4 — Al Kharid & Varrock (~40 minutes)": "第四阶段 — 阿卡里德与瓦罗克（约40分钟）",
            "4.5 📍 Phase 5 — Dragon Slayer (~30 minutes)": "第五阶段 — 屠龙者（约30分钟）",
            "5.1 🚀 Hour 1: Unlock Critical Members Teleports": "第1小时：解锁关键会员传送",
            "5.2 💰 Hour 2-3: Start Making GP": "第2-3小时：开始赚取GP",
            "5.3 🗡️ Hour 4+: Start Questing for Key Unlocks": "第4小时后：开始做任务解锁关键内容",
            "6.1 ❌ Buying Membership Before Doing Any Quests": "在做任何任务前购买会员",
            "6.2 ❌ Skipping Rune Mysteries": "跳过符文之谜",
            "6.3 ❌ Doing Shield of Arrav Without Planning": "毫无计划地开始阿勒夫盾牌",
            "6.4 ❌ Fighting Elvarg Unprepared": "毫无准备地挑战艾尔瓦格",
            "6.5 ❌ Buying Bonds Instead of Membership": "用Bond替代订阅",
        },
    },
    # File 13
    "osrs-f2p-to-member-first-10-things-2026.html": {
        "zh_title": "OSRS 新手入门 — 10 Things to Do First After Buying OSRS Membership (2026 Roadmap)",
        "cn_h1": "购买OSRS会员后首先做的10件事（2026路线图）",
        "cn_summary": "刚升级到付费会员？按此10步路线图进行：解锁5+传送网络、4小时内战斗到50+级、用会员方法每小时赚50万+GP、获得43祈祷、开始瀑布任务。不要在第一天瞎逛浪费宝贵的会员时间。",
        "toc_translations": {
            "🗺️ Quest Log & Unlock Teleports": "任务日志与解锁传送",
            "🎯 Train Combat to 50+": "训练战斗技能到50+",
            "💰 Get a Money-Making Method Going": "开始赚钱方法",
            "🏪 Unlock Key Members Areas": "解锁关键会员区域",
            "🎣 Fishing/Cooking 60+ & 43 Prayer": "钓鱼/烹饪60+和43祈祷",
            "📦 Organize Bank & Start Members Quests": "整理银行并开始会员任务",
            "🏋️ Join a Clan & Set Up XP Tracker": "加入公会并设置经验追踪",
            "❓ FAQs": "常见问题",
        },
        "h2_translations": {
            "① 🗺️ Set Up Your Quest Log & Unlock Teleports": "设置任务日志并解锁传送",
            "② 🎯 Train Attack/Strength/Defence to 50+ Immediately": "立即训练攻击/力量/防御到50+",
            "③ 💰 Get a Money-Making Method Going": "开始赚钱方法",
            "④ 🏪 Unlock Key Members Areas": "解锁关键会员区域",
            "⑤ 🎣 Level Fishing & Cooking to 60+ and Get 43 Prayer": "将钓鱼和烹饪升至60+并获取43祈祷",
            "⑥ 📦 Organize Your Bank & Start Members Quests": "整理银行并开始会员任务",
            "⑦ 🏋️ Join a Clan & Set Up Your XP Tracker": "加入公会并设置经验追踪",
            "⑧ ❓ FAQs — First Things to Do as a New OSRS Member": "常见问题 — 新手会员首先做什么",
        },
        "h3_translations": {
            "1.1 📜 Open Your Quest Log & Pick a Starting Quest": "打开任务日志并选择起始任务",
            "1.2 🧚 Unlock Fairy Rings & Spirit Trees": "解锁精灵环与精灵树",
            "1.3 🏠 Get a Player-Owned House (POH)": "购买玩家住房",
            "2.1 🦀 Go to Sand Crabs (Best AFK Training)": "去沙蟹（最佳挂机训练）",
            "2.2 ⚔️ Gear Progression: What to Wear": "装备升级：穿什么",
            "2.3 💊 Use Combat Potions": "使用战斗药水",
            "3.1 🌿 Wintertodt (Low Requirements, High Profit)": "冬潮（低需求高利润）",
            "3.2 🐉 Killing Green Dragons (Combat + GP)": "击杀绿龙（战斗+赚钱）",
            "3.3 🧹 Early Slayer for Long-Term GP": "早期打怪任务获取长期收入",
            "4.1 🏦 Varrock & the Grand Exchange": "瓦罗克与大交易所",
            "4.2 🎣 Catherby (Fishing & Cooking Hub)": "凯瑟比（钓鱼烹饪中心）",
            "4.3 🏰 Ardougne & Seers' Village": "阿杜因与先知村",
            "4.4 🌑 Canifis & Morytania": "卡尼菲斯与莫里塔尼亚",
            "5.1 🐟 Fishing & Cooking: The Catherby Route": "钓鱼与烹饪：凯瑟比路线",
            "5.2 🙏 Why 43 Prayer Is Non-Negotiable": "为什么43祈祷是必须的",
            "5.3 🦴 Best Way to Buy Bones": "购买骨头的最佳方式",
            "6.1 🏷️ Set Up Bank Tabs": "设置银行标签",
            "6.2 📜 Priority Members Quests (Do These First)": "优先会员任务（先做这些）",
            "6.3 🎯 Recipe for Disaster: The Long Game": "灾难食谱：长期目标",
            "7.1 👥 Join a Clan": "加入公会",
            "7.2 📊 Install RuneLite & Set Up XP Tracking": "安装RuneLite并设置经验追踪",
            "7.3 🎯 Set Goals and Track Them": "设定目标并追踪进度",
        },
    },
    # File 14
    "osrs-farming-herb-runs-beginner-guide-2026.html": {
        "zh_title": "OSRS 赚钱攻略 — OSRS Farming Herb Runs Guide 2026 — Passive Income 500K+ GP/Hour",
        "cn_h1": "OSRS农场药草跑指南 — 被动收入每小时50万+GP（2026版）",
        "cn_summary": "OSRS最佳被动收入方法：5分钟种植药草，90分钟后收获10-50万GP利润。覆盖全部9个药草地点的路线图、最佳种植药草、所需任务和每日赚取100万+GP的专业技巧。",
        "toc_translations": {
            "Why Farming Herb Runs Are the Best Passive Income": "为什么药草跑是最佳被动收入",
            "Requirements to Start Herb Runs": "开始药草跑的要求",
            "Best Herbs to Plant (Profit per Run)": "最佳种植药草（每次利润）",
            "All Herb Patch Locations (Map Route)": "全部药草地点（地图路线）",
            "Step-by-Step Herb Run (5 Minutes)": "分步药草跑（5分钟）",
            "Profit Calculator — How Much You Make": "利润计算器 — 你能赚多少",
            "5 Tips to Maximize Farming Profit": "最大化农场利润的5个技巧",
            "FAQ": "常见问题",
        },
        "h2_translations": {
            "🌿 1. Why Farming Herb Runs Are the Best Passive Income": "为什么药草跑是最佳被动收入",
            "📋 2. Requirements to Start Herb Runs": "开始药草跑的要求",
            "🌱 3. Best Herbs to Plant (Profit per Run)": "最佳种植药草（每次利润）",
            "🗺️ 4. All Herb Patch Locations (Map Route)": "全部药草地点（地图路线）",
            "🚶 5. Step-by-Step Herb Run (5 Minutes)": "分步药草跑（5分钟）",
            "📊 6. Profit Calculator — How Much You Make": "利润计算器 — 你能赚多少",
            "⚡ 7. 5 Tips to Maximize Farming Profit": "最大化农场利润的5个技巧",
            "❓ 8. FAQ": "常见问题",
        },
        "h3_translations": {
            "① Why Ranarr Weed Is the Best Mid-Game Herb": "为什么兰纳草是中后期最佳药草",
            "① Optimal Herb Run Route (9 Patches)": "最佳药草跑路线（9个地块）",
            "① Rake the Patch (If Weedy)": "耙地（如果有杂草）",
            "② Add Ultracompost": "添加超堆肥",
            "③ Plant the Seeds": "播种",
            "④ Wait 90 Minutes (or do other content)": "等待90分钟（或做其他内容）",
            "⑤ Harvest (90 Minutes Later)": "收获（90分钟后）",
            "① Always Use Ultracompost": "始终使用超堆肥",
            "② Get Magic Secateurs (A Fairy Tale Part I)": "获取魔法剪刀（童话故事第一章）",
            "③ Use Farming Potion Before Harvesting": "收获前使用农场药水",
            "④ Unlock the Farming Guild ASAP": "尽快解锁农场公会",
            "⑤ Do Tree Runs Simultaneously": "同时进行种树跑",
        },
    },
}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


def add_cn_title_and_summary(en_content, cn_h1, cn_summary):
    """Add Chinese h1 and summary before English h1 in hero section."""
    # Find the English h1 in the hero section
    pattern = r'(<section class="guide-hero">.*?<div class="container">\s*<p class="breadcrumb">.*?</p>\s*)(<h1[^>]*>)'
    replacement = r'\1' + \
        f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_h1}</h1>\n' + \
        f'<p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>\n' + \
        r'\2'
    
    result = re.sub(pattern, replacement, en_content, count=1, flags=re.DOTALL)
    
    # If no match, try alternate hero structure (file 9, 10, 12, 13 style)
    if result == en_content:
        pattern2 = r'(<section class="guide-hero">.*?<div class="container">\s*<p class="breadcrumb">.*?</p>\s*)(<h1[^>]*>)'
        result = re.sub(pattern2, r'\1' + 
            f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_h1}</h1>\n' +
            f'<p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>\n' + 
            r'\2', result, count=1, flags=re.DOTALL)
    
    return result


def add_translations_to_toc(content, toc_trans):
    """Add Chinese translations to TOC links."""
    if not toc_trans:
        return content
    for en_text, cn_text in toc_trans.items():
        pattern = rf'(<a\s+href="[^"]*"[^>]*>)\s*{re.escape(en_text)}\s*(</a>)'
        content = re.sub(pattern, lambda m: m.group(1) + en_text + '（' + cn_text + '）' + m.group(2), content)
    return content


def add_h2_h3_translations(content, h2_trans, h3_trans):
    """Add Chinese translations to h2 and h3 elements."""
    # h2 translations
    for en_text, cn_text in h2_trans.items():
        pattern = rf'(<h2[^>]*>)\s*{re.escape(en_text)}\s*(</h2>)'
        content = re.sub(pattern, lambda m: m.group(1) + en_text + '（' + cn_text + '）' + m.group(2), content)
    
    # h3 translations
    for en_text, cn_text in h3_trans.items():
        pattern = rf'(<h3[^>]*>)\s*{re.escape(en_text)}\s*(</h3>)'
        content = re.sub(pattern, lambda m: m.group(1) + en_text + '（' + cn_text + '）' + m.group(2), content)
    
    return content


def handle_quick_summary(content, bullets):
    """Translate quick-summary box bullets to Chinese."""
    if not bullets:
        return content
    # Find the quick-summary div
    pattern = r'(<div class="quick-summary"[^>]*>.*?<h3[^>]*>.*?</h3>\s*<ul[^>]*>).*?(</ul>\s*</div>)'
    
    bullets_html = "\n".join(f'                    <li>{b}</li>' for b in bullets)
    # Escape properly
    replacement = r'\1\n' + bullets_html + r'\n                \2'
    result = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if result != content:
        return result
    
    # Try with different whitespace
    pattern2 = r'(<div class="quick-summary"[^>]*>.*?<h3[^>]*>.*?</h3>\s*<ul[^>]*>\s*).*?(\s*</ul>\s*</div>)'
    replacement2 = r'\1\n' + bullets_html + r'\n                \2'
    return re.sub(pattern2, replacement2, content, flags=re.DOTALL)


def process_file(filename, data):
    """Process a single file pair."""
    en_path = os.path.join(EN_DIR, filename)
    zh_path = os.path.join(ZH_DIR, filename)
    
    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    
    # Read files
    en_html = read_file(en_path)
    
    if os.path.exists(zh_path):
        zh_html = read_file(zh_path)
    else:
        zh_html = en_html
    
    # Start from English content
    new_zh = en_html
    
    # Step 2a: Change html lang to zh-Hans
    new_zh = new_zh.replace('<html lang="en">', '<html lang="zh-Hans">', 1)
    
    # Step 2b: Change title
    zh_title = data["zh_title"]
    # Extract current English title for replacement
    title_match = re.search(r'<title>(.*?)</title>', new_zh)
    if title_match:
        old_title = title_match.group(1)
        new_zh = new_zh.replace(f'<title>{old_title}</title>', f'<title>{zh_title}</title>', 1)
    
    # Step 2c: Change canonical URL to zh version
    # Replace the canonical URL (the one ending in /guides/...) with /zh/guides/...
    def fix_canonical(m):
        href = m.group(1)
        if "/zh/guides/" not in href:
            new_href = href.replace("/guides/", "/zh/guides/")
            return f'<link rel="canonical" href="{new_href}">'
        return m.group(0)
    
    new_zh = re.sub(r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>', fix_canonical, new_zh)
    
    # Also fix og:url
    def fix_og_url(m):
        content = m.group(1)
        if "/zh/guides/" not in content:
            new_content = content.replace("/guides/", "/zh/guides/")
            return f'<meta property="og:url" content="{new_content}">'
        return m.group(0)
    new_zh = re.sub(r'<meta\s+property="og:url"\s+content="([^"]+)"\s*/?>', fix_og_url, new_zh)
    
    # Step 3: Add Chinese title and summary in hero section
    new_zh = add_cn_title_and_summary(new_zh, data["cn_h1"], data["cn_summary"])
    
    # Step 4: Add translations to TOC
    new_zh = add_translations_to_toc(new_zh, data.get("toc_translations", {}))
    
    # Step 5: Add translations to h2 and h3
    new_zh = add_h2_h3_translations(new_zh, data.get("h2_translations", {}), data.get("h3_translations", {}))
    
    # Step 6: Handle quick-preview-box / quick-summary
    new_zh = handle_quick_summary(new_zh, data.get("quick_summary_bullets", []))
    
    # Write the file
    write_file(zh_path, new_zh)
    print(f"  Done: {filename}")


def main():
    for filename in FILENAMES:
        if filename in FILE_DATA:
            process_file(filename, FILE_DATA[filename])
        else:
            print(f"\nWARNING: No data for {filename}, skipping.")
    
    print(f"\n{'='*60}")
    print("All 7 files processed!")


if __name__ == "__main__":
    main()
