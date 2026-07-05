#!/usr/bin/env python3
"""
Final cleanup: remove duplicate quick previews, fix annotations on quick-preview h3,
and clean up references/sources headings.
"""
import re
import os

BASE = r"C:\Users\Lenovo\osrs-guide-site"

FILES = [
    "osrs-1-99-mining-guide-beginner-2026.html",
    "osrs-all-skills-overview-guide-2026.html",
    "osrs-cheap-flipping-methods-new-players.html",
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
    "osrs-first-boss-progression-roadmap-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
    "osrs-how-to-beat-zulrah-beginners-rotation.html",
    "osrs-how-to-solo-god-wars-boss-for-beginners.html",
    "osrs-how-to-train-prayer-cheap-f2p.html",
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-low-effort-money-making-beginners.html",
    "osrs-members-vs-f2p-comparison-2026.html",
    "osrs-money-making-beginner-2026.html",
    "osrs-nmz-beginner-guide-2026.html",
    "osrs-obor-bryophyta-f2p-boss-guide-2026.html",
    "osrs-prayer-training-beginner-guide-2026.html",
    "osrs-skills-overview-beginner-2026.html",
    "osrs-skill-training-beginner-complete-guide-2026.html",
    "osrs-skill-training-beginner-fast-track-2026.html",
    "osrs-slayer-beginner-first-master-guide-2026.html",
    "osrs-slayer-beginner-guide-2026.html",
    "osrs-toa-solo-beginner-guide-2026.html",
    "osrs-top-10-skills-to-train-first-2026.html",
]

def cleanup_file(filename):
    zh_path = os.path.join(BASE, "zh/guides", filename)
    if not os.path.exists(zh_path):
        return
    
    with open(zh_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    changes = []
    
    # 1. Remove （中文说明） from 30秒快速预览 headings
    old = html
    html = re.sub(r'30秒快速预览（中文说明）', '30秒快速预览', html)
    if html != old:
        changes.append("Cleaned quick-preview annotations")
    
    # 2. Remove duplicate quick preview boxes (keep the first one)
    # Find all occurrences of quick-summary divs
    count = html.count('30秒快速预览')
    if count > 1:
        # Split by quick-summary start
        parts = html.split('<div class="quick-summary"', 2)
        if len(parts) >= 3:
            # We have 2+ quick-summary divs
            first_part = parts[0] + '<div class="quick-summary"' + parts[1]
            remaining = '<div class="quick-summary"' + parts[2]
            
            # Find the end of the second quick-summary div
            # It starts with: <div class="quick-summary" style=...> and ends with </div>
            # Find the matching closing div
            depth = 0
            end_idx = 0
            for m in re.finditer(r'</?div[^>]*>', remaining):
                tag = m.group(0)
                if tag.startswith('</div'):
                    depth -= 1
                    if depth <= 0:
                        end_idx = m.end()
                        break
                else:
                    depth += 1
            
            if end_idx > 0:
                html = first_part + remaining[end_idx:]
                changes.append("Removed duplicate quick-preview")
    
    # 3. Remove （中文说明） from References & Sources headings
    old = html
    html = re.sub(r'References & Sources（中文说明）', 'References & Sources', html)
    if html != old:
        changes.append("Cleaned References heading")
    
    # 4. Remove （中文说明） from Quick-Jump TOC headings
    old = html
    html = re.sub(r'Table of Contents（中文说明）', 'Table of Contents', html)
    if html != old:
        changes.append("Cleaned TOC heading")
    
    if changes:
        with open(zh_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  FIXED ({', '.join(changes)}): {filename}")
    else:
        print(f"  OK: {filename}")

def main():
    for i, f in enumerate(FILES, 1):
        print(f"[{i}/{len(FILES)}] {f}")
        cleanup_file(f)
    print("Done!")

if __name__ == '__main__':
    main()
