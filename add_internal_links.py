#!/usr/bin/env python3
"""
批量给 OSRS 攻略文章添加内链
每个攻略页面添加 3-5 个相关文章的链接
"""

import re
import os
from pathlib import Path

# 网站根目录
BASE_DIR = Path(__file__).parent
GUIDES_DIR = BASE_DIR / "guides"

# 内链映射表：每篇文章推荐的相关文章（3-5个）
# 格式：文件名 -> [相关文件名列表]
INTERNAL_LINKS = {
    # 赚钱攻略类
    "osrs-ironman-money-making-f2p-2026.html": [
        "osrs-low-effort-money-making-for-beginners.html",
        "osrs-f2p-money-making-no-stats-required.html",
        "osrs-f2p-ironman-money-making-early-game.html",
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-passive-money-making-while-offline.html",
    ],
    "osrs-low-effort-money-making-for-beginners.html": [
        "osrs-ironman-money-making-f2p-2026.html",
        "osrs-f2p-money-making-no-stats-required.html",
        "osrs-passive-money-making-while-offline.html",
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-wintertodt-money-making-per-hour.html",
    ],
    "osrs-how-to-make-gold-with-fishing-2026.html": [
        "osrs-fastest-99-cooking-guide-f2p.html",
        "osrs-how-to-get-99-fishing-afk-method.html",
        "osrs-ironman-money-making-f2p-2026.html",
        "osrs-low-effort-money-making-for-beginners.html",
        "osrs-how-to-make-money-with-zulrah.html",
    ],
    "osrs-f2p-money-making-no-stats-required.html": [
        "osrs-ironman-money-making-f2p-2026.html",
        "osrs-low-effort-money-making-for-beginners.html",
        "osrs-f2p-ironman-money-making-early-game.html",
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-killing-green-dragons-money-per-hour.html",
    ],
    "osrs-passive-money-making-while-offline.html": [
        "osrs-low-effort-money-making-for-beginners.html",
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-wintertodt-money-making-per-hour.html",
        "osrs-ironman-money-making-f2p-2026.html",
    ],
    "osrs-how-to-flip-items-for-profit-mid-game.html": [
        "osrs-cheap-flipping-methods-for-new-players.html",
        "osrs-how-to-rune-spinning-profit-2026.html",
        "osrs-hunter-money-making-guide-2026.html",
    ],
    "osrs-cheap-flipping-methods-for-new-players.html": [
        "osrs-how-to-flip-items-for-profit-mid-game.html",
        "osrs-cheapest-99-runecrafting-2026.html",
        "osrs-low-effort-money-making-for-beginners.html",
    ],
    "osrs-hunter-money-making-guide-2026.html": [
        "osrs-1-99-hunter-guide-afk-method.html",
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-low-effort-money-making-for-beginners.html",
        "osrs-wintertodt-money-making-per-hour.html",
    ],
    "osrs-how-to-make-money-with-crafting-low-level.html": [
        "osrs-cheapest-99-runecrafting-2026.html",
        "osrs-fastest-99-cooking-guide-f2p.html",
        "osrs-how-to-get-graceful-outfit-full-guide.html",
    ],
    "osrs-wintertodt-money-making-per-hour.html": [
        "osrs-how-to-get-99-fishing-afk-method.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-passive-money-making-while-offline.html",
        "osrs-low-effort-money-making-for-beginners.html",
    ],
    "osrs-chambers-of-xeric-loot-profit-guide.html": [
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-how-to-fight-corporeal-beast-loot-guide.html",
        "osrs-sarachnis-loot-guide-for-ironman.html",
    ],
    "osrs-f2p-ironman-money-making-early-game.html": [
        "osrs-ironman-money-making-f2p-2026.html",
        "osrs-f2p-money-making-no-stats-required.html",
        "osrs-low-effort-money-making-for-beginners.html",
        "osrs-1-99-thieving-guide-for-ironman.html",
    ],
    "osrs-how-to-rune-spinning-profit-2026.html": [
        "osrs-cheap-flipping-methods-for-new-players.html",
        "osrs-how-to-flip-items-for-profit-mid-game.html",
        "osrs-cheapest-99-runecrafting-2026.html",
    ],
    "osrs-killing-green-dragons-money-per-hour.html": [
        "osrs-how-to-get-dragon-defender-2026.html",
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-how-to-make-money-with-zulrah.html",
    ],
    "osrs-how-to-make-money-with-zulrah.html": [
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-sarachnis-loot-guide-for-ironman.html",
    ],
    # 技能训练类
    "osrs-fastest-99-cooking-guide-f2p.html": [
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-low-cost-1-99-herblore-guide.html",
        "osrs-how-to-get-graceful-outfit-full-guide.html",
    ],
    "osrs-1-99-thieving-guide-for-ironman.html": [
        "osrs-ironman-1-99-smithing-guide.html",
        "osrs-f2p-ironman-money-making-early-game.html",
        "osrs-how-to-increase-slayer-points-fast.html",
    ],
    "osrs-cheapest-99-runecrafting-2026.html": [
        "osrs-how-to-unlock-the-abyss-guide.html",
        "osrs-cheap-flipping-methods-for-new-players.html",
        "osrs-low-cost-1-99-herblore-guide.html",
    ],
    "osrs-how-to-get-99-fishing-afk-method.html": [
        "osrs-how-to-make-gold-with-fishing-2026.html",
        "osrs-fastest-99-cooking-guide-f2p.html",
        "osrs-1-99-woodcutting-guide-early-game.html",
    ],
    "osrs-1-99-woodcutting-guide-early-game.html": [
        "osrs-ironman-1-99-smithing-guide.html",
        "osrs-how-to-get-to-fossil-island-quick-guide.html",
        "osrs-how-to-train-prayer-cheap-f2p.html",
    ],
    "osrs-fastest-99-attack-strength-defence.html": [
        "osrs-how-to-get-dragon-defender-2026.html",
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
    ],
    "osrs-how-to-train-prayer-cheap-f2p.html": [
        "osrs-fastest-99-cooking-guide-f2p.html",
        "osrs-low-cost-1-99-herblore-guide.html",
        "osrs-desert-treasure-quest-guide-for-low-level.html",
    ],
    "osrs-1-99-hunter-guide-afk-method.html": [
        "osrs-hunter-money-making-guide-2026.html",
        "osrs-how-to-get-to-fossil-island-quick-guide.html",
        "osrs-how-to-unlock-dinosaur-hunting-osrs.html",
    ],
    "osrs-ironman-1-99-smithing-guide.html": [
        "osrs-how-to-get-dragon-defender-2026.html",
        "osrs-1-99-thieving-guide-for-ironman.html",
        "osrs-fastest-99-attack-strength-defence.html",
    ],
    "osrs-how-to-unlock-dinosaur-hunting-osrs.html": [
        "osrs-how-to-get-to-fossil-island-quick-guide.html",
        "osrs-1-99-hunter-guide-afk-method.html",
        "osrs-how-to-get-to-alchemical-hydra-guide.html",
    ],
    "osrs-how-to-get-99-agility-fast-2026.html": [
        "osrs-fastest-99-agility-guide-2026.html",
        "osrs-how-to-get-graceful-outfit-full-guide.html",
        "osrs-how-to-increase-slayer-points-fast.html",
    ],
    "osrs-fastest-99-agility-guide-2026.html": [
        "osrs-how-to-get-99-agility-fast-2026.html",
        "osrs-how-to-get-graceful-outfit-full-guide.html",
        "osrs-how-to-increase-slayer-points-fast.html",
    ],
    "osrs-low-cost-1-99-herblore-guide.html": [
        "osrs-cheapest-99-runecrafting-2026.html",
        "osrs-how-to-train-prayer-cheap-f2p.html",
        "osrs-fastest-99-cooking-guide-f2p.html",
    ],
    # 任务剧情类
    "osrs-how-to-get-dragon-defender-2026.html": [
        "osrs-fastest-99-attack-strength-defence.html",
        "osrs-ironman-1-99-smithing-guide.html",
        "osrs-how-to-complete-lost-city-guide.html",
    ],
    "osrs-how-to-complete-lost-city-guide.html": [
        "osrs-how-to-unlock-fairy-rings-quick-guide.html",
        "osrs-desert-treasure-quest-guide-for-low-level.html",
        "osrs-how-to-finish-dragon-slayer-2-guide.html",
    ],
    "osrs-how-to-unlock-fairy-rings-quick-guide.html": [
        "osrs-how-to-complete-lost-city-guide.html",
        "osrs-how-to-get-to-fossil-island-quick-guide.html",
        "osrs-how-to-increase-slayer-points-fast.html",
    ],
    "osrs-desert-treasure-quest-guide-for-low-level.html": [
        "osrs-how-to-finish-dragon-slayer-2-guide.html",
        "osrs-how-to-complete-monkey-madness-quest.html",
        "osrs-how-to-unlock-the-abyss-guide.html",
    ],
    "osrs-how-to-get-graceful-outfit-full-guide.html": [
        "osrs-how-to-get-99-agility-fast-2026.html",
        "osrs-fastest-99-agility-guide-2026.html",
        "osrs-how-to-increase-slayer-points-fast.html",
    ],
    "osrs-how-to-complete-monkey-madness-quest.html": [
        "osrs-how-to-finish-dragon-slayer-2-guide.html",
        "osrs-desert-treasure-quest-guide-for-low-level.html",
        "osrs-how-to-get-rune-pouch-guide.html",
    ],
    "osrs-how-to-get-rune-pouch-guide.html": [
        "osrs-how-to-unlock-the-abyss-guide.html",
        "osrs-cheapest-99-runecrafting-2026.html",
        "osrs-how-to-complete-monkey-madness-quest.html",
    ],
    "osrs-how-to-finish-dragon-slayer-2-guide.html": [
        "osrs-how-to-complete-monkey-madness-quest.html",
        "osrs-desert-treasure-quest-guide-for-low-level.html",
        "osrs-how-to-get-dragon-defender-2026.html",
    ],
    "osrs-how-to-unlock-the-abyss-guide.html": [
        "osrs-how-to-get-rune-pouch-guide.html",
        "osrs-cheapest-99-runecrafting-2026.html",
        "osrs-desert-treasure-quest-guide-for-low-level.html",
    ],
    "osrs-how-to-complete-fremennik-trials-guide.html": [
        "osrs-how-to-get-to-kourend-castle-quick-guide.html",
        "osrs-how-to-unlock-fairy-rings-quick-guide.html",
    ],
    # Boss攻略类
    "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html": [
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-how-to-make-money-with-zulrah.html",
        "osrs-how-to-fight-corporeal-beast-loot-guide.html",
    ],
    "osrs-low-gear-setup-for-vorkath-guide.html": [
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
        "osrs-how-to-fight-corporeal-beast-loot-guide.html",
        "osrs-how-to-get-to-thermonuclear-smoke-devil.html",
    ],
    "osrs-how-to-solo-god-wars-boss-for-beginners.html": [
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-grotesque-guardians-guide-for-low-stats.html",
        "osrs-how-to-fight-corporeal-beast-loot-guide.html",
    ],
    "osrs-how-to-fight-corporeal-beast-loot-guide.html": [
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
        "osrs-chambers-of-xeric-loot-profit-guide.html",
        "osrs-sarachnis-loot-guide-for-ironman.html",
    ],
    "osrs-how-to-get-to-thermonuclear-smoke-devil.html": [
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-grotesque-guardians-guide-for-low-stats.html",
        "osrs-how-to-get-to-alchemical-hydra-guide.html",
    ],
    "osrs-grotesque-guardians-guide-for-low-stats.html": [
        "osrs-how-to-solo-god-wars-boss-for-beginners.html",
        "osrs-how-to-get-to-thermonuclear-smoke-devil.html",
        "osrs-how-to-fight-corporeal-beast-loot-guide.html",
    ],
    "osrs-how-to-get-to-alchemical-hydra-guide.html": [
        "osrs-how-to-get-to-thermonuclear-smoke-devil.html",
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
        "osrs-sarachnis-loot-guide-for-ironman.html",
    ],
    "osrs-sarachnis-loot-guide-for-ironman.html": [
        "osrs-chambers-of-xeric-loot-profit-guide.html",
        "osrs-how-to-fight-corporeal-beast-loot-guide.html",
        "osrs-how-to-make-money-with-zulrah.html",
    ],
    # 杂项场景类
    "osrs-how-to-get-to-fossil-island-quick-guide.html": [
        "osrs-how-to-unlock-dinosaur-hunting-osrs.html",
        "osrs-1-99-woodcutting-guide-early-game.html",
        "osrs-how-to-get-to-kourend-castle-quick-guide.html",
    ],
    "osrs-how-to-increase-slayer-points-fast.html": [
        "osrs-how-to-get-graceful-outfit-full-guide.html",
        "osrs-how-to-unlock-fairy-rings-quick-guide.html",
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
    ],
    "osrs-how-to-get-house-teleport-tablet.html": [
        "osrs-how-to-get-to-kourend-castle-quick-guide.html",
        "osrs-how-to-unlock-fairy-rings-quick-guide.html",
    ],
    "osrs-how-to-get-to-kourend-castle-quick-guide.html": [
        "osrs-how-to-get-to-fossil-island-quick-guide.html",
        "osrs-how-to-complete-fremennik-trials-guide.html",
        "osrs-how-to-get-house-teleport-tablet.html",
    ],
    "osrs-how-to-reclaim-twisted-bow-when-lost.html": [
        "osrs-how-to-beat-zulrah-for-beginners-rotation-guide.html",
        "osrs-low-gear-setup-for-vorkath-guide.html",
        "osrs-sarachnis-loot-guide-for-ironman.html",
    ],
}


def get_article_title(filepath):
    """从HTML文件中提取标题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # 尝试从 <title> 标签提取
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1)
                # 清理标题
                title = re.sub(r'OSRS\s*', '', title)
                title = re.sub(r'\s*2026\s*', '', title)
                title = title.strip()
                return title
    except:
        pass
    return filepath.stem.replace('-', ' ').title()


def add_internal_links_to_file(filepath, related_files):
    """给单个HTML文件添加内链"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有内链部分
        if 'class="related-guides"' in content or 'class="internal-links"' in content:
            print(f"  ⏭️  已存在内链: {filepath.name}")
            return False
        
        # 构建内链HTML
        links_html = '\n        <div class="related-guides">\n            <h3><i class="fas fa-link"></i> Related Guides</h3>\n            <ul>\n'
        
        for related_file in related_files[:5]:  # 最多5个
            related_path = GUIDES_DIR / related_file
            if related_path.exists():
                title = get_article_title(related_path)
                links_html += f'                <li><a href="{related_file}">{title}</a></li>\n'
            else:
                print(f"  ⚠️  文件不存在: {related_file}")
        
        links_html += '            </ul>\n        </div>\n'
        
        # 在 </article> 或 </body> 前插入内链
        insert_pos = content.rfind('</article>')
        if insert_pos == -1:
            # 如果没有 </article>，尝试在 </body> 前插入
            insert_pos = content.rfind('</body>')
        if insert_pos == -1:
            print(f"  ❌ 找不到 </article> 或 </body>: {filepath.name}")
            return False
        
        new_content = content[:insert_pos] + links_html + content[insert_pos:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ 已添加内链: {filepath.name}")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误: {filepath.name} - {e}")
        return False


def add_internal_links_css():
    """给CSS文件添加内链样式"""
    css_file = BASE_DIR / "css" / "style.css"
    
    if not css_file.exists():
        print(f"⚠️  CSS文件不存在: {css_file}")
        return
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 检查是否已有样式
    if 'related-guides' in css_content:
        print("⏭️  CSS样式已存在")
        return
    
    # 添加样式
    css_append = """
/* Related Guides / Internal Links */
.related-guides {
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    margin: 30px 0;
}

.related-guides h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.2em;
}

.related-guides ul {
    list-style: none;
    padding: 0;
}

.related-guides li {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}

.related-guides li:last-child {
    border-bottom: none;
}

.related-guides a {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.related-guides a:hover {
    color: #2980b9;
    text-decoration: underline;
}

.related-guides i {
    margin-right: 8px;
    color: #3498db;
}
"""
    
    with open(css_file, 'a', encoding='utf-8') as f:
        f.write(css_append)
    
    print("✅ 已添加CSS样式")


def main():
    print("=" * 60)
    print("OSRS 攻略站内链批量添加工具")
    print("=" * 60)
    print()
    
    # 添加CSS样式
    print("📋 步骤1: 添加CSS样式")
    add_internal_links_css()
    print()
    
    # 批量处理文件
    print("📋 步骤2: 批量添加内链")
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for filename, related_files in INTERNAL_LINKS.items():
        filepath = GUIDES_DIR / filename
        
        if not filepath.exists():
            print(f"  ⚠️  文件不存在: {filename}")
            error_count += 1
            continue
        
        result = add_internal_links_to_file(filepath, related_files)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print()
    print("=" * 60)
    print("✅ 完成！统计:")
    print(f"   成功添加: {success_count} 篇")
    print(f"   跳过(已存在): {skip_count} 篇")
    print(f"   错误/缺失: {error_count} 篇")
    print("=" * 60)
    print()
    print("📌 下一步:")
    print("   1. 检查 guides/*.html 文件确认内链已添加")
    print("   2. 提交到 git: git add . && git commit -m 'Add internal links for SEO'")
    print("   3. 推送到GitHub: git push")


if __name__ == "__main__":
    main()
