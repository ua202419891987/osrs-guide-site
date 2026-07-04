/**
 * OSRS Gear Recommender — Stripe Payment Integration
 * ====================================================
 *
 * 纯前端 Stripe 支付集成，使用 Stripe Payment Links（无需后端）。
 * 管理订阅流程：打开付款链接 → 用户付款 → 重定向回 verify.html → 激活订阅。
 *
 * 依赖:
 *   - subscription.js (subscriptionManager)
 *
 * 兼容:
 *   - GitHub Pages 静态托管
 *   - 所有现代浏览器
 *
 * @version 1.0.0
 * @see https://stripe.com/docs/payment-links
 */

(function (root) {
  'use strict';

  // ============================================================
  //  CONFIGURATION
  // ============================================================

  /**
   * Stripe Payment Link URL
   *
   * 在 Stripe Dashboard 创建 Payment Link 后替换此值：
   *   Products → OSRS Guru Premium ($1.9/month) → Payment Link
   *
   * 重定向 URL 设置为: https://osrsguru.com/premium/verify.html?session_id={CHECKOUT_SESSION_ID}
   */
  var STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/your_stripe_link_here';

  /**
   * 成功付款后的重定向页面 URL
   */
  var VERIFY_PAGE_URL = '/premium/verify.html';

  /**
   * 订阅产品名称
   */
  var PRODUCT_NAME = 'OSRS Guru Premium';

  /**
   * 订阅价格（仅用于显示）
   */
  var SUBSCRIPTION_PRICE = 1.90;

  /**
   * 货币
   */
  var CURRENCY = 'USD';

  // ============================================================
  //  STATE
  // ============================================================

  /**
   * 付款窗口引用（用于防止弹窗被拦截）
   */
  var _paymentWindow = null;

  /**
   * 是否正在处理支付
   */
  var _isProcessing = false;

  // ============================================================
  //  STRIPE INTEGRATION API
  // ============================================================

  var stripeIntegration = {

    // ==========================================================
    //  openCheckout
    // ==========================================================

    /**
     * 打开 Stripe Payment Link 付款页面
     *
     * 使用 window.open 打开 Stripe 托管的支付页面。
     * 支付完成后，用户被重定向回 verify.html，由 subscriptionManager 处理激活。
     *
     * @param {Object} [options] - 可选参数
     * @param {string} [options.successUrl] - 自定义成功重定向 URL
     * @param {string} [options.cancelUrl] - 自定义取消重定向 URL
     */
    openCheckout: function (options) {
      if (_isProcessing) {
        console.warn('[Stripe] Payment already in progress.');
        return;
      }

      options = options || {};

      // 构建付款 URL
      var paymentUrl = STRIPE_PAYMENT_LINK;

      // 添加 UTM 参数用于追踪
      var params = [];
      params.push('utm_source=osrsguru');
      params.push('utm_medium=tool');
      params.push('utm_campaign=gear-recommender-premium');

      if (params.length > 0) {
        paymentUrl += (paymentUrl.indexOf('?') === -1 ? '?' : '&') + params.join('&');
      }

      // 打开付款窗口
      _isProcessing = true;

      // 使用 window.open 打开（比直接跳转更好，用户可返回）
      _paymentWindow = window.open(paymentUrl, '_blank', 'width=800,height=700,scrollbars=yes');

      if (!_paymentWindow || _paymentWindow.closed) {
        // 弹窗被拦截，直接跳转作为降级方案
        console.warn('[Stripe] Popup blocked, falling back to direct navigation.');
        window.location.href = paymentUrl;
      }

      // 轮询检查付款窗口是否关闭
      this._startPolling();

      // 触发事件
      this._dispatchEvent('stripe:checkout-opened', {
        paymentUrl: paymentUrl,
        timestamp: Date.now()
      });
    },

    // ==========================================================
    //  verifySession
    // ==========================================================

    /**
     * 验证 Stripe Checkout Session
     *
     * 在 verify.html 页面加载时调用。
     * 从 URL 获取 session_id，调用 subscriptionManager 激活订阅。
     *
     * 注意：这是纯前端方案，仅模拟验证流程。
     * 生产环境建议使用 Cloudflare Worker 或类似方案进行 Stripe Webhook 验证。
     *
     * @param {string} [sessionId] - Stripe Checkout Session ID（从 URL 获取）
     * @returns {Promise<boolean>} 是否验证成功
     */
    verifySession: function (sessionId) {
      // 如果未传入 sessionId，从 URL 参数获取
      if (!sessionId) {
        var params = new URLSearchParams(window.location.search);
        sessionId = params.get('session_id');
      }

      if (!sessionId) {
        console.error('[Stripe] No session ID provided.');
        this._dispatchEvent('stripe:verification-failed', {
          error: 'No session ID',
          timestamp: Date.now()
        });
        return Promise.resolve(false);
      }

      console.log('[Stripe] Verifying session:', sessionId);

      // 检查 subscriptionManager 是否存在
      if (!root.subscriptionManager) {
        console.error('[Stripe] subscriptionManager not loaded. Include subscription.js first.');
        return Promise.resolve(false);
      }

      // 调用 subscriptionManager 激活订阅
      return root.subscriptionManager.activateSubscription(sessionId)
        .then(function (success) {
          if (success) {
            console.log('[Stripe] Subscription activated successfully for session:', sessionId);
            stripeIntegration._dispatchEvent('stripe:subscription-activated', {
              sessionId: sessionId,
              timestamp: Date.now()
            });
          } else {
            console.warn('[Stripe] Subscription activation returned false for session:', sessionId);
            stripeIntegration._dispatchEvent('stripe:activation-failed', {
              sessionId: sessionId,
              timestamp: Date.now()
            });
          }
          return success;
        })
        .catch(function (err) {
          console.error('[Stripe] Verification error:', err);
          stripeIntegration._dispatchEvent('stripe:verification-error', {
            error: err.message,
            sessionId: sessionId,
            timestamp: Date.now()
          });
          return false;
        });
    },

    // ==========================================================
    //  cancelSubscription
    // ==========================================================

    /**
     * 取消订阅
     *
     * 打开 Stripe Customer Portal 让用户自行管理/取消订阅。
     * Customer Portal 需要在 Stripe Dashboard 中启用。
     *
     * Customer Portal 配置步骤：
     *   Settings → Customer Portal → 启用 → 配置允许的操作（取消、更新等）
     *
     * Customer Portal 链接格式：
     *   https://buy.stripe.com/customer/{customer_id}
     *
     * 注意：此为简化版，实际需要 Customer Portal 配置。
     * 或者引导用户联系 support@osrsguru.com 取消。
     */
    cancelSubscription: function () {
      // 检查是否有订阅数据
      if (!root.subscriptionManager || !root.subscriptionManager.isActive()) {
        console.warn('[Stripe] No active subscription to cancel.');
        return;
      }

      var subscriptionData = root.subscriptionManager.getSubscriptionData();
      var customerPortalUrl = null;

      // 如果有 Stripe Customer ID，尝试打开 Customer Portal
      if (subscriptionData && subscriptionData.stripeCustomerId) {
        // Stripe Customer Portal URL（需要配置）
        customerPortalUrl = 'https://buy.stripe.com/customer/' +
          encodeURIComponent(subscriptionData.stripeCustomerId);
      }

      if (customerPortalUrl) {
        // 打开 Customer Portal
        var portalWindow = window.open(customerPortalUrl, '_blank', 'width=800,height=700');
        if (!portalWindow || portalWindow.closed) {
          window.location.href = customerPortalUrl;
        }
      } else {
        // 没有 Customer ID，引导用户联系支持
        var message = 'To cancel your subscription, please email support@osrsguru.com ' +
          'from the email address you used for payment.';
        alert(message);
        console.log('[Stripe] Cancellation info:', message);
      }

      this._dispatchEvent('stripe:cancel-initiated', {
        timestamp: Date.now()
      });
    },

    // ==========================================================
    //  getPaymentLink
    // ==========================================================

    /**
     * 获取 Stripe Payment Link URL
     *
     * @returns {string} Payment Link URL
     */
    getPaymentLink: function () {
      return STRIPE_PAYMENT_LINK;
    },

    // ==========================================================
    //  isCheckoutOpen
    // ==========================================================

    /**
     * 检查付款窗口是否仍然打开
     *
     * @returns {boolean}
     */
    isCheckoutOpen: function () {
      return _paymentWindow && !_paymentWindow.closed;
    },

    // ==========================================================
    //  getPriceDisplay
    // ==========================================================

    /**
     * 获取格式化的价格显示文本
     *
     * @returns {string} 例如 "$1.90 / month"
     */
    getPriceDisplay: function () {
      return '$' + SUBSCRIPTION_PRICE.toFixed(2) + ' / month';
    },

    // ==========================================================
    //  PRIVATE HELPERS
    // ==========================================================

    /**
     * 开始轮询付款窗口状态
     * @private
     */
    _startPolling: function () {
      var self = this;
      var pollInterval = 1500; // 1.5 秒轮询一次
      var maxPolls = 1200;     // 最多轮询 30 分钟

      var pollCount = 0;
      var pollTimer = setInterval(function () {
        pollCount++;

        // 窗口已关闭
        if (!_paymentWindow || _paymentWindow.closed) {
          clearInterval(pollTimer);
          _isProcessing = false;
          _paymentWindow = null;

          self._dispatchEvent('stripe:checkout-closed', {
            timestamp: Date.now()
          });

          console.log('[Stripe] Checkout window closed by user.');
          return;
        }

        // 超时保护
        if (pollCount >= maxPolls) {
          clearInterval(pollTimer);
          _isProcessing = false;
          console.warn('[Stripe] Payment polling timed out.');
        }
      }, pollInterval);
    },

    /**
     * 派发自定义事件
     * @private
     * @param {string} eventName - 事件名
     * @param {Object} detail - 事件数据
     */
    _dispatchEvent: function (eventName, detail) {
      try {
        var event = new CustomEvent(eventName, {
          detail: detail,
          bubbles: true,
          cancelable: true
        });
        document.dispatchEvent(event);
      } catch (e) {
        // CustomEvent 不支持时静默失败
        console.debug('[Stripe] Event dispatch not supported:', eventName);
      }
    }

  };

  // ============================================================
  //  EXPORT
  // ============================================================

  // 暴露到全局
  root.stripeIntegration = stripeIntegration;

  // AMD / CommonJS 支持
  if (typeof define === 'function' && define.amd) {
    define([], function () { return stripeIntegration; });
  } else if (typeof module === 'object' && module.exports) {
    module.exports = stripeIntegration;
  }

  console.log('[Stripe] Integration loaded. Payment link:', STRIPE_PAYMENT_LINK);

})(typeof window !== 'undefined' ? window : this);
