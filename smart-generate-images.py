#!/usr/bin/env python3
"""
智能生成所有被 HTML 引用的图片
扫描所有 HTML 文件，找出所有 <img src="..."> 引用，然后生成对应的图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import re
import glob

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
    # print(f"✅ 已创建: {filename}")

def find_all_image_refs():
    """找出所有 HTML 文件中引用的图片"""
    image_refs = set()
    
    # 1. 扫描根目录的 HTML 文件
    for html_file in glob.glob("*.html"):
        find_images_in_file(html_file, image_refs)
    
    # 2. 扫描 guides/ 目录中的 HTML 文件
    for html_file in glob.glob("guides/*.html"):
        find_images_in_file(html_file, image_refs)
    
    return image_refs

def find_images_in_file(html_file, image_refs):
    """在单个 HTML 文件中查找图片引用"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找所有 <img src="..."> 引用
        imgs = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', content)
        
        for img_src in imgs:
            # 转换为绝对路径
            if img_src.startswith('../'):
                # 相对路径：../images/xxx.jpg → images/xxx.jpg
                abs_path = img_src.replace('../', '')
            elif img_src.startswith('images/'):
                # 绝对路径：images/xxx.jpg
                abs_path = img_src
            elif img_src.startswith('guides/images/'):
                # guides/ 目录
                abs_path = img_src
            else:
                # 其他情况，跳过
                continue
            
            image_refs.add(abs_path)
            
    except Exception as e:
        print(f"❌ 错误: {html_file} - {e}")

def generate_all_images(image_refs):
    """生成所有引用的图片"""
    print(f"📂 需要生成 {len(image_refs)} 张图片\n")
    
    generated = 0
    skipped = 0
    
    for img_path in image_refs:
        # 转换为绝对路径
        abs_path = os.path.join("C:/Users/Lenovo/osrs-guide-site", img_path)
        
        # 检查文件是否已存在
        if os.path.exists(abs_path):
            # print(f"⏭️  跳过 (已存在): {img_path}")
            skipped += 1
            continue
        
        # 确保目录存在
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        # 根据文件名 determining 尺寸
        if 'hero' in img_path.lower():
            size = (1200, 400)
        elif 'logo' in img_path.lower():
            size = (200, 60)
        elif img_path.endswith('.jpg'):
            size = (800, 400)
        elif img_path.endswith('.png'):
            size = (64, 64)
        else:
            size = (800, 400)
        
        # 提取显示文字（从文件名）
        display_text = os.path.basename(img_path).replace('.jpg', '').replace('.png', '').replace('-', ' ')[:30]
        
        # 生成图片
        create_placeholder_image(*size, display_text, abs_path)
        print(f"✅ 已生成: {img_path}")
        generated += 1
    
    print(f"\n📊 生成完成: {generated} 张新图片, {skipped} 张已存在")

def main():
    print("=== 智能生成所有被引用的图片 ===\n")
    
    # 1. 找出所有图片引用
    print("📂 扫描所有 HTML 文件，查找图片引用...")
    image_refs = find_all_image_refs()
    
    # 2. 生成所有图片
    generate_all_images(image_refs)
    
    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
