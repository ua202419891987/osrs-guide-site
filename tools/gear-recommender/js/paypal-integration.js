/**
 * OSRS Gear Recommender — PayPal Subscription Integration
 * ========================================================
 *
 * 纯前端 PayPal 支付集成，使用 PayPal hosted subscription button。
 * GitHub Pages 静态站点兼容，无需后端服务。
 *
 * 流程：用户点击订阅 → 跳转 PayPal 付款 → 重定向回 verify.html → localStorage 激活
 *
 * @version 1.0.0
 */

(function (root) {
  'use strict';

  // ============================================================
  //  CONFIGURATION
  // ============================================================

  /**
   * PayPal Subscription Link
   *
   * 在 PayPal 后台创建订阅计划后替换此值：
   *   1. 登录 https://www.paypal.com  → 商家工具 → 订阅按钮
   *   2. 创建 $1.9/月 订阅计划
   *   3. 生成 hosted button ID 或 subscription link
   *   4. 将链接粘贴到这里
   *
   * 重定向: 在 PayPal 按钮设置中配置 return_url = https://osrsguru.com/premium/verify.html
   */
  var PAYPAL_SUBSCRIPTION_LINK = 'https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=P-7YW48381J13616844NJEMW2I';

  /**
   * 成功付款后的重定向页面 URL
   */
  var VERIFY_PAGE_URL = '/premium/verify.html';

  // ============================================================
  //  PUBLIC API
  // ============================================================

  /**
   * 打开 PayPal 订阅付款页面
   * @param {string} [customVerifyUrl] - 可选的自定义重定向 URL
   */
  function openCheckout(customVerifyUrl) {
    var returnUrl = customVerifyUrl || (window.location.origin + VERIFY_PAGE_URL);
    var paypalUrl = PAYPAL_SUBSCRIPTION_LINK;

    // 如果有 return_url 参数，附加到 PayPal URL
    if (paypalUrl.indexOf('?') === -1) {
      paypalUrl += '?return_url=' + encodeURIComponent(returnUrl);
    } else {
      paypalUrl += '&return_url=' + encodeURIComponent(returnUrl);
    }

    // 打开 PayPal checkout
    window.open(paypalUrl, '_blank', 'width=800,height=700,scrollbars=yes,resizable=yes');

    // 派发 checkout 打开事件
    root.dispatchEvent(new CustomEvent('paypal:checkout-opened', {
      detail: { url: paypalUrl }
    }));
  }

  /**
   * 验证付款状态（在 verify.html 调用）
   * 从 URL 参数中提取订阅信息并激活
   */
  function verifyPayment() {
    var params = new URLSearchParams(window.location.search);
    var subscriptionId = params.get('subscription_id');
    var baToken = params.get('ba_token');  // Billing Agreement token
    var payerId = params.get('PayerID');

    if (subscriptionId || baToken) {
      // 标记订阅为活跃
      activateSubscription(subscriptionId || baToken);
      return true;
    }
    return false;
  }

  /**
   * 激活订阅（存入 localStorage）
   * @param {string} subscriptionId
   */
  function activateSubscription(subscriptionId) {
    try {
      var now = new Date();
      var expiry = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000); // 30 days

      var subscriptionData = {
        provider: 'paypal',
        active: true,
        activatedAt: now.toISOString(),
        expiresAt: expiry.toISOString(),
        subscriptionId: subscriptionId,
        autoRenew: true
      };

      localStorage.setItem('osrsguru_premium', JSON.stringify(subscriptionData));
      localStorage.setItem('osrsguru_premium_status', 'active');

      // 派发激活事件
      root.dispatchEvent(new CustomEvent('paypal:subscription-activated', {
        detail: subscriptionData
      }));
    } catch (e) {
      console.error('[PayPal] Failed to save subscription:', e);
    }
  }

  /**
   * 取消订阅（跳转到 PayPal 用户中心）
   */
  function cancelSubscription() {
    window.open('https://www.paypal.com/myaccount/autopay/', '_blank');
  }

  /**
   * 获取当前订阅状态
   * @returns {{active: boolean, provider: string, expiresAt: string}|null}
   */
  function getStatus() {
    try {
      var data = localStorage.getItem('osrsguru_premium');
      if (!data) return null;

      var parsed = JSON.parse(data);
      var now = new Date();

      // 检查是否过期
      if (parsed.expiresAt && new Date(parsed.expiresAt) < now) {
        parsed.active = false;
        localStorage.setItem('osrsguru_premium_status', 'expired');
      }

      return parsed;
    } catch (e) {
      return null;
    }
  }

  // ============================================================
  //  EXPORTS
  // ============================================================

  root.OSRSPayPal = {
    openCheckout: openCheckout,
    verifyPayment: verifyPayment,
    cancelSubscription: cancelSubscription,
    getStatus: getStatus
  };

})(typeof window !== 'undefined' ? window : this);
