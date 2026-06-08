"""
给根目录 HTML 文件添加 AI 问答浮窗脚本
这些文件用 js/features.js（不是 ../js/features.js）
"""
from pathlib import Path

ROOT = Path(__file__).parent
ROOT_FILES = ["about.html", "boss-guides.html", "ga4_dashboard.html", 
              "money-making.html", "privacy-policy.html", "quest-guides.html", 
              "skill-training.html"]

SEARCH = '<script src="js/features.js"></script>'
INSERT = '<script src="js/ai-qa-widget.js"></script>'

added, skipped, errors = 0, 0, 0

for fn in ROOT_FILES:
    fp = ROOT / fn
    if not fp.exists():
        print(f"  MISSING: {fn}")
        errors += 1
        continue
    
    content = fp.read_text(encoding="utf-8")
    
    if 'ai-qa-widget.js' in content:
        print(f"  SKIP (already added): {fn}")
        skipped += 1
        continue
    
    if SEARCH in content:
        new_content = content.replace(SEARCH, f"{SEARCH}\n{INSERT}")
        fp.write_text(new_content, encoding="utf-8")
        print(f"  OK: {fn}")
        added += 1
    else:
        print(f"  WARN (no features.js): {fn}")
        errors += 1

print(f"\n=== Summary ===")
print(f"Added: {added} | Skipped: {skipped} | Errors: {errors}")
