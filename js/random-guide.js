/* ===================================================
   OSRS Guru — Random Guide Button
   Picks a random guide and navigates to it
   =================================================== */

const RANDOM_GUIDES = [
  // ── New Player Series (Stage 0) ──
  'guides/osrs-new-player-guide-2026.html',
  'guides/osrs-interface-controls-beginner-guide-2026.html',
  'guides/osrs-combat-triangle-explained-2026.html',
  'guides/osrs-all-skills-overview-guide-2026.html',
  'guides/osrs-bank-inventory-management-2026.html',
  'guides/osrs-maps-travel-guide-2026.html',
  'guides/osrs-questing-beginner-guide-2026.html',
  'guides/osrs-combat-training-beginner-2026.html',
  'guides/osrs-money-making-beginner-2026.html',
  'guides/osrs-gear-beginner-guide-2026.html',

  // ── Money Making ──
  'money-making.html',
  'guides/osrs-ironman-money-making-f2p-2026.html',
  'guides/osrs-how-to-make-money-with-zulrah.html',
  'guides/osrs-wintertodt-money-making-per-hour.html',
  'guides/osrs-killing-green-dragons-money-per-hour.html',
  'guides/osrs-how-to-flip-items-profit-mid-game.html',
  'guides/osrs-chambers-of-xeric-loot-profit-guide.html',

  // ── Skill Training ──
  'skill-training.html',
  'guides/osrs-fastest-99-cooking-f2p.html',
  'guides/osrs-cheapest-99-runecrafting-2026.html',
  'guides/osrs-ironman-1-99-smithing-guide.html',
  'guides/osrs-how-to-get-99-agility-fast-2026.html',
  'guides/osrs-fastest-99-attack-strength-defence.html',
  'guides/osrs-low-cost-1-99-herblore-guide.html',

  // ── Boss Guides ──
  'boss-guides.html',
  'guides/osrs-how-to-beat-zulrah-beginners-rotation.html',
  'guides/osrs-low-gear-setup-vorkath-guide.html',
  'guides/osrs-how-to-get-dragon-defender-2026.html',
  'guides/osrs-gauntlet-meta-changes-2026.html',

  // ── Quests ──
  'quest-guides.html',
  'guides/osrs-goraik-quest-guide-2026.html',
  'guides/osrs-goraik-rewards-worth-it-2026.html',
  'guides/osrs-khopesh-guide-2026.html',

  // ── Updates ──
  'monthly-updates.html',
  'weekly-updates.html',
  'guides/osrs-summer-sweep-up-2026-guide.html',
  'guides/osrs-blood-moon-rises-guide-2026.html',
  'guides/osrs-sailing-wyrmscraig-guide-2026.html',
];

function openRandomGuide() {
  const idx = Math.floor(Math.random() * RANDOM_GUIDES.length);
  const url = RANDOM_GUIDES[idx];
  window.location.href = url;
}
