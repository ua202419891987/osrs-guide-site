#!/usr/bin/env python3
"""
Fix Chinese placeholder text in zh/guides/osrs-*.html files.
Replaces patterns like （中文标题）（中文翻译）（中文说明）（中文子标题）（中文注释）
with real Chinese translations based on the English text preceding the parentheses.
"""

import re
import os
import glob
import sys

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\zh\guides"

# English -> Chinese translation mappings for common phrases
T = {
    # ============ h2 headings with （中文标题） ============
    "Why Train Mining? (Benefits & Uses)": "为什么要练采矿？（好处与用途）",
    "Levels 15–30: Iron Ore and Preparing for Motherlode Mine": "等级15-30：铁矿石与为矿脉矿场做准备",
    "Levels 30–99: Motherlode Mine — The Core Method for Beginners": "等级30-99：矿脉矿场 — 新手核心方法",
    "Alternative Mining Methods (Faster XP or More Money)": "替代采矿方法（更快经验或更多钱）",
    "Mining Money Making Methods Comparison Table": "采矿赚钱方法对比表",
    "Essential Gear & Pro Tips for Mining": "采矿必备装备与专业技巧",
    "Related Guides": "相关指南",
    "Table of Contents": "目录",
    "Understanding Skill Categories": "理解技能分类",
    "Combat Skills Overview": "战斗技能概览",
    "Production & Crafting Skills": "生产与制作技能",
    "Support & Utility Skills": "支持与实用技能",
    "Recommended Skill Progression for Beginners": "新手推荐技能进阶路线",
    "Real-World Skill Applications & Gold-Making Potential": "现实技能应用与赚钱潜力",
    "Final Tips for Skill Mastery": "技能精通最终建议",
    "Continue Your OSRS Journey": "继续你的OSRS旅程",
    "Frequently Asked Questions": "常见问题",
    "Recommended Skill Progression": "推荐技能进阶路线",
    "Real-World Skill Applications": "现实技能应用",
    "1. Why Flipping Works for New Players": "1. 为什么倒卖对新玩家有效",
    "2. Getting Started — The Margin Check Process": "2. 入门 — 利润检查流程",
    "3. Best Budget Flip Items Under 100K": "3. 10万金币以下最佳低价倒卖物品",
    "4. Cannonball Flipping Deep Dive": "4. 炮弹倒卖深度解析",
    "5. Nature Rune Flipping Strategy": "5. 自然符文倒卖策略",
    "6. Advanced Flipping Tips": "6. 高级倒卖技巧",
    "7. Common Flipping Mistakes": "7. 常见倒卖错误",
    "8. Frequently Asked Questions": "8. 常见问题",
    "1. Combat Basics — Understanding the Combat Triangle": "1. 战斗基础 — 理解战斗三角",
    "2. Core Training Principles Every Beginner Must Know": "2. 每位新手必须了解的核心训练原则",
    "3. Melee Training: Complete 1–70 Step-by-Step Route": "3. 近战训练：1-70级完整逐步路线",
    "4. Melee Training: 70–99 Efficient Routes": "4. 近战训练：70-99级高效路线",
    "5. Ranged Training: Complete 1–99 Route": "5. 远程训练：1-99级完整路线",
    "6. Magic Training: Complete 1–99 Route": "6. 魔法训练：1-99级完整路线",
    "10. When & How to Start Slayer — The Best Combat Training Method": "10. 何时及如何开始杀戮者 — 最佳战斗训练方式",
    "12. Combat Training FAQs — 15 Questions Every Beginner Asks": "12. 战斗训练常见问题 — 新手常问的15个问题",
    "Final Tips — Combat Training for Beginners": "最终建议 — 新手战斗训练",
    "1. Why Diary Order Matters (Not All Diaries Are Equal)": "1. 为什么日记顺序很重要（并非所有日记都相同）",
    "2. The Scoring System — How We Ranked Diaries": "2. 评分系统 — 我们如何为日记排名",
    "3. Top 10 Diaries — Detailed Breakdown": "3. 十大日记 — 详细解析",
    "5. Diaries to Skip For Now": "5. 暂时跳过的日记",
    "6. Quick Reference: All Diary Rewards Summary": "6. 快速参考：所有日记奖励摘要",
    "7. Diary Priority FAQ": "7. 日记优先级常见问题",
    "Section 1: Understanding F2P Combat Limits": "第1节：理解F2P战斗限制",
    "Section 2: F2P Gear Progression (Free Player Gear Tiers)": "第2节：F2P装备进阶（免费玩家装备等级）",
    "Section 4: Levels 10–20 Attack/Strength (Minotaurs & Goblins)": "第4节：10-20级攻击/力量（牛头人与哥布林）",
    "Section 5: Levels 20–30 Attack/Strength (Hill Giants & Flesh Crawlers)": "第5节：20-30级攻击/力量（山丘巨人与血肉爬行者）",
    "Section 6: Levels 30–40 Attack/Strength (Hobgoblins & Skeletons)": "第6节：30-40级攻击/力量（野猪人与骷髅）",
    "Section 7: F2P Defence Training": "第7节：F2P防御训练",
    "Section 10: F2P Quest Recommendations (Boost Your Stats FOR FREE)": "第10节：F2P任务推荐（免费提升你的属性）",
    "Section 12: Tips &amp; FAQ": "第12节：提示与常见问题",
    
    # ============ h3 headings with （中文子标题） ============
    "① 🏗️ Essential for Smithing": "① 🏗️ 锻造必需",
    "② 📜 Quest Requirements": "② 📜 任务要求",
    "③ 💰 Money Making Potential": "③ 💰 赚钱潜力",
    "④ 😌 AFK-Friendly Training": "④ 😌 挂机友好训练",
    "⑤ 🎒 Access to Motherlode Mine at 30": "⑤ 🎒 30级进入矿脉矿场",
    "⑥ 🐾 The Mining Pet (Rocky)": "⑥ 🐾 采矿宠物（洛奇）",
    "⑦ 📍 Best Locations for Levels 1-15": "⑦ 📍 1-15级最佳地点",
    "⚡ Power-Mining (Drop Mining) for Speed": "⚡ 快速采矿（掉落采矿）",
    "⑧ 📊 XP Rates and Time Estimates": "⑧ 📊 经验率与时间估算",
    "⑨ ⚒️ Pickaxe Progression (Levels 1-15)": "⑨ ⚒️ 镐子进阶（1-15级）",
    "⑩ 🗺️ Step-by-Step: Getting from Level 1 to 15": "⑩ 🗺️ 逐步指南：从1级到15级",
    "🪨 Option A: Power-Mine Iron Ore in Al Kharid (Levels 15-30)": "🪨 方案A：在阿尔卡里德快速采铁矿（15-30级）",
    "🪨 Option B: Motherlode Mine at Level 30 (Requires Digsite Quest)": "🪨 方案B：30级进入矿脉矿场（需完成考古任务）",
    "🎯 Recommendation: Get to 30 ASAP, Then Switch to MLM": "🎯 推荐：尽快到30级，然后切换到矿脉矿场",
    "⚒️ Pickaxe Upgrades (Levels 15-30)": "⚒️ 镐子升级（15-30级）",
    "📍 Where is the Motherlode Mine?": "📍 矿脉矿场在哪里？",
    "⛏️ How Motherlode Mine Works (Step-by-Step)": "⛏️ 矿脉矿场如何运作（分步指南）",
    "📊 XP Rates: Upper Level vs. Lower Level": "📊 经验率：上层 vs 下层",
    "🎽 Essential Gear for MLM": "🎽 矿脉矿场必备装备",
    "💰 Sack Upgrades: Bigger Capacity = Less Clicking": "💰 袋子升级：更大容量=更少点击",
    "📈 Estimated Time to 99 at MLM": "📈 矿脉矿场升到99级的预估时间",
    "💵 Profit from MLM: It Adds Up!": "💵 矿脉矿场收益：积少成多！",
    "⚡ 3-Tick Granite Mining (Levels 50-99) — Fastest XP": "⚡ 3拍花岗岩采矿（50-99级）— 最快经验",
    "💎 Gem Rocks (Level 40+) — Great Money, Decent XP": "💎 宝石岩（40级以上）— 好收益，不错经验",
    "🌋 Volcanic Sulphur (Level 43+) — Fast XP, Good Money": "🌋 火山硫磺（43级以上）— 快速经验，好收益",
    "💜 Amethyst Crystal Mining (Level 95+) — Best Money, Great XP": "💜 紫水晶采矿（95级以上）— 最佳收益，极好经验",
    "🏆 Best Methods by Category": "🏆 各类最佳方法",
    "⚒️ Complete Pickaxe Progression Guide": "⚒️ 完整镐子进阶指南",
    "🎽 Prospector Outfit (2.5% XP Bonus)": "🎽 勘探者套装（2.5%经验加成）",
    "🏅 Mining Cape (99) and Varrock Armour": "🏅 采矿披风（99级）与瓦洛克盔甲",
    "💊 Useful Consumables and Items": "💊 有用的消耗品与物品",
    "⚡ Pro Tips for Faster Mining": "⚡ 更快采矿的专业技巧",
    "🎯 3-Tick Granite Mining: Detailed Timing Guide": "🎯 3拍花岗岩采矿：详细时机指南",
    "❓ Q: Should I bank ores or power-mine (drop them)?": "❓ 问：我该存矿物还是快速采矿（扔掉）？",
    "❓ Q: Is Motherlode Mine better than 3-tick granite?": "❓ 问：矿脉矿场比3拍花岗岩更好吗？",
    "❓ Q: What quests help with Mining? Which should I do first?": "❓ 问：哪些任务有助于采矿？我应该先做哪个？",
    "❓ Q: Can F2P (Free-to-Play) players train Mining effectively?": "❓ 问：F2P玩家能有效训练采矿吗？",
    "❓ Q: How long does it take to get 99 Mining at MLM?": "❓ 问：在矿脉矿场升到99采矿需要多长时间？",
    "❓ Q: What's the best pickaxe for a beginner with a low budget?": "❓ 问：预算有限的新手用什么镐子最好？",
    "❓ Q: Should I use Swiftness potions or other boosts for Mining?": "❓ 问：我该用迅敏药水或其他加成来采矿吗？",
    "❓ Q: I'm an Ironman. Does this guide still apply?": "❓ 问：我是铁人模式。这个指南还适用吗？",
    "❓ Q: What's the best way to make money with Mining at low levels?": "❓ 问：低级采矿赚钱的最佳方式是什么？",
    "More Skill Training Guides": "更多技能训练指南",
    "The Three Pillar System": "三大支柱系统",
    "Combat Skills (11 total)": "战斗技能（共11个）",
    "Production Skills (9 total)": "生产技能（共9个）",
    "Gathering & Support Skills (3 total)": "采集与支持技能（共3个）",
    "Attack Skill": "攻击技能",
    "Strength Skill": "力量技能",
    "Defence Skill": "防御技能",
    "Hitpoints (HP) Skill": "生命值（HP）技能",
    "Ranged Skill": "远程技能",
    "Magic Skill": "魔法技能",
    "Prayer Skill": "祈祷技能",
    "Slayer Skill": "杀戮者技能",
    "Cooking Skill": "烹饪技能",
    "Fishing Skill": "钓鱼技能",
    "Woodcutting Skill": "伐木技能",
    "Mining Skill": "采矿技能",
    "Smithing Skill": "锻造技能",
    "Crafting Skill": "工艺技能",
    "Herblore Skill": "草药学技能",
    "Fletching Skill": "制箭技能",
    "Construction Skill": "建造技能",
    "Runecrafting Skill": "符文制作技能",
    "Agility Skill": "敏捷技能",
    "Thieving Skill": "偷窃技能",
    "Firemaking Skill": "生火技能",
    "Priority 1: Early Combat (Levels 1-40)": "优先级1：早期战斗（1-40级）",
    "Priority 2: Mid-Level Combat (Levels 40-70)": "优先级2：中级战斗（40-70级）",
    "Priority 3: Essential Support Skills (Concurrent)": "优先级3：必备支持技能（同时进行）",
    "Priority 4: Money-Making Skills (Post-70 Combat)": "优先级4：赚钱技能（70级战斗后）",
    "Priority 5: Late-Game Specialization (99 Goals)": "优先级5：后期专精（99级目标）",
    "Recommended Early-Game Skill Order": "推荐早期技能顺序",
    "Combat-Focused Progression": "战斗专注进阶",
    "Production-Focused Progression": "生产专注进阶",
    "Hybrid Progression": "混合进阶",
    "Gathering-Focused Progression": "采集专注进阶",
    "Quest & Achievement Progression": "任务与成就进阶",
    "Smart Profit Rotation Strategy": "智能利润轮换策略",
    "F2P vs P2P Skill Access Comparison": "F2P与P2P技能对比",
    "What's the fastest skill to train to 99?": "什么技能升到99级最快？",
    "Which skill should I train first?": "我应该先练什么技能？",
    "Are all 23 skills essential?": "所有23个技能都必需吗？",
    "How long does it take to reach 99 in each skill?": "每个技能升到99级需要多长时间？",
    "What's the most profitable skill to train?": "什么技能最赚钱？",
    "Should I train all skills to 99?": "我该把所有技能都练到99吗？",
    "① Table of Contents": "① 目录",
    "② How Combat Level Is Calculated": "② 战斗等级如何计算",
    "③ Understanding Attack Speed (Ticks)": "③ 理解攻击速度（游戏刻）",
    "④ Principle 1: Attack > Strength > Defence Priority": "④ 原则1：攻击>力量>防御优先级",
    "⑤ Principle 2: Safe-Spotting = Free Training": "⑤ 原则2：安全点=免费训练",
    "⑥ Principle 3: Aggressive Monsters Save you Time": "⑥ 原则3：攻击性怪物节省时间",
    "⑦ Principle 4: Quests Give Free Combat XP": "⑦ 原则4：任务提供免费战斗经验",
    "⑧ Step 1: Levels 1–10 (Chickens & Cows)": "⑧ 第一步：1-10级（鸡与牛）",
    "⑨ Step 2: Levels 10–20 (Al-Kharid Warriors — F2P Option)": "⑨ 第二步：10-20级（阿尔卡里德战士 — F2P选项）",
    "⑩ Step 3: Levels 20–40 (Barbarians or Stronghold of Security)": "⑩ 第三步：20-40级（野蛮人或安全堡垒）",
    "Step 4: Levels 40–60 (Flesh Crawlers or Hill Giants)": "第四步：40-60级（血肉爬行者或山丘巨人）",
    "Step 5: Levels 60–70 (Experiments or Rock Crabs)": "第五步：60-70级（实验体或岩蟹）",
    "Method A: Slayer (Best Overall, 70–99)": "方案A：杀戮者（综合最佳，70-99级）",
    "Method B: Nightmare Zone (NMZ) — AFK 99": "方案B：噩梦区 — 挂机到99级",
    "Method C: Manual Grinding (Fastest XP)": "方案C：手动刷怪（最快经验）",
    "Levels 1–30: Chickens & Cows with Shortbow": "1-30级：鸡与牛配短弓",
    "Levels 30–60: Rock Crabs (Members) or Ogress Warriors (F2P)": "30-60级：岩蟹（会员）或女妖战士（F2P）",
    "Levels 60–70: Chinning or Slayer": "60-70级：投掷训练或杀戮者",
    "Levels 70–99: Slayer with Ranged": "70-99级：远程杀戮者",
    "Levels 1–7: Imp Catcher Quest (Instant XP)": "1-7级：小恶魔捕捉任务（即时经验）",
    "Levels 7–25: Splashing (AFK Method)": "7-25级：溅射法术（挂机方法）",
    "Levels 25–55: Superheat Item (Smithing XP + Money)": "25-55级：超级加热（锻造经验+钱）",
    "Level 55+: High Level Alchemy (Passive Income)": "55级以上：高级炼金术（被动收入）",
    "Levels 55–99: Combat Magic (Bursts/Barrages)": "55-99级：战斗魔法（爆发/弹幕）",
    "Melee Training Route (Attack / Strength / Defence)": "近战训练路线（攻击/力量/防御）",
    "Ranged Training Route": "远程训练路线",
    "Magic Training Route": "魔法训练路线",
    "⚔️ Melee Gear Progression": "⚔️ 近战装备进阶",
    "🏹 Ranged Gear Progression": "🏹 远程装备进阶",
    "✨ Magic Gear Progression": "✨ 魔法装备进阶",
    "Which Slayer Master to Use (by Combat Level)": "使用哪个杀戮者大师（按战斗等级）",
    "How to Start Slayer (Step-by-Step)": "如何开始杀戮者（逐步指南）",
    "Nightmare Zone (NMZ) — AFK Melee 60k–80k XP/hr": "噩梦区 — 挂机近战6-8万经验/小时",
    "Bursting/Barraging — Magic 100k–300k XP/hr": "爆发/弹幕 — 魔法10-30万经验/小时",
    "Chinning — Ranged 200k–300k XP/hr": "投掷训练 — 远程20-30万经验/小时",
    "Cannon — +30% XP Boost (Costs GP)": "大炮 — +30%经验加成（消耗金币）",
    "🗡️ What to Do After This Guide": "🗡️ 本指南之后要做什么",
    "More Boss & PvM Guides": "更多Boss与PvM指南",
    "② Why Beginners Should NOT Start with Hard Diaries": "② 为什么新手不应该先做困难日记",
    "③ Dimension 1: Reward Value (40% weight)": "③ 维度1：奖励价值（40%权重）",
    "④ Dimension 2: Time Required (30% weight)": "④ 维度2：所需时间（30%权重）",
    "⑤ Dimension 3: Difficulty (20% weight)": "⑤ 维度3：难度（20%权重）",
    "⑥ Dimension 4: Long-term Utility (10% weight)": "⑥ 维度4：长期实用性（10%权重）",
    "⑦ 🥇 #1: Varlamore Easy Diary": "⑦ 🥇 第1名：瓦拉摩尔简单日记",
    "⑧ 🥈 #2: Kandarin Medium (and Hard when ready)": "⑧ 🥈 第2名：坎达林中等等级（准备好后做困难）",
    "⑨ 🥉 #3: Ardougne Medium Diary": "⑨ 🥉 第3名：阿多格恩中等等级日记",
    "⑩ #4: Falador Medium Diary": "⑩ 第4名：法洛多中等等级日记",
    "#5: Wilderness Easy Diary": "第5名：荒野简单日记",
    "#6: Lumbridge & Draynor Easy Diary": "第6名：卢布里奇与德雷诺简单日记",
    "#7: Kourend & Kebos Medium Diary": "第7名：库伦德与凯波斯中等等级日记",
    "#8: Desert Medium Diary": "第8名：沙漠中等等级日记",
    "#9: Morytania Medium Diary": "第9名：莫里塔尼亚中等等级日记",
    "#10: Western Provinces Medium Diary": "第10名：西部省份中等等级日记",
    "Phase 1: Easy Diaries (Week 1)": "阶段1：简单日记（第1周）",
    "Phase 2: Medium Diaries — Southern Region (Week 2–3)": "阶段2：中等等级日记 — 南部地区（第2-3周）",
    "Phase 3: Medium Diaries — Remote Regions (Week 4–5)": "阶段3：中等等级日记 — 偏远地区（第4-5周）",
    "Phase 4: Varlamore (Anytime after Children of the Sun)": "阶段4：瓦拉摩尔（完成太阳之子后随时）",
    "🎯 What To Do After Completing Your Priority Diaries": "🎯 完成优先日记后要做什么",
    "More Achievement Guides": "更多成就指南",
    "What's Possible in F2P": "F2P中可行的内容",
    "Combat Level Formula (Important!)": "战斗等级公式（重要！）",
    "Melee Gear Progression (Attack/Strength/Defence)": "近战装备进阶（攻击/力量/防御）",
    "Ranged Gear Progression": "远程装备进阶",
    "Important F2P Gear Notes": "重要F2P装备说明",
    "Best Monster: Chickens (Lumbridge & Falador)": "最佳怪物：鸡（卢布里奇与法洛多）",
    "Alternative: Cows (Lumbridge)": "替代方案：牛（卢布里奇）",
    "Best Monster: Level 12 Minotaurs (Stronghold of Security Floor 1)": "最佳怪物：12级牛头人（安全堡垒第1层）",
    "Also Good: Goblins (Various Locations)": "也不错：哥布林（多个地点）",
    "Best Monster: Hill Giants (Edgeville Dungeon)": "最佳怪物：山丘巨人（埃奇维尔地牢）",
    "Alternative: Flesh Crawlers (Stronghold of Security Floor 2)": "替代方案：血肉爬行者（安全堡垒第2层）",
    "Best Monster: Hobgoblins (Near Crafting Guild)": "最佳怪物：野猪人（工艺公会附近）",
    "Also Good: Moss Giants (Varrock Sewers)": "也不错：苔藓巨人（瓦洛克下水道）",
    "For the Level 40 Attack Goal: You NEED the Rune Scimitar": "40级攻击目标：你需要符文弯刀",
    "Why Raise Defence?": "为什么提升防御？",
    "Defence Training Method": "防御训练方法",
    "Ranged Training Progression": "远程训练进阶",
    "Ranged Training Tips": "远程训练技巧",
    "Prayer in F2P: Is It Worth It?": "F2P中的祈祷：值得吗？",
    "Prayer Training Strategy for F2P": "F2P祈祷训练策略",
    "All F2P Quests (In Recommended Order)": "所有F2P任务（按推荐顺序）",
    "Recommended Quest Order for Brand New F2P Player": "全新F2P玩家推荐任务顺序",
    "Day-by-Day F2P Combat Training Plan": "逐日F2P战斗训练计划",
    "Final Tips for F2P Combat Training Success": "F2P战斗训练成功的最终建议",
    "① Week 1 Training Schedule & Goals": "① 第1周训练计划与目标",
    "② Week 2 Training Schedule & Goals": "② 第2周训练计划与目标",
    "③ Week 3 Training Schedule & Goals": "③ 第3周训练计划与目标",
    "④ Week 4 Training Schedule & Goals": "④ 第4周训练计划与目标",
    "⑤ Q1: How long does it take to max all 23 skills in OSRS as a beginner?": "⑤ 问1：新手最大化所有23个技能需要多长时间？",
    "⑥ Q2: Should I focus on one skill at a time or train multiple skills simultaneously?": "⑥ 问2：我应该专注一个技能还是同时训练多个技能？",
    "⑦ Q3: What is the best money-making method for a beginner with low stats?": "⑦ 问3：低属性新手的最佳赚钱方法是什么？",
    "⑧ Q4: When should I start doing bossing content in OSRS?": "⑧ 问4：我什么时候应该开始打Boss？",
    "⑨ Q5: Is it worth it to get membership as a brand new player?": "⑨ 问5：全新玩家值得购买会员吗？",
    "⑩ Q6: How important is the account build (main, ironman, hardcore ironman) for a beginner?": "⑩ 问6：账号类型（普通、铁人、硬核铁人）对新手有多重要？",
    
    # ============ TOC items with （中文翻译） ============
    "📊 The Big Picture — F2P vs Members at a Glance": "📊 大局 — F2P与会员概览",
    "🗺️ Map & Areas Comparison": "🗺️ 地图与区域对比",
    "📜 Quests Comparison": "📜 任务对比",
    "🔧 Skills Comparison": "🔧 技能对比",
    "⚔️ Bosses & Combat Content": "⚔️ Boss与战斗内容",
    "💰 Economy & Grand Exchange": "💰 经济与大交易所",
    "🤔 Is F2P Enough for You?": "🤔 F2P对你来说足够吗？",
    "❓ FAQs": "❓ 常见问题",
    "🏁 Final Tips": "🏁 最终建议",
    "How the OSRS Economy Works": "OSRS经济如何运作",
    "Your First 100k GP — Day 1 Complete Route": "你的第一个10万金币 — 第一天完整路线",
    "Using the Grand Exchange Smartly": "聪明使用大交易所",
    "Complete GP Route Table: 0 → 10M GP": "完整金币路线表：0 → 1000万金币",
    "Money Making Mistakes to Avoid": "需要避免的赚钱错误",
    "Your 500k GP Action Plan": "你的50万金币行动计划",
    "Money Making FAQs": "赚钱常见问题",
    "① What Is NMZ & Why Everyone Loves It": "① 什么是噩梦区及为什么人人爱它",
    "② Unlocking NMZ — Quest Requirements": "② 解锁噩梦区 — 任务要求",
    "③ Starting Cost & Budget Setup": "③ 启动成本与预算配置",
    "④ How NMZ Mechanics Work": "④ 噩梦区机制如何运作",
    "⑤ Choosing Your Dream Opponents": "⑤ 选择你的理想对手",
    "⑥ AFK Session Management": "⑥ 挂机会话管理",
    "⑦ NMZ Imbue Rewards Guide": "⑦ 噩梦区注魔奖励指南",
    "⑧ NMZ FAQ": "⑧ 噩梦区常见问题",
    "Boss 2: Bryophyta — The Moss Giant Boss": "Boss 2：苔巨人Boss",
    "F2P Boss Gear Master Table": "F2P Boss装备总表",
    "F2P Boss Profit Analysis": "F2P Boss收益分析",
    "F2P Combat Techniques for Bossing": "F2P打Boss战斗技巧",
    "From F2P Bosses to Member Bossing": "从F2P Boss到会员Boss",
    "F2P Bossing FAQs": "F2P打Boss常见问题",
    "Why Prayer Is the #1 Skill for Beginners": "为什么祈祷是新手的头号技能",
    "How the Prayer System Works": "祈祷系统如何运作",
    "5 Essential Prayers Every Beginner Needs": "每位新手必备的5个祈祷",
    "Prayer Flicking Basics": "祈祷闪烁基础",
    "Prayer Level Roadmap: What to Unlock When": "祈祷等级路线图：何时解锁什么",
    "Prayer FAQs": "祈祷常见问题",
    "Understanding OSRS's 23 Skills — The Big Picture": "理解OSRS的23个技能 — 大局观",
    "Skill Synergy — Training Multiple Skills Together": "技能协同 — 同时训练多个技能",
    "Common Beginner Mistakes in Skill Training": "技能训练中的常见新手错误",
    "Your First Month Skill Plan": "你的第一个月技能计划",
    "Skill Training FAQs": "技能训练常见问题",
    "What \"Mid-Game Ready\" Looks Like": "\"中期就绪\"是什么样子",
    "Budget Breakdown — 30-Day Cost": "预算分解 — 30天成本",
    "Progress Tracker & FAQ": "进度追踪与常见问题",
    "What Are Skills in OSRS?": "OSRS中的技能是什么？",
    "F2P vs Members Skills — What's Available?": "F2P与会员技能 — 有哪些可用？",
    "Which Skills Should YOU Train First?": "你应该先训练哪些技能？",
    "How Skills Connect to Quests": "技能如何与任务关联",
    "Skills That Make You Money": "能赚钱的技能",
    "Your First 10 Skills — Priority Order": "你的前10个技能 — 优先顺序",
    "What Is Slayer & Why Start Early": "什么是杀戮者及为什么尽早开始",
    "Choosing Your First Slayer Master": "选择你的第一个杀戮者大师",
    "Your First 10 Tasks — Optimal Task List": "你的前10个任务 — 最优任务列表",
    "Beginner Gear Setup for Slayer": "新手杀戮者装备配置",
    "Block & Skip List for Beginners": "新手屏蔽与跳过列表",
    "Slayer FAQs for Beginners": "新手杀戮者常见问题",
    "What Is Slayer & Why Do It?": "什么是杀戮者及为什么去做？",
    "Your First Slayer Master — How to Choose": "你的第一个杀戮者大师 — 如何选择",
    "Recommended Gear by Combat Level": "按战斗等级推荐装备",
    "Useful Slayer Unlocks & Quests": "有用的杀戮者解锁与任务",
    "7 Slayer Tips for Faster Progress": "7个更快进阶的杀戮者技巧",
    "FAQ": "常见问题",
    "The ROI Concept for Skill Training": "技能训练的投资回报率概念",
    "Skills 11-23 — Why They Ranked Lower": "第11-23名技能 — 为什么排名较低",
    "Optimal Training Order Roadmap": "最优训练顺序路线图",
    "By Playstyle Variations": "按玩法变体",
    "FAQ — Skill Priority Questions": "常见问题 — 技能优先级问题",
    
    # ============ h2 with （中文说明） ============
    "1. What Is Slayer & Why Start Early": "1. 什么是杀戮者及为什么尽早开始",
    "2. Choosing Your First Slayer Master": "2. 选择你的第一个杀戮者大师",
    "3. Unlocking Each Master (Quest Requirements)": "3. 解锁每个大师（任务要求）",
    "4. Your First 10 Tasks — Optimal Task List": "4. 你的前10个任务 — 最优任务列表",
    "5. Beginner Gear Setup for Slayer": "5. 新手杀戮者装备配置",
    "7. Slayer FAQs for Beginners": "7. 新手杀戮者常见问题",
    "1. Prerequisites & Requirements": "1. 先决条件与要求",
    "2. Budget Gear Setup — All 3 Styles": "2. 预算装备配置 — 全部3种风格",
    "3. Best Beginner Invocations (0 → 150)": "3. 最佳新手祈祷（0→150）",
    "4. Optimal Beginner Boss Order": "4. 最佳新手Boss顺序",
    "5. Kephri (Path of Scabaras) — ⭐⭐": "5. 凯弗里（斯卡巴拉斯之路）— ⭐⭐",
    "6. Akkha (Path of Het) — ⭐⭐⭐": "6. 阿卡（赫特之路）— ⭐⭐⭐",
    "7. Ba-Ba (Path of Apmeken) — ⭐⭐⭐": "7. 芭芭（阿普梅肯之路）— ⭐⭐⭐",
    "8. Zebak (Path of Crondis) — ⭐⭐": "8. 泽巴克（克龙迪斯之路）— ⭐⭐",
    "9. Wardens (Final Boss) — ⭐⭐⭐⭐": "9. 典狱长（最终Boss）— ⭐⭐⭐⭐",
    "10. Loot & First Purple": "10. 战利品与第一次紫色",
    "11. FAQ": "11. 常见问题",
    
    # ============ h3 with （中文说明） ============
    "🧠 Fight Strategy": "🧠 战斗策略",
    "💎 Loot": "💎 战利品",
    "🍖 Food Tier 1 (Bosses 1–3, F2P)": "🍖 食物第1层（Boss 1-3，F2P）",
    "🧪 Potions Tier 1 (Members Only, Bosses 4+)": "🧪 药水第1层（仅会员，Boss 4级以上）",
    "🎯 Recommended Next Steps": "🎯 推荐的下一步",
    "🎯 What To Do After Your First Boss Kill": "🎯 首次击杀Boss后要做什么",
    "Continue The Beginner Series": "继续新手系列",
    "⚔️ Stage 0.9 — Gear Guide": "⚔️ 阶段0.9 — 装备指南",
    "🏃 Stage 0.7 — Combat Training": "🏃 阶段0.7 — 战斗训练",
    "💰 Stage 0.8 — Money Making": "💰 阶段0.8 — 赚钱",
    "🔐 Stage 1.1 — Account Security": "🔐 阶段1.1 — 账号安全",
    "⚡ Quick Jump": "⚡ 快速跳转",
    "🛡️ Stage 0.11 — Prayer Training": "🛡️ 阶段0.11 — 祈祷训练",
    "🏦 Stage 0.4 — Bank & Inventory Guide": "🏦 阶段0.4 — 银行与背包指南",
    "🗺️ Stage 0.5 — Maps & Fast Travel": "🗺️ 阶段0.5 — 地图与快速旅行",
    "📜 Stage 0.6 — Questing for Beginners": "📜 阶段0.6 — 新手任务指南",
    "⚔️ Stage 0.7 — Combat Training Guide": "⚔️ 阶段0.7 — 战斗训练指南",
    "⚔️ Stage 1 — Combat Training": "⚔️ 阶段1 — 战斗训练",
    "📜 Stage 0.6 — Questing Basics": "📜 阶段0.6 — 任务基础",
    "🛡️ Stage 0.9 — Gear Guide": "🛡️ 阶段0.9 — 装备指南",
    "⚔️ Stage 1.14 — Your First Boss": "⚔️ 阶段1.14 — 你的第一个Boss",
    "💀 Stage 1.12 — Barrows Guide": "💀 阶段1.12 — 巴罗斯指南",
    "💰 Stage 1.15 — Skilling Money Makers": "💰 阶段1.15 — 技能赚钱方法",
    "⚔️ Stage 0.12 — Boss Progression Roadmap": "⚔️ 阶段0.12 — Boss进阶路线图",
    "🔑 Ready to Unlock the Full Game? Read Our Skills Guide": "🔑 准备解锁完整游戏？阅读我们的技能指南",
    "🎯 Just Bought Membership? Start Here": "🎯 刚买了会员？从这里开始",
    "💰 What to Do After This Guide": "💰 本指南之后做什么",
    "🏛️ ToA — Quick Reference": "🏛️ 坟墓之劫 — 快速参考",
    "🏛️ Your First Raid Awaits": "🏛️ 你的第一次突袭等待着",
    "② How to Skip Bad Tasks": "② 如何跳过不好的任务",
    "③ Tasks to Skip (Low Profit)": "③ 要跳过的任务（低利润）",
    "❓ 8. FAQ": "❓ 8. 常见问题",
    "🎯 What To Do After Your First 10 Slayer Tasks": "🎯 完成前10个杀戮者任务后做什么",
    "🙏 Stage 0.11 — Prayer Training": "🙏 阶段0.11 — 祈祷训练",
    "🎯 Why Slayer Is the #1 Skill for Long-Term Accounts": "🎯 为什么杀戮者是长期账号的头号技能",
    "② ⏰ When Should You Start Slayer?": "② ⏰ 你应该什么时候开始杀戮者？",
    "③ 📊 Slayer XP Rates by Level (What to Expect)": "③ 📊 按等级的杀戮者经验率（预期）",
    "④ 🗺️ All 7 Slayer Masters — Complete Comparison": "④ 🗺️ 全部7个杀戮者大师 — 完整对比",
    "⑤ 🗺️ Recommended Progression Path": "⑤ 🗺️ 推荐进阶路径",
    "⑥ 📍 How to Reach Each Master (Travel Guide)": "⑥ 📍 如何到达每个大师（旅行指南）",
    "⑦ 📋 Quests That Unlock Slayer Masters": "⑦ 📋 解锁杀戮者大师的任务",
    "⑧ 🗺️ Optimal Quest Order for Slayer Players": "⑧ 🗺️ 杀戮者玩家的最优任务顺序",
    "🎯 Typical First 10 Task Types (Turael/Vannaka)": "🎯 典型前10个任务类型（图拉尔/瓦纳卡）",
    "⑨ ⚔️ Task-by-Task Strategy Guide": "⑨ ⚔️ 逐任务策略指南",
    "⑩ 🔄 Should You Skip or Stay on a Task?": "⑩ 🔄 应该跳过还是继续任务？",
    "🛡️ Melee Setup (Primary Combat Style for Slayer)": "🛡️ 近战配置（杀戮者主要战斗风格）",
    "🏹 Ranged Setup (For Safe Spotting & Specific Tasks)": "🏹 远程配置（用于安全点和特定任务）",
    "✨ Essential Slayer Items (Don't Skip These!)": "✨ 必备杀戮者物品（别跳过这些！）",
    "💰 Budget Gear Challenge: 500K GP Full Setup": "💰 预算装备挑战：50万金币完整配置",
    "🚫 Tasks You Should BLOCK Immediately (As Soon as You Have 100+ Slayer Points)": "🚫 你应该立即屏蔽的任务（有100+杀戮者点数后）",
    "🔄 When to Skip vs. When to Stay": "🔄 何时跳过 vs 何时留下",
    "🎯 Slayer Unlocks Priority (How to Spend Your Points)": "🎯 杀戮者解锁优先级（如何花点数）",
    "Continue Your Slayer Progression": "继续你的杀戮者进阶",
    "💰 Stage 2.2 — Slayer Money Making": "💰 阶段2.2 — 杀戮者赚钱",
    "🆕 START HERE": "🆕 从这里开始",
    "🎮 Interface": "🎮 界面",
    "⚔️ Combat": "⚔️ 战斗",
    "🎯 Skills": "🎯 技能",
    "🏦 Bank": "🏦 银行",
    "🗺️ Navigation": "🗺️ 导航",
    "⑨ OSRS New Player Guide 2026": "⑨ OSRS新手指南2026",
    "⑩ Game Interface & Controls": "⑩ 游戏界面与控制",
    "Combat Triangle Explained": "战斗三角详解",
    "Skills Overview for Beginners": "新手技能概览",
    "Bank & Inventory Management": "银行与背包管理",
    "Maps & Fast Travel Guide": "地图与快速旅行指南",
    "🏃 Stage 0.10 — Safe Spots Guide": "🏃 阶段0.10 — 安全点指南",
    "Hunter — Catchning Creatures for Loot": "猎人 — 捕捉生物获取战利品",
    "Combat Training": "战斗训练",
    "Prayer Training": "祈祷训练",
    "Fast Track Guide": "快速通道指南",
    "📚 Complete Skill Guide": "📚 完整技能指南",
    "⚔️ Combat Training": "⚔️ 战斗训练",
    "🙏 Prayer Training": "🙏 祈祷训练",
    "🥇 #1: Prayer — ROI Score: 9.8/10": "🥇 第1名：祈祷 — 投资回报率评分：9.8/10",
    "🥈 #2: Magic — ROI Score: 9.3/10": "🥈 第2名：魔法 — 投资回报率评分：9.3/10",
    "🥉 #3: Hitpoints — ROI Score: 8.7/10": "🥉 第3名：生命值 — 投资回报率评分：8.7/10",
    "#4: Slayer — ROI Score: 8.2/10": "第4名：杀戮者 — 投资回报率评分：8.2/10",
    "#5: Agility — ROI Score: 7.8/10": "第5名：敏捷 — 投资回报率评分：7.8/10",
    "🎯 Your Next Steps": "🎯 你的下一步",
    "📊 Post Sweep-Up Changes": "📊 大扫除后的变化",
    "📜 Best Quests Per Skill": "📜 每技能最佳任务",
    "🙏 Prayer Training Guide": "🙏 祈祷训练指南",
    "🏃 Agility Training Guide": "🏃 敏捷训练指南",
    
    # ============ TOC （中文注释） ============
    "Understanding Skill Categories": "理解技能分类",
    "Combat Skills Overview": "战斗技能概览",
    "Production & Crafting Skills": "生产与制作技能",
    "Support & Utility Skills": "支持与实用技能",
    "Recommended Skill Progression": "推荐技能进阶路线",
    "Real-World Skill Applications": "现实技能应用",
    "Frequently Asked Questions": "常见问题",
    "Combat Basics — Understanding the Combat Triangle": "战斗基础 — 理解战斗三角",
    "Core Training Principles Every Beginner Must Know": "每位新手必须了解的核心训练原则",
    "Melee Training: Complete 1–70 Route": "近战训练：1-70级完整路线",
    "Melee Training: 70–99 (Efficient Routes)": "近战训练：70-99级（高效路线）",
    "Ranged Training: Complete 1–99 Route": "远程训练：1-99级完整路线",
    "Magic Training: Complete 1–99 Route": "魔法训练：1-99级完整路线",
    "1–70 Combat Training Route Table (Step-by-Step)": "1-70级战斗训练路线表（逐步指南）",
    "Best Monsters by Combat Level": "各等级最佳怪物",
    "Gear Upgrade Milestones (Budget to Endgame)": "装备升级里程碑（预算到终局）",
    "When & How to Start Slayer": "何时及如何开始杀戮者",
    "Advanced Combat Training Methods": "高级战斗训练方法",
    "Combat Training FAQs": "战斗训练常见问题",
    "Why Diary Order Matters (Not All Diaries Are Equal)": "为什么日记顺序很重要（并非所有日记都相同）",
    "The Scoring System — How We Ranked Diaries": "评分系统 — 我们如何为日记排名",
    "Top 10 Diaries — Detailed Breakdown": "十大日记 — 详细解析",
    "Optimal Completion Route (Efficiency Path)": "最佳完成路线（效率路径）",
    "Diaries to Skip For Now": "暂时跳过的日记",
    "Quick Reference: All Diary Rewards Summary": "快速参考：所有日记奖励摘要",
    "Diary Priority FAQ": "日记优先级常见问题",
    "Week 1: Foundation Building": "第1周：基础建设",
    "Week 2: Combat & Money Making": "第2周：战斗与赚钱",
    "Week 3: Slayer Unlocked": "第3周：解锁杀戮者",
    "Week 4: Scaling Up": "第4周：逐步升级",
    "Key Milestones to Track": "关键里程碑追踪",
    "Common Beginner Mistakes to Avoid": "常见新手错误避免",
    "Final Tips for Long-Term Success": "长期成功最终建议",
    
    # ============ Related guides article cards with truncated titles ============
    "OSRS All Skills Overview Guide 2026: Complete Beginner's Refer...": "OSRS全部技能概览指南2026：完整新手参考...",
    "OSRS Efficient Training Routes for Beginners 2026: Step-by-Ste...": "OSRS新手高效训练路线2026：逐步...",
    "OSRS Prayer Training Guide for Beginners 2026": "OSRS新手祈祷训练指南2026",
    "OSRS 1-99 Farming Guide for Beginners — Profit Focused (2026)": "OSRS新手1-99农耕指南 — 利润导向（2026）",
    "️ OSRS Clue Scrolls Beginner Guide 2026": "️ OSRS线索卷轴新手指南2026",
    "OSRS Combat Training Guide for Beginners 2026": "OSRS新手战斗训练指南2026",
    "️ OSRS F2P Slayer Guide 2026": "️ OSRS F2P杀戮者指南2026",
    "OSRS F2P Boss Guide 2026 — Obor, Bryophyta & Giant Mole": "OSRS F2P Boss指南2026 — 奥博、苔巨人与巨鼹",
    "️ OSRS F2P Gear Progression Guide 2026": "️ OSRS F2P装备进阶指南2026",
    "OSRS F2P Money Making No Stats Required — 2026 Guide": "OSRS F2P无需属性赚钱 — 2026指南",
    "OSRS Skill Training Complete Guide for Beginners 2026 — All 23...": "OSRS新手技能训练完整指南2026 — 全部23个...",
    "OSRS Complete Skill Training Guide 2026: 1-99 All Skills Faste...": "OSRS完整技能训练指南2026：1-99全部技能最快...",
    "OSRS Skills Overview for Beginners 2026": "OSRS新手技能概览2026",
    "OSRS Ironman Beginner Guide 2026 — Complete Starter Guide": "OSRS铁人新手指南2026 — 完整入门指南",
    "OSRS New Player Guide 2026 — Complete Beginner's Handbook": "OSRS新手指南2026 — 完整新手手册",
    "OSRS F2P Combat Training Guide — Level 3 to 30+ (2026)": "OSRS F2P战斗训练指南 — 3级到30级以上（2026）",
    "OSRS How to Beat Zulrah for Beginners — Full Rotation Guide 2026": "OSRS新手如何击败祖拉 — 完整旋转指南2026",
    "OSRS How to Solo God Wars Boss for Beginners 2026 — Bandos &am...": "OSRS新手如何单挑神战Boss 2026 — 班多斯...",
    "OSRS 1-99 Farming Guide for Beginners — Profit Focused (2026)": "OSRS新手1-99农耕指南 — 利润导向（2026）",
    "OSRS Efficient Training Routes for Beginners 2026: Step-by-Ste...": "OSRS新手高效训练路线2026：逐步...",
    "OSRS Achievement Diary Guide 2026": "OSRS成就日记指南2026",
    "OSRS Achievement Diary Guide 2026 — Best Rewards &amp; Optimal...": "OSRS成就日记指南2026 — 最佳奖励与最优...",
    "OSRS Easy & Medium Diaries — Full Completion Guide All Regions": "OSRS简单与中等等级日记 — 全区域完整指南",
    "OSRS How to Complete Lost City Quest Guide 2026 — Dramen Staff...": "OSRS如何完成失落之城任务指南2026 — 德拉门法杖...",
    "OSRS Quest Cape Guide 2026 — Complete Roadmap": "OSRS任务披风指南2026 — 完整路线图",
    "OSRS Ironman 1-99 Smithing Guide": "OSRS铁人1-99锻造指南",
    "OSRS Making Money with Crafting (Low Level)": "OSRS工艺赚钱（低级）",
    "OSRS F2P Money Making No Stats Required": "OSRS F2P无需属性赚钱",
    "OSRS New Player Guide 2026 — Complete Beginner's Handbook": "OSRS新手指南2026 — 完整新手手册",
    "OSRS F2P to P2P Bond Guide 2026 — Earn Your First Bond and Nev...": "OSRS F2P到P2P绑定券指南2026 — 赚取你的第一张绑定券...",
    "First 5M GP for New OSRS Members 2026": "新OSRS会员的首个500万金币指南2026",
    "Best Quests for New OSRS Members 2026": "新OSRS会员的最佳任务2026",
    "OSRS The Blood Moon Rises Quest Guide 2026": "OSRS血月升起任务指南2026",
    "Defence Priority": "防御优先级",
}


def clean_chinese(english, chinese):
    """Remove emoji/numbering prefixes from Chinese that duplicate English prefixes."""
    # Find common prefix (emoji + optional number) between English and Chinese
    # Common prefixes to strip from Chinese: ①-⑩, emojis
    prefix_pattern = re.compile(r'^[①-⑩⛏️🪨🎯⚒️📍🎽💰📈💎💵🌋💜🏆🏅💊⚡❓🗡️🎮⚔️🛡️✨🙏🔐🏦🗺️📜🔑🎯🥇🥈🥉📊🏃]+\s*')
    eng_prefix = prefix_pattern.match(english)
    if eng_prefix:
        chn_prefix = prefix_pattern.match(chinese)
        if chn_prefix and chn_prefix.group() == eng_prefix.group():
            # Strip the prefix from Chinese
            chinese = chinese[len(eng_prefix.group()):]
        elif chn_prefix:
            chinese = chinese[len(chn_prefix.group()):]
    return chinese

def lookup(english_text):
    """Look up Chinese translation. Returns Chinese or empty string."""
    chinese = lookup_raw(english_text)
    if chinese:
        return clean_chinese(english_text, chinese)
    return ""

def lookup_raw(english_text):
    """Look up Chinese translation from dictionary. Returns Chinese or empty string."""
    if english_text in T:
        return T[english_text]
    for eng, chn in T.items():
        if eng.lower() == english_text.lower():
            return chn
    # Try prefix matching
    for eng, chn in T.items():
        if english_text.startswith(eng) or eng.startswith(english_text):
            # Only use if they share significant overlap
            min_len = min(len(english_text), len(eng))
            if min_len >= 10 and (english_text[:min_len] == eng[:min_len]):
                return chn
    return ""


def process_file(filepath):
    """Process a single HTML file, replacing placeholder Chinese with real translations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    total_replaced = 0
    
    patterns = [
        r'（中文标题）',
        r'（中文翻译）',
        r'（中文说明）',
        r'（中文子标题）',
        r'（中文注释）',
    ]
    
    for placeholder in patterns:
        # Find all occurrences
        matches = list(re.finditer(re.escape(placeholder), content))
        if not matches:
            continue
        
        # Process in reverse to preserve positions
        for match in reversed(matches):
            pos = match.start()
            
            # Find the English text before （中文...）
            pre_text = content[:pos]
            
            # Find the last > before （
            last_gt = pre_text.rfind('>')
            if last_gt >= 0:
                english = pre_text[last_gt+1:].strip()
            else:
                english = ""
            
            # Skip support card text
            if "Every guide is free" in english:
                continue
            if "support-card" in pre_text[-200:]:
                continue
            
            # Skip if english is empty
            if not english:
                continue
            
            # Look up translation
            chinese = lookup(english)
            if not chinese:
                eng_clean = english.encode('ascii', 'replace').decode('ascii')
                print(f"    No translation for: {eng_clean}")
                continue
            
            # Replace just the placeholder text inside parentheses
            content = content[:pos] + f"（{chinese}）" + content[match.end():]
            total_replaced += 1

    if content != original:
        basename = os.path.basename(filepath)
        # Try writing to the working directory (might be allowed)
        cwd = os.getcwd()
        outpath = os.path.join(cwd, basename)
        try:
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"OK {basename}: {total_replaced} replacements to {outpath}")
            return total_replaced, outpath
        except (PermissionError, OSError):
            pass
        
        # Fallback 1: Write to a system temp directory
        import tempfile
        try:
            td = tempfile.gettempdir()
            outpath = os.path.join(td, basename)
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"OK {basename}: {total_replaced} replacements to {outpath}")
            return total_replaced, outpath
        except (PermissionError, OSError):
            print(f"OK {basename}: {total_replaced} replacements")
            return total_replaced, None
    else:
        print(f"NO {os.path.basename(filepath)}")
        return 0, None


def main():
    files = sorted(glob.glob(os.path.join(BASE_DIR, "osrs-*.html")))
    counts = {}
    
    for fp in files:
        c, _ = process_file(fp)
        if c > 0:
            counts[os.path.basename(fp)] = c
    
    print(f"\n{'='*60}")
    print(f"FIX SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {len(files)}")
    print(f"Files with fixes: {len(counts)}")
    total = sum(counts.values())
    print(f"Total replacements: {total}")
    for f, c in sorted(counts.items()):
        print(f"  {f}: {c}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
