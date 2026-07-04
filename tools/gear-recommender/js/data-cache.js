/**
 * OSRS Gear Recommender — Data Cache Layer
 * 
 * 通用缓存管理器，支持 TTL、版本控制、自动清理。
 * 管理装备数据库（gear-database.json）的加载和缓存。
 * 当数据版本更新时自动清除旧缓存。
 * 
 * 依赖: 无（独立运行）
 * 兼容: GitHub Pages 静态托管
 * 
 * @version 1.0.0
 */

/* ========================================================================
   Cache Manager — 通用缓存管理器
   ======================================================================== */

const cacheManager = (function () {
  'use strict';

  /**
   * 创建一个缓存管理器实例
   * 
   * @param {Object} options - 配置选项
   * @param {string} options.namespace - 缓存命名空间（避免键冲突）
   * @param {number} [options.defaultTTL] - 默认过期时间（毫秒），默认 24 小时
   * @param {boolean} [options.enableVersionCheck] - 是否启用版本检查
   * @param {string} [options.versionKey] - 版本号存储键名
   * @returns {Object} 缓存管理器 API
   */
  function createCacheManager(options) {
    if (!options || !options.namespace) {
      throw new Error('[CacheManager] namespace is required');
    }

    var namespace = options.namespace;
    var defaultTTL = options.defaultTTL || 24 * 60 * 60 * 1000; // 24 小时
    var enableVersionCheck = options.enableVersionCheck !== false;
    var versionKey = options.versionKey || namespace + '_version';

    /**
     * 生成带命名空间的缓存键
     * @param {string} key - 原始键名
     * @returns {string} 带命名空间的键名
     */
    function _ns(key) {
      return 'cm_' + namespace + '_' + key;
    }

    /**
     * 安全的 localStorage 读取
     */
    function _safeGet(key) {
      try {
        var raw = localStorage.getItem(_ns(key));
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        console.warn('[CacheManager:' + namespace + '] Read error:', e);
        return null;
      }
    }

    /**
     * 安全的 localStorage 写入
     */
    function _safeSet(key, value) {
      try {
        localStorage.setItem(_ns(key), JSON.stringify(value));
        return true;
      } catch (e) {
        console.warn('[CacheManager:' + namespace + '] Write error (quota?):', e);
        return false;
      }
    }

    /**
     * 安全的删除
     */
    function _safeRemove(key) {
      try {
        localStorage.removeItem(_ns(key));
      } catch (e) {
        console.warn('[CacheManager:' + namespace + '] Remove error:', e);
      }
    }

    /**
     * 读取缓存的条目（含 TTL 检查）
     * @param {string} key - 缓存键名
     * @returns {*|null} 缓存的数据，过期或不存在返回 null
     */
    function get(key) {
      var entry = _safeGet(key);
      if (!entry) return null;

      // 检查 TTL
      if (entry.expiresAt && Date.now() > entry.expiresAt) {
        console.log('[CacheManager:' + namespace + '] Cache expired:', key);
        remove(key);
        return null;
      }

      return entry.data;
    }

    /**
     * 写入缓存条目
     * @param {string} key - 缓存键名
     * @param {*} data - 要缓存的数据
     * @param {number} [ttl] - 可选，自定义过期时间（毫秒）
     * @returns {boolean} 是否写入成功
     */
    function set(key, data, ttl) {
      var expiresAt = Date.now() + (ttl || defaultTTL);

      var entry = {
        data: data,
        createdAt: Date.now(),
        expiresAt: expiresAt,
        namespace: namespace
      };

      return _safeSet(key, entry);
    }

    /**
     * 删除缓存条目
     * @param {string} key - 缓存键名
     */
    function remove(key) {
      _safeRemove(key);
    }

    /**
     * 检查缓存是否存在且未过期
     * @param {string} key - 缓存键名
     * @returns {boolean}
     */
    function has(key) {
      var entry = _safeGet(key);
      if (!entry) return false;
      if (entry.expiresAt && Date.now() > entry.expiresAt) {
        remove(key);
        return false;
      }
      return true;
    }

    /**
     * 清理所有属于此命名空间的缓存
     * @param {number} [maxAge] - 仅清理超过指定毫秒数的旧缓存
     */
    function clear(maxAge) {
      try {
        var prefix = 'cm_' + namespace + '_';
        var keysToRemove = [];

        for (var i = 0; i < localStorage.length; i++) {
          var storageKey = localStorage.key(i);
          if (storageKey && storageKey.indexOf(prefix) === 0) {
            if (maxAge) {
              try {
                var raw = localStorage.getItem(storageKey);
                var entry = raw ? JSON.parse(raw) : null;
                if (entry && entry.createdAt && (Date.now() - entry.createdAt) < maxAge) {
                  continue; // 未达到最大年龄，跳过
                }
              } catch (e) {
                // 解析失败则删除
              }
            }
            keysToRemove.push(storageKey);
          }
        }

        keysToRemove.forEach(function (k) {
          try { localStorage.removeItem(k); } catch (e) {}
        });

        console.log('[CacheManager:' + namespace + '] Cleared', keysToRemove.length, 'entries');
        return keysToRemove.length;
      } catch (e) {
        console.warn('[CacheManager:' + namespace + '] Clear error:', e);
        return 0;
      }
    }

    /**
     * 设置/获取版本号
     * @param {string} [version] - 要设置的版本号，不传则读取
     * @returns {string|null} 当前版本号
     */
    function version(version) {
      if (version !== undefined) {
        _safeSet('_version', version);
        return version;
      }
      var v = _safeGet('_version');
      return v ? v.data || v : null;
    }

    /**
     * 获取缓存统计信息
     * @returns {{ totalKeys: number, namespaceKeys: number, keys: string[] }}
     */
    function stats() {
      var statsResult = {
        totalKeys: 0,
        namespaceKeys: 0,
        keys: []
      };

      try {
        var prefix = 'cm_' + namespace + '_';
        for (var i = 0; i < localStorage.length; i++) {
          statsResult.totalKeys++;
          var storageKey = localStorage.key(i);
          if (storageKey && storageKey.indexOf(prefix) === 0) {
            statsResult.namespaceKeys++;
            statsResult.keys.push(storageKey.replace(prefix, ''));
          }
        }
      } catch (e) {}

      return statsResult;
    }

    // 返回公共 API
    return {
      get: get,
      set: set,
      remove: remove,
      has: has,
      clear: clear,
      version: version,
      stats: stats,
      namespace: namespace
    };
  }

  /* ========================================================================
     Public API
     ======================================================================== */

  return {
    createCacheManager: createCacheManager
  };
})();

/* ========================================================================
   Gear Database Cache — 装备数据库缓存（基于 cacheManager）
   ======================================================================== */

/**
 * 装备数据库缓存实例
 * 
 * 管理 gear-database.json 的加载、缓存和版本控制。
 * 使用内存缓存（最快）+ localStorage 缓存（持久化）的双层策略。
 */
const gearDatabaseCache = (function () {
  'use strict';

  /** 数据库 URL */
  var DB_URL = 'data/gear-database.json';

  /** 数据库缓存管理器 */
  var dbCache = cacheManager.createCacheManager({
    namespace: 'gear_db',
    defaultTTL: 7 * 24 * 60 * 60 * 1000, // 7 天（装备数据不频繁变化）
    enableVersionCheck: true
  });

  /** 内存缓存 */
  var _memoryCache = null;

  /** 数据是否正在加载 */
  var _loading = false;

  /** 等待加载完成的 Promise 队列 */
  var _loadQueue = [];

  /** 当前已知的数据库版本（从 HTML meta 或 JS 常量获取） */
  var _expectedVersion = null;

  /**
   * 设置期望版本号（可在 HTML 中通过脚本设置）
   * @param {string} version - 语义化版本号，如 "1.2.0"
   */
  function setExpectedVersion(version) {
    _expectedVersion = version;
  }

  /**
   * 缓存装备数据
   * 
   * @param {Object} data - gear-database.json 的完整数据对象
   * @param {string} [version] - 数据的版本号，用于版本校验
   */
  function cacheGearDatabase(data, version) {
    if (!data) {
      console.warn('[GearDB] Attempted to cache null data');
      return false;
    }

    // 写入缓存管理器
    var saved = dbCache.set('database', data);

    // 记录版本号
    var dbVersion = version || (data.meta && data.meta.version) || 'unknown';
    dbCache.version(dbVersion);

    // 同时写入内存缓存
    _memoryCache = data;

    console.log('[GearDB] Database cached, version:', dbVersion);
    return saved;
  }

  /**
   * 从缓存获取装备数据库
   * 
   * 优先级：内存 → localStorage → 网络加载
   * 
   * @param {boolean} [forceRefresh=false] - 强制从网络加载
   * @returns {Promise<Object|null>} gear-database.json 数据
   */
  async function getCachedGearDatabase(forceRefresh) {
    if (forceRefresh === undefined) forceRefresh = false;

    console.log('[GearDB] getCachedGearDatabase called' + (forceRefresh ? ' (force refresh)' : ''));

    // 1. 内存缓存（最快）
    if (_memoryCache && !forceRefresh) {
      console.log('[GearDB] Using memory cache');
      return _memoryCache;
    }

    // 2. 如果正在加载，加入等待队列
    if (_loading) {
      return new Promise(function (resolve) {
        _loadQueue.push(resolve);
      });
    }

    // 3. 检查 localStorage 缓存（版本校验）
    if (!forceRefresh) {
      var cached = dbCache.get('database');
      var cachedVersion = dbCache.version();

      if (cached) {
        // 版本检查：如果版本不一致，清除缓存重新加载
        if (_expectedVersion && cachedVersion && cachedVersion !== _expectedVersion) {
          console.log('[GearDB] Version mismatch: expected', _expectedVersion, 'cached', cachedVersion);
          dbCache.remove('database');
        } else {
          _memoryCache = cached;
          console.log('[GearDB] Using localStorage cache, version:', cachedVersion);
          return cached;
        }
      }
    }

    // 4. 网络加载
    _loading = true;

    try {
      console.log('[GearDB] Fetching from network:', DB_URL);
      var response = await fetch(DB_URL);

      if (!response.ok) {
        throw new Error('HTTP ' + response.status + ' ' + response.statusText);
      }

      var data = await response.json();

      // 校验基本结构
      if (!data || !data.meta) {
        throw new Error('Invalid database structure: missing meta');
      }

      // 缓存
      var version = data.meta && data.meta.version;
      cacheGearDatabase(data, version);

      console.log('[GearDB] Loaded from network, version:', version);
      return data;
    } catch (err) {
      console.error('[GearDB] Network load failed:', err.message);

      // 降级：使用过期的 localStorage 缓存
      var staleCache = dbCache.get('database');
      if (staleCache) {
        console.warn('[GearDB] Using stale cache (data may be outdated)');
        _memoryCache = staleCache;
        return staleCache;
      }

      console.error('[GearDB] No cache available, data unavailable');
      return null;
    } finally {
      _loading = false;

      // 通知所有等待者
      _loadQueue.forEach(function (resolve) {
        resolve(_memoryCache);
      });
      _loadQueue = [];
    }
  }

  /**
   * 获取当前缓存的版本号
   * @returns {string|null}
   */
  function getCachedVersion() {
    return dbCache.version();
  }

  /**
   * 清理所有数据库缓存
   */
  function clearDatabaseCache() {
    _memoryCache = null;
    dbCache.remove('database');
    dbCache.remove('_version');
    console.log('[GearDB] Cache cleared');
  }

  /**
   * 获取数据库缓存状态
   * @returns {{ inMemory: boolean, inLocalStorage: boolean, version: string|null, loading: boolean }}
   */
  function getDatabaseStatus() {
    return {
      inMemory: !!_memoryCache,
      inLocalStorage: dbCache.has('database'),
      version: dbCache.version(),
      loading: _loading,
      expectedVersion: _expectedVersion
    };
  }

  /* ========================================================================
     Expose Public API
     ======================================================================== */

  return {
    setExpectedVersion: setExpectedVersion,
    cacheGearDatabase: cacheGearDatabase,
    getCachedGearDatabase: getCachedGearDatabase,
    getCachedVersion: getCachedVersion,
    clearDatabaseCache: clearDatabaseCache,
    getDatabaseStatus: getDatabaseStatus,

    // 底层缓存管理器（高级用途）
    cacheManager: dbCache
  };
})();

/* ========================================================================
   Auto-cleanup — 自动清理过期缓存（页面加载时运行）
   ======================================================================== */

(function autoCleanup() {
  try {
    // 清理所有超过 30 天未使用的缓存数据
    var thirtyDays = 30 * 24 * 60 * 60 * 1000;

    for (var i = 0; i < localStorage.length; i++) {
      var key = localStorage.key(i);
      if (key && key.indexOf('cm_') === 0) {
        try {
          var raw = localStorage.getItem(key);
          var entry = raw ? JSON.parse(raw) : null;
          if (entry && entry.expiresAt && Date.now() > entry.expiresAt) {
            localStorage.removeItem(key);
          }
        } catch (e) {
          // 无法解析的条目可能损坏，删除
          localStorage.removeItem(key);
        }
      }
    }
  } catch (e) {
    // 静默失败
  }
})();
