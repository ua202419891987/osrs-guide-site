#!/usr/bin/env python3
"""Update Related Guides internal linking - v2 with proper UTF-8 handling."""
import os

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

EDITS = {
    "osrs-beginner-guide-2026.html": {
        "old": """            <ul class="related-guides">
                <li><a href="osrs-optimal-quest-order-2026.html">Optimal Quest Order 2026</a></li>
                <li><a href="osrs-ironman-progression-guide-2026.html">Ironman Progression Guide</a></li>
                <li><a href="osrs-best-money-making-methods-2026.html">Best Money Making Methods 2026</a></li>
                <li><a href="osrs-fastest-99-agility-guide-2026.html">Agility 1-99 Guide</a></li>
                <li><a href="osrs-how-to-get-barrows-gloves-2026.html">Barrows Gloves Guide</a></li>
                <li><a href="osrs-how-to-get-fire-cape-2026.html">Fire Cape Guide</a></li>
            </ul>""",
        "new": """            <ul class="related-guides">
                <li><a href="osrs-new-player-guide-2026.html">OSRS New Player Guide 2026</a></li>
                <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                <li><a href="osrs-farming-guide-1-99-2026.html">OSRS 1-99 Farming Guide</a></li>
                <li><a href="osrs-best-money-making-tier-list-2026.html">OSRS Money Making Tier List</a></li>
                <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order 2026</a></li>
                <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
            </ul>"""
    },
    "osrs-ironman-progression-guide-2026.html": {
        "old": """            <ul class="related-guides">
                <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                <li><a href="osrs-slayer-guide-1-99-2026.html">Slayer 1-99 Guide</a></li>
                <li><a href="osrs-optimal-quest-order-2026.html">Optimal Quest Order 2026</a></li>
                <li><a href="osrs-ironman-early-game-guide-2026.html">Ironman Early Game Guide</a></li>
                <li><a href="osrs-farming-guide-1-99-2026.html">Farming 1-99 Guide</a></li>
            </ul>""",
        "new": """            <ul class="related-guides">
                <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order 2026</a></li>
                <li><a href="osrs-achievement-diary-guide-2026.html">OSRS Achievement Diary Guide</a></li>
                <li><a href="osrs-farming-guide-1-99-2026.html">OSRS 1-99 Farming Guide</a></li>
                <li><a href="osrs-mining-guide-1-99-2026.html">OSRS 1-99 Mining Guide</a></li>
            </ul>"""
    },
    "osrs-farming-guide-1-99-2026.html": {
        "old": """                <ul>
                    <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide 2026</a></li>
                    <li><a href="osrs-low-cost-1-99-herblore-guide.html">OSRS 1-99 Herblore Guide</a></li>
                    <li><a href="osrs-how-to-farm-herbs-for-profit-2026.html">OSRS Herb Farming Profit Guide</a></li>
                    <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                    <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide</a></li>
                </ul>""",
        "new": """                <ul>
                    <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                    <li><a href="osrs-low-cost-1-99-herblore-guide.html">OSRS 1-99 Herblore Guide</a></li>
                    <li><a href="osrs-how-to-farm-herbs-for-profit-2026.html">OSRS Herb Farming Profit Guide</a></li>
                    <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                    <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide</a></li>
                    <li><a href="osrs-magic-guide-1-99-2026.html">OSRS 1-99 Magic Guide</a></li>
                </ul>"""
    },
    "osrs-mining-guide-1-99-2026.html": {
        "old": """                <ul>
                    <li><a href="osrs-ironman-1-99-smithing-guide.html">OSRS 1-99 Smithing Guide</a></li>
                    <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                    <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                    <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide</a></li>
                </ul>""",
        "new": """                <ul>
                    <li><a href="osrs-ironman-1-99-smithing-guide.html">OSRS 1-99 Smithing Guide</a></li>
                    <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                    <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                    <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide</a></li>
                    <li><a href="osrs-main-account-guide-max-cape-2026.html">OSRS Max Cape Guide</a></li>
                    <li><a href="osrs-firemaking-guide-1-99-2026.html">OSRS 1-99 Firemaking Guide</a></li>
                </ul>"""
    },
    "osrs-optimal-quest-order-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-how-to-complete-monkey-madness-quest.html">Monkey Madness Quest Guide</a></li>
                        <li><a href="osrs-desert-treasure-2-guide-2026.html">Desert Treasure II Guide</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-new-player-guide-2026.html">OSRS New Player Guide 2026</a></li>
                        <li><a href="osrs-achievement-diary-guide-2026.html">OSRS Achievement Diary Guide</a></li>
                        <li><a href="osrs-desert-treasure-2-guide-2026.html">OSRS Desert Treasure II Guide</a></li>
                    </ul>"""
    },
    "osrs-clue-scroll-guide-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-best-money-making-methods-2026.html">OSRS Best Money Making Methods 2026</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-achievement-diary-guide-2026.html">OSRS Achievement Diary Guide</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-best-money-making-methods-2026.html">OSRS Best Money Making Methods</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-achievement-diary-guide-2026.html">OSRS Achievement Diary Guide</a></li>
                        <li><a href="osrs-wilderness-guide-2026.html">OSRS Wilderness Guide</a></li>
                        <li><a href="osrs-ranged-guide-1-99-2026.html">OSRS 1-99 Ranged Guide</a></li>
                    </ul>"""
    },
    "osrs-achievement-diary-guide-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order 2026</a></li>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide 2026</a></li>
                        <li><a href="osrs-main-account-guide-max-cape-2026.html">OSRS Main Account Max Cape Guide</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order</a></li>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide</a></li>
                        <li><a href="osrs-main-account-guide-max-cape-2026.html">OSRS Max Cape Guide</a></li>
                        <li><a href="osrs-wilderness-guide-2026.html">OSRS Wilderness Guide</a></li>
                    </ul>"""
    },
    "osrs-best-money-making-tier-list-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-best-money-making-methods-2026.html">OSRS Best Money Making Methods 2026 (Detailed)</a></li>
                        <li><a href="osrs-best-f2p-money-making-2026.html">OSRS Best F2P Money Making 2026</a></li>
                        <li><a href="money-making.html">OSRS Money Making Hub</a></li>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-best-money-making-methods-2026.html">OSRS Best Money Making (Detailed)</a></li>
                        <li><a href="osrs-best-f2p-money-making-2026.html">OSRS Best F2P Money Making</a></li>
                        <li><a href="money-making.html">OSRS Money Making Hub</a></li>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-wilderness-guide-2026.html">OSRS Wilderness Money Making</a></li>
                    </ul>"""
    },
    "osrs-wilderness-guide-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-best-money-making-methods-2026.html">OSRS Best Money Making Methods 2026</a></li>
                        <li><a href="osrs-how-to-train-prayer-cheap-f2p.html">OSRS 1-99 Prayer Guide</a></li>
                        <li><a href="osrs-best-in-slot-gear-guide-2026.html">OSRS Best in Slot Gear Guide</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-best-money-making-methods-2026.html">OSRS Best Money Making Methods</a></li>
                        <li><a href="osrs-how-to-train-prayer-cheap-f2p.html">OSRS 1-99 Prayer Guide</a></li>
                        <li><a href="osrs-best-in-slot-gear-guide-2026.html">OSRS Best in Slot Gear Guide</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-clue-scroll-guide-2026.html">OSRS Clue Scroll Guide</a></li>
                        <li><a href="osrs-achievement-diary-guide-2026.html">OSRS Achievement Diary Guide</a></li>
                    </ul>"""
    },
    "osrs-main-account-guide-max-cape-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order</a></li>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-best-money-making-tier-list-2026.html">OSRS Money Making Tier List</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order</a></li>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-best-money-making-tier-list-2026.html">OSRS Money Making Tier List</a></li>
                        <li><a href="osrs-fletching-guide-1-99-2026.html">OSRS 1-99 Fletching Guide</a></li>
                        <li><a href="osrs-firemaking-guide-1-99-2026.html">OSRS 1-99 Firemaking Guide</a></li>
                        <li><a href="osrs-POH-max-house-guide-2026.html">OSRS Max POH House Guide</a></li>
                        <li><a href="osrs-minigames-guide-2026.html">OSRS Minigames Guide</a></li>
                    </ul>"""
    },
    "osrs-minigames-guide-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-guardians-of-the-rift-guide-2026.html">OSRS Guardians of the Rift Guide</a></li>
                        <li><a href="osrs-tempoross-guide-2026.html">OSRS Tempoross Guide</a></li>
                        <li><a href="osrs-nightmare-zone-guide-ironman-2026.html">OSRS Nightmare Zone Guide</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026</a></li>
                        <li><a href="osrs-guardians-of-the-rift-guide-2026.html">OSRS Guardians of the Rift Guide</a></li>
                        <li><a href="osrs-tempoross-guide-2026.html">OSRS Tempoross Guide</a></li>
                        <li><a href="osrs-nightmare-zone-guide-ironman-2026.html">OSRS Nightmare Zone Guide</a></li>
                        <li><a href="osrs-POH-max-house-guide-2026.html">OSRS Max POH House Guide</a></li>
                        <li><a href="osrs-firemaking-guide-1-99-2026.html">OSRS 1-99 Firemaking Guide</a></li>
                    </ul>"""
    },
    "osrs-new-player-guide-2026.html": {
        "old": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026 (Detailed)</a></li>
                        <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order</a></li>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-best-f2p-money-making-2026.html">OSRS Best F2P Money Making</a></li>
                    </ul>""",
        "new": """                    <ul>
                        <li><a href="osrs-beginner-guide-2026.html">OSRS Beginner Guide 2026 (Detailed)</a></li>
                        <li><a href="osrs-optimal-quest-order-2026.html">OSRS Optimal Quest Order</a></li>
                        <li><a href="osrs-ironman-progression-guide-2026.html">OSRS Ironman Progression Guide</a></li>
                        <li><a href="osrs-best-f2p-money-making-2026.html">OSRS Best F2P Money Making</a></li>
                        <li><a href="osrs-slayer-guide-1-99-2026.html">OSRS 1-99 Slayer Guide</a></li>
                        <li><a href="osrs-best-money-making-tier-list-2026.html">OSRS Money Making Tier List</a></li>
                    </ul>"""
    },
}


def main():
    success = 0
    for filename, edit in EDITS.items():
        filepath = os.path.join(GUIDES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if edit["old"] not in content:
            print(f"  ? {filename}: old text not found (may already be updated)")
            # Try to locate it
            idx = content.find("<h2>Related Guides</h2>")
            if idx >= 0:
                print(f"    Found Related Guides at offset {idx}")
                print(f"    Surrounding: ...{content[idx:idx+300]}...")
            continue

        content = content.replace(edit["old"], edit["new"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {filename}")
        success += 1
    
    print(f"\n✅ Updated {success}/{len(EDITS)} files.")


if __name__ == "__main__":
    main()
