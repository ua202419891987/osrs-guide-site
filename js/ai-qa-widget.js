/**
 * OSRS Guru AI Question & Answer Widget
 * 右下角悬浮窗 - AI 问答系统
 * v2.12.0 - Add 12 new Money Making Deep Dive guides (Slayer Money, Boss Profit, Flipping, Mid-Game, AFK, Daily Routine, Quest-Unlocked, Wilderness, Ironman P2P, Skilling Post-Sailing, Non-Boss Combat, Spend GP Wisely)
 * v2.11.0 - Add 16 new CD+Windrose guides to article index (Co-op, Farming, Build, Endgame, PvP, Secrets, Performance, Patch)
 * v2.14.1 - Fix: brighter pulse ring (white/gold), badge always visible, bubble shows every 2hrs
 * v2.14.0 - Visibility boost: pulse animation + NEW badge + preview bubble + page-context suggested questions
 * v2.13.0 - Hybrid mode: suggested buttons trigger AI answers + article links; search box keeps article links
 * v2.12.2 - Add suggested questions + article page CTA injection
 * v2.10.0 - Add 22 new OSRS guides to article index (Skill Training + Money Making + Slayer + Boss + Quest)
 *   - OSRS_ARTICLES: 154 → 176 entries
 * v2.9.2 - FIX: Add leading / to all URLs (404 fix)
 *   - OSRS: local match grouped by stage (beginner/mid/boss), display as "Pick your stage"
 *   - CD/Windrose: flat list (all beginners)
 *   - Backend: OSRS → Wiki → DeepSeek V3; CD/Windrose → DeepSeek V3 only
 *   - v2.9 fix: source=osrsguru → NO text bubble, just link; others → max 300 chars
 */

(function () {
  'use strict';

  // ========== 模块级变量（供 window.OSRSQA.ask 访问） ==========
  var widget, input, sendBtn;

  // ========== 游戏上下文检测 ==========
  const GAME = detectGame();

  function detectGame() {
    var path = window.location.pathname.toLowerCase();
    if (path.indexOf('/crimson-desert/') !== -1 || path.indexOf('crimson-desert') !== -1) return 'crimson-desert';
    if (path.indexOf('/windrose/') !== -1 || path.indexOf('windrose') !== -1) return 'windrose';
    return 'osrs';
  }

  // ========== 配置 ==========
  var CONFIG = {
    apiBase: window.location.hostname === 'localhost'
      ? 'http://localhost:8000'
      : 'https://osrs-rag-api.vercel.app',
    widgetId: 'osrs-qa-widget',
    widgetButtonId: 'osrs-qa-toggle-btn',
    maxMessages: 10,
    game: GAME,
    gameName: GAME === 'crimson-desert' ? 'Crimson Desert' : (GAME === 'windrose' ? 'Windrose' : 'OSRS'),
    gameIcon: GAME === 'crimson-desert' ? '⚔️' : (GAME === 'windrose' ? '⚓' : '⚔️'),
    assistantTitle: GAME === 'crimson-desert' ? 'Crimson Desert AI Assistant' : (GAME === 'windrose' ? 'Windrose AI Assistant' : 'OSRS AI Assistant'),
    inputPlaceholder: GAME === 'crimson-desert' ? 'Ask about Crimson Desert...' : (GAME === 'windrose' ? 'Ask about Windrose...' : 'Ask about OSRS guides...'),
    sourceGuruLabel: GAME === 'crimson-desert' ? 'Crimson Desert Guru' : (GAME === 'windrose' ? 'Windrose Guru' : 'OSRS Guru'),
  };

  // ========== 动态TOC提取 ==========
  function extractPageTOC() {
    var toc = [];
    // 通用选择器：取所有有id的h2/h3，排除导航/侧栏
    var allHeadings = document.querySelectorAll('h2[id], h3[id]');
    for (var i = 0; i < allHeadings.length; i++) {
      if (allHeadings[i].closest('nav, footer, header, aside, .sidebar, .navigation, .qa-header, .qa-input-group, .qa-messages')) continue;
      var text = (allHeadings[i].textContent || '').replace(/^\d+[\.:]\s*/, '').replace(/^Section\s+\d+[\.:]?\s*/i, '').trim();
      toc.push({
        id: allHeadings[i].id,
        text: text,
        rawText: (allHeadings[i].textContent || '').trim(),
        element: allHeadings[i]
      });
    }
    return toc;
  }

  // ========== 问题匹配TOC段落 ==========
  function matchTOCSections(question, toc) {
    if (!toc || toc.length === 0) return [];
    var lowerQ = question.toLowerCase();
    // 提取问题中的关键词（去掉标点，取长度>3的词）
    var qWords = lowerQ.replace(/[?.,!;:'"()\[\]{}]/g, ' ').split(/\s+/).filter(function(w) { return w.length > 3; });
    var matches = [];

    for (var i = 0; i < toc.length; i++) {
      var hText = toc[i].text.toLowerCase();
      var hRaw = toc[i].rawText.toLowerCase();
      var bestScore = 0;
      var matchedWord = '';

      for (var w = 0; w < qWords.length; w++) {
        var word = qWords[w];
        if (hText.indexOf(word) !== -1 || hRaw.indexOf(word) !== -1) {
          // 越长的关键词匹配得分越高
          var score = word.length + (hText.indexOf(word) === 0 ? 2 : 0);
          if (score > bestScore) {
            bestScore = score;
            matchedWord = word;
          }
        }
      }

      if (bestScore > 0) {
        matches.push({ tocItem: toc[i], score: bestScore, matchedWord: matchedWord });
      }
    }

    matches.sort(function(a, b) { return b.score - a.score; });
    return matches.slice(0, 2); // 最多返回2个最相关段落
  }

  // ========== 本地文章索引（200篇，2026-06-17） ==========
  var CD_ARTICLES = [
    { label: 'Crimson Desert Boss Guide 2026 \u2014 Every Boss, Strategy &amp; Rewards', url: '/guides/crimson-desert/crimson-desert-boss-guide-2026.html', kw: 'boss bosses bossing cd crimson desert pvm pywel kliff strategy' },
    { label: 'Crimson Desert Combat Guide 2026 \u2014 Master Parry, Dodge &amp; Combo Chains', url: '/guides/crimson-desert/crimson-desert-combat-guide-2026.html', kw: 'combat cd crimson desert dodge parry pywel kliff attack defence defense strength', anchorMap: { 'parry': 'section2', 'dodge': 'section2', 'combo': 'section3', 'stamina': 'section4', 'spirit': 'section5', 'surge': 'section5', 'grapple': 'section6', 'counter': 'section2', 'fight': 'section1', 'combat': 'section1' } },
    { label: 'Crimson Desert Beginner Guide 2026 \u2014 How to Start Strong in Pywel', url: '/guides/crimson-desert/crimson-desert-new-player-guide-2026.html', kw: 'beginner cd crimson desert pywel kliff start strong new player' },
    { label: 'Crimson Desert Quest Walkthrough 2026 \u2014 Main Story &amp; Side Quests', url: '/guides/crimson-desert/crimson-desert-quest-walkthrough-2026.html', kw: 'cd choices crimson desert diary quest questing quests story walkthrough kliff pywel' },
    { label: 'Crimson Desert Skills &amp; Builds Guide 2026', url: '/guides/crimson-desert/crimson-desert-skills-builds-guide-2026.html', kw: 'build builds cd crimson desert skills skill trees paths pywel kliff' },
    { label: 'Crimson Desert Weapons &amp; Equipment Guide 2026', url: '/guides/crimson-desert/crimson-desert-weapons-gear-guide-2026.html', kw: 'armor armour cd crimson desert equipment gear weapons stats locations pywel kliff' },
    { label: 'Crimson Desert Co-op Multiplayer Guide 2026', url: '/guides/crimson-desert/crimson-desert-coop-multiplayer-guide-2026.html', kw: 'co-op multiplayer friends boss coop loot sharing server' },
    { label: 'Crimson Desert Money Farming Guide 2026', url: '/guides/crimson-desert/crimson-desert-money-farming-guide-2026.html', kw: 'money farming gold resource grinding route crimson desert' },
    { label: 'Crimson Desert Meta Build Tier List 2026', url: '/guides/crimson-desert/crimson-desert-meta-build-tier-list-2026.html', kw: 'build tier list meta best builds damage calculation crimson desert' },
    { label: 'Crimson Desert Endgame Guide 2026', url: '/guides/crimson-desert/crimson-desert-endgame-guide-2026.html', kw: 'endgame post-game legendary gear ng+ crimson desert' },
    { label: 'Crimson Desert PvP Arena Guide 2026', url: '/guides/crimson-desert/crimson-desert-pvp-arena-guide-2026.html', kw: 'pvp arena ranking rewards pvp builds crimson desert' },
    { label: 'Crimson Desert Hidden Secrets &amp; Easter Eggs 2026', url: '/guides/crimson-desert/crimson-desert-hidden-secrets-easter-eggs-2026.html', kw: 'secrets easter eggs hidden locations lore items crimson desert' },
    { label: 'Crimson Desert Best Settings &amp; Performance 2026', url: '/guides/crimson-desert/crimson-desert-best-settings-performance-2026.html', kw: 'performance fps optimization settings stuttering fix crimson desert' },
    { label: 'Crimson Desert Patch Notes Analysis 2026', url: '/guides/crimson-desert/crimson-desert-patch-notes-analysis-2026.html', kw: 'patch notes updates changes nerfs buffs crimson desert' },
  ];

  var WINDROSE_ARTICLES = [
    { label: 'Windrose Base Building &amp; Advanced Tips 2026', url: '/guides/windrose/windrose-base-building-tips-2026.html', kw: 'base building defenses endgame naval pirate sailing ship windrose' },
    { label: 'Windrose Beginner Guide 2026 \u2014 Survive &amp; Thrive in the Age of Piracy', url: '/guides/windrose/windrose-beginner-guide-2026.html', kw: 'beginner naval new player piracy pirate sailing ship start survive thrive windrose' },
    { label: 'Windrose Boss Guide 2026 \u2014 Every Boss, Strategy &amp; Drops', url: '/guides/windrose/windrose-boss-guide-2026.html', kw: 'boss bosses bossing drops naval pirate pvm sailing ship strategy windrose' },
    { label: 'Windrose Combat &amp; Naval Guide 2026 \u2014 Ship Battles &amp; Boarding', url: '/guides/windrose/windrose-combat-ship-guide-2026.html', kw: 'combat naval parry dodge ship battles boarding pirate sailing windrose attack defence defense strength' },
    { label: 'Windrose Crafting &amp; Gear Guide 2026 \u2014 Best Weapons, Armor &amp; Ship Upgrades', url: '/guides/windrose/windrose-crafting-gear-guide-2026.html', kw: 'armor armour crafting equipment gear weapons ship upgrades naval pirate sailing windrose' },
    { label: 'Windrose Quest &amp; Exploration Guide 2026 \u2014 Hidden Treasures &amp; Lore', url: '/guides/windrose/windrose-quest-exploration-guide-2026.html', kw: 'exploration lore naval pirate quest questing quests routes sailing ship treasures windrose' },
    { label: 'Windrose Co-op Multiplayer Guide 2026', url: '/guides/windrose/windrose-coop-multiplayer-guide-2026.html', kw: 'co-op multiplayer friends server hosting roles voice chat windrose' },
    { label: 'Windrose Resource Farming Guide 2026', url: '/guides/windrose/windrose-resource-farming-guide-2026.html', kw: 'resource farming routes rare materials grinding windrose' },
    { label: 'Windrose Meta Build Tier List 2026', url: '/guides/windrose/windrose-meta-build-tier-list-2026.html', kw: 'build tier list meta best builds stat allocation windrose' },
    { label: 'Windrose Endgame Guide 2026', url: '/guides/windrose/windrose-endgame-guide-2026.html', kw: 'endgame post-game legendary ships challenges windrose' },
    { label: 'Windrose Ship PvP Combat Guide 2026', url: '/guides/windrose/windrose-ship-pvp-combat-guide-2026.html', kw: 'ship pvp combat naval battle tactics boarding windrose' },
    { label: 'Windrose Treasure Map &amp; Secrets Guide 2026', url: '/guides/windrose/windrose-treasure-map-secrets-2026.html', kw: 'treasure map secrets hidden caves easter eggs windrose' },
    { label: 'Windrose Performance Optimization 2026', url: '/guides/windrose/windrose-performance-optimization-2026.html', kw: 'performance fps optimization lag fix settings windrose' },
    { label: 'Windrose Early Access Update Guide 2026', url: '/guides/windrose/windrose-early-access-update-guide-2026.html', kw: 'early access updates patch notes roadmap windrose' },
  ];

  // OSRS 176篇全索引（154篇原有 + 22篇新增，2026-06-16）
  var OSRS_ARTICLES = [
    { label: 'Account Security \u2014 Protect From Hackers', url: '/guides/account-security-guide-2026.html', stage: 'beginner', kw: 'account authenticator bank hackers protect security' },
    { label: 'Barrows \u2014 First Boss GP', url: '/guides/barrows-first-boss-gp-2026.html', stage: 'beginner', kw: 'ahrim barrows boss bosses bossing brothers dharok gp pvm' },
    { label: 'Best Quests for New Members', url: '/guides/best-quests-new-members-2026.html', stage: 'beginner', kw: 'diary members quest questing quests roadmap' },
    { label: 'Blood Moon Rises Quest Walkthrough', url: '/guides/blood-moon-rises-quest-guide-2026.html', stage: 'mid', kw: 'blood moon quest questing rises walkthrough diary' },
    { label: 'Combat Achievements \u2014 Easy to Grandmaster', url: '/guides/combat-achievements-guide-2026.html', stage: 'mid', kw: 'achievements attack combat defence defense grandmaster strength' },
    { label: 'F2P to P2P Bond \u2014 Earn Membership', url: '/guides/f2p-to-p2p-bond-guide-2026.html', stage: 'beginner', kw: 'bond f2p free play member membership p2p' },
    { label: 'First 5M GP for New Members', url: '/guides/first-5m-gp-members-2026.html', stage: 'beginner', kw: 'gp money members first' },
    { label: 'League 6 Preparation \u2014 Predictions & Strategy', url: '/guides/league-6-prep-guide-2026.html', stage: 'mid', kw: 'league leagues preparation seasonal strategy' },
    { label: 'Max Cape Efficient Route', url: '/guides/max-cape-route-2026.html', stage: 'boss', kw: 'cape efficient max record' },
    { label: 'Mid-Game Money Making 1M to 100M', url: '/guides/mid-game-money-making-2026.html', stage: 'mid', kw: 'flip flipping gp intermediate mid game money profit' },
    { label: 'New Boss Guide \u2014 Kill Strategy & Loot', url: '/guides/new-boss-loot-guide-2026.html', stage: 'mid', kw: 'boss bosses bossing kill loot pvm strategy' },
    { label: '1-99 Crafting \u2014 Fast, Cheap & Ironman', url: '/guides/osrs-1-99-crafting-guide-2026.html', stage: 'mid', kw: 'battlestaff cheap crafting gems ironman jewelry methods' },
    { label: '1-99 Farming \u2014 Profit Focused', url: '/guides/osrs-1-99-farming-guide-beginner-profit-2026.html', stage: 'mid', kw: 'allotment beginner farming herb patch profit' },
    { label: '1-99 Hitpoints Training Methods & XP', url: '/guides/osrs-1-99-hitpoints-guide-2026.html', stage: 'mid', kw: 'hitpoints methods training xp' },
    { label: '1-99 Hitpoints Training', url: '/guides/osrs-1-99-hitpoints-training-guide-2026.html', stage: 'mid', kw: 'hitpoints training' },
    { label: '1-99 Hunter AFK Method \u2014 Birdhouses & Chinchompas', url: '/guides/osrs-1-99-hunter-guide-afk-method.html', stage: 'mid', kw: 'afk bird birdhouses chinchompa herbiboar hunter trap monkeys' },
    { label: '1-99 Magic Training Cheap Methods', url: '/guides/osrs-1-99-magic-training-cheap-guide-2026.html', stage: 'mid', kw: 'cheap enchant mage magic methods spell training' },
    { label: '1-99 Mining Beginner', url: '/guides/osrs-1-99-mining-guide-beginner-2026.html', stage: 'beginner', kw: 'beginner mining ore pickaxe rock' },
    { label: '1-99 Prayer \u2014 Fast, Cheap & Ironman', url: '/guides/osrs-1-99-prayer-guide-2026.html', stage: 'mid', kw: 'altar bones cheap gilded ironman methods prayer' },
    { label: '1-99 Prayer All Methods Fastest & Cheapest', url: '/guides/osrs-1-99-prayer-guide-all-methods-2026.html', stage: 'mid', kw: 'altar bones cheapest fastest gilded methods prayer' },
    { label: '1-99 Thieving Ironman \u2014 Pyramid Plunder & Knights', url: '/guides/osrs-1-99-thieving-guide-ironman.html', stage: 'mid', kw: 'farmers iron ironman ironmen knight pickpocket plunder pyramid thieving xp' },
    { label: '1-99 Woodcutting Early Game F2P to Redwoods', url: '/guides/osrs-1-99-woodcutting-guide-early-game.html', stage: 'beginner', kw: 'axe log redwood tree woodcutting f2p' },
    { label: '2026 Roadmap \u2014 New Skills, Raids & Quests', url: '/guides/osrs-2026-roadmap.html', stage: 'mid', kw: 'quests raids roadmap skills updates map teleport transport travel' },
    { label: 'Achievement Diary \u2014 All Diaries & Rewards', url: '/guides/osrs-achievement-diary-guide-2026.html', stage: 'mid', kw: 'achievement diaries diary order rewards task' },
    { label: 'Affordable Leveling on a Budget', url: '/guides/osrs-affordable-leveling-guide-2026.html', stage: 'beginner', kw: 'affordable budget leveling methods' },
    { label: 'Agility Training 1-99 Rooftop Courses', url: '/guides/osrs-agility-training-guide-2026.html', stage: 'mid', kw: 'agility course courses graceful rooftop training xp' },
    { label: 'All Skills Overview Beginner Reference', url: '/guides/osrs-all-skills-overview-guide-2026.html', stage: 'beginner', kw: 'beginner overview reference skills' },
    { label: 'Araxxor Boss \u2014 Slayer Strategy & Noxious Halberd', url: '/guides/osrs-araxxor-guide-2026.html', stage: 'boss', kw: 'araxxor boss gear halberd noxious slayer strategy' },
    { label: 'Bank & Inventory Management', url: '/guides/osrs-bank-inventory-management-2026.html', stage: 'mid', kw: 'bank inventory items organize' },
    { label: 'Blood Moon Rises Prep Checklist (June 30)', url: '/guides/osrs-blood-moon-prep-checklist-2026.html', stage: 'mid', kw: 'blood checklist june moon prep rises' },
    { label: 'Blood Moon Rises \u2014 Myreque Finale', url: '/guides/osrs-blood-moon-rises-guide-2026.html', stage: 'mid', kw: 'blood finale june moon myreque rises' },
    { label: 'Boss Profit Tier List \u2014 Ranked by GP/hr', url: '/guides/osrs-boss-profit-tier-list-2026.html', stage: 'boss', kw: 'boss bosses bossing gp profit pvm ranked meta' },
    { label: 'Cerberus Boss \u2014 Mid-Game Slayer', url: '/guides/osrs-cerberus-boss-guide-2026.html', stage: 'boss', kw: 'boss cerberus hellhound midgame primordial pvm slayer' },
    { label: 'Chambers of Xeric Loot & Profit \u2014 Twisted Bow', url: '/guides/osrs-chambers-of-xeric-loot-profit-guide.html', stage: 'boss', kw: 'bow chambers drops gp loot olm profit twisted xeric' },
    { label: 'Cheap Flipping Methods 100K Capital', url: '/guides/osrs-cheap-flipping-methods-new-players.html', stage: 'beginner', kw: 'capital cheap flipping methods players' },
    { label: 'Cheapest 99 Runecrafting \u2014 Lava Runes, ZMI & GOTR', url: '/guides/osrs-cheapest-99-runecrafting-2026.html', stage: 'mid', kw: 'cheapest essence gems gotr guardians lava rune runecrafting zmi' },
    { label: 'Combat Training 1-99 Beginners', url: '/guides/osrs-combat-training-beginner-2026.html', stage: 'beginner', kw: 'attack beginner beginners combat defence defense strength training' },
    { label: 'Combat Triangle Explained', url: '/guides/osrs-combat-triangle-explained-2026.html', stage: 'beginner', kw: 'attack combat defence defense magic melee ranged strength triangle' },
    { label: 'Complete Skill Training 1-99 All Skills', url: '/guides/osrs-complete-skill-training-guide-2026.html', stage: 'beginner', kw: 'methods skill skills training complete' },
    { label: 'Corrupted Gauntlet Advanced Boss Mechanics', url: '/guides/osrs-corrupted-gauntlet-advanced-guide-2026.html', stage: 'boss', kw: 'advanced boss corrupted crystal gauntlet hunllef strategy deathless' },
    { label: 'Corrupted Gauntlet \u2014 Budget Setup & Strategy', url: '/guides/osrs-corrupted-gauntlet-guide-2026.html', stage: 'boss', kw: 'budget corrupted crystal gauntlet hunllef setup strategy' },
    { label: 'Dagannoth Kings DKs Solo/Duo/Tribrid', url: '/guides/osrs-dagannoth-kings-guide-2026.html', stage: 'boss', kw: 'dagannoth dks kings rex ring solo strategy tribrid farming' },
    { label: 'Desert Treasure Quest \u2014 Low Level', url: '/guides/osrs-desert-treasure-quest-guide-low-level.html', stage: 'beginner', kw: 'ancient desert diary quest questing requirements treasure bosses' },
    { label: 'Efficient Training Routes Beginners', url: '/guides/osrs-efficient-training-routes-beginners-2026.html', stage: 'beginner', kw: 'beginner beginners efficient routes training' },
    { label: 'F2P Combat Training Level 3-30+', url: '/guides/osrs-f2p-combat-training-guide-2026.html', stage: 'beginner', kw: 'attack combat defence defense f2p free play strength training' },
    { label: 'F2P Ironman Money Making Early Game', url: '/guides/osrs-f2p-ironman-money-making-early-game.html', stage: 'beginner', kw: 'alching cowhides crafting f2p flip flipping free gp iron ironman ironmen money profit' },
    { label: 'F2P Money Making No Stats Required', url: '/guides/osrs-f2p-money-making-no-stats.html', stage: 'beginner', kw: 'f2p flip flipping free gp money methods profit stats' },
    { label: 'F2P to P2P Membership When & How', url: '/guides/osrs-f2p-to-p2p-membership-guide-2026.html', stage: 'beginner', kw: 'f2p free member membership p2p' },
    { label: 'Fastest 1-99 Crafting', url: '/guides/osrs-fastest-1-99-crafting-guide-2026.html', stage: 'mid', kw: 'battlestaff crafting gems jewelry' },
    { label: 'Fastest 99 Attack/Strength/Defence \u2014 NMZ & Crabs', url: '/guides/osrs-fastest-99-attack-strength-defence.html', stage: 'mid', kw: 'attack crabs defence fastest methods nmz strength xp' },
    { label: 'Fastest 99 Cooking F2P \u2014 Wines & Karambwans', url: '/guides/osrs-fastest-99-cooking-f2p.html', stage: 'beginner', kw: 'budget cooking f2p food karambwan methods wine' },
    { label: 'Fighter Torso & Barbarian Assault', url: '/guides/osrs-fighter-torso-barbarian-assault-guide-2026.html', stage: 'mid', kw: 'assault barbarian fighter queen role strategies torso' },
    { label: 'Fire Cape \u2014 Jad Strategy & Fight Caves', url: '/guides/osrs-fire-cape-jad-guide-2026.html', stage: 'mid', kw: 'budget cape caves fight fire jad setup strategy tzhaar walkthrough' },
    { label: 'Fire Cape to Infernal Cape Progression', url: '/guides/osrs-fire-cape-to-infernal-progression-2026.html', stage: 'boss', kw: 'cape fire infernal inferno progression pvm zuk' },
    { label: 'First 100M GP Mid Level to Wealthy', url: '/guides/osrs-first-100m-gp-mid-level-2026.html', stage: 'mid', kw: 'gp intermediate mid game money wealthy' },
    { label: 'First Week Progression Day-by-Day', url: '/guides/osrs-first-week-progression-guide-2026.html', stage: 'beginner', kw: 'week progression' },
    { label: 'Gauntlet & PvM Meta Changes Post-Sweep-Up', url: '/guides/osrs-gauntlet-meta-changes-2026.html', stage: 'boss', kw: 'changes corrupted crystal gauntlet hunllef meta pvm' },
    { label: 'Gear for Beginners \u2014 Equipment at Every Level', url: '/guides/osrs-gear-beginner-guide-2026.html', stage: 'beginner', kw: 'armor armour beginner equipment gear level weapon' },
    { label: 'Gear Upgrade Priority Order Mid to High', url: '/guides/osrs-gear-upgrade-priority-order-2026.html', stage: 'mid', kw: 'armor armour equipment gear order priority upgrade weapon' },
    { label: 'Goraik Quest Walkthrough', url: '/guides/osrs-goraik-quest-guide-2026.html', stage: 'mid', kw: 'goraik quest questing varlamore walkthrough diary' },
    { label: 'Goraik Rewards Worth It?', url: '/guides/osrs-goraik-rewards-worth-it-2026.html', stage: 'mid', kw: 'analysis goraik rewards varlamore worth' },
    { label: 'Grotesque Guardians \u2014 Dawn & Dusk Low Stats', url: '/guides/osrs-grotesque-guardians-guide-low-stats.html', stage: 'boss', kw: 'dawn dusk gargoyle grotesque guardians stats strategy' },
    { label: 'Guardians of the Rift \u2014 Fast Runecrafting', url: '/guides/osrs-guardians-of-the-rift-guide-2026.html', stage: 'mid', kw: 'guardians rewards rift runecrafting strategy' },
    { label: 'Herb Run Mastery \u2014 Passive Millions', url: '/guides/osrs-herb-run-mastery-guide-2026.html', stage: 'mid', kw: 'herb mastery patches profit routes' },
    { label: 'How to Beat Zulrah \u2014 Full Rotation for Beginners', url: '/guides/osrs-how-to-beat-zulrah-beginners-rotation.html', stage: 'boss', kw: 'beat beginner gp poison rotation snake zulrah' },
    { label: 'Fremennik Trials Quest', url: '/guides/osrs-how-to-complete-fremennik-trials-guide.html', stage: 'beginner', kw: 'fremennik helm neitiznot trials' },
    { label: 'Lost City Quest \u2014 Dramen Staff & Fairy Rings', url: '/guides/osrs-how-to-complete-lost-city-guide.html', stage: 'beginner', kw: 'city dramen fairy lost quest rings staff' },
    { label: 'Monkey Madness Quest Walkthrough', url: '/guides/osrs-how-to-complete-monkey-madness-quest.html', stage: 'mid', kw: 'madness monkey quest walkthrough diary' },
    { label: 'Corporeal Beast Loot Table & Strategy', url: '/guides/osrs-how-to-fight-corporal-beast-loot-guide.html', stage: 'boss', kw: 'beast corporeal loot setup solo strategy table' },
    { label: 'Dragon Slayer 2 \u2014 Full Quest Walkthrough', url: '/guides/osrs-how-to-finish-dragon-slayer-2-guide.html', stage: 'boss', kw: 'dragon slayer ds2 block master task vorkath' },
    { label: 'Flip Items for Profit Mid Game', url: '/guides/osrs-how-to-flip-items-profit-mid-game.html', stage: 'mid', kw: 'capital flip flipping ge intermediate mid game profit' },
    { label: 'How to Get 99 Agility Fast', url: '/guides/osrs-how-to-get-99-agility-fast-2026.html', stage: 'mid', kw: 'agility course graceful rooftop' },
    { label: 'How to Get 99 Fishing AFK Method', url: '/guides/osrs-how-to-get-99-fishing-afk-method.html', stage: 'mid', kw: 'afk fish fishing harpoon net' },
    { label: 'Dragon Defender \u2014 Warriors Guild', url: '/guides/osrs-how-to-get-dragon-defender-2026.html', stage: 'beginner', kw: 'defender dragon guild warrior' },
    { label: 'Graceful Outfit \u2014 Marks of Grace Fastest Route', url: '/guides/osrs-how-to-get-graceful-outfit-full-guide.html', stage: 'beginner', kw: 'grace graceful marks outfit recolors route' },
    { label: 'House Teleport Tablet', url: '/guides/osrs-how-to-get-house-teleport-tablet.html', stage: 'beginner', kw: 'house tablet teleport' },
    { label: 'Rune Pouch \u2014 Slayer & NPC Contact', url: '/guides/osrs-how-to-get-rune-pouch-guide.html', stage: 'mid', kw: 'contact npc pouch rune slayer' },
    { label: 'Alchemical Hydra \u2014 Access & Profit', url: '/guides/osrs-how-to-get-to-alchemical-hydra-guide.html', stage: 'boss', kw: 'access alchemical claw hydra profit slayer' },
    { label: 'Fossil Island Quick Unlock & Activities', url: '/guides/osrs-how-to-get-to-fossil-island-quick-guide.html', stage: 'beginner', kw: 'activities fossil island quick transport unlock' },
    { label: 'Kourend Castle Quick Guide', url: '/guides/osrs-how-to-get-to-kourend-castle-quick-guide.html', stage: 'beginner', kw: 'castle kourend quick' },
    { label: 'Thermonuclear Smoke Devil \u2014 Location & Strategy', url: '/guides/osrs-how-to-get-to-thermonuclear-smoke-devil.html', stage: 'boss', kw: 'boss devil gear location smoke strategy thermonuclear' },
    { label: 'Increase Slayer Points Fast \u2014 9+1 Method', url: '/guides/osrs-how-to-increase-slayer-points-fast.html', stage: 'mid', kw: 'block increase master masters method points slayer task' },
    { label: 'Crafling Money Making Low Level', url: '/guides/osrs-how-to-make-money-with-crafting-low-level.html', stage: 'mid', kw: 'battlestaff crafting flip flipping gems gp make money profit' },
    { label: 'Make Money with Zulrah \u2014 GP/Kill & Rotations', url: '/guides/osrs-how-to-make-money-with-zulrah.html', stage: 'boss', kw: 'budget flip flipping gp kill money poison profit rotation snake zulrah' },
    { label: 'Reclaim Twisted Bow When Lost', url: '/guides/osrs-how-to-reclaim-twisted-bow-when-lost.html', stage: 'boss', kw: 'bow death lost mechanics reclaim recovery twisted' },
    { label: 'Rune Spinning Profit \u2014 Flax to Bowstrings', url: '/guides/osrs-how-to-rune-spinning-profit-2026.html', stage: 'beginner', kw: 'bowstrings flax gp locations profit rune spinning' },
    { label: 'Solo God Wars Boss for Beginners \u2014 Bandos & Armadyl', url: '/guides/osrs-how-to-solo-god-wars-boss-for-beginners.html', stage: 'beginner', kw: 'armadyl bandos beginner boss bosses god pvm solo wars' },
    { label: 'Train Prayer Cheap F2P \u2014 Big Bones & Ectofuntus', url: '/guides/osrs-how-to-train-prayer-cheap-f2p.html', stage: 'beginner', kw: 'altar bones cheap ectofuntus f2p gilded prayer train' },
    { label: 'Unlock Dinosaur Hunting \u2014 Fossil Island Hunter', url: '/guides/osrs-how-to-unlock-dinosaur-hunting-osrs.html', stage: 'beginner', kw: 'dinosaur fossil herbiboar hunter hunting island unlock' },
    { label: 'Unlock Fairy Rings \u2014 Lost City & Fairy Tale', url: '/guides/osrs-how-to-unlock-fairy-rings.html', stage: 'beginner', kw: 'fairy lost city rings tale unlock' },
    { label: 'Unlock the Abyss', url: '/guides/osrs-how-to-unlock-the-abyss-guide.html', stage: 'beginner', kw: 'abyss unlock' },
    { label: 'Hunter Money Making \u2014 Black/Red Chins & Herbiboar', url: '/guides/osrs-hunter-money-making-guide-2026.html', stage: 'mid', kw: 'bird chinchompa chins flip flipping gp herbiboar hunter money profit trap' },
    { label: 'Hunter Training 1-99 All Methods', url: '/guides/osrs-hunter-training-guide-2026.html', stage: 'mid', kw: 'bird chinchompa hunter methods profit training trap xp' },
    { label: 'Interface & Controls Beginner', url: '/guides/osrs-interface-controls-beginner-guide-2026.html', stage: 'beginner', kw: 'beginner controls game interface ui' },
    { label: 'Ironman 1-99 Smithing', url: '/guides/osrs-ironman-1-99-smithing-guide.html', stage: 'mid', kw: 'anvil bar blast furnace iron ironman smithing' },
    { label: 'Ironman Money Making F2P', url: '/guides/osrs-ironman-money-making-f2p-2026.html', stage: 'beginner', kw: 'f2p flip flipping free gp iron ironman money profit' },
    { label: 'Kalphite Queen KQ Beginner \u2014 Stop Dying!', url: '/guides/osrs-kalphite-queen-kq-beginner-guide-2026.html', stage: 'beginner', kw: 'beginner kalphite kq queen' },
    { label: 'Khopesh \u2014 How to Get & Worth It?', url: '/guides/osrs-khopesh-guide-2026.html', stage: 'mid', kw: 'khopesh melee worth' },
    { label: 'Khopesh vs Alternative Weapons Comparison', url: '/guides/osrs-khopesh-vs-alternative-weapons-2026.html', stage: 'mid', kw: 'comparison gear khopesh melee weapons' },
    { label: 'Killing Green Dragons 400K-800K GP/hr', url: '/guides/osrs-killing-green-dragons-money-per-hour.html', stage: 'beginner', kw: 'dragons flip flipping gp green killing money profit wilderness' },
    { label: 'Low Cost 1-99 Herblore', url: '/guides/osrs-low-cost-1-99-herblore-guide.html', stage: 'mid', kw: 'herb herblore potion' },
    { label: 'Low Effort Money Making Beginners 10 Methods', url: '/guides/osrs-low-effort-money-making-beginners.html', stage: 'beginner', kw: 'beginner effort flip flipping gp money profit stats' },
    { label: 'Low Gear Vorkath \u2014 Budget Setup & Woox Walk', url: '/guides/osrs-low-gear-setup-vorkath-guide.html', stage: 'boss', kw: 'armor armour budget dragon equipment gear kill profit setup undead vorkath walk woox' },
    { label: 'Maps & Fast Travel \u2014 Navigate Gielinor', url: '/guides/osrs-maps-travel-guide-2026.html', stage: 'mid', kw: 'map maps navigate teleport transport travel' },
    { label: 'Maxing \u2014 Which 99 First? Optimal Order', url: '/guides/osrs-maxing-99-order-guide-2026.html', stage: 'mid', kw: 'maxing order optimal' },
    { label: 'Membership \u2014 Is It Worth Buying?', url: '/guides/osrs-membership-guide-2026.html', stage: 'beginner', kw: 'members membership worth f2p p2p comparison' },
    { label: 'Mid-Game Breakthrough \u2014 Stop Being Stuck', url: '/guides/osrs-mid-game-breakthrough-guide-2026.html', stage: 'mid', kw: 'breakthrough intermediate mid game progress stuck' },
    { label: 'Mid Level Bossing Ladder \u2014 First 10 Bosses', url: '/guides/osrs-mid-level-bossing-ladder-2026.html', stage: 'mid', kw: 'boss bosses bossing intermediate mid level order pvm' },
    { label: 'Mid to High Level Progression Roadmap', url: '/guides/osrs-mid-to-high-progression-roadmap-2026.html', stage: 'mid', kw: 'advanced endgame high intermediate mid progression roadmap' },
    { label: 'Mobile Membership Purchase Android & iOS', url: '/guides/osrs-mobile-membership-guide-2026.html', stage: 'beginner', kw: 'android ios membership mobile purchase' },
    { label: 'Money Making Beginners \u2014 0 GP to 500K', url: '/guides/osrs-money-making-beginner-2026.html', stage: 'beginner', kw: 'beginner flip flipping gp money profit zero' },
    { label: 'Money Making with Fishing \u2014 Lobsters to Eels', url: '/guides/osrs-money-making-fishing-2026.html', stage: 'mid', kw: 'eels fish fishing flip flipping gp lobster money net profit' },
    { label: 'Money Making Tier List \u2014 All Methods Ranked', url: '/guides/osrs-money-making-tier-list-2026.html', stage: 'mid', kw: 'flip flipping gp money methods profit ranked' },
    { label: 'New Player Handbook \u2014 Zero to Bossing', url: '/guides/osrs-new-player-guide-2026.html', stage: 'beginner', kw: 'beginner bossing player zero' },
    { label: 'Nex \u2014 Strategy, Gear & Loot Table', url: '/guides/osrs-nex-guide-2026.html', stage: 'mid', kw: 'god wars gear loot nex setup strategy zaros' },
    { label: 'Nightmare & Phosanis \u2014 Curse Flicking & Inquisitor', url: '/guides/osrs-nightmare-phosanis-guide-2026.html', stage: 'boss', kw: 'curse flicking inquisitor nightmare phosani sleepwalker' },
    { label: 'Optimal Leveling \u2014 Maximize XP/Hour', url: '/guides/osrs-optimal-leveling-guide-2026.html', stage: 'mid', kw: 'leveling maximize optimal xp skill' },
    { label: 'Passive Money Making \u2014 Earn GP Overnight', url: '/guides/osrs-passive-money-making-offline.html', stage: 'mid', kw: 'flip flipping gp herbs kingdom money offline overnight passive profit' },
    { label: 'Pest Control & Void Knight \u2014 Full Void Set', url: '/guides/osrs-pest-control-void-guide-2026.html', stage: 'mid', kw: 'control knight pest void xp strategy' },
    { label: 'Phantom Muspah \u2014 Boss Strategy & Profit', url: '/guides/osrs-phantom-muspah-guide-2026.html', stage: 'boss', kw: 'ancient boss gear muspah phantom profit setup strategy' },
    { label: 'POH Optimal Layout \u2014 Best House for PvM', url: '/guides/osrs-poh-optimal-layout-guide-2026.html', stage: 'mid', kw: 'house layout poh pvm skilling' },
    { label: 'Prayer Training Beginners \u2014 Protect Prayers', url: '/guides/osrs-prayer-training-beginner-guide-2026.html', stage: 'beginner', kw: 'altar beginner bones efficient gilded prayer prayers protect training' },
    { label: 'Questing Beginners \u2014 Best Starter Quests', url: '/guides/osrs-questing-beginner-guide-2026.html', stage: 'beginner', kw: 'beginner diary quest questing quests rewards starter' },
    { label: 'Raid Entry Requirements \u2014 CoX/ToB/ToA', url: '/guides/osrs-raid-entry-requirements-2026.html', stage: 'mid', kw: 'amascut chambers raid requirements theatre tombs xeric' },
    { label: 'Range Training 1-99 Fastest', url: '/guides/osrs-range-training-1-99-guide-2026.html', stage: 'mid', kw: 'arrow bow crossbow range ranged training' },
    { label: 'Regional Worlds \u2014 Japan/Singapore/South Africa', url: '/guides/osrs-regional-worlds-guide-2026.html', stage: 'beginner', kw: 'regional servers singapore south worlds' },
    { label: 'Royal Titans \u2014 Duo Boss & Deadeye Prayers', url: '/guides/osrs-royal-titans-guide-2026.html', stage: 'boss', kw: 'boss deadeye duo loot prayers royal titans vigor' },
    { label: 'RuneLite Setup \u2014 Better Than Steam!', url: '/guides/osrs-runelite-setup-guide-2026.html', stage: 'beginner', kw: 'runelite setup steam' },
    { label: 'Safe Spots Beginners \u2014 Fight Without Taking Damage', url: '/guides/osrs-safe-spots-beginner-2026.html', stage: 'beginner', kw: 'beginner damage fight safe spots without' },
    { label: 'Sailing 1-99 Complete \u2014 Fastest Routes & AFK', url: '/guides/osrs-sailing-1-99-guide-2026.html', stage: 'mid', kw: 'afk boat crew naval profit routes sailing ship training' },
    { label: 'Sailing AFK \u2014 Shipwreck Salvaging 1-99', url: '/guides/osrs-sailing-afk-training-guide-2026.html', stage: 'mid', kw: 'afk boat crew naval sailing salvaging ship shipwreck training' },
    { label: 'Sailing Money Making \u2014 GP/hr Ranked', url: '/guides/osrs-sailing-money-making-guide-2026.html', stage: 'mid', kw: 'boat crew flip flipping gp money naval profit ranked sailing ship' },
    { label: 'Sailing Ship Upgrades & Crew \u2014 Best Boats & Setup', url: '/guides/osrs-sailing-ship-crew-guide-2026.html', stage: 'mid', kw: 'boat boats crew facilities naval sailing setup ship upgrades' },
    { label: 'Sailing & Wyrmscraig Preview \u2014 Everything We Know', url: '/guides/osrs-sailing-wyrmscraig-guide-2026.html', stage: 'mid', kw: 'boat crew naval preview sailing ship wyrmscraig' },
    { label: 'Sarachnis Loot Ironman \u2014 Cudgel & Seeds', url: '/guides/osrs-sarachnis-loot-guide-for-ironman.html', stage: 'mid', kw: 'cudgel gear iron ironman loot sarachnis seeds spider' },
    { label: 'Sarachnis Solo \u2014 Best Beginner Boss', url: '/guides/osrs-sarachnis-solo-guide-2026.html', stage: 'beginner', kw: 'beginner boss cudgel sarachnis solo spider' },
    { label: 'Skills Overview Beginners \u2014 All 23 Skills', url: '/guides/osrs-skills-overview-beginner-2026.html', stage: 'beginner', kw: 'beginner overview skills' },
    { label: 'Skill Progression Path Optimal Route', url: '/guides/osrs-skills-progression-path-2026.html', stage: 'mid', kw: 'path progression route skill' },
    { label: 'Slayer 70-95 Money Making Best Tasks', url: '/guides/osrs-slayer-70-to-95-money-makers-2026.html', stage: 'mid', kw: 'block flip flipping gp making master money profit slayer task xp' },
    { label: 'Slayer Block & Skip List Optimal Tasks', url: '/guides/osrs-slayer-block-skip-list-2026.html', stage: 'mid', kw: 'block gp master masters skip slayer task xp' },
    { label: 'Summer Sweep-Up \u2014 Rebuild Account Strategy', url: '/guides/osrs-summer-sweep-up-2026-account-guide.html', stage: 'mid', kw: 'account authenticator bank rebuild security summer sweep update' },
    { label: 'Summer Sweep-Up Complete \u2014 Gauntlet & Meta Changes', url: '/guides/osrs-summer-sweep-up-2026-guide.html', stage: 'mid', kw: 'changes gauntlet gear meta rebuild summer sweep' },
    { label: 'Tempoross \u2014 Fishing Boss Strategy & Rewards', url: '/guides/osrs-tempoross-guide-2026.html', stage: 'mid', kw: 'boss fishing rates rewards strategy tempoross xp' },
    { label: 'Theatre of Blood \u2014 Complete ToB Walkthrough', url: '/guides/osrs-theatre-of-blood-guide-2026.html', stage: 'boss', kw: 'blood rooms scythe theatre tob verzik walkthrough' },
    { label: 'ToA Solo Beginner \u2014 Tombs of Amascut 0-150 Invo', url: '/guides/osrs-toa-solo-beginner-guide-2026.html', stage: 'boss', kw: 'amascut beginner invo solo toa tombs' },
    { label: 'Wintertodt Complete \u2014 Fast 99 Firemaking', url: '/guides/osrs-wintertodt-complete-guide-2026.html', stage: 'mid', kw: 'firemaking mass profit solo strategy wintertodt' },
    { label: 'Wintertodt Money Making Per Hour', url: '/guides/osrs-wintertodt-money-making-per-hour.html', stage: 'mid', kw: 'crates firemaking flip flipping gp money profit wintertodt' },
    { label: 'Quest Cape Roadmap \u2014 Optimal Order & Strategy', url: '/guides/quest-cape-roadmap-2026.html', stage: 'mid', kw: 'cape diary map order quest questing roadmap strategy' },
    { label: 'Sailing Skill Complete Level 1-99', url: '/guides/sailing-complete-guide-2026.html', stage: 'mid', kw: 'boat crew naval sailing ship skill' },
    { label: 'Sailing Phase 1 Training Maps & Profit Spots', url: '/guides/sailing-phase-1-training-2026.html', stage: 'mid', kw: 'boat crew maps naval phase profit sailing ship training' },
    { label: 'Sailing PvP \u2014 Naval Combat & Piracy Mechanics', url: '/guides/sailing-pvp-guide-2026.html', stage: 'mid', kw: 'boat combat crew mechanics naval piracy pvp sailing ship' },
    { label: 'Slayer Training 1-99 Best Tasks & Masters', url: '/guides/slayer-1-99-guide-2026.html', stage: 'mid', kw: 'block gp master slayer task training' },
    { label: 'Vault of Ralos Raid Walkthrough & Strategy', url: '/guides/vault-of-ralos-raid-guide-2026.html', stage: 'boss', kw: 'raid ralos strategy vault walkthrough' },
    { label: 'Skill Training \u2014 Beginner Complete Guide 2026', url: '/guides/osrs-skill-training-beginner-complete-guide-2026.html', stage: 'beginner', kw: 'beginner complete guide level 1 skill skills training' },
    { label: 'Skill Training \u2014 Beginner Fast Track 2026', url: '/guides/osrs-skill-training-beginner-fast-track-2026.html', stage: 'beginner', kw: 'beginner fast leveling shortcut skill skills track training' },
    { label: 'Skill Training \u2014 Mid-Game Guide 2026', url: '/guides/osrs-skill-training-mid-game-guide-2026.html', stage: 'mid', kw: 'efficiency method mid game skill skills training xp' },
    { label: 'Skill Training \u2014 Mid-Game Optimization 2026', url: '/guides/osrs-skill-training-mid-game-optimization-2026.html', stage: 'mid', kw: 'afk efficiency gp hr optimization profit skill skills training' },
    { label: 'Skill Training \u2014 Endgame Guide 2026', url: '/guides/osrs-skill-training-endgame-guide-2026.html', stage: 'mid', kw: 'endgame fast level 80 99 max skill skills tick training' },
    { label: 'Skill Training \u2014 Max Account Ultimate 2026', url: '/guides/osrs-skill-training-max-account-2026.html', stage: 'mid', kw: '2277 all 99 complete guide max skill skills total ultimate' },
    { label: 'Money Making Summer Sweep-Up 2026', url: '/guides/osrs-money-making-summer-sweep-up-2026.html', stage: 'mid', kw: 'gold gp making money profit summer sweep' },
    { label: 'Money Making Under 1M Investment 2026', url: '/guides/osrs-money-making-under-1m-investment-2026.html', stage: 'beginner', kw: 'budget cheap gp investment low making money one million under' },
    { label: 'Slayer Beginner First Master Guide 2026', url: '/guides/osrs-slayer-beginner-first-master-guide-2026.html', stage: 'beginner', kw: 'beginner first guide master slayer task turael vannaka' },
    { label: 'Slayer Low-Level Money Makers 2026', url: '/guides/osrs-slayer-low-level-money-makers-2026.html', stage: 'beginner', kw: 'gold gp guide low level making money slayer' },
    { label: 'Combat Achievements Easy Walkthrough 2026', url: '/guides/osrs-combat-achievements-easy-walkthrough-2026.html', stage: 'beginner', kw: 'achievement ca combat easy ghommal hilt task walkthrough' },
    { label: 'Ghommal Hilt Fast Guide 2026', url: '/guides/osrs-ghommal-hilt-fast-guide-2026.html', stage: 'mid', kw: 'achievement ca combat fast ghommal hilt teleport unlock' },
    { label: 'First Boss Progression Roadmap 2026', url: '/guides/osrs-first-boss-progression-roadmap-2026.html', stage: 'beginner', kw: 'boss bryophyta first obor order progression pvm roadmap' },
    { label: 'Obor & Bryophyta F2P Boss Guide 2026', url: '/guides/osrs-obor-bryophyta-f2p-boss-guide-2026.html', stage: 'beginner', kw: 'boss bryophyta f2p free giant hill moss obor play' },
    { label: 'Returning Player Catch-Up Guide 2026', url: '/guides/osrs-returning-player-catch-up-guide-2026.html', stage: 'beginner', kw: '2026 back break catch coming guide returning up' },
    { label: 'Returning Player Fast Track 2026', url: '/guides/osrs-returning-player-fast-track-2026.html', stage: 'mid', kw: '2026 fast gear guide progression returning route track' },
    { label: 'Achievement Diary Priority Order Beginner 2026', url: '/guides/osrs-diary-priority-order-beginner-2026.html', stage: 'beginner', kw: 'achievement beginner diary easy first order priority task' },
    { label: 'Achievement Diary Easy & Medium Complete 2026', url: '/guides/osrs-diary-easy-medium-complete-guide-2026.html', stage: 'mid', kw: 'achievement complete diary easy medium requirement reward task' },
    { label: 'Skill Training After Sweep-Up 2026', url: '/guides/osrs-skill-training-after-sweep-up-2026.html', stage: 'mid', kw: 'after guide meta new skill sweep training update' },
    { label: 'Top 10 Skills to Train First 2026', url: '/guides/osrs-top-10-skills-to-train-first-2026.html', stage: 'beginner', kw: 'best first priority skills ten to top train training' },
    { label: 'Blood Moon Rises Prep Checklist Detailed 2026', url: '/guides/osrs-blood-moon-rises-prep-checklist-detailed-2026.html', stage: 'mid', kw: 'blood checklist guide moon prepared quest requirement rises' },
    { label: 'Best Quests Per Skill 2026', url: '/guides/osrs-best-quests-per-skill-2026.html', stage: 'mid', kw: 'best cape experience per quest quests reward skill xp' },
    { label: 'Slayer Money Making Guide 2026 — Best Tasks & GP/hr', url: '/guides/osrs-slayer-money-making-guide-2026.html', stage: 'mid', kw: 'block list skip slayer monetary task gp per hour profit' },
    { label: 'Boss Profit Comparison 2026 — All Bosses Ranked by GP', url: '/guides/osrs-boss-profit-comparison-2026.html', stage: 'boss', kw: 'bosses comparison gp per kill profit ranked ranking tier' },
    { label: 'GE Flipping Guide for Beginners 2026 — Start With 100K', url: '/guides/osrs-flipping-guide-beginners-2026.html', stage: 'beginner', kw: 'beginner capital flip flipping ge guide low margin profit' },
    { label: 'Mid-Game Money Making Roadmap 2026 — Combat 60-100', url: '/guides/osrs-mid-game-money-making-roadmap-2026.html', stage: 'mid', kw: '60 100 combat intermediate middle game roadmap making money' },
    { label: 'AFK Money Making Ultimate Guide 2026 — 20+ Low-Attention Methods', url: '/guides/osrs-afk-money-making-ultimate-guide-2026.html', stage: 'mid', kw: 'afk attention low afkable idle passive second screen methods' },
    { label: 'Daily & Weekly Money Routine 2026 — Maximize Passive Income', url: '/guides/osrs-daily-weekly-money-routine-2026.html', stage: 'mid', kw: 'daily weekly routine birdhouse herb run kingdom miscellania staves' },
    { label: 'Quest-Unlocked Money Methods 2026 — Best Quests for GP', url: '/guides/osrs-quest-unlocked-money-methods-2026.html', stage: 'mid', kw: 'dragon slayer ii ds2 sote song elves quests unlock gp methods' },
    { label: 'Wilderness Money Making Guide 2026 — High Risk High Reward', url: '/guides/osrs-wilderness-money-making-2026.html', stage: 'mid', kw: 'wilderness pvp pk risk revs revenant lava dragon black chin' },
    { label: 'Ironman P2P Money Making Guide 2026 — Mid-Game Gold', url: '/guides/osrs-ironman-p2p-money-making-2026.html', stage: 'mid', kw: 'ironman iron ironmen p2p mid game gold self sufficient alchemy' },
    { label: 'Skilling Money Post-Sailing Update 2026 — All Profitable Skills', url: '/guides/osrs-skilling-money-post-sailing-2026.html', stage: 'mid', kw: 'mining runecrafting hunter farming fishing woodcutting sailing post update profit' },
    { label: 'Combat Money Making Non-Boss 2026 — Monsters That Drop GP', url: '/guides/osrs-combat-money-making-non-boss-2026.html', stage: 'beginner', kw: 'monster non boss combat dragon brutal gargoyle wyvern rune' },
    { label: 'How to Spend Your GP Wisely 2026 — Best Investments Per Budget', url: '/guides/osrs-how-to-spend-gp-wisely-2026.html', stage: 'mid', kw: 'budget gold gp investment roi spend wisely gear upgrade priority' },
  ];

  // ========== 本地文章匹配（CD/Windrose/OSRS 通用） ==========
  function matchLocalArticles(question, game) {
    var articles;
    if (game === 'crimson-desert') articles = CD_ARTICLES;
    else if (game === 'windrose') articles = WINDROSE_ARTICLES;
    else articles = OSRS_ARTICLES;

    var lowerQ = question.toLowerCase();
    var matches = [];

    // 常见拼写纠错映射
    var typos = {
      'palyer': 'player', 'playr': 'player', 'plaer': 'player',
      'beginer': 'beginner', 'begineer': 'beginner',
      'wepon': 'weapon', 'weapn': 'weapon', 'wpn': 'weapon',
      'bosse': 'boss', 'bss': 'boss',
      'comba': 'combat', 'cmbat': 'combat',
      'questt': 'quest', 'qust': 'quest',
      'guilde': 'guide', 'guid': 'guide',
      'startt': 'start', 'stat': 'start', 'strt': 'start',
      'howto': 'how to', 'howdoi': 'how do i', 'du': 'do', 'waht': 'what', 'whats': "what's",
      'crimson': 'crimson desert', 'desert': 'crimson desert',
      'windros': 'windrose', 'windose': 'windrose', 'windroses': 'windrose',
      'zulrah': 'zulrah', 'vorkath': 'vorkath', 'corp': 'corporeal',
      'tob': 'theatre of blood', 'cox': 'chambers of xeric', 'toa': 'tombs of amascut',
      'gauntlet': 'gauntlet', 'cg': 'corrupted gauntlet',
    };

    var cleanedQ = lowerQ;
    for (var typo in typos) {
      if (cleanedQ.indexOf(typo) !== -1) {
        cleanedQ = cleanedQ.replace(new RegExp(typo, 'g'), typos[typo]);
      }
    }
    var searchQ = lowerQ + ' ' + cleanedQ;

    for (var i = 0; i < articles.length; i++) {
      var score = 0;
      var keywords = (articles[i].kw || articles[i].keywords).split(' ');
      var titleLower = (articles[i].label || articles[i].title).toLowerCase();

      for (var k = 0; k < keywords.length; k++) {
        if (searchQ.indexOf(keywords[k]) !== -1) {
          score += (keywords[k].length > 4 ? 3 : 1);
        }
      }

      var titleWords = titleLower.replace(/osrs |guide |2026|beginner| /g, ' ').split(' ');
      for (var w = 0; w < titleWords.length; w++) {
        if (titleWords[w].length > 2 && searchQ.indexOf(titleWords[w]) !== -1) {
          score += 2;
        }
      }

      if (score > 0) {
        // 找最佳锚点
        var bestAnchor = '';
        if (articles[i].anchorMap) {
          for (var key in articles[i].anchorMap) {
            if (searchQ.indexOf(key) !== -1 && articles[i].anchorMap[key]) {
              bestAnchor = articles[i].anchorMap[key];
              break;
            }
          }
        }
        matches.push({ article: articles[i], score: score, anchor: bestAnchor });
      }
    }

    matches.sort(function(a, b) { return b.score - a.score; });
    // v2.9: 返回更多候选，确保 OSRS 阶段分组每阶段至少有1篇
    return matches.slice(0, 12);
  }

  // ========== CSS 注入 ==========
  function injectStyles() {
    var style = document.createElement('style');
    style.textContent = 
      '#osrs-qa-widget{position:fixed;bottom:20px;right:20px;width:420px;max-height:600px;background:linear-gradient(135deg,rgba(39,33,26,0.98),rgba(59,38,21,0.95));border:2px solid rgba(212,175,55,0.4);border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 20px rgba(212,175,55,0.15);display:none;flex-direction:column;z-index:10000;font-family:"Segoe UI",Tahoma,Geneva,sans-serif;overflow:hidden;}' +
      '#osrs-qa-widget.open{display:flex;animation:qaSlideUp 0.3s ease-out;}' +
      '@keyframes qaSlideUp{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}' +
      '#osrs-qa-widget .qa-header{background:linear-gradient(90deg,rgba(212,175,55,0.15),rgba(212,175,55,0.08));border-bottom:1px solid rgba(212,175,55,0.25);padding:16px 18px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}' +
      '#osrs-qa-widget .qa-header-title{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;color:#d4af37;font-family:"Cinzel",serif;}' +
      '#osrs-qa-widget .qa-close-btn{background:none;border:none;color:rgba(212,175,55,0.6);font-size:20px;cursor:pointer;padding:4px;transition:color 0.2s;}' +
      '#osrs-qa-widget .qa-close-btn:hover{color:#d4af37;}' +
      '#osrs-qa-widget .qa-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;}' +
      '#osrs-qa-widget .qa-message{display:flex;gap:8px;animation:qaFadeIn 0.3s ease-out;}' +
      '@keyframes qaFadeIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}' +
      '#osrs-qa-widget .qa-message.user{justify-content:flex-end;}' +
      '#osrs-qa-widget .qa-message.assistant{justify-content:flex-start;}' +
      '#osrs-qa-widget .qa-message-bubble{max-width:85%;padding:10px 14px;border-radius:8px;font-size:13px;line-height:1.5;word-wrap:break-word;}' +
      '#osrs-qa-widget .qa-message.user .qa-message-bubble{background:rgba(212,175,55,0.25);border:1px solid rgba(212,175,55,0.35);color:#e8d5b7;}' +
      '#osrs-qa-widget .qa-message.assistant .qa-message-bubble{background:rgba(100,80,60,0.4);border:1px solid rgba(212,175,55,0.2);color:#d4af37;}' +
      '#osrs-qa-widget .qa-message.assistant .qa-message-bubble.loading{display:flex;align-items:center;gap:6px;min-height:24px;}' +
      '#osrs-qa-widget .qa-source{font-size:11px;color:rgba(212,175,55,0.6);margin-top:4px;font-style:italic;}' +
      '#osrs-qa-widget .qa-input-group{border-top:1px solid rgba(212,175,55,0.2);padding:12px;background:rgba(0,0,0,0.2);display:flex;gap:8px;flex-shrink:0;}' +
      '#osrs-qa-widget .qa-input-group input{flex:1;background:rgba(59,38,21,0.6);border:1px solid rgba(212,175,55,0.25);border-radius:6px;padding:8px 12px;color:#d4af37;font-size:13px;font-family:inherit;transition:border-color 0.2s;}' +
      '#osrs-qa-widget .qa-input-group input::placeholder{color:rgba(212,175,55,0.4);}' +
      '#osrs-qa-widget .qa-input-group input:focus{outline:none;border-color:rgba(212,175,55,0.5);background:rgba(59,38,21,0.8);}' +
      '#osrs-qa-widget .qa-send-btn{background:linear-gradient(135deg,rgba(212,175,55,0.35),rgba(212,175,55,0.2));border:1px solid rgba(212,175,55,0.4);border-radius:6px;color:#d4af37;font-size:15px;cursor:pointer;padding:6px 12px;transition:all 0.2s;font-weight:600;}' +
      '#osrs-qa-widget .qa-send-btn:hover:not(:disabled){background:linear-gradient(135deg,rgba(212,175,55,0.5),rgba(212,175,55,0.35));border-color:rgba(212,175,55,0.6);transform:scale(1.02);}' +
      '#osrs-qa-widget .qa-send-btn:disabled{opacity:0.5;cursor:not-allowed;}' +
      '#osrs-qa-toggle-btn{position:fixed;top:50%;transform:translateY(-50%);right:20px;width:100px;height:108px;background:#4A90D9;border:none;border-radius:42% 42% 50% 50% / 44% 44% 58% 58%;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999;transition:all 0.3s ease;box-shadow:0 4px 24px rgba(74,144,217,0.55);gap:0;outline:none;padding:0;color:#fff;animation:aiFloat 3s ease-in-out infinite;}' +
      '#osrs-qa-toggle-btn .peach-face{display:flex;flex-direction:column;align-items:center;gap:5px;}' +
      '#osrs-qa-toggle-btn .peach-eyes{display:flex;gap:14px;}' +
      '#osrs-qa-toggle-btn .peach-eyes span{display:block;width:10px;height:11px;background:#1a3a5c;border-radius:50%;}' +
      '#osrs-qa-toggle-btn .peach-mouth{width:22px;height:10px;border-bottom:2.5px solid #1a3a5c;border-radius:0 0 14px 14px;}' +
      '#osrs-qa-toggle-btn .ai-label{font-size:15px;font-weight:700;color:#fff;letter-spacing:1px;font-family:"Segoe UI","Cinzel",sans-serif;line-height:1;margin-top:4px;}' +
      '#osrs-qa-toggle-btn:hover{transform:scale(1.07);box-shadow:0 6px 28px rgba(74,144,217,0.6);background:#5A9DE5;}' +
      '#osrs-qa-toggle-btn.hide{display:none;}' +
      '@media(max-width:600px){#osrs-qa-widget{width:100%;height:100%;max-height:100%;bottom:0;right:0;border-radius:0;max-height:80vh;}}' +
      '#osrs-qa-widget .qa-article-link{display:block;margin-top:6px;padding:8px 12px;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.25);border-radius:6px;color:#d4af37;text-decoration:none;font-size:12px;line-height:1.4;transition:all 0.2s;}' +
      '#osrs-qa-widget .qa-article-link:hover{background:rgba(212,175,55,0.2);border-color:rgba(212,175,55,0.5);}' +
      '#osrs-qa-widget .qa-article-link .qa-link-icon{margin-right:6px;}' +
      '#osrs-qa-widget .qa-toc-match{display:block;margin-top:4px;padding:6px 10px;background:rgba(212,175,55,0.08);border-left:3px solid #d4af37;border-radius:0 4px 4px 0;color:#e8d5b7;text-decoration:none;font-size:12px;line-height:1.4;transition:all 0.2s;}' +
      '#osrs-qa-widget .qa-toc-match:hover{background:rgba(212,175,55,0.15);color:#d4af37;}' +
      '#osrs-qa-widget .qa-section-label{font-size:11px;color:rgba(212,175,55,0.7);margin-top:8px;margin-bottom:2px;font-weight:600;}' +
      '#osrs-qa-widget .qa-article-link.qa-stage-beginner{border-left:3px solid #4caf50;}' +
      '#osrs-qa-widget .qa-article-link.qa-stage-mid{border-left:3px solid #ff9800;}' +
      '#osrs-qa-widget .qa-article-link.qa-stage-boss{border-left:3px solid #f44336;}' +
      '#osrs-qa-widget .qa-suggested{padding:14px 12px;border-bottom:1px solid rgba(212,175,55,0.15);margin-bottom:4px;}' +
      '#osrs-qa-widget .qa-suggested-title{font-size:12px;color:rgba(212,175,55,0.7);margin-bottom:8px;display:flex;align-items:center;gap:5px;}' +
      '#osrs-qa-widget .qa-suggested-btns{display:flex;flex-direction:column;gap:6px;}' +
      '#osrs-qa-widget .qa-suggested-btn{display:block;width:100%;text-align:left;padding:7px 11px;background:rgba(212,175,55,0.07);border:1px solid rgba(212,175,55,0.18);border-radius:6px;color:#e8d5b7;font-size:12.5px;cursor:pointer;transition:all 0.2s;font-family:inherit;}' +
      '#osrs-qa-widget .qa-suggested-btn:hover{background:rgba(212,175,55,0.16);border-color:rgba(212,175,55,0.38);color:#d4af37;}' +
      '#osrs-qa-widget .qa-article-cta{display:block;margin:28px 0 12px 0;padding:16px 18px;background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.2);border-radius:10px;text-align:center;}' +
      '#osrs-qa-widget .qa-article-cta-title{font-size:14px;color:#d4af37;font-weight:600;margin-bottom:6px;}' +
      '#osrs-qa-widget .qa-article-cta-desc{font-size:12px;color:rgba(232,213,183,0.7);margin-bottom:10px;}' +
      '#osrs-qa-widget .qa-article-cta-btn{display:inline-block;padding:8px 18px;background:linear-gradient(135deg,rgba(212,175,55,0.3),rgba(212,175,55,0.15));border:1px solid rgba(212,175,55,0.4);border-radius:6px;color:#d4af37;font-size:13px;font-weight:600;cursor:pointer;text-decoration:none;transition:all 0.2s;}' +
      '#osrs-qa-widget .qa-article-cta-btn:hover{background:linear-gradient(135deg,rgba(212,175,55,0.45),rgba(212,175,55,0.25));border-color:rgba(212,175,55,0.6);}' +
      '@keyframes aiFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}' +
      // === P0: 脉冲光环动画 ===
      '@keyframes aiPulseRing{0%{box-shadow:0 4px 24px rgba(74,144,217,0.55),0 0 0 0 rgba(255,255,255,0.8);}70%{box-shadow:0 4px 24px rgba(74,144,217,0.55),0 0 0 22px rgba(255,215,0,0);}100%{box-shadow:0 4px 24px rgba(74,144,217,0.55),0 0 0 0 rgba(255,215,0,0);}}' +
      '#osrs-qa-toggle-btn.pulse{animation:aiFloat 3s ease-in-out infinite,aiPulseRing 2s ease-out 3;}' +
      // === P0: NEW 红点徽章 ===
      '#osrs-qa-toggle-btn .peach-badge{position:absolute;top:-8px;right:-4px;background:#e74c3c;color:#fff;font-size:10px;font-weight:700;padding:3px 6px;border-radius:10px;line-height:1;letter-spacing:0.5px;box-shadow:0 2px 8px rgba(231,76,60,0.6);animation:badgeBounce 1.5s ease-in-out infinite;z-index:10000;}' +
      '@keyframes badgeBounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-3px);}}' +
      // === P1: 预览气泡 ===
      '#osrs-qa-preview-bubble{position:fixed;top:50%;right:140px;transform:translateY(-50%);background:linear-gradient(135deg,rgba(39,33,26,0.98),rgba(59,38,21,0.95));border:2px solid rgba(74,144,217,0.4);border-radius:12px;padding:12px 16px;max-width:220px;box-shadow:0 4px 20px rgba(0,0,0,0.5);z-index:9998;display:none;cursor:pointer;}' +
      '#osrs-qa-preview-bubble.show{display:block;animation:qaBubbleIn 0.4s ease-out;}' +
      '#osrs-qa-preview-bubble .bubble-title{color:#d4af37;font-size:13px;font-weight:600;}' +
      '#osrs-qa-preview-bubble .bubble-sub{color:rgba(232,213,183,0.7);font-size:11px;margin-top:4px;}' +
      '#osrs-qa-preview-bubble::after{content:"";position:absolute;right:-10px;top:50%;transform:translateY(-50%);border:8px solid transparent;border-left-color:rgba(74,144,217,0.4);}' +
      '@keyframes qaBubbleIn{from{opacity:0;transform:translateY(-50%) translateX(15px);}to{opacity:1;transform:translateY(-50%) translateX(0);}}';
      // 裁剪消息数量
      document.head.appendChild(style);
  }

  // ========== P2: 页面场景匹配引导问题 ==========
  function getSuggestedQuestions() {
    var path = window.location.pathname.toLowerCase();

    // 赚钱相关页面
    if (path.indexOf('money') !== -1 || path.indexOf('flipping') !== -1 || path.indexOf('gp') !== -1 || path.indexOf('profit') !== -1 || path.indexOf('wealth') !== -1) {
      return [
        { q: 'How to make first 1 million GP new player OSRS 2026?', label: '💰 How to make first 1M GP?' },
        { q: 'Best money making methods mid game OSRS 2026?', label: '📈 Best mid-game money methods?' },
        { q: 'What bosses are most profitable OSRS 2026?', label: '🏆 Most profitable bosses?' },
        { q: 'How to flip items on GE for profit OSRS?', label: '🔄 How to flip GE items?' },
        { q: 'Best AFK money making methods OSRS 2026?', label: '😴 Best AFK money methods?' }
      ];
    }

    // 技能训练相关页面
    if (path.indexOf('training') !== -1 || path.indexOf('1-99') !== -1 || path.indexOf('skill') !== -1 || path.indexOf('leveling') !== -1 || path.indexOf('agility') !== -1 || path.indexOf('mining') !== -1 || path.indexOf('fishing') !== -1 || path.indexOf('woodcutting') !== -1 || path.indexOf('crafting') !== -1 || path.indexOf('prayer') !== -1 || path.indexOf('magic') !== -1 || path.indexOf('hunter') !== -1 || path.indexOf('thieving') !== -1 || path.indexOf('herblore') !== -1 || path.indexOf('farming') !== -1 || path.indexOf('runecraft') !== -1 || path.indexOf('cooking') !== -1 || path.indexOf('firemaking') !== -1 || path.indexOf('smithing') !== -1) {
      return [
        { q: 'Best 1-99 training path 2026 OSRS?', label: '🗺️ Best 1-99 training path?' },
        { q: 'Fastest 99 without spending real money OSRS F2P?', label: '🎯 Fastest 99 F2P?' },
        { q: 'Cheapest 1-99 Prayer training OSRS?', label: '🙏 Cheapest 1-99 Prayer?' },
        { q: 'Best AFK training methods OSRS 2026?', label: '😴 Best AFK training?' },
        { q: 'How to get 99 Agility fast OSRS?', label: '🏃 How to get 99 Agility fast?' }
      ];
    }

    // Boss/战斗相关页面
    if (path.indexOf('boss') !== -1 || path.indexOf('combat') !== -1 || path.indexOf('zulrah') !== -1 || path.indexOf('vorkath') !== -1 || path.indexOf('gauntlet') !== -1 || path.indexOf('slayer') !== -1 || path.indexOf('pvm') !== -1 || path.indexOf('raid') !== -1 || path.indexOf('jad') !== -1 || path.indexOf('cape') !== -1 || path.indexOf('araxxor') !== -1 || path.indexOf('cerberus') !== -1 || path.indexOf('hydra') !== -1 || path.indexOf('nex') !== -1 || path.indexOf('tob') !== -1 || path.indexOf('toa') !== -1 || path.indexOf('cox') !== -1 || path.indexOf('xeric') !== -1 || path.indexOf('amascut') !== -1 || path.indexOf('blood') !== -1 || path.indexOf('dks') !== -1 || path.indexOf('dagannoth') !== -1 || path.indexOf('sarachnis') !== -1 || path.indexOf('kq') !== -1 || path.indexOf('kalphite') !== -1) {
      return [
        { q: 'What is the first boss I should kill OSRS?', label: '🥇 What boss should I kill first?' },
        { q: 'Best boss progression order for beginners OSRS?', label: '📊 Best boss progression order?' },
        { q: 'How to beat Zulrah for beginners OSRS?', label: '🐍 How to beat Zulrah?' },
        { q: 'What gear do I need for raids OSRS?', label: '⚔️ What gear for raids?' },
        { q: 'How to get Fire Cape Jad fight caves OSRS?', label: '🔥 How to get Fire Cape?' }
      ];
    }

    // 任务相关页面
    if (path.indexOf('quest') !== -1 || path.indexOf('diary') !== -1 || path.indexOf('walkthrough') !== -1) {
      return [
        { q: 'What quests should I do first OSRS beginner?', label: '📋 Best first quests?' },
        { q: 'Quest cape optimal order OSRS 2026?', label: '🗺️ Quest cape order?' },
        { q: 'Which quests unlock the best content OSRS?', label: '🔑 Best unlock quests?' },
        { q: 'How to complete Recipe for Disaster OSRS?', label: '🍳 Recipe for Disaster guide?' },
        { q: 'Best quests for XP rewards OSRS?', label: '⭐ Best XP reward quests?' }
      ];
    }

    // 会员相关页面
    if (path.indexOf('membership') !== -1 || path.indexOf('bond') !== -1 || path.indexOf('f2p') !== -1 || path.indexOf('p2p') !== -1 || path.indexOf('member') !== -1) {
      return [
        { q: 'Is OSRS membership worth it 2026 bond vs subscription?', label: '🔥 Is membership worth it?' },
        { q: 'How to buy membership with bonds OSRS?', label: '💰 How to buy with bonds?' },
        { q: 'F2P to P2P when should I upgrade OSRS?', label: '🔄 When to go P2P?' },
        { q: 'What content is members only OSRS?', label: '🔒 What\'s members only?' },
        { q: 'Best member benefits for new players OSRS?', label: '⭐ Best member benefits?' }
      ];
    }

    // 默认（首页/其他页面）
    return [
      { q: 'Best 1-99 training path 2026 OSRS?', label: '🗺️ Best 1-99 training path?' },
      { q: 'How to make first 1 million GP new player OSRS 2026?', label: '💰 How to make first 1M GP?' },
      { q: 'Is OSRS membership worth it 2026 bond vs subscription?', label: '🔥 Is membership worth it?' },
      { q: 'How to start Ironman mode OSRS beginner guide 2026?', label: '🔒 How to start Ironman?' },
      { q: 'Fastest 99 without spending real money OSRS F2P?', label: '🎯 Fastest 99 without spending?' }
    ];
  }

  // ========== HTML 结构创建 ==========
  function createWidget() {
    widget = document.createElement('div');
    widget.id = CONFIG.widgetId;
    // === P2: 动态生成场景匹配的引导问题 ===
    var suggestions = getSuggestedQuestions();
    var suggestedHTML = '<div class="qa-suggested"><div class="qa-suggested-title">💡 Try asking:</div><div class="qa-suggested-btns">';
    for (var si = 0; si < suggestions.length; si++) {
      suggestedHTML += '<button class="qa-suggested-btn" data-q="' + suggestions[si].q + '" data-force-ai="true">' + suggestions[si].label + '</button>';
    }
    suggestedHTML += '</div></div>';

    widget.innerHTML =
      '<div class="qa-header">' +
        '<div class="qa-header-title">' +
          '<span class="qa-icon">' + CONFIG.gameIcon + '</span>' +
          '<span>' + CONFIG.assistantTitle + '</span>' +
        '</div>' +
        '<button class="qa-close-btn" aria-label="Close AI widget">✕</button>' +
      '</div>' +
      '<div class="qa-messages">' + suggestedHTML + '</div>' +
      '<div class="qa-input-group">' +
        '<input type="text" class="qa-input" placeholder="' + CONFIG.inputPlaceholder + '" aria-label="Ask a question" />' +
        '<button class="qa-send-btn" aria-label="Send message">Send</button>' +
      '</div>';

    var toggleBtn = document.createElement('button');
    toggleBtn.id = CONFIG.widgetButtonId;
    // === P0: 加 NEW 红点徽章 ===
    toggleBtn.innerHTML = '<div class="peach-face"><div class="peach-eyes"><span></span><span></span></div><div class="peach-mouth"></div></div><span class="ai-label">AI</span><span class="peach-badge">NEW</span>';
    toggleBtn.style.position = 'fixed';
    toggleBtn.title = 'Open ' + CONFIG.assistantTitle;

    document.body.appendChild(widget);
    document.body.appendChild(toggleBtn);

    return { widget: widget, toggleBtn: toggleBtn };
  }

  // ========== 交互逻辑 ==========
  function setupEventHandlers(widget, toggleBtn) {
    var closeBtn = widget.querySelector('.qa-close-btn');
    sendBtn = widget.querySelector('.qa-send-btn');
    input = widget.querySelector('.qa-input');
    var messagesContainer = widget.querySelector('.qa-messages');

    toggleBtn.addEventListener('click', function() {
      widget.classList.toggle('open');
      if (widget.classList.contains('open')) input.focus();
    });

    closeBtn.addEventListener('click', function() {
      widget.classList.remove('open');
    });

    var sendMessage = function(forceAI) {
      var message = input.value.trim();
      if (!message) return;

      addMessage(messagesContainer, message, 'user');
      input.value = '';
      var suggestedEl = messagesContainer.querySelector('.qa-suggested');
      if (suggestedEl) suggestedEl.style.display = 'none';
      sendBtn.disabled = true;
      addMessage(messagesContainer, forceAI ? '🤖 Thinking...' : 'Searching...', 'assistant', true);

      // === forceAI模式：跳过本地匹配，直接调用AI后端 ===
      if (forceAI) {
        callBackendAPI(message, messagesContainer, sendBtn, GAME, [], [], true);
        return;
      }

      // === 优先：动态TOC匹配（所有页面通用） ===
      var toc = extractPageTOC();
      var tocMatches = matchTOCSections(message, toc);

      // === 本地文章匹配 ===
      var localMatches = matchLocalArticles(message, GAME);

      // 移除加载消息
      var loadingMsg = messagesContainer.lastElementChild;
      if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
        loadingMsg.remove();
      }

      // 显示TOC匹配结果（跳转到当前页面段落）
      if (tocMatches.length > 0) {
        var tocIntro = document.createElement('div');
        tocIntro.className = 'qa-message assistant';
        tocIntro.innerHTML = '<div class="qa-message-bubble">📍 <b>Found on this page:</b> Click to jump to the exact section:</div>';
        messagesContainer.appendChild(tocIntro);

        for (var t = 0; t < tocMatches.length; t++) {
          var tocLink = document.createElement('a');
          tocLink.className = 'qa-toc-match';
          tocLink.href = '#' + tocMatches[t].tocItem.id;
          tocLink.textContent = '👉 ' + tocMatches[t].tocItem.rawText;
          tocLink.addEventListener('click', function(e) {
            e.preventDefault();
            var targetId = this.getAttribute('href').substring(1);
            var target = document.getElementById(targetId);
            if (target) {
              target.scrollIntoView({ behavior: 'smooth', block: 'start' });
              // 高亮效果
              target.style.transition = 'background 0.5s';
              target.style.background = 'rgba(212,175,55,0.25)';
              setTimeout(function() { target.style.background = ''; }, 2000);
            }
            widget.classList.remove('open');
          });

          var tocMsg = document.createElement('div');
          tocMsg.className = 'qa-message assistant';
          tocMsg.appendChild(tocLink);
          messagesContainer.appendChild(tocMsg);
        }
      }

      // 显示本地文章匹配结果
      if (localMatches.length > 0) {
        if (GAME === 'osrs') {
          // === OSRS: 按阶段分组显示 ===
          var stageGroups = { 'beginner': [], 'mid': [], 'boss': [] };
          for (var i = 0; i < localMatches.length; i++) {
            var s = (localMatches[i].article.stage || 'mid');
            if (!stageGroups[s]) stageGroups[s] = [];
            stageGroups[s].push(localMatches[i]);
          }
          var stageIntro = document.createElement('div');
          stageIntro.className = 'qa-message assistant';
          stageIntro.innerHTML = '<div class="qa-message-bubble">🎯 <b>Pick your stage:</b></div>';
          messagesContainer.appendChild(stageIntro);
          var stageConfigs = [
            { key: 'beginner', emoji: '🟢', label: 'New Player' },
            { key: 'mid',       emoji: '🟡', label: 'Mid-Game' },
            { key: 'boss',      emoji: '🔴', label: 'Boss Hunter' }
          ];
          for (var si = 0; si < stageConfigs.length; si++) {
            var sc = stageConfigs[si];
            var group = stageGroups[sc.key] || [];
            if (group.length === 0) continue;
            var best = group[0];
            var article = best.article;
            var url = article.url;
            if (best.anchor) url += '#' + best.anchor;
            var displayLabel = article.label || article.title;
            var link = document.createElement('a');
            link.className = 'qa-article-link qa-stage-' + sc.key;
            link.href = url;
            link.target = '_blank';
            link.rel = 'noopener';
            link.innerHTML = '<span class="qa-link-icon">' + sc.emoji + '</span> ' + sc.label + ' → ' + displayLabel;
            var linkMsg = document.createElement('div');
            linkMsg.className = 'qa-message assistant';
            linkMsg.appendChild(link);
            messagesContainer.appendChild(linkMsg);
          }
        } else {
          // === CD/Windrose: 平铺列表 ===
          var prefixText = tocMatches.length > 0
            ? '📚 <b>Related guides:</b>'
            : 'Found the best guides for your question:';
          var articleIntro = document.createElement('div');
          articleIntro.className = 'qa-message assistant';
          articleIntro.innerHTML = '<div class="qa-message-bubble">' + prefixText + '</div>';
          messagesContainer.appendChild(articleIntro);
          for (var i = 0; i < localMatches.length; i++) {
            var article = localMatches[i].article;
            var url = article.url;
            if (localMatches[i].anchor) {
              url += '#' + localMatches[i].anchor;
            }
            var link = document.createElement('a');
            link.className = 'qa-article-link';
            link.href = url;
            link.target = '_blank';
            link.rel = 'noopener';
            var displayLabel = article.label || article.title;
            link.innerHTML = '<span class="qa-link-icon">📖</span>' + displayLabel + (localMatches[i].anchor ? ' <span style="color:rgba(212,175,55,0.6);font-size:11px;">(jump to section)</span>' : '');
            var linkMsg = document.createElement('div');
            linkMsg.className = 'qa-message assistant';
            linkMsg.appendChild(link);
            messagesContainer.appendChild(linkMsg);
          }
        }
        // 裁剪消息数量
        while (messagesContainer.children.length > CONFIG.maxMessages + 4) {
          messagesContainer.firstChild.remove();
        }
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        sendBtn.disabled = false;
        // === 本地匹配成功 → 秒回链接，不调API ===
        return;
      }

      // === 本地0匹配 → 调用后端API兜底 ===
      callBackendAPI(message, messagesContainer, sendBtn, GAME);
    };

    sendBtn.addEventListener('click', function() { sendMessage(false); });
    input.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') sendMessage(false);
    });

    // === Suggested question buttons — forceAI=true → AI answer + article links ===
    var suggestedBtns = widget.querySelectorAll('.qa-suggested-btn');
    for (var b = 0; b < suggestedBtns.length; b++) {
      suggestedBtns[b].addEventListener('click', (function(btn) {
        return function() {
          input.value = btn.getAttribute('data-q') || btn.textContent;
          sendMessage(true);
        };
      })(suggestedBtns[b]));
    }
  }

  // ========== 调用后端API ==========
  function callBackendAPI(message, messagesContainer, sendBtn, gameContext, tocMatches, alreadyShownMatches, forceAI) {
    if (!alreadyShownMatches) alreadyShownMatches = [];
    if (!forceAI) forceAI = false;
    var shownUrls = alreadyShownMatches.map(function(m) { return m.article.url; });
    var apiUrl = CONFIG.apiBase + '/rag-api/search?q=' + encodeURIComponent(message);
    if (gameContext && gameContext !== 'osrs') {
      apiUrl += '&game=' + encodeURIComponent(gameContext);
    }
    if (forceAI) {
      apiUrl += '&force_ai=true';
    }

    fetch(apiUrl)
      .then(function(response) {
        if (!response.ok) throw new Error('API error: ' + response.status);
        return response.json();
      })
      .then(function(data) {
        var loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }

        var answer = data.answer || 'No answer available';
        var source = data.source || 'unknown';

        // === v2.13: 智能显示策略 — forceAI vs 普通模式 ===
        if (forceAI) {
          // === forceAI模式：AI回答 + 深度阅读文章链接 ===
          // 显示AI回答（允许500字，比普通模式更长）
          if (answer && answer.length > 20) {
            if (answer.length > 500) {
              answer = answer.substring(0, 497) + '...';
            }
            addMessage(messagesContainer, answer, 'assistant', false, source);
          } else if (data.title && data.url) {
            // 后端只返回了文章链接没有AI回答 → 生成简短引导语
            addMessage(messagesContainer, 'Here\'s what I found for you:', 'assistant', false, source);
          }

          // 显示"深度阅读"相关文章（1-3篇）
          var deepDive = matchLocalArticles(message, GAME).slice(0, 3);
          if (data.title && data.url) {
            // 先显示API返回的主文章
            var mainLink = document.createElement('a');
            mainLink.className = 'qa-article-link';
            mainLink.href = data.url;
            mainLink.target = '_blank';
            mainLink.rel = 'noopener';
            mainLink.innerHTML = '<span class="qa-link-icon">📖</span>' + data.title;
            var mainMsg = document.createElement('div');
            mainMsg.className = 'qa-message assistant';
            mainMsg.appendChild(mainLink);
            messagesContainer.appendChild(mainMsg);
          }
          if (deepDive.length > 0) {
            var ddLabel = document.createElement('div');
            ddLabel.className = 'qa-section-label';
            ddLabel.textContent = '📖 Deep dive guides:';
            messagesContainer.appendChild(ddLabel);
            for (var i = 0; i < deepDive.length; i++) {
              var ddArticle = deepDive[i].article;
              var ddLink = document.createElement('a');
              ddLink.className = 'qa-article-link';
              ddLink.href = ddArticle.url;
              ddLink.target = '_blank';
              ddLink.rel = 'noopener';
              ddLink.innerHTML = '<span class="qa-link-icon">📖</span>' + (ddArticle.label || ddArticle.title);
              var ddMsg = document.createElement('div');
              ddMsg.className = 'qa-message assistant';
              ddMsg.appendChild(ddLink);
              messagesContainer.appendChild(ddMsg);
            }
          }
        } else {
          // === 普通模式（v2.9逻辑）：osrsguru只显示链接，其他显示文字 ===
          if (source !== 'osrsguru') {
            if (answer.length > 300) {
              answer = answer.substring(0, 297) + '...';
            }
            addMessage(messagesContainer, answer, 'assistant', false, source);
          }

          if (data.title && data.url) {
            var link = document.createElement('a');
            link.className = 'qa-article-link';
            link.href = data.url;
            link.target = '_blank';
            link.rel = 'noopener';
            link.innerHTML = '<span class="qa-link-icon">📖</span>Read full guide: ' + data.title;
            var linkMsg = document.createElement('div');
            linkMsg.className = 'qa-message assistant';
            linkMsg.appendChild(link);
            messagesContainer.appendChild(linkMsg);
          }

          // 补充显示未重复的本地相关文章（过滤已显示的）
          var extra = matchLocalArticles(message, GAME).filter(function(m) {
            return shownUrls.indexOf(m.article.url) === -1;
          }).slice(0, 3);
          if (extra.length > 0) {
            var label = document.createElement('div');
            label.className = 'qa-section-label';
            label.textContent = 'You may also like:';
            messagesContainer.appendChild(label);
            for (var i = 0; i < extra.length; i++) {
              var exArticle = extra[i].article;
              var exLink = document.createElement('a');
              exLink.className = 'qa-article-link';
              exLink.href = exArticle.url;
              exLink.target = '_blank';
              exLink.rel = 'noopener';
              exLink.innerHTML = '<span class="qa-link-icon">📖</span>' + (exArticle.label || exArticle.title);
              var exMsg = document.createElement('div');
              exMsg.className = 'qa-message assistant';
              exMsg.appendChild(exLink);
              messagesContainer.appendChild(exMsg);
            }
          }
        }
      })
      .catch(function(error) {
        console.error('RAG API error:', error);
        var loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }
        var offlineMsg = GAME === 'crimson-desert'
          ? "Sorry, I couldn't find a specific match.\n\nHere are our Crimson Desert guides:\n• New Player Guide\n• Combat Guide\n• Weapons & Gear\n• Quest Walkthrough\n• Boss Guide\n• Skills & Builds\n\nBrowse all: osrsguru.com/guides/crimson-desert/"
          : (GAME === 'windrose'
            ? "Sorry, I couldn't find a specific match.\n\nHere are our Windrose guides:\n• Beginner Guide\n• Combat & Ship Guide\n• Crafting & Gear\n• Quest & Exploration\n• Boss Guide\n• Base Building\n\nBrowse all: osrsguru.com/guides/windrose/"
            : 'AI Assistant is being upgraded!\n\nWe are building a smarter knowledge base with 150+ guides.\n\nBrowse osrsguru.com for all guides.');
        addMessage(messagesContainer, offlineMsg, 'assistant', false, CONFIG.sourceGuruLabel);
      })
      .then(function() {
        sendBtn.disabled = false;
      });
  }

  // ========== 显示相关文章推荐 ==========
  function showRelatedArticles(container, question) {
    var matches = matchLocalArticles(question, GAME);
    if (matches.length === 0) return;

    var label = document.createElement('div');
    label.className = 'qa-section-label';
    label.textContent = 'More guides you may like:';
    container.appendChild(label);

    for (var i = 0; i < matches.length; i++) {
      var article = matches[i].article;
      var link = document.createElement('a');
      link.className = 'qa-article-link';
      link.href = article.url;
      link.target = '_blank';
      link.rel = 'noopener';
      link.innerHTML = '<span class="qa-link-icon">📖</span>' + (article.label || article.title);
      var msg = document.createElement('div');
      msg.className = 'qa-message assistant';
      msg.appendChild(link);
      container.appendChild(msg);
    }

    while (container.children.length > CONFIG.maxMessages + 6) {
      container.firstChild.remove();
    }
    container.scrollTop = container.scrollHeight;
  }

  // ========== 辅助函数 ==========
  function addMessage(container, text, role, isLoading, source) {
    if (isLoading === undefined) isLoading = false;
    if (source === undefined) source = null;

    var messageDiv = document.createElement('div');
    messageDiv.className = 'qa-message ' + role;

    var bubble = document.createElement('div');
    bubble.className = 'qa-message-bubble' + (isLoading ? ' loading' : '');
    bubble.textContent = text;

    messageDiv.appendChild(bubble);

    if (!isLoading && source) {
      var sourceTag = document.createElement('div');
      sourceTag.className = 'qa-source';
      var sourceLabel = '';
      if (source === 'osrsguru') sourceLabel = '📚 ' + CONFIG.sourceGuruLabel;
      else if (source === 'osrs_wiki+deepseek') sourceLabel = '📚+🤖 Wiki + DeepSeek';
      else if (source === 'osrs_wiki') sourceLabel = '📖 OSRS Wiki';
      else if (source === 'deepseek') sourceLabel = '🤖 DeepSeek V3';
      else sourceLabel = '📚 ' + CONFIG.sourceGuruLabel;
      sourceTag.textContent = 'Source: ' + sourceLabel;
      messageDiv.appendChild(sourceTag);
    }

    container.appendChild(messageDiv);

    while (container.children.length > CONFIG.maxMessages) {
      container.firstChild.remove();
    }
    container.scrollTop = container.scrollHeight;
  }

  // ========== 全局API（搜索框联动）==========
  // 搜索框无匹配时调用此API打开AI浮窗并发送问题
  window.OSRSQA = {
    /**
     * 打开/关闭AI浮窗
     * @param {boolean} [forceOpen] - 传true强制打开，false强制关闭，不传则toggle
     */
    open: function(forceOpen) {
      if (!widget) return;
      if (forceOpen === true) {
        widget.classList.add('open');
        if (input) input.focus();
      } else if (forceOpen === false) {
        widget.classList.remove('open');
      } else {
        widget.classList.toggle('open');
        if (widget.classList.contains('open') && input) input.focus();
      }
    },

    /**
     * 向AI助手发送问题（搜索框联动主入口）
     * @param {string} query - 用户输入的搜索词
     */
    ask: function(query) {
      if (!widget || !input || !sendBtn) {
        console.warn('OSRSQA: widget not ready');
        return;
      }
      // 1. 打开浮窗并聚焦输入框
      widget.classList.add('open');
      // 2. 填入问题
      input.value = query;
      input.focus();
      // 3. 启用发送按钮（程序赋值不会触发input事件）
      sendBtn.disabled = false;
      // 4. 触发发送
      sendBtn.click();
    }
  };

  // ========== 初始化 ==========
  // ========== 文章页CTA注入 ==========
  function injectArticleCTA() {
    // 只在攻略页注入（URL含 /guides/ 或存在 .guide-content）
    var isGuidePage = (window.location.pathname.indexOf('/guides/') !== -1) ||
                      !!document.querySelector('.guide-content, .article-content');
    if (!isGuidePage) return;

    var target = document.querySelector('.guide-content, .article-content, main');
    if (!target) return;

    var ctal = document.createElement('div');
    ctal.className = 'qa-article-cta';
    ctal.innerHTML =
      '<div class="qa-article-cta-title">💬 Still have questions?</div>' +
      '<div class="qa-article-cta-desc">Ask <b>Blue Peach</b> AI assistant for a personalized plan — free during beta!</div>' +
      '<a class="qa-article-cta-btn" href="javascript:void(0);">🤖 Ask AI Now</a>';

    ctal.querySelector('.qa-article-cta-btn').addEventListener('click', function(e) {
      e.preventDefault();
      var widgetEl = document.getElementById('osrs-qa-widget');
      if (widgetEl) {
        widgetEl.classList.add('open');
        var input = widgetEl.querySelector('.qa-input');
        if (input) input.focus();
      }
    });

    target.appendChild(ctal);
  }

  // ========== P0+P1: 按钮可见性增强 ==========
  function showPreviewBubble(toggleBtn) {
    // 2小时内未看过气泡的用户才显示
    try {
      var lastSeen = localStorage.getItem('osrs_qa_seen_bubble');
      if (lastSeen) {
        var elapsed = Date.now() - parseInt(lastSeen, 10);
        if (elapsed < 2 * 60 * 60 * 1000) return; // 2小时内不再弹
      }
    } catch(e) {}

    // 8秒后弹出预览气泡
    setTimeout(function() {
      try {
        var lastSeen2 = localStorage.getItem('osrs_qa_seen_bubble');
        if (lastSeen2) {
          var elapsed2 = Date.now() - parseInt(lastSeen2, 10);
          if (elapsed2 < 2 * 60 * 60 * 1000) return;
        }
      } catch(e) {}

      var bubble = document.createElement('div');
      bubble.id = 'osrs-qa-preview-bubble';
      bubble.innerHTML = '<div class="bubble-title">🤖 Ask me anything about ' + CONFIG.gameName + '!</div><div class="bubble-sub">Tap to try →</div>';
      document.body.appendChild(bubble);
      // 触发动画
      requestAnimationFrame(function() { bubble.classList.add('show'); });

      // 点击气泡 → 打开浮窗
      bubble.addEventListener('click', function() {
        widget.classList.add('open');
        if (input) input.focus();
        bubble.style.transition = 'opacity 0.3s';
        bubble.style.opacity = '0';
        setTimeout(function() { if (bubble.parentNode) bubble.remove(); }, 300);
        try { localStorage.setItem('osrs_qa_seen_bubble', String(Date.now())); } catch(e) {}
      });

      // 5秒后自动消失
      setTimeout(function() {
        if (bubble.parentNode) {
          bubble.style.transition = 'opacity 0.5s';
          bubble.style.opacity = '0';
          setTimeout(function() { if (bubble.parentNode) bubble.remove(); }, 500);
        }
        try { localStorage.setItem('osrs_qa_seen_bubble', String(Date.now())); } catch(e) {}
      }, 5000);
    }, 8000);
  }

  function initPulseAndBadge(toggleBtn) {
    // === P0: 脉冲动画（3次呼吸后停止）===
    toggleBtn.classList.add('pulse');
    setTimeout(function() {
      toggleBtn.classList.remove('pulse');
    }, 6000); // 3 cycles × 2s

    // === P0: NEW 徽章 — 始终显示（小徽章不扰民）===
    // 已移除 localStorage 隐藏逻辑，确保所有用户都能看到
  }

  function init() {
    injectStyles();
    var elements = createWidget();
    setupEventHandlers(elements.widget, elements.toggleBtn);
    injectArticleCTA();
    // === P0+P1: 可见性增强 ===
    initPulseAndBadge(elements.toggleBtn);
    showPreviewBubble(elements.toggleBtn);
    console.log('✅ ' + CONFIG.assistantTitle + ' v2.14.1 initialized (pulse + badge + preview bubble + context questions)');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
