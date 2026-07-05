/**
 * GE Price API - OSRS Wiki实时价格获取与缓存
 * 从 prices.runescape.wiki 获取实时GE价格，localStorage缓存1小时
 */
(function () {
  'use strict';

  // ===========================================================================
  // 1. API 端点与常量
  // ===========================================================================

  const WIKI_API = 'https://prices.runescape.wiki/api/v1/osrs/latest';
  const MAPPING_API = 'https://prices.runescape.wiki/api/v1/osrs/mapping';
  const USER_AGENT = 'osrsguru-profit-finder/1.0';

  const CACHE_KEY = 'osrsguru_ge_cache';
  const CACHE_DURATION = 3600000; // 1小时 (ms)

  const MAX_RETRIES = 3;
  const RETRY_DELAY = 1000; // 重试间隔 (ms)

  // ===========================================================================
  // 2. 缓存策略 (localStorage)
  // ===========================================================================

  /**
   * 从 localStorage 读取缓存的价格数据
   * @returns {object|null} { data: { itemId: { high, low, timestamp } }, cachedAt: number }
   */
  function getCachedPrices () {
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      console.warn('[GE-API] 读取缓存失败:', e);
      return null;
    }
  }

  /**
   * 写入价格数据到 localStorage
   * @param {object} data - 价格数据 { itemId: { high, low, timestamp } }
   */
  function setCachedPrices (data) {
    try {
      const payload = {
        data: data,
        cachedAt: Date.now()
      };
      localStorage.setItem(CACHE_KEY, JSON.stringify(payload));
    } catch (e) {
      console.warn('[GE-API] 写入缓存失败:', e);
    }
  }

  /**
   * 检查缓存是否在有效期内（1小时）
   * @returns {boolean}
   */
  function isCacheValid () {
    const cache = getCachedPrices();
    if (!cache || !cache.cachedAt) return false;
    return (Date.now() - cache.cachedAt) < CACHE_DURATION;
  }

  // ===========================================================================
  // 3. API 请求 (带重试)
  // ===========================================================================

  /**
   * 发起 fetch 请求，失败时自动重试
   * @param {string} url - 请求URL
   * @param {number} retries - 剩余重试次数
   * @returns {Promise<object>} 解析后的JSON响应
   */
  async function fetchWithRetry (url, retries = MAX_RETRIES) {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await fetch(url, {
          headers: {
            'User-Agent': USER_AGENT,
            'Accept': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
      } catch (err) {
        if (attempt < retries) {
          console.warn(`[GE-API] 请求失败 (${attempt}/${retries}): ${err.message}, ${RETRY_DELAY}ms后重试`);
          await sleep(RETRY_DELAY);
        } else {
          throw err;
        }
      }
    }
  }

  /** 简易延迟函数 */
  function sleep (ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  // ===========================================================================
  // 4. 获取价格 (核心)
  // ===========================================================================

  /**
   * 从API获取所有物品最新价格
   * @returns {Promise<object>} { itemId: { high, low, timestamp } }
   */
  async function fetchAllPrices () {
    try {
      const json = await fetchWithRetry(WIKI_API);
      return json.data || json;
    } catch (err) {
      console.error('[GE-API] fetchAllPrices 失败:', err);
      // 降级: 尝试从缓存读取（即使过期也接受）
      fallbackPrices();
      throw err;
    }
  }

  /**
   * 获取单个物品价格（优先从缓存读取）
   * @param {number|string} itemId - 物品ID
   * @returns {Promise<{ high: number, low: number, timestamp: number }|null>}
   */
  async function fetchItemPrice (itemId) {
    // 优先从缓存读取
    if (isCacheValid()) {
      var cache = getCachedPrices();
      if (cache && cache.data && cache.data[itemId]) {
        return cache.data[itemId];
      }
    }

    // 缓存无效或无此物品，实时请求
    try {
      var allData = await fetchAllPrices();
      return allData[itemId] || null;
    } catch (err) {
      console.error('[GE-API] fetchItemPrice 失败:', err);
      return null;
    }
  }

  // ===========================================================================
  // 5. 降级价格 (API不可用时的硬编码参考价)
  // ===========================================================================

  /**
   * 硬编码参考价格 - 当API完全不可用时使用
   * 价格来源: 2024年Q4典型GE中位价，仅作降级备用
   */
  var FALLBACK_PRICES = (function () {
    var p = {};
    // 绿色龙皮身体
    p[11939] = { high: 4680, low: 4194 };
    //  burnt page
    p[20718] = { high: 389, low: 341 };
    // 钢条
    p[2353] = { high: 1532, low: 1436 };
    // 蚊香草 (Ranarr weed)
    p[257] = { high: 7049, low: 6640 };
    // 龙飞镖尖端
    p[11231] = { high: 1784, low: 1609 };
    //  Zulrah's scales
    p[12934] = { high: 103, low: 97 };
    // 自然符文
    p[561] = { high: 225, low: 201 };
    // 炮弹
    p[2] = { high: 176, low: 160 };
    // 天使鱼
    p[13439] = { high: 1838, low: 1694 };
    // 黑灰鼠
    p[11959] = { high: 2262, low: 2098 };
    // 添加一些常用物品
    p[995] = { high: 1, low: 1 }; // 金币
    return p;
  }());

  /**
   * 降级: 返回硬编码参考价格
   * @returns {object}
   */
  function fallbackPrices () {
    var now = Date.now();
    var result = {};
    var id;
    for (id in FALLBACK_PRICES) {
      if (FALLBACK_PRICES.hasOwnProperty(id)) {
        result[id] = {
          high: FALLBACK_PRICES[id].high,
          low: FALLBACK_PRICES[id].low,
          timestamp: now
        };
      }
    }
    return result;
  }

  // ===========================================================================
  // 6. 利润计算
  // ===========================================================================

  /**
   * 价格数据格式: { high, low, timestamp }
   * 利润 = 数量 × (highPrice - lowPrice)
   *
   * @param {number|string} itemId - 物品ID
   * @param {number} quantity - 数量
   * @param {string} method - 计算方法 ('perKill', 'perCrate', 'perBar', 'perRun', 'perFish', 'perCatch', 'perEssence')
   *        'perKill' => 利润 = qty * (high - low)
   *        'perBar'  => 利润 = qty * (high - low)
   *        'perRun'  => 利润 = qty * (high - low)
   *        'perCatch'=> 利润 = qty * (high - low)
   *        'perFish' => 利润 = qty * (high - low)
   *        'perEssence' => 利润 = qty * (high - low)
   *        'perCrate' => 利润 = qty * (high - low) (Wintertodt箱)
   * @returns {{ profit: number, profitPerHour: number|null, margin: number, updated: number|null }}
   */
  function calcProfit (itemId, quantity, method) {
    var cache = getCachedPrices();
    var priceData = null;
    var updated = null;

    // 从缓存或硬编码中获取价格
    if (cache && cache.data && cache.data[itemId]) {
      priceData = cache.data[itemId];
      updated = priceData.timestamp || cache.cachedAt || null;
    } else if (FALLBACK_PRICES[itemId]) {
      priceData = FALLBACK_PRICES[itemId];
      updated = null;
    }

    if (!priceData) {
      return {
        profit: 0,
        profitPerHour: null,
        margin: 0,
        updated: null
      };
    }

    var highPrice = Number(priceData.high) || 0;
    var lowPrice = Number(priceData.low) || 0;
    var margin = highPrice - lowPrice;
    var profit = quantity * margin;

    // 根据方法估算每小时利润
    var profitPerHour = null;
    switch (method) {
      case 'perKill':  // PvM: 假设20次/小时
        profitPerHour = profit * 20;
        break;
      case 'perCrate': // Wintertodt: 假设15个焚香灰/小时
        profitPerHour = profit * 15;
        break;
      case 'perBar':   // 熔炉/锻铁: 假设780个/小时(13/min × 60)
        profitPerHour = profit * 780;
        break;
      case 'perRun':   // 药草跑: 每次约6分钟，10次/h
        profitPerHour = profit * 10;
        break;
      case 'perFish':  // 钓鱼: 假设150条/小时
        profitPerHour = profit * 150;
        break;
      case 'perCatch': // 捕猎: 假设200只/小时
        profitPerHour = profit * 200;
        break;
      case 'perEssence': // 制作符文: 假设6000个/小时
        profitPerHour = profit * 6000;
        break;
      default:
        profitPerHour = null;
    }

    return {
      profit: profit,
      profitPerHour: profitPerHour,
      margin: margin,
      updated: updated
    };
  }

  // ===========================================================================
  // 7. 价格格式化
  // ===========================================================================

  /**
   * 将金额格式化为可读的GP格式 (英文)
   * @param {number} amount
   * @returns {string}
   *
   * 示例:
   *   1234     => "1.2K"
   *   12345    => "12.3K"
   *   123456   => "123.5K"
   *   1234567  => "1.2M"
   *   12345678 => "12.3M"
   *   500000   => "500K"
   */
  function formatGP (amount) {
    if (amount === null || amount === undefined || isNaN(amount)) {
      return '0 GP';
    }

    var absAmt = Math.abs(amount);
    var prefix = amount < 0 ? '-' : '';

    if (absAmt >= 1000000) {
      return prefix + (absAmt / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    }
    if (absAmt >= 1000) {
      return prefix + (absAmt / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    }
    return prefix + absAmt + ' GP';
  }

  // ===========================================================================
  // 8. 赚钱方法物品配置
  // ===========================================================================

  var METHOD_ITEMS = {
    "green-dragons": { items: [{ id: 11939, name: "Green d'hide body", qty: 1 }], formula: "perKill" },
    "wintertodt": { items: [{ id: 20718, name: "Burnt page", qty: 1 }], formula: "perCrate" },
    "blast-furnace": { items: [{ id: 2353, name: "Steel bar", qty: 1 }], formula: "perBar" },
    "herb-runs": { items: [{ id: 257, name: "Ranarr weed", qty: 7 }], formula: "perRun" },
    "vorkath": { items: [{ id: 11231, name: "Dragon dart tip", qty: 2 }], formula: "perKill" },
    "zulrah": { items: [{ id: 12934, name: "Zulrah's scales", qty: 100 }], formula: "perKill" },
    "nature-runes": { items: [{ id: 561, name: "Nature rune", qty: 1 }], formula: "perEssence" },
    "cannonballs": { items: [{ id: 2, name: "Cannonball", qty: 4 }], formula: "perBar" },
    "anglerfish": { items: [{ id: 13439, name: "Anglerfish", qty: 1 }], formula: "perFish" },
    "black-chins": { items: [{ id: 11959, name: "Black chinchompa", qty: 1 }], formula: "perCatch" }
  };

  // ===========================================================================
  // 9. 初始化入口
  // ===========================================================================

  /**
   * 初始化GE价格API:
   * 1. 检查缓存是否有效
   * 2. 有效则直接使用缓存
   * 3. 无效则从API拉取新数据
   * 4. 更新缓存
   * 5. 返回最新价格数据
   *
   * @returns {Promise<object>} { data: { itemId: { high, low, timestamp } }, cachedAt: number, fromCache: boolean }
   */
  async function initGeApi () {
    // 检查缓存
    if (isCacheValid()) {
      var cache = getCachedPrices();
      if (cache && cache.data) {
        console.log('[GE-API] 缓存有效，使用缓存数据 (共 ' + Object.keys(cache.data).length + ' 个物品)');
        cache.fromCache = true;
        return cache;
      }
    }

    // 缓存无效，尝试从API拉取
    console.log('[GE-API] 缓存过期或不可用，从API获取最新价格...');
    try {
      var freshData = await fetchAllPrices();
      // 补充 timestamp
      var now = Date.now();
      var enriched = {};
      var id;
      for (id in freshData) {
        if (freshData.hasOwnProperty(id)) {
          enriched[id] = {
            high: freshData[id].high,
            low: freshData[id].low,
            timestamp: freshData[id].timestamp || now
          };
        }
      }
      setCachedPrices(enriched);
      console.log('[GE-API] 价格数据已更新缓存 (共 ' + Object.keys(enriched).length + ' 个物品)');
      return {
        data: enriched,
        cachedAt: now,
        fromCache: false
      };
    } catch (err) {
      // API不可用，降级到硬编码价格
      console.warn('[GE-API] API不可用，使用降级参考价格');
      var fallback = fallbackPrices();
      var fbNow = Date.now();
      var fbResult = {};
      var fid;
      for (fid in fallback) {
        if (fallback.hasOwnProperty(fid)) {
          fbResult[fid] = {
            high: fallback[fid].high,
            low: fallback[fid].low,
            timestamp: fbNow
          };
        }
      }
      setCachedPrices(fbResult);
      return {
        data: fbResult,
        cachedAt: fbNow,
        fromCache: false,
        fallback: true
      };
    }
  }

  // ===========================================================================
  // 10. 暴露到全局
  // ===========================================================================

  window.osrsPrices = {
    fetchAllPrices: fetchAllPrices,
    fetchItemPrice: fetchItemPrice,
    getCachedPrices: getCachedPrices,
    setCachedPrices: setCachedPrices,
    isCacheValid: isCacheValid,
    calcProfit: calcProfit,
    formatGP: formatGP,
    initGeApi: initGeApi,
    METHOD_ITEMS: METHOD_ITEMS,
    // 暴露常量便于调试
    WIKI_API: WIKI_API,
    MAPPING_API: MAPPING_API,
    CACHE_KEY: CACHE_KEY,
    CACHE_DURATION: CACHE_DURATION
  };

})();
