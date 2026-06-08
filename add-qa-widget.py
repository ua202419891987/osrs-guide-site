"""
批量添加 AI 问答浮窗脚本到所有 guide 页面
在 ../js/features.js 之后插入 ai-qa-widget.js
"""
from pathlib import Path

GUIDES_DIR = Path(__file__).parent / "guides"
SEARCH = '<script src="../js/features.js"></script>'
INSERT = '<script src="../js/ai-qa-widget.js"></script>'

files = sorted(GUIDES_DIR.glob("*.html"))
print(f"Found {len(files)} guide pages")

added, skipped, errors = 0, 0, 0

for f in files:
    try:
        content = f.read_text(encoding="utf-8")
        
        # Skip if already has ai-qa-widget
        if 'ai-qa-widget.js' in content:
            print(f"  SKIP (already added): {f.name}")
            skipped += 1
            continue
        
        # Insert after features.js
        if SEARCH in content:
            new_content = content.replace(SEARCH, f"{SEARCH}\n{INSERT}")
            f.write_text(new_content, encoding="utf-8")
            print(f"  OK: {f.name}")
            added += 1
        else:
            print(f"  WARN (no features.js found): {f.name}")
            errors += 1
    except Exception as e:
        print(f"  ERROR: {f.name} — {e}")
        errors += 1

print(f"\n=== Summary ===")
print(f"Added: {added} | Skipped: {skipped} | Errors: {errors}")
