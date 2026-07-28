"""
noindex_zh_pt.py — 给 ZH/PT-BR 全站临时加 noindex（方便重投 AdSense 时只让英文高质量站被评估）
用法:
  python scripts/noindex_zh_pt.py            # 加 noindex
  python scripts/noindex_zh_pt.py --revert   # 撤回 noindex
排除: 红线5篇(任何语言)、临时辅助文件(_frag*.html/_enrich.py/__enrich.py)、.git 等
"""
import argparse
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Lenovo/osrs-guide-site")
TARGETS = ["zh/**/*.html", "pt-br/**/*.html"]
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".workbuddy"}
REDLINE = ["osrs-how-to-make-money-with-zulrah", "osrs-wilderness-bosses-guide-2026",
           "osrs-gauntlet-meta-changes-2026", "osrs-hunter-money-making-guide-2026",
           "osrs-slayer-70-to-95-money-makers-2026"]
STRAY = ("_frag", "_enrich", "__enrich", "css_override_complete", "googlef2d4bacd14fcdb05")

META = '    <meta name="robots" content="noindex,follow">\n'


def is_excluded(rel: str) -> bool:
    if any(r in rel.lower() for r in REDLINE):
        return True
    name = rel.split("/")[-1]
    if name.startswith(STRAY):
        return True
    return False


def collect():
    out = []
    for pat in TARGETS:
        for fp in ROOT.glob(pat):
            if not fp.is_file():
                continue
            if set(fp.relative_to(ROOT).parts) & EXCLUDE_DIRS:
                continue
            rel = str(fp.relative_to(ROOT)).replace("\\", "/")
            if is_excluded(rel):
                continue
            out.append(fp)
    return sorted(set(out))


def add(fp):
    html = fp.read_text(encoding="utf-8")
    if 'name="robots"' in html:
        # 已有 robots meta：直接替换为 noindex,follow（覆盖 index,follow，绝不跳过）
        new, n = re.subn(r'<meta\b[^>]*name=["\']robots["\'][^>]*>',
                         META.strip(), html, flags=re.I)
        if n:
            fp.write_text(new, encoding="utf-8")
            return True
        return False
    # 没有 robots meta：插在 <head> 之后第一行
    new, n = re.subn(r'(<head[^>]*>)', lambda m: m.group(1) + "\n" + META, html, count=1, flags=re.I)
    if n == 0:
        # 没有 <head> 就不处理
        return False
    fp.write_text(new, encoding="utf-8")
    return True


def revert(fp):
    html = fp.read_text(encoding="utf-8")
    new, n = re.subn(r'\s*<meta name="robots" content="noindex,follow">\n?', "", html, flags=re.I)
    if n:
        fp.write_text(new, encoding="utf-8")
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revert", action="store_true")
    args = ap.parse_args()
    files = collect()
    changed = 0
    for fp in files:
        ok = revert(fp) if args.revert else add(fp)
        if ok:
            changed += 1
    verb = "撤回" if args.revert else "加 noindex"
    print(f"[{verb}] 处理 {len(files)} 个文件，实际变更 {changed} 个")


if __name__ == "__main__":
    main()
