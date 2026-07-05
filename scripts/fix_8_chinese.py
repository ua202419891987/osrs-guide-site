#!/usr/bin/env python
"""批量修复8篇英文站文章中的中文残留"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\Lenovo\osrs-guide-site\guides'
fixes = []

# 1. combat-achievements-guide-2026.html — Quick Summary 5处中文
fixes.append((
    os.path.join(BASE, 'combat-achievements-guide-2026.html'),
    [
        ('📌 <strong>Combat Achievements</strong> — 战斗成就系统，包含5个难度等级（Easy至Grandmaster）',
         '📌 <strong>Combat Achievements</strong> — 5 difficulty tiers from Easy to Grandmaster with unique rewards'),
        ('📌 <strong>Easy/Medium奖励</strong> — 免费 combat XP lamp 和哥布林彩蛋外观',
         '📌 <strong>Easy/Medium Rewards</strong> — free combat XP lamps and goblin cosmetic unlocks'),
        ('📌 <strong>前置要求</strong> — 必须有一定 combat 等级和大任务完成度',
         '📌 <strong>Prerequisites</strong> — requires minimum combat levels and significant quest completion'),
        ('📌 <strong>2026新增</strong> — 新增 Sailing 相关成就',
         '📌 <strong>2026 Update</strong> — new Sailing-related achievements added'),
        ('📌 <strong>推荐策略</strong> — 从 Easy 开始做，逐步解锁更好奖励',
         '📌 <strong>Strategy</strong> — start from Easy tier and work up to unlock better rewards gradually'),
    ]
))

# 2. osrs-complete-skill-training-guide-2026.html — "阿尔Khazard"
fixes.append((
    os.path.join(BASE, 'osrs-complete-skill-training-guide-2026.html'),
    [
        ('cows,阿尔Khazard Warriors', 'cows, Al Khazard Warriors'),
    ]
))

# 3. osrs-fractured-archive-prep-guide-2026.html — "珍贵·collection"
fixes.append((
    os.path.join(BASE, 'osrs-fractured-archive-prep-guide-2026.html'),
    [
        ('Guthix\'s most珍贵·collection of artifacts', 'Guthix\'s most precious collection of artifacts'),
    ]
))

# 4. osrs-how-to-unlock-fairy-rings.html — 中文警告框
fixes.append((
    os.path.join(BASE, 'osrs-how-to-unlock-fairy-rings.html'),
    [
        ('''    <!-- 直接答案：最快解锁5步流程 -->
    <div style="background:#EDE8F5;border:2px solid #7A64B8;border-radius:10px;padding:18px 22px;margin-bottom:24px;">
      <h3 style="margin:0 0 10px 0;color:#5B4A9C;font-size:17px">⚡ 最快解锁妖精戒指：5步流程（总计2-3小时）</h3>
      <ol style="margin:0;padding-left:22px;color:#2D2A33;font-size:14px;line-height:2.0">
        <li><strong>做 Lost City 任务</strong>（30分钟）→ 获得 Dramen Staff，可以用妖精戒指（需要装备Staff）</li>
        <li><strong>做 A Fairy Tale Part I</strong>（45分钟）→ 获得 Magic Secateurs，妖精戒指网络扩展</li>
        <li><strong>开始（不用完成！）A Fairy Tale Part II</strong>（2分钟）→ 从此可以<strong>不用装备Staff</strong>直接用妖精戒指 ✅</li>
        <li><strong>（可选）85 Construction 后在房子里建妖精戒指</strong> → 配合珠宝盒成为全游戏最快传送网络</li>
        <li><strong>记住以下核心代码</strong> → DKS（DKs）、AIQ（Fight Caves）、BJS（Fossil Island）、CIR（Zulrah附近）</li>
      </ol>
      <p style="margin:10px 0 0 0;color:#5B4A9C;font-size:13px;font-weight:600">🎯 关键技巧：Fairy Tale Part II <strong>不需要完成</strong>，只要开始就能解除Staff限制！</p>
    </div>''',
     '''    <!-- ⚡ Fast Track: Fairy Ring Unlock in 5 Steps -->
    <div style="background:#EDE8F5;border:2px solid #7A64B8;border-radius:10px;padding:18px 22px;margin-bottom:24px;">
      <h3 style="margin:0 0 10px 0;color:#5B4A9C;font-size:17px">⚡ Fastest Fairy Ring Unlock: 5 Steps (2-3 Hours Total)</h3>
      <ol style="margin:0;padding-left:22px;color:#2D2A33;font-size:14px;line-height:2.0">
        <li><strong>Complete Lost City</strong> (30 min) → Get Dramen Staff, you can now use fairy rings (must equip staff)</li>
        <li><strong>Complete A Fairy Tale Part I</strong> (45 min) → Get Magic Secateurs, fairy ring network expands</li>
        <li><strong>Start (do NOT finish!) A Fairy Tale Part II</strong> (2 min) → From here on you can use fairy rings <strong>without equipping the staff</strong> ✅</li>
        <li><strong>(Optional) Build fairy rings in your POH at 85 Construction</strong> → combined with jewelry box, this is the fastest teleport network in the game</li>
        <li><strong>Memorize these key codes</strong> → DKS (Dagannoth Kings), AIQ (Fight Caves), BJS (Fossil Island), CIR (near Zulrah)</li>
      </ol>
      <p style="margin:10px 0 0 0;color:#5B4A9C;font-size:13px;font-weight:600">🎯 Key tip: Fairy Tale Part II <strong>does NOT need to be completed</strong> — just starting it removes the staff requirement!</p>
    </div>'''),
    ]
))

# 5. osrs-ironman-beginner-guide-2026.html — Quick Summary 5处中文
fixes.append((
    os.path.join(BASE, 'osrs-ironman-beginner-guide-2026.html'),
    [
        ('<li>📌 <strong>Ironman = 完全自给自足</strong> — 不能交易、不能 GE，所有物品靠自己获取</li>',
         '<li>📌 <strong>Ironman = completely self-sufficient</strong> — no trading, no GE, every item earned through your own effort</li>'),
        ('<li>📌 <strong>新手不建议铁人开局</strong> — 先玩普通号熟悉游戏，再挑战铁人模式</li>',
         '<li>📌 <strong>Not recommended for brand new players</strong> — play a normal account first to learn the game, then try ironman</li>'),
        ('<li>📌 <strong>铁人赚钱三大途径</strong> — high alchemy、slayer drops、herb runs</li>',
         '<li>📌 <strong>Ironman money making trifecta</strong> — high alchemy, slayer drops, herb runs</li>'),
        ('<li>📌 <strong>任务比普通号更重要</strong> — 优先做 waterfall quest、fairytale、lost city</li>',
         '<li>📌 <strong>Quests matter more for ironmen</strong> — prioritize Waterfall Quest, Fairy Tale, Lost City</li>'),
        ('<li>📌 <strong>Wintertodt 是最佳开局</strong> — 火做+掉落让你跳过早期资源瓶颈</li>',
         '<li>📌 <strong>Wintertodt is the best start</strong> — firemaking XP + supply drops skip early resource bottlenecks</li>'),
    ]
))

# 6. osrs-mobile-guide-2026.html — Quick Summary 5处中文
fixes.append((
    os.path.join(BASE, 'osrs-mobile-guide-2026.html'),
    [
        ('<li>📌 <strong>OSRS Mobile</strong> — 免费 App，iOS/Android 都支持</li>',
         '<li>📌 <strong>OSRS Mobile</strong> — free app available on both iOS and Android</li>'),
        ('<li>📌 <strong>触屏操作</strong> — Tap-hold 代替右键，是核心操作区别</li>',
         '<li>📌 <strong>Touch controls</strong> — tap-hold replaces right-click, this is the core difference in gameplay</li>'),
        ('<li>📌 <strong>最佳 AFK 活动</strong> — Fishing、Woodcutting、Cooking 最适合手机</li>',
         '<li>📌 <strong>Best AFK activities</strong> — Fishing, Woodcutting, and Cooking work best on mobile</li>'),
        ('<li>📌 <strong>RuneLite 插件</strong> — Android 可侧载，iOS 不支持</li>',
         '<li>📌 <strong>RuneLite plugins</strong> — Android supports sideloading, iOS does not</li>'),
        ('<li>📌 <strong>流量消耗</strong> — 每小时仅 30–50MB，适合通勤</li>',
         '<li>📌 <strong>Data usage</strong> — only 30-50MB per hour, perfect for commuting</li>'),
    ]
))

# 7. osrs-questing-beginner-guide-2026.html — 副标题中文
fixes.append((
    os.path.join(BASE, 'osrs-questing-beginner-guide-2026.html'),
    [
        ('Quests是OSRS里跳过练级痛苦的最快方式。做对任务可以让你从Combat 1直接跳到30+，省下几十小时的无聊练级时间。',
         'Quests are the fastest way to skip the early grind in OSRS. The right quests can jump you from Combat level 1 to 30+, saving dozens of hours of tedious training time.'),
    ]
))

# 8. osrs-returning-player-guide-2026.html — Quick Summary 5处中文
fixes.append((
    os.path.join(BASE, 'osrs-returning-player-guide-2026.html'),
    [
        ('<li>📌 <strong>180+ 新内容更新</strong> — 如果你2年+没玩，现在回归需注意海量新技能、新Boss和经济变动</li>',
         '<li>📌 <strong>180+ content updates</strong> — if you haven\'t played in 2+ years, expect new skills, new bosses, and major economy shifts</li>'),
        ('<li>📌 <strong>Sailing 第24个技能</strong> — 2026年全面上线，从 Port Sarim 的 Pandemonium 任务开始</li>',
         '<li>📌 <strong>Sailing is the 24th skill</strong> — fully launched in 2026, starting with the Pandemonium quest at Port Sarim</li>'),
        ('<li>📌 <strong>经济系统已变</strong> — 新Boss导致部分掉落涨价，附魔骨装备价格高企</li>',
         '<li>📌 <strong>The economy has changed</strong> — new bosses have shifted drop prices, enchanted bone gear remains expensive</li>'),
        ('<li>📌 <strong>推荐回归顺序</strong> — Quests → Sailing → Slayer → Boss，逐步适应新版本</li>',
         '<li>📌 <strong>Recommended return path</strong> — Quests → Sailing → Slayer → Boss, ease into the new meta</li>'),
        ('<li>📌 <strong>账号安全优先</strong> — 如果号被盗了，先看 account-security-guide</li>',
         '<li>📌 <strong>Security comes first</strong> — if your account was compromised, check the account security guide immediately</li>'),
    ]
))

# Apply all fixes
ok, fail = 0, 0
for path, replacements in fixes:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)
            changes += 1
            print(f'✅ [{os.path.basename(path)}] replaced: {old[:40]}...')
        else:
            # Try HTML-escaped or other variants
            old_escaped = old.replace("'", "&apos;")
            if old_escaped in content:
                content = content.replace(old_escaped, new, 1)
                changes += 1
                print(f'✅ [{os.path.basename(path)}] replaced (escaped): {old[:40]}...')
            else:
                print(f'⚠️ [{os.path.basename(path)}] NOT FOUND: {old[:40]}...')
                fail += 1
    
    if changes > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        ok += 1
        print(f'  → {os.path.basename(path)} saved ({changes} changes)\n')
    else:
        print(f'  → {os.path.basename(path)} NO CHANGES\n')

print(f'\n=== Done: {ok}/8 files fixed, {fail} replacements failed ===')
