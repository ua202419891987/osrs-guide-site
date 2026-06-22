import os
import re

guides_dir = "C:/Users/Lenovo/osrs-guide-site/guides"

all_html = sorted([f for f in os.listdir(guides_dir) if f.endswith(".html")])

fixed_files = []
change_details = []

for filename in all_html:
    filepath = os.path.join(guides_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "<img" not in content:
        continue
    
    modified = False
    new_content = content
    file_changes = []
    
    img_pattern = re.compile(r'<img\b([^>]*?)>', re.DOTALL)
    
    for m in img_pattern.finditer(content):
        img_attrs = m.group(1)
        
        has_width = re.search(r'\bwidth\s*=\s*["\']', img_attrs)
        has_height = re.search(r'\bheight\s*=\s*["\']', img_attrs)
        
        if has_width and has_height:
            continue
        
        add_parts = []
        if not has_width:
            add_parts.append('width="500"')
        if not has_height:
            add_parts.append('height="300"')
        
        original_tag = m.group(0)
        inserted = " ".join(add_parts)
        
        if original_tag.strip().endswith("/>"):
            new_tag = original_tag.replace("/>", f' {inserted} />', 1)
        else:
            new_tag = original_tag.replace(">", f' {inserted}>', 1)
        
        new_content = new_content.replace(original_tag, new_tag, 1)
        modified = True
        file_changes.append((original_tag, new_tag))
    
    if modified:
        fixed_files.append(filename)
        change_details.append((filename, file_changes))
        print(f"[FIX] {filename} ({len(file_changes)} changes)")
        for orig, new in file_changes[:2]:
            print(f"  OLD: {orig[:120]}")
            print(f"  NEW: {new[:120]}")
            print()
    
    # 只处理前5个文件做测试
    if len(fixed_files) >= 5:
        break

print(f"\nTotal: {len(fixed_files)} files to fix")
