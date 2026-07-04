/**
 * OSRS Gear Recommender — GE Price Management Module
 * 
 * 管理来自 OSRS Wiki API 的实时价格数据。
 * 使用 localStorage 缓存策略，API 不可用时降级到 gear-database.json 的静态预估价格。
 * 
 * 依赖: 无
 * 兼容: GitHub Pages 静态托管
 * 
 * @version 1.0.0
 * @see https://prices.runescape.wiki/api/v1/osrs/latest
 */

/* ========================================================================
   Constants & Configuration
   ======================================================================== */

const GE_PRICES = (function () {
  'use strict';

  /** localStorage 缓存键名 */
  const CACHE_KEYS = {
    PRICES: 'osrs_ge_prices_data',
    MAPPING: 'osrs_ge_name_to_id',
    TIMESTAMP: 'osrs_ge_fetch_timestamp',
    MAPPING_TIMESTAMP: 'osrs_ge_mapping_timestamp',
    VERSION: 'osrs_ge_data_version'
  };

  /** 缓存有效期：24 小时（价格每天更新一次） */
  const CACHE_TTL_MS = 24 * 60 * 60 * 1000;

  /** 映射缓存有效期：7 天（物品 ID 映射几乎不变） */
  const MAPPING_CACHE_TTL_MS = 7 * 24 * 60 * 60 * 1000;

  /** Wiki API 端点 */
  const API = {
    LATEST: 'https://prices.runescape.wiki/api/v1/osrs/latest',
    MAPPING: 'https://prices.runescape.wiki/api/v1/osrs/mapping'
  };

  /** 请求头：Wiki 要求提供 User-Agent */
  const REQUEST_HEADERS = {
    'User-Agent': 'OSRS Guru Gear Recommender/1.0 (https://osrsguru.com)',
    'Accept': 'application/json'
  };

  /** API 限流保护：上次请求时间戳 */
  let _lastApiCall = 0;

  /** API 调用最小间隔（毫秒） */
  const API_RATE_LIMIT_MS = 6000;

  /** 内存中的价格数据（避免反复读 localStorage） */
  let _pricesCache = null;

  /** 内存中的映射数据 */
  let _mappingCache = null;

  /* ========================================================================
     Internal Helpers
     ======================================================================== */

  /**
   * 安全的 localStorage 读取
   * @param {string} key - 缓存键名
   * @returns {*} 解析后的数据，或 null
   */
  function _safeGetItem(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      console.warn('[GE Price] localStorage read error for', key, e);
      return null;
    }
  }

  /**
   * 安全的 localStorage 写入
   * @param {string} key - 缓存键名
   * @param {*} value - 要存储的数据
   */
  function _safeSetItem(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.warn('[GE Price] localStorage write error (quota exceeded?):', e);
    }
  }

  /**
   * 检查缓存是否过期
   * @param {string} timestampKey - 时间戳缓存键名
   * @param {number} ttlMs - 过期时间（毫秒）
   * @returns {boolean} true 表示缓存有效
   */
  function _isCacheValid(timestampKey, ttlMs) {
    const ts = localStorage.getItem(timestampKey);
    if (!ts) return false;
    return (Date.now() - parseInt(ts, 10)) < ttlMs;
  }

  /**
   * 遵守 API 频率限制
   */
  async function _rateLimit() {
    const now = Date.now();
    const elapsed = now - _lastApiCall;
    if (elapsed < API_RATE_LIMIT_MS) {
      const wait = API_RATE_LIMIT_MS - elapsed;
      console.log('[GE Price] Rate limiting: waiting', wait, 'ms');
      await new Promise(function (resolve) { setTimeout(resolve, wait); });
    }
    _lastApiCall = Date.now();
  }

  /**
   * 执行 API 请求（带重试和降级）
   * @param {string} url - API URL
   * @param {number} retries - 重试次数
   * @returns {Promise<Object|null>} JSON 响应，或 null
   */
  async function _fetchWithRetry(url, retries) {
    if (retries === undefined) retries = 2;

    for (var attempt = 0; attempt <= retries; attempt++) {
      try {
        await _rateLimit();

        console.log('[GE Price] Fetching:', url, '(attempt', (attempt + 1) + '/' + (retries + 1) + ')');

        var response = await fetch(url, { headers: REQUEST_HEADERS });

        if (!response.ok) {
          throw new Error('HTTP ' + response.status + ' ' + response.statusText);
        }

        return await response.json();
      } catch (err) {
        console.warn('[GE Price] Fetch attempt', (attempt + 1), 'failed:', err.message);

        if (attempt < retries) {
          // 指数退避：1s, 2s
          var backoff = (attempt + 1) * 1000;
          await new Promise(function (resolve) { setTimeout(resolve, backoff); });
        }
      }
    }

    return null;
  }

  /* ========================================================================
     Public API
     ======================================================================== */

  /**
   * 从 OSRS Wiki API 获取最新 GE 价格
   * 
   * 获取/item mapping → 建立 name → osrsId 映射
   * 获取 latest prices → 建立 osrsId → { high, low } 映射
   * 两套数据缓存到 localStorage
   * 
   * @param {boolean} [forceRefresh=false] - 强制刷新缓存
   * @returns {Promise<Object|null>} 价格数据对象 { [itemName]: { high, low, avg } }，或 null
   */
  async function fetchGEPrices(forceRefresh) {
    if (forceRefresh === undefined) forceRefresh = false;

    console.log('[GE Price] fetchGEPrices called' + (forceRefresh ? ' (force refresh)' : ''));

    // 1. 获取 ID 映射（mapping）
    var mapping = _mappingCache;
    if (!mapping || forceRefresh || !_isCacheValid(CACHE_KEYS.MAPPING_TIMESTAMP, MAPPING_CACHE_TTL_MS)) {
      var mappingResponse = await _fetchWithRetry(API.MAPPING);

      if (mappingResponse && mappingResponse.data) {
        mapping = {};
        for (var i = 0; i < mappingResponse.data.length; i++) {
          var item = mappingResponse.data[i];
          mapping[item.name.toLowerCase()] = item.id;
        }
        _safeSetItem(CACHE_KEYS.MAPPING, mapping);
        localStorage.setItem(CACHE_KEYS.MAPPING_TIMESTAMP, String(Date.now()));
        _mappingCache = mapping;
        console.log('[GE Price] Mapping updated:', Object.keys(mapping).length, 'items');
      } else {
        // 降级：使用缓存映射
        mapping = _safeGetItem(CACHE_KEYS.MAPPING) || {};
        _mappingCache = mapping;
        console.warn('[GE Price] Mapping fetch failed, using cached mapping');
      }
    } else {
      console.log('[GE Price] Using cached mapping');
    }

    // 2. 获取最新价格
    var pricesData = null;

    // 检查缓存是否有效
    if (!forceRefresh && _isCacheValid(CACHE_KEYS.TIMESTAMP, CACHE_TTL_MS)) {
      var cached = _safeGetItem(CACHE_KEYS.PRICES);
      if (cached) {
        _pricesCache = cached;
        console.log('[GE Price] Using cached price data');
        return cached;
      }
    }

    var pricesResponse = await _fetchWithRetry(API.LATEST);

    if (pricesResponse && pricesResponse.data) {
      // 转换 raw data: { osrsId: { high, low } } → { itemName: { high, low, avg } }
      var transformed = {};
      var rawData = pricesResponse.data;

      for (var osrsId in rawData) {
        if (Object.prototype.hasOwnProperty.call(rawData, osrsId)) {
          var pricePoint = rawData[osrsId];
          var high = pricePoint.high || 0;
          var low = pricePoint.low || 0;
          var avg = (high + low) > 0 ? Math.round((high + low) / 2) : 0;

          // 通过 osrsId 反向查找名称（不常用）
          // 主要存储 ID 索引的价格
          transformed[osrsId] = {
            high: high,
            low: low,
            avg: avg
          };
        }
      }

      // 缓存
      _safeSetItem(CACHE_KEYS.PRICES, transformed);
      localStorage.setItem(CACHE_KEYS.TIMESTAMP, String(Date.now()));
      _pricesCache = transformed;

      console.log('[GE Price] Prices updated:', Object.keys(transformed).length, 'items');
      return transformed;
    }

    // 3. 降级链：缓存 → null
    console.warn('[GE Price] API fetch failed, using stale cache');
    var fallback = _safeGetItem(CACHE_KEYS.PRICES);
    _pricesCache = fallback || null;
    return _pricesCache;
  }

  /**
   * 从 localStorage 获取缓存的 GE 价格
   * @returns {Object|null} 缓存的价格数据
   */
  function getCachedPrices() {
    if (_pricesCache) return _pricesCache;

    _pricesCache = _safeGetItem(CACHE_KEYS.PRICES);
    return _pricesCache;
  }

  /**
   * 更新价格数据（带频率限制：每天最多更新一次）
   * 
   * 如果当天已经更新过，则跳过。
   * 适用于页面初始化时自动调用。
   * 
   * @returns {Promise<Object|null>} 更新后的价格数据
   */
  async function updatePrices() {
    console.log('[GE Price] updatePrices called');

    // 检查当天是否已更新
    var lastUpdate = localStorage.getItem(CACHE_KEYS.TIMESTAMP);
    var today = new Date();
    var todayStr = today.toISOString().slice(0, 10); // YYYY-MM-DD

    if (lastUpdate) {
      var lastDate = new Date(parseInt(lastUpdate, 10));
      var lastStr = lastDate.toISOString().slice(0, 10);

      if (lastStr === todayStr) {
        console.log('[GE Price] Already updated today, skipping');
        return getCachedPrices();
      }
    }

    // 强制刷新获取新数据
    var prices = await fetchGEPrices(true);
    return prices;
  }

  /**
   * 通过物品名称获取单个物品的当前价格
   * 
   * 先尝试从 mapping 找 osrsId → 从 prices 获取实时价格
   * 降级到返回 null（由调用方使用 gear-database.json 的静态价格）
   * 
   * @param {string} itemName - 物品名称（不区分大小写）
   * @param {Object} [pricesData] - 可选，已加载的价格数据
   * @param {Object} [mappingData] - 可选，已加载的映射数据
   * @returns {{ high: number, low: number, avg: number }|null}
   */
  function getPrice(itemName, pricesData, mappingData) {
    if (!itemName) return null;

    var name = itemName.toLowerCase().trim();
    var prices = pricesData || _pricesCache || _safeGetItem(CACHE_KEYS.PRICES);
    var mapping = mappingData || _mappingCache || _safeGetItem(CACHE_KEYS.MAPPING);

    if (!prices || !mapping) return null;

    // 通过名称找到 osrs ID
    var osrsId = mapping[name];
    if (!osrsId) {
      // 尝试部分匹配
      for (var mapName in mapping) {
        if (Object.prototype.hasOwnProperty.call(mapping, mapName)) {
          if (mapName.indexOf(name) !== -1 || name.indexOf(mapName) !== -1) {
            osrsId = mapping[mapName];
            break;
          }
        }
      }
    }

    if (!osrsId) return null;

    var priceData = prices[String(osrsId)];
    if (!priceData) return null;

    return {
      high: priceData.high || 0,
      low: priceData.low || 0,
      avg: priceData.avg || Math.round(((priceData.high || 0) + (priceData.low || 0)) / 2)
    };
  }

  /**
   * 格式化价格显示
   * 
   * 规则：
   *   >= 1,000,000,000 → 1.2B
   *   >= 1,000,000     → 1.2M
   *   >= 1,000         → 350K
   *   < 1,000          → 原样显示
   *   = 0              → "Free"
   * 
   * @param {number} gp - 游戏内的金币数量
   * @returns {string} 格式化后的价格字符串
   */
  function formatPrice(gp) {
    if (gp === null || gp === undefined) return 'N/A';

    var price = Number(gp);
    if (isNaN(price)) return 'N/A';
    if (price === 0) return 'Free';

    var absPrice = Math.abs(price);
    var sign = price < 0 ? '-' : '';

    if (absPrice >= 1000000000) {
      return sign + (absPrice / 1000000000).toFixed(1) + 'B';
    }
    if (absPrice >= 1000000) {
      return sign + (absPrice / 1000000).toFixed(1) + 'M';
    }
    if (absPrice >= 1000) {
      return sign + (absPrice / 1000).toFixed(0) + 'K';
    }
    return sign + String(absPrice);
  }

  /**
   * 根据价格获取价格区间分类
   * 
   * @param {number} price - 物品价格
   * @returns {string} price tier: 'free' | 'cheap' | 'medium' | 'expensive' | 'biS'
   */
  function getPriceCategory(price) {
    if (price === 0) return 'free';
    if (price < 50000) return 'cheap';
    if (price < 500000) return 'medium';
    if (price < 50000000) return 'expensive';
    return 'biS';
  }

  /**
   * 清理所有缓存的价格数据
   */
  function clearPriceCache() {
    try {
      localStorage.removeItem(CACHE_KEYS.PRICES);
      localStorage.removeItem(CACHE_KEYS.TIMESTAMP);
      localStorage.removeItem(CACHE_KEYS.MAPPING);
      localStorage.removeItem(CACHE_KEYS.MAPPING_TIMESTAMP);
      _pricesCache = null;
      _mappingCache = null;
      console.log('[GE Price] Cache cleared');
    } catch (e) {
      console.warn('[GE Price] Cache clear error:', e);
    }
  }

  /**
   * 获取价格数据的状态信息
   * @returns {{ cached: boolean, timestamp: string|null, age: number|null }}
   */
  function getPriceStatus() {
    var ts = localStorage.getItem(CACHE_KEYS.TIMESTAMP);
    var cached = !!_pricesCache || !!localStorage.getItem(CACHE_KEYS.PRICES);

    return {
      cached: cached,
      timestamp: ts ? new Date(parseInt(ts, 10)).toISOString() : null,
      age: ts ? (Date.now() - parseInt(ts, 10)) : null
    };
  }

  /* ========================================================================
     Expose Public API as Global Object
     ======================================================================== */

  return {
    fetchGEPrices: fetchGEPrices,
    getCachedPrices: getCachedPrices,
    updatePrices: updatePrices,
    getPrice: getPrice,
    formatPrice: formatPrice,
    getPriceCategory: getPriceCategory,
    clearPriceCache: clearPriceCache,
    getPriceStatus: getPriceStatus,

    // 常量暴露（供调试/测试）
    CACHE_KEYS: CACHE_KEYS,
    CACHE_TTL_MS: CACHE_TTL_MS
  };
})();
