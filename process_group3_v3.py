#!/usr/bin/env python3
"""
Group 3 v3: Final version - fixes all known issues.
"""

import os
import re

BASE_DIR = "C:/Users/Lenovo/osrs-guide-site"

ARTICLES = [
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
    "osrs-vorkath-money-making-guide-2026.html",
]

CN_INFO = {
    "osrs-money-making-beginner-2026.html": {
        "title": "OSRS 新手赚钱指南 — 从零开始赚金币（2026版）",
        "summary": "2026年最新新手赚钱攻略大全。从零开始，涵盖 F2P 和 P2P 两个阶段共 20 多种赚钱方法，按 GP/小时排序，附详细操作步骤和装备建议。",
        "preview": [
            "📌 涵盖 <strong>20 多种赚钱方法按 GP/小时排序</strong> — 从 15K（牛皮鞣制）到 200 万+/小时（韦克思）",
            "📌 <strong>最佳 F2P 方法：</strong>萨莫拉克酒（Wine of Zamorak）每小时 10 万–180 万 GP — 仅需 33 级魔法",
            "📌 <strong>首个绑定券路线图：</strong>F2P 需要 55–75 小时，或者直接购买会员（$7.99），然后赚钱速度快 10 倍",
            "📌 <strong>最佳早期 P2P：</strong>高炉炼钢（Blast Furnace）每小时 70 万–180 万 GP，仅需 30 级锻造",
            "📌 <strong>被动收入秘诀：</strong>草药种植 + 鸟屋 = 每天 100 万+ GP，只需 30 分钟活跃操作",
        ]
    },
    "osrs-money-making-fishing-2026.html": {
        "title": "OSRS 钓鱼赚钱指南 — 钓鱼也能发家致富（2026版）",
        "summary": "2026年钓鱼赚钱完整攻略。从新手到高手，涵盖所有钓鱼赚钱方法：虾、鳟鱼、金枪鱼、龙虾、暗影鱼、僧侣鱼、水族鱼、天使鱼等，附 GP/小时收益对比。",
        "preview": [
            "📌 涵盖 <strong>10+ 种钓鱼赚钱方法</strong> — 从新手到 99 级全程覆盖",
            "📌 <strong>最佳新手方法：</strong>钓龙虾（Lobster）每小时 5 万–10 万 GP，仅需 40 级钓鱼",
            "📌 <strong>最佳挂机方法：</strong>僧侣鱼（Monkfish）每小时 8 万–15 万 GP，62 级钓鱼 + 天鹅之歌任务",
            "📌 <strong>最高收益：</strong>暗影鱼（Anglerfish）每小时 15 万–25 万 GP，82 级钓鱼",
            "📌 <strong>被动收入：</strong>鱼饵箱（Fish Barrel）+ 钓鱼沙坑，边看电影边赚钱",
        ]
    },
    "osrs-money-making-no-skills-guide-2026.html": {
        "title": "OSRS 零技能赚钱指南 — 无需任何等级（2026版）",
        "summary": "2026年零技能需求赚钱攻略。无需任何技能等级，适合新注册账号。涵盖收集、拾荒、倒卖等 15 种零门槛方法，快速积累第一桶金。",
        "preview": [
            "📌 涵盖 <strong>15 种零技能需求赚钱方法</strong> — 创建账号即可开始",
            "📌 <strong>最佳起步：</strong>安全堡垒（Stronghold of Security）15 分钟赚 1 万 GP",
            "📌 <strong>最高收益零门槛：</strong>拾取玩家丢弃物品 + 倒卖 GE，每小时 3 万–8 万 GP",
            "📌 <strong>最快方法：</strong>收集牛皮 + 鞣制出售，每小时 1.5 万–2.5 万 GP",
            "📌 <strong>进阶路线：</strong>用第一笔钱购买装备，转向更高效的战斗赚钱",
        ]
    },
    "osrs-money-making-summer-sweep-up-2026.html": {
        "title": "OSRS 夏日扫荡赚钱指南 — 限时活动赚金攻略（2026版）",
        "summary": "2026年夏日活动赚钱攻略。限时活动期间的高收益赚钱方法汇总，包含各类季节性活动、特殊掉落品和限时商机分析。",
        "preview": [
            "📌 涵盖 <strong>所有 2026 夏日限时活动赚钱方法</strong> — 活动持续期间收益翻倍",
            "📌 <strong>最佳活动方法：</strong>海滩派对（Beach Party）收集贝壳兑换稀有物品，每小时 50 万–100 万 GP",
            "📌 <strong>快速倒卖：</strong>趁活动低价收购限量物品，活动结束后高价卖出",
            "📌 <strong>活动专属掉落：</strong>限时怪物掉落的活动专属装备和材料，价格往往翻倍",
            "📌 <strong>时间管理：</strong>合理安排活动任务和日常赚钱，收益最大化",
        ]
    },
    "osrs-money-making-tier-list-2026.html": {
        "title": "OSRS 赚钱方法梯级排名 — 各阶段最佳选择（2026版）",
        "summary": "2026年赚钱方法梯级排名。将所有赚钱方式按收益、稳定性、入门门槛分为 S/A/B/C/D 五个等级，帮助玩家选择最适合自己的方法。",
        "preview": [
            "📌 <strong>S 级：</strong>每小时 200 万+ GP — 韦克思、九头蛇、遗迹洞穴",
            "📌 <strong>A 级：</strong>每小时 80 万–200 万 GP — 高炉炼钢、弹幕杀怪、符文龙",
            "📌 <strong>B 级：</strong>每小时 30 万–80 万 GP — 草药种植、倒卖 GE、高级 Slayer",
            "📌 <strong>C 级：</strong>每小时 10 万–30 万 GP — 钓鱼、砍树、低级 Slayer",
            "📌 <strong>D 级：</strong>每小时 10 万以下 — 新手 F2P 方法，适合刚起步阶段",
        ]
    },
    "osrs-money-making-under-1m-investment-2026.html": {
        "title": "OSRS 低成本赚钱指南 — 100 万本金以内（2026版）",
        "summary": "2026年小本金赚钱攻略。本金不足 100 万 GP 也能赚钱的方法汇总，涵盖倒卖、制作、收集等多种低投入高回报策略。",
        "preview": [
            "📌 涵盖 <strong>15 种低本金赚钱方法</strong> — 从 1 万 GP 起步即可",
            "📌 <strong>最佳倒卖方法：</strong>低买高卖热门消耗品，每天 10 万–50 万 GP，只需 5 万本金",
            "📌 <strong>最佳制作方法：</strong>购买原材料加工后出售，如弓箭、药水、食物",
            "📌 <strong>低风险高回报：</strong>利用 GE 价格波动，批量收购降价物品等待反弹",
            "📌 <strong>滚雪球策略：</strong>1 万 → 10 万 → 100 万 → 1000 万，逐步扩大本金",
        ]
    },
    "osrs-money-making-zero-req-2026.html": {
        "title": "OSRS 零门槛赚钱指南 — 无任何要求（2026版）",
        "summary": "2026年零要求赚钱方法合集。刚创建账号就能开始的赚钱方式，无需战斗、无需技能、无需任务，真正零门槛起步。",
        "preview": [
            "📌 涵盖 <strong>20 种零要求赚钱方法</strong> — 无战斗、无技能、无任务",
            "📌 <strong>最佳拾荒：</strong>卢姆布里奇牛场捡牛皮，每小时 1.5 万–2.5 万 GP",
            "📌 <strong>最佳收集：</strong>瓦洛克矿场捡铁矿石，每小时 2 万–4 万 GP",
            "📌 <strong>最佳倒卖：</strong>利用 GE 市场差价，小本经营逐步扩大",
            "📌 <strong>零门槛到第一桶金：</strong>预估时间 4–6 小时赚取 10 万 GP",
        ]
    },
    "osrs-passive-money-making-offline.html": {
        "title": "OSRS 离线被动收入指南 — 不上线也能赚钱",
        "summary": "利用游戏机制实现离线或低在线时间也能持续赚取金币的被动收入方法指南。包括农场种植、鸟屋、工坊等不费力赚钱方式。",
        "preview": [
            "📌 涵盖 <strong>8 种被动收入方法</strong> — 每天登录 15 分钟即可",
            "📌 <strong>最佳被动收入：</strong>草药种植（Herb Runs）每 80 分钟一次，每次 10 万–30 万 GP",
            "📌 <strong>鸟屋跑图：</strong>每 50 分钟一次，每次 1 万–3 万 GP，顺带训练猎人",
            "📌 <strong>巨海藻种植：</strong>每 70 分钟一次，每次 5 万–10 万 GP",
            "📌 <strong>组合策略：</strong>草药 + 鸟屋 + 海藻 = 每天 200 万+ GP，在线仅需 30 分钟",
        ]
    },
    "osrs-quest-unlocked-money-methods-2026.html": {
        "title": "OSRS 任务解锁赚钱方法 — 完成任务赚大钱（2026版）",
        "summary": "2026年任务解锁赚钱方法大全。梳理各个任务完成后解锁的高收益赚钱途径，让任务奖励从一次性变成长期收入来源。",
        "preview": [
            "📌 涵盖 <strong>20+ 种任务解锁的赚钱方法</strong> — 按任务排序，附 GP/小时数据",
            "📌 <strong>最佳任务解锁：</strong>龙族杀手 II（Dragon Slayer II）解锁韦克思，每小时 200 万+ GP",
            "📌 <strong>早期必做：</strong>瀑布任务（Waterfall Quest）+ 妖精试炼（Fairytale）解锁草药种植",
            "📌 <strong>中等任务：</strong>国王的赎金 + 僧侣好友解锁僧侣鱼和高级锻造",
            "📌 <strong>高回报任务链：</strong>精灵系列任务解锁高级符文制作和 Prifddinas 区域",
        ]
    },
    "osrs-revenants-caves-guide-2026.html": {
        "title": "OSRS 遗迹洞穴赚钱指南 — 高风险高回报（2026版）",
        "summary": "2026年遗迹洞穴（Revenant Caves）完整攻略。高风险高回报的 Wilderness 刷金圣地，包含装备推荐、PK 规避技巧和收益分析。",
        "preview": [
            "📌 <strong>平均收益：</strong>每小时 80 万–200 万 GP，高级玩家可达 300 万+",
            "📌 <strong>最佳装备：</strong>黑面具（Black Mask）+ 魔法短弓（Magic Shortbow），总成本低于 5 万 GP",
            "📌 <strong>PK 规避技巧：</strong>设置单键逃跑、佩戴护身符、学会使用魔咒重定向",
            "📌 <strong>最佳地点：</strong>低级玩家去洞穴入口附近，高级玩家去深层区域",
            "📌 <strong>注意事项：</strong>只携带 3–4 件装备，剩余全部用品，最大化每次利润",
        ]
    },
    "osrs-rune-dragons-money-guide-2026.html": {
        "title": "OSRS 符文龙赚钱指南 — 顶级 PvM 收益（2026版）",
        "summary": "2026年符文龙赚钱攻略。符文龙作为顶级 PvM 内容，掉落符文装备、龙弩等高价物品。本文详解击杀方法、装备搭配和收益统计。",
        "preview": [
            "📌 <strong>平均收益：</strong>每小时 150 万–250 万 GP，稳定且可预测",
            "📌 <strong>主要掉落：</strong>符文装备、龙弩（Dragon Crossbow）部件、符文矿石",
            "📌 <strong>要求：</strong>85+ 战斗技能、龙族杀手 II 任务完成、抗龙火盾",
            "📌 <strong>最佳装备：</strong>近战搭配龙火盾 + 防龙火药水 + 稳定食物",
            "📌 <strong>技巧：</strong>学习符文龙的攻击模式切换，减少食物消耗提高续航",
        ]
    },
    "osrs-slayer-70-to-95-money-makers-2026.html": {
        "title": "OSRS 70-95 级 Slayer 赚钱攻略 — 中期到高级（2026版）",
        "summary": "2026年中级到高级 Slayer（70-95级）赚钱攻略。涵盖 Gargoyle、Nechryael、Kraken、Cerberus、Hydra 等高级 Slayer 怪物的收益分析和击杀技巧。",
        "preview": [
            "📌 涵盖 <strong>70-95 级所有重要 Slayer 任务</strong> — 逐个任务 GP/小时排名",
            "📌 <strong>最佳任务：</strong>九头蛇（Hydra）每小时 320 万 GP + 95 级 Slayer",
            "📌 <strong>弹幕刷怪：</strong>Nechryael 弹幕每小时 250 万 GP + 9 万 Slayer 经验",
            "📌 <strong>最佳拦截列表：</strong>屏蔽低收益任务，扩展高收益任务",
            "📌 <strong>70-95 总计收益：</strong>全程约 1.5 亿–3.5 亿 GP",
        ]
    },
    "osrs-slayer-low-level-money-makers-2026.html": {
        "title": "OSRS 低级 Slayer 赚钱攻略 — 1-70 级快速入门（2026版）",
        "summary": "2026年低级 Slayer（1-70级）赚钱攻略。从零开始，涵盖 Turoth、Basilisk、Bloodveld 等低级别 Slayer 任务的赚钱方法和升级路线。",
        "preview": [
            "📌 涵盖 <strong>1-70 级所有赚钱 Slayer 任务</strong> — 按等级和收益排序",
            "📌 <strong>1-50 级：</strong>主要靠战利品积累，每小时 5 万–20 万 GP",
            "📌 <strong>50-70 级：</strong>Turoth 和 Basilisk 掉落草药和符文，每小时 20 万–50 万 GP",
            "📌 <strong>关键解锁：</strong>55 级解锁 Bloodveld，65 级解锁 Dust Devil，收益大幅提升",
            "📌 <strong>最佳升级策略：</strong>选择 Vannaka/Chaeldar 作为 Slayer 大师，屏蔽最差任务",
        ]
    },
    "osrs-slayer-money-making-guide-2026.html": {
        "title": "OSRS Slayer 赚钱指南 — 全面攻略（2026版）",
        "summary": "2026年 Slayer 赚钱完整指南。从 1 级到 99 级，系统梳理所有 Slayer 任务相关的赚钱方法，包含任务选择策略和装备推荐。",
        "preview": [
            "📌 涵盖 <strong>1-99 级全阶段 Slayer 赚钱方法</strong> — 完整任务选择策略",
            "📌 <strong>低级（1-50）：</strong>以经验为主赚钱为辅，每小时 3 万–10 万 GP",
            "📌 <strong>中级（50-80）：</strong>Gargoyles 和 Nechryael 带来稳定收入，每小时 30 万–80 万 GP",
            "📌 <strong>高级（80-99）：</strong>Cerberus、Kraken、Hydra 等 Boss，每小时 100 万–300 万 GP",
            "📌 <strong>任务选择策略：</strong>何时拦截、何时扩展、何时跳过，最大化利润/时间比",
        ]
    },
    "osrs-vorkath-money-making-guide-2026.html": {
        "title": "OSRS 韦克思赚钱指南 — 新手 Boss 首选（2026版）",
        "summary": "2026年韦克思（Vorkath）赚钱完整攻略。新手友好型 Boss，稳定 2M+ GP/小时。本文涵盖装备搭配、战斗策略、掉落分析和收益计算。",
        "preview": [
            "📌 <strong>平均收益：</strong>每小时 200 万–300 万 GP，OSRS 最稳定的赚钱 Boss 之一",
            "📌 <strong>要求：</strong>龙族杀手 II 任务完成、75+ 远程或近战、抗龙火盾",
            "📌 <strong>最佳策略：</strong>远程使用龙弩（Dragon Hunter Crossbow）+ 防龙火盾",
            "📌 <strong>效率翻倍：</strong>学会快速处理特殊攻击阶段，减少每击杀时间",
            "📌 <strong>背包配置：</strong>合理携带食物/药水/掉落，一次可停留 20-30 击杀",
        ]
    },
}


# ============================================================
# HTML processing via line-by-line approach
# ============================================================

def build_zh_head(en_html, filename):
    """Build <head> for Chinese version from English head."""
    m = re.search(r'<head>(.*?)</head>', en_html, re.DOTALL)
    if not m:
        return ""
    head = m.group(1)
    
    cn_title = CN_INFO.get(filename, {}).get("title", filename)
    cn_summary = CN_INFO.get(filename, {}).get("summary", "")
    base_url = f"https://osrsguru.com/zh/guides/{filename}"
    en_url = f"https://osrsguru.com/guides/{filename}"
    
    # Replace title
    head = re.sub(r'<title>.*?</title>', f'<title>{cn_title}</title>', head)
    
    # Replace or add meta description  
    desc = f'完整OSRS 赚钱攻略（2026版）：GP/小时对比、装备要求、收益分析。{cn_summary}'
    if re.search(r'<meta name="description"', head):
        head = re.sub(
            r'<meta name="description"[^>]*>',
            f'<meta name="description" content="{desc}">',
            head
        )
    
    # Update OG title if exists
    if re.search(r'<meta property="og:title"', head):
        head = re.sub(
            r'<meta property="og:title"[^>]*>',
            f'<meta property="og:title" content="{cn_title}">',
            head
        )
    
    # Update OG url to zh version
    if re.search(r'<meta property="og:url"', head):
        head = re.sub(
            r'<meta property="og:url"[^>]*>',
            f'<meta property="og:url" content="{base_url}">',
            head
        )
    
    # Update OG description
    if re.search(r'<meta property="og:description"', head):
        head = re.sub(
            r'<meta property="og:description"[^>]*>',
            f'<meta property="og:description" content="{desc}">',
            head
        )
    
    # Remove existing canonical and hreflang
    head = re.sub(r'<link rel="canonical".*?>', '', head)
    head = re.sub(r'<link rel="alternate".*?>', '', head)
    
    # Add zh canonical and proper hreflang (append to head content)
    zh_tags = f'''
    <link rel="canonical" href="{base_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="zh" href="{base_url}">
    <link rel="alternate" hreflang="x-default" href="{base_url}">
    '''
    head = head + zh_tags
    
    return head


def build_body(filename):
    """Build the full body content from English source with Chinese annotations."""
    en_path = os.path.join(BASE_DIR, "guides", filename)
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    cn_info = CN_INFO.get(filename, {})
    cn_title = cn_info.get("title", "")
    cn_summary = cn_info.get("summary", "")
    cn_preview = cn_info.get("preview", [])
    
    en_lines = en_html.split('\n')
    out_lines = []
    
    # Find start of content (skip <head>, <header>, start at guide-hero or hero-image)
    content_start = None
    for i, line in enumerate(en_lines):
        s = line.strip()
        if ('<section' in s and 'class="guide-hero"' in s) or \
           ('class="hero-image"' in s and ('<div' in s or 'style=' in s)):
            content_start = i
            break
    
    # Fallback: start after </header>
    if content_start is None:
        for i, line in enumerate(en_lines):
            if '</header>' in line:
                content_start = i + 1
                break
    
    if content_start is None:
        content_start = 0
    
    # Find end of content (before support-card, tool-callout, </main>, or <footer>)
    content_end = None
    for i in range(content_start, len(en_lines)):
        l = en_lines[i]
        if 'class="support-card"' in l:
            content_end = i
            break
        if 'class="tool-callout"' in l:
            content_end = i
            break
    
    if content_end is None:
        for i in range(content_start, len(en_lines)):
            if '</main>' in en_lines[i]:
                content_end = i
                break
    
    if content_end is None:
        for i in range(content_start, len(en_lines)):
            if '<footer>' in en_lines[i]:
                content_end = i
                break
    
    if content_end is None:
        content_end = len(en_lines)
    
    body_lines = en_lines[content_start:content_end]
    
    # Now process body_lines to add Chinese annotations
    i = 0
    skip_quick_summary = False
    
    while i < len(body_lines):
        line = body_lines[i]
        stripped = line.strip()
        
        # --- Phase 1: Skip original 30-second preview sections (quick-summary or quick-preview) ---
        if ('class="quick-summary"' in stripped or 'class="quick-preview"' in stripped):
            # Skip the entire original quick-summary block
            depth = 0
            depth += line.count('<div') - line.count('</div')
            i += 1
            while i < len(body_lines) and depth > 0:
                depth += body_lines[i].count('<div') - body_lines[i].count('</div')
                i += 1
            # Add Chinese quick-summary
            out_lines.append(f'            <div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">')
            out_lines.append(f'                <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⚡ 30秒快速预览</h3>')
            out_lines.append(f'                <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">')
            for bullet in cn_preview:
                out_lines.append(f'                    <li>{bullet}</li>')
            out_lines.append(f'                </ul>')
            out_lines.append(f'            </div>')
            continue
        
        # --- Phase 2: Add cn-title and cn-summary after h1 ---
        if '<h1' in stripped and 'font-size' in stripped:
            # This is the hero-image style h1 (slayer-70-to-95 etc.)
            out_lines.append(line)
            if cn_title:
                out_lines.append(f'            <h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title}</h1>')
            if cn_summary:
                out_lines.append(f'            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>')
            i += 1
            continue
        
        if stripped == '<h1>' or stripped.startswith('<h1>') or (stripped.startswith('<h1 ') and 'style' not in stripped):
            # Standard h1 in guide-hero
            # Check if we're inside guide-hero (look back)
            ctx = '\n'.join(out_lines[-5:]) if len(out_lines) >= 5 else '\n'.join(out_lines)
            if 'guide-hero' in ctx:
                out_lines.append(line)
                if cn_title:
                    out_lines.append(f'            <h1 class="cn-title" style="font-size:1.5rem;color:#1a1a1a;margin-bottom:4px;font-weight:700;">{cn_title}</h1>')
                if cn_summary:
                    out_lines.append(f'            <p class="cn-summary" style="color:#333;font-size:0.95rem;margin-bottom:16px;line-height:1.6;">{cn_summary}</p>')
                i += 1
                continue
            else:
                out_lines.append(line)
                i += 1
                continue
        
        # --- Phase 3: TOC items - add（中文翻译）---
        if 'class="toc"' in stripped or stripped == '<div class="toc">':
            out_lines.append(line)
            i += 1
            # Track depth inside TOC
            depth = 1  # counting from after the toc opening
            while i < len(body_lines) and depth > 0:
                l = body_lines[i]
                s = l.strip()
                depth += l.count('<div') - l.count('</div')
                
                # Add（中文翻译）to TOC list items
                if '<li>' in s and '<a href=' in s and depth == 1:
                    m = re.search(r'<a href="([^"]*)">(.*?)</a>', s)
                    if m and '（' not in m.group(2):
                        href = m.group(1)
                        text = m.group(2)
                        indent = re.match(r'^(\s*)', l).group(1)
                        out_lines.append(f'{indent}<li><a href="{href}">{text}（中文翻译）</a></li>')
                        i += 1
                        continue
                
                out_lines.append(l)
                i += 1
            continue
        
        # --- Phase 4: h2 - add（中文标题）---
        if re.match(r'^\s*<h2[>\s]', stripped):
            # Extract text between <h2> and </h2>
            m = re.match(r'(\s*)<h2[^>]*>(.*?)</h2>', stripped)
            if m:
                indent, text = m.group(1), m.group(2)
                # Skip if already annotated
                if '（' not in text and '中文' not in text:
                    cleaned = re.sub(r'（[^）]*）', '', text).strip()
                    out_lines.append(f'{indent}<h2>{cleaned}（中文标题）</h2>')
                else:
                    out_lines.append(line)
            else:
                out_lines.append(line)
            i += 1
            continue
        
        # --- Phase 5: h3 - add（中文说明）, but NOT in tool-cta, card, sidebar contexts ---
        if re.match(r'^\s*<h3[>\s]', stripped):
            # Check context - look at recent lines to see if we're in a sidebar
            ctx = '\n'.join(out_lines[-15:] + [''] + [line]) if len(out_lines) >= 15 else '\n'.join(out_lines + [''] + [line])
            if any(skip in ctx for skip in ['tool-cta', 'tool-callout', 'support-card', 'related-guides', 'article-card']):
                out_lines.append(line)
                i += 1
                continue
            
            m = re.match(r'(\s*)<h3[^>]*>(.*?)</h3>', stripped)
            if m:
                indent, text = m.group(1), m.group(2)
                if '（' not in text and '中文' not in text:
                    cleaned = re.sub(r'（[^）]*）', '', text).strip()
                    out_lines.append(f'{indent}<h3>{cleaned}（中文说明）</h3>')
                else:
                    out_lines.append(line)
            else:
                out_lines.append(line)
            i += 1
            continue
        
        # Default: pass through
        out_lines.append(line)
        i += 1
    
    return '\n'.join(out_lines)


def extract_header(en_html):
    """Extract header from English HTML."""
    m = re.search(r'(<header[^>]*>.*?</header>)', en_html, re.DOTALL)
    return m.group(1) if m else ""


def extract_footer(en_html):
    """Extract support card + footer from English HTML."""
    # Find support card
    m = re.search(r'(<div class="support-card".*)', en_html, re.DOTALL)
    if m:
        return m.group(1)
    # Fallback
    m = re.search(r'(</main>\s*.*)', en_html, re.DOTALL)
    return m.group(1) if m else ""


def process_article(filename):
    """Process a single article."""
    en_path = os.path.join(BASE_DIR, "guides", filename)
    zh_path = os.path.join(BASE_DIR, "zh/guides", filename)
    
    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    print(f"{'='*60}")
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    # Build parts
    zh_head = build_zh_head(en_html, filename)
    header = extract_header(en_html)
    body = build_body(filename)
    footer = extract_footer(en_html)
    
    if not body:
        print(f"  ERROR: Empty body")
        return False
    
    # Assemble final HTML
    out = []
    out.append('<!DOCTYPE html>')
    out.append('<html lang="zh-Hans">')
    out.append('<head>')
    out.append(zh_head.strip())
    out.append('</head>')
    out.append('<body>')
    out.append(header.strip())
    out.append('')
    out.append(body.strip())
    out.append('')
    # Strip body/html tags from footer end only
    footer_clean = footer.strip()
    # Remove ALL </body> and </html> tags (handles pre-existing duplicates in source)
    footer_clean = re.sub(r'</body>\s*', '', footer_clean)
    footer_clean = re.sub(r'</html>\s*', '', footer_clean)
    out.append(footer_clean.strip())
    out.append('</body>')
    out.append('</html>')
    
    final_html = '\n'.join(out)
    
    os.makedirs(os.path.dirname(zh_path), exist_ok=True)
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"  Written: {zh_path} ({len(final_html)} chars)")
    return True


if __name__ == '__main__':
    success = 0
    fail = 0
    for article in ARTICLES:
        if process_article(article):
            success += 1
        else:
            fail += 1
    print(f"\n{'='*60}")
    print(f"Done: {success} succeeded, {fail} failed out of {len(ARTICLES)}")
