#!/usr/bin/env python3
"""
OSRS攻略批量生成脚本 - 方案C
读取关键词清单，调用WorkBuddy API批量生成高质量攻略HTML文件
"""

import os
import json
import time
from pathlib import Path

# ========== 配置区域 ==========
WORKBUDDY_API_KEY = "YOUR_WORKBUDDY_API_KEY_HERE"  # 替换为你的WorkBuddy API Key
WORKBUDDY_API_URL = "https://api.workbuddy.cn/v1/chat/completions"  # WorkBuddy API地址
OUTPUT_DIR = Path("C:/Users/Lenovo/osrs-guide-site/guides")
CSS_PATH = "../css/style.css"  # 相对路径

# 50个关键词清单（按你的原计划）
KEYWORDS = [
    # 💰 赚钱攻略类（15个）
    "OSRS ironman money making f2p 2026",
    "OSRS low effort money making for beginners",
    "OSRS how to make gold with fishing 2026",
    "OSRS f2p money making no stats required",
    "OSRS passive money making while offline",
    "OSRS how to flip items for profit mid game",
    "OSRS cheap flipping methods for new players",
    "OSRS hunter money making guide 2026",
    "OSRS how to make money with crafting low level",
    "OSRS wintertodt money making per hour",
    "OSRS Chambers of Xeric loot profit guide",
    "OSRS f2p ironman money making early game",
    "OSRS how to rune spinning profit 2026",
    "OSRS killing green dragons money per hour",
    "OSRS how to make money with Zulrah",
    
    # 🎯 技能训练类（12个）
    "OSRS fastest 99 cooking guide f2p",
    "OSRS 1-99 thieving guide for ironman",
    "OSRS cheapest 99 runecrafting 2026",
    "OSRS how to get 99 fishing afk method",
    "OSRS 1-99 woodcutting guide early game",
    "OSRS fastest 99 attack strength defence",
    "OSRS how to train prayer cheap f2p",
    "OSRS 1-99 hunter guide afk method",
    "OSRS ironman 1-99 smithing guide",
    "OSRS how to unlock dinosaur hunting osrs",
    "OSRS how to get 99 agility fast 2026",
    "OSRS low cost 1-99 herblore guide",
    
    # 🧩 任务剧情类（10个）
    "OSRS how to get dragon defender 2026",
    "OSRS how to complete lost city guide",
    "OSRS how to unlock fairy rings quick guide",
    "OSRS desert treasure quest guide for low level",
    "OSRS how to get graceful outfit full guide",
    "OSRS how to complete monkey madness quest",
    "OSRS how to get rune pouch guide",
    "OSRS how to finish dragon slayer 2 guide",
    "OSRS how to unlock the abyss guide",
    "OSRS how to complete fremennik trials guide",
    
    # 👹 Boss攻略类（8个）
    "OSRS how to beat Zulrah for beginners rotation guide",
    "OSRS low gear setup for Vorkath guide",
    "OSRS how to solo god wars boss for beginners",
    "OSRS how to fight Corporeal Beast loot guide",
    "OSRS how to get to Thermonuclear Smoke devil",
    "OSRS Grotesque Guardians guide for low stats",
    "OSRS how to get to Alchemical Hydra guide",
    "OSRS Sarachnis loot guide for ironman",
    
    # 🎖️ 场景杂项（5个）
    "OSRS how to get to Fossil Island quick guide",
    "OSRS how to increase slayer points fast",
    "OSRS how to get house teleport tablet",
    "OSRS how to get to Kourend Castle quick guide",
    "OSRS how to reclaim twisted bow when lost",
]

# ========== 生成模板 ==========
PROMPT_TEMPLATE = """Please generate a complete independent strategy page for the keyword: {keyword}, follow all requirements below:

1. **Content length**: 1200-1800 words, structure with clear H2 and H3 headings, adapt to American readers' reading habits
2. **Update all content to 2026 latest Old School RuneScape game mechanics**, mark any updated changes compared to old versions
3. **Add practical step-by-step instructions**, include specific level requirements, item costs, profit per hour data (if it's money making/skill guide), practical tips for beginners
4. **Automatically write SEO friendly title, meta description and keywords** for this page, include the target keyword at the beginning
5. **Output complete standalone HTML code** that can be directly added to my existing OSRS strategy website, keep the same navigation bar and footer style as the existing site
6. **Include related guides section** with 3-5 internal links to other guides (use placeholder links like "related-guide-1.html")
7. **Add FAQ section** with 3-5 common questions and answers
8. **Use proper CSS classes**: method-box, profit-table, tip, note, guide-meta, guide-intro (same as existing site style)
9. **Filename suggestion**: {filename}

Output ONLY the complete HTML code, starting with <!DOCTYPE html> and ending with </html>. No extra explanation."""


def generate_filename(keyword: str) -> str:
    """根据关键词生成文件名"""
    # 移除特殊字符，替换为连字符
    filename = keyword.lower()
    filename = filename.replace("OSRS ".lower(), "")
    filename = filename.replace(" ", "-")
    filename = "".join(c for c in filename if c.isalnum() or c == "-")
    return f"osrs-{filename}.html"


def call_workbuddy_api(keyword: str, filename: str) -> str:
    """调用WorkBuddy API生成攻略内容"""
    import requests
    
    prompt = PROMPT_TEMPLATE.format(keyword=keyword, filename=filename)
    
    headers = {
        "Authorization": f"Bearer {WORKBUDDY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "workbuddy-default",  # 或你喜欢的模型
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        response = requests.post(WORKBUDDY_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        html_content = result["choices"][0]["message"]["content"]
        return html_content
    except Exception as e:
        print(f"  ❌ API调用失败: {e}")
        return None


def save_html_file(filename: str, content: str) -> bool:
    """保存HTML文件"""
    try:
        file_path = OUTPUT_DIR / filename
        file_path.write_text(content, encoding="utf-8")
        print(f"  ✅ 已保存: {filename}")
        return True
    except Exception as e:
        print(f"  ❌ 保存失败 {filename}: {e}")
        return False


def main():
    print("🚀 OSRS攻略批量生成脚本启动...")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📊 待生成: {len(KEYWORDS)} 篇攻略\n")
    
    # 检查API Key
    if WORKBUDDY_API_KEY == "YOUR_WORKBUDDY_API_KEY_HERE":
        print("⚠️  请先配置WORKBUDDY_API_KEY！")
        print("   1. 打开脚本，找到 WORKBUDDY_API_KEY 变量")
        print("   2. 替换为你自己的WorkBuddy API Key")
        print("   3. 重新运行脚本")
        return
    
    success_count = 0
    fail_count = 0
    
    for i, keyword in enumerate(KEYWORDS, 1):
        filename = generate_filename(keyword)
        print(f"\n[{i}/{len(KEYWORDS)}] 生成中: {keyword}")
        print(f"  📝 文件名: {filename}")
        
        # 调用API
        html_content = call_workbuddy_api(keyword, filename)
        
        if html_content:
            # 保存文件
            if save_html_file(filename, html_content):
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1
        
        # 避免API频率限制
        if i < len(KEYWORDS):
            print(f"  ⏳ 等待5秒...")
            time.sleep(5)
    
    print(f"\n✅ 批量生成完成！")
    print(f"   成功: {success_count} 篇")
    print(f"   失败: {fail_count} 篇")
    print(f"   成功率: {success_count/len(KEYWORDS)*100:.1f}%")
    
    print(f"\n📋 下一步:")
    print(f"   1. 检查生成的HTML文件")
    print(f"   2. 运行更新脚本更新sitemap.xml")
    print(f"   3. 部署到GitHub Pages")


if __name__ == "__main__":
    main()