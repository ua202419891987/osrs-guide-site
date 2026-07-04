/**
 * OSRS Gear Recommender — Subscription Management Module
 * 
 * 管理免费/付费用户分层、使用次数跟踪、订阅验证。
 * 纯前端方案：使用 localStorage 存储订阅状态。
 * 付费用户数据通过本地 token 验证（简单方案，无后端依赖）。
 * 
 * 付费方案: $1.9/月
 * 支付方式: Stripe Payment Link / PayPal
 * 
 * 依赖: 无
 * 兼容: GitHub Pages 静态托管
 * 
 * @version 1.0.0
 */

/* ========================================================================
   Constants & Configuration
   ======================================================================== */

const subscriptionManager = (function () {
  'use strict';

  /** localStorage 键名 */
  var STORAGE_KEYS = {
    SUBSCRIPTION_TOKEN: 'osrsguru_premium_token',
    SUBSCRIPTION_DATA: 'osrsguru_premium_data',
    USAGE_COUNT: 'osrsguru_usage_count',
    USAGE_DATE: 'osrsguru_usage_date',
    LAST_QUERY_DATE: 'osrsguru_last_query_date',
    QUERY_COUNT_TODAY: 'osrsguru_query_count_today'
  };

  /**
   * 功能矩阵
   * 免费层 vs 付费层功能对比
   */
  var FEATURES = {
    FREE: {
      label: 'Free',
      maxQueriesPerDay: 3,
      maxCombatStyles: 1,
      budgetPresets: true,        // 预设4档预算
      exactBudgetInput: false,    // 精确预算金额输入
      upgradePaths: false,        // 升级路径
      saveBuilds: false,          // 保存搭配
      maxSavedBuilds: 0,
      exportBuilds: false,        // 导出搭配
      adFree: false,              // 去广告
      multiStyleCompare: false,   // 多战斗风格对比
      showQuestLocked: false,     // 显示任务锁定物品
      degradeWarning: true        // 降解警告
    },
    PREMIUM: {
      label: 'Premium',
      maxQueriesPerDay: Infinity,
      maxCombatStyles: Infinity,
      budgetPresets: true,
      exactBudgetInput: true,
      upgradePaths: true,
      saveBuilds: true,
      maxSavedBuilds: 50,
      exportBuilds: true,
      adFree: true,
      multiStyleCompare: true,
      showQuestLocked: true,
      degradeWarning: true
    }
  };

  /** 订阅价格 */
  var SUBSCRIPTION_PRICE = 1.9; // $1.9/月

  /** Stripe Payment Link（替换为实际的 Stripe 链接） */
  var STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/your_stripe_link_here';

  /** PayPal 订阅链接（替换为实际的 PayPal 链接） */
  var PAYPAL_SUBSCRIPTION_LINK = 'https://www.paypal.com/webapps/billing/your_subscription_link_here';

  /** Token 有效期：30 天（配合月付周期） */
  var TOKEN_TTL_MS = 30 * 24 * 60 * 60 * 1000;

  /* ========================================================================
     Internal State
     ======================================================================== */

  /** 内存中的订阅数据 */
  var _subscriptionData = null;

  /** 内存中的 token */
  var _token = null;

  /** 监听器列表 */
  var _listeners = [];

  /* ========================================================================
     Internal Helpers
     ======================================================================== */

  /**
   * 安全的 localStorage 读取
   */
  function _safeGet(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  /**
   * 安全的 localStorage 写入
   */
  function _safeSet(key, value) {
    try {
      localStorage.setItem(key, value);
      return true;
    } catch (e) {
      console.warn('[Subscription] localStorage write error:', e);
      return false;
    }
  }

  /**
   * 安全的 JSON 读取
   */
  function _safeGetJSON(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  /**
   * 安全的 JSON 写入
   */
  function _safeSetJSON(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      return false;
    }
  }

  /**
   * 安全删除
   */
  function _safeRemove(key) {
    try {
      localStorage.removeItem(key);
    } catch (e) {}
  }

  /**
   * 通知所有状态监听器
   */
  function _notifyListeners() {
    var status = getSubscriptionStatus();
    _listeners.forEach(function (listener) {
      try {
        listener(status);
      } catch (e) {
        console.warn('[Subscription] Listener error:', e);
      }
    });
  }

  /* ========================================================================
     Token Management
     ======================================================================== */

  /**
   * 生成简单的本地 token
   * 注意：这是前端的简单方案，正式生产环境应使用 Cloudflare Worker 验证
   * 
   * @param {Object} payload - token 载荷
   * @returns {string} base64 编码的 token
   */
  function _generateLocalToken(payload) {
    var header = { alg: 'none', typ: 'simple-token' };
    var now = Date.now();

    var fullPayload = {
      sub: payload.userId || 'local_user_' + now,
      exp: now + TOKEN_TTL_MS,
      iat: now,
      tier: 'premium',
      features: FEATURES.PREMIUM,
      source: payload.source || 'local'
    };

    // 简单 base64 编码（非加密，仅用于本地验证）
    var encoded = btoa(JSON.stringify({ header: header, payload: fullPayload }));
    return 'osrs_' + encoded;
  }

  /**
   * 解码本地 token
   * @param {string} token - token 字符串
   * @returns {Object|null} 解码后的 payload
   */
  function _decodeLocalToken(token) {
    if (!token || token.indexOf('osrs_') !== 0) return null;

    try {
      var encoded = token.slice(5); // 去掉 'osrs_' 前缀
      var decoded = JSON.parse(atob(encoded));
      return decoded.payload || null;
    } catch (e) {
      return null;
    }
  }

  /**
   * 检查 token 是否过期
   * @param {Object} payload - decoded payload
   * @returns {boolean}
   */
  function _isTokenExpired(payload) {
    return payload.exp && payload.exp < Date.now();
  }

  /* ========================================================================
     Public API — 订阅状态管理
     ======================================================================== */

  /**
   * 初始化订阅管理器（页面加载时调用）
   * 从 localStorage 恢复 token 和订阅数据
   */
  function init() {
    console.log('[Subscription] Initializing...');

    _token = _safeGet(STORAGE_KEYS.SUBSCRIPTION_TOKEN);
    _subscriptionData = _safeGetJSON(STORAGE_KEYS.SUBSCRIPTION_DATA);

    if (_token) {
      var payload = _decodeLocalToken(_token);
      if (payload && !_isTokenExpired(payload)) {
        console.log('[Subscription] Token valid, tier: premium');
        _subscriptionData = {
          tier: 'premium',
          features: payload.features || FEATURES.PREMIUM,
          expiresAt: payload.exp,
          source: payload.source || 'unknown'
        };
        _safeSetJSON(STORAGE_KEYS.SUBSCRIPTION_DATA, _subscriptionData);
      } else {
        // Token 过期
        console.log('[Subscription] Token expired');
        _token = null;
        _subscriptionData = null;
        _safeRemove(STORAGE_KEYS.SUBSCRIPTION_TOKEN);
        _safeRemove(STORAGE_KEYS.SUBSCRIPTION_DATA);
      }
    }

    _notifyListeners();
    console.log('[Subscription] Initialized, tier:', getCurrentTier());
  }

  /**
   * 获取当前用户层级
   * @returns {string} 'free' | 'premium'
   */
  function getCurrentTier() {
    if (_subscriptionData && _subscriptionData.tier === 'premium') {
      return 'premium';
    }
    return 'free';
  }

  /**
   * 检查用户是否已付费
   * @returns {boolean}
   */
  function isPremium() {
    return getCurrentTier() === 'premium';
  }

  /**
   * 检查用户是否可以使用某个功能
   * @param {string} featureName - 功能名称
   * @returns {boolean}
   */
  function hasFeature(featureName) {
    var tier = getCurrentTier();

    if (tier === 'premium') {
      return _subscriptionData.features[featureName] === true;
    }

    return FEATURES.FREE[featureName] === true;
  }

  /**
   * 获取当前用户的功能列表
   * @returns {Object} 功能配置对象
   */
  function getFeatures() {
    var tier = getCurrentTier();
    return tier === 'premium' ? FEATURES.PREMIUM : FEATURES.FREE;
  }

  /**
   * 检查用户订阅状态（完整状态）
   * @returns {Object} 订阅状态对象
   */
  function checkUserTier() {
    var tier = getCurrentTier();
    var features = getFeatures();

    return {
      tier: tier,
      label: features.label,
      isPremium: tier === 'premium',
      features: features,
      expiresAt: _subscriptionData ? _subscriptionData.expiresAt : null,
      daysRemaining: _subscriptionData ? Math.floor((_subscriptionData.expiresAt - Date.now()) / (24 * 60 * 60 * 1000)) : 0
    };
  }

  /**
   * 获取订阅状态摘要（简化版）
   * @returns {{ tier: string, isPremium: boolean }}
   */
  function getSubscriptionStatus() {
    return {
      tier: getCurrentTier(),
      isPremium: isPremium()
    };
  }

  /* ========================================================================
     Public API — 使用次数跟踪
     ======================================================================== */

  /**
   * 获取今天的日期字符串（YYYY-MM-DD）
   */
  function _getTodayStr() {
    var d = new Date();
    return d.getFullYear() + '-' +
           String(d.getMonth() + 1).padStart(2, '0') + '-' +
           String(d.getDate()).padStart(2, '0');
  }

  /**
   * 检查并重置每日计数
   */
  function _checkAndResetDaily() {
    var today = _getTodayStr();
    var lastDate = _safeGet(STORAGE_KEYS.QUERY_COUNT_TODAY + '_date');

    if (lastDate !== today) {
      _safeSet(STORAGE_KEYS.QUERY_COUNT_TODAY, '0');
      _safeSet(STORAGE_KEYS.QUERY_COUNT_TODAY + '_date', today);
      return 0;
    }

    var count = parseInt(_safeGet(STORAGE_KEYS.QUERY_COUNT_TODAY), 10);
    return isNaN(count) ? 0 : count;
  }

  /**
   * 记录一次使用
   * 跟踪每日查询次数，免费用户有上限
   * 
   * @returns {Object} { allowed: boolean, remaining: number, tier: string }
   */
  function trackUsage() {
    var tier = getCurrentTier();
    var features = getFeatures();

    // 付费用户无限
    if (tier === 'premium') {
      return {
        allowed: true,
        remaining: Infinity,
        tier: 'premium'
      };
    }

    // 免费用户检查每日限制
    var todayCount = _checkAndResetDaily();
    var maxQueries = features.maxQueriesPerDay;

    todayCount = todayCount + 1; // 本次查询
    _safeSet(STORAGE_KEYS.QUERY_COUNT_TODAY, String(todayCount));

    var allowed = todayCount <= maxQueries;
    var remaining = Math.max(0, maxQueries - todayCount);

    console.log('[Subscription] Usage tracked: today=' + todayCount + ', allowed=' + allowed + ', remaining=' + remaining);

    return {
      allowed: allowed,
      remaining: remaining,
      tier: 'free'
    };
  }

  /**
   * 获取当前使用统计
   * @returns {{ queriesToday: number, maxQueries: number, remaining: number, tier: string }}
   */
  function getUsageStats() {
    var tier = getCurrentTier();
    var features = getFeatures();

    if (tier === 'premium') {
      return {
        queriesToday: 0,
        maxQueries: Infinity,
        remaining: Infinity,
        tier: 'premium'
      };
    }

    var todayCount = _checkAndResetDaily();
    var maxQueries = features.maxQueriesPerDay;

    return {
      queriesToday: todayCount,
      maxQueries: maxQueries,
      remaining: Math.max(0, maxQueries - todayCount),
      tier: 'free'
    };
  }

  /**
   * 重置每日使用计数（主要用于测试）
   */
  function resetDailyUsage() {
    _safeSet(STORAGE_KEYS.QUERY_COUNT_TODAY, '0');
    _safeSet(STORAGE_KEYS.QUERY_COUNT_TODAY + '_date', '');
    console.log('[Subscription] Daily usage reset');
  }

  /* ========================================================================
     Public API — 支付集成
     ======================================================================== */

  /**
   * 初始化支付流程
   * 
   * 提供两种支付方式：
   *   1. Stripe Payment Link（推荐）
   *   2. PayPal 订阅按钮
   * 
   * @param {string} [provider='stripe'] - 支付提供商: 'stripe' | 'paypal'
   * @param {Function} [callback] - 支付窗口关闭后的回调
   */
  function initPayment(provider, callback) {
    if (provider === undefined) provider = 'stripe';

    console.log('[Subscription] Initializing payment, provider:', provider);

    var paymentUrl;

    if (provider === 'paypal') {
      paymentUrl = PAYPAL_SUBSCRIPTION_LINK;
    } else {
      // 默认使用 Stripe
      paymentUrl = STRIPE_PAYMENT_LINK;
    }

    // 在新窗口/标签页打开支付页面
    var paymentWindow = window.open(paymentUrl, '_blank', 'width=800,height=700');

    if (!paymentWindow) {
      // 弹窗被阻止，直接导航
      console.warn('[Subscription] Popup blocked, redirecting');
      window.location.href = paymentUrl;
    }

    // 可选：轮询检查支付完成
    if (typeof callback === 'function') {
      var checkInterval = setInterval(function () {
        if (paymentWindow && paymentWindow.closed) {
          clearInterval(checkInterval);
          callback();
        }
      }, 1000);
    }
  }

  /**
   * 获取 Stripe Payment Link
   * @returns {string}
   */
  function getStripePaymentLink() {
    return STRIPE_PAYMENT_LINK;
  }

  /**
   * 获取 PayPal 订阅链接
   * @returns {string}
   */
  function getPayPalPaymentLink() {
    return PAYPAL_SUBSCRIPTION_LINK;
  }

  /**
   * 获取订阅价格
   * @returns {{ amount: number, currency: string, period: string }}
   */
  function getPriceInfo() {
    return {
      amount: SUBSCRIPTION_PRICE,
      currency: 'USD',
      period: 'month'
    };
  }

  /* ========================================================================
     Public API — 订阅验证
     ======================================================================== */

  /**
   * 验证订阅 token
   * 
   * 在当前纯前端方案中：
   *   - 解码 localStorage 中的 token
   *   - 检查是否过期
   *   - 检查 token 格式是否有效
   * 
   * 生产环境应使用 Cloudflare Worker 验证：
   *   POST /api/verify-token { token }
   * 
   * @param {string} [token] - 要验证的 token，不传则验证当前 token
   * @returns {Promise<{ valid: boolean, tier: string, expiresAt: number|null }>}
   */
  async function verifySubscription(token) {
    var tokenToVerify = token || _token;

    if (!tokenToVerify) {
      console.log('[Subscription] No token to verify');
      return { valid: false, tier: 'free', expiresAt: null };
    }

    // 解码本地 token
    var payload = _decodeLocalToken(tokenToVerify);

    if (!payload) {
      console.warn('[Subscription] Invalid token format');
      _safeRemove(STORAGE_KEYS.SUBSCRIPTION_TOKEN);
      _safeRemove(STORAGE_KEYS.SUBSCRIPTION_DATA);
      _token = null;
      _subscriptionData = null;
      _notifyListeners();
      return { valid: false, tier: 'free', expiresAt: null };
    }

    // 检查过期
    if (payload.exp && payload.exp < Date.now()) {
      console.log('[Subscription] Token expired');
      _safeRemove(STORAGE_KEYS.SUBSCRIPTION_TOKEN);
      _safeRemove(STORAGE_KEYS.SUBSCRIPTION_DATA);
      _token = null;
      _subscriptionData = null;
      _notifyListeners();
      return { valid: false, tier: 'free', expiresAt: payload.exp };
    }

    // 更新内存状态
    _subscriptionData = {
      tier: 'premium',
      features: payload.features || FEATURES.PREMIUM,
      expiresAt: payload.exp,
      source: payload.source || 'unknown'
    };
    _safeSetJSON(STORAGE_KEYS.SUBSCRIPTION_DATA, _subscriptionData);

    _notifyListeners();

    return {
      valid: true,
      tier: 'premium',
      expiresAt: payload.exp
    };
  }

  /**
   * 从支付回调激活订阅
   * 
   * 当用户从 Stripe/PayPal 支付完成后重定向回站点时调用。
   * 目前使用本地 token 生成。
   * 生产环境应调用 Cloudflare Worker API 验证 Stripe session。
   * 
   * @param {string} sessionId - Stripe Checkout Session ID 或 PayPal 订单 ID
   * @param {string} [source='stripe'] - 支付来源
   * @returns {Promise<boolean>} 是否激活成功
   */
  async function activateSubscription(sessionId, source) {
    if (source === undefined) source = 'stripe';

    console.log('[Subscription] Activating subscription, session:', sessionId, 'source:', source);

    try {
      // 生成本地 token
      var newToken = _generateLocalToken({
        userId: 'user_' + sessionId.slice(-8),
        source: source
      });

      // 保存 token
      _token = newToken;
      _safeSet(STORAGE_KEYS.SUBSCRIPTION_TOKEN, newToken);

      // 验证并加载
      var result = await verifySubscription(newToken);

      if (result.valid) {
        console.log('[Subscription] Subscription activated successfully');
        return true;
      }

      console.error('[Subscription] Activation verification failed');
      return false;
    } catch (e) {
      console.error('[Subscription] Activation error:', e);
      return false;
    }
  }

  /**
   * 取消订阅（清除本地 token）
   * 注意：实际取消需要在 Stripe/PayPal 端操作
   */
  function cancelSubscription() {
    console.log('[Subscription] Cancelling subscription (local only)');

    _token = null;
    _subscriptionData = null;
    _safeRemove(STORAGE_KEYS.SUBSCRIPTION_TOKEN);
    _safeRemove(STORAGE_KEYS.SUBSCRIPTION_DATA);

    _notifyListeners();
    console.log('[Subscription] Local subscription cancelled');
  }

  /**
   * 登出（清除所有订阅数据）
   */
  function logout() {
    cancelSubscription();
  }

  /* ========================================================================
     Public API — 事件监听
     ======================================================================== */

  /**
   * 添加订阅状态变化监听器
   * @param {Function} listener - 回调函数，接收 { tier, isPremium }
   * @returns {Function} 取消监听的函数
   */
  function addListener(listener) {
    if (typeof listener !== 'function') {
      console.warn('[Subscription] Listener must be a function');
      return function () {};
    }

    _listeners.push(listener);

    // 立即通知当前状态
    try {
      listener(getSubscriptionStatus());
    } catch (e) {
      console.warn('[Subscription] Listener initial call error:', e);
    }

    // 返回取消订阅函数
    return function () {
      var index = _listeners.indexOf(listener);
      if (index !== -1) {
        _listeners.splice(index, 1);
      }
    };
  }

  /**
   * 移除监听器
   * @param {Function} listener
   */
  function removeListener(listener) {
    var index = _listeners.indexOf(listener);
    if (index !== -1) {
      _listeners.splice(index, 1);
    }
  }

  /* ========================================================================
     Public API — 付费功能门控辅助
     ======================================================================== */

  /**
   * 获取特定功能的 upsell 消息
   * @param {string} featureName - 功能名称
   * @returns {string|null} 如果功能需要付费，返回推广文案
   */
  function getFeatureUpsellMessage(featureName) {
    var tier = getCurrentTier();

    if (tier === 'premium') return null;

    var premiumFeature = FEATURES.PREMIUM[featureName];
    var freeFeature = FEATURES.FREE[featureName];

    if (premiumFeature && !freeFeature) {
      return 'Upgrade to Premium ($' + SUBSCRIPTION_PRICE + '/month) to unlock ' + featureName.replace(/([A-Z])/g, ' $1').toLowerCase() + '.';
    }

    return null;
  }

  /**
   * 获取所有被锁定的功能列表
   * @returns {string[]}
   */
  function getLockedFeatures() {
    var locked = [];
    var features = FEATURES.PREMIUM;

    for (var feature in features) {
      if (Object.prototype.hasOwnProperty.call(features, feature)) {
        if (features[feature] && !FEATURES.FREE[feature]) {
          locked.push(feature);
        }
      }
    }

    return locked;
  }

  /* ========================================================================
     Auto-initialize on page load
     ======================================================================== */

  // 页面加载时自动初始化
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  }

  /* ========================================================================
     Expose Public API
     ======================================================================== */

  return {
    // 初始化与状态
    init: init,
    getCurrentTier: getCurrentTier,
    isPremium: isPremium,
    hasFeature: hasFeature,
    getFeatures: getFeatures,
    checkUserTier: checkUserTier,
    getSubscriptionStatus: getSubscriptionStatus,

    // 使用跟踪
    trackUsage: trackUsage,
    getUsageStats: getUsageStats,
    resetDailyUsage: resetDailyUsage,

    // 支付
    initPayment: initPayment,
    getStripePaymentLink: getStripePaymentLink,
    getPayPalPaymentLink: getPayPalPaymentLink,
    getPriceInfo: getPriceInfo,

    // 订阅验证与管理
    verifySubscription: verifySubscription,
    activateSubscription: activateSubscription,
    cancelSubscription: cancelSubscription,
    logout: logout,

    // 事件
    addListener: addListener,
    removeListener: removeListener,

    // 功能门控
    getFeatureUpsellMessage: getFeatureUpsellMessage,
    getLockedFeatures: getLockedFeatures,

    // 常量暴露
    FEATURES: FEATURES,
    STORAGE_KEYS: STORAGE_KEYS,
    SUBSCRIPTION_PRICE: SUBSCRIPTION_PRICE
  };
})();
