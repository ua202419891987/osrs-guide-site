"""
build_chunks.py — 重建 OSRS Guru AI 助手知识库 (chunks.json)
扫描全站 HTML，按文章切片，排除红线5篇付费文，输出 chunks.json。
输出默认到 D 盘暂存（沙箱禁止写仓库 data/），由用户 copy 回 data/ 后部署。

用法:
    python scripts/build_chunks.py            # 生成到 D:\网站下载文件专栏\osrs-index\chunks.json
    python scripts/build_chunks.py --out X    # 指定输出路径
"""
import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Lenovo/osrs-guide-site")
STAGE = Path(r"D:/网站下载文件专栏/osrs-index")
STAGE.mkdir(parents=True, exist_ok=True)
DEFAULT_OUT = STAGE / "chunks.json"

# 扫描范围（含子目录递归）
SCAN_GLOBS = [
    "guides/**/*.html",   # 英文主站 + crimson-desert/ + windrose/ 子目录
    "zh/**/*.html",
    "pt-br/**/*.html",
    "levels/**/*.html",
    "blog/**/*.html",
    "*.html",             # 根目录枢纽页
]
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".workbuddy"}

# 红线5篇付费文（任何语言版本都排除，未公开不能进AI泄露）
RED_LINE_STEMS = [
    "osrs-how-to-make-money-with-zulrah",
    "osrs-wilderness-bosses-guide-2026",
    "osrs-gauntlet-meta-changes-2026",
    "osrs-hunter-money-making-guide-2026",
    "osrs-slayer-70-to-95-money-makers-2026",
]

CHUNK_WORDS = 600
OVERLAP_WORDS = 100


def is_redline(rel: str) -> bool:
    stem = Path(rel).stem.lower()
    return any(rl in stem for rl in RED_LINE_STEMS)


def collect_html() -> list[Path]:
    out = []
    for pat in SCAN_GLOBS:
        for fp in ROOT.glob(pat):
            if not fp.is_file():
                continue
            parts = set(fp.relative_to(ROOT).parts)
            if parts & EXCLUDE_DIRS:
                continue
            if is_redline(str(fp.relative_to(ROOT))):
                continue
            out.append(fp)
    # 去重并稳定排序
    seen = set()
    uniq = []
    for fp in sorted(out):
        if fp not in seen:
            seen.add(fp)
            uniq.append(fp)
    return uniq


def extract(fp: Path) -> tuple[str, str]:
    html = fp.read_text(encoding="utf-8", errors="ignore")
    # title
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    title = re.sub(r"\s+", " ", m.group(1)).strip() if m else fp.stem
    # 去掉 script/style
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-zA-Z#0-9]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return title, text


def make_url(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if rel.lower() == "index.html":
        return "https://osrsguru.com/"
    return "https://osrsguru.com/" + rel


def chunk_text(text: str, title: str, url: str) -> list[dict]:
    words = text.split()
    if not words:
        return []
    if len(words) <= CHUNK_WORDS:
        return [{"title": title, "url": url, "text": text}]
    step = CHUNK_WORDS - OVERLAP_WORDS
    res = []
    i = 0
    n = 1
    while i < len(words):
        seg = words[i:i + CHUNK_WORDS]
        t = " ".join(seg)
        suffix = f" (part {n})" if len(words) > CHUNK_WORDS else ""
        res.append({"title": title + suffix, "url": url, "text": t})
        i += step
        n += 1
        if i + CHUNK_WORDS >= len(words):
            # 最后一段
            last = words[i:]
            if last:
                res.append({"title": title + f" (part {n})", "url": url, "text": " ".join(last)})
            break
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    out_path = Path(args.out)

    files = collect_html()
    print(f"[1] 扫描到 {len(files)} 个 HTML 页面（已排除红线5篇/CD/WR目录）")
    chunks = []
    for fp in files:
        rel = str(fp.relative_to(ROOT))
        try:
            title, text = extract(fp)
        except Exception as e:
            print(f"  跳过 {rel}: {e}")
            continue
        if not text:
            continue
        chunks.extend(chunk_text(text, title, make_url(rel)))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)
    size_mb = out_path.stat().st_size / 1_048_576
    print(f"[2] 生成 {len(chunks)} 个 chunk -> {out_path} ({size_mb:.2f} MiB)")
    print("[3] 用户本地执行: copy /Y D:\\网站下载文件专栏\\osrs-index\\chunks.json C:\\Users\\Lenovo\\osrs-guide-site\\data\\chunks.json")


if __name__ == "__main__":
    main()
