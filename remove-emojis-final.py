#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用逐字符方式删除所有 Emoji（保留 ASCII 和中文等正常字符）
"""

from pathlib import Path
import unicodedata

BASE_DIR = Path("C:/Users/Lenovo/osrs-guide-site/")
GUIDES_DIR = BASE_DIR / "guides"

def is_emoji(char):
    """判断一个字符是否是 Emoji"""
    # 方法1：Unicode 类别
    cp = ord(char)
    # Emoji 常见 Unicode 范围
    if 0x1F000 <= cp <= 0x1FAFF:
        return True
    if 0x2600 <= cp <= 0x27BF:  # 杂项符号
        return True
    if 0xFE00 <= cp <= 0xFE0F:  # 变体选择器
        return True
    if 0x1F3FB <= cp <= 0x1F3FF:  # 肤色修饰符
        return True
    if 0xE0020 <= cp <= 0xE007F:  # 标签
        return True
    if 0x200D == cp:  # 零宽连接符
        return True
    # 用 unicodedata 判断
    try:
        cat = unicodedata.category(char)
        name = unicodedata.name(char, "")
        if "EMOJI" in name or "EMOTICON" in name:
            return True
    except:
        pass
    return False

def clean_emoji_from_file(filepath):
    """清除文件中的所有 Emoji 字符"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return False
    
    original_len = len(content)
    # 过滤掉 Emoji 字符
    cleaned = ''.join(c for c in content if not is_emoji(c))
    
    if len(cleaned) != original_len:
        filepath.write_text(cleaned, encoding="utf-8")
        return True
    return False

def main():
    fixed = 0
    checked = 0
    
    all_files = list(BASE_DIR.glob("*.html")) + list(GUIDES_DIR.glob("*.html"))
    
    for html_file in all_files:
        if "TEMPLATE" in html_file.name or "template" in html_file.name:
            continue
        checked += 1
        if clean_emoji_from_file(html_file):
            fixed += 1
            print(f"✅ {html_file.name}")
    
    print(f"\n检查了 {checked} 个文件，修改了 {fixed} 个")

if __name__ == "__main__":
    main()
