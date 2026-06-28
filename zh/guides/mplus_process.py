#!/usr/bin/env python3
"""
M+ Format Processor for 8 OSRS Guide Files
Adds: Chinese H1, Chinese summary, Chinese translations for H2/H3
"""
import re
import os

FILES_DIR = "C:/Users/Lenovo/osrs-guide-site/zh/guides"

# ============================================================
# FILE DATA: Chinese H1 titles, summaries, and H2/H3 translations
# ============================================================

FILE_DATA = {
    "osrs-sailing-1-99-guide-2026.html": {
        "cn_h1": "OSRS 航海1-99完整指南2026 — 最快路线、AFK与收益",
        "cn_summary": "掌握OSRS航海技能从1级到99级的完整指南。涵盖Barracuda Trials最快路线（70-80小时）、AFK打捞路线（160小时）、船只升级、船员配置、经验值速率和收益分析。2026年6月更新。",
        "h2_h3": {
            # Table of Contents
            '📑 Table of Contents': '📑 目录',
            # Section 1
            '1. How to Start Sailing in OSRS': '1. 如何在OSRS中开始航海（如何在OSRS中开始航海）',
            # Section 2
            '2. How Sailing Works — 5 Core Training Activities': '2. 航海机制 — 5种核心训练活动（航海机制 — 5种核心训练活动）',
            '📋 Port Tasks (Level 1+)': '📋 港口任务（港口任务，1级+）',
            '🗺️ Sea Charting (Level 1+)': '🗺️ 海域测绘（海域测绘，1级+）',
            '⚓ Shipwreck Salvaging (Level 15+) — The AFK King': '⚓ 沉船打捞（沉船打捞，15级+）— AFK王者',
            '🏎️ Barracuda Trials (Level 30+) — Fastest XP': '🏎️ Barracuda试炼（Barracuda试炼，30级+）— 最快经验值',
            '🐟 Deep Sea Trawling (Level 50+)': '🐟 深海拖网（深海拖网，50级+）',
            # Section 3
            '3. The Fastest 1-99 Sailing Route (70–80 Hours)': '3. 最快1-99航海路线（最快1-99航海路线，70-80小时）',
            # Section 4
            '4. AFK 1-99 Sailing Path (~160 Hours)': '4. AFK 1-99航海路径（AFK 1-99航海路径，约160小时）',
            # Section 5
            '5. Hybrid Strategy — Best of Both Worlds (~100–120 Hours)': '5. 混合策略 — 两全其美（混合策略，约100-120小时）',
            # Section 6
            '6. Boat & Crew Upgrades — When to Upgrade': '6. 船只与船员升级 — 何时升级（船只与船员升级）',
            '🛶 Boat Progression': '🛶 船只进阶（船只进阶）',
            '🔧 Key Facilities to Install': '🔧 关键设施安装（关键设施安装）',
            # Section 7
            '7. Sailing XP Table — Key Milestones': '7. 航海经验值表 — 关键里程碑（航海经验值表）',
            # Section 8
            '8. Sailing Money Making & Profit Breakdown': '8. 航海赚钱与收益分析（航海赚钱与收益分析）',
            '💰 Profit on the Way to 99': '💰 通往99级的收益（通往99级的收益）',
            '🔥 Post-99 Sailing Money Makers': '🔥 99级后航海赚钱方法（99级后航海赚钱方法）',
            # Section 9
            '9. Crew Management & Best Crew Setup': '9. 船员管理与最佳配置（船员管理与最佳配置）',
            '👥 Crew Roles': '👥 船员角色（船员角色）',
            '⭐ Best Crew Setup by Activity': '⭐ 按活动最佳船员配置（按活动最佳船员配置）',
            # Section 10
            '10. 2026 Sailing Roadmap — What\'s Coming': '10. 2026航海路线图 — 即将到来（2026航海路线图）',
            # Section 11
            '11. Pro Tips & RuneLite Plugins for Sailing': '11. 航海专业技巧与RuneLite插件（航海专业技巧与RuneLite插件）',
            '🔌 Essential RuneLite Plugins': '🔌 必备RuneLite插件（必备RuneLite插件）',
            '🧠 Expert Tips': '🧠 专家技巧（专家技巧）',
            # Section 12
            '12. Frequently Asked Questions': '12. 常见问题（常见问题）',
            # Conclusion
            '🚢 Ready to Set Sail?': '🚢 准备起航？（准备起航？）',
            # Related
            '📚 Related Guides You Might Like': '📚 你可能喜欢的相关指南（你可能喜欢的相关指南）',
            '⛵ Sailing Quick Reference': '⛵ 航海快速参考（航海快速参考）',
            # Q headings in FAQ
            'Q: Is Sailing worth training for a main account?': 'Q：航海值得主账号训练吗？（航海值得主账号训练吗？）',
            'Q: Is Sailing good for Ironmen?': 'Q：航海适合铁人模式吗？（航海适合铁人模式吗？）',
            'Q: Can I do Sailing with low combat stats?': 'Q：低战斗属性可以玩航海吗？（低战斗属性可以玩航海吗？）',
            'Q: What\'s better — AFK Salvaging or sweating Trials?': 'Q：哪个更好 — AFK打捞还是努力试炼？（AFK打捞还是努力试炼？）',
            'Q: When should I upgrade from Skiff to Sloop?': 'Q：何时从小艇升级到单桅帆船？（何时从小艇升级到单桅帆船？）',
            'How Long Does It Take to Get 99 Sailing?': '如何快速达到99级航海？',
        }
    },

    "osrs-skills-overview-beginner-2026.html": {
        "cn_h1": "OSRS 新手技能总览2026 — 全部23项技能简单解析",
        "cn_summary": "OSRS拥有23项技能，听起来很多——确实如此。但你不需要第一天就全部理解。本指南用简单语言解析每项技能，解释哪些对新手最重要，并给出训练优先级顺序。",
        "h2_h3": {
            '① Table of Contents': '① 目录（目录）',
            '1. What Are Skills in OSRS?': '1. OSRS中的技能是什么？（OSRS中的技能是什么？）',
            '② The 4 Categories (23 Skills Total)': '② 4大类别（4大类别，共23项技能）',
            '2. Combat Skills — Your Foundation': '2. 战斗技能 — 你的基础（战斗技能 — 你的基础）',
            '② The 7 Combat Skills': '② 七大战斗技能（七大战斗技能）',
            '3. Production Skills — Make Useful Items': '3. 生产技能 — 制作有用物品（生产技能 — 制作有用物品）',
            '③ The 6 Production Skills': '③ 六大生产技能（六大生产技能）',
            '🍳 Cooking: The #1 Beginner Production Skill': '🍳 烹饪：新手第一生产技能（烹饪：新手第一生产技能）',
            '4. Gathering Skills — Collect Resources': '4. 采集技能 — 收集资源（采集技能 — 收集资源）',
            '④ The 5 Gathering Skills': '④ 五大采集技能（五大采集技能）',
            '5. Support Skills — Quality of Life & Unlocks': '5. 支持技能 — 生活品质与解锁（支持技能 — 生活品质与解锁）',
            '⑤ The 5 Support Skills': '⑤ 五大支持技能（五大支持技能）',
            '⚡ Slayer: The Most Important Mid-Game Skill': '⚡ 杀戮：最重要的中期技能（杀戮：最重要的中期技能）',
            '6. F2P vs Members Skills — What\'s Available?': '6. 免费与会员技能 — 有哪些可用？（免费与会员技能）',
            '7. Which Skills Should YOU Train First? (Priority Order)': '7. 你应该先训练哪些技能？（你应该先训练哪些技能？优先级顺序）',
            '🥇 Priority 1: Combat Skills (Attack → Strength → Defence)': '🥇 优先级1：战斗技能（优先级1：战斗技能，攻击→力量→防御）',
            '🥈 Priority 2: Cooking + Fishing (or Mining + Smithing)': '🥈 优先级2：烹饪+钓鱼（优先级2：烹饪+钓鱼，或采矿+锻造）',
            '🥉 Priority 3: One Support Skill (Agility or Thieving)': '🥉 优先级3：一项支持技能（优先级3：一项支持技能，敏捷或盗窃）',
            '8. How Skills Connect to Quests': '8. 技能如何与任务关联（技能如何与任务关联）',
            '⑥ Important Quest Chains and Their Skill Requirements': '⑥ 重要任务链及其技能要求（重要任务链及其技能要求）',
            '9. Skills That Make You Money (The Profit Skills)': '9. 能赚钱的技能（能赚钱的技能，获利技能）',
            '10. Your First 10 Skills — Priority Order Roadmap': '10. 你的前10项技能 — 优先级路线图（前10项技能优先级路线图）',
            '📅 Month 1 Skill Roadmap': '📅 第一个月技能路线图（第一个月技能路线图）',
            'Frequently Asked Questions — OSRS Skills': '常见问题 — OSRS技能（常见问题 — OSRS技能）',
            'Final Tips — Skills Overview for Beginners': '最终建议 — 新手技能总览（最终建议 — 新手技能总览）',
            '🎯 Your First Skill Goals — A Quick Checklist': '🎯 你的第一个技能目标 — 快速清单（你的第一个技能目标快速清单）',
            '⑦ 📊 What to Do After This Guide': '⑦ 📊 本指南之后做什么（本指南之后做什么）',
            '⑧ 📚 Continue the Beginner Series': '⑧ 📚 继续新手系列（继续新手系列）',
            '💰 The Gathering → Production Loop': '💰 采集→生产循环（采集→生产循环）',
            '💡 Prayer Is Different': '💡 祈祷与众不同（祈祷与众不同）',
            '💡 My Recommendation: Play F2P for 1-2 Weeks First': '💡 我的建议：先玩1-2周免费版（我的建议：先玩1-2周免费版）',
            '💡 Beginner Money-Making Strategy: The 3-Step Loop': '💡 新手赚钱策略：三步循环（新手赚钱策略：三步循环）',
            '🧩 Quest Strategy: Do Quests That Give XP Rewards Early': '🧩 任务策略：尽早做给经验奖励的任务（任务策略：尽早做给经验奖励的任务）',
            '🗺️ What to Read Next': '🗺️ 下一步阅读（下一步阅读）',
        }
    },

    "osrs-skills-progression-path-2026.html": {
        "cn_h1": "OSRS 技能发展路径2026 — 玩家最佳路线",
        "cn_summary": "合理规划OSRS技能发展是提高效率、避免浪费时间的关键。本指南提供针对不同游戏风格和发展目标的战略性技能发展路径，帮助您规划最佳技能顺序，最大化效率。",
        "h2_h3": {
            'Table of Contents': '目录（目录）',
            'Understanding Skill Dependencies & Prerequisites': '理解技能依赖关系与前提条件（理解技能依赖关系与前提条件）',
            'What Are Skill Dependencies?': '什么是技能依赖关系？（什么是技能依赖关系？）',
            'Combat-Based Dependencies': '基于战斗的依赖关系（基于战斗的依赖关系）',
            'Production-Based Dependencies': '基于生产的依赖关系（基于生产的依赖关系）',
            'Quest & Content Prerequisites': '任务与内容前提条件（任务与内容前提条件）',
            'Dependency Priority Matrix': '依赖优先级矩阵（依赖优先级矩阵）',
            'Early, Mid, and Late-Game Progression Phases': '前期、中期和后期发展阶段（前期、中期和后期发展阶段）',
            'Early-Game Phase (0-40 Total Level)': '前期阶段（前期阶段，0-40总等级）',
            'Early-Mid-Game Phase (40-70 Total Level)': '前中期阶段（前中期阶段，40-70总等级）',
            'Mid-Game Phase (70-85 Total Level)': '中期阶段（中期阶段，70-85总等级）',
            'Late-Game Phase (85-99 Total Level)': '后期阶段（后期阶段，85-99总等级）',
            'Milestone Checklist': '里程碑清单（里程碑清单）',
            'Playstyle-Specific Progression Paths': '按游戏风格的发展路径（按游戏风格的发展路径）',
            'The Casual Completionist Path': '休闲完成主义者路径（休闲完成主义者路径）',
            'The Hardcore Money-Maker Path': '硬核赚钱者路径（硬核赚钱者路径）',
            'The PvP Combat Specialist Path': 'PvP战斗专家路径（PvP战斗专家路径）',
            'The Boss Raider Path': 'Boss攻略者路径（Boss攻略者路径）',
            'The AFK-Friendly Path': 'AFK友好路径（AFK友好路径）',
            'Progression Path Comparison': '发展路径对比（发展路径对比）',
            'Return on Investment Analysis: Time vs. Benefits': '投资回报分析：时间 vs. 收益（投资回报分析：时间 vs. 收益）',
            'Understanding Skill ROI': '理解技能ROI（理解技能ROI）',
            'Exceptional ROI Skills (Early-Game Priority)': '卓越ROI技能（卓越ROI技能，前期优先）',
            'Good ROI Skills (Mid-Game Focus)': '良好ROI技能（良好ROI技能，中期重点）',
            'Mediocre ROI Skills (Optional Specialization)': '一般ROI技能（一般ROI技能，可选专精）',
            'Low ROI Skills (Late-Game Only)': '低ROI技能（低ROI技能，仅后期）',
            'ROI Calculation Example': 'ROI计算示例（ROI计算示例）',
            'Common Progression Mistakes & How to Avoid Them': '常见发展错误及如何避免（常见发展错误及如何避免）',
            'Mistake 1: Training Skills in Random Order': '错误1：随机顺序训练技能（错误1：随机顺序训练技能）',
            'Mistake 2: Ignoring Prayer Too Long': '错误2：忽视祈祷太久（错误2：忽视祈祷太久）',
            'Mistake 3: Over-Investing in Low-ROI Skills': '错误3：过度投资低ROI技能（错误3：过度投资低ROI技能）',
            'Mistake 4: Not Planning for Quest Requirements': '错误4：未规划任务要求（错误4：未规划任务要求）',
            'Mistake 5: Ignoring Your Playstyle': '错误5：忽视你的游戏风格（错误5：忽视你的游戏风格）',
            'Mistake 6: Rushing to 99s Too Early': '错误6：过早冲刺99级（错误6：过早冲刺99级）',
            'Mistake 7: Not Using Available Resources': '错误7：未利用可用资源（错误7：未利用可用资源）',
            'Final Strategic Tips for Optimal Progression': '优化发展的最终策略建议（优化发展的最终策略建议）',
            'Monthly Checkpoint System': '月度检查点系统（月度检查点系统）',
            'Quest-Gated Skill Requirements': '任务锁定的技能要求（任务锁定的技能要求）',
            'Ready to Optimize Your Progression?': '准备好优化你的发展了吗？（准备好优化你的发展了吗？）',
            'Frequently Asked Questions': '常见问题（常见问题）',
            "What's the absolute fastest path to late-game viability?": "达到后期可行性的绝对最快路径是什么？（达到后期可行性的绝对最快路径是什么？）",
            'Should I pursue 99s early or spread skills evenly?': '应该早期追求99级还是均匀分配技能？（应该早期追求99级还是均匀分配技能？）',
            "How do I know which playstyle is right for me?": "如何知道哪种游戏风格适合我？（如何知道哪种游戏风格适合我？）",
            'Is Prayer training expensive?': '祈祷训练贵吗？（祈祷训练贵吗？）',
            'Can I skip any skills entirely?': '我可以完全跳过某些技能吗？（我可以完全跳过某些技能吗？）',
            "What if I've already trained in suboptimal order?": "如果我已经以次优顺序训练了怎么办？（如果我已经以次优顺序训练了怎么办？）",
            'How often should I update my progression plan?': '我应该多久更新一次发展计划？（我应该多久更新一次发展计划？）',
            'Related Progression Guides': '相关发展指南（相关发展指南）',
        }
    },

    "osrs-skill-training-after-sweep-up-2026.html": {
        "cn_h1": "OSRS Summer Sweep-Up 2026后技能训练 — 变化与新最佳经验方法",
        "cn_summary": "Summer Sweep-Up 2026改变了OSRS训练格局。本指南全面解析每项受影响技能的变化、新的最佳经验值方法、以及所有23项技能的更新训练优先级。如果您仍在使用更新前的训练路线，那是在浪费时间。",
        "h2_h3": {
            'Table of Contents': '目录（目录）',
            '1. Summer Sweep-Up Impact on Skills — Overview': '1. Summer Sweep-Up对技能的影响 — 概述（Summer Sweep-Up对技能的影响）',
            '📊 Which Skills Were Affected Most?': '📊 哪些技能受影响最大？（哪些技能受影响最大？）',
            '🔴 Major Overhaul (Training Method Changed Significantly)': '重大改革',
            '🟡 Moderate Changes (Some Methods Better/Worse)': '中等变化',
            '🟢 Minimal or No Changes': '🟢 微小或无变化（微小或无变化）',
            '🎯 Why You Need to Update Your Training Plan': '🎯 为什么需要更新训练计划（为什么需要更新训练计划）',
            '2. Skills With Major Changes': '2. 重大变化的技能（重大变化的技能）',
            '🏹 Hunter — Complete Overhaul': '🏹 猎人 — 全面改革（猎人 — 全面改革）',
            "What's New in Hunter": '猎人的新内容（猎人的新内容）',
            '🏃 Agility — New Courses & Redesigned Shortcuts': '🏃 敏捷 — 新课程与重新设计的捷径（敏捷 — 新课程与重新设计的捷径）',
            'NEW: Oo\'glog Agility Course (Level 50+)': '新增：Oo\'glog敏捷课程（新增：Oo\'glog敏捷课程，50级+）',
            'NEW: TzHaar Agility Course (Level 85+)': '新增：TzHaar敏捷课程（新增：TzHaar敏捷课程，85级+）',
            '🗡️ Thieving — Blackjack Rework & New Targets': '🗡️ 盗窃 — 21点重做与新目标（盗窃 — 21点重做与新目标）',
            'NEW: Pickpocket Dwarves (Level 65+)': '新增：扒窃矮人（新增：扒窃矮人，65级+）',
            'NEW: Pickpocket Elves (Level 80+)': '新增：扒窃精灵（新增：扒窃精灵，80级+）',
            '⛏️ Mining — Powerleveling Rebalanced': '⛏️ 采矿 — 快速升级重新平衡（采矿 — 快速升级重新平衡）',
            'NEW: Gem Rocks (Level 45+)': '新增：宝石岩（新增：宝石岩，45级+）',
            '🔨 Smithing — Blast Furnace Adjusted': '🔨 锻造 — 高炉调整（锻造 — 高炉调整）',
            '3. Skills With Minor Tweaks': '3. 微调技能（微调技能）',
            '⚔️ Combat Skills (Attack/Strength/Defence/Hitpoints)': '⚔️ 战斗技能（战斗技能：攻击/力量/防御/生命值）',
            '🔮 Magic': '🔮 魔法（魔法）',
            'New Spells Worth Knowing': '值得了解的新法术（值得了解的新法术）',
            '🌀 Runecraft': '🌀 符文制作（符文制作）',
            '🌿 Herblore': '🌿 草药学（草药学）',
            '🌱 Farming': '🌱 农耕（农耕）',
            '4. Skills That Stayed the Same': '4. 未变化的技能（未变化的技能）',
            '✅ Skills With No Meaningful Changes': '✅ 无实质变化的技能（无实质变化的技能）',
            '5. New Training Methods That Didn\'t Exist Before': '5. 前所未有的新训练方法（前所未有的新训练方法）',
            '🆕 Mangrove Sifaka Hunting (Hunter 43+)': '🆕 红树林狐猴狩猎（红树林狐猴狩猎，猎人43+）',
            '🆕 Oo\'glog Agility Course (Agility 50+)': '🆕 Oo\'glog敏捷课程（Oo\'glog敏捷课程，敏捷50+）',
            '🆕 Pickpocket Dwarves (Thieving 65+)': '🆕 扒窃矮人（扒窃矮人，盗窃65+）',
            '🆕 Sunlight Moth Catching (Hunter 80+)': '🆕 阳光飞蛾捕捉（阳光飞蛾捕捉，猎人80+）',
            '🆕 TzHaar Agility Course (Agility 85+)': '🆕 TzHaar敏捷课程（TzHaar敏捷课程，敏捷85+）',
            '🆕 Gem Rocks Mining (Mining 45+)': '🆕 宝石岩采矿（宝石岩采矿，采矿45+）',
            '6. Updated All-Skills Priority Ranking': '6. 更新后的全技能优先级排名（更新后的全技能优先级排名）',
            '7. FAQ — Summer Sweep-Up Training Questions': '7. 常见问题 — Summer Sweep-Up训练问题（常见问题）',
            '🎯 What To Do After Reading This Guide': '🎯 阅读本指南后做什么（阅读本指南后做什么）',
            'Related Guides': '相关指南（相关指南）',
            '💡 Key Takeaways From the New Ranking': '💡 新排名要点（新排名要点）',
            '💡 Smithing Takeaway': '💡 锻造要点（锻造要点）',
            '💡 The Bottom Line': '💡 底线（底线）',
            '💡 New Best Hunter Route (Post-Sweep-Up)': '新的最佳猎人路线（更新后）',
            '⚠️ Blackjack Change Warning': '⚠️ 21点变更警告（21点变更警告）',
            '💡 Herblore Cost Impact': '💡 草药学成本影响（草药学成本影响）',
            '💡 What This Means for You': '💡 这对你意味着什么（这对你意味着什么）',
        }
    },

    "osrs-skill-training-beginner-complete-guide-2026.html": {
        "cn_h1": "OSRS 新手完整技能训练指南2026 — 全部23项技能解析",
        "cn_summary": "OSRS拥有23项技能，知道哪些先练以及它们如何关联，是区别挫败新手与快速解锁终局内容玩家的关键。本指南解释每项技能、它们如何相互作用，并给出从1级到中期的完整路线图。",
        "h2_h3": {
            '① Table of Contents': '① 目录（目录）',
            '1. Understanding OSRS\'s 23 Skills — The Big Picture': '1. 理解OSRS的23项技能 — 大局观（理解OSRS的23项技能）',
            '② The 5 Categories of OSRS Skills': '② OSRS技能的5大类别（OSRS技能的5大类别）',
            'Combat Skills (7 skills)': '战斗技能（战斗技能，7项）',
            'Gathering Skills (6 skills)': '采集技能（采集技能，6项）',
            'Artisan Skills (7 skills)': '工匠技能（工匠技能，7项）',
            'Support Skills (3 skills)': '支持技能（支持技能，3项）',
            '③ How Skills Connect — The Dependency Web': '③ 技能如何连接 — 依赖网络（技能如何连接）',
            '④ Why You Should NOT Try to Max All Skills Early': '④ 为什么不应该早期尝试将所有技能练满（为什么不应该早期尝试将所有技能练满）',
            '2. Combat Skills — Your Foundation (7 Skills)': '2. 战斗技能 — 你的基础（战斗技能 — 你的基础，7项）',
            '⑤ Attack — Unlocking Better Weapons': '⑤ 攻击 — 解锁更好的武器（攻击 — 解锁更好的武器）',
            '⑥ Strength — Hitting Harder': '⑥ 力量 — 打出更高伤害（力量 — 打出更高伤害）',
            '⑦ Defence — Taking Less Damage': '⑦ 防御 — 承受更少伤害（防御 — 承受更少伤害）',
            '⑧ Hitpoints — Your Health Bar': '⑧ 生命值 — 你的血条（生命值 — 你的血条）',
            '⑨ Ranged — Distance Combat': '⑨ 远程 — 远程战斗（远程 — 远程战斗）',
            '⑩ Magic — Spells & Utility': '⑩ 魔法 — 法术与实用功能（魔法 — 法术与实用功能）',
            'Prayer — Combat Multiplier': '祈祷 — 战斗倍增器（祈祷 — 战斗倍增器）',
            'Optimal Combat Progression (Level 3 → Level 70+)': '最佳战斗进阶（最佳战斗进阶，3级到70级以上）',
            'Combat Triangle in Practice': '实战中的战斗三角（实战中的战斗三角）',
            '3. Gathering Skills — Where Resources Come From (6 Skills)': '3. 采集技能 — 资源来源（采集技能 — 资源来源，6项）',
            'Mining — Digging for Ores and Gems': '采矿 — 挖掘矿石和宝石（采矿 — 挖掘矿石和宝石）',
            'Fishing — Catching Fish for Food and GP': '钓鱼 — 钓鱼获取食物和金币（钓鱼 — 钓鱼获取食物和金币）',
            'Woodcutting — Chopping Trees for Logs': '伐木 — 砍树获取原木（伐木 — 砍树获取原木）',
            'Firemaking — Burning Logs for XP': '生火 — 烧原木获取经验（生火 — 烧原木获取经验）',
            'Farming — Growing Resources Over Time': '农耕 — 随时间种植资源（农耕 — 随时间种植资源）',
            'Farming Routine for Beginners': '新手农耕日常（新手农耕日常）',
            'Hunter — Catching Creatures for Loot': '猎人 — 捕捉生物获取战利品（猎人 — 捕捉生物获取战利品）',
            'F2P vs Member Gathering Skills': '免费版与会员版采集技能对比（免费版与会员版采集技能对比）',
            '4. Artisan Skills — Turning Raw Into Gold (7 Skills)': '4. 工匠技能 — 变原料为黄金（工匠技能 — 变原料为黄金，7项）',
            'Smithing — Making Metal Gear and Ammo': '锻造 — 制作金属装备和弹药（锻造 — 制作金属装备和弹药）',
            'Cooking — Making Food for Healing': '烹饪 — 制作回复食物（烹饪 — 制作回复食物）',
            'Crafting — Making Gear, Ammo, and Utilities': '手工艺 — 制作装备、弹药和实用物品（手工艺 — 制作装备、弹药和实用物品）',
            'Herblore — Making Potions for Buffs': '草药学 — 制作增益药水（草药学 — 制作增益药水）',
            'Herblore Training on a Budget': '预算有限的草药学训练（预算有限的草药学训练）',
            'Fletching — Making Ranged Ammunition': '制箭 — 制作远程弹药（制箭 — 制作远程弹药）',
            'Runecrafting — Making Runes for Magic': '符文制作 — 制作魔法符文（符文制作 — 制作魔法符文）',
            'Construction — Building Your Player-Owned House': '建筑 — 建造你的玩家住宅（建筑 — 建造你的玩家住宅）',
            'Artisan Skills — Profit vs Cost Summary': '工匠技能 — 利润与成本对比（工匠技能 — 利润与成本对比）',
            '5. Support Skills — The Force Multipliers (3 Skills)': '5. 支持技能 — 力量倍增器（支持技能 — 力量倍增器，3项）',
            'Agility — Move Faster, Unlock Shortcuts': '敏捷 — 移动更快，解锁捷径（敏捷 — 移动更快，解锁捷径）',
            'Thieving — Steal Items, Unlock Areas': '盗窃 — 偷窃物品，解锁区域（盗窃 — 偷窃物品，解锁区域）',
            'Slayer — The Best Combat Training Method': '杀戮 — 最佳战斗训练方法（杀戮 — 最佳战斗训练方法）',
            'When to Start Slayer': '何时开始杀戮（何时开始杀戮）',
            '6. Skill Synergy — Training Multiple Skills Together': '6. 技能协同 — 同时训练多项技能（技能协同 — 同时训练多项技能）',
            'Combo 1: Slayer = 8 Skills at Once': '组合1：杀戮 = 同时训练8项技能（组合1：杀戮 = 同时训练8项技能）',
            'Combo 2: Farming Herbs + Herblore': '组合2：农耕草药 + 草药学（组合2：农耕草药 + 草药学）',
            'Combo 3: Questing = Multiple Skills + Unlocks': '组合3：做任务 = 多项技能 + 解锁（组合3：做任务 = 多项技能 + 解锁）',
            'Sample "Synergy Schedule" for a New Member': '新会员的"协同日程"示例（新会员的"协同日程"示例）',
            '7. Common Beginner Mistakes in Skill Training': '7. 技能训练中新手的常见错误（技能训练中新手的常见错误）',
            '8. Your First Month Skill Plan': '8. 你的第一个月技能计划（你的第一个月技能计划）',
            '9. Skill Training FAQs': '9. 技能训练常见问题（技能训练常见问题）',
            'What To Do After Reading This Guide': '阅读本指南后做什么（阅读本指南后做什么）',
            'Continue Your Skill Training Journey': '继续你的技能训练之旅（继续你的技能训练之旅）',
            'The Golden Rule of OSRS Skill Training': 'OSRS技能训练的黄金法则（OSRS技能训练的黄金法则）',
            'Mining Tip': '采矿技巧（采矿技巧）',
            'Smithing Cost Warning': '锻造成本警告（锻造成本警告）',
            'Runecrafting Alternative': '符文制作替代方案（符文制作替代方案）',
            'Graceful Armor — Why Agility Matters': '优雅套装 — 为什么敏捷重要（优雅套装 — 为什么敏捷重要）',
        }
    },

    "osrs-skill-training-beginner-fast-track-2026.html": {
        "cn_h1": "OSRS 快速通道技能指南 — 30天达到中期数据（2026）",
        "cn_summary": '你刚创建新账号或成为会员，想在30天内达到「中期就绪」状态。本指南提供精确的逐日计划——训练什么、在哪里训练、带什么物品、需要多少金币。没有废话，只有行动。',
        "h2_h3": {
            '① Table of Contents': '① 目录（目录）',
            '1. What "Mid-Game Ready" Looks Like': '1. "中期就绪"是什么样？（"中期就绪"是什么样？）',
            '🎯 Target Stats After 30 Days': '🎯 30天后目标数据（30天后目标数据）',
            '② Prerequisites Before Starting': '② 开始前的必要条件（开始前的必要条件）',
            '2. Week 1: Combat Foundation (Days 1-7)': '2. 第1周：战斗基础（第1周：战斗基础，第1-7天）',
            '📅 Week 1 Daily Schedule (2-3 hours/day)': '📅 第1周每日计划（第1周每日计划，2-3小时/天）',
            '③ 🗺️ Exact Training Locations (Week 1)': '③ 🗺️ 精确训练地点（精确训练地点，第1周）',
            'Location 1: Chickens (Lumbridge)': '地点1：鸡（地点1：鸡，Lumbridge）',
            'Location 2: Cows (Lumbridge Swamp)': '地点2：牛（地点2：牛，Lumbridge Swamp）',
            'Location 3: Al-Kharid Warriors (F2P) or Moss Giants (Members)': '地点3：Al-Kharid战士（地点3：Al-Kharid战士（免费版）或苔藓巨人（会员版））',
            'Week 1 Pro Tip': '第1周专业提示（第1周专业提示）',
            '3. Week 2: Gathering & First GP (Days 8-14)': '3. 第2周：采集与第一桶金（第2周：采集与第一桶金，第8-14天）',
            '📅 Week 2 Daily Schedule (2-3 hours/day)': '📅 第2周每日计划（第2周每日计划，2-3小时/天）',
            '④ 🗺️ Exact Training Locations (Week 2)': '④ 🗺️ 精确训练地点（精确训练地点，第2周）',
            'Mining Iron — Best XP + GP': '采矿铁矿石 — 最佳经验+金币（采矿铁矿石 — 最佳经验+金币）',
            'Fishing Lobsters — Food + GP': '钓鱼龙虾 — 食物+金币（钓鱼龙虾 — 食物+金币）',
            'Woodcutting Willows — AFK XP': '伐木柳树 — AFK经验（伐木柳树 — AFK经验）',
            'Week 2 Pro Tip': '第2周专业提示（第2周专业提示）',
            '4. Week 3: Artisan & Support Skills (Days 15-21)': '4. 第3周：工匠与支持技能（第3周：工匠与支持技能，第15-21天）',
            '📅 Week 3 Daily Schedule (2-3 hours/day)': '📅 第3周每日计划（第3周每日计划，2-3小时/天）',
            '⑤ Cooking Training — Efficient Method': '⑤ 烹饪训练 — 高效方法（烹饪训练 — 高效方法）',
            'Levels 1-40: Cook Fish From Fishing': '1-40级：烹饪钓鱼获得的鱼（1-40级：烹饪钓鱼获得的鱼）',
            '⑥ Crafting Training — Leather Armor': '⑥ 手工艺训练 — 皮甲（手工艺训练 — 皮甲）',
            'Levels 1-30: Leather From Cows': '1-30级：用牛皮制作皮革（1-30级：用牛皮制作皮革）',
            '⑦ Agility Training — Gnome Stronghold': '⑦ 敏捷训练 — Gnome要塞（敏捷训练 — Gnome要塞）',
            'Levels 1-30: Gnome Stronghold Agility Course': '1-30级：Gnome要塞敏捷课程（1-30级：Gnome要塞敏捷课程）',
            'Week 3 Pro Tip': '第3周专业提示（第3周专业提示）',
            '5. Week 4: Polishing & Preparation (Days 22-30)': '5. 第4周：打磨与准备（第4周：打磨与准备，第22-30天）',
            '📅 Week 4 Daily Schedule (2-3 hours/day)': '📅 第4周每日计划（第4周每日计划，2-3小时/天）',
            '⑧ 🗺️ Rock Crabs — Best Combat Training (Levels 50-70)': '⑧ 🗺️ 岩石蟹 — 最佳战斗训练（岩石蟹 — 最佳战斗训练，50-70级）',
            'Why Rock Crabs?': '为什么选岩石蟹？（为什么选岩石蟹？）',
            '⑨ 🙏 Getting Prayer 43 — Protect Prayers': '⑨ 🙏 达到祈祷43级 — 保护祈祷（达到祈祷43级 — 保护祈祷）',
            'Method 1: Bury Bones (Free but Slow)': '方法1：埋骨（方法1：埋骨，免费但慢）',
            'Method 2: Gilded Altar (Members, Fast)': '方法2：镀金祭坛（方法2：镀金祭坛，会员版，快速）',
            '⑩ ⚔️ Starting Slayer — Talk to Turael': '⑩ ⚔️ 开始杀戮 — 与Turael交谈（开始杀戮 — 与Turael交谈）',
            'How to Start Slayer': '如何开始杀戮（如何开始杀戮）',
            'Week 4 Pro Tip': '第4周专业提示（第4周专业提示）',
            '6. Alternative Schedules (1hr/5hrs + Ironman + F2P)': '6. 替代计划（6. 替代计划，1小时/5小时 + 铁人模式 + 免费版）',
            '⏱️ Schedule A: 1 Hour/Day (60-Day Version)': '⏱️ 计划A：每天1小时（计划A：每天1小时，60天版）',
            '⏱️ Schedule B: 5+ Hours/Day (15-Day Version)': '⏱️ 计划B：每天5小时以上（计划B：每天5小时以上，15天版）',
            '⚔️ Ironman Adjustments': '⚔️ 铁人模式调整（铁人模式调整）',
            '🆓 F2P-Only Version (Before Membership)': '🆓 仅免费版（仅免费版，成为会员前）',
            'Which Schedule Should You Use?': '应该使用哪种计划？（应该使用哪种计划？）',
            '7. Budget Breakdown — 30-Day Cost': '7. 预算明细 — 30天成本（预算明细 — 30天成本）',
            '💰 Total 30-Day Budget Summary': '💰 30天总预算概要（30天总预算概要）',
            '💡 How to Make GP During the 30-Day Plan': '💡 30天计划中如何赚钱（30天计划中如何赚钱）',
            'Budget Pro Tip': '预算专业提示（预算专业提示）',
            '8. Progress Tracker & FAQ': '8. 进度追踪器与常见问题（进度追踪器与常见问题）',
            '✅ 30-Day Progress Tracker': '✅ 30天进度追踪器（30天进度追踪器）',
            '📋 FAQ — Fast Track Skill Guide': '📋 常见问题 — 快速通道技能指南（常见问题 — 快速通道技能指南）',
            'What To Do After 30 Days': '30天后做什么（30天后做什么）',
            'Related Skill Training Guides': '相关技能训练指南（相关技能训练指南）',
        }
    },

    "osrs-skill-training-endgame-guide-2026.html": {
        "cn_h1": "OSRS 终局技能训练指南2026 — 70到99级方法与策略",
        "cn_summary": "你已达到70级，真正的磨练才刚刚开始。本权威指南涵盖从70到99训练所有23项技能的最快、最便宜和最聪明的方法，包括详细成本分析、tick操作技术和战略性99优先级路线图。",
        "h2_h3": {
            'Table of Contents': '目录（目录）',
            '1. The Endgame Skill Landscape': '1. 终局技能概览（终局技能概览）',
            '📊 The XP Curve: What 70→99 Really Means': '📊 经验曲线：70→99的真正含义（经验曲线：70→99的真正含义）',
            '🎯 Three Phases of 70→99': '🎯 70→99的三个阶段（70→99的三个阶段）',
            'Phase 1: Levels 70–80 (Transition)': '阶段1：70-80级（阶段1：70-80级，过渡期）',
            'Phase 2: Levels 80–92 (The Long Middle — "Halfway")': '阶段2：80-92级（阶段2：80-92级，漫长的中途）',
            'Phase 3: Levels 92–99 (The Final Push)': '阶段3：92-99级（阶段3：92-99级，最后冲刺）',
            '🔓 Key Level Unlocks That Redefine Skills': '🔓 重新定义技能的关键等级解锁（关键等级解锁）',
            '2. Fastest 99 Methods Per Skill (Complete Rankings)': '2. 每项技能最快99级方法（每项技能最快99级方法，完整排名）',
            '⚔️ Combat Skills (7)': '⚔️ 战斗技能（战斗技能，7项）',
            'Attack / Strength / Defence (70→99)': '攻击/力量/防御（攻击/力量/防御，70→99）',
            'Hitpoints (70→99)': '生命值（生命值，70→99）',
            'Ranged (70→99)': '远程（远程，70→99）',
            'Magic (70→99)': '魔法（魔法，70→99）',
            'Prayer (70→99)': '祈祷（祈祷，70→99）',
            '🌲 Gathering Skills (6)': '🌲 采集技能（采集技能，6项）',
            'Mining (70→99)': '采矿（采矿，70→99）',
            'Fishing (70→99)': '钓鱼（钓鱼，70→99）',
            'Woodcutting (70→99)': '伐木（伐木，70→99）',
            'Firemaking (70→99)': '生火（生火，70→99）',
            'Farming (70→99)': '农耕（农耕，70→99）',
            'Hunter (70→99)': '猎人（猎人，70→99）',
            '🛠️ Artisan Skills (7)': '🛠️ 工匠技能（工匠技能，7项）',
            'Smithing (70→99)': '锻造（锻造，70→99）',
            'Cooking (70→99)': '烹饪（烹饪，70→99）',
            'Crafting (70→99)': '手工艺（手工艺，70→99）',
            'Herblore (70→99)': '草药学（草药学，70→99）',
            'Fletching (70→99)': '制箭（制箭，70→99）',
            'Runecrafting (70→99)': '符文制作（符文制作，70→99）',
            'Construction (70→99)': '建筑（建筑，70→99）',
            '🏃 Support Skills (3)': '🏃 支持技能（支持技能，3项）',
            'Agility (70→99)': '敏捷（敏捷，70→99）',
            'Thieving (70→99)': '盗窃（盗窃，70→99）',
            'Slayer (70→99)': '杀戮（杀戮，70→99）',
            '3. The Most Expensive 99s (And How to Fund Them)': '3. 最贵的99级（最贵的99级及如何筹集资金）',
            '💰 Complete 99 Cost Rankings (70→99)': '💰 完整99级成本排名（完整99级成本排名，70→99）',
            '🎯 Funding Strategy: The Synergy Map': '🎯 资金策略：协同图谱（资金策略：协同图谱）',
            'Synergy 1: Slayer → All Buyables': '协同1：杀戮 → 所有可购买技能（协同1：杀戮 → 所有可购买技能）',
            'Synergy 2: Runecrafting (Soul) → Herblore + Construction': '协同2：符文制作（灵魂符文）→ 草药学 + 建筑（协同2：符文制作 → 草药学 + 建筑）',
            'Synergy 3: Hunter (Chins) → Ranged + Fletching': '协同3：猎人（Chins）→ 远程 + 制箭（协同3：猎人 → 远程 + 制箭）',
            'Synergy 4: Bossing → All Buyables': '协同4：打Boss → 所有可购买技能（协同4：打Boss → 所有可购买技能）',
            '📈 GP/Hour by Endgame Activity': '📈 终局活动每小时金币（终局活动每小时金币）',
            '4. Recommended 99 Order — Tier System': '4. 推荐的99级顺序 — 分级系统（推荐的99级顺序 — 分级系统）',
            '🥇 Tier 1: Foundation 99s (Do These First)': '🥇 第一梯队：基础99级（第一梯队：基础99级，先做这些）',
            '1. Slayer (to 93+ or 99)': '1. 杀戮（杀戳，到93+或99级）',
            '2. Runecrafting (to 90+)': '2. 符文制作（符文制作，到90+级）',
            '3. Hunter (to 99)': '3. 猎人（猎人，到99级）',
            '4. Farming (to 99)': '4. 农耕（农耕，到99级）',
            '5. Magic (to 99)': '5. 魔法（魔法，到99级）',
            '🥈 Tier 2: High-Value 99s (Medium Priority)': '🥈 第二梯队：高价值99级（第二梯队：高价值99级，中等优先级）',
            'Ranged (99)': '远程（99级）',
            'Prayer (99)': '祈祷（99级）',
            'Cooking (99)': '烹饪（99级）',
            'Fishing + Cooking (Together)': '钓鱼 + 烹饪（钓鱼 + 烹饪，一起练）',
            'Agility (99)': '敏捷（99级）',
            '🥉 Tier 3: Expensive/Low-Priority 99s (Save for Last)': '🥉 第三梯队：昂贵/低优先级99级（第三梯队：昂贵/低优先级99级，留到最后）',
            'Construction (99)': '建筑（99级）',
            'Herblore (99)': '草药学（99级）',
            'Smithing (99)': '锻造（99级）',
            'Fletching (99)': '制箭（99级）',
            '5. Advanced Tick-Manipulation Methods': '5. 高级Tick操作技巧（高级Tick操作技巧）',
            '⏱️ What Is a Game Tick?': '⏱️ 什么是游戏Tick？（什么是游戏Tick？）',
            '🎯 Entry-Level 3-Tick Methods (Worth Learning)': '🎯 入门级3-Tick方法（入门级3-Tick方法，值得学习）',
            '3-Tick Mining (Copper/Tin/Iron)': '3-Tick采矿（3-Tick采矿，铜/锡/铁）',
            '3-Tick Woodcutting (Normal→Oak→Willow)': '3-Tick伐木（3-Tick伐木，普通→橡木→柳树）',
            '🔥 Advanced 1-Tick & 2-Tick Methods (High APM)': '🔥 高级1-Tick和2-Tick方法（高级1-Tick和2-Tick方法，高APM）',
            '1-Tick Fletching (Dragon Darts)': '1-Tick制箭（1-Tick制箭，龙镖）',
            '2-Tick Cooking (Wine)': '2-Tick烹饪（2-Tick烹饪，葡萄酒）',
            '❌ Skills NOT Worth Tick Manipulating': '❌ 不值得Tick操作的技能（不值得Tick操作的技能）',
            '6. Managing Burnout on Long Grinds': '6. 管理长期练级中的倦怠（管理长期练级中的倦怠）',
            '📅 Set Milestone Goals (Not Just "99")': '📅 设定里程碑目标（设定里程碑目标，不只是"99"）',
            '🎮 Train Multiple Skills in Parallel': '🎮 并行训练多项技能（并行训练多项技能）',
            'The "Rotation Method"': '"轮换方法"（"轮换方法"）',
            '📺 Passive Training While Consuming Content': '📺 消费内容时的被动训练（消费内容时的被动训练）',
            '🏆 Track Progress Visually': '🏆 可视化追踪进度（可视化追踪进度）',
            '🤝 Join a Clan': '🤝 加入一个公会（加入一个公会）',
            '🔄 Take Planned Breaks (Not Unplanned Burnout)': '🔄 有计划地休息（有计划地休息，而非意外倦怠）',
            '7. Endgame Skill Requirements Checklist': '7. 终局技能要求清单（终局技能要求清单）',
            '🏅 Quest Requirements (Notable Skills)': '🏅 任务要求（任务要求，重要技能）',
            '🎯 Achievement Diary Requirements': '🎯 成就日记要求（成就日记要求）',
            'Easy Diaries': '简单日记（简单日记）',
            'Medium Diaries': '中等日记（中等日记）',
            'Hard Diaries': '困难日记（困难日记）',
            'Elite Diaries': '精英日记（精英日记）',
            '🗡️ Boss Entry Requirements': '🗡️ Boss进入要求（Boss进入要求）',
            '🏆 Max Cape Path': '🏆 Max披风路径（Max披风路径）',
            '8. Endgame Training FAQs': '8. 终局训练常见问题（终局训练常见问题）',
            '🎯 What to Do After Reading This Guide': '🎯 阅读本指南后做什么（阅读本指南后做什么）',
            'Continue Your Endgame Journey': '继续你的终局之旅（继续你的终局之旅）',
            '💡 The 92 Soul Runecrafting Rule': '💡 92级灵魂符文制作规则（92级灵魂符文制作规则）',
            '💡 The "Big 4" Expense Problem': '💡 "四大"费用问题（"四大"费用问题）',
            '🏆 The "Optimal" Order for Most Players': '🏆 大多数玩家的"最佳"顺序（大多数玩家的"最佳"顺序）',
            '⚠️ Tick Manipulation and the "Efficiency" Trap': '⚠️ Tick操作与"效率"陷阱（Tick操作与"效率"陷阱）',
            '💡 The "5% Rule"': '💡 "5%规则"（"5%规则"）',
            '⚠️ The "GP Burnout" Trap': '⚠️ "金币倦怠"陷阱（"金币倦怠"陷阱）',
            '💡 The "Step Away" Test': '💡 "暂停"测试（"暂停"测试）',
        }
    },

    "osrs-skill-training-max-account-2026.html": {
        "cn_h1": "OSRS 满级账号技能规划2026 — 通往2277总等级之路",
        "cn_summary": "达到2277总等级并解锁Max披风是Old School RuneScape中的终极账号目标。本综合指南涵盖从中期到满级的完整路线图，包括现实时间估算、金币预算计算、技能协同效应以及磨练数百小时所需的心态。",
        "h2_h3": {
            'Table of Contents': '目录（目录）',
            '1. The Max Cape — Why Go For 2277?': '1. Max披风 — 为什么要追求2277？（Max披风 — 为什么要追求2277？）',
            '🏆 What the Max Cape Actually Gives You': '🏆 Max披风实际给你什么（Max披风实际给你什么）',
            'Max Cape Stats & Benefits': 'Max披风属性与好处（Max披风属性与好处）',
            '💰 Total Cost — An Honest Estimate': '💰 总成本 — 诚实估算（总成本 — 诚实估算）',
            '🎯 Who Should Pursue Max Cape?': '🎯 谁应该追求Max披风？（谁应该追求Max披风？）',
            'Max Cape is Right For You If:': 'Max披风适合你如果：（Max披风适合你如果：）',
            'Max Cape is NOT Right For You If:': 'Max披风不适合你如果：（Max披风不适合你如果：）',
            '2. Full Skills Roadmap to 2277': '2. 完整技能路线图到2277（完整技能路线图到2277）',
            '⚔️ Phase 1: Combat First (1,000 → ~1,400 Total)': '⚔️ 第一阶段：战斗优先（第一阶段：战斗优先，1,000到约1,400总等级）',
            'Step 1.1: Strength to 99 (Do This First)': '步骤1.1：力量到99级（步骤1.1：力量到99级，先做这个）',
            'Step 1.2: Attack to 99': '步骤1.2：攻击到99级（步骤1.2：攻击到99级）',
            'Step 1.3: Defence to 99': '步骤1.3：防御到99级（步骤1.3：防御到99级）',
            'Step 1.4: Ranged to 99': '步骤1.4：远程到99级（步骤1.4：远程到99级）',
            'Step 1.5: Magic to 99': '步骤1.5：魔法到99级（步骤1.5：魔法到99级）',
            'Step 1.6: Hitpoints to 99': '步骤1.6：生命值到99级（步骤1.6：生命值到99级）',
            '⚡ Phase 2: Fast Skiller 99s (1,400 → ~1,700 Total)': '⚡ 第二阶段：快速技能99级（第二阶段：快速技能99级，1,400到约1,700总等级）',
            '2.1: Cooking to 99 (8 hours)': '2.1：烹饪到99级（2.1：烹饪到99级，8小时）',
            '2.2: Fletching to 99 (27 hours)': '2.2：制箭到99级（2.2：制箭到99级，27小时）',
            '2.3: Firemaking to 99 (90 hours)': '2.3：生火到99级（2.3：生火到99级，90小时）',
            '2.4: Crafting to 99 (52 hours)': '2.4：手工艺到99级（2.4：手工艺到99级，52小时）',
            '2.5: Thieving to 99 (54 hours)': '2.5：盗窃到99级（2.5：盗窃到99级，54小时）',
            '🌲 Phase 3: Slow Gathering 99s (1,700 → ~1,950 Total)': '🌲 第三阶段：慢速采集99级（第三阶段：慢速采集99级，1,700到约1,950总等级）',
            '3.1: Agility to 99 (160 hours)': '3.1：敏捷到99级（3.1：敏捷到99级，160小时）',
            '3.2: Mining to 99 (181 hours)': '3.2：采矿到99级（3.2：采矿到99级，181小时）',
            '3.3: Woodcutting to 99 (136 hours)': '3.3：伐木到99级（3.3：伐木到99级，136小时）',
            '3.4: Fishing to 99 (160 hours)': '3.4：钓鱼到99级（3.4：钓鱼到99级，160小时）',
            '3.5: Hunter to 99 (72 hours)': '3.5：猎人到99级（3.5：猎人到99级，72小时）',
            '💰 Phase 4: Expensive 99s (1,950 → ~2,200 Total)': '💰 第四阶段：昂贵99级（第四阶段：昂贵99级，1,950到约2,200总等级）',
            '4.1: Prayer to 99 (54 hours, 28M GP)': '4.1：祈祷到99级（4.1：祈祷到99级，54小时，2800万金币）',
            '4.2: Runecrafting to 99 (64 hours, FREE / +40M GP profit)': '4.2：符文制作到99级（4.2：符文制作到99级，64小时，免费/赚4000万金币）',
            '4.3: Construction to 99 (54 hours, 120M GP)': '4.3：建筑到99级（4.3：建筑到99级，54小时，1.2亿金币）',
            '4.4: Herblore to 99 (36 hours, 180M GP)': '4.4：草药学到99级（4.4：草药学到99级，36小时，1.8亿金币）',
            '🌾 Phase 5: Clean-Up Phase (2,200 → 2,277)': '🌾 第五阶段：清理阶段（第五阶段：清理阶段，2,200到2,277总等级）',
            '5.1: Farming to 99 (90 hours active, 15M GP)': '5.1：农耕到99级（5.1：农耕到99级，90小时活跃，1500万金币）',
            '5.2: Slayer to 99 (Last 0.5–2% of progress)': '5.2：杀戮到99级（5.2：杀戮到99级，最后0.5-2%进度）',
            '5.3: Smithing + Fletching to 99 (IF going for Max)': '5.3：锻造+制箭到99级（5.3：锻造+制箭到99级，如果追求Max）',
            '3. Skill Synergies — Training Multiple Skills to 99 Together': '3. 技能协同 — 同时将多项技能训练到99级（技能协同 — 同时将多项技能训练到99级）',
            '🔗 Tier 1: The Core Synergies (Use These)': '🔗 第一梯队：核心协同（第一梯队：核心协同，使用这些）',
            'Synergy 1: Slayer + Combat (The Classic Combo)': '协同1：杀戮+战斗（协同1：杀戮+战斗，经典组合）',
            'Synergy 2: Woodcutting + Firemaking (Resource Loop)': '协同2：伐木+生火（协同2：伐木+生火，资源循环）',
            'Synergy 3: Fishing + Cooking (Feed Your Own Training)': '协同3：钓鱼+烹饪（协同3：钓鱼+烹饪，自给自足训练）',
            'Synergy 4: Mining + Smithing (GF + BF + Armor Making)': '协同4：采矿+锻造（协同4：采矿+锻造，GF+BF+装备制作）',
            'Synergy 5: Agility + Construction (Rooftop GP → House Upgrades)': '协同5：敏捷+建筑（协同5：敏捷+建筑，屋顶金币→房屋升级）',
            '🔗 Tier 2: Secondary Synergies (Nice to Have)': '🔗 第二梯队：次要协同（第二梯队：次要协同，锦上添花）',
            'Synergy 6: Hunter + Construction (Maniacal Monkeys → Gilded Bones)': '协同6：猎人+建筑（协同6：猎人+建筑，疯狂猴子→镀金骨）',
            'Synergy 7: Slayer + Farming (Herb Drops + Herb Runs)': '协同7：杀戮+农耕（协同7：杀戮+农耕，草药掉落+草药种植）',
            'Synergy 8: Wintertodt + ALL (The King of Synergies)': '协同8：Wintertodt+所有（协同8：Wintertodt+所有，协同之王）',
            '📊 Synergy Effectiveness Ranking': '📊 协同效果排名（协同效果排名）',
            '4. Total GP Required & Money Strategy': '4. 所需总金币与赚钱策略（所需总金币与赚钱策略）',
            '💰 Total GP Cost Breakdown': '💰 总金币成本明细（总金币成本明细）',
            '📊 Sources of Free / Self-Funded GP': '📊 免费/自筹金币来源（免费/自筹金币来源）',
            'Free GP Source 1: Profitable Skills (200M+ GP)': '免费金币来源1：盈利技能（免费金币来源1：盈利技能，2亿+金币）',
            'Free GP Source 2: Quest Rewards (~50M GP total)': '免费金币来源2：任务奖励（免费金币来源2：任务奖励，总计约5000万金币）',
            'Free GP Source 3: Achievement Diary Rewards (~20M GP value)': '免费金币来源3：成就日记奖励（免费金币来源3：成就日记奖励，约2000万金币价值）',
            '🎯 Net GP Cost: The Bottom Line': '🎯 净金币成本：底线（净金币成本：底线）',
            '💰 Best Money-Making Methods for Funding Max': '💰 为Max筹集资金的最佳赚钱方法（为Max筹集资金的最佳赚钱方法）',
            'Method 1: Vorkath (Best GP/Hour, 3–5M)': '方法1：Vorkath（方法1：Vorkath，最佳金币/小时，300-500万）',
            'Method 2: Zulrah (2–4M GP/Hour)': '方法2：Zulrah（方法2：Zulrah，200-400万金币/小时）',
            'Method 3: Raids (Chambers of Xeric, 2–6M GP/Hour)': '方法3：团队副本（方法3：团队副本，Xeric密室，200-600万金币/小时）',
            'Method 4: Slayer Tasks (1–3M GP/Hour)': '方法4：杀戮任务（方法4：杀戮任务，100-300万金币/小时）',
            '📅 When to Start Bank-Rolling for Expensive 99s': '📅 何时开始为昂贵99级囤积资金（何时开始为昂贵99级囤积资金）',
            '5. Time Management & Realistic Scheduling': '5. 时间管理与现实规划（时间管理与现实规划）',
            '⏱️ EHP Explained: What is "Efficient Hours Played"?': '⏱️ EHP解释：什么是"高效游戏时间"？（EHP解释：什么是"高效游戏时间"？）',
            '📅 Realistic Time Tables by Playtime': '📅 按游戏时间的现实时间表（按游戏时间的现实时间表）',
            'Schedule A: 1 Hour Per Day (Casual Player)': '计划A：每天1小时（计划A：每天1小时，休闲玩家）',
            'Schedule B: 2–3 Hours Per Day (Moderate Player)': '计划B：每天2-3小时（计划B：每天2-3小时，中等玩家）',
            'Schedule C: 4–6 Hours Per Day (Dedicated Player)': '计划C：每天4-6小时（计划C：每天4-6小时，专注玩家）',
            'Schedule D: 8+ Hours Per Day (No-Life Player)': '计划D：每天8小时以上（计划D：每天8小时以上，全职玩家）',
            '📆 The "Pomodoro" Method for OSRS': '📆 OSRS的"番茄工作法"（OSRS的"番茄工作法"）',
            '🎯 Monthly Milestones for a Moderate Player': '🎯 中等玩家的月度里程碑（中等玩家的月度里程碑）',
            '6. Tools & Resources': '6. 工具与资源（工具与资源）',
            '📊 Progress Trackers': '📊 进度追踪器（进度追踪器）',
            'WiseOldMan (wiseoldman.net)': 'WiseOldMan（WiseOldMan（wiseoldman.net））',
            'CrystalMathLabs (crystalmathlabs.com)': 'CrystalMathLabs（CrystalMathLabs（crystalmathlabs.com））',
            'OSRS Hiscores (official)': 'OSRS官方积分榜（OSRS官方积分榜）',
            '🔧 Essential RuneLite Plugins': '🔧 必备RuneLite插件（必备RuneLite插件）',
            '📈 Time Tracking': '📈 时间追踪（时间追踪）',
            'Google Sheets XP Tracker': 'Google Sheets经验追踪器（Google Sheets经验追踪器）',
            'Toggl Track (Free Time-Tracking App)': 'Toggl Track（Toggl Track，免费时间追踪应用）',
            '📚 Information Resources': '📚 信息资源（信息资源）',
            '7. After Max — What\'s Next?': '7. Max之后 — 接下来做什么？（Max之后 — 接下来做什么？）',
            '🏆 Tier 1: "Easy" Post-Max Goals': '🏆 第一梯队：Max后"简单"目标（第一梯队：Max后"简单"目标）',
            'Quest Cape': '任务披风（任务披风）',
            'Achievement Cape': '成就披风（成就披风）',
            'Achievement Diary Cape': '成就日记披风（成就日记披风）',
            '🏅 Tier 2: Collection Goals': '🏅 第二梯队：收藏目标（第二梯队：收藏目标）',
            'Pet Hunting': '宠物狩猎（宠物狩猎）',
            'Collection Log Completion': '收藏日志完成（收藏日志完成）',
            '💀 Tier 3: PvM Mastery': '💀 第三梯队：PvM精通（第三梯队：PvM精通）',
            'High-Level Raids': '高级团队副本（高级团队副本）',
            'The Inferno (1 Completion = Max PvM Achievement)': '地狱挑战（地狱挑战，1次完成=最高PvM成就）',
            'Solo Bossing Mastery': '单刷Boss精通（单刷Boss精通）',
            '🌍 Tier 4: New Game+ / Fresh Accounts': '🌍 第四梯队：新游戏+/新账号（第四梯队：新游戏+/新账号）',
            '8. FAQ & Motivation': '8. 常见问题与动力（常见问题与动力）',
            '🎯 What to Do After Reading This Guide': '🎯 阅读本指南后做什么（阅读本指南后做什么）',
            'Continue Your Max Journey': '继续你的Max之旅（继续你的Max之旅）',
            '⚔️ Slayer: The Universal Combat Trainer': '⚔️ 杀戮：通用战斗训练师（杀戮：通用战斗训练师）',
            '💡 The "Synergy-First" Mentality': '💡 "协同优先"心态（"协同优先"心态）',
            '💡 The "5% Rule"': '💡 "5%规则"（"5%规则"）',
        }
    }
}


def add_cn_title_and_summary(html, cn_h1, cn_summary):
    """Add Chinese H1 before English H1 in guide-hero section, and add Chinese summary after subtitle."""
    cn_h1_tag = f'<h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_h1}</h1>'
    cn_h1_insert = f'{cn_h1_tag}\n            <h1'
    found_h1 = False
    
    # Try to find guide-hero or hero-section and add cn-title before the first H1 inside it
    hero_pattern = r'(<(?:section|div)\s+class="(?:guide-hero|hero-section)">.*?</(?:section|div)>)'
    hero_match = re.search(hero_pattern, html, re.DOTALL)
    if hero_match:
        hero_content = hero_match.group(1)
        # Check if H1 exists inside hero content
        inner_h1 = re.search(r'<h1(?! class="cn-title")', hero_content)
        if inner_h1:
            new_hero = re.sub(r'(<h1(?! class="cn-title"))', cn_h1_insert, hero_content, count=1)
            html = html.replace(hero_content, new_hero, 1)
            found_h1 = True
        else:
            found_h1 = False
    else:
        found_h1 = False
    
    # Fallback: add cn-title before the first H1 in the body
    if not found_h1:
        html = re.sub(r'(<h1(?! class="cn-title"))', cn_h1_insert, html, count=1)
    
    # Add Chinese summary after subtitle or intro paragraph
    subtitle_pattern = r'(<p class="subtitle">.*?</p>)'
    match = re.search(subtitle_pattern, html)
    if match:
        subtitle = match.group(1)
        summary_html = f'\n            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>'
        html = html.replace(subtitle, subtitle + summary_html, 1)
    else:
        # No subtitle - try intro section paragraph
        intro_match = re.search(r'(<section class="intro">\s*<p>.*?</p>)', html, re.DOTALL)
        if intro_match:
            intro_p = intro_match.group(1)
            summary_html = f'<p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>'
            html = html.replace(intro_p, intro_p + '\n                ' + summary_html, 1)
    
    return html


def add_h2_h3_translations(html, translations):
    """Add Chinese translations in parentheses after H2/H3 headings."""
    for eng_text, cn_text in translations.items():
        escaped = re.escape(eng_text)
        
        # Clean cn_text: if format "A（A）" where content in parens matches the prefix, strip duplicate
        m = re.match(r'^(.+?)（(.+)）$', cn_text.strip())
        if m and m.group(1).strip() == m.group(2).strip():
            clean_cn = m.group(1).strip()
        else:
            clean_cn = cn_text
        
        suffix = '（' + clean_cn + '）'
        
        # Replace H2
        h2_pattern = rf'(<h2[^>]*>\s*){escaped}(?!\s*（[^）]*）)(\s*</h2>)'
        html = re.sub(h2_pattern, lambda m: m.group(1) + eng_text + suffix + m.group(2), html)
        
        # Replace H3
        h3_pattern = rf'(<h3[^>]*>\s*){escaped}(?!\s*（[^）]*）)(\s*</h3>)'
        html = re.sub(h3_pattern, lambda m: m.group(1) + eng_text + suffix + m.group(2), html)
        
        # Replace H4
        h4_pattern = rf'(<h4[^>]*>\s*){escaped}(?!\s*（[^）]*）)(\s*</h4>)'
        html = re.sub(h4_pattern, lambda m: m.group(1) + eng_text + suffix + m.group(2), html)
    
    return html


def process_file(filename, data):
    filepath = os.path.join(FILES_DIR, filename)
    outdir = r"C:\Users\Lenovo\WorkBuddy\2026-06-28-07-19-44\temp_output"
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, filename)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Step 1: Add Chinese H1 and summary
    html = add_cn_title_and_summary(html, data["cn_h1"], data["cn_summary"])
    
    # Step 2: Add Chinese translations to H2/H3/H4
    html = add_h2_h3_translations(html, data["h2_h3"])
    
    # Write to temp output (safe location)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Processed: {filename} -> {outpath}")
    return True


def main():
    # Note: osrs-sailing-ship-crew-guide-2026.html doesn't exist,
    # using osrs-sailing-1-99-guide-2026.html instead
    
    file_list = [
        "osrs-sailing-1-99-guide-2026.html",
        "osrs-skills-overview-beginner-2026.html",
        "osrs-skills-progression-path-2026.html",
        "osrs-skill-training-after-sweep-up-2026.html",
        "osrs-skill-training-beginner-complete-guide-2026.html",
        "osrs-skill-training-beginner-fast-track-2026.html",
        "osrs-skill-training-endgame-guide-2026.html",
        "osrs-skill-training-max-account-2026.html",
    ]
    
    success = 0
    for filename in file_list:
        if filename in FILE_DATA:
            if process_file(filename, FILE_DATA[filename]):
                success += 1
        else:
            print(f"No data for: {filename}")
    
    print(f"\n{'='*50}")
    print(f"Completed: {success}/{len(file_list)} files processed")


if __name__ == "__main__":
    main()
