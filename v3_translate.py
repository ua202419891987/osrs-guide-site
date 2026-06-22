#!/usr/bin/env python3
"""
OSRS Guru v3 Translation Script
Automates mechanical transformations for v3 format (English + Chinese annotations)
"""
import re
import sys
import os

# Chinese translations for common elements
TITLE_MAP = {
    "osrs-ironman-p2p-money-making-2026.html": "OSRS Ironman P2P 赚钱指南 2026 — 9种方法 | OSRS Guru",
    "first-5m-gp-members-2026.html": "OSRS 新手会员首个500万金币 2026 — 7种赚钱方法 | OSRS Guru",
    "mid-game-money-making-2026.html": "OSRS 中期赚钱指南 2026 — 从100万到1亿金币 | OSRS Guru",
    "osrs-first-100m-gp-mid-level-2026.html": "OSRS 首个1亿金币指南 2026 — 中级赚钱方法 | OSRS Guru",
    "osrs-daily-weekly-money-routine-2026.html": "OSRS 每日每周赚钱流程 2026 — 被动收入计划 | OSRS Guru",
    "osrs-low-level-skilling-money-makers-2026.html": "OSRS 低等级技能赚钱方法 2026 — 零战斗要求 | OSRS Guru",
    "osrs-slayer-money-making-guide-2026.html": "OSRS Slayer 赚钱完全指南 2026 — 从1级到99级 | OSRS Guru",
    "osrs-slayer-low-level-money-makers-2026.html": "OSRS Slayer 低等级赚钱方法 2026 — 初学者指南 | OSRS Guru",
    "osrs-combat-money-making-non-boss-2026.html": "OSRS 非Boss战斗赚钱方法 2026 — 稳定金币收入 | OSRS Guru",
    "osrs-quest-unlocked-money-methods-2026.html": "OSRS 任务解锁赚钱方法 2026 — 任务奖励金币指南 | OSRS Guru",
    "osrs-money-making-tier-list-2026.html": "OSRS 赚钱方法等级排名 2026 — 从S到F级别 | OSRS Guru",
    "osrs-money-making-under-1m-investment-2026.html": "OSRS 不到100万投资赚钱方法 2026 — 低成本高回报 | OSRS Guru",
}

DESC_MAP = {
    "osrs-ironman-p2p-money-making-2026.html": "2026年OSRS铁人会员赚钱完整指南。涵盖属性40-70的自给自足赚钱方法，无需依赖Grand Exchange。含高炼金、偷窃、敏捷金字塔等多种方法。",
    "first-5m-gp-members-2026.html": "刚买会员就破产了？2026年OSRS新手会员首个500万金币详细攻略。含鸟屋、药草种植、Blast Furnace、Slayer等7种方法及精确金币/小时数据。",
    "mid-game-money-making-2026.html": "从第一个百万到一亿金币的完整OSRS中期赚钱指南。Barrows、Zulrah、Vorkath、Slayer、药草循环、GE倒卖及被动收入方法对比分析。",
    "osrs-first-100m-gp-mid-level-2026.html": "OSRS中级玩家首个1亿金币完整攻略。涵盖中级战斗赚钱、技能赚钱、被动收入及每日流程的详细方法。",
    "osrs-daily-weekly-money-routine-2026.html": "2026年OSRS每日每周赚钱流程完整指南。被动收入计划，从日常活动到每周任务的最佳金币获取方案。",
    "osrs-low-level-skilling-money-makers-2026.html": "OSRS低等级技能赚钱方法指南。零战斗要求的高效赚钱方式，适合新手和技能型玩家。",
    "osrs-slayer-money-making-guide-2026.html": "2026年OSRS Slayer赚钱完全指南。从1级到99级，每个阶段的Slayer怪物最佳金币获取方法及掉落列表。",
    "osrs-slayer-low-level-money-makers-2026.html": "OSRS Slayer低等级赚钱方法指南。适合初学者的最佳Slayer任务和怪物选择。",
    "osrs-combat-money-making-non-boss-2026.html": "OSRS非Boss战斗赚钱方法指南。无需高难度Boss战斗也能高效获取金币的稳定方法。",
    "osrs-quest-unlocked-money-methods-2026.html": "OSRS任务解锁赚钱方法完整指南。通过完成特定任务解锁的高效金币获取方式。",
    "osrs-money-making-tier-list-2026.html": "2026年OSRS赚钱方法等级排名。从S级到F级的完整排名，帮助玩家选择最优赚钱方式。",
    "osrs-money-making-under-1m-investment-2026.html": "不到100万金币投资的OSRS赚钱方法指南。低成本高回报的最佳选择。",
}

KW_MAP = {
    "osrs-ironman-p2p-money-making-2026.html": "OSRS铁人赚钱,OSRS铁人P2P金币,OSRS铁人中期赚钱,OSRS敏捷金字塔铁人,OSRS铁人偷窃金币,OSRS铁人高炼金,OSRS铁人Slayer掉落",
    "first-5m-gp-members-2026.html": "OSRS新手赚钱,OSRS会员赚钱,OSRS首个500万,OSRS鸟屋赚钱,OSRS药草种植利润,OSRS Blast Furnace赚钱,OSRS新手金币指南",
    "mid-game-money-making-2026.html": "OSRS中期赚钱,OSRS 100万到1亿,Barrows赚钱,Zulrah赚钱,Vorkath赚钱,Slayer利润,药草循环,GE倒卖",
    "osrs-first-100m-gp-mid-level-2026.html": "OSRS首个1亿,OSRS中级赚钱,OSRS中期金币,OSRS战斗赚钱,OSRS技能赚钱",
    "osrs-daily-weekly-money-routine-2026.html": "OSRS日常赚钱,OSRS每周赚钱,OSRS被动收入,OSRS金币流程,OSRS每日任务金币",
    "osrs-low-level-skilling-money-makers-2026.html": "OSRS低等级赚钱,OSRS技能赚钱,OSRS零战斗赚钱,OSRS新手赚钱方法,OSRS采集赚钱",
    "osrs-slayer-money-making-guide-2026.html": "OSRS Slayer赚钱,OSRS Slayer金币,OSRS Slayer掉落,OSRS Slayer 1-99,OSRS Slayer任务金币",
    "osrs-slayer-low-level-money-makers-2026.html": "OSRS Slayer新手,OSRS低等级Slayer,OSRS Slayer赚钱,OSRS Slayer初级指南",
    "osrs-combat-money-making-non-boss-2026.html": "OSRS战斗赚钱,OSRS非Boss金币,OSRS怪物掉落金币,OSRS稳定赚钱",
    "osrs-quest-unlocked-money-methods-2026.html": "OSRS任务赚钱,OSRS任务金币,OSRS任务奖励,OSRS任务解锁方法",
    "osrs-money-making-tier-list-2026.html": "OSRS赚钱排名,OSRS赚钱等级,OSRS金币方法排名,OSRS最佳赚钱,OSRS赚钱对比",
    "osrs-money-making-under-1m-investment-2026.html": "OSRS低成本赚钱,OSRS小投资赚钱,OSRS 100万以下赚钱,OSRS新手投资赚钱",
}

H1_SUBTITLE_MAP = {
    "osrs-ironman-p2p-money-making-2026.html": "— 铁人P2P赚钱完全指南：9种方法（100K-800K/小时）",
    "first-5m-gp-members-2026.html": "— 新手会员首个500万金币完整攻略：7种方法",
    "mid-game-money-making-2026.html": "— 中期赚钱完全指南：从1M到100M金币",
    "osrs-first-100m-gp-mid-level-2026.html": "— 中级玩家首个1亿金币攻略",
    "osrs-daily-weekly-money-routine-2026.html": "— 每日每周赚钱流程：被动收入蓝图",
    "osrs-low-level-skilling-money-makers-2026.html": "— 低等级技能赚钱方法大全",
    "osrs-slayer-money-making-guide-2026.html": "— Slayer赚钱完全指南：1-99级",
    "osrs-slayer-low-level-money-makers-2026.html": "— Slayer低等级赚钱入门指南",
    "osrs-combat-money-making-non-boss-2026.html": "— 非Boss战斗赚钱方法指南",
    "osrs-quest-unlocked-money-methods-2026.html": "— 任务解锁赚钱方法大全",
    "osrs-money-making-tier-list-2026.html": "— 赚钱方法完整等级排名",
    "osrs-money-making-under-1m-investment-2026.html": "— 不到100万投资赚钱方法指南",
}

BREADCRUMB_LAST_MAP = {
    "osrs-ironman-p2p-money-making-2026.html": "OSRS Ironman P2P 赚钱指南",
    "first-5m-gp-members-2026.html": "新手首个500万金币",
    "mid-game-money-making-2026.html": "中期赚钱完全指南",
    "osrs-first-100m-gp-mid-level-2026.html": "首个1亿金币攻略",
    "osrs-daily-weekly-money-routine-2026.html": "每日每周赚钱流程",
    "osrs-low-level-skilling-money-makers-2026.html": "低等级技能赚钱",
    "osrs-slayer-money-making-guide-2026.html": "Slayer 赚钱指南",
    "osrs-slayer-low-level-money-makers-2026.html": "Slayer 低等级赚钱",
    "osrs-combat-money-making-non-boss-2026.html": "非Boss战斗赚钱",
    "osrs-quest-unlocked-money-methods-2026.html": "任务解锁赚钱方法",
    "osrs-money-making-tier-list-2026.html": "赚钱方法等级排名",
    "osrs-money-making-under-1m-investment-2026.html": "低成本投资赚钱",
}

PUB_DATE_MAP = {
    "osrs-ironman-p2p-money-making-2026.html": ("2026-06-08", "2026-06-15"),
    "first-5m-gp-members-2026.html": ("2026-06-01", "2026-06-08"),
    "mid-game-money-making-2026.html": ("2026-06-01", "2026-06-08"),
}

# Default dates for files without specific dates
DEFAULT_DATES = ("2026-06-01", "2026-06-08")

def get_meta(filename):
    """Get metadata for a file"""
    title = TITLE_MAP.get(filename, "OSRS Guide | OSRS Guru")
    desc = DESC_MAP.get(filename, "OSRS攻略中文版")
    keywords = KW_MAP.get(filename, "OSRS")
    h1_subtitle = H1_SUBTITLE_MAP.get(filename, "")
    breadcrumb_last = BREADCRUMB_LAST_MAP.get(filename, "攻略")
    pub_date, mod_date = PUB_DATE_MAP.get(filename, DEFAULT_DATES)
    return title, desc, keywords, h1_subtitle, breadcrumb_last, pub_date, mod_date

def generate_head(filename, title, desc, keywords, pub_date, mod_date):
    """Generate v3 head section"""
    return f'''<!DOCTYPE html>
<html lang="zh">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S1BGC91MYV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-S1BGC91MYV');
</script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="dns-prefetch" href="//www.google-analytics.com">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="https://osrsguru.com/zh/guides/{filename}">
  <link rel="alternate" hreflang="en" href="https://osrsguru.com/guides/{filename}">
  <link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/guides/{filename}">

  <meta property="og:title" content="{title}">
 <meta property="og:description" content="{desc}">
 <meta property="og:type" content="article">
 <meta property="og:url" content="https://osrsguru.com/zh/guides/{filename}">
 <meta property="article:published_time" content="{pub_date}T08:00:00+00:00">
 <meta property="article:modified_time" content="{mod_date}T12:00:00+00:00">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "author": {{"@type": "Organization", "name": "OSRS Guru"}},
  "publisher": {{"@type": "Organization", "name": "OSRS Guru", "url": "https://osrsguru.com"}},
  "datePublished": "{pub_date}",
  "dateModified": "{mod_date}",
  "mainEntityOfPage": "https://osrsguru.com/zh/guides/{filename}"
}}
</script>
<link rel="stylesheet" href="../../css/style.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435" crossorigin="anonymous"></script>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="header-inner">
    <a href="../../index.html" class="logo">OSRS<span>Guru</span></a>
    <nav id="main-nav">
      <a href="../../index.html">首页</a>
      <a href="../../money-making.html" class="active">赚钱方法</a>
      <a href="../../skill-training.html">技能训练</a>
      <a href="../../quest-guides.html">任务</a>
      <a href="../../boss-guides.html">Boss攻略</a>
    </nav>
    <a href="../../money-making.html" class="btn btn-primary header-cta">更多攻略</a>
    <button class="menu-toggle" onclick="document.getElementById('main-nav').classList.toggle('open')" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
'''

def generate_footer():
    """Generate v3 footer"""
    return '''
<!-- FOOTER -->
<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="logo">OSRS<span>Guru</span></div>
        <p>OSRS Guru — 你的Old School RuneScape攻略站。所有内容基于2026年游戏机制更新。</p>
      </div>
      <div class="footer-col">
        <h4>Money Making<span style="font-size:0.75em;font-weight:400;">（赚钱方法）</span></h4>
        <ul>
          <li><a href="osrs-ironman-money-making-f2p-2026.html">Ironman F2P</a></li>
          <li><a href="osrs-ironman-p2p-money-making-2026.html">Ironman P2P</a></li>
          <li><a href="mid-game-money-making-2026.html">Mid-Game Money</a></li>
          <li><a href="../../money-making.html">All Methods →</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Skill Training<span style="font-size:0.75em;font-weight:400;">（技能训练）</span></h4>
        <ul>
          <li><a href="osrs-1-99-crafting-guide-2026.html">99 Crafting</a></li>
          <li><a href="osrs-1-99-farming-guide-beginner-profit-2026.html">99 Farming</a></li>
          <li><a href="osrs-1-99-thieving-guide-ironman.html">99 Thieving</a></li>
          <li><a href="../../skill-training.html">All Skills →</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Boss &amp; Quests<span style="font-size:0.75em;font-weight:400;">（Boss与任务）</span></h4>
        <ul>
          <li><a href="osrs-how-to-beat-zulrah-beginners-rotation.html">Zulrah Guide</a></li>
          <li><a href="osrs-quest-unlocked-money-methods-2026.html">Quest Money</a></li>
          <li><a href="../../boss-guides.html">All Bosses →</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 OSRS Guru (osrsguru.com). All rights reserved.
      <br><small style="opacity:0.7;">Fan site, not affiliated with Jagex Ltd. / 粉丝站点，非Jagex官方关联。</small></span>
    </div>
  </div>
</footer>

<script src="/js/main.js"></script>
<script src="../../js/features.js"></script>
<script src="../../js/ai-qa-widget.js"></script>
<style>.guide-content li{{color:#e8d5b7!important}}</style>
</body>
</html>'''

# ========== H2/H3 Chinese annotation mapping ==========
# These are content-specific and need to be defined per file

H2_ANNOTATIONS = {
    "osrs-ironman-p2p-money-making-2026.html": {
        "🎯 Why Ironman Is Different: GP Economy": "（为什么铁人与众不同：金币经济体系）",
        "🏃 Agility Pyramid: 100K-200K/hr (Level 30+)": "（敏捷金字塔 · 每小时100K-200K · 30级起）",
        "🗡️ Thieving: 200K/hr (Knights + Masters)": "（偷窃 · 每小时200K · 骑士+农场主）",
        "✨ High Alchemy: Profit List (Battlestaves + Bows)": "（高炼金 · 利润一览 · 战斗法杖+弓）",
        "⚔️ Slayer Drops: 300K/hr (Best Tasks)": "（Slayer掉落 · 每小时300K · 最佳任务）",
        "🔨 Crafting/Fletching: GP + XP (Battlestaves + Bows)": "（制造/制弓 · 金币+经验 · 战斗法杖+弓）",
        "🔨 Giant's Foundry — Smithing Items into GP": "（巨人铸造 · 将锻炼物品转化为金币）",
        "📅 Daily GP for Ironmen — Battlestaves, Herb Runs, Birdhouses": "（铁人日常金币 · 战斗法杖、药草、鸟屋）",
        "❓ FAQ": "（常见问题）",
    }
}

H3_ANNOTATIONS = {
    "osrs-ironman-p2p-money-making-2026.html": {
        "📊 The Ironman GP Economy": "（铁人金币经济体系）",
        "💡 Key Ironman Money Making Principles": "（铁人赚钱核心原则）",
        "📋 Mid-Game Ironman GP Needs (Priority)": "（中期铁人金币需求 · 优先级排序）",
        "📋 Agility Pyramid Basics": "（敏捷金字塔基础知识）",
        "🗺️ Agility Pyramid Route Guide": "（敏捷金字塔路线指南）",
        "🎯 Ironman-Specific Considerations": "（铁人特别注意事项）",
        "📊 Thieving Method Comparison": "（偷窃方法对比）",
        "🏠 HAM Store Rooms — The Early Game Ironman GP Strategy": "（HAM储藏室 · 早期铁人金币获取策略）",
        "🌾 Master Farmers — The Ironman Meta": "（农场主 · 铁人核心玩法）",
        "✨ Best Ironman Alch Items (Craftable)": "（最佳铁人炼金物品 · 可制作）",
        "🌿 Nature Rune Supply for Ironmen": "（铁人自然符文的获取来源）",
        "🎯 Best Slayer Tasks for Ironman GP": "（铁人最佳Slayer金币任务）",
        "💡 Slayer Money Management Tips for Ironmen": "（铁人Slayer金币管理技巧）",
        "🔨 Battlestaves — The Ironman GP Engine": "（战斗法杖 · 铁人金币引擎）",
        "🏹 Fletching for GP — Yew Longbows and Magic Longbows": "（制弓赚钱 · 紫杉长弓与魔法长弓）",
        "💍 Crafting Jewelry for GP — Gem Mining and Gold Bars": "（制作珠宝赚钱 · 宝石采矿与金条）",
        "🔨 Giant's Foundry Basics": "（巨人铸造基础知识）",
        "🎯 Ironman Integration with Giant's Foundry": "（铁人与巨人铸造的结合运用）",
        "📅 Daily GP Routine (Mid-Game Ironman)": "（日常金币流程 · 中期铁人）",
        "📋 The Ironman Daily GP Blueprint": "（铁人日常金币蓝图）",
    }
}

def process_file(filename):
    """Process a single file"""
    src_path = f'C:/Users/Lenovo/osrs-guide-site/guides/{filename}'
    dest_path = f'C:/Users/Lenovo/osrs-guide-site/zh/guides/{filename}'
    
    if not os.path.exists(src_path):
        print(f"  SKIP: {filename} — source not found")
        return False
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title, desc, keywords, h1_subtitle, breadcrumb_last, pub_date, mod_date = get_meta(filename)
    
    # 1. Remove everything before </header> and after <footer>
    # Extract the main content body
    # For now, just print what would be done
    print(f"  Processing: {filename}")
    print(f"    Title: {title}")
    print(f"    Breadcrumb: {breadcrumb_last}")
    
    return True

if __name__ == '__main__':
    files = [
        "osrs-ironman-p2p-money-making-2026.html",
        "first-5m-gp-members-2026.html",
        "mid-game-money-making-2026.html",
    ]
    
    for f in files:
        process_file(f)
