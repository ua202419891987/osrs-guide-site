# PowerShell script to fix Chinese placeholders in all 15 files
param(
    [string]$BasePath = "C:\Users\Lenovo\osrs-guide-site\zh\guides"
)

$files = @(
    "osrs-money-making-beginner-2026.html",
    "osrs-money-making-fishing-2026.html",
    "osrs-money-making-no-skills-guide-2026.html",
    "osrs-money-making-summer-sweep-up-2026.html",
    "osrs-money-making-tier-list-2026.html",
    "osrs-money-making-under-1m-investment-2026.html",
    "osrs-money-making-zero-req-2026.html",
    "osrs-passive-money-making-offline.html",
    "osrs-quest-unlocked-money-methods-2026.html",
    "osrs-revenants-caves-guide-2026.html",
    "osrs-rune-dragons-money-guide-2026.html",
    "osrs-slayer-70-to-95-money-makers-2026.html",
    "osrs-slayer-low-level-money-makers-2026.html",
    "osrs-slayer-money-making-guide-2026.html",
    "osrs-vorkath-money-making-guide-2026.html"
)

# Build translation maps from CSV data
# Each line: pattern, english_text, chinese_text

$translations = @"

map,Quick Summary — All Methods by GP/hr,快速概览 — 按 GP/小时排序的所有方法
map,Your First 100K GP — Day 1 Starter Methods,你的第一个 10 万 GP — 首日起步方法
map,Best F2P Money Making Methods (Full Breakdown),最佳 F2P 赚钱方法（完整解析）
map,The F2P to P2P Transition — How to Get Your First Bond,从 F2P 到 P2P 的过渡 — 如何获得第一张绑定券
map,Early P2P Money Making (First Month as Member),早期 P2P 赚钱（成为会员的第一个月）
map,Passive Income Methods — Herb Runs & Birdhouses,被动收入方法 — 草药种植与鸟屋
map,Advanced Active Money Makers (Mid-Game),高级主动赚钱方法（中期）
map,Money Making FAQs,赚钱常见问题
map,Final Tips — Build Wealth Faster,最终提示 — 更快积累财富
map,1. Fishing Profit Comparison (All Levels),1. 钓鱼收益对比（全等级）
map,2. Low Level Methods (1-50): Getting Started,2. 低级方法（1-50）：入门
map,3. Mid-Level Methods (50-70): Monkfish & Karambwans,3. 中级方法（50-70）：僧侣鱼与卡拉姆万鱼
map,4. High-Level Methods (70-99): Premium Profit,4. 高级方法（70-99）：高端收益
map,5. Gear & Inventory for Fishing Money Making,5. 钓鱼赚钱的装备与背包配置
map,6. Common Mistakes & Pro Tips,6. 常见错误与专业技巧
map,7. Frequently Asked Questions,7. 常见问题
map,🎣 Fishing — The Ultimate AFK Income,🎣 钓鱼 — 终极挂机收入
map,How Zero-Requirement Money Making Works,零需求赚钱方法的原理
map,F2P Zero-Requirement Methods (Ranked),F2P 零需求方法（排名）
map,P2P Zero-Requirement Methods (Ranked),P2P 零需求方法（排名）
map,Top 6 Methods Compared,前 6 种方法对比
map,Zero to First Million: Step-by-Step,从零到第一个百万：逐步指南
map,Methods That Need Zero GP to Start,需要零 GP 起步的方法
map,Hidden Gem Methods Most Guides Miss,大多数攻略遗漏的隐藏宝藏方法
map,Money Making No Skills FAQs,零技能赚钱常见问题
map,How This Tier List Works,梯级排名说明
map,S Tier — 8M+ GP/hr (End-Game),S 级 — 每小时 800 万+ GP（终局）
map,A Tier — 3-8M GP/hr (Daily Grind),A 级 — 每小时 300-800 万 GP（日常刷金）
map,B Tier — 1-3M GP/hr (Mid-Game),B 级 — 每小时 100-300 万 GP（中期）
map,C Tier — 1.8M-1M GP/hr (Low-Mid),C 级 — 每小时 18 万-100 万 GP（低中期）
map,D Tier — 400-1.8M GP/hr (Beginner),D 级 — 每小时 40 万-18 万 GP（新手）
map,Meta Shifts — July 2026 Changes,版本变迁 — 2026 年 7 月改动
map,FAQ,常见问题
map,Flipping Myth: You Need Millions to Start,倒卖误区：你需要数百万才能开始
map,Getting Started — The 100K Setup,入门指南 — 10 万 GP 配置
map,Best Items for Small-Capital Flips,小本金倒卖的最佳物品
map,Margin Checking — The Most Important Skill,差价检查 — 最重要的技能
map,Risk Management for Small Accounts,小账号的风险管理
map,Daily Routine — 10 Minutes a Day Plan,日常流程 — 每天 10 分钟计划
map,From 1M to 5M — Scaling Up,从 100 万到 500 万 — 逐步扩大
map,Common Beginner Mistakes,新手常见错误
map,Quick Reference & FAQ,快速参考与常见问题
map,All Methods Comparison Table,所有方法对比表
map,Getting Your First 10K GP,赚取你的第一个 1 万 GP
map,Collection Methods — Gather Items from the World,收集方法 — 从世界中收集物品
map,Pickup Methods — Loot What Others Leave Behind,拾取方法 — 拾取他人遗留物品
map,Exchange Methods — Buy Low, Sell High (Arbitrage),交易方法 — 低买高卖（套利）
map,Zero-to-Bond Complete Roadmap,从零到绑定券完整路线图
map,Zero Requirement Money Making FAQs,零要求赚钱常见问题
map,Final Tips — Scale Your Income,最终提示 — 扩大收入
map,Summer Sweep-Up 2026 — What Actually Changed,2026 夏日扫荡 — 真正发生了什么变化
map,F2P Money Making Post-Sweep-Up,扫荡后的 F2P 赚钱方法
map,Low-Level Member Methods (Combat 30-60),低级会员方法（战斗等级 30-60）
map,Mid-Level Methods (Combat 60-80),中级方法（战斗等级 60-80）
map,High-Level / Endgame Updates,高级/终局更新
map,Method Comparison: Before vs After Sweep-Up,方法对比：扫荡前后
map,What's Next — Predictions for Blood Moon Era,下一步 — 血月时代预测
map,🎯 Why Quests Pay: 6M GP/hr Unlocked,🎯 为什么任务值得做：解锁 600 万 GP/小时
map,📜 Top 10 Quests: Priority Ranking,📜 前 10 个任务：优先级排名
map,🐉 Dragon Slayer II: Vorkath 3M/hr,🐉 龙族杀手 II：韦克思 300 万/小时
map,🧚 Song of the Elves: CG 6M/hr,🧚 精灵之歌：腐蚀遗迹 600 万/小时
map,🧛 Sins of the Father: Sepulchre 2.5M/hr,🧛 父辈之罪：圣陵 250 万/小时
map,🔓 Other Quest Unlocks: 1.8M/hr,🔓 其他任务解锁：180 万/小时
map,🗺️ Completion Order: Phase 1-3,🗺️ 完成顺序：阶段 1-3
map,❓ FAQ,❓ 常见问题
map,① 📋 Requirements &amp; Preparations,① 📋 要求与准备
map,② 🗺️ Entrance Locations &amp; How to Get There,② 🗺️ 入口位置与如何到达
map,③ 👾 Revenant Types — Imp Through Dragon,③ 👾 亡灵类型 — 从小鬼到龙
map,④ 💎 Complete Drop Table (2026 Updated),④ 💎 完整掉落表（2026 更新）
map,⑤ 📊 GP Per Hour Analysis (1.8M-2M/hr),⑤ 📊 每小时 GP 分析（180 万-200 万/小时）
map,⑥ ⚔️ Recommended Gear &amp; Inventory,⑥ ⚔️ 推荐装备与背包
map,⑦ 🏃 Escape Strategies &amp; PK Awareness,⑦ 🏃 逃生策略与 PK 警觉
map,⑧ 🎯 Safe Spots &amp; Wilderness Agility Shortcuts,⑧ 🎯 安全点与荒野敏捷捷径
map,⑨ ❓ FAQ — Revenants Caves,⑨ ❓ 常见问题 — 亡灵洞穴
map,① Requirements — Dragon Slayer 2 & Stat Checks,① 要求 — 龙族杀手 2 与属性检查
map,② Gear Setups — Best Melee Builds (Hasta / Lance),② 装备配置 — 最佳近战搭配（长矛/龙枪）
map,③ Inventory & Supplies,③ 背包与补给
map,④ Rune Dragon Mechanics — Dragonfire, Shielding & Combat Switches,④ 符文龙机制 — 龙火、护盾与战斗切换
map,⑤ Loot Table & GP/hr Breakdown,⑤ 掉落表与 GP/小时分析
map,⑥ Strategies & Pro Tips for Maximum Profit,⑥ 策略与专业技巧最大化收益
map,⑦ FAQ — Rune Dragons Money Making,⑦ 常见问题 — 符文龙赚钱
map,Why 70-95 Is the Golden Range,为什么 70-95 级是黄金区间
map,Which Slayer Master at Each Level,各等级选择哪个 Slayer 大师
map,Task GP/hr Ranking — 70-95,任务 GP/小时排名 — 70-95
map,Optimal Block List (Minimum 4, Maximum 6 Slots),最佳屏蔽列表（最少 4 个，最多 6 个槽位）
map,Which Tasks to Extend,哪些任务需要扩展
map,Slayer Boss Unlocks and When to Do Them,Slayer Boss 解锁及何时击杀
map,Gear Setup Per Task Type,各任务类型的装备配置
map,Final Tips,最终提示
map,Why Slayer = Best Early Money Making,为什么 Slayer = 最佳早期赚钱方式
map,Top 10 Money-Making Tasks (Combat 30-60),前 10 个赚钱任务（战斗等级 30-60）
map,Task-by-Task Strategy Guide,逐个任务策略指南
map,Gear on a Budget (30-60 Combat),预算装备（战斗等级 30-60）
map,Maximizing Profit Per Task,最大化每个任务的利润
map,Tasks to Avoid (Money Losers),需要避免的任务（亏钱）
map,Slayer Money Making FAQs,Slayer 赚钱常见问题
map,🎯 Why Slayer Pays (1.8M-4M GP/hr),🎯 为什么 Slayer 能赚钱（180 万-400 万 GP/小时）
map,💰 Best Slayer Master for Profit,💰 最佳赚钱 Slayer 大师
map,📊 Top 15 Tasks (S/A/B Tier),📊 前 15 个任务（S/A/B 级）
map,🛡️ Block/Skip List (6 Slots),🛡️ 屏蔽/跳过列表（6 个槽位）
map,⚔️ Gear Setups (Budget → Max),⚔️ 装备配置（预算 → 顶级）
map,🔥 Task-Specific Guides (5 Methods),🔥 特定任务指南（5 种方法）
map,⚖️ XP vs GP: When to Prioritize,⚖️ 经验 vs 金币：何时优先选择
map,❓ FAQ + Pro Tips,❓ 常见问题 + 专业技巧
map,Requirements &amp; Recommendations,要求与建议
map,Gear Setups by Budget,按预算的装备配置
map,Inventory &amp; Supplies,背包与补给
map,Boss Mechanics &amp; Strategies,Boss 机制与策略
map,Advanced: The Woox Walk,进阶：Woox 走位法
map,Loot Table &amp; GP Analysis,掉落表与 GP 分析
map,Budget-Friendly Strategies,预算友好策略
map,1. Managing Miscellania — Best Overall Passive Income,1. 管理 Miscellania — 最佳整体被动收入
map,2. Herb Farming Runs — 5 Minutes Every 80 Minutes,2. 草药种植 — 每 80 分钟 5 分钟
map,3. Birdhouse Trapping on Fossil Island,3. 化石岛鸟屋陷阱
map,4. GE Flipping While Offline,4. 离线 GE 倒卖
map,5. The Daily 10-Minute Routine,5. 每天 10 分钟日常流程
map,6. Common Mistakes With Passive Income,6. 被动收入的常见错误
map,💰 Compound Your Wealth Passively,💰 被动复利积累财富
h2,1. Your First 100K GP — Day 1 Starter Methods,1. 你的第一个 10 万 GP — 首日起步方法
h2,2. Best F2P Money Making Methods (Full Breakdown),2. 最佳 F2P 赚钱方法（完整解析）
h2,3. The F2P to P2P Transition — Getting Your First Bond,3. 从 F2P 到 P2P 的过渡 — 获得你的第一张绑定券
h2,4. Early P2P Money Making (First Month as Member),4. 早期 P2P 赚钱（成为会员的第一个月）
h2,5. Passive Income Methods — Herb Runs & Birdhouses,5. 被动收入方法 — 草药种植与鸟屋
h2,6. Advanced Active Money Makers (Mid-Game),6. 高级主动赚钱方法（中期）
h2,7. Money Making FAQs,7. 赚钱常见问题
h2,8. Final Tips — Build Wealth Faster,8. 最终提示 — 更快积累财富
h2,1. Fishing Profit Comparison (All Levels),1. 钓鱼收益对比（全等级）
h2,2. Low Level Methods (1-50): Getting Started,2. 低级方法（1-50）：入门
h2,3. Mid-Level Methods (50-70): Monkfish & Karambwans,3. 中级方法（50-70）：僧侣鱼与卡拉姆万鱼
h2,4. High-Level Methods (70-99): Premium Profit,4. 高级方法（70-99）：高端收益
h2,5. Gear & Inventory for Fishing Money Making,5. 钓鱼赚钱的装备与背包配置
h2,6. Common Mistakes & Pro Tips,6. 常见错误与专业技巧
h2,🎣 Fishing — The Ultimate AFK Income,🎣 钓鱼 — 终极挂机收入
h2,1. How Zero-Requirement Money Making Works,1. 零需求赚钱方法的原理
h2,2. F2P Zero-Requirement Methods (Ranked),2. F2P 零需求方法（排名）
h2,3. P2P Zero-Requirement Methods (Ranked),3. P2P 零需求方法（排名）
h2,4. Top 6 Methods Compared,4. 前 6 种方法对比
h2,5. Zero to First Million: Step-by-Step,5. 从零到第一个百万：逐步指南
h2,6. Methods That Need Zero GP to Start,6. 需要零 GP 起步的方法
h2,7. Hidden Gem Methods Most Guides Miss,7. 大多数攻略遗漏的隐藏宝藏方法
h2,8. Money Making No Skills FAQs,8. 零技能赚钱常见问题
h2,How This Tier List Works,梯级排名说明
h2,S Tier — 8M+ GP/hr (End-Game Dominance),S 级 — 每小时 800 万+ GP（终局统治）
h2,A Tier — 3-8M GP/hr (Your Daily Money Printer),A 级 — 每小时 300-800 万 GP（日常印钞机）
h2,B Tier — 1-3M GP/hr (Solid Mid-Game Money),B 级 — 每小时 100-300 万 GP（稳健中期收入）
h2,C Tier — 1.8M-1M GP/hr (Low-Mid Accounts),C 级 — 每小时 18 万-100 万 GP（低中期账号）
h2,D Tier — 1.8M-1.8M GP/hr (Starting Out),D 级 — 每小时 18 万-180 万 GP（起步阶段）
h2,Meta Shifts — June 2026 Changes That Affected Rankings,版本变迁 — 2026 年 6 月影响排名的改动
h2,Which Tier Should YOU Farm?,你应该刷哪个等级？
h2,FAQ — Money Making Tier List,常见问题 — 赚钱梯级排名
h2,1. Flipping Myth: "You Need Millions to Start",1. 倒卖误区："你需要数百万才能开始"
h2,2. Getting Started — The 100K Setup,2. 入门指南 — 10 万 GP 配置
h2,3. Best Items for Small-Capital Flips (By Budget Tier),3. 小本金倒卖的最佳物品（按预算等级）
h2,4. Margin Checking — The Most Important Skill,4. 差价检查 — 最重要的技能
h2,5. Risk Management for Small Accounts,5. 小账号的风险管理
h2,6. Daily Routine — 10 Minutes a Day Plan,6. 日常流程 — 每天 10 分钟计划
h2,7. From 1M to 5M — Scaling Up,7. 从 100 万到 500 万 — 逐步扩大
h2,8. Common Beginner Mistakes (And How to Avoid),8. 新手常见错误（以及如何避免）
h2,9. Quick Reference & FAQ,9. 快速参考与常见问题
h2,1. All Methods Comparison Table,1. 所有方法对比表
h2,2. Getting Your First 10K GP (15 Minutes),2. 赚取你的第一个 1 万 GP（15 分钟）
h2,3. Collection Methods — Gather Items from the World,3. 收集方法 — 从世界中收集物品
h2,4. Pickup Methods — Loot What Others Leave Behind,4. 拾取方法 — 拾取他人遗留物品
h2,5. Exchange Methods — Buy Low, Sell High (Arbitrage),5. 交易方法 — 低买高卖（套利）
h2,6. Zero-to-Bond Complete Roadmap,6. 从零到绑定券完整路线图
h2,7. Zero Requirement Money Making FAQs,7. 零要求赚钱常见问题
h2,8. Final Tips — Scale Your Income,8. 最终提示 — 扩大收入
h2,1. Summer Sweep-Up 2026 — What Actually Changed,1. 2026 夏日扫荡 — 真正发生了什么变化
h2,2. F2P Money Making Post-Sweep-Up,2. 扫荡后的 F2P 赚钱方法
h2,3. Low-Level Member Methods (Combat 30-60),3. 低级会员方法（战斗等级 30-60）
h2,4. Mid-Level Methods (Combat 60-80),4. 中级方法（战斗等级 60-80）
h2,5. High-Level / Endgame Updates,5. 高级/终局更新
h2,6. Method Comparison: Before vs After Sweep-Up,6. 方法对比：扫荡前后
h2,7. What's Next — Predictions for Blood Moon Era,7. 下一步 — 血月时代预测
h2,8. FAQ — Summer Sweep-Up Money Making,8. 常见问题 — 夏日扫荡赚钱
h2,1. Managing Miscellania — Best Overall Passive Income,1. 管理 Miscellania — 最佳整体被动收入
h2,2. Herb Farming Runs — 5 Minutes Every 80 Minutes,2. 草药种植 — 每 80 分钟 5 分钟
h2,3. Birdhouse Trapping on Fossil Island,3. 化石岛鸟屋陷阱
h2,4. GE Flipping While Offline,4. 离线 GE 倒卖
h2,5. The Daily 10-Minute Routine,5. 每天 10 分钟日常流程
h2,6. Common Mistakes With Passive Income,6. 被动收入的常见错误
h2,💰 Compound Your Wealth Passively,💰 被动复利积累财富
h2,🎯 Why Quests Pay: 6M GP/hr Unlocked,🎯 为什么任务值得做：解锁 600 万 GP/小时
h2,📜 Top 10 Quests: Priority Ranking (6M GP/hr),📜 前 10 个任务：优先级排名（600 万 GP/小时）
h2,🐉 Dragon Slayer II: Vorkath 3M/hr (Full Guide),🐉 龙族杀手 II：韦克思 300 万/小时（完整指南）
h2,🧚 Song of the Elves: CG 6M/hr + Zalcano (Full Guide),🧚 精灵之歌：腐蚀遗迹 600 万/小时 + 萨尔卡诺（完整指南）
h2,🧛 Sins of the Father: Sepulchre 2.5M/hr + Vyrewatch,🧛 父辈之罪：圣陵 250 万/小时 + 维瑞瓦奇
h2,🔓 Other Quest Unlocks: 1.8M/hr (Bone Voyage + Cabin Fever),🔓 其他任务解锁：180 万/小时（远航 + 船舱热）
h2,🗺️ Completion Order: Phase 1-3 (Quest Roadmap),🗺️ 完成顺序：阶段 1-3（任务路线图）
h2,❓ FAQ — Quest Money Making Questions,❓ 常见问题 — 任务赚钱问题
h2,① 📋 Requirements &amp; Preparations,① 📋 要求与准备
h2,② 🗺️ Entrance Locations &amp; How to Get There,② 🗺️ 入口位置与如何到达
h2,③ 👾 Revenant Types — Imp Through Dragon,③ 👾 亡灵类型 — 从小鬼到龙
h2,④ 💎 Complete Drop Table (2026 Updated),④ 💎 完整掉落表（2026 更新）
h2,⑤ 📊 GP Per Hour Analysis (1.8M-2M/hr),⑤ 📊 每小时 GP 分析（180 万-200 万/小时）
h2,⑥ ⚔️ Recommended Gear &amp; Inventory,⑥ ⚔️ 推荐装备与背包
h2,⑦ 🏃 Escape Strategies &amp; PK Awareness,⑦ 🏃 逃生策略与 PK 警觉
h2,① Requirements — Dragon Slayer 2 & Stat Checks,① 要求 — 龙族杀手 2 与属性检查
h2,② Gear Setups — Best Melee Builds (Hasta / Lance),② 装备配置 — 最佳近战搭配（长矛/龙枪）
h2,③ Inventory & Supplies,③ 背包与补给
h2,④ Rune Dragon Mechanics — Dragonfire, Shielding & Combat Switches,④ 符文龙机制 — 龙火、护盾与战斗切换
h2,⑤ Loot Table & GP/hr Breakdown,⑤ 掉落表与 GP/小时分析
h2,⑥ Strategies & Pro Tips for Maximum Profit,⑥ 策略与专业技巧最大化收益
h2,⑦ FAQ — Rune Dragons Money Making,⑦ 常见问题 — 符文龙赚钱
h2,Why 70-95 Is the Golden Range,为什么 70-95 级是黄金区间
h2,Which Slayer Master at Each Level,各等级选择哪个 Slayer 大师
h2,Task GP/hr Ranking — 70-95,任务 GP/小时排名 — 70-95
h2,Optimal Block List (Minimum 4, Maximum 6 Slots),最佳屏蔽列表（最少 4 个，最多 6 个槽位）
h2,Which Tasks to Extend,哪些任务需要扩展
h2,Slayer Boss Unlocks and When to Do Them,Slayer Boss 解锁及何时击杀
h2,Gear Setup Per Task Type,各任务类型的装备配置
h2,FAQ,常见问题
h2,Final Tips,最终提示
h2,1. Why Slayer = Best Early Money Making,1. 为什么 Slayer = 最佳早期赚钱方式
h2,2. Top 10 Money-Making Tasks (Combat 30-60),2. 前 10 个赚钱任务（战斗等级 30-60）
h2,3. Task-by-Task Strategy Guide,3. 逐个任务策略指南
h2,4. Gear on a Budget (Combat 30-60),4. 预算装备（战斗等级 30-60）
h2,5. Maximizing Profit Per Task,5. 最大化每个任务的利润
h2,6. Tasks to Avoid (Money Losers),6. 需要避免的任务（亏钱）
h2,7. Slayer Money Making FAQs,7. Slayer 赚钱常见问题
h2,🎯 Why Slayer Is the Best Money Maker: 1.8M-4M GP/hr,🎯 为什么 Slayer 是最好的赚钱方式：180 万-400 万 GP/小时
h2,💰 Slayer Master Selection: Duradel = Best Profit,💰 Slayer 大师选择：Duradel = 最佳收益
h2,📊 Top 15 Most Profitable Slayer Tasks — 2026 Tier List,📊 前 15 个最赚钱的 Slayer 任务 — 2026 梯级排名
h2,🛡️ Slayer Block/Skip List: What to Block & Why,🛡️ Slayer 屏蔽/跳过列表：屏蔽什么及原因
h2,⚔️ Gear Setups Per Task Type (Budget → Max),⚔️ 各任务类型的装备配置（预算 → 顶级）
h2,🔥 Task-Specific Money Guides (Step-by-Step),🔥 特定任务赚钱指南（逐步）
h2,⚖️ Slayer XP vs GP: When to Prioritize Which,⚖️ Slayer 经验 vs 金币：何时优先选择
h2,❓ FAQ + Pro Tips,❓ 常见问题 + 专业技巧
h2,① Requirements &amp; Recommendations,① 要求与建议
h2,② Gear Setups by Budget,② 按预算的装备配置
h2,③ Inventory &amp; Supplies,③ 背包与补给
h2,④ Boss Mechanics &amp; Strategies,④ Boss 机制与策略
h2,⑤ Advanced: The Woox Walk,⑤ 进阶：Woox 走位法
h2,⑥ Loot Table &amp; GP Analysis,⑥ 掉落表与 GP 分析
h2,⑦ Budget-Friendly Strategies,⑦ 预算友好策略
h2,❓ Frequently Asked Questions,❓ 常见问题
h3,① Stronghold of Security — 10K GP (15 Minutes),① 安全堡垒 — 1 万 GP（15 分钟）
h3,② Cowhide Tanning — 15K–25K GP/hr,② 牛皮鞣制 — 1.5 万–2.5 万 GP/小时
h3,③ Mining Iron Ore — 30K–50K GP/hr,③ 挖掘铁矿石 — 3 万–5 万 GP/小时
h3,🏆 Best F2P Method: Wine of Zamorak (100K–1.8M GP/hr),🏆 最佳 F2P 方法：萨莫拉克酒（10 万–180 万 GP/小时）
h3,💪 Ogress Warriors — Best F2P Combat Money,💪 食人魔战士 — 最佳 F2P 战斗赚钱
h3,🎯 Bond Roadmap: 0 → 12.8M GP,🎯 绑定券路线图：0 → 1280 万 GP
h3,⚒️ Blast Furnace — 1.8M–700K GP/hr (Active),⚒️ 高炉炼钢 — 18 万–70 万 GP/小时（主动）
h3,✨ High Alchemy — 100K–1.8M GP/hr + Magic XP,✨ 高等级炼金术 — 10 万–180 万 GP/小时 + 魔法经验
h3,🌿 Herb Runs — 100K–1.8M+ GP per Run (80 min cycle),🌿 草药种植 — 每次 10 万–180 万+ GP（80 分钟周期）
h3,🐦 Birdhouse Runs — 10K–30K GP per Run (50 min cycle),🐦 鸟屋跑图 — 每次 1 万–3 万 GP（50 分钟周期）
h3,🌾 Giant Seaweed — 50K–100K GP per Run (70 min cycle),🌾 巨海藻 — 每次 5 万–10 万 GP（70 分钟周期）
h3,⚔️ Slayer (70+) — 1.8M–1.8M GP/hr,⚔️ 杀戮（70+） — 18 万–180 万 GP/小时
h3,🐍 Zulrah — 1.8M–3M GP/hr,🐍 祖拉 — 18 万–300 万 GP/小时
h3,🐉 Vorkath — 2M–4M GP/hr,🐉 韦克思 — 200 万–400 万 GP/小时
h3,🎯 What To Do After This Guide,🎯 阅读本指南后的行动建议
h3,🎣 Fishing Profit — Quick Reference,🎣 钓鱼收益 — 快速参考
h3,Lobsters at Musa Point (Level 40) — First Profitable Fish,穆萨角钓龙虾（40 级） — 第一种赚钱鱼
h3,Swordfish + Tuna (Level 50),剑鱼 + 金枪鱼（50 级）
h3,Monkfish (Level 62 — Swan Song Quest Required),僧侣鱼（62 级 — 需要天鹅之歌任务）
h3,Karambwans (Level 65 — Best Mid-Level Profit),卡拉姆万鱼（65 级 — 最佳中级收益）
h3,Infernal Eels (Level 80) — Best AFK Money Maker,地狱鳗鱼（80 级） — 最佳挂机赚钱
h3,Minnows → Sharks (Level 82) — Highest GP/Hour,小鱼 → 鲨鱼（82 级） — 最高 GP/小时
h3,📚 Related Guides,📚 相关指南
h3,① F2P Route (0 to 1M GP in ~4-5 hours),① F2P 路线（0 到 100 万 GP 约 4-5 小时）
h3,② P2P Route (0 to 1M GP in ~2-3 hours),② P2P 路线（0 到 100 万 GP 约 2-3 小时）
h3,① Collecting Desert Goat Horns (P2P, 150K-1.8M/hr),① 收集沙漠山羊角（P2P，15 万-180 万/小时）
h3,② Picking Potato Cactus (P2P, 120K-180K/hr),② 采摘土豆仙人掌（P2P，12 万-18 万/小时）
h3,③ Collecting Snape Grass (P2P, 60K-90K/hr),③ 收集斯内普草（P2P，6 万-9 万/小时）
h3,④ Reselling from Ogre Shop (F2P, 50K-80K/hr),④ 从食人魔商店转卖（F2P，5 万-8 万/小时）
h3,🎯 After You've Made Your First GP,🎯 赚取第一笔 GP 之后
h3,🥇 Theatre of Blood (Hard Mode) S,🥇 鲜血剧院（困难模式）S 级
h3,🥈 Tombs of Amascut (Expert 400+) S,🥈 阿玛斯库特之墓（专家 400+）S 级
h3,🥉 Chambers of Xeric (Challenge Mode) S,🥉 塞里克密室（挑战模式）S 级
h3,🔥 Corrupted Gauntlet A ⬆️ NEWLY BUFFED,🔥 腐蚀遗迹 A 级 ⬆️ 新增强化
h3,💀 Phantom Muspah A,💀 幻影穆斯帕 A 级
h3,🐉 Vorkath (Dragon Hunter Crossbow) A,🐉 韦克思（龙猎弩）A 级
h3,🐍 Zulrah A ⬆️ BUFFED,🐍 祖拉 A 级 ⬆️ 增强
h3,👹 Demonic Gorillas A,👹 恶魔大猩猩 A 级
h3,🏰 Hallowed Sepulchre (Floor 5) B,🏰 圣陵（第 5 层）B 级
h3,⚔️ Slayer (85+) B,⚔️ 杀戮（85+）B 级
h3,⛏️ Zalcano B,⛏️ 萨尔卡诺 B 级
h3,🌿 Herb Runs (Passive) B,🌿 草药种植（被动）B 级
h3,🌊 Tempoross B,🌊 坦波罗罗斯 B 级
h3,💀 Barrows C,💀 巴罗斯 C 级
h3,🔥 Blast Furnace C,🔥 高炉炼钢 C 级
h3,🐉 Green Dragons (Myths' Guild) C,🐉 绿龙（神话公会）C 级
h3,🗡️ Gargoyles (75 Slayer) C,🗡️ 石像鬼（75 杀戮）C 级
h3,🐮 Cowhide Tanning D,🐮 牛皮鞣制 D 级
h3,🪙 High Alchemy (Profitable Items) D,🪙 高等级炼金术（盈利物品）D 级
h3,🎣 Fishing (Lobsters / Swordfish) D,🎣 钓鱼（龙虾/剑鱼）D 级
h3,📊 What Changed and Why,📊 变化内容及原因
h3,Q: Why isn't Nightmare on this list?,问：为什么梦魇不在列表中？
h3,Q: What's the best AFK money maker?,问：最佳挂机赚钱方法是什么？
h3,Q: I have 50M GP. Should I buy gear or flip?,问：我有 5000 万 GP。应该买装备还是倒卖？
h3,Q: Is Corrupted Gauntlet really better than Vorkath now?,问：腐蚀遗迹现在真的比韦克思好吗？
h3,💰 Top Money Guides,💰 顶级赚钱指南
h3,📊 Quick Reference,📊 快速参考
h3,📅 July 2026 Updates,📅 2026 年 7 月更新
h3,Small Capital vs Large Capital Flipping,小本金与大本金倒卖对比
h3,The Math: How 100K GP Can Become 1M GP,计算：10 万 GP 如何变成 100 万 GP
h3,How to Get Your First 100K GP,如何赚取第一个 10 万 GP
h3,Flipping Basics: How It Works,倒卖基础：运作原理
h3,Tier 1: 100K-1.8M GP Capital,第一档：10 万-18 万 GP 本金
h3,Tier 2: 1.8M-1.5M GP Capital,第二档：18 万-150 万 GP 本金
h3,Tier 3: 1.5M-1M GP Capital,第三档：150 万-1000 万 GP 本金
h3,What Is Margin Checking?,什么是差价检查？
h3,How to Check Margins Accurately,如何准确检查差价
h3,Rule 1: Never Invest More Than 20% of Your Capital in One Flip,规则 1：永远不要在一次倒卖中投入超过 20% 的本金
h3,Rule 2: Set a Time Limit (Cut Losses Early),规则 2：设定时间限制（及早止损）
h3,Rule 3: Diversify (Don't Put All GP in One Item),规则 3：分散投资（不要把所有 GP 投在一个物品上）
h3,Rule 4: Track Your Flips,规则 4：记录你的倒卖
h3,Sample Daily Schedule (10 Minutes Active Time),示例日程安排（10 分钟活跃时间）
h3,Combining Flipping with Other OSRS Activities,将倒卖与其他 OSRS 活动结合
h3,When to Change Your Strategy,何时改变策略
h3,New Opportunities at 1M+ GP Capital,100 万+ GP 本金的新机会
h3,Quick Reference Tables,快速参考表
h3,What To Do After Reading This Guide,阅读本指南后的行动建议
h3,📍 Stronghold of Security — 10,000 GP Free,📍 安全堡垒 — 免费 1 万 GP
h3,📍 Alternative: Pickpocket Men in Lumbridge,📍 替代方法：在卢姆布里奇扒窃路人
h3,🐄 Cowhide Collecting (Lumbridge) — 40K–60K GP/hr,🐄 收集牛皮（卢姆布里奇） — 4 万–6 万 GP/小时
h3,🍌 Banana Picking (Karamja) — 20K–30K GP/hr,🍌 采摘香蕉（卡拉马贾） — 2 万–3 万 GP/小时
h3,🌾 Flax Picking (Seers' Village) — 25K–40K GP/hr,🌾 采摘亚麻（先知村） — 2.5 万–4 万 GP/小时
h3,⚔️ Wilderness Ditch Looting (Edgeville) — 50K–1.8M+ GP/hr,⚔️ 荒野沟渠拾荒（埃奇维尔） — 5 万–180 万+ GP/小时
h3,🦴 Wilderness Bone Yard — 80K–120K GP/hr,🦴 荒野骨场 — 8 万–12 万 GP/小时
h3,💀 Graveyard of Shadows (Level 15 Wilderness),💀 暗影墓地（荒野 15 级）
h3,🔄 Shop-to-GE Arbitrage — 30K–100K+ GP/hr,🔄 商店到 GE 套利 — 3 万–10 万+ GP/小时
h3,📈 Grand Exchange Flipping — 10K–50K+ GP/hr (scales with capital),📈 GE 倒卖 — 1 万–5 万+ GP/小时（随本金增长）
h3,📊 Major Balance Changes Overview,📊 主要平衡性变更概览
h3,🔴 Heavily Nerfed Methods (Avoid These Now),🔴 严重削弱的方法（现在避免这些）
h3,🟢 Buffed Methods (Now More Profitable),🟢 增强的方法（现在更赚钱）
h3,✨ Brand New Money Making Methods (Post-Sweep-Up Only),✨ 全新的赚钱方法（仅扫荡后）
h3,🏆 Top 10 F2P Methods (Post-Sweep-Up Rankings),🏆 前 10 个 F2P 方法（扫荡后排名）
h3,Method Spotlight: Cowhide Collection (Still #1 for F2P),方法聚焦：收集牛皮（F2P 仍排第一）
h3,F2P Method: Iron Ore Mining (East Varrock),F2P 方法：挖掘铁矿石（东瓦洛克）
h3,🏆 Top 10 Low-Level Member Methods (Updated Rankings),🏆 前 10 个低级会员方法（更新排名）
h3,🆕 Newly Viable: Chaos Druids (Taverley Dungeon),🆕 新可行：混沌德鲁伊（塔弗利地牢）
h3,Method Spotlight: Wine of Zamorak (Non-Combat Option),方法聚焦：萨莫拉克酒（非战斗方案）
h3,🆕 Overlooked Method: Astral Runecrafting (Post-Sweep-Up Buff),🆕 被忽视的方法：星界符文制作（扫荡后增强）
h3,🏆 Top 10 Mid-Level Methods (Updated Rankings),🏆 前 10 个中级方法（更新排名）
h3,Method Spotlight: Barrows (Biggest Nerf Survivor → Now Buffed!),方法聚焦：巴罗斯（最大削弱幸存者 → 现在增强了！）
h3,🆕 New Method: Fortis Colosseum (Medium Difficulty),🆕 新方法：福尔蒂斯竞技场（中等难度）
h3,🏆 Top 10 High-Level Methods (Updated Rankings),🏆 前 10 个高级方法（更新排名）
h3,Method Spotlight: Vorkath (Now #1 GP/Hour),方法聚焦：韦克思（现在 GP/小时排第一）
h3,🆕 New High-Level Method: Chambers of Xeric (Post-Sweep-Up Changes),🆕 新高级方法：塞里克密室（扫荡后变化）
h3,📊 GP/Hour Comparison Table,📊 GP/小时对比表
h3,📈 What This Means for Your Money Making Strategy,📈 这对你的赚钱策略意味着什么
h3,🌑 What Is the Blood Moon Era?,🌑 什么是血月时代？
h3,💰 How to Prepare for the Blood Moon Era,💰 如何为血月时代做准备
h3,😴 Passive Income — Quick Reference,😴 被动收入 — 快速参考
h3,Setup Steps:,设置步骤：
h3,Optimal Herb Run Route (5 Patches):,最佳草药种植路线（5 块地）：
h3,Offline Flipping Routine:,离线倒卖流程：
h3,📊 Quest Rewards vs. Quest Unlocks,📊 任务奖励 vs 任务解锁
h3,📉 The Opportunity Cost of Not Questing,📉 不做任务的机会成本
h3,⚡ Quick Wins vs. Long-Term Investments,⚡ 快速收益 vs 长期投资
h3,🐉 Why Vorkath Is the Best Quest-Unlocked Money Maker,🐉 为什么韦克思是最佳任务解锁赚钱方式
h3,⚔️ Vorkath Gear Setup Tiers,⚔️ 韦克思装备配置等级
h3,🎒 Vorkath Inventory Setup,🎒 韦克思背包配置
h3,⚔️ Vorkath Kill Mechanics (Quick Reference),⚔️ 韦克思击杀机制（快速参考）
h3,🏟️ Corrupted Gauntlet (3M-6M GP/hr),🏟️ 腐蚀遗迹（300 万-600 万 GP/小时）
h3,🎯 Corrupted Gauntlet Strategy,🎯 腐蚀遗迹策略
h3,⛏️ Zalcano (3M-2.5M GP/hr),⛏️ 萨尔卡诺（300 万-250 万 GP/小时）
h3,🏃 Hallowed Sepulchre (1M-2.5M GP/hr),🏃 圣陵（100 万-250 万 GP/小时）
h3,🎯 Hallowed Sepulchre Strategy,🎯 圣陵策略
h3,🧛 Vyrewatch Sentinels (1.8M-1.8M GP/hr),🧛 维瑞瓦奇哨兵（18 万-180 万 GP/小时）
h3,🐦 Bone Voyage — Birdhouse Runs (1.8M-1.5M GP/day),🐦 远航 — 鸟屋跑图（180 万-150 万 GP/天）
h3,🍄 Fairytale II — Fairy Rings (Farm Run Efficiency),🍄 童话 II — 妖精环（农场跑效率）
h3,👻 Cabin Fever — Cave Horrors (1.8M-1.8M GP/hr),👻 船舱热 — 洞穴恐怖（18 万-180 万 GP/小时）
h3,1️⃣ Phase 1: Foundation (First Week — ~15 QP),1️⃣ 阶段 1：基础（第一周 — 约 15 任务点）
h3,2️⃣ Phase 2: Mid-Game Unlocks (Weeks 2-4),2️⃣ 阶段 2：中期解锁（第 2-4 周）
h3,3️⃣ Phase 3: Major Unlocks (Month 2+),3️⃣ 阶段 3：重大解锁（第 2 个月+）
h3,📋 Quest Progression Route (Condensed Checklist),📋 任务推进路线（精简清单）
h3,① Minimum Requirements,① 最低要求
h3,① Recommended Items Checklist,① 推荐物品清单
h3,① Recommended Stats for Different Tiers,① 不同等级推荐属性
h3,① The Main Entrances (All 4 Locations),① 主要入口（全部 4 个位置）
h3,① Best Route for Each Setup,① 每种配置的最佳路线
h3,① Revenant Hierarchy (Difficulty & Value),① 亡灵等级（难度与价值）
h3,① Which Revenants Should You Kill?,① 应该击杀哪些亡灵？
h3,① Revenant Dragon — The Boss of the Caves,① 亡灵龙 — 洞穴 Boss
h3,① Ancient Artefacts (The "Big Ticket" Drops),① 远古神器（"大奖"掉落）
h3,① Secondary Drops (Common),① 次级掉落（常见）
h3,① Rare Weapon Drops,① 稀有武器掉落
h3,① Budget Setup: 1.8M-1.8M GP/hr,① 预算配置：18 万-180 万 GP/小时
h3,① Mid-Tier Setup: 1.8M-3M GP/hr,① 中级配置：18 万-300 万 GP/小时
h3,① High-End Setup: 3M-2.5M GP/hr,① 高端配置：300 万-250 万 GP/小时
h3,⚡ GP/hr Verdict,⚡ GP/小时结论
h3,① Budget Setup (~1.8M Risk),① 预算配置（约 18 万 GP 风险）
h3,① Mid-Tier Setup (~1.8M-700K Risk),① 中级配置（约 18 万-70 万 GP 风险）
h3,① High-End / BiS Setup (~10M-30M Risk),① 高端/顶级配置（约 1000 万-3000 万 GP 风险）
h3,① Inventory Setup,① 背包配置
h3,① Detecting PKers Early,① 早期发现 PK 玩家
h3,① Escape Routes — 3 Proven Methods,① 逃生路线 — 3 种经过验证的方法
h3,① Fighting Back — Anti-PK Setup,① 反击 — 反 PK 配置
h3,① Safe Spots Strategy,① 安全点策略
h3,① Wilderness Agility Shortcuts,① 荒野敏捷捷径
h3,📜 Dragon Slayer 2 — Quest Requirements,📜 龙族杀手 2 — 任务要求
h3,🗝️ Accessing the Lithkirk Vault (Post-Quest),🗝️ 进入利斯卡克宝库（任务后）
h3,📊 Recommended Stats for Farming,📊 推荐的刷怪属性
h3,⚔️ Best Stab Weapons Ranked,⚔️ 最佳刺击武器排名
h3,🛡️ Budget Setup (~2M Total),🛡️ 预算配置（约 200 万 GP 总计）
h3,💰 High-End Setup (~150M+),💰 高端配置（约 1.5 亿+）
h3,🔄 Weapon Switch Option: Dragon Claws,🔄 武器切换选项：龙爪
h3,📦 Standard Inventory Setup,📦 标准背包配置
h3,🔁 Trip Rotation Strategy,🔁 行程轮换策略
h3,💰 Looting Bag Strategy,💰 战利品袋策略
h3,🔥 Dragonfire Attacks (Two Types),🔥 龙火攻击（两种类型）
h3,🛡️ Shielding Phase (The "Shell" Mechanic),🛡️ 护盾阶段（"外壳"机制）
h3,🔁 Combat Style Switches,🔁 战斗风格切换
h3,💰 Main Loot Table — Consistent Drops,💰 主要掉落表 — 稳定掉落
h3,💎 Rare Drops — The Big Ticket Items,💎 稀有掉落 — 大件物品
h3,🧮 GP/hr Calculation (June 2026),🧮 GP/小时计算（2026 年 6 月）
h3,⭐ 5 Pro Strategies to Boost Your GP/hr,⭐ 提升 GP/小时的 5 个专业策略
h3,📊 Comparison: Rune Dragons vs Other Money Makers,📊 对比：符文龙与其他赚钱方式
h3,S-Tier Tasks (1M+ GP/hr — Always Do),S 级任务（100 万+ GP/小时 — 务必完成）
h3,A-Tier Tasks (1.5M-1M GP/hr — Extend All),A 级任务（15 万-100 万 GP/小时 — 全部扩展）
h3,B-Tier Tasks (1.8M-1.5M GP/hr — Do, Don't Extend),B 级任务（18 万-15 万 GP/小时 — 做但不扩展）
h3,Block These (in priority order):,屏蔽这些（按优先级顺序）：
h3,Always Skip These (using points, not block slots):,始终跳过这些（使用点数，不使用屏蔽槽位）：
h3,Melee Tasks (Gargoyles, Wyverns, Kurasks, Bloodvelds),近战任务（石像鬼、飞龙、库拉斯克、血精灵）
h3,Bursting/Barraging Tasks (Nechryael, Dust Devils, Abyssal Demons, Smoke Devils),爆破/弹幕任务（尼查尔、沙尘恶魔、深渊恶魔、烟雾恶魔）
h3,Ready to Print GP With Slayer?,准备好用 Slayer 赚取 GP 了吗？
h3,📊 Slayer vs. Other Money Making Methods (Combat 30-60),📊 Slayer 与其他赚钱方式对比（战斗等级 30-60）
h3,💰 The Slayer Advantage Breakdown,💰 Slayer 优势解析
h3,💰 Realistic GP Expectations for Low-Level Slayer,💰 低级 Slayer 的合理 GP 预期
h3,💡 The "Lucky Hour" Factor,💡 "幸运时刻"因素
h3,🎯 Strategy Deep-Dive: Hill Giants (The Beginner's Goldmine),🎯 策略深入：山丘巨人（新手金矿）
h3,🎯 Strategy Deep-Dive: Banshees (Efficient Herb Farming),🎯 策略深入：女妖（高效草药采集）
h3,🎯 Strategy Deep-Dive: Cave Bugs (Caviar Farming),🎯 策略深入：洞穴虫子（鱼子酱采集）
h3,🎯 Strategy Deep-Dive: Lesser Demons (Rune Item Farming),🎯 策略深入：低级恶魔（符文物品采集）
h3,🎯 Strategy Deep-Dive: Kalphites (Risk vs. Reward),🎯 策略深入：卡尔菲特（风险 vs 回报）
h3,💰 Tier 1: Ultra Budget (0–100K GP Total),💰 第一档：超低预算（总计 0-10 万 GP）
h3,💰 Tier 2: Entry P2P (100K–1.8M GP Total),💰 第二档：入门 P2P（总计 10 万-18 万 GP）
h3,💰 Tier 3: Mid-Game (1.8M–2M GP Total),💰 第三档：中期（总计 18 万-200 万 GP）
h3,🎒 Essential Inventory for Every Task,🎒 每个任务必备的背包配置
h3,📦 Loot Management Strategy,📦 战利品管理策略
h3,⚔️ Combat Efficiency Tips,⚔️ 战斗效率技巧
h3,💎 Slayer Points Spending Priority for Money Makers,💎 赚钱者的 Slayer 点数消费优先顺序
h3,📊 Time Cost vs. GP Analysis,📊 时间成本 vs GP 分析
h3,🎯 What To Do After Building Your First 1M GP from Slayer,🎯 通过 Slayer 赚取第一个 100 万 GP 后的行动建议
h3,Expected Slayer GP Milestones,Slayer 预期 GP 里程碑
h3,S-Tier Tasks (2M-2M+ GP/hr),S 级任务（200 万-200 万+ GP/小时）
h3,A-Tier Tasks (1.8M-2M GP/hr),A 级任务（18 万-200 万 GP/小时）
h3,B-Tier Tasks (1.8M-1.8M GP/hr),B 级任务（18 万-180 万 GP/小时）
h3,Tasks to ALWAYS Skip (Spend Points),始终跳过的任务（消耗点数）
h3,Tasks to ALWAYS Extend,始终扩展的任务
h3,Melee DPS Setup — Gargoyles, Kurasks, Bloodvelds, Wyverns,近战 DPS 配置 — 石像鬼、库拉斯克、血精灵、飞龙
h3,Burst/Barrage Setup — Nechryaels, Dust Devils, Abyssal Demons,爆破/弹幕配置 — 尼查尔、沙尘恶魔、深渊恶魔
h3,Standard Slayer Inventory (All Tasks),标准 Slayer 背包（所有任务）
h3,1️⃣ Abyssal Demons — Catacombs (1.8M-2.5M GP/hr),1️⃣ 深渊恶魔 — 地下墓穴（180 万-250 万 GP/小时）
h3,2️⃣ Nechryaels — Catacombs (2M-2.5M GP/hr),2️⃣ 尼查尔 — 地下墓穴（200 万-250 万 GP/小时）
h3,3️⃣ Dust Devils — Catacombs (700K-1M GP/hr),3️⃣ 沙尘恶魔 — 地下墓穴（70 万-100 万 GP/小时）
h3,4️⃣ Gargoyles — Slayer Tower (1.8M-700K GP/hr),4️⃣ 石像鬼 — Slayer 塔（18 万-70 万 GP/小时）
h3,5️⃣ Kurasks — Iorwerth Dungeon (1.8M-700K GP/hr),5️⃣ 库拉斯克 — 伊奥沃斯地牢（18 万-70 万 GP/小时）
h3,XP Tasks vs GP Tasks — Quick Reference,经验任务 vs GP 任务 — 快速参考
h3,Q: What's the single best Slayer task for GP?,问：哪个 Slayer 任务的 GP 最高？
h3,Q: Should I use Konar or Duradel for money?,问：赚钱应该用 Konar 还是 Duradel？
h3,Q: Is it worth doing boss variants on Slayer tasks?,问：在 Slayer 任务中打 Boss 变种值得吗？
h3,Q: How much GP should I expect from 1-99 Slayer?,问：1-99 级 Slayer 应该有多少 GP 收入？
h3,Q: What Slayer unlocks should I prioritize for money?,问：为赚钱应该优先解锁哪些 Slayer 功能？
h3,Q: Can I make money on Slayer with 50-70 combat stats?,问：50-70 战斗等级能通过 Slayer 赚钱吗？
h3,Q: What's better — bursting in Catacombs or bossing on task?,问：哪个更好 — 在地下墓穴爆破还是做任务打 Boss？
h3,① Quest Requirements,① 任务要求
h3,② Stat Recommendations,② 属性建议
h3,③ Key Unlocks Worth Getting,③ 值得获取的关键解锁
h3,① Max Gear — DHCB Method (4M+/hr),① 顶级装备 — DHCB 方法（400 万+/小时）
h3,② Mid-Tier — Dragon Hunter Lance Method (3.5M+/hr),② 中级 — 龙猎枪方法（350 万+/小时）
h3,③ Budget Setup — Toxic Blowpipe (2.5M+/hr),③ 预算配置 — 毒吹管（250 万+/小时）
h3,① Standard Inventory (DHCB / Ranged),① 标准背包（DHCB / 远程）
h3,② Melee Inventory (Lance),② 近战背包（龙枪）
h3,③ Teleport and Re-supply Strategy,③ 传送与补给策略
h3,① Vorkath's Basic Attack Pattern,① 韦克思的基础攻击模式
h3,② Special Attacks — Spawn Phase,② 特殊攻击 — 召唤阶段
h3,③ Special Attacks — Acid Phase,③ 特殊攻击 — 酸液阶段
h3,④ Special Attack Weapons and Spec Timing,④ 特殊攻击武器与技能时机
h3,⑤ Death Mechanics and Item Recovery,⑤ 死亡机制与物品回收
h3,① What Is the Woox Walk?,① 什么是 Woox 走位法？
h3,② How to Execute the Woox Walk,② 如何执行 Woox 走位法
h3,③ Woox Walk Gear Notes,③ Woox 走位装备说明
h3,④ Common Woox Walk Mistakes,④ 常见的 Woox 走位错误
h3,① Regular Drop Table Highlights,① 常规掉落表亮点
h3,② Unique Drops,② 独特掉落
h3,③ GP Per Hour Breakdown,③ 每小时 GP 收益分析
h3,④ Supply Cost Calculator,④ 补给成本计算
h3,① Starting Out — Under 10M Setup,① 起步 — 低于 1000 万配置
h3,② Efficient Progression Path,② 高效进阶路径
h3,③ Tips to Reduce Death Rate,③ 降低死亡率的技巧
h3,④ Recommended Quest and Diary Completions,④ 推荐的任务与日记完成
h3,⑤ When to Take a Break,⑤ 何时休息
h3,Is Vorkath worth doing in 2026?,2026 年韦克思还值得打吗？
h3,What's better for Vorkath — DHCB or DHL?,打韦克思哪个更好 — DHCB 还是 DHL？
h3,Do I need Rigour for Vorkath?,打韦克思需要 Rigour 吗？
h3,How many kills per trip can I expect?,每次行程可以击杀多少次？
h3,Can I kill Vorkath with 70 Range?,70 级远程能打韦克思吗？
h3,Should I use Ruby or Diamond bolts?,应该用红宝石还是钻石弩箭？
h3,Is Void Knight gear good for Vorkath?,虚空骑士装备适合打韦克思吗？
h3,What's the fastest way to Ungael?,去恩格尔的最快方式是什么？
h3,How long does the Skeletal Visage take to get?,骷髅面罩需要多久才能获得？
h3,Does the Woox Walk really matter?,Woox 走位法真的重要吗？
h3,Should I use a Dragonfire Shield or an Anti-Dragon Shield?,应该用龙火盾还是防龙盾？
h3,Can I kill Vorkath on a Slayer Task?,能在 Slayer 任务中击杀韦克思吗？
h3,What is the best special attack weapon for Vorkath?,打韦克思的最佳特殊攻击武器是什么？
h3,How do I avoid Vorkath's dragonfire attack?,如何躲避韦克思的龙火攻击？
h3,Is Vorkath harder than Zulrah or Muspah?,韦克思比祖拉或穆斯帕难吗？
h3,What is the alch value of Vorkath's drops per kill?,韦克思每次击杀掉落的炼金价值是多少？
h3,Can I use the Blowpipe on rapid at Vorkath?,打韦克思能用吹管的快速模式吗？
h3,Should I sell my bank for a DHCB?,应该卖掉我的仓库买 DHCB 吗？
h3,How does Vorkath compare to the Phantom Muspah for money?,韦克思与幻影穆斯帕赚钱对比如何？
h3,What happens if I run out of prayer at Vorkath?,打韦克思时祈祷用完了会怎样？
h3,How do I practice Vorkath without risking gear?,如何在不冒险装备的情况下练习打韦克思？
h3,Is it worth using a Ring of Suffering at Vorkath?,打韦克思值得用苦难之戒吗？
"@

Write-Host "Loading translations..."
$mapTOC = @{}
$mapH2 = @{}
$mapH3 = @{}

$lines = $translations -split "`n"
foreach ($line in $lines) {
    $line = $line.Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    
    $parts = $line -split ',', 3
    if ($parts.Length -lt 3) { continue }
    
    $type = $parts[0].Trim()
    $en = $parts[1]
    $cn = $parts[2]
    
    if ($type -eq "map") {
        $mapTOC[$en] = $cn
    } elseif ($type -eq "h2") {
        $mapH2[$en] = $cn
    } elseif ($type -eq "h3") {
        $mapH3[$en] = $cn
    }
}

Write-Host "Loaded: $($mapTOC.Count) TOC, $($mapH2.Count) H2, $($mapH3.Count) H3"

# Process each file
$totalReplaced = 0
foreach ($file in $files) {
    $path = Join-Path $BasePath $file
    if (-not (Test-Path $path)) {
        Write-Host "  NOT FOUND: $file"
        continue
    }
    
    $content = Get-Content $path -Raw
    $count = 0
    
    # Process TOC links (中文翻译)
    foreach ($en in $mapTOC.Keys) {
        $cn = $mapTOC[$en]
        $old = "$en（中文翻译）"
        $new = "$en（$cn）"
        $idx = $content.IndexOf($old)
        if ($idx -ge 0) {
            $content = $content.Replace($old, $new)
            $count++
        }
    }
    
    # Process H2 (中文标题)
    foreach ($en in $mapH2.Keys) {
        $cn = $mapH2[$en]
        $old = "$en（中文标题）"
        $new = "$en（$cn）"
        $idx = $content.IndexOf($old)
        if ($idx -ge 0) {
            $content = $content.Replace($old, $new)
            $count++
        }
    }
    
    # Process H3 (中文说明)
    foreach ($en in $mapH3.Keys) {
        $cn = $mapH3[$en]
        $old = "$en（中文说明）"
        $new = "$en（$cn）"
        $idx = $content.IndexOf($old)
        if ($idx -ge 0) {
            $content = $content.Replace($old, $new)
            $count++
        }
    }
    
    if ($count -gt 0) {
        Set-Content $path $content -NoNewline
        Write-Host "  ✓ $file — $count replacements"
        $totalReplaced += $count
    } else {
        Write-Host "  ✗ $file — NO replacements (check keys)"
    }
}

Write-Host "`nDONE! Total replacements: $totalReplaced across all files."
