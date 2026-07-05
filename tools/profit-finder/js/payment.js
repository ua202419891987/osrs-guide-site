/**
 * payment.js — Freemium Payment Module for Profit Finder
 * 
 * $1.90 one-time purchase to unlock premium features.
 * Supports Stripe Checkout (primary) and PayPal (backup).
 * All state persisted in localStorage.
 */

(function () {
  'use strict';

  // ──────────────────────────── Constants ────────────────────────────
  const PAYMENT_KEY = 'osrsguru_profit_finder_unlocked';

  const STRIPE_PRICE_ID = 'price_1.90_profit_finder';
  const STRIPE_PUBLIC_KEY = 'pk_live_...'; // TODO: replace with real publishable key

  const PAYPAL_CLIENT_ID = 'your_paypal_client_id'; // TODO: replace with real client ID

  const PAYMENT_AMOUNT_USD = 1.90;

  const CALLBACK_PARAM = 'payment';

  const SUCCESS_MESSAGE = '🎉 Unlocked! Real-time prices and goal tracking are now available!';

  // ──────────────────────── DOM Selectors (lazy) ──────────────────────
  // These elements are expected to exist in the HTML markup:
  //   <div id="paywallSection"> … </div>
  //   <div id="premiumArea"> … </div>
  //   <button id="paywallBtn">Unlock Premium — $1.90</button>
  //   <div id="paypal-button-container"></div>
  //   <div id="payment-success-banner"></div>

  let _paywallEl = null;
  let _premiumEl = null;
  let _successBanner = null;

  function _getEl(id) {
    return document.getElementById(id);
  }

  // ──────────────────────── State ─────────────────────────────────────
  function _readState() {
    try {
      const raw = localStorage.getItem(PAYMENT_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  function _writeState(data) {
    localStorage.setItem(PAYMENT_KEY, JSON.stringify(data));
  }

  // ──────────────────────── Public API ────────────────────────────────

  /**
   * Check whether the user has unlocked premium.
   * @returns {boolean}
   */
  function isUnlocked() {
    const state = _readState();
    return !!(state && state.unlocked === true);
  }

  /**
   * Show the paywall overlay and hide premium content.
   */
  function showPaywall() {
    _paywallEl = _paywallEl || _getEl('paywallSection');
    _premiumEl = _premiumEl || _getEl('premiumArea');

    // Also remove any success banner left from a previous unlock
    _hideSuccessBanner();
  }

  /**
   * Unlock premium: hide paywall, show content, persist state.
   * @param {string} [transactionId] - Optional transaction identifier.
   */
  function unlockPremium(transactionId) {
    _paywallEl = _paywallEl || _getEl('paywallSection');
    _premiumEl = _premiumEl || _getEl('premiumArea');

    if (_paywallEl) {
      _paywallEl.style.display = 'none';
    }
    if (_premiumEl) {
      _premiumEl.style.display = 'block';
    }

    // Persist
    _writeState({
      unlocked: true,
      timestamp: Date.now(),
      transactionId: transactionId || 'manual'
    });

    // Show success banner
    _showSuccessMessage();

    // Re-init any premium UI components that depend on unlocked state
    _notifyPremiumReady();
  }

  /**
   * Clear all payment / unlock state (useful for testing).
   */
  function clearPayment() {
    localStorage.removeItem(PAYMENT_KEY);
    _hideSuccessBanner();
    // Re-apply paywall so the UI returns to locked state
    if (!isUnlocked()) {
      showPaywall();
    }
  }

  /**
   * Retrieve payment info.
   * @returns {{ unlocked: boolean, timestamp: number|null, transactionId: string|null }}
   */
  function getPaymentInfo() {
    const state = _readState();
    if (!state) {
      return { unlocked: false, timestamp: null, transactionId: null };
    }
    return {
      unlocked: state.unlocked === true,
      timestamp: state.timestamp || null,
      transactionId: state.transactionId || null
    };
  }

  // ──────────────────────── Payment Initialization ────────────────────

  function _initPaymentButtons() {
    // Primary: PayPal NCP link button
    _initPayPalButton();
  }

  // ──────────────────────── PayPal (Primary) ────────────────────────

  /**
   * Render the real PayPal payment link button.
   * Uses the same PayPal NCP link as the site-wide support cards.
   */
  const PAYPAL_NCP_LINK = 'https://www.paypal.com/ncp/payment/XW8PRCTGNMUG4';

  function _initPayPalButton() {
    const container = _getEl('paypal-button-container');
    if (!container) return;

    container.innerHTML =
      '<a href="' + PAYPAL_NCP_LINK + '" target="_blank" ' +
      'style="display:block;width:100%;padding:12px;background:#ffc439;' +
      'border:0;border-radius:4px;font-size:16px;cursor:pointer;' +
      'text-align:center;text-decoration:none;color:#111;font-weight:600;">' +
      '&#127881; PayPal — $' + PAYMENT_AMOUNT_USD.toFixed(2) +
      '</a>' +
      '<p style="font-size:12px;color:#666;margin-top:8px;">' +
      'After payment, return here and refresh the page to unlock premium.</p>';

    // Also check for return URL parameter from PayPal redirect
    var params = new URLSearchParams(window.location.search);
    if (params.get('payment_success') === '1') {
      unlockPremium('paypal_ncp_' + Date.now());
      var url = new URL(window.location);
      url.searchParams.delete('payment_success');
      window.history.replaceState({}, document.title, url.toString());
    }
  }

  // ──────────────────────── Callback Handler ──────────────────────────

  /**
   * Check URL parameters for a payment success indicator.
   * If found, unlock premium and clean the URL.
   * @returns {boolean} true if a callback was handled
   */
  function _handlePaymentCallback() {
    const params = new URLSearchParams(window.location.search);
    const status = params.get(CALLBACK_PARAM);

    if (status === 'success') {
      unlockPremium('url_callback_' + Date.now());

      // Clean the URL without reloading
      const url = new URL(window.location);
      url.searchParams.delete(CALLBACK_PARAM);
      window.history.replaceState({}, document.title, url.toString());

      return true;
    }
    return false;
  }

  // ──────────────────────── Internal Helpers ──────────────────────────

  function _showSuccessMessage() {
    _successBanner = _successBanner || _getEl('payment-success-banner');
    if (_successBanner) {
      _successBanner.textContent = SUCCESS_MESSAGE;
      _successBanner.style.display = 'block';
    } else {
      // Fallback: create a floating banner
      const banner = document.createElement('div');
      banner.id = 'payment-success-banner';
      banner.textContent = SUCCESS_MESSAGE;
      Object.assign(banner.style, {
        position: 'fixed',
        top: '16px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: '9999',
        background: '#16a34a',
        color: '#fff',
        padding: '14px 28px',
        borderRadius: '8px',
        fontSize: '16px',
        fontWeight: '600',
        boxShadow: '0 4px 16px rgba(0,0,0,0.25)'
      });
      document.body.appendChild(banner);
      _successBanner = banner;
    }

    // Auto-dismiss after 8 seconds
    if (_successBanner._dismissTimer) {
      clearTimeout(_successBanner._dismissTimer);
    }
    _successBanner._dismissTimer = setTimeout(function () {
      _hideSuccessBanner();
    }, 8000);
  }

  function _hideSuccessBanner() {
    if (_successBanner) {
      _successBanner.style.display = 'none';
      if (_successBanner._dismissTimer) {
        clearTimeout(_successBanner._dismissTimer);
        _successBanner._dismissTimer = null;
      }
    }
  }

  /**
   * Dispatch a custom event so other modules can react to the unlock.
   */
  function _notifyPremiumReady() {
    try {
      window.dispatchEvent(new CustomEvent('premium:unlocked', {
        detail: getPaymentInfo()
      }));
    } catch (_) {
      // Some older browsers may not support CustomEvent; ignore.
    }
  }

  // ──────────────────────── Initialization ────────────────────────────

  /**
   * Main initializer — call once on page load.
   * 1. Check URL callback parameter
   * 2. Check localStorage state
   * 3. Set up Stripe / PayPal buttons
   * 4. Show or hide paywall accordingly
   */
  function initPayment() {
    console.log('[Payment] Initializing payment module...');

    // Priority 1: handle incoming payment callback (URL param)
    const callbackHandled = _handlePaymentCallback();

    if (!callbackHandled) {
      // Priority 2: existing unlock state
      if (isUnlocked()) {
        unlockPremium(_readState().transactionId);
      } else {
        showPaywall();
      }
    }

    // Always wire up payment buttons (they are hidden behind paywall anyway)
    _initPaymentButtons();

    console.log('[Payment] Initialized. Unlocked:', isUnlocked());
  }

  // ──────────────────────── Auto-init on DOM ready ────────────────────

  // Support both synchronous and async page loads
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPayment);
  } else {
    initPayment();
  }

  // ──────────────────────── Global Export ─────────────────────────────

  window.payment = {
    isUnlocked: isUnlocked,
    showPaywall: showPaywall,
    unlockPremium: unlockPremium,
    initPayment: initPayment,
    clearPayment: clearPayment,
    getPaymentInfo: getPaymentInfo
  };

})();
