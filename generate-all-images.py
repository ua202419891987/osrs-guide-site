#!/usr/bin/env python3
"""
生成所有缺失的图片 for OSRS 攻略网站
创建一个映射表：HTML 中引用的图片 → 实际生成的图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import re

def create_placeholder_image(width, height, text, filename, bg_color=(45, 52, 64), text_color=(255, 215, 0)):
    """创建一个简单的占位图片"""
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
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

def generate_all_missing_images():
    """生成所有缺失的图片"""
    base_dir = "C:/Users/Lenovo/osrs-guide-site"
    
    # 图片尺寸
    hero_size = (1200, 400)
    thumbnail_size = (800, 400)
    icon_size = (64, 64)
    
    # 1. 根目录图片 (images/)
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    create_placeholder_image(*hero_size, "OSRS Guide Hero", os.path.join(images_dir, "hero-bg.jpg"))
    create_placeholder_image(200, 60, "OSRS Guide", os.path.join(images_dir, "logo.png"))
    
    # 分类图标
    icons = {
        "money.png": "💰",
        "skill.png": "⚔️",
        "quest.png": "📜",
        "boss.png": "🐉"
    }
    
    for icon_file, emoji in icons.items():
        create_placeholder_image(*icon_size, emoji, os.path.join(images_dir, icon_file))
    
    # 2. guides/ 目录中的图片 (guides/images/)
    guides_images_dir = os.path.join(base_dir, "guides", "images")
    os.makedirs(guides_images_dir, exist_ok=True)
    
    # 生成所有攻略文章的特色图片
    guides_dir = os.path.join(base_dir, "guides")
    if os.path.exists(guides_dir):
        for filename in os.listdir(guides_dir):
            if filename.endswith(".html") and filename != "TEMPLATE.html":
                # 提取攻略名称
                guide_name = filename.replace("osrs-", "").replace(".html", "").replace("-", " ").title()
                img_filename = filename.replace('.html', '.jpg')
                img_path = os.path.join(guides_images_dir, img_filename)
                
                # 只生成前 30 个字符（避免文字过长）
                display_text = guide_name[:30]
                create_placeholder_image(*thumbnail_size, display_text, img_path)
    
    print("\n✅ 所有图片已生成！")

def main():
    print("=== 生成所有缺失的图片 ===\n")
    generate_all_missing_images()
    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
