#!/usr/bin/env python3
"""
自动为所有指南页面添加 AI 问答浮窗脚本
"""

from pathlib import Path
import re

GUIDES_DIR = Path("guides")
SCRIPT_TAG = '<script src="../js/ai-qa-widget.js"></script>'

def patch_guide_files():
    html_files = list(GUIDES_DIR.glob("*.html"))
    print(f"Found {len(html_files)} guide files")
    
    patched_count = 0
    skipped_count = 0
    
    for file in html_files:
        content = file.read_text(encoding='utf-8')
        
        # 检查是否已包含浮窗脚本
        if "ai-qa-widget.js" in content:
            print(f"⏭️  Already patched: {file.name}")
            skipped_count += 1
            continue
        
        # 添加浮窗脚本
        new_content = content.replace(
            '<script src="../js/features.js"></script>',
            f'<script src="../js/features.js"></script>\n{SCRIPT_TAG}'
        )
        
        file.write_text(new_content, encoding='utf-8')
        print(f"✅ Patched: {file.name}")
        patched_count += 1
    
    print(f"\n总结: {patched_count} 个文件已更新，{skipped_count} 个文件已跳过")

if __name__ == "__main__":
    patch_guide_files()
