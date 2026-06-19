// Search Results Panel — show ALL matching articles instead of single redirect
// Hot keywords → direct redirect to hub/summary pages (skip article matching)
(function() {
  var panel = document.getElementById('searchResultsPanel');
  var grid = document.getElementById('searchResultsGrid');
  var cnt = document.getElementById('searchResultCount');
  var aiHint = document.getElementById('searchAIHint');

  if (!panel || !grid) return;

  // ── Hot Keyword → Hub Page Redirect Map ──────────────────────────
  // When user searches these keywords, jump directly to the column summary page
  var HUB_REDIRECTS = [
    { page: 'skill-training.html',
      keywords: ['skill','skills','skill training','training hub','1-99','99 skill',
                 'leveling','level up','crafting guide','prayer guide','hitpoints',
                 'cooking guide','thieving guide','runecrafting','smithing guide',
                 'herblore guide','magic training','mining guide','woodcutting',
                 'fishing afk','hunter guide','agility training','fletching',
                 'construction','farming guide','slayer guide'] },
    { page: 'money-making.html',
      keywords: ['money making','money-making','make money','earn money','gp per hour',
                 'gp/hour','gold farming','profit','afk money','get rich','wealth',
                 'flipping','merching','moneymaking'] },
    { page: 'boss-guides.html',
      keywords: ['boss','bosses','boss guide','pvm','raids','cox','tob','chambers of xeric',
                 'theatre of blood','god wars','gwd','nex','zulrah','barrows',
                 'cerberus','araxxor','corporeal beast','kalphite queen','king black dragon',
                 'kbd','dagannoth kings','dks','giant mole','skotizo','venenatis',
                 'vetion','callisto','chaos elemental','saradomin','zamorak','bandos',
                 'armadyl'] },
    { page: 'quest-guides.html',
      keywords: ['quest','quests','quest guide','quest walkthrough','dragon slayer',
                 'recipe for disaster','monkey madness','desert treasure','song of the elves',
                 'sins of the father','dream mentor','regicide','underground pass',
                 'horror from the deep','bone Voyage','the great brain robbery',
                 'between a rock','olaf\'s quest','fairy tale'] },
    { page: 'mid-to-high.html',
      keywords: ['mid game','mid-game','breakthrough','mid to high','progression',
                 'high level','endgame prep','pvm progression','late game','gear upgrade',
                 'midgame'] },
    { page: 'weekly-updates.html',
      keywords: ['weekly update','weekly updates','this week','osrs news',
                 'patch notes','jagex update','game update','new update'] },
    { page: 'monthly-updates.html',
      keywords: ['monthly update','monthly updates','month in review','month recap',
                 'monthly roundup'] }
  ];

  function checkHubRedirect(q) {
    var ql = q.toLowerCase().trim();
    for (var i = 0; i < HUB_REDIRECTS.length; i++) {
      var hub = HUB_REDIRECTS[i];
      for (var k = 0; k < hub.keywords.length; k++) {
        var kw = hub.keywords[k];
        // Exact match or contains-as-whole-word match
        if (ql === kw || (' ' + ql + ' ').indexOf(' ' + kw + ' ') !== -1 ||
            ql.indexOf(kw) !== -1) {
          window.location.href = hub.page;
          return true;
        }
      }
    }
    return false;
  }

  window.OSRSSearch = {
    /**
     * Perform search — checks hot keyword redirects first,
     * then falls back to article fuzzy matching
     * @param {string} rawQuery - original user input
     */
    run: function(rawQuery) {
      if (!rawQuery || !rawQuery.trim()) return;

      // ── STEP 1: Check hot keyword → direct hub redirect ──
      if (checkHubRedirect(rawQuery)) {
        return; // Redirected, done!
      }

      // ── STEP 2: No hot keyword match → fuzzy match articles ──
      var q = rawQuery.toLowerCase().trim();
      var qw = q.split(/\s+/);
      var matches = [];
      var keys = Object.keys(ARTICLE_INDEX);

      for (var i = 0; i < keys.length; i++) {
        var kw = keys[i].split(/\s+/);
        var mc = 0;
        for (var j = 0; j < qw.length; j++) {
          if (kw.indexOf(qw[j]) !== -1) mc++;
        }
        if (mc >= Math.max(1, Math.floor(qw.length * 0.5))) {
          matches.push({ key: keys[i], url: ARTICLE_INDEX[keys[i]], score: mc });
        }
      }

      // Sort by relevance score descending
      matches.sort(function(a, b) { return b.score - a.score; });

      if (matches.length > 0) {
        this.showResults(matches, rawQuery);
      } else {
        // No article match → fall through to AI assistant
        if (window.OSRSQA && typeof window.OSRSQA.ask === 'function') {
          window.OSRSQA.ask(rawQuery);
        } else {
          alert('No guide found for: ' + rawQuery);
          if (window.OSRSQA) window.OSRSQA.open(true);
        }
      }
    },

    showResults: function(matches, rawQuery) {
      // Clear previous results
      grid.innerHTML = '';
      
      // Update count text
      cnt.textContent = 'Found ' + matches.length + ' guide' + (matches.length > 1 ? 's' : '') + ' for "' + rawQuery + '"';

      // Build result cards (max 20)
      var maxShow = Math.min(matches.length, 20);
      for (var m = 0; m < maxShow; m++) {
        var item = matches[m];
        var title = item.key.replace(/-/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); });
        
        var card = document.createElement('a');
        card.href = item.url;
        card.className = 'search-result-card';
        
        var titleEl = document.createElement('div');
        titleEl.className = 'sr-title';
        titleEl.textContent = title;
        
        var pathEl = document.createElement('div');
        pathEl.className = 'sr-path';
        pathEl.textContent = item.url.replace('guides/', '').replace('.html', '').replace(/-/g, ' ');
        
        card.appendChild(titleEl);
        card.appendChild(pathEl);
        grid.appendChild(card);
      }

      // Show "more" link if needed
      if (matches.length > 20) {
        var more = document.createElement('div');
        more.className = 'sr-more';
        more.textContent = '... and ' + (matches.length - 20) + ' more results';
        grid.appendChild(more);
      }

      // Show AI hint at bottom
      aiHint.style.display = 'block';

      // Show panel
      panel.style.display = 'block';
      panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    },

    close: function() {
      panel.style.display = 'none';
      document.getElementById('homeSearchInput').focus();
    }
  };
})();
