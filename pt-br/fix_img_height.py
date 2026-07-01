import os
import glob
import re

total_fixes = 0
files_modified = 0

for filepath in glob.glob('guides/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Find all <img ...> tags
    def fix_img_tag(match):
        global total_fixes
        tag = match.group(0)
        if 'width="500"' in tag and 'height=' not in tag:
            tag = tag.replace('width="500"', 'width="500" height="300"', 1)
            total_fixes += 1
        return tag

    content = re.sub(r'<img\s+[^>]*>', fix_img_tag, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_modified += 1

print(f"Img height fixes: {total_fixes}")
print(f"Files modified: {files_modified}")
