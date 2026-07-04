/**
 * OSRS Gear Recommender Engine
 * =============================
 * Core recommendation algorithm for the OSRS Guru Gear Tool.
 * 
 * This module provides:
 *   - loadGearDatabase()       – Load gear data from JSON with caching
 *   - recommendGear()          – Core recommendation algorithm
 *   - getUpgradePath()         – Get next upgrade steps
 *   - calculateTotalCost()     – Sum gear loadout costs
 *   - filterByBudget()         – Filter items by budget
 * 
 * @version 1.0.0
 * @license MIT
 * @see https://osrsguru.com/tools/gear-recommender
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.OSRSGearEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ============================================================
  //  CONSTANTS
  // ============================================================

  /** @const {string} Path to gear database JSON (relative to page) */
  const DATABASE_URL = 'data/gear-database.json';

  /** @const {string} OSRS Wiki GE Prices API */
  const GE_API_URL = 'https://prices.runescape.wiki/api/v1/osrs/latest';

  /** @const {string} OSRS Wiki Item Mapping API */
  const GE_MAPPING_URL = 'https://prices.runescape.wiki/api/v1/osrs/mapping';

  /** @const {string} User agent for API requests */
  const USER_AGENT = 'osrsguru-gear-tool/1.0 (tools@osrsguru.com)';

  /** @const {number} Price cache TTL (24 hours in ms) */
  const CACHE_TTL = 24 * 60 * 60 * 1000;

  /** @const {number} Mapping cache TTL (7 days in ms) */
  const MAPPING_CACHE_TTL = 7 * 24 * 60 * 60 * 1000;

  /** @const {Object} Price tier thresholds */
  const PRICE_TIERS = {
    cheap:     { label: 'Cheap',     min: 0,       max: 50000,      icon: '💰' },
    medium:    { label: 'Medium',    min: 50000,   max: 500000,     icon: '💰💰' },
    expensive: { label: 'Expensive', min: 500000,  max: 50000000,   icon: '💰💰💰' },
    biS:       { label: 'Best in Slot', min: 50000000, max: Infinity, icon: '👑' }
  };

  /** @const {Object} Scoring weights for recommendation algorithm */
  const SCORE_WEIGHTS = {
    primaryStat:     0.35,
    secondaryStat:   0.20,
    defence:         0.10,
    priceEfficiency: 0.20,
    priority:        0.15,
    penaltyDegradable:  0.05,
    penaltyQuestLocked: 0.10
  };

  /** @const {number} Max budget slider value (in thousands) */
  const MAX_BUDGET_K = 5000;

  /** @const {Array} All gear slots in display order */
  const ALL_SLOTS = [
    'head', 'cape', 'amulet', 'body', 'legs',
    'weapon', 'shield', 'gloves', 'boots', 'ring'
  ];

  /** @const {Object} Slot display labels */
  const SLOT_LABELS = {
    head:    { label: '头饰', icon: '🪖' },
    cape:    { label: '披风', icon: '🧣' },
    amulet:  { label: '项链', icon: '📿' },
    neck:    { label: '项链', icon: '📿' },
    body:    { label: '身体', icon: '🛡️' },
    legs:    { label: '腿甲', icon: '👖' },
    weapon:  { label: '武器', icon: '⚔️' },
    shield:  { label: '盾牌', icon: '🔰' },
    gloves:  { label: '手套', icon: '🧤' },
    boots:   { label: '靴子', icon: '👢' },
    ring:    { label: '戒指', icon: '💍' }
  };

  /** @const {Object} Style-specific key stat mapping */
  const STYLE_STATS = {
    melee:  { primary: ['strengthBonus', 'slash'], primaryLabel: '力量/斩击', secondaryLabel: '力量' },
    ranged: { primary: ['ranged', 'rangedStrength'], primaryLabel: '远程攻击', secondaryLabel: '远程力量' },
    magic:  { primary: ['magic', 'magicDamage'], primaryLabel: '魔法攻击', secondaryLabel: '魔法伤害' }
  };

  /** @const {Object} Level config for each combat style */
  const LEVEL_CONFIG = {
    melee:  [
      { key: 'attack',    label: '攻击 Attack',    max: 99 },
      { key: 'strength',  label: '力量 Strength',  max: 99 },
      { key: 'defence',   label: '防御 Defence',   max: 99 },
      { key: 'hitpoints', label: '生命 Hitpoints', max: 99 }
    ],
    ranged: [
      { key: 'ranged',    label: '远程 Ranged',    max: 99 },
      { key: 'defence',   label: '防御 Defence',   max: 99 },
      { key: 'hitpoints', label: '生命 Hitpoints', max: 99 }
    ],
    magic:  [
      { key: 'magic',     label: '魔法 Magic',     max: 99 },
      { key: 'defence',   label: '防御 Defence',   max: 99 },
      { key: 'hitpoints', label: '生命 Hitpoints', max: 99 }
    ]
  };

  /** @const {Object} Chinese style names */
  const STYLE_CN = { melee: '近战', ranged: '远程', magic: '魔法' };

  // ============================================================
  //  CACHE KEYS
  // ============================================================

  const CACHE = {
    PRICES:    'osrs_ge_prices',
    MAPPING:   'osrs_ge_mapping',
    TIMESTAMP: 'osrs_ge_timestamp',
    MAPPING_TS:'osrs_ge_mapping_timestamp',
    DATABASE:  'osrs_gear_database',
    DB_VER:    'osrs_gear_database_version'
  };

  // ============================================================
  //  INTERNAL STATE
  // ============================================================

  /** @private In-memory database cache */
  let _db = null;

  /** @private In-memory price cache */
  let _prices = null;

  /** @private In-memory name-to-id mapping */
  let _nameToId = null;

  // ============================================================
  //  INTERNAL HELPERS
  // ============================================================

  /**
   * Normalize item name for ID matching (lowercase, trim).
   * @param {string} name
   * @returns {string}
   */
  function _normalizeName(name) {
    return name.toLowerCase().replace(/[^\w\s]/g, '').trim();
  }

  /**
   * Format a GP amount into human-readable string.
   * @param {number} gp
   * @returns {string}
   */
  function formatGP(gp) {
    if (!gp && gp !== 0) return '未知';
    if (gp >= 1000000) return (gp / 1000000).toFixed(gp % 1000000 === 0 ? 0 : 1) + 'M';
    if (gp >= 1000) return Math.round(gp / 1000) + 'K';
    return String(gp);
  }

  /**
   * Parse a GP string like "~48K" or "~1.2M" back to number.
   * @param {string} str
   * @returns {number}
   */
  function parseGP(str) {
    if (!str) return 0;
    const cleaned = str.replace(/[~≈\s,]/g, '').toLowerCase();
    if (cleaned.endsWith('m')) return parseFloat(cleaned) * 1000000;
    if (cleaned.endsWith('k')) return parseFloat(cleaned) * 1000;
    const num = parseFloat(cleaned);
    return isNaN(num) ? 0 : num;
  }

  /**
   * Determine price tier label from a numeric price.
   * @param {number} price
   * @returns {string}
   */
  function getPriceTier(price) {
    if (price < 50000) return 'cheap';
    if (price < 500000) return 'medium';
    if (price < 50000000) return 'expensive';
    return 'biS';
  }

  /**
   * Deep-clone a simple object.
   * @param {*} obj
   * @returns {*}
   */
  function _clone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  /**
   * Check if a level value meets a requirement.
   * @param {number|undefined} level
   * @param {number} required
   * @returns {boolean}
   */
  function _meetsLevel(level, required) {
    return (level || 0) >= (required || 0);
  }

  /**
   * Safely parse JSON from localStorage.
   * @param {string} key
   * @returns {*|null}
   */
  function _lsGet(key) {
    try {
      const val = localStorage.getItem(key);
      return val ? JSON.parse(val) : null;
    } catch (e) {
      return null;
    }
  }

  /**
   * Safely set JSON to localStorage.
   * @param {string} key
   * @param {*} value
   */
  function _lsSet(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.warn('[GearEngine] localStorage write failed:', key);
    }
  }

  // ============================================================
  //  DATA LOADERS
  // ============================================================

  /**
   * Load the gear database JSON file.
   * Uses in-memory cache first, then localStorage, then fetch.
   * 
   * @param {boolean} [forceRefresh=false] - Bypass caches
   * @returns {Promise<Object>} The parsed gear database
   * @throws {Error} If database cannot be loaded
   */
  async function loadGearDatabase(forceRefresh) {
    // In-memory cache
    if (!forceRefresh && _db) return _db;

    // localStorage cache with version check
    if (!forceRefresh) {
      const cached = _lsGet(CACHE.DATABASE);
      if (cached && cached.meta) {
        _db = cached;
        return _db;
      }
    }

    // Network fetch
    try {
      const response = await fetch(DATABASE_URL);
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const data = await response.json();

      // Validate structure
      if (!data.combat_styles && !data.items) {
        throw new Error('Invalid database schema: missing combat_styles or items');
      }

      _db = data;
      _lsSet(CACHE.DATABASE, data);
      _lsSet(CACHE.DB_VER, data.meta ? data.meta.version : '1.0');

      return data;
    } catch (error) {
      console.error('[GearEngine] Failed to load gear database:', error);

      // Last resort: return empty structure
      if (!_db) {
        _db = { combat_styles: {}, items: [], upgradePaths: [] };
      }
      return _db;
    }
  }

  /**
   * Load GE price data from the OSRS Wiki API.
   * Uses localStorage cache with 24-hour TTL.
   * Falls back to cached or static prices on failure.
   * 
   * @param {boolean} [forceRefresh=false] - Skip cache
   * @returns {Promise<Object|null>} Price map { itemId: {high, low} }
   */
  async function loadGEPrices(forceRefresh) {
    // In-memory cache
    if (!forceRefresh && _prices) return _prices;

    // Check localStorage cache expiry
    const ts = localStorage.getItem(CACHE.TIMESTAMP);
    const valid = ts && (Date.now() - parseInt(ts)) < CACHE_TTL;

    if (!forceRefresh && valid) {
      const cached = _lsGet(CACHE.PRICES);
      if (cached) {
        _prices = cached;
        return _prices;
      }
    }

    // Fetch from API
    try {
      const response = await fetch(GE_API_URL, {
        headers: {
          'User-Agent': USER_AGENT,
          'Accept': 'application/json'
        }
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);

      const json = await response.json();
      const data = json.data || json;

      _prices = data;
      _lsSet(CACHE.PRICES, data);
      localStorage.setItem(CACHE.TIMESTAMP, String(Date.now()));

      return data;
    } catch (error) {
      console.warn('[GearEngine] GE API fetch failed:', error.message);

      // Fallback: use stale cache
      const stale = _lsGet(CACHE.PRICES);
      if (stale) {
        _prices = stale;
        console.warn('[GearEngine] Using stale cached prices');
        return _prices;
      }

      // Final fallback: return null (engine will use estimated prices)
      _prices = null;
      return null;
    }
  }

  /**
   * Load item name-to-ID mapping from the OSRS Wiki API.
   * 
   * @param {boolean} [forceRefresh=false]
   * @returns {Promise<Object>} Map of { "item name": osrsId }
   */
  async function loadMapping(forceRefresh) {
    if (!forceRefresh && _nameToId) return _nameToId;

    const ts = localStorage.getItem(CACHE.MAPPING_TS);
    const valid = ts && (Date.now() - parseInt(ts)) < MAPPING_CACHE_TTL;

    if (!forceRefresh && valid) {
      const cached = _lsGet(CACHE.MAPPING);
      if (cached) {
        _nameToId = cached;
        return _nameToId;
      }
    }

    try {
      const response = await fetch(GE_MAPPING_URL, {
        headers: {
          'User-Agent': USER_AGENT,
          'Accept': 'application/json'
        }
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);

      const json = await response.json();
      const items = json.data || json;

      // Build name → ID map
      const map = {};
      for (const item of items) {
        map[_normalizeName(item.name)] = item.id;
      }

      _nameToId = map;
      _lsSet(CACHE.MAPPING, map);
      localStorage.setItem(CACHE.MAPPING_TS, String(Date.now()));

      return map;
    } catch (error) {
      console.warn('[GearEngine] Mapping fetch failed:', error.message);
      const stale = _lsGet(CACHE.MAPPING);
      _nameToId = stale || {};
      return _nameToId;
    }
  }

  // ============================================================
  //  DATABASE QUERIES
  // ============================================================

  /**
   * Get all items for a given combat style at a specific tier/level range.
   * 
   * @param {Object} db - The gear database
   * @param {string} combatStyle - 'melee' | 'ranged' | 'magic'
   * @param {Object} levels - { attack, strength, defence, ranged, magic, hitpoints }
   * @param {boolean} isMember - Whether the user is P2P
   * @returns {Object} Items grouped by slot { slotName: [items] }
   */
  function getItemsForStyle(db, combatStyle, levels, isMember) {
    const styleData = db.combat_styles && db.combat_styles[combatStyle];
    if (!styleData || !styleData.tiers) {
      return getItemsFromArray(db, combatStyle, levels, isMember);
    }

    // Tier-based database (gear-database.json format v1.1)
    const defenceLevel = levels.defence || 1;
    const primaryLevel = levels[styleData.skill_key] || 1;

    // Determine which tier (level range) the user qualifies for
    let selectedTier = null;
    let selectedTierIndex = -1;

    for (let i = styleData.tiers.length - 1; i >= 0; i--) {
      const tier = styleData.tiers[i];
      const range = tier.level_range.split('-').map(Number);
      const tierMin = range[0] || 1;
      const tierMax = range[1] || 99;

      // Check if player meets the tier requirements
      if (primaryLevel >= tierMin || defenceLevel >= tierMin) {
        selectedTier = tier;
        selectedTierIndex = i;
        break;
      }
    }

    if (!selectedTier) {
      selectedTier = styleData.tiers[0];
      selectedTierIndex = 0;
    }

    // Get the recommended gear for this tier
    const gear = selectedTier.recommended_gear || {};
    const result = {};

    for (const slot of ALL_SLOTS) {
      // Map 'amulet' to 'neck' if needed
      const slotKey = gear[slot] ? slot : 
                      (slot === 'amulet' && gear.neck) ? 'neck' : null;

      if (slotKey && gear[slotKey]) {
        const item = gear[slotKey];
        // Apply membership filter
        if (!isMember && item.f2p === false) {
          result[slot] = null;
          continue;
        }
        result[slot] = item;
      } else {
        result[slot] = null;
      }
    }

    return result;
  }

  /**
   * Alternative: Get items from flat items array (future schema v2.0).
   * 
   * @param {Object} db
   * @param {string} combatStyle
   * @param {Object} levels
   * @param {boolean} isMember
   * @returns {Object}
   */
  function getItemsFromArray(db, combatStyle, levels, isMember) {
    const items = db.items || [];
    const result = {};

    for (const slot of ALL_SLOTS) {
      result[slot] = null;
    }

    // Filter items matching style and level requirements
    const candidates = items.filter(item => {
      // Combat style match
      if (item.combatStyle !== combatStyle && item.combatStyle !== 'all') return false;

      // Membership filter
      if (!isMember && item.memberTier === 'p2p') return false;

      // Level check
      const reqs = item.requirements || {};
      for (const skill of ['attack', 'strength', 'defence', 'ranged', 'magic', 'prayer', 'hitpoints']) {
        if (reqs[skill] && (levels[skill] || 0) < reqs[skill]) return false;
      }

      return true;
    });

    // Group by slot and pick best per slot
    const bySlot = {};
    for (const item of candidates) {
      const slot = item.slot;
      if (!bySlot[slot]) bySlot[slot] = [];
      bySlot[slot].push(item);
    }

    // For each slot, sort by recommendationPriority desc and pick top
    const slotKeys = Object.keys(bySlot);
    for (const slotKey of slotKeys) {
      const slotItems = bySlot[slotKey].sort((a, b) => {
        return (b.recommendationPriority || 0) - (a.recommendationPriority || 0);
      });
      result[slotKey] = slotItems[0] || null;
    }

    return result;
  }

  // ============================================================
  //  RECOMMENDATION ALGORITHM
  // ============================================================

  /**
   * Main recommendation function.
   * Takes combat style, level info, budget, and membership status,
   * returns a complete gear loadout with reasons and upgrade paths.
   * 
   * @param {string} combatStyle - 'melee' | 'ranged' | 'magic'
   * @param {Object} levels - Skill levels { attack, strength, defence, ranged, magic, hitpoints }
   * @param {Object} budget - Budget configuration { tier, maxAmount? }
   * @param {Object} [options]
   * @param {boolean} [options.isMember=true]
   * @param {boolean} [options.isPremium=false]
   * @param {string[]} [options.questsCompleted=[]]
   * @returns {Promise<Object>} Recommendation result
   */
  async function recommendGear(combatStyle, levels, budget, options) {
    options = Object.assign({
      isMember: true,
      isPremium: false,
      questsCompleted: []
    }, options || {});

    // 1. Load data
    let db;
    try {
      db = await loadGearDatabase();
    } catch (e) {
      console.error('[GearEngine] Database load failed:', e);
      throw new Error('无法加载装备数据库，请刷新页面重试');
    }

    // 2. Try to load real-time prices (non-blocking — fall back to static)
    let pricesPromise = null;
    try {
      pricesPromise = loadGEPrices();
    } catch (e) {
      // Ignore — will use static prices
    }

    // 3. Get items for this style and level
    const gear = getItemsForStyle(db, combatStyle, levels, options.isMember);

    // 4. Get style data for upgrade paths and stats
    const styleData = db.combat_styles && db.combat_styles[combatStyle];
    const styleStats = STYLE_STATS[combatStyle] || STYLE_STATS.melee;

    // 5. Build recommendations per slot
    const recommendations = {};
    let realPrices = null;

    for (const slot of ALL_SLOTS) {
      const item = gear[slot];
      if (!item) {
        recommendations[slot] = {
          item: null,
          reason: '无推荐装备（等级不足或会员限制）',
          alternatives: [],
          upgradeTo: null,
          price: 0
        };
        continue;
      }

      // Get effective price
      const itemPrice = getItemEffectivePrice(item);

      // Budget check (skip for free unlimited, apply for all others)
      if (budget && budget.maxAmount > 0 && itemPrice > budget.maxAmount) {
        // Try to find a cheaper alternative in the database
        const cheaper = findCheaperAlternative(db, combatStyle, slot, levels, budget.maxAmount, options.isMember);
        recommendations[slot] = {
          item: cheaper || item,
          reason: cheaper
            ? '预算内替代品（非当前等级最佳）'
            : '超出预算，显示最佳装备供参考',
          alternatives: [],
          upgradeTo: null,
          price: cheaper ? getItemEffectivePrice(cheaper) : itemPrice
        };
        continue;
      }

      // Generate recommendation reason
      const reason = generateReason(item, combatStyle, styleStats);

      // Upgrade path (premium only)
      let upgradePath = null;
      if (options.isPremium) {
        upgradePath = findUpgradeForItem(db, item, combatStyle);
      }

      recommendations[slot] = {
        item: item,
        reason: reason,
        alternatives: [],
        upgradeTo: upgradePath,
        price: itemPrice,
        locked: !options.isPremium && upgradePath !== null
      };
    }

    // 6. Wait for prices (non-blocking)
    try {
      if (pricesPromise) {
        const result = await Promise.race([
          pricesPromise,
          new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 5000))
        ]);
        if (result) {
          realPrices = result;
          // Update prices with real data if mapping is available
          const mapping = await loadMapping().catch(() => ({}));
          for (const slot of ALL_SLOTS) {
            const rec = recommendations[slot];
            if (rec && rec.item && realPrices) {
              const itemName = rec.item.name;
              if (itemName && mapping) {
                const nameKey = _normalizeName(itemName);
                const osrsId = mapping[nameKey];
                if (osrsId && realPrices[osrsId]) {
                  const p = realPrices[osrsId];
                  const avg = (p.high + p.low) / 2;
                  if (avg > 0) rec.price = Math.round(avg);
                }
              }
            }
          }
        }
      }
    } catch (e) {
      // Silently use estimated prices
    }

    // 7. Calculate total cost
    const totalCost = calculateTotalCost(recommendations);

    // 8. Get upgrade path
    const upgradePath = options.isPremium
      ? getUpgradePath(combatStyle, levels, recommendations, db)
      : [];

    return {
      style: combatStyle,
      styleName: STYLE_CN[combatStyle] || combatStyle,
      levels: levels,
      budget: budget,
      slots: recommendations,
      totalCost: totalCost,
      totalCostFormatted: formatGP(totalCost),
      upgradePath: upgradePath,
      hasRealPrices: realPrices !== null
    };
  }

  // ============================================================
  //  HELPERS: PRICE / FILTER / REASON
  // ============================================================

  /**
   * Get effective price of an item from the gear database.
   * 
   * @param {Object} item
   * @returns {number}
   */
  function getItemEffectivePrice(item) {
    if (!item) return 0;

    // Try various price field locations
    if (typeof item.ge_price_estimate === 'number') return item.ge_price_estimate;
    if (typeof item.ge_price_estimate === 'string') return parseGP(item.ge_price_estimate);
    if (item.price && typeof item.price.estimated === 'number') return item.price.estimated;
    if (item.cost) return parseGP(item.cost);

    return 0;
  }

  /**
   * Filter a list of gear items by a maximum budget.
   * Returns items whose effective price <= budget.maxAmount.
   * 
   * @param {Object} gear - Gear object keyed by slot
   * @param {Object} budget - { maxAmount: number }
   * @returns {Object} Filtered gear
   */
  function filterByBudget(gear, budget) {
    if (!budget || !budget.maxAmount || budget.maxAmount <= 0) return gear;

    const filtered = {};
    for (const slot of ALL_SLOTS) {
      const item = gear[slot];
      if (!item) {
        filtered[slot] = null;
        continue;
      }

      const price = getItemEffectivePrice(item);
      if (price <= budget.maxAmount) {
        filtered[slot] = item;
      } else {
        // Keep item but mark as over-budget
        filtered[slot] = Object.assign({}, item, {
          _overBudget: true,
          _overBy: price - budget.maxAmount
        });
      }
    }
    return filtered;
  }

  /**
   * Find a cheaper alternative for a slot within budget.
   * 
   * @param {Object} db - Database
   * @param {string} combatStyle
   * @param {string} slot
   * @param {Object} levels
   * @param {number} maxBudget
   * @param {boolean} isMember
   * @returns {Object|null}
   */
  function findCheaperAlternative(db, combatStyle, slot, levels, maxBudget, isMember) {
    // Try earlier tiers (cheaper equipment)
    const styleData = db.combat_styles && db.combat_styles[combatStyle];
    if (!styleData || !styleData.tiers) return null;

    const tiers = styleData.tiers;
    for (let i = tiers.length - 2; i >= 0; i--) {
      const tier = tiers[i];
      const gear = tier.recommended_gear || {};
      const item = gear[slot] || (slot === 'amulet' ? gear.neck : null);
      if (!item) continue;

      // Membership filter
      if (!isMember && item.f2p === false) continue;

      const price = getItemEffectivePrice(item);
      if (price > 0 && price <= maxBudget) {
        return item;
      }
    }

    return null;
  }

  /**
   * Generate a human-readable reason why an item was recommended.
   * 
   * @param {Object} item
   * @param {string} combatStyle
   * @param {Object} styleStats
   * @returns {string}
   */
  function generateReason(item, combatStyle, styleStats) {
    if (!item) return '';

    const parts = [];

    // Primary stat praise
    const primaryStat = styleStats.primary[0];
    if (item.stats && item.stats.other && item.stats.other[primaryStat]) {
      parts.push(`+${item.stats.other[primaryStat]} ${styleStats.primaryLabel}`);
    }

    // Check if it's a good value
    const price = getItemEffectivePrice(item);
    if (price > 0 && price < 50000) {
      parts.push('新手性价比之选');
    }

    // F2P tag
    if (item.f2p === true) {
      parts.push('F2P可用');
    }

    // Task/quest note
    if (item.upgrade_note) {
      // Extract key tip (first sentence)
      const tip = item.upgrade_note.split('。')[0];
      if (tip) parts.push(tip);
    }

    return parts.length > 0 ? parts.join(' · ') : '推荐装备';
  }

  // ============================================================
  //  UPGRADE PATH
  // ============================================================

  /**
   * Find the next upgrade for a specific item.
   * 
   * @param {Object} db - Database
   * @param {Object} item - Current item
   * @param {string} combatStyle
   * @returns {Object|null} Upgrade info or null
   */
  function findUpgradeForItem(db, item, combatStyle) {
    if (!item) return null;

    const itemName = item.name || '';
    const upgradeNote = item.upgrade_note || '';

    // Check upgradePaths array in the database
    const paths = db.upgradePaths || [];

    // Find a path starting from this item
    const path = paths.find(p => {
      const pFrom = p.from ? p.from.replace(/_/g, ' ').toLowerCase() : '';
      const itemKey = itemName.toLowerCase();
      return pFrom === itemKey || p.slot === (item.slot || '');
    });

    if (path) {
      return {
        from: itemName,
        to: path.to,
        slot: path.slot,
        statGain: path.statGain || {},
        priceGap: path.priceGap || 0,
        levelGap: path.levelGap || {},
        recommendedLevel: path.recommendedLevel || 0
      };
    }

    // Fallback: parse upgrade_note from database
    if (upgradeNote) {
      return {
        from: itemName,
        to: upgradeNote,
        slot: item.slot || '',
        statGain: null,
        priceGap: 0,
        note: upgradeNote
      };
    }

    return null;
  }

  /**
   * Get full upgrade path for the current loadout.
   * Premium feature.
   * 
   * @param {string} combatStyle
   * @param {Object} levels
   * @param {Object} recommendations - Current slot recommendations
   * @param {Object} db - Database
   * @returns {Array} Sorted upgrade suggestions
   */
  function getUpgradePath(combatStyle, levels, recommendations, db) {
    const upgrades = [];

    for (const slot of ALL_SLOTS) {
      const rec = recommendations[slot];
      if (!rec || !rec.item) continue;

      const upgrade = findUpgradeForItem(db, rec.item, combatStyle);
      if (upgrade) {
        // Calculate priority based on price gap and stat gain
        let priority = 'low';
        const priceGap = upgrade.priceGap || 0;

        if (priceGap <= 100000) {
          priority = 'high';
        } else if (priceGap <= 1000000) {
          priority = 'medium';
        } else {
          priority = 'low';
        }

        // Adjust priority if level gap has been met
        const levelGap = upgrade.levelGap || {};
        const levelMet = Object.keys(levelGap).every(skill => {
          return (levels[skill] || 0) >= (levelGap[skill] || 0);
        });

        if (levelMet && priority === 'low') priority = 'medium';
        if (levelMet && priority === 'medium') priority = 'high';

        upgrades.push({
          slot: slot,
          slotLabel: SLOT_LABELS[slot]?.label || slot,
          currentName: rec.item.name || 'Unknown',
          targetName: upgrade.to || 'Unknown',
          targetId: upgrade.to,
          priceGap: priceGap,
          priceGapFormatted: formatGP(priceGap),
          priority: priority,
          statGain: upgrade.statGain,
          levelGap: levelGap,
          note: upgrade.note || null
        });
      } else {
        // Check if there's an upgrade note in the tier data
        const upgradeNote = rec.item.upgrade_note;
        if (upgradeNote) {
          // Try to extract target name
          const match = upgradeNote.match(/换(.+?)([。.）\s]|$)/);
          upgrades.push({
            slot: slot,
            slotLabel: SLOT_LABELS[slot]?.label || slot,
            currentName: rec.item.name || 'Unknown',
            targetName: match ? match[1].trim() : '下一代装备',
            priceGap: 0,
            priceGapFormatted: '?',
            priority: 'medium',
            note: upgradeNote
          });
        }
      }
    }

    // Sort: high > medium > low
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    upgrades.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

    return upgrades;
  }

  // ============================================================
  //  COST CALCULATION
  // ============================================================

  /**
   * Calculate the total cost of a gear loadout.
   * 
   * @param {Object} loadout - Recommendations keyed by slot { slot: { item, price } }
   * @param {Object} [prices] - Optional price overrides
   * @returns {number} Total cost in GP
   */
  function calculateTotalCost(loadout, prices) {
    let total = 0;

    for (const slot of ALL_SLOTS) {
      const entry = loadout[slot];
      if (!entry) continue;

      if (typeof entry.price === 'number') {
        total += entry.price;
      } else if (entry.item) {
        total += getItemEffectivePrice(entry.item);
      }
    }

    return total;
  }

  // ============================================================
  //  LEVEL-TO-TIER HELPERS
  // ============================================================

  /**
   * Get the level bracket label for a given skill and level.
   * 
   * @param {Object} db
   * @param {string} skill - 'attack', 'defence', 'ranged', 'magic'
   * @param {number} level
   * @returns {string}
   */
  function getLevelBracket(db, skill, level) {
    const brackets = db.levelBrackets && db.levelBrackets[skill];
    if (!brackets) return 'Unknown';

    for (const bracket of brackets) {
      if (level >= bracket.min && level <= bracket.max) {
        return bracket.label;
      }
    }
    return 'Endgame';
  }

  /**
   * Get the price tier name from a numeric budget value (in K).
   * 
   * @param {number} budgetK - Budget in thousands
   * @returns {string} tier name
   */
  function getBudgetTierFromK(budgetK) {
    const gp = budgetK * 1000;
    if (gp <= 0) return 'unlimited';
    if (gp < 50000) return 'cheap';
    if (gp < 500000) return 'medium';
    if (gp < 50000000) return 'expensive';
    return 'biS';
  }

  /**
   * Format a budget value (in K) to display string.
   * 
   * @param {number} valK
   * @returns {string}
   */
  function formatBudget(valK) {
    const v = parseInt(valK);
    if (v === 0) return '不限';
    if (v < 1000) return v + 'K';
    return (v / 1000).toFixed(v % 1000 === 0 ? 0 : 1) + 'M';
  }

  // ============================================================
  //  UTILITY EXPORTS
  // ============================================================

  /**
   * Clear all cached data (prices, database, mapping).
   * Useful for debugging or forcing refresh.
   */
  function clearCache() {
    localStorage.removeItem(CACHE.PRICES);
    localStorage.removeItem(CACHE.TIMESTAMP);
    localStorage.removeItem(CACHE.MAPPING);
    localStorage.removeItem(CACHE.MAPPING_TS);
    localStorage.removeItem(CACHE.DATABASE);
    localStorage.removeItem(CACHE.DB_VER);
    _db = null;
    _prices = null;
    _nameToId = null;
  }

  /**
   * Get current DB version from cache.
   * @returns {string|null}
   */
  function getCachedDbVersion() {
    return localStorage.getItem(CACHE.DB_VER);
  }

  // ============================================================
  //  PUBLIC API
  // ============================================================

  const OSRSGearEngine = {
    // Data loading
    loadGearDatabase:   loadGearDatabase,
    loadGEPrices:       loadGEPrices,
    loadMapping:        loadMapping,

    // Core recommendation
    recommendGear:      recommendGear,
    getItemsForStyle:   getItemsForStyle,
    filterByBudget:     filterByBudget,
    findCheaperAlternative: findCheaperAlternative,

    // Upgrade path
    getUpgradePath:     getUpgradePath,
    findUpgradeForItem: findUpgradeForItem,

    // Cost
    calculateTotalCost: calculateTotalCost,
    getItemEffectivePrice: getItemEffectivePrice,

    // Formatting
    formatGP:           formatGP,
    parseGP:            parseGP,
    formatBudget:       formatBudget,
    getPriceTier:       getPriceTier,
    getBudgetTierFromK: getBudgetTierFromK,
    getLevelBracket:    getLevelBracket,

    // Utilities
    clearCache:         clearCache,
    getCachedDbVersion: getCachedDbVersion,

    // Constants (read-only)
    ALL_SLOTS:          ALL_SLOTS,
    SLOT_LABELS:        SLOT_LABELS,
    STYLE_CN:           STYLE_CN,
    STYLE_STATS:        STYLE_STATS,
    LEVEL_CONFIG:       LEVEL_CONFIG,
    PRICE_TIERS:        PRICE_TIERS,
    SCORE_WEIGHTS:      SCORE_WEIGHTS,
    MAX_BUDGET_K:       MAX_BUDGET_K,
    DATABASE_URL:       DATABASE_URL
  };

  return OSRSGearEngine;
}));
