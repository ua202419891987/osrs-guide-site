"""
restore_after_adsense.py — AdSense 过审后一键恢复中葡站收录
功能:
  1. 把 zh/ 和 pt-br/ 所有页面的 noindex,follow 改回 index,follow (恢复收录)
  2. 把 sitemap-zh.xml / sitemap-pt.xml 加回 sitemap.xml 主索引
用法 (用户本地 CMD):
  cd /d C:/Users/Lenovo/osrs-guide-site
  python scripts/restore_after_adsense.py
  git add -A && git commit -m "restore: re-enable zh/pt indexing after AdSense approval" && git push origin main
  # 然后在 Google Search Console 重新提交 https://osrsguru.com/sitemap.xml
排除: 红线5篇(任何语言)、临时辅助文件(_frag/_enrich/__enrich)、.git 等
"""
from pathlib import Path

ROOT = Path(r"C:/Users/Lenovo/osrs-guide-site")
TARGETS = ["zh/**/*.html", "pt-br/**/*.html"]
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".workbuddy"}
REDLINE = ["osrs-how-to-make-money-with-zulrah", "osrs-wilderness-bosses-guide-2026",
           "osrs-gauntlet-meta-changes-2026", "osrs-hunter-money-making-guide-2026",
           "osrs-slayer-70-to-95-money-makers-2026"]
STRAY = ("_frag", "_enrich", "__enrich", "css_override_complete", "googlef2d4bacd14fcdb05")

NOINDEX_TAG = '<meta name="robots" content="noindex,follow">'
INDEX_TAG = '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">'

SITEMAP = ROOT / "sitemap.xml"
ZH_LOC = "https://osrsguru.com/sitemap-zh.xml"
PT_LOC = "https://osrsguru.com/sitemap-pt.xml"
ZH_BLOCK = (
    '  <sitemap>\n'
    '    <loc>https://osrsguru.com/sitemap-zh.xml</loc>\n'
    '    <lastmod>2026-07-03</lastmod>\n'
    '  </sitemap>\n'
)
PT_BLOCK = (
    '  <sitemap>\n'
    '    <loc>https://osrsguru.com/sitemap-pt.xml</loc>\n'
    '    <lastmod>2026-07-03</lastmod>\n'
    '  </sitemap>\n'
)


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


def restore_meta(fp):
    html = fp.read_text(encoding="utf-8")
    if NOINDEX_TAG not in html:
        return False
    new = html.replace(NOINDEX_TAG, INDEX_TAG)
    fp.write_text(new, encoding="utf-8")
    return True


def restore_sitemap():
    txt = SITEMAP.read_text(encoding="utf-8")
    blocks = ""
    if ZH_LOC not in txt:
        blocks += ZH_BLOCK
    if PT_LOC not in txt:
        blocks += PT_BLOCK
    if not blocks:
        return 0
    txt = txt.replace("</sitemapindex>", blocks + "</sitemapindex>")
    SITEMAP.write_text(txt, encoding="utf-8")
    return blocks.count("<sitemap>")


def main():
    files = collect()
    meta_changed = 0
    for fp in files:
        if restore_meta(fp):
            meta_changed += 1
    sm_changed = restore_sitemap()
    print(f"[restore] 恢复 index meta: {meta_changed}/{len(files)} 个中葡页面")
    print(f"[restore] 恢复 sitemap 引用: {sm_changed} 个 (zh/pt)")
    print("")
    print("下一步 (用户本地执行):")
    print('  git add -A')
    print('  git commit -m "restore: re-enable zh/pt indexing after AdSense approval"')
    print("  git push origin main")
    print("  然后在 Google Search Console 重新提交 sitemap.xml")


if __name__ == "__main__":
    main()
