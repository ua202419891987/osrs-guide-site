#!/usr/bin/env python3
"""
Deduplicate quick-summary divs: keep only the first one, remove all others.
Also ensure support cards are clean.
"""
import re
import os

BASE = r"C:\Users\Lenovo\osrs-guide-site"

FILES = [
    "osrs-1-99-mining-guide-beginner-2026.html",
    "osrs-cheap-flipping-methods-new-players.html",
    "osrs-combat-training-beginner-2026.html",
    "osrs-diary-priority-order-beginner-2026.html",
    "osrs-f2p-combat-training-guide-2026.html",
    "osrs-f2p-ironman-money-making-early-game.html",
    "osrs-f2p-leveling-guide-2026.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-quests-before-membership-2026.html",
    "osrs-f2p-to-member-first-10-things-2026.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
    "osrs-first-boss-progression-roadmap-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-low-effort-money-making-beginners.html",
    "osrs-money-making-beginner-2026.html",
    "osrs-prayer-training-beginner-guide-2026.html",
    "osrs-skill-training-beginner-complete-guide-2026.html",
    "osrs-skill-training-beginner-fast-track-2026.html",
    "osrs-slayer-beginner-guide-2026.html",
    "osrs-all-skills-overview-guide-2026.html",
    "osrs-efficient-training-routes-beginners-2026.html",
    "osrs-how-to-beat-zulrah-beginners-rotation.html",
    "osrs-how-to-solo-god-wars-boss-for-beginners.html",
    "osrs-how-to-train-prayer-cheap-f2p.html",
    "osrs-members-vs-f2p-comparison-2026.html",
    "osrs-nmz-beginner-guide-2026.html",
    "osrs-obor-bryophyta-f2p-boss-guide-2026.html",
    "osrs-skills-overview-beginner-2026.html",
    "osrs-slayer-beginner-first-master-guide-2026.html",
    "osrs-toa-solo-beginner-guide-2026.html",
    "osrs-top-10-skills-to-train-first-2026.html",
    "osrs-fastest-99-cooking-f2p.html",
]

def deduplicate_quick_summaries(html):
    """Find all quick-summary divs, keep only the first one."""
    # Find all quick-summary starts
    pattern = re.compile(r'<div[^>]*class="quick-summary"[^>]*>')
    matches = list(pattern.finditer(html))
    
    if len(matches) <= 1:
        return html  # 0 or 1 quick-summary, no dedup needed
    
    # Keep only the first one
    # Find where the second one starts and find its end
    second_start = matches[1].start()
    
    # Find the matching end of the second quick-summary div
    # Count nesting to find the right </div>
    remaining = html[second_start:]
    depth = 0
    end_idx = 0
    for m in re.finditer(r'</?div[^>]*>', remaining):
        tag = m.group(0)
        if tag.startswith('</div'):
            depth -= 1
            if depth <= 0:
                end_idx = second_start + m.end()
                break
        else:
            depth += 1
    
    if end_idx > 0:
        html = html[:second_start] + html[end_idx:]
    
    # Check if there are still more (3rd+)
    return deduplicate_quick_summaries(html)


def fix_support_card(html):
    """Remove （中文说明） from support card h3."""
    html = re.sub(
        r'(<div[^>]*class="support-card[^"]*"[^>]*>.*?<h3[^>]*>.*?)（中文说明）(.*?</h3>)',
        r'\1\2', html, flags=re.DOTALL
    )
    return html


def main():
    for filename in FILES:
        path = os.path.join(BASE, "zh/guides", filename)
        if not os.path.exists(path):
            print(f"SKIP: {filename}")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        changes = []
        
        old = html
        html = deduplicate_quick_summaries(html)
        if html != old:
            changes.append("dedup quick-summary")
        
        old = html
        html = fix_support_card(html)
        if html != old:
            changes.append("fixed support card")
        
        # Also remove any remaining （中文说明） from 30秒预览
        old = html
        html = html.replace('30秒快速预览（中文说明）', '30秒快速预览')
        if html != old:
            changes.append("cleaned preview annotation")
        
        if changes:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"FIXED ({', '.join(changes)}): {filename}")
        else:
            print(f"OK: {filename}")

if __name__ == '__main__':
    main()
