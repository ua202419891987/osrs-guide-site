// Search Results Panel — show ALL matching articles instead of single redirect
(function() {
  var panel = document.getElementById('searchResultsPanel');
  var grid = document.getElementById('searchResultsGrid');
  var cnt = document.getElementById('searchResultCount');
  var aiHint = document.getElementById('searchAIHint');

  if (!panel || !grid) return;

  window.OSRSSearch = {
    /**
     * Perform search — finds ALL matching articles and displays results panel
     * @param {string} rawQuery - original user input
     */
    run: function(rawQuery) {
      if (!rawQuery || !rawQuery.trim()) return;
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
