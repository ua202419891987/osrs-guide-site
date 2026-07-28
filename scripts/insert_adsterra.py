"""
insert_adsterra.py — 在英文站文章顶部+文中插入 Adsterra 广告位占位（占位框，用户拿到 Adsterra 代码后替换 inner 文本即可）
范围: guides/*.html(顶层,不含crimson-desert/windrose), levels/**, *.html(根), blog/**
排除: 红线5篇, CD/WR 子目录, 谷歌验证文件, css_override_complete, 已含标记的页
用法: python scripts/insert_adsterra.py
"""
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Lenovo/osrs-guide-site")
# 只插英文文章内容页（guides 顶层 / levels / blog），不碰根目录导航/法律页（index/about/privacy 等）
TARGETS = ["guides/*.html", "levels/**/*.html", "blog/**/*.html"]
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".workbuddy", "crimson-desert", "windrose"}
REDLINE = ["osrs-how-to-make-money-with-zulrah", "osrs-wilderness-bosses-guide-2026",
           "osrs-gauntlet-meta-changes-2026", "osrs-hunter-money-making-guide-2026",
           "osrs-slayer-70-to-95-money-makers-2026"]
SKIP = {"googlef2d4bacd14fcdb05.html", "css_override_complete.html"}

AD_BOX = ('<div class="ad-banner" style="text-align:center;margin:22px auto;padding:10px;'
          'border:1px dashed #d4af37;border-radius:8px;max-width:728px;min-height:90px;'
          'color:#d4af37;font-size:12px;box-sizing:border-box;">'
          'Adsterra ad slot — paste your Adsterra banner code here</div>')
TOP = "<!--ADSTERRA_TOP-->\n" + AD_BOX + "\n"
MID = "<!--ADSTERRA_MID-->\n" + AD_BOX + "\n"


def is_excluded(rel: str) -> bool:
    if any(r in rel.lower() for r in REDLINE):
        return True
    name = rel.split("/")[-1]
    if name in SKIP:
        return True
    if name.startswith("_") or name.startswith("__"):  # 临时辅助文件残留
        return True
    if name.endswith(".backup"):
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


def process(fp):
    html = fp.read_text(encoding="utf-8")
    if "ADSTERRA_TOP" in html:
        return False
    # TOP: 文章正文开头
    if '<div class="guide-content">' in html:
        html = html.replace('<div class="guide-content">', '<div class="guide-content">\n' + TOP, 1)
    elif "</header>" in html:
        html = html.replace("</header>", "</header>\n" + TOP, 1)
    else:
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + TOP, html, count=1)
    # MID: 第一个 </h2> 之后（章节之间）
    html = re.sub(r"(</h2>)", lambda m: m.group(1) + "\n" + MID, html, count=1)
    fp.write_text(html, encoding="utf-8")
    return True


def main():
    files = collect()
    done = 0
    for fp in files:
        if process(fp):
            done += 1
    print(f"[Adsterra] 处理 {len(files)} 个英文页，实际插入 {done} 个")


if __name__ == "__main__":
    main()
