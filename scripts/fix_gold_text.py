#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix gold/cream TEXT on light backgrounds in OSRS article pages.

Problem: article pages use color:#d4af37 (gold) / #e8d5b7 (cream) as text
on white/light backgrounds inside tables, tip-boxes, callouts -> unreadable.
Body <p> text itself is already dark (#1a1a1a) and fine.

Fix: change those text colors to near-black #1a1a1a.
Scope: guides/*.html, zh/guides/*.html, pt-br/guides/*.html
PROTECTED (never changed):
  - .guide-hero section (dark bronze bg, gold text is by-design)
  - .support-card block (green donation box, format must NOT change)
"""
import os
import re
import sys

ROOT = r"C:\Users\Lenovo\osrs-guide-site"

# Files to NEVER modify (Early Access paid content, embargo until 2026-08-23)
SKIP_FILES = {
    "guides/osrs-how-to-make-money-with-zulrah.html",
    "guides/osrs-wilderness-bosses-guide-2026.html",
    "guides/osrs-gauntlet-meta-changes-2026.html",
    "guides/osrs-hunter-money-making-guide-2026.html",
    "guides/osrs-slayer-70-to-95-money-makers-2026.html",
}

SCOPE_DIRS = [
    os.path.join(ROOT, "guides"),
    os.path.join(ROOT, "zh", "guides"),
    os.path.join(ROOT, "pt-br", "guides"),
]

TEXT_COLOR_FIXES = [
    ("color:#d4af37", "color:#1a1a1a"),
    ("color: #d4af37", "color: #1a1a1a"),
    ("color:#e8d5b7", "color:#1a1a1a"),
    ("color: #e8d5b7", "color: #1a1a1a"),
    ("color:#b8860b", "color:#1a1a1a"),
    ("color: #b8860b", "color: #1a1a1a"),
]

HERO_PAT = re.compile(
    r'<section\b[^>]*class="[^"]*guide-hero[^"]*"[\s\S]*?</section>', re.I)

DRY = "--dry-run" in sys.argv


def replace_gold(text):
    for old, new in TEXT_COLOR_FIXES:
        if old in text:
            text = text.replace(old, new)
    return text


def fix_file(c):
    # 1) protect support-card block (usually near end) -> keep as tail, untouched
    idx = c.rfind('class="support-card"')
    if idx == -1:
        body, tail = c, ""
    else:
        body, tail = c[:idx], c[idx:]

    # 2) protect hero section inside body
    heroes = []

    def protect(m):
        heroes.append(m.group(0))
        return "\x02%d\x02" % (len(heroes) - 1)

    body = HERO_PAT.sub(protect, body)

    # 3) replace gold text only in non-hero, non-support body
    body = replace_gold(body)

    # 4) restore hero
    for i, h in enumerate(heroes):
        body = body.replace("\x02%d\x02" % i, h)

    return body + tail


def collect_files():
    out = []
    for d in SCOPE_DIRS:
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".html"):
                out.append(os.path.join(d, fn))
    return out


def main():
    files = collect_files()
    total_files = 0
    total_repl = 0
    for p in files:
        # Skip paid Early Access articles
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if rel in SKIP_FILES:
            continue
        try:
            c = open(p, encoding="utf-8").read()
        except Exception:
            continue
        new = fix_file(c)
        cnt = len(c) - len(new)  # rough; count actual replacements below
        # accurate count
        cnt = 0
        tmp = c
        for old, _ in TEXT_COLOR_FIXES:
            cnt += tmp.count(old)
        if new != c:
            total_files += 1
            total_repl += cnt
            if not DRY:
                open(p, "w", encoding="utf-8").write(new)
    if DRY:
        print("[DRY-RUN] files that would change: %d" % total_files)
        print("[DRY-RUN] total text-color replacements: %d" % total_repl)
    else:
        print("[APPLIED] files changed: %d" % total_files)
        print("[APPLIED] total text-color replacements: %d" % total_repl)


if __name__ == "__main__":
    main()
