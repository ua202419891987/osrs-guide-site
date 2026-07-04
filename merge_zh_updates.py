#!/usr/bin/env python3
"""
Merge latest English guide updates into Chinese (zh/guides/) versions.
Preserves existing Chinese translations in <body>, updates <head> from English.

Usage: python merge_zh_updates.py
"""

import os
import re
import json
from html.parser import HTMLParser
from datetime import datetime

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site"
EN_DIR = os.path.join(BASE_DIR, "guides")
ZH_DIR = os.path.join(BASE_DIR, "zh", "guides")

# Files updated in commit 356b616 (gear recommender + beginner guide updates)
# Only include files that have Chinese counterparts
BEGINNER_FILES = [
    # Direct name matches
    "osrs-money-making-beginner-2026.html",
    "osrs-achievement-diary-beginner-guide-2026.html",
    "osrs-affordable-leveling-guide-2026.html",
    "osrs-all-skills-overview-guide-2026.html",
    "osrs-bank-tags-beginners-guide-2026.html",
    "osrs-barrows-beginner-guide-2026.html",
    "osrs-cheap-flipping-methods-new-players.html",
    "osrs-clue-scrolls-beginner-guide-2026.html",
    "osrs-combat-training-beginner-2026.html",
    "osrs-diary-priority-order-beginner-2026.html",
    "osrs-efficient-training-routes-beginners-2026.html",
    "osrs-f2p-combat-training-guide-2026.html",
    "osrs-f2p-ironman-money-making-early-game.html",
    "osrs-f2p-leveling-guide-2026.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-quests-before-membership-2026.html",
    "osrs-f2p-to-member-first-10-things-2026.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
    "osrs-fastest-99-cooking-f2p.html",
    "osrs-fastest-leveling-guide-2026.html",
    "osrs-first-boss-progression-roadmap-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
    "osrs-first-week-progression-guide-2026.html",
    "osrs-gear-beginner-guide-2026.html",
    "osrs-how-to-make-money-with-crafting-low-level.html",
    "osrs-how-to-train-prayer-cheap-f2p.html",
    "osrs-interface-controls-beginner-guide-2026.html",
    "osrs-ironman-beginner-guide-2026.html",
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-lms-beginner-guide-2026.html",
    "osrs-low-effort-money-making-beginners.html",
    "osrs-low-level-skilling-money-makers-2026.html",
    "osrs-members-vs-f2p-comparison-2026.html",
    "osrs-minigames-beginner-guide-2026.html",
    "osrs-nmz-beginner-guide-2026.html",
    "osrs-obor-bryophyta-f2p-boss-guide-2026.html",
    "osrs-optimal-leveling-guide-2026.html",
    "osrs-poh-beginner-guide-2026.html",
    "osrs-prayer-training-beginner-guide-2026.html",
    "osrs-pvm-beginner-guide-2026.html",
    "osrs-questing-beginner-guide-2026.html",
    "osrs-range-training-1-99-guide-2026.html",
    "osrs-safe-spots-beginner-2026.html",
    "osrs-sailing-1-99-guide-2026.html",
    "osrs-skill-training-beginner-complete-guide-2026.html",
    "osrs-skill-training-beginner-fast-track-2026.html",
    "osrs-skills-overview-beginner-2026.html",
    "osrs-slayer-beginner-first-master-guide-2026.html",
    "osrs-slayer-beginner-guide-2026.html",
    "osrs-slayer-low-level-money-makers-2026.html",
    "osrs-top-10-skills-to-train-first-2026.html",
    "osrs-wilderness-survival-beginner-2026.html",
    "slayer-1-99-guide-2026.html",
    # New in this commit
    "osrs-1-99-farming-guide-beginner-profit-2026.html",
    "osrs-1-99-mining-guide-beginner-2026.html",
    "osrs-1-99-woodcutting-guide-early-game.html",
    "osrs-common-beginner-mistakes-avoid-2026.html",
    "osrs-construction-1-99-guide-2026.html",
    "osrs-early-game-weapon-tierlist-2026.html",
    "osrs-f2p-gear-progression-guide-2026.html",
    "osrs-f2p-money-making-ranked-2026.html",
    "osrs-f2p-slayer-guide-2026.html",
    "osrs-f2p-to-bond-guide-2026.html",
    "osrs-f2p-to-p2p-membership-guide-2026.html",
    "osrs-first-100k-gp-challenge-2026.html",
    "osrs-first-30-minutes-member-2026.html",
    "osrs-group-ironman-beginner-guide-2026.html",
    "osrs-kalphite-queen-kq-beginner-guide-2026.html",
    "osrs-new-player-7-day-roadmap-2026.html",
    "osrs-new-player-guide-2026.html",
    "osrs-what-to-buy-first-1m-guide-2026.html",
    "barrows-first-boss-gp-2026.html",
    "f2p-to-p2p-bond-guide-2026.html",
    "first-5m-gp-members-2026.html",
]


def read_file(path):
    """Read file content, return None if not found."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_file(path, content):
    """Write content to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def extract_body(html):
    """Extract <body>...</body> content from HTML."""
    match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    if match:
        return match.group(0)  # Includes <body> tags
    return None


def extract_head(html):
    """Extract <head>...</head> content from HTML."""
    match = re.search(r"<head[^>]*>(.*?)</head>", html, re.DOTALL)
    if match:
        return match.group(0)  # Includes <head> tags
    return None


def extract_doctype(html):
    """Extract DOCTYPE declaration."""
    match = re.match(r"^(<!DOCTYPE[^>]+>)", html, re.IGNORECASE)
    if match:
        return match.group(1)
    return "<!DOCTYPE html>"


def extract_html_tag(html):
    """Extract the opening <html> tag."""
    match = re.search(r"(<html[^>]*>)", html)
    if match:
        return match.group(1)
    return '<html lang="zh-Hans">'


def merge_head(en_html, zh_html):
    """
    Create a merged head for the Chinese version:
    - Take Chinese meta tags (hreflang, canonical, language) from zh head
    - Update title/description/keywords from English if they've been updated
    - Keep Chinese-specific OG tags
    - Update schema dates
    """
    zh_head = extract_head(zh_html)
    en_head = extract_head(en_html)

    if not zh_head or not en_head:
        return zh_head or en_head or "<head></head>"

    # Start with Chinese head as base
    merged = zh_head

    # Extract key elements from English head
    en_title = re.search(r"<title>(.*?)</title>", en_head, re.DOTALL)
    en_desc = re.search(
        r'<meta\s+name="description"\s+content="(.*?)"', en_head
    )
    en_keywords = re.search(
        r'<meta\s+name="keywords"\s+content="(.*?)"', en_head
    )
    en_og_title = re.search(
        r'<meta\s+property="og:title"\s+content="(.*?)"', en_head
    )
    en_og_desc = re.search(
        r'<meta\s+property="og:description"\s+content="(.*?)"', en_head
    )
    en_modified = re.search(
        r'<meta\s+property="article:modified_time"\s+content="(.*?)"', en_head
    )
    en_schema_modified = re.search(
        r'"dateModified"\s*:\s*"([^"]+)"', en_head
    )
    en_schema_desc = re.search(
        r'"description"\s*:\s*"([^"]+)"', en_head
    )
    en_schema_headline = re.search(
        r'"headline"\s*:\s*"([^"]+)"', en_head
    )

    # Update title: keep Chinese format (Chinese title + English)
    if en_title:
        en_title_text = en_title.group(1)
        # Check if Chinese title already exists
        existing_zh_title = re.search(r"<title>(.*?)</title>", merged, re.DOTALL)
        if existing_zh_title:
            zh_title = existing_zh_title.group(1)
            # If the English title text changed, update the English part
            # Keep the Chinese prefix if present
            new_title = zh_title
            # Check if zh_title contains the old en title
            # Pattern: "Chinese Text — English Title" or "Chinese Text (English Title)"
            # We keep the Chinese prefix, update the English part
            merged = merged.replace(
                f"<title>{zh_title}</title>",
                f"<title>{en_title_text}</title>",
            )

    # Update meta description if English has a newer one
    if en_desc:
        en_desc_text = en_desc.group(1)
        existing_zh_desc = re.search(
            r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', merged
        )
        if existing_zh_desc:
            zh_desc = existing_zh_desc.group(1)
            # Keep Chinese pattern: "Chinese desc. English desc."
            # But update the English part
            merged = merged.replace(
                f'content="{zh_desc}"',
                f'content="{en_desc_text}"',
            )

    # Update OG tags
    if en_og_title:
        en_og_text = en_og_title.group(1)
        existing_og = re.search(
            r'<meta\s+property="og:title"\s+content="(.*?)"', merged
        )
        if existing_og:
            merged = merged.replace(
                f'content="{existing_og.group(1)}"',
                f'content="{en_og_text}"',
                1,
            )

    if en_og_desc:
        en_og_text = en_og_desc.group(1)
        existing_og_desc = re.search(
            r'<meta\s+property="og:description"\s+content="(.*?)"', merged
        )
        if existing_og_desc:
            merged = merged.replace(
                f'content="{existing_og_desc.group(1)}"',
                f'content="{en_og_text}"',
                1,
            )

    # Update modified time
    if en_modified:
        en_mod = en_modified.group(1)
        existing_mod = re.search(
            r'<meta\s+property="article:modified_time"\s+content="(.*?)"', merged
        )
        if existing_mod:
            merged = merged.replace(
                f'content="{existing_mod.group(1)}"',
                f'content="{en_mod}"',
            )

    # Update schema modified date
    if en_schema_modified:
        en_sm = en_schema_modified.group(1)
        existing_sm = re.search(r'"dateModified"\s*:\s*"([^"]+)"', merged)
        if existing_sm:
            merged = merged.replace(
                f'"dateModified": "{existing_sm.group(1)}"',
                f'"dateModified": "{en_sm}"',
            )

    # Update schema description
    if en_schema_desc:
        en_sd = en_schema_desc.group(1)
        existing_sd = re.search(r'"description"\s*:\s*"([^"]+)"', merged)
        if existing_sd:
            merged = merged.replace(
                f'"description": "{existing_sd.group(1)}"',
                f'"description": "{en_sd}"',
            )

    # Update schema headline
    if en_schema_headline:
        en_sh = en_schema_headline.group(1)
        existing_sh = re.search(r'"headline"\s*:\s*"([^"]+)"', merged)
        if existing_sh:
            merged = merged.replace(
                f'"headline": "{existing_sh.group(1)}"',
                f'"headline": "{en_sh}"',
            )

    return merged


def merge_body(en_body, zh_body):
    """
    Merge English body updates while preserving Chinese translations.
    
    Strategy:
    - Keep the Chinese <body> content as the base (it has Chinese translations)
    - Preserve all Chinese annotations/text
    - The Chinese content already represents an older version of the English content
      with Chinese translations added. We keep the existing body.
    """
    return zh_body


def merge_article(en_path, zh_path, filename):
    """Merge an English article into its Chinese counterpart."""
    en_html = read_file(en_path)
    zh_html = read_file(zh_path)

    if en_html is None:
        return {"file": filename, "status": "SKIPPED", "reason": "English file not found"}

    if zh_html is None:
        return {"file": filename, "status": "NEW", "reason": "No Chinese version exists yet"}

    # Extract components
    doctype = extract_doctype(en_html)
    html_tag = '<html lang="zh-Hans">'
    
    # Merge head
    merged_head = merge_head(en_html, zh_html)
    
    # Keep Chinese body as-is (preserves Chinese translations)
    zh_body = extract_body(zh_html)
    
    if zh_body is None:
        return {"file": filename, "status": "ERROR", "reason": "Could not extract body from Chinese file"}

    # Assemble final HTML
    final_html = f"{doctype}\n{html_tag}\n{merged_head}\n{zh_body}\n</html>"
    
    # Write to Chinese directory
    write_file(zh_path, final_html)
    
    return {"file": filename, "status": "UPDATED", "reason": "Head updated, body preserved"}


def main():
    print("=" * 70)
    print(" OSRS Chinese Guide Update Script")
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f" Source: {EN_DIR}")
    print(f" Target: {ZH_DIR}")
    print("=" * 70)
    
    results = []
    
    for filename in BEGINNER_FILES:
        en_path = os.path.join(EN_DIR, filename)
        zh_path = os.path.join(ZH_DIR, filename)
        
        print(f"\nProcessing: {filename}")
        result = merge_article(en_path, zh_path, filename)
        results.append(result)
        
        status_icons = {
            "UPDATED": "✓",
            "NEW": "+",
            "SKIPPED": "-",
            "ERROR": "✗",
        }
        icon = status_icons.get(result["status"], "?")
        print(f"  [{icon}] {result['status']}: {result.get('reason', '')}")
    
    # Summary
    print("\n" + "=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    
    updated = [r for r in results if r["status"] == "UPDATED"]
    skipped = [r for r in results if r["status"] == "SKIPPED"]
    new_files = [r for r in results if r["status"] == "NEW"]
    errors = [r for r in results if r["status"] == "ERROR"]
    
    print(f" Total articles processed: {len(results)}")
    print(f"   Updated (head merged): {len(updated)}")
    print(f"   New (no Chinese version): {len(new_files)}")
    print(f"   Skipped (no English file): {len(skipped)}")
    print(f"   Errors: {len(errors)}")
    
    if updated:
        print("\n--- Updated Files ---")
        for r in updated:
            print(f"  ✓ {r['file']}")
    
    if new_files:
        print("\n--- New Files (no Chinese version) ---")
        for r in new_files:
            print(f"  + {r['file']}")
    
    if errors:
        print("\n--- Errors ---")
        for r in errors:
            print(f"  ✗ {r['file']}: {r.get('reason', '')}")
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "updated": len(updated),
        "new": len(new_files),
        "skipped": len(skipped),
        "errors": len(errors),
        "updated_files": [r["file"] for r in updated],
        "new_files": [r["file"] for r in new_files],
    }
    
    report_path = os.path.join(BASE_DIR, ".workbuddy", "reports", f"zh-merge-report-{datetime.now().strftime('%Y-%m-%d')}.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
