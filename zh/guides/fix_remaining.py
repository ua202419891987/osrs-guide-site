#!/usr/bin/env python3
"""Fix remaining placeholders that have embedded HTML or &amp; entities."""
import os, re

BASE = r"C:\Users\Lenovo\osrs-guide-site\zh\guides"

fixes = {
    # osrs-money-making-fishing-2026.html
    os.path.join(BASE, "osrs-money-making-fishing-2026.html"): {
        '7. Frequently Asked Questions（中文标题）': '7. Frequently Asked Questions（常见问题解答）',
    },
    # osrs-passive-money-making-offline.html
    os.path.join(BASE, "osrs-passive-money-making-offline.html"): {
        '7. Frequently Asked Questions（中文标题）': '7. Frequently Asked Questions（常见问题解答）',
    },
    # osrs-quest-unlocked-money-methods-2026.html
    os.path.join(BASE, "osrs-quest-unlocked-money-methods-2026.html"): {
        '⛏️ Zalcano (3M-2.5M GP/hr)（中文说明）': '⛏️ Zalcano (3M-2.5M GP/hr)（萨尔卡诺——300万-250万 GP/小时）',
    },
    # osrs-slayer-money-making-guide-2026.html
    os.path.join(BASE, "osrs-slayer-money-making-guide-2026.html"): {
        'Slayer Master Location &amp; Teleports（中文说明）': 'Slayer Master Location &amp; Teleports（Slayer大师位置与传送）',
    },
    # osrs-revenants-caves-guide-2026.html
    os.path.join(BASE, "osrs-revenants-caves-guide-2026.html"): {
        '① Revenant Hierarchy (Difficulty &amp; Value)（中文说明）': '① Revenant Hierarchy (Difficulty &amp; Value)（亡灵等级——难度与价值）',
        '① Skull Trick Avoidance — Critical!（中文说明）': '① Skull Trick Avoidance — Critical!（骷髅标记规避——至关重要！）',
        '⑧ 🎯 Safe Spots &amp; Wilderness Agility Shortcuts（中文标题）': '⑧ 🎯 Safe Spots &amp; Wilderness Agility Shortcuts（安全点与荒野敏捷捷径）',
        '① Best Safe Spots in the Revenants Caves（中文说明）': '① Best Safe Spots in the Revenants Caves（亡灵洞穴最佳安全点）',
        '① Wilderness Agility Shortcuts — Your #1 Escape Tool（中文说明）': '① Wilderness Agility Shortcuts — Your #1 Escape Tool（荒野敏捷捷径——你的头号逃生工具）',
        '① Advanced Escape Route: The "Agility Gauntlet"（中文说明）': '① Advanced Escape Route: The "Agility Gauntlet"（高级逃生路线：敏捷手套）',
        '① RuneLite Plugins for the Caves（中文说明）': '① RuneLite Plugins for the Caves（洞穴适用的RuneLite插件）',
        '⑨ ❓ FAQ — Revenants Caves (2026 Updated)（中文标题）': '⑨ ❓ FAQ — Revenants Caves (2026 Updated)（常见问题——亡灵洞穴2026更新版）',
        '🏆 Final Tips for Revenant Hunters（中文说明）': '🏆 Final Tips for Revenant Hunters（亡灵猎人的最终提示）',
        '💰 Want More Wilderness Money Makers?（中文说明）': '💰 Want More Wilderness Money Makers?（想要更多荒野赚钱方法？）',
        '⚔️ Need Help With Gear?（中文说明）': '⚔️ Need Help With Gear?（需要装备方面的帮助？）',
    },
    # osrs-money-making-tier-list-2026.html — h3 with <span> inside
    os.path.join(BASE, "osrs-money-making-tier-list-2026.html"): {
        '<h3>🥇 Theatre of Blood (Hard Mode) <span class="tier-badge tier-s">S</span>（中文说明）</h3>': '<h3>🥇 Theatre of Blood (Hard Mode) <span class="tier-badge tier-s">S</span>（鲜血剧院——困难模式）</h3>',
        '<h3>🥈 Tombs of Amascut (Expert 400+) <span class="tier-badge tier-s">S</span>（中文说明）</h3>': '<h3>🥈 Tombs of Amascut (Expert 400+) <span class="tier-badge tier-s">S</span>（阿玛斯库特之墓——专家400+）</h3>',
        '<h3>🥉 Chambers of Xeric (Challenge Mode) <span class="tier-badge tier-s">S</span>（中文说明）</h3>': '<h3>🥉 Chambers of Xeric (Challenge Mode) <span class="tier-badge tier-s">S</span>（塞里克密室——挑战模式）</h3>',
        '<h3>🔥 Corrupted Gauntlet <span class="tier-badge tier-a">A</span> ⬆️ NEWLY BUFFED（中文说明）</h3>': '<h3>🔥 Corrupted Gauntlet <span class="tier-badge tier-a">A</span> ⬆️ NEWLY BUFFED（腐蚀遗迹——新增强化）</h3>',
        '<h3>💀 Phantom Muspah <span class="tier-badge tier-a">A</span>（中文说明）</h3>': '<h3>💀 Phantom Muspah <span class="tier-badge tier-a">A</span>（幻影穆斯帕）</h3>',
        '<h3>🐉 Vorkath (Dragon Hunter Crossbow) <span class="tier-badge tier-a">A</span>（中文说明）</h3>': '<h3>🐉 Vorkath (Dragon Hunter Crossbow) <span class="tier-badge tier-a">A</span>（韦克思——龙猎弩）</h3>',
        '<h3>🐍 Zulrah <span class="tier-badge tier-a">A</span> ⬆️ BUFFED（中文说明）</h3>': '<h3>🐍 Zulrah <span class="tier-badge tier-a">A</span> ⬆️ BUFFED（祖拉——已增强）</h3>',
        '<h3>👹 Demonic Gorillas <span class="tier-badge tier-a">A</span>（中文说明）</h3>': '<h3>👹 Demonic Gorillas <span class="tier-badge tier-a">A</span>（恶魔大猩猩）</h3>',
        '<h3>🏰 Hallowed Sepulchre (Floor 5) <span class="tier-badge tier-b">B</span>（中文说明）</h3>': '<h3>🏰 Hallowed Sepulchre (Floor 5) <span class="tier-badge tier-b">B</span>（神圣墓穴——第5层）</h3>',
        '<h3>⚔️ Slayer (85+) <span class="tier-badge tier-b">B</span>（中文说明）</h3>': '<h3>⚔️ Slayer (85+) <span class="tier-badge tier-b">B</span>（杀戮——85级以上）</h3>',
        '<h3>⛏️ Zalcano <span class="tier-badge tier-b">B</span>（中文说明）</h3>': '<h3>⛏️ Zalcano <span class="tier-badge tier-b">B</span>（萨尔卡诺）</h3>',
        '<h3>🌿 Herb Runs (Passive) <span class="tier-badge tier-b">B</span>（中文说明）</h3>': '<h3>🌿 Herb Runs (Passive) <span class="tier-badge tier-b">B</span>（草药种植——被动）</h3>',
        '<h3>🌊 Tempoross <span class="tier-badge tier-b">B</span>（中文说明）</h3>': '<h3>🌊 Tempoross <span class="tier-badge tier-b">B</span>（坦波罗斯）</h3>',
        '<h3>💀 Barrows <span class="tier-badge tier-c">C</span>（中文说明）</h3>': '<h3>💀 Barrows <span class="tier-badge tier-c">C</span>（巴罗斯）</h3>',
        '<h3>🔥 Blast Furnace <span class="tier-badge tier-c">C</span>（中文说明）</h3>': '<h3>🔥 Blast Furnace <span class="tier-badge tier-c">C</span>（高炉炼钢）</h3>',
        '<h3>🐉 Green Dragons (Myths Guild) <span class="tier-badge tier-c">C</span>（中文说明）</h3>': '<h3>🐉 Green Dragons (Myths Guild) <span class="tier-badge tier-c">C</span>（绿龙——神话公会）</h3>',
        '<h3>🗡️ Gargoyles (75 Slayer) <span class="tier-badge tier-c">C</span>（中文说明）</h3>': '<h3>🗡️ Gargoyles (75 Slayer) <span class="tier-badge tier-c">C</span>（石像鬼——75级杀戮）</h3>',
        '<h3>🐮 Cowhide Tanning <span class="tier-badge tier-d">D</span>（中文说明）</h3>': '<h3>🐮 Cowhide Tanning <span class="tier-badge tier-d">D</span>（牛皮鞣制）</h3>',
        '<h3>🪙 High Alchemy (Profitable Items) <span class="tier-badge tier-d">D</span>（中文说明）</h3>': '<h3>🪙 High Alchemy (Profitable Items) <span class="tier-badge tier-d">D</span>（高等级炼金术——盈利物品）</h3>',
        '<h3>🎣 Fishing (Lobsters / Swordfish) <span class="tier-badge tier-d">D</span>（中文说明）</h3>': '<h3>🎣 Fishing (Lobsters / Swordfish) <span class="tier-badge tier-d">D</span>（钓鱼——龙虾/剑鱼）</h3>',
    },
}

total = 0
for fpath, replacements in fixes.items():
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
    if count > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK  {os.path.basename(fpath)} — {count} replacements")
        total += count
    else:
        print(f"  --  {os.path.basename(fpath)} — no matching patterns found")

print(f"\nRemaining fixes applied: {total}")
