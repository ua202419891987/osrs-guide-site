#!/usr/bin/env python3
"""
生成占位图片 for OSRS 攻略网站
创建简单的 PNG 图片作为占位符
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(width, height, text, filename, bg_color=(45, 52, 64), text_color=(255, 215, 0)):
    """创建一个简单的占位图片"""
    # 创建图片
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 尝试使用默认字体
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, fill=text_color, font=font)
    
    # 保存图片
    img.save(filename)
    print(f"✅ 已创建: {filename}")

def main():
    # 确保目录存在
    os.makedirs("images", exist_ok=True)
    os.makedirs("guides/images", exist_ok=True)
    
    # 1. 网站 Logo (首页用)
    create_placeholder_image(200, 60, "OSRS Guide", "images/logo.png")
    
    # 2. Hero 背景图 (首页用)
    create_placeholder_image(1200, 400, "OSRS Guide Hero", "images/hero-bg.jpg")
    
    # 3. 攻略文章特色图片 (guides/images/)
    # 为每篇攻略创建一个占位图片
    guides_dir = "guides"
    if os.path.exists(guides_dir):
        for filename in os.listdir(guides_dir):
            if filename.endswith(".html") and filename != "TEMPLATE.html":
                # 提取攻略名称
                guide_name = filename.replace("osrs-", "").replace(".html", "").replace("-", " ").title()
                img_filename = f"guides/images/{filename.replace('.html', '.jpg')}"
                create_placeholder_image(800, 400, guide_name[:30], img_filename)
    
    # 4. 分类图标 (emoji 图标，用图片代替)
    icons = {
        "money.png": "💰",
        "skill.png": "⚔️",
        "quest.png": "📜",
        "boss.png": "🐉"
    }
    
    for icon_file, emoji in icons.items():
        create_placeholder_image(64, 64, emoji, f"images/{icon_file}")

if __name__ == "__main__":
    main()
