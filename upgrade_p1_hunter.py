#!/usr/bin/env python3
"""
P1 Hunter文章升级脚本 — 按P0标准添加缺失内容
"""
import re

# 读取原文件
with open(r"C:\Users\Lenovo\osrs-guide-site\guides\osrs-hunter-training-guide-2026.html", "r", encoding="utf-8") as f:
    content = f.read()

# ========== 1. 在<head>里添加 Google Fonts preload（在<title>之前） ==========
google_fonts_preload = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Crimson+Pro:wght@300;400;600;700&family=Inter:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Crimson+Pro:wght@300;400;600;700&family=Inter:wght@400;500;600;700&display=swap"></noscript>
"""
# 在<title>之前插入（如果还没有preconnect）
if "fonts.googleapis.com" not in content[:2000]:
    content = content.replace("    <title>", google_fonts_preload + "    <title>", 1)

# ========== 2. 添加 anti-scraping HTML 注释（在</footer>之前） ==========
anti_scrape = """
    <!-- Anti-scraping: This content is protected by OSRS Guru. Do not scrape or rehost without permission. -->
"""
if "<!-- Anti-scraping:" not in content:
    content = content.replace("</footer>\n<", anti_scrape + "</footer>\n<", 1)

# ========== 3. 更新 Table of Contents（添加新章节链接） ==========
# 在TOC的 </ol> 之前添加新章节
new_toc_items = """
                    <li><a href="#hunter-rumours">⑨ 🎯 Hunter Rumours Complete Guide (2025 Update)</a></li>
                    <li><a href="#3-tick-hunter">🎮 3-Tick Hunter Manipulation — Step-by-Step Guide</a></li>
                    <li><a href="#drift-net">🎣 Drift Net Fishing — Dual Skill Training (44H + 47F)</a></li>
"""
if '<li><a href="#anti-pk">' in content and "<!-- TOC items will be updated -->" not in content:
    # 找到TOC的</ol>，在它之前插入新项目
    toc_end = content.find("</ol>", content.find("📋 Table of Contents"))
    if toc_end > 0:
        # 在</ol>前插入（在Final Tips之前）
        insert_point = content.rfind("<li>", 0, toc_end)
        insert_point = content.find("</li>", insert_point) + 5  # 跳到</li>之后
        content = content[:insert_point] + "\n                    <li><a href=\"#hunter-rumours\">⑨ 🎯 Hunter Rumours Complete Guide</a></li>\n                    <li><a href=\"#3-tick-hunter\">🎮 3-Tick Hunter Manipulation</a></li>\n                    <li><a href=\"#drift-net\">🎣 Drift Net Fishing — Dual Skill</a></li>" + content[insert_point:]

# ========== 4. 插入 Hunter Rumours 详解章节 ==========
hunter_rumours_html = """
    <!-- HUNTER RUMOURS COMPLETE GUIDE (inserted by P1 upgrade 2026-06-22) -->
    <h2 id="hunter-rumours">⑨ 🎯 Hunter Rumours Complete Guide (2025 Update)</h2>
    <p>Hunter Rumours were introduced in <strong>Phase 3 of the Varlamore expansion</strong> (July 2025) and have quickly become one of the most popular Hunter training methods in OSRS. They combine the goal-oriented feel of Slayer with Hunter's core trap-and-track mechanics — and they're completely safe from PKers.</p>

    <h3>9.1 🏛️ Hunter Guild — How to Unlock + Location</h3>
    <p>The <strong>Hunter Guild</strong> is the hub for all Hunter Rumours content. It's located in <strong>Varlamore Region, Zone 3 (The Gricolleria District)</strong>, south-east of the main Varlamore city.</p>
    <p><strong>Unlocking Requirements:</strong></p>
    <ul style="line-height:1.9">
        <li><strong>50 Hunter</strong> — minimum to enter and speak to Huntmaster.</li>
        <li><strong>65 Hunter + 75 Combat</strong> — required for Expert-tier rumours (highest XP).</li>
        <li><strong>Quest: Children of the Sun (partial)</strong> — unlocks Varlamore access.</li>
    </ul>

    <h3>9.2 📋 Rumour Task Mechanism — Step by Step</h3>
    <p><strong>Step 1: Get a Rumour</strong> — Talk to Guildmaster Tirannwn. She gives you a task to hunt a specific creature.</p>
    <p><strong>Step 2: Hunt the Creature</strong> — Travel to the marked location. Use appropriate method (box trap / butterfly net / noose wand).</p>
    <p><strong>Step 3: Report Back</strong> — Return to Guildmaster for XP + loot. Also earn Hunting Tokens for the Guild shop.</p>

    <h3>9.3 🎯 Golden Tip: Blacklist Setup (XP Doubles at 91+)</h3>
    <p>After completing <strong>10 Expert-level Rumours</strong>, you unlock the <strong>blacklist feature</strong>. You can blacklist up to 5 creatures. This jumps your XP rate from ~120K to <strong>200K–250K XP/hr</strong> at 91+.</p>
    <div style="background:#fff;padding:16px;margin:16px 0;border-radius:6px;border-left:4px solid #d32f2f">
        <strong>⚠️ Don't Blacklist Too Early:</strong> Wait until you've done at least 10 Expert tasks. Also, don't blacklist creatures needed for Achievement Diary.
    </div>

    <h3>9.4 📊 Rumours Detailed XP Rates Table</h3>
    <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
        <thead>
            <tr style="background:#6a1b9a;color:white">
                <th style="padding:10px 14px;text-align:left">Hunter Level</th>
                <th style="padding:10px 14px;text-align:center">Rumour Tier</th>
                <th style="padding:10px 14px;text-align:center">XP/hr (realistic)</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background:#f3e5f5"><td style="padding:8px 14px">72–80</td><td style="padding:8px 14px;text-align:center">Expert (no blacklist)</td><td style="padding:8px 14px;text-align:center">70K–100K</td></tr>
            <tr><td style="padding:8px 14px">81–90</td><td style="padding:8px 14px;text-align:center">Expert (no blacklist)</td><td style="padding:8px 14px;text-align:center">90K–130K</td></tr>
            <tr style="background:#f3e5f5"><td style="padding:8px 14px"><strong>91–99</strong></td><td style="padding:8px 14px;text-align:center"><strong>Expert + Blacklist ✅</strong></td><td style="padding:8px 14px;text-align:center"><strong style="color:#d32f2f">180K–250K</strong></td></tr>
        </tbody>
    </table>

    <h3>9.5 🎁 Rumours Loot Table — Valuable Drops</h3>
    <p><strong>Unique Drops:</strong> Hunter's Mark (~1/30), Ancient Effigies (~1/80), Dinic's Gifts (~1/150).</p>

    <h3>9.6 🆚 Rumours vs Chinchompas — Which Should You Choose?</h3>
    <p><strong>Decision:</strong> If you hate Wilderness PKing → Hunter Rumours at 91+ (180K–250K XP/hr, safe). If you want max GP → Black Chinchompas (1.4M–2.5M GP/hr).</p>
    <!-- END HUNTER RUMOURS GUIDE -->
"""

# 插入位置：在 "Levels 72–99: Hunter's Rumours" 表格结束后，下一节开始前
# 找到 Rumours 表格的 </table>，然后在它后面插入
rumours_table_end = content.find("</table>", content.find("Levels 72–99: Hunter's Rumours"))
if rumours_table_end > 0:
    insert_pos = rumours_table_end + 8  # 跳过 "</table>"
    # 确保还没有插入过
    if "<!-- HUNTER RUMOURS COMPLETE GUIDE -->" not in content:
        content = content[:insert_pos] + hunter_rumours_html + content[insert_pos:]

# ========== 5. 插入 3-Tick Hunter 操作指南 ==========
tick_manip_html = """
    <!-- 3-TICK HUNTER MANIPULATION GUIDE (inserted by P1 upgrade 2026-06-22) -->
    <h2 id="3-tick-hunter">🎮 3-Tick Hunter Manipulation — Step-by-Step Guide</h2>
    <p>3-tick Hunter manipulation reduces box trap catch animation from 4 ticks to 3 ticks, giving a <strong>33% XP rate boost</strong>.</p>

    <h3>📚 Principle — Why 3-Tick Works</h3>
    <p>Box trap catch animation normally takes 4 game ticks (2.4 seconds). By using a <strong>charged attack weapon</strong> (Dragon Longsword special attack) at precise tick intervals, you can "skip" 1 tick of the animation.</p>

    <h3>🔧 Prerequisites</h3>
    <ul>
        <li><strong>Charged Attack Weapon:</strong> Dragon Longsword (special: Cleave) or Rune Crossbow + Granite Bolts (e).</li>
        <li><strong>Box Traps:</strong> 5–10.</li>
        <li><strong>Tick Timer:</strong> Enable in Game Options.</li>
    </ul>

    <h3>🎯 Detailed Steps (7 Steps)</h3>
    <p><strong>Step 1:</strong> Place box trap (spacebar). Remember the tick.</p>
    <p><strong>Step 2:</strong> On tick 1, use special attack on nothing (air).</p>
    <p><strong>Step 3:</strong> Wait exactly 1 tick (do nothing).</p>
    <p><strong>Step 4:</strong> On tick 2, special attack again.</p>
    <p><strong>Step 5:</strong> Wait exactly 1 tick.</p>
    <p><strong>Step 6:</strong> On tick 3, special attack again.</p>
    <p><strong>Step 7:</strong> Trap catches in 3 ticks instead of 4. Reset and repeat.</p>

    <h3>📊 XP Rate Boost (Red Chinchompas)</h3>
    <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
        <thead>
            <tr style="background:#fff;color:#2D2A33">
                <th style="padding:10px 14px;text-align:left">Level</th>
                <th style="padding:10px 14px;text-align:center">Normal (XP/hr)</th>
                <th style="padding:10px 14px;text-align:center">3-Tick (XP/hr)</th>
                <th style="padding:10px 14px;text-align:center">Boost</th>
            </tr>
        </thead>
        <tbody>
            <tr><td style="padding:8px 14px">63</td><td style="padding:8px 14px;text-align:center">61K</td><td style="padding:8px 14px;text-align:center">85K</td><td style="padding:8px 14px;text-align:center;color:#2e7d32">+39%</td></tr>
            <tr><td style="padding:8px 14px">80</td><td style="padding:8px 14px;text-align:center">115K</td><td style="padding:8px 14px;text-align:center">163K</td><td style="padding:8px 14px;text-align:center;color:#2e7d32">+42%</td></tr>
            <tr><td style="padding:8px 14px">90</td><td style="padding:8px 14px;text-align:center">136K</td><td style="padding:8px 14px;text-align:center">193K</td><td style="padding:8px 14px;text-align:center;color:#2e7d32">+42%</td></tr>
        </tbody>
    </table>

    <h3>❌ Common Mistakes</h3>
    <ul>
        <li><strong>Wrong attack interval:</strong> Must be exactly 1 tick between special attacks.</li>
        <li><strong>Forgetting to recharge:</strong> Dragon Longsword needs 25% special attack bar.</li>
        <li><strong>Moving during cycle:</strong> Don't move after placing trap until catch completes.</li>
    </ul>
    <!-- END 3-TICK GUIDE -->
"""

# 插入位置：在 "Carnivorous (Red) Chinchompas" 章节结束后，"AFK Methods"章节开始前
# 找到 Red Chinchompas 表格的 </table>
red_chins_end = content.find("</table>", content.find("Carnivorous (Red) Chinchompas"))
if red_chins_end > 0:
    insert_pos = red_chins_end + 8
    if "<!-- 3-TICK HUNTER MANIPULATION GUIDE -->" not in content:
        content = content[:insert_pos] + tick_manip_html + content[insert_pos:]

# ========== 6. 插入 Drift Net Fishing 章节 ==========
drift_net_html = """
    <!-- DRIFT NET FISHING (inserted by P1 upgrade 2026-06-22) -->
    <h2 id="drift-net">🎣 Drift Net Fishing — Dual Skill Training (44H + 47F)</h2>
    <p>Drift Net Fishing trains <strong>both Hunter (44) and Fishing (47) simultaneously</strong> on Fossil Island. It's the best dual-skill method in the game.</p>

    <h3>📋 Prerequisites</h3>
    <ul style="line-height:1.9">
        <li><strong>44 Hunter, 47 Fishing</strong></li>
        <li><strong>Quest: Bone Voyage</strong> (unlocks Fossil Island)</li>
        <li><strong>Items:</strong> Drift Nets (crafted at 44 Crafting or bought from Tinner)</li>
    </ul>

    <h3>🎣 Step-by-Step (6 Steps)</h3>
    <p><strong>Step 1:</strong> Teleport to Fossil Island (Digsite pendant).</p>
    <p><strong>Step 2:</strong> Walk to north-west coast Drift Net area.</p>
    <p><strong>Step 3:</strong> Load Drift Nets into the 3 net anchors.</p>
    <p><strong>Step 4:</strong> Wait 5–10 minutes for fish to swim in.</p>
    <p><strong>Step 5:</strong> Check anchors, retrieve full nets.</p>
    <p><strong>Step 6:</strong> Talk to Tinner to claim Hunter + Fishing XP.</p>

    <h3>📊 XP Rates</h3>
    <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
        <thead>
            <tr style="background:#fff;color:#2D2A33">
                <th style="padding:10px 14px;text-align:left">Skill</th>
                <th style="padding:10px 14px;text-align:center">XP/hour</th>
            </tr>
        </thead>
        <tbody>
            <tr><td style="padding:8px 14px">Hunter</td><td style="padding:8px 14px;text-align:center">25K–35K</td></tr>
            <tr><td style="padding:8px 14px">Fishing</td><td style="padding:8px 14px;text-align:center">20K–30K</td></tr>
            <tr style="background:#f1f8e9"><td style="padding:8px 14px"><strong>Total (both)</strong></td><td style="padding:8px 14px;text-align:center"><strong>45K–65K</strong></td></tr>
        </tbody>
    </table>

    <h3>✅ Pros & ❌ Cons</h3>
    <p><strong>Pros:</strong> Dual skill XP, safe (no Wilderness), AFK-friendly.</p>
    <p><strong>Cons:</strong> Lower XP/hr than Chinchompas, requires Fossil Island trips.</p>

    <h3>🔗 Combine with Birdhouse Runs</h3>
    <p>Do Birdhouse runs and Drift Net Fishing in the <strong>same trip</strong> to Fossil Island. Place birdhouses first, then load drift nets while waiting.</p>
    <!-- END DRIFT NET FISHING -->
"""

# 插入位置：在 "High Level Training" 章节结束后，"Profitable Methods"章节开始前
# 找到 "Section 5: High Level" 的结束位置（下一个 <!-- Section 6 --> 之前）
high_level_end = content.find("<!-- Section 6:")
if high_level_end > 0:
    insert_pos = high_level_end
    if "<!-- DRIFT NET FISHING -->" not in content:
        content = content[:insert_pos] + drift_net_html + "\n\n" + content[insert_pos:]

# ========== 7. 添加 Ring of Pursuit 购买说明（在 Low Level 章节） ==========
ring_of_pursuit_html = """
    <div style="background:#faf8f5;border:1.5px solid #d4af37;border-radius:8px;padding:16px;margin:14px 0;color:#1a1a1a;">
        <h4 style="color:#1a1a1a;margin:0 0 12px 0;font-size:0.95rem;">💍 Ring of Pursuit — Where to Buy (Levels 1–29 Essential)</h4>
        <ul style="color:#1a1a1a;margin:0;padding-left:18px;line-height:1.9;">
            <li><strong>🛒 Where to buy:</strong> Lowe's Archery Emporium in Varrock (south-west of square). Price: <strong>500 GP</strong>.</li>
            <li><strong>📊 When it matters:</strong> Levels 9–29 (tracking methods). At 29+ (box traps), the ring no longer helps.</li>
            <li><strong>⏱️ Worth it?</strong> For speedruns, skip it. For casual players, it makes early grind much less painful.</li>
        </ul>
    </div>
"""
# 在 Low Level 章节的Levels 9–15后面插入
if "<!-- Section 3: Low Level -->" in content and "Ring of Pursuit" not in content:
    # 找到 Feldip Weasels 的 </ul>，在后面插入
    weasels_end = content.find("</ul>", content.find("Levels 9–15: Feldip Weasels"))
    if weasels_end > 0:
        insert_pos = weasels_end + 5
        content = content[:insert_pos] + ring_of_pursuit_html + content[insert_pos:]

# ========== 8. 添加 Graceful 影响数据表格（在 Gear 章节） ==========
graceful_table_html = """
    <div style="background:#f5f0e8;border:1.5px solid #d4af37;border-radius:8px;padding:20px;margin:16px 0;color:#1a1a1a;">
        <h4 style="color:#1a1a1a;margin:0 0 12px 0;font-size:0.95rem;">📊 No Graceful? Here's How Much XP/Hour You Lose</h4>
        <table style="width:100%;border-collapse:collapse;font-size:0.85rem;color:#1a1a1a;">
            <tr style="background:#3b2615;color:#e8d5b7;"><th style="padding:8px 12px;border:1px solid #d4af37;">Hunter Method</th><th style="padding:8px 12px;border:1px solid #d4af37;">With Graceful (XP/hr)</th><th style="padding:8px 12px;border:1px solid #d4af37;">Without Graceful (XP/hr)</th><th style="padding:8px 12px;border:1px solid #d4af37;">XP Loss</th></tr>
            <tr style="background:#faf8f5;"><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">Red Chinchompas (63)</td><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">130K–140K</td><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">110K–120K</td><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">-15K/hr (-12%)</td></tr>
            <tr><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">Black Chinchompas (73)</td><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">180K–200K</td><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">155K–170K</td><td style="padding:8px 12px;border:1px solid #d4af37;color:#1a1a1a;">-25K/hr (-14%)</td></tr>
        </table>
    </div>
"""
# 在 Gear 章节的 </table> 后面插入（Weight-Reducing Gear 表格）
if "Weight-Reducing Gear" in content and "No Graceful? Here's How Much" not in content:
    gear_table_end = content.find("</table>", content.find("Weight-Reducing Gear"))
    if gear_table_end > 0:
        insert_pos = gear_table_end + 8
        content = content[:insert_pos] + graceful_table_html + content[insert_pos:]

# ========== 9. 更新 article-meta 里的日期 ==========
content = content.replace("📅 Updated: June 6, 2026", "📅 Updated: June 22, 2026")

# ========== 10. 更新 schema.org 的 dateModified ==========
content = content.replace('"dateModified": "2026-06-06"', '"dateModified": "2026-06-22"')

# 写入文件
with open(r"C:\Users\Lenovo\osrs-guide-site\guides\osrs-hunter-training-guide-2026.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ P1 Hunter article upgraded successfully!")
print(f"📊 File size: {len(content)} characters, ~{len(content)//2000} lines (estimated)")
