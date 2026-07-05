/**
 * engine.js — Core Matching & Recommendation Engine for Profit Finder
 *
 * Loads money-methods.json, scores each method against user answers,
 * ranks and returns the Top 3 recommendations with personalized reasons.
 *
 * Dependencies:
 *   - data/money-methods.json (loaded on first fetch)
 *   - payment.js (window.payment) for unlock status (optional)
 *   - ge-api.js (window.geApi) for real-time prices (optional, behind paywall)
 *
 * Exports:
 *   window.findBestMethods(answers)  — main entry point
 *   window.renderResults(result)     — UI rendering
 *   window.loadMethods()             — manual reload trigger
 *   window.engine                    — full API object
 */

(function () {
  'use strict';

  // ──────────────────────────── Constants ────────────────────────────

  /** URL to the methods database JSON file */
  var METHODS_URL = 'data/money-methods.json';

  /** Scoring weights — sum = 100 */
  var WEIGHTS = {
    membership: 25,
    combat: 20,
    goal: 15,
    skill: 15,
    time: 15,
    attention: 10
  };

  /** Ordered arrays for proximity-based scoring (index = level) */
  var COMBAT_LEVELS     = ['3-40', '40-70', '70-90', '90+'];
  var TIME_LEVELS       = ['5min', '30min', '2h+'];
  var ATTENTION_LEVELS  = ['fullAfk', 'semiAfk', 'focused', 'highRisk'];
  
  /** Goal label mapping for reason generation */
  var GOAL_LABELS = {
    firstBond:   '赚取首张债券',
    gearUpgrade: '升级装备',
    bigItem:     '购买大件物品',
    maxGp:       '最大化GP'
  };

  /** Time label mapping for reason generation */
  var TIME_LABELS = {
    '5min': '5分钟',
    '30min': '30分钟',
    '2h+': '长时间(2h+)'
  };

  // ──────────────────────── Module State ──────────────────────────────

  /** @type {Array<Object>} Cached method data from JSON */
  var methodsData = [];

  /** @type {Promise|null} Singleton fetch promise */
  var loadPromise = null;

  // ──────────────────── Database Loading ──────────────────────────────

  /**
   * Fetch and cache the money-methods database.
   * Subsequent calls return the cached promise (singleton).
   * @returns {Promise<Array<Object>>}
   */
  function loadMethods() {
    if (loadPromise) return loadPromise;

    loadPromise = fetch(METHODS_URL)
      .then(function (res) {
        if (!res.ok) {
          throw new Error('HTTP ' + res.status + ': ' + res.statusText);
        }
        return res.json();
      })
      .then(function (data) {
        methodsData = data;
        console.log('[Engine] Loaded ' + data.length + ' methods from database.');
        return data;
      })
      .catch(function (err) {
        methodsData = [];
        loadPromise = null; // Allow retry
        console.error('[Engine] Failed to load methods data:', err.message);
        throw err;
      });

    return loadPromise;
  }

  // ──────────────────── Proximity Helpers ────────────────────────────

  /**
   * Get the index of a value within an ordered level array.
   * @param {Array<string>} levelArray
   * @param {string} value
   * @returns {number} Index or -1 if not found
   */
  function getLevelIndex(levelArray, value) {
    return levelArray.indexOf(value);
  }

  // ──────────────────── Individual Dimension Scoring ─────────────────

  /**
   * Score the membership dimension.
   *   - Exact match → +25
   *   - F2P user pushed P2P method → -10
   *   - P2P user pushed F2P method → +5
   * @param {Object} method
   * @param {string} membership
   * @returns {number}
   */
  function calcMembershipScore(method, membership) {
    var matchArr = method.membershipMatch || [];
    if (matchArr.indexOf(membership) !== -1) {
      return WEIGHTS.membership;
    }

    if (membership === 'f2p' && matchArr.indexOf('p2p') !== -1) {
      return -10;
    }

    if (membership === 'p2p' && matchArr.indexOf('f2p') !== -1) {
      return 5;
    }

    return 0;
  }

  /**
   * Score the combat level dimension.
   *   - Exact match → +20
   *   - Difference of 1 level → +15
   *   - Difference of 2 levels → +10
   *   - Difference of 3+ levels → 0
   * @param {Object} method
   * @param {string} combat
   * @returns {number}
   */
  function calcCombatScore(method, combat) {
    var matchArr = method.combatMatch || [];
    if (matchArr.indexOf(combat) !== -1) {
      return WEIGHTS.combat;
    }

    var userIdx = getLevelIndex(COMBAT_LEVELS, combat);
    if (userIdx === -1) return 0;

    var bestDiff = 999;
    for (var i = 0; i < matchArr.length; i++) {
      var methodIdx = getLevelIndex(COMBAT_LEVELS, matchArr[i]);
      if (methodIdx !== -1) {
        var diff = Math.abs(userIdx - methodIdx);
        if (diff < bestDiff) bestDiff = diff;
      }
    }

    if (bestDiff === 999) return 0;
    if (bestDiff === 1) return WEIGHTS.combat - 5;  // 15
    if (bestDiff === 2) return WEIGHTS.combat - 10; // 10
    return 0;
  }

  /**
   * Score the goal dimension — exact match only.
   * @param {Object} method
   * @param {string} goal
   * @returns {number}
   */
  function calcGoalScore(method, goal) {
    var matchArr = method.goalMatch || [];
    if (matchArr.indexOf(goal) !== -1) {
      return WEIGHTS.goal;
    }
    return 0;
  }

  /**
   * Score the skill dimension.
   *   - Specific skill in bestSkill/skillMatch → +15
   *   - "other" → +7 (neutral)
   *   - "none" → +3 (no preference)
   * @param {Object} method
   * @param {string} skill
   * @returns {number}
   */
  function calcSkillScore(method, skill) {
    if (!skill || skill === 'none') {
      return 3;
    }

    if (skill === 'other') {
      return 7;
    }

    var skillMatchArr = method.skillMatch || [];
    var bestSkill = method.bestSkill || '';

    if (bestSkill === skill || skillMatchArr.indexOf(skill) !== -1) {
      return WEIGHTS.skill;
    }

    return 0;
  }

  /**
   * Score the time-per-session dimension.
   *   - Exact match → +15
   *   - Difference of 1 level → +8
   *   - Difference of 2+ levels → +2
   * @param {Object} method
   * @param {string} time
   * @returns {number}
   */
  function calcTimeScore(method, time) {
    var matchArr = method.timeMatch || [];
    if (matchArr.indexOf(time) !== -1) {
      return WEIGHTS.time;
    }

    var userIdx = getLevelIndex(TIME_LEVELS, time);
    if (userIdx === -1) return 0;

    var bestDiff = 999;
    for (var i = 0; i < matchArr.length; i++) {
      var methodIdx = getLevelIndex(TIME_LEVELS, matchArr[i]);
      if (methodIdx !== -1) {
        var diff = Math.abs(userIdx - methodIdx);
        if (diff < bestDiff) bestDiff = diff;
      }
    }

    if (bestDiff === 999) return 0;
    if (bestDiff === 1) return 8;
    return 2;
  }

  /**
   * Score the attention level dimension.
   *   - Exact match → +10
   *   - Difference of 1 level → +5
   *   - Difference of 2+ levels → 0
   * @param {Object} method
   * @param {string} attention
   * @returns {number}
   */
  function calcAttentionScore(method, attention) {
    var matchArr = method.attentionMatch || [];
    if (matchArr.indexOf(attention) !== -1) {
      return WEIGHTS.attention;
    }

    var userIdx = getLevelIndex(ATTENTION_LEVELS, attention);
    if (userIdx === -1) return 0;

    var bestDiff = 999;
    for (var i = 0; i < matchArr.length; i++) {
      var methodIdx = getLevelIndex(ATTENTION_LEVELS, matchArr[i]);
      if (methodIdx !== -1) {
        var diff = Math.abs(userIdx - methodIdx);
        if (diff < bestDiff) bestDiff = diff;
      }
    }

    if (bestDiff === 999) return 0;
    if (bestDiff === 1) return 5;
    return 0;
  }

  // ──────────────────── Main Scoring Function ────────────────────────

  /**
   * Score a single method against all 6 user answers.
   * @param {Object} method - Method object from database
   * @param {Object} answers - User answers { membership, combat, goal, skill, time, attention }
   * @returns {number} Total score (0-100)
   */
  function scoreMethod(method, answers) {
    try {
      var score = 0;
      score += calcMembershipScore(method, answers.membership);
      score += calcCombatScore(method, answers.combat);
      score += calcGoalScore(method, answers.goal);
      score += calcSkillScore(method, answers.skill);
      score += calcTimeScore(method, answers.time);
      score += calcAttentionScore(method, answers.attention);
      return score;
    } catch (err) {
      console.warn('[Engine] Error scoring method "' + (method.id || 'unknown') + '":', err);
      return 0;
    }
  }

  // ──────────────────── Match Percentage ──────────────────────────────

  /**
   * Convert raw score to percentage (0-100).
   * Max possible score is always 100 (sum of all weights).
   * The score can theoretically dip below 0 due to F2P penalty, clamped to 0.
   * @param {number} score
   * @returns {number}
   */
  function calcMatchPercentage(score) {
    var clamped = Math.max(0, score);
    return Math.round((clamped / 100) * 100);
  }

  // ──────────────────── Reason Generation ────────────────────────────

  /**
   * Generate a personalized recommendation reason string.
   * Combines skill match, time fit, goal, and membership context.
   * @param {Object} method
   * @param {Object} answers
   * @param {number} rank - 1-based rank (1, 2, 3)
   * @returns {string}
   */
  function generateReason(method, answers, rank) {
    try {
      var parts = [];

      // ── Skill match ──
      if (answers.skill && answers.skill !== 'none' && answers.skill !== 'other') {
        var skillName = answers.skill.charAt(0).toUpperCase() + answers.skill.slice(1);
        var bestSkill = method.bestSkill || '';
        var skillMatchArr = method.skillMatch || [];

        if (bestSkill === answers.skill || skillMatchArr.indexOf(answers.skill) !== -1) {
          var skillLevel = method.minSkillLevel || 1;
          parts.push('你有 ' + skillName + ' ' + skillLevel);
        }
      }

      // ── Time fit ──
      if (answers.time) {
        var timeLabel = TIME_LABELS[answers.time] || answers.time;
        var methodTimeArr = method.timeMatch || [];
        if (methodTimeArr.indexOf(answers.time) !== -1) {
          parts.push(timeLabel + '完美匹配');
        } else {
          parts.push('适合 ' + timeLabel);
        }
      }

      // ── Goal ──
      if (answers.goal && GOAL_LABELS[answers.goal]) {
        parts.push('目标: ' + GOAL_LABELS[answers.goal]);
      }

      // ── Membership context ──
      if (answers.membership === 'f2p' && method.membership === 'f2p') {
        parts.push('纯F2P方法');
      } else if (answers.membership === 'p2p' && method.membership === 'p2p') {
        parts.push('P2P专属');
      } else if (answers.membership === 'f2p' && method.membership === 'p2p') {
        parts.push('需要P2P会员');
      }

      var reason = parts.join('，') || method.description.substring(0, 60);
      return reason;
    } catch (err) {
      console.warn('[Engine] Error generating reason for "' + method.id + '":', err);
      return method.description ? method.description.substring(0, 60) : 'Recommended for your play style.';
    }
  }

  // ──────────────────── Recommendation Engine ─────────────────────────

  /**
   * Main entry point — find the best 3 methods for a user's answers.
   * Steps:
   *   1. Validate answers
   *   2. Score every method via scoreMethod()
   *   3. Sort descending by score
   *   4. Take Top 3
   *   5. Generate personalized reasons
   *
   * @param {Object} answers - { membership, combat, goal, skill, time, attention }
   * @returns {{ error?: string, methods: Array<Object>, totalCount: number }}
   */
  function findBestMethods(answers) {
    try {
      // ── Validation ──
      if (!answers) {
        return { error: 'Please answer all 6 questions first.', methods: [], totalCount: 0 };
      }

      var required = ['membership', 'combat', 'goal', 'skill', 'time', 'attention'];
      for (var r = 0; r < required.length; r++) {
        var val = answers[required[r]];
        if (val === undefined || val === null || val === '') {
          return { error: 'Please answer all 6 questions first.', methods: [], totalCount: 0 };
        }
      }

      if (methodsData.length === 0) {
        return { error: 'Failed to load methods data. Please try again.', methods: [], totalCount: 0 };
      }

      // ── Score all methods ──
      var scored = [];
      for (var i = 0; i < methodsData.length; i++) {
        var method = methodsData[i];
        var score = scoreMethod(method, answers);
        var pct = calcMatchPercentage(score);
        scored.push({
          method: method,
          score: score,
          percentage: pct
        });
      }

      // ── Sort: score descending, then gpPerHour descending for ties ──
      scored.sort(function (a, b) {
        if (b.score !== a.score) return b.score - a.score;
        return (b.method.gpPerHour || 0) - (a.method.gpPerHour || 0);
      });

      // ── Take Top 3 ──
      var top = scored.slice(0, 3);

      // ── Generate results ──
      var results = [];
      for (var k = 0; k < top.length; k++) {
        var item = top[k];
        results.push({
          id: item.method.id,
          name: item.method.name,
          score: item.score,
          percentage: Math.min(100, Math.max(0, item.percentage)),
          gpPerHour: item.method.gpPerHour,
          gpPerHourMin: item.method.gpPerHourMin,
          gpPerHourMax: item.method.gpPerHourMax,
          guideUrl: item.method.guideUrl,
          matchTags: item.method.matchTags || [],
          reason: generateReason(item.method, answers, k + 1),
          difficulty: item.method.difficulty,
          membership: item.method.membership,
          category: item.method.category,
          profitNote: item.method.profitNote || ''
        });
      }

      return {
        methods: results,
        totalCount: methodsData.length
      };
    } catch (err) {
      console.error('[Engine] Error in findBestMethods:', err);
      return {
        error: 'An unexpected error occurred. Please try again.',
        methods: [],
        totalCount: 0
      };
    }
  }

  // ──────────────────── Result Rendering ──────────────────────────────

  /**
   * Render Top 3 results into the DOM.
   * 1. Hides question card area
   * 2. Shows/create results container
   * 3. Builds result cards with rank emoji, match %, GP/hr, reason, tags, guide link
   * 4. If payment is unlocked, fetches real-time GE prices
   *
   * @param {{ error?: string, methods: Array<Object>, totalCount: number }} result
   */
  function renderResults(result) {
    try {
      // ── 1. Hide questions section ──
      var questionsSection = document.querySelector(
        '#questionsFlow, .questions-flow'
      );
      if (questionsSection) {
        questionsSection.style.display = 'none';
      }

      // ── 2. Find or create results container ──
      var resultSection = document.querySelector(
        '#resultsArea, .results-area'
      );
      if (!resultSection) {
        resultSection = document.createElement('div');
        resultSection.id = 'engine-results';
        resultSection.className = 'results-area';
        var container = document.querySelector(
          '.tool-container'
        ) || document.body;
        container.appendChild(resultSection);
      }
      resultSection.style.display = 'block';

      // ── Error state ──
      if (result.error) {
        resultSection.innerHTML = [
          '<div class="error-message" style="text-align:center;padding:48px 20px;">',
            '<p style="font-size:18px;font-weight:600;color:#ef4444;margin:0 0 16px;">',
              escapeHtml(result.error),
            '</p>',
            '<button class="btn-retry" onclick="window.location.reload()"',
            ' style="padding:10px 24px;background:#f59e0b;color:#1a1a2e;',
            'border:0;border-radius:6px;font-size:16px;font-weight:600;cursor:pointer;">',
              'Retry',
            '</button>',
          '</div>'
        ].join('');
        return;
      }

      // ── 3-7. Build result cards ──
      var rankEmojis   = ['🥇', '🥈', '🥉'];
      var rankClasses  = ['rank-1', 'rank-2', 'rank-3'];
      var isUnlocked = window.payment &&
        typeof window.payment.isUnlocked === 'function' &&
        window.payment.isUnlocked();

      var html = [
        '<div class="results-header" style="text-align:center;margin-bottom:32px;">',
          '<h2 style="font-size:28px;color:#f59e0b;margin:0 0 8px;">Recommended Methods</h2>',
          '<p style="color:#94a3b8;font-size:14px;margin:0;">',
            'Based on ', result.totalCount, ' methods analyzed',
          '</p>',
        '</div>',
        '<div class="results-grid" style="display:flex;flex-direction:column;gap:20px;max-width:800px;margin:0 auto;">'
      ].join('');

      for (var i = 0; i < result.methods.length; i++) {
        var m = result.methods[i];
        var pct = Math.min(100, Math.max(0, m.percentage));
        var pctColor = pct >= 80 ? '#22c55e' : (pct >= 60 ? '#f59e0b' : '#ef4444');

        // GP display
        var gpHtml = '';
        if (m.gpPerHourMin && m.gpPerHourMax && m.gpPerHourMin !== m.gpPerHourMax) {
          gpHtml = '<span class="gp-value">' +
            formatGp(m.gpPerHourMin) + ' - ' + formatGp(m.gpPerHourMax) +
            '</span>';
        } else {
          gpHtml = '<span class="gp-value">' + formatGp(m.gpPerHour) + '</span>';
        }

        // Tags
        var tagsHtml = '';
        if (m.matchTags && m.matchTags.length > 0) {
          tagsHtml = '<div class="result-tags" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;">';
          for (var t = 0; t < m.matchTags.length; t++) {
            tagsHtml += [
              '<span class="tag" style="display:inline-block;padding:4px 10px;',
                'background:rgba(245,158,11,0.15);color:#fbbf24;',
                'border-radius:4px;font-size:12px;font-weight:500;">',
                escapeHtml(m.matchTags[t]),
              '</span>'
            ].join('');
          }
          tagsHtml += '</div>';
        }

        // Guide link
        var guideLinkHtml = [
          '<a href="', escapeHtml(m.guideUrl), '" class="guide-link" target="_blank"',
          ' style="display:inline-flex;align-items:center;gap:6px;margin-top:16px;',
          'padding:8px 16px;background:linear-gradient(135deg,#f59e0b,#d97706);',
          'color:#1a1a2e;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;">',
            '📖 查看完整攻略',
          '</a>'
        ].join('');

        html += [
          '<div class="result-card" data-method-id="', escapeHtml(m.id), '"',
          ' style="display:flex;background:rgba(255,255,255,0.04);',
          'border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:0;overflow:hidden;">',

            // Rank badge
            '<div class="result-rank ', rankClasses[i], '"',
            ' style="display:flex;align-items:center;justify-content:center;',
            'width:80px;min-width:80px;font-size:36px;background:rgba(245,158,11,0.08);">',
              rankEmojis[i],
            '</div>',

            // Content
            '<div class="result-content" style="flex:1;padding:20px 24px;">',

              // Title row + match badge
              '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">',
                '<h3 style="margin:0;font-size:20px;color:#f1f5f9;">', escapeHtml(m.name), '</h3>',
                '<div class="match-badge" style="display:inline-flex;align-items:center;gap:6px;',
                'padding:4px 12px;background:', pctColor, '20;color:', pctColor, ';',
                'border-radius:20px;font-size:14px;font-weight:700;">',
                  '🔥 ', pct, '%',
                '</div>',
              '</div>',

              // GP info
              '<div class="gp-info" style="display:flex;align-items:center;gap:8px;margin-top:10px;">',
                gpHtml,
                '<span class="gp-label" style="color:#94a3b8;font-size:13px;">GP/hr</span>',
              '</div>',

              // Reason
              '<div class="match-reason" style="margin-top:12px;color:#cbd5e1;font-size:14px;line-height:1.5;">',
                escapeHtml(m.reason),
              '</div>',

              tagsHtml,
              guideLinkHtml,
            '</div>',
          '</div>'
        ].join('');
      }

      html += '</div>';

      // Reset button
      html += [
        '<div style="text-align:center;margin-top:28px;">',
          '<button class="btn-reset" onclick="window.dispatchEvent(new CustomEvent(\'profit-finder:reset\'))"',
          ' style="padding:10px 20px;background:transparent;border:1px solid rgba(255,255,255,0.2);',
          'color:#94a3b8;border-radius:8px;font-size:14px;cursor:pointer;transition:all 0.2s;"',
          ' onmouseover="this.style.borderColor=\'#f59e0b\';this.style.color=\'#f59e0b\'"',
          ' onmouseout="this.style.borderColor=\'rgba(255,255,255,0.2)\';this.style.color=\'#94a3b8\'">',
            '← Start Over',
          '</button>',
        '</div>'
      ].join('');

      resultSection.innerHTML = html;

      // ── 8. Real-time prices (if unlocked) ──
      if (isUnlocked && window.osrsPrices && typeof window.osrsPrices.fetchItemPrice === 'function') {
        for (var p = 0; p < result.methods.length; p++) {
          fetchRealTimePrice(result.methods[p].id, result.methods[p].name);
        }
      }
    } catch (err) {
      console.error('[Engine] Error rendering results:', err);
      var errContainer = document.querySelector(
        '#resultsArea, .results-area, #engine-results'
      );
      if (errContainer) {
        errContainer.innerHTML = [
          '<div class="error-message" style="text-align:center;padding:40px;">',
            '<p style="color:#ef4444;font-size:16px;">',
              'An error occurred while displaying results. Please try again.',
            '</p>',
          '</div>'
        ].join('');
      }
    }
  }

  // ──────────────────── Real-Time Price Fetch ─────────────────────────

  /**
   * Attempt to fetch and display the real-time GE price for a method.
   * Only fires when payment is unlocked and geApi is available.
   * @param {string} methodId
   * @param {string} itemName
   */
  function fetchRealTimePrice(methodId, itemName) {
    try {
      var priceEl = document.getElementById('ge-price-' + methodId);
      if (!priceEl || !window.osrsPrices) return;

      window.osrsPrices.fetchItemPrice(itemName)
        .then(function (price) {
          if (priceEl && price !== null && price !== undefined) {
            priceEl.textContent = formatGp(price);
          }
        })
        .catch(function () {
          if (priceEl) {
            priceEl.textContent = 'N/A';
          }
        });
    } catch (_) {
      // Silently ignore — real-time price is a nice-to-have
    }
  }

  // ──────────────────── Utility Helpers ──────────────────────────────

  /**
   * Format a GP value for display (e.g. 1500000 → "1.5M").
   * @param {number} value
   * @returns {string}
   */
  function formatGp(value) {
    if (value === undefined || value === null) return 'N/A';
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    }
    if (value >= 1000) {
      return (value / 1000).toFixed(0) + 'K';
    }
    return Number(value).toLocaleString();
  }

  /**
   * Escape HTML special characters to prevent XSS.
   * @param {*} str
   * @returns {string}
   */
  function escapeHtml(str) {
    if (typeof str !== 'string') {
      str = String(str || '');
    }
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ──────────────────── Global Exports ───────────────────────────────

  /** Primary entry point — find best methods for user answers */
  window.findBestMethods = function (answers) {
    return findBestMethods(answers);
  };

  /** Render results into the DOM */
  window.renderResults = function (result) {
    renderResults(result);
  };

  /** Trigger a manual reload of the methods database */
  window.loadMethods = function () {
    return loadMethods();
  };

  /** Full API object for advanced usage */
  window.engine = {
    loadMethods: loadMethods,
    findBestMethods: findBestMethods,
    renderResults: renderResults,
    scoreMethod: scoreMethod,
    calcMatchPercentage: calcMatchPercentage,
    generateReason: generateReason,
    calcMembershipScore: calcMembershipScore,
    calcCombatScore: calcCombatScore,
    calcGoalScore: calcGoalScore,
    calcSkillScore: calcSkillScore,
    calcTimeScore: calcTimeScore,
    calcAttentionScore: calcAttentionScore
  };

  // ──────────────────── Auto-Init ─────────────────────────────────────

  // Start loading methods data immediately so it's ready when needed
  loadMethods().catch(function (err) {
    console.warn('[Engine] Initial data load failed; will retry on first findBestMethods call:', err.message);
  });

  // ──────────────────── Reset Event Listener ──────────────────────────

  /**
   * Listen for 'profit-finder:reset' custom event.
   * Hides results and re-shows the questions section.
   */
  document.addEventListener('profit-finder:reset', function () {
    try {
      var resultSection = document.querySelector(
        '.results-section, #results-section, #engine-results'
      );
      if (resultSection) {
        resultSection.style.display = 'none';
      }

      var questionsSection = document.querySelector(
        '.questions-section, #questions-section, .question-cards, [data-section="questions"]'
      );
      if (questionsSection) {
        questionsSection.style.display = 'block';
      }
    } catch (err) {
      console.warn('[Engine] Error during reset:', err);
    }
  });

})();
