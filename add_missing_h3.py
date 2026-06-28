#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补全各文件中遗漏的H3中文翻译"""
import re

GUIDES_DIR = "C:/Users/Lenovo/osrs-guide-site/zh/guides"

# 需要补充的H3翻译
EXTRA_H3 = {
    # 所有文件共有
    "Table of Contents": "目录",
    "Every guide is free \u2014 this one stays free either way.": "每份攻略都是免费的——无论怎样都保持免费",
    "\u26a1 Quick-Jump Table of Contents": "\u26a1 快速跳转目录",
    
    # crafting FAQ
    "Q: How long does 1-99 Crafting take?": "问：1-99制作技能需要多长时间？",
    "Q: What's the best method for Ironman?": "问：铁人模式的最佳方法是什么？",
    "Q: Is Crafting expensive to train?": "问：训练制作技能贵吗？",
    "Q: When should I stop glassblowing and switch to something faster?": "问：什么时候应该停止玻璃吹制转用更快的方法？",
    "Q: What's the best Crafting item for profit?": "问：最佳赚钱的制作物品是什么？",
    "Q: Can I train Crafting on F2P?": "问：我可以在免费模式下训练制作技能吗？",
    "Q: Do I need Crafting for any important quests?": "问：制作技能对重要任务有必要吗？",
    
    # hitpoints FAQ
    "Q: How long does 1-99 Hitpoints take?": "问：1-99生命值需要多长时间？",
    "Q: Will I hit 99 HP before 99 Attack/Strength/Defence?": "问：我会在攻击/力量/防御到99之前达到99生命值吗？",
    "Q: What's the fastest way to train Hitpoints?": "问：最快训练生命值的方法是什么？",
    "Q: What's the most AFK way to train Hitpoints?": "问：最挂机的生命值训练方法是什么？",
    "Q: Is it worth getting 99 Hitpoints?": "问：达到99生命值值得吗？",
    "Q: How do Ironmen train Hitpoints?": "问：铁人模式如何训练生命值？",
    "Q: Can I train Hitpoints on F2P?": "问：我可以在免费模式下训练生命值吗？",
    "Q: Does the Hitpoints Cape effect stack with other regen items?": "问：生命值披风效果与其他恢复物品叠加吗？",
    
    # magic FAQ
    "Q: Which spellbook should I use?": "问：我应该使用哪个法术书？",
    "Q: Should I buy runes or craft them?": "问：我应该买符文还是自己制作？",
    "Q: Is enchanting jewelry really profitable?": "问：附魔珠宝真的能赚钱吗？",
    "Q: When should I switch from cheap methods to fast methods?": "问：什么时候应该从省钱方法切换到快速方法？",
    "Q: What gear helps with Magic training?": "问：什么装备有助于魔法训练？",
    "Q: Can I use a cannon to train Magic?": "问：我可以用大炮训练魔法吗？",
    "Q: What about NMZ (Nightmare Zone) for Magic?": "问：NMZ（梦魇空间）对魔法训练如何？",
    "Q: I'm an Ironman. What's different for me?": "问：我是铁人模式玩家。对我来说有什么不同？",
    # magic h3
    "What Makes a Method 'Cheap'?": "什么方法算'便宜'？",
    # guess the file uses single quote vs curly quote
    
    # mining FAQ
    "\u2753 Q: Should I bank ores or power-mine (drop them)?": "\u2753 问：我应该存矿还是快速采矿（丢弃）？",
    "\u2753 Q: Is Motherlode Mine better than 3-tick granite?": "\u2753 问：母矿脉比3刻花岗岩更好吗？",
    "\u2753 Q: What quests help with Mining? Which should I do first?": "\u2753 问：哪些任务有助于采矿？应该先做哪些？",
    "\u2753 Q: Can F2P (Free-to-Play) players train Mining effectively?": "\u2753 问：免费玩家能有效训练采矿吗？",
    "\u2753 Q: How long does it take to get 99 Mining at MLM?": "\u2753 问：在MLM达到99采矿需要多长时间？",
    "\u2753 Q: What's the best pickaxe for a beginner with a low budget?": "\u2753 问：初学者低预算的最佳镐子是什么？",
    "\u2753 Q: Should I use Swiftness potions or other boosts for Mining?": "\u2753 问：我应该使用急速药水或其他增益来采矿吗？",
    "\u2753 Q: I'm an Ironman. Does this guide still apply?": "\u2753 问：我是铁人模式。这个指南仍然适用吗？",
    "\u2753 Q: What's the best way to make money with Mining at low levels?": "\u2753 问：低等级采矿的最佳赚钱方式是什么？",
}

files_to_fix = [
    "combat-achievements-guide-2026.html",
    "max-cape-route-2026.html",
    "osrs-1-99-crafting-guide-2026.html",
    "osrs-1-99-hitpoints-guide-2026.html",
    "osrs-1-99-hitpoints-training-guide-2026.html",
    "osrs-1-99-hunter-guide-2026.html",
    "osrs-1-99-hunter-guide-afk-method.html",
    "osrs-1-99-magic-training-cheap-guide-2026.html",
    "osrs-1-99-mining-guide-beginner-2026.html",
]

for filename in files_to_fix:
    filepath = GUIDES_DIR + "/" + filename
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for eng, cn in EXTRA_H3.items():
        escaped = re.escape(eng)
        pattern = re.compile(r'(<h3[^>]*>)' + escaped + r'(</h3>)')
        def make_repl(en=eng, c=cn):
            return lambda m: m.group(1) + en + '\uff08' + c + '\uff09' + m.group(2)
        new_content = pattern.sub(make_repl(), content)
        if new_content != content:
            count += 1
            content = new_content
    
    # Also try with \u2019 (curly single quote) variants for files that might use them
    # Check for 'Quick-Jump' which failed in hunter
    # The hunter file has "⚡ Quick-Jump Table of Contents"
    
    outpath = "/tmp/" + filename
    import os as _os
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{filename}: 补充了{count}个H3翻译")

print("\n完成！")
