#!/usr/bin/env python3
"""
OSRS Guru - Batch fix image width/height attributes (fix CLS issue)
Usage: python fix_img.py
"""

import os
import re
import glob

GUIDES_DIR = "C:/Users/Lenovo/osrs-guide-site/guides"

def fix_img_dimensions(content):
    """Add width/height to <img> tags if missing"""
    img_pattern = r'<img([^>]+?)>'
    
    def replace_img(match):
        img_tag = match.group(1)
        
        has_width = 'width=' in img_tag
        has_height = 'height=' in img_tag
        
        if has_width and has_height:
            return f'<img{img_tag}>'
        
        if not has_width:
            img_tag = ' width="500"' + img_tag
        
        if not has_height:
            if 'width="500"' in img_tag:
                img_tag = img_tag.replace(' width="500"', ' width="500" height="300"', 1)
            else:
                img_tag = img_tag + ' height="300"'
        
        return f'<img{img_tag}>'
    
    fixed_content = re.sub(img_pattern, replace_img, content)
    return fixed_content

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        fixed = fix_img_dimensions(original)
        
        if fixed != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            return True
        return False
    except Exception as e:
        print(f"ERROR: {filepath} - {str(e)}")
        return None

def main():
    print("Starting batch fix for image width/height...")
    print(f"Directory: {GUIDES_DIR}\n")
    
    html_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    print(f"Found {len(html_files)} HTML files\n")
    
    fixed = 0
    for filepath in html_files:
        result = process_file(filepath)
        if result:
            print(f"FIXED: {os.path.basename(filepath)}")
            fixed += 1
    
    print(f"\n{'='*50}")
    print(f"Done! Fixed {fixed} files")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
