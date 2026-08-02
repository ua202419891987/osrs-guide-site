/**
 * OSRS Guru — Unified Premium / Subscription Gate (osrs-subscription.js)
 * ---------------------------------------------------------------------------
 * 全站工具统一的 freemium 门控层。所有工具（免费 + 付费）都必须接入这一个模块，
 * 保证：一次订阅 = 解锁全部付费工具（Payhip One-Time：$2.66/月、$8.99/4月、$23.99/年）。
 *
 * 设计原则
 *   1. 免费层必须真的好用（引流 + 留存），付费层解锁"决策级"能力
 *   2. 纯静态站可运行：localStorage token + 支付回跳激活，无需后端
 *   3. 埋点内建：撞墙 / 点升级 / 订阅成功 自动上报，无需工具自己写
 *   4. 未来接 Cloudflare Worker 只需替换 _verifyRemote()，工具页零改动
 *
 * 用法
 *   <script src="../shared/js/osrs-analytics.js"></script>
 *   <script src="../shared/js/osrs-subscription.js"></script>
 *
 *   if (!OSRSPremium.require('dps-calculator', 'multiStyleCompare')) return;
 *   var gate = OSRSPremium.consume('dps-calculator');   // 每日次数限制
 *   if (!gate.allowed) return;                          // 已自动弹墙
 *
 * @version 1.1.0
 */
(function (global) {
  'use strict';

  /* =====================================================================
     1. 定价与支付（Payhip One-Time Purchase，2026-08-02 接入）
     ===================================================================== */
  var PRICES = {
    month:   { usd: 2.66,  ttlDays: 31,  label: '1 Month' },
    quarter: { usd: 8.99,  ttlDays: 122, label: '4 Months' },
    year:    { usd: 23.99, ttlDays: 366, label: '12 Months' }
  };
  // 默认展示价（用于 badge / 回退）
  var PRICE = PRICES.month.usd;
  var PRICE_YEARLY = PRICES.year.usd;

  /**
   * Payhip One-Time Purchase 结账链接（燕春已在 Payhip 建好 3 个 pricing plan）
   * 注意：One-Time 无自动续费，付费后由 success 页回跳激活 localStorage token。
   */
  var PAY_LINKS = {
    month:   'https://payhip.com/order?link=mWJzl&pricing_plan=nLWRaRk4Ga',
    quarter: 'https://payhip.com/order?link=mWJzl&pricing_plan=rdWQ8kKyGj',
    year:    'https://payhip.com/order?link=mWJzl&pricing_plan=Q7zqexm7zg'
  };

  var TOKEN_TTL_MS = PRICES.month.ttlDays * 864e5; // 默认 31 天

  /* =====================================================================
     2. 全站功能矩阵（免费 / 付费边界的唯一真相源）
     ===================================================================== */
  var MATRIX = {
    // ---------- 免费引流工具：不限次，仅高级功能上锁 ----------
    'profit-finder': {
      free:    { dailyLimit: Infinity, goalTracker: false, exportPlan: false, adFree: false },
      premium: { dailyLimit: Infinity, goalTracker: true,  exportPlan: true,  adFree: true }
    },
    'gear-recommender': {
      free:    { dailyLimit: 3, exactBudget: false, upgradePaths: false, saveBuilds: false, multiStyleCompare: false, adFree: false },
      premium: { dailyLimit: Infinity, exactBudget: true, upgradePaths: true, saveBuilds: true, multiStyleCompare: true, adFree: true }
    },
    'bank-layout': {
      free:    { dailyLimit: Infinity, savePreset: true, maxPresets: 3, exportImage: false, sharePreset: false, adFree: false },
      premium: { dailyLimit: Infinity, savePreset: true, maxPresets: 50, exportImage: true, sharePreset: true, adFree: true }
    },
    'drop-lookup': {
      free:    { dailyLimit: Infinity, dryCalc: true, expectedValue: false, compareTargets: false, adFree: false },
      premium: { dailyLimit: Infinity, dryCalc: true, expectedValue: true, compareTargets: true, adFree: true }
    },
    // ---------- 付费核心工具：免费给"尝鲜"，核心结论上锁 ----------
    'dps-calculator': {
      free:    { dailyLimit: 5, basicDps: true, specialAttack: false, multiStyleCompare: false, gpPerDamage: false, saveSetups: false, adFree: false },
      premium: { dailyLimit: Infinity, basicDps: true, specialAttack: true, multiStyleCompare: true, gpPerDamage: true, saveSetups: true, adFree: true }
    },
    'gp-tracker': {
      free:    { dailyLimit: 3, sessionCost: true, livePrices: true, netProfit: false, history: false, exportCsv: false, adFree: false },
      premium: { dailyLimit: Infinity, sessionCost: true, livePrices: true, netProfit: true, history: true, exportCsv: true, adFree: true }
    },
    'clog-advisor': {
      free:    { dailyLimit: 3, topPick: true, fullRanking: false, timeToComplete: false, plannerExport: false, adFree: false },
      premium: { dailyLimit: Infinity, topPick: true, fullRanking: true, timeToComplete: true, plannerExport: true, adFree: true }
    }
  };

  /** 面向用户的功能文案（弹墙时显示，别让用户看到驼峰变量名） */
  var FEATURE_LABELS = {
    // 免费层已有的能力（弹墙时不会用到，但 Hub 定价表需要人话标签）
    basicDps: 'Basic DPS & max hit calculator',
    dryCalc: 'Dry-streak probability calculator',
    sessionCost: 'Supply cost per session',
    livePrices: 'Live Grand Exchange prices',
    savePreset: 'Save bank layout presets',
    maxPresets: 'Saved preset slots',
    topPick: 'Top recommendation',
    // 付费层能力
    goalTracker: 'Goal Tracker',
    exportPlan: 'Export your money-making plan',
    exactBudget: 'Exact budget input',
    upgradePaths: 'Gear upgrade paths',
    saveBuilds: 'Save unlimited builds',
    multiStyleCompare: 'Compare all combat styles side by side',
    specialAttack: 'Special attack & multi-hit DPS modelling',
    gpPerDamage: 'GP-per-damage economy view',
    saveSetups: 'Save setups',
    netProfit: 'True net profit (revenue − supplies)',
    history: 'Session history & trends',
    exportCsv: 'CSV export',
    fullRanking: 'Full ranked list of what to grind next',
    timeToComplete: 'Time-to-completion estimates',
    plannerExport: 'Export your collection log plan',
    exportImage: 'Export bank layout as image',
    sharePreset: 'Share preset link',
    expectedValue: 'Expected GP value per kill',
    compareTargets: 'Compare multiple drop sources',
    adFree: 'Ad-free experience',
    dailyLimit: 'Unlimited daily uses'
  };

  var KEYS = {
    TOKEN: 'osrsguru_premium_token',
    DATA: 'osrsguru_premium_data',
    USE_PREFIX: 'osrsguru_use_',
    PENDING_PLAN: 'osrsguru_pending_plan'
  };

  var _data = null;
  var _token = null;
  var _listeners = [];

  /* =====================================================================
     3. Storage helpers
     ===================================================================== */
  function _get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function _set(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function _del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function _getJSON(k, f) { try { var r = localStorage.getItem(k); return r ? JSON.parse(r) : f; } catch (e) { return f; } }
  function _setJSON(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function _today() {
    var d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  function _analytics() { return global.OSRSAnalytics || null; }

  /* =====================================================================
     4. Token
     ===================================================================== */
  function _encode(payload) {
    try { return 'osrs_' + btoa(unescape(encodeURIComponent(JSON.stringify(payload)))); }
    catch (e) { return null; }
  }
  function _decode(token) {
    if (!token || token.indexOf('osrs_') !== 0) return null;
    try { return JSON.parse(decodeURIComponent(escape(atob(token.slice(5))))); }
    catch (e) { return null; }
  }

  function init() {
    _token = _get(KEYS.TOKEN);
    if (_token) {
      var p = _decode(_token);
      if (p && p.exp && p.exp > Date.now()) {
        _data = { tier: 'premium', expiresAt: p.exp, source: p.source || 'unknown', plan: p.plan || 'month' };
        _setJSON(KEYS.DATA, _data);
      } else {
        _token = null; _data = null;
        _del(KEYS.TOKEN); _del(KEYS.DATA);
      }
    }
    _handleReturnFromPayment();
    _handlePendingPlanOnLoad();
    _notify();
  }

  /**
   * B 方案（Payhip 不支持自定义回跳）：用户在付费墙点 plan 后会把 plan 存进
   * localStorage(PENDING_PLAN) 并开新标签去 Payhip 付款。Payhip 不回跳本站，
   * 所以用户付完手动返回并刷新页面时，这里检测 pending plan 弹出激活横幅。
   */
  function _handlePendingPlanOnLoad() {
    try {
      if (isPremium()) { _del(KEYS.PENDING_PLAN); return; }
      var plan = _get(KEYS.PENDING_PLAN);
      if (!plan || !PRICES[plan]) return;
      _showPendingBanner(plan);
    } catch (e) {}
  }

  function _showPendingBanner(plan) {
    _ensureStyles();
    if (document.querySelector('.opw-banner')) return;
    var label = PRICES[plan] ? PRICES[plan].label : 'Premium';
    var banner = document.createElement('div');
    banner.className = 'opw-banner';
    banner.innerHTML =
      '<span>💡 Welcome back — if you completed your Payhip payment, tap to activate <b>' + label + '</b>.</span>' +
      '<button class="opw-activate" type="button">Activate Premium</button>' +
      '<button class="opw-dismiss" type="button">Dismiss</button>';
    document.body.appendChild(banner);
    banner.querySelector('.opw-activate').addEventListener('click', function () {
      activate('manual_' + Date.now(), 'payhip', plan);
      _del(KEYS.PENDING_PLAN);
      if (_analytics()) _analytics().trackSubscribeSuccess('payhip', PRICES[plan] ? PRICES[plan].usd : PRICE);
      banner.remove();
      toast('✅ Premium activated — thanks for supporting OSRS Guru!');
    });
    banner.querySelector('.opw-dismiss').addEventListener('click', function () {
      banner.remove();
    });
  }

  /** 支付回跳自动激活：/tools/xxx/?premium=ok&provider=payhip&plan=month */
  function _handleReturnFromPayment() {
    try {
      var q = new URLSearchParams(global.location.search);
      if (q.get('premium') === 'ok') {
        var provider = q.get('provider') || 'payhip';
        var sid = q.get('sid') || ('s' + Date.now());
        var planFromUrl = q.get('plan');
        // 兼容旧 'monthly'/'yearly' 写法
        var planMap = { monthly: 'month', yearly: 'year' };
        var plan = planFromUrl ? (planMap[planFromUrl] || planFromUrl) : null;
        // 没有 URL plan 时，用点击结账时存的 pending plan
        if (!plan || !PRICES[plan]) {
          var pending = _get(KEYS.PENDING_PLAN);
          plan = pending && PRICES[pending] ? pending : 'month';
        }
        activate(sid, provider, plan);
        var price = PRICES[plan] ? PRICES[plan].usd : PRICE;
        if (_analytics()) _analytics().trackSubscribeSuccess(provider, price);
        _del(KEYS.PENDING_PLAN);
        // 清掉 URL 参数，避免用户分享链接就白送会员
        if (global.history && global.history.replaceState) {
          global.history.replaceState({}, '', global.location.pathname);
        }
        toast('✅ Premium activated — thanks for supporting OSRS Guru!');
      }
    } catch (e) {}
  }

  function activate(sessionId, source, plan) {
    var key = PRICES[plan] ? plan : 'month';
    var ttl = PRICES[key].ttlDays * 864e5;
    var payload = {
      sub: 'u_' + String(sessionId).slice(-10),
      iat: Date.now(),
      exp: Date.now() + ttl,
      tier: 'premium',
      plan: key,
      source: source || 'manual'
    };
    var tok = _encode(payload);
    if (!tok) return false;
    _token = tok;
    _set(KEYS.TOKEN, tok);
    _data = { tier: 'premium', expiresAt: payload.exp, source: payload.source, plan: payload.plan };
    _setJSON(KEYS.DATA, _data);
    _notify();
    return true;
  }

  function deactivate() {
    _token = null; _data = null;
    _del(KEYS.TOKEN); _del(KEYS.DATA);
    _notify();
  }

  /* =====================================================================
     5. 状态查询
     ===================================================================== */
  function getTier() { return (_data && _data.tier === 'premium' && _data.expiresAt > Date.now()) ? 'premium' : 'free'; }
  function isPremium() { return getTier() === 'premium'; }
  function daysRemaining() {
    if (!isPremium()) return 0;
    return Math.max(0, Math.ceil((_data.expiresAt - Date.now()) / 864e5));
  }
  function getPlan() { return (_data && _data.plan) || 'month'; }

  function features(tool) {
    var m = MATRIX[tool];
    if (!m) return { dailyLimit: Infinity };
    return isPremium() ? m.premium : m.free;
  }

  function hasFeature(tool, key) {
    var f = features(tool);
    return f[key] === true || (typeof f[key] === 'number' && f[key] > 0);
  }

  /* =====================================================================
     6. 门控 API（工具页只需要用这两个）
     ===================================================================== */

  /**
   * 检查某个高级功能是否可用；不可用时自动埋点 + 弹墙
   * @returns {boolean} true = 放行
   */
  function require(tool, featureKey, opts) {
    if (hasFeature(tool, featureKey)) return true;
    if (_analytics()) _analytics().trackPaywallHit(featureKey, 'feature_locked');
    showPaywall({
      tool: tool,
      feature: featureKey,
      title: (opts && opts.title) || 'Premium feature',
      body: (opts && opts.body) || null
    });
    return false;
  }

  /**
   * 消耗一次使用配额（免费用户每日限次的工具用）
   * @returns {{allowed:boolean, remaining:number, tier:string}}
   */
  function consume(tool) {
    var f = features(tool);
    var limit = f.dailyLimit;
    if (limit === Infinity || limit === undefined) {
      return { allowed: true, remaining: Infinity, tier: getTier() };
    }
    var key = KEYS.USE_PREFIX + tool;
    var rec = _getJSON(key, { date: '', n: 0 });
    if (rec.date !== _today()) rec = { date: _today(), n: 0 };

    if (rec.n >= limit) {
      if (_analytics()) _analytics().trackPaywallHit('dailyLimit', 'limit_reached');
      showPaywall({
        tool: tool,
        feature: 'dailyLimit',
        title: 'Daily free limit reached',
        body: 'You have used all <strong>' + limit + '</strong> free runs today. Premium removes the limit on every tool.'
      });
      return { allowed: false, remaining: 0, tier: getTier() };
    }
    rec.n += 1;
    _setJSON(key, rec);
    return { allowed: true, remaining: Math.max(0, limit - rec.n), tier: getTier() };
  }

  /** 只读查询剩余次数（用于页面上显示 "2/3 free runs left today"） */
  function quota(tool) {
    var f = features(tool);
    var limit = f.dailyLimit;
    if (limit === Infinity || limit === undefined) return { limit: Infinity, used: 0, remaining: Infinity };
    var rec = _getJSON(KEYS.USE_PREFIX + tool, { date: '', n: 0 });
    var used = rec.date === _today() ? rec.n : 0;
    return { limit: limit, used: used, remaining: Math.max(0, limit - used) };
  }

  /* =====================================================================
     7. Paywall UI（自带样式，任何工具页无需额外 CSS）
     ===================================================================== */
  function _ensureStyles() {
    if (document.getElementById('osrs-paywall-style')) return;
    var s = document.createElement('style');
    s.id = 'osrs-paywall-style';
    s.textContent = [
      '.opw-mask{position:fixed;inset:0;background:rgba(26,15,5,.62);z-index:9998;display:flex;align-items:center;justify-content:center;padding:18px;}',
      '.opw-box{background:#fff;border:1px solid #e0d5c0;border-radius:14px;max-width:440px;width:100%;padding:26px 24px;box-shadow:0 18px 50px rgba(0,0,0,.28);font-family:inherit;}',
      '.opw-box h3{margin:0 0 10px;color:#3b2615;font-size:1.25rem;}',
      '.opw-box p{margin:0 0 14px;color:#3f3f3f;line-height:1.6;font-size:.95rem;}',
      '.opw-list{margin:0 0 18px;padding:0;list-style:none;}',
      '.opw-list li{color:#2f2f2f;font-size:.9rem;padding:5px 0 5px 22px;position:relative;}',
      '.opw-list li:before{content:"✓";position:absolute;left:0;color:#2e7d32;font-weight:800;}',
      '.opw-btn{display:block;width:100%;padding:13px;border:none;border-radius:9px;font-size:1rem;font-weight:700;cursor:pointer;text-align:center;text-decoration:none;margin-bottom:9px;}',
      '.opw-btn-main{background:#2e7d32;color:#fff;}',
      '.opw-btn-main:hover{background:#256428;}',
      '.opw-btn-alt{background:#fff;color:#3b2615;border:1px solid #cbb89a;}',
      '.opw-btn-alt:hover{background:#f6efe2;}',
      '.opw-close{background:none;border:none;color:#8a7a62;font-size:.86rem;cursor:pointer;display:block;margin:6px auto 0;}',
      '.opw-toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:#3b2615;color:#fff;padding:12px 20px;border-radius:9px;z-index:9999;font-size:.92rem;box-shadow:0 8px 24px rgba(0,0,0,.3);}',
      '.opw-banner{position:fixed;bottom:0;left:0;right:0;background:#3b2615;color:#fff;padding:13px 18px;z-index:9997;display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;font-size:.92rem;box-shadow:0 -4px 18px rgba(0,0,0,.25);}',
      '.opw-banner b{color:#d4af37;}',
      '.opw-banner button.opw-activate{background:#d4af37;color:#3b2615;border:none;border-radius:8px;padding:8px 16px;font-weight:700;cursor:pointer;font-size:.9rem;}',
      '.opw-banner button.opw-activate:hover{background:#e6c14e;}',
      '.opw-banner button.opw-dismiss{background:none;border:none;color:#cbb89a;cursor:pointer;font-size:.85rem;margin-left:4px;}',
      '@media(max-width:640px){.opw-box{padding:22px 18px;}.opw-banner{font-size:.84rem;}}'
    ].join('');
    document.head.appendChild(s);
  }

  function _perks(tool) {
    var m = MATRIX[tool];
    var out = [];
    if (m) {
      for (var k in m.premium) {
        if (!Object.prototype.hasOwnProperty.call(m.premium, k)) continue;
        var pv = m.premium[k], fv = m.free[k];
        if (k === 'dailyLimit') {
          if (fv !== Infinity) out.push(FEATURE_LABELS.dailyLimit);
          continue;
        }
        if (pv === true && fv !== true) out.push(FEATURE_LABELS[k] || k);
        if (typeof pv === 'number' && typeof fv === 'number' && pv > fv) {
          out.push('Up to ' + pv + ' saved items (free: ' + fv + ')');
        }
      }
    }
    out.push('Unlocks every premium tool on OSRS Guru');
    return out.slice(0, 6);
  }

  function showPaywall(opts) {
    opts = opts || {};
    _ensureStyles();
    var old = document.querySelector('.opw-mask');
    if (old) old.parentNode.removeChild(old);

    var tool = opts.tool || 'unknown';
    var label = FEATURE_LABELS[opts.feature] || opts.feature || 'this feature';
    var mask = document.createElement('div');
    mask.className = 'opw-mask';

    var planBtns = Object.keys(PRICES).map(function (k) {
      var p = PRICES[k];
      var cls = (k === 'year') ? 'opw-btn opw-btn-main' : 'opw-btn opw-btn-alt';
      var tag = (k === 'year') ? ' 🔥 best value' : '';
      return '<a class="' + cls + '" data-plan="' + k + '" href="#">' + p.label + ' — $' + p.usd + tag + '</a>';
    }).join('');

    mask.innerHTML =
      '<div class="opw-box" role="dialog" aria-modal="true">' +
        '<h3>🔓 ' + (opts.title || 'Unlock ' + label) + '</h3>' +
        '<p>' + (opts.body || '<strong>' + label + '</strong> is part of OSRS Guru Premium. Everything else on this tool stays free, forever.') + '</p>' +
        '<ul class="opw-list">' + _perks(tool).map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul>' +
        '<div style="font-size:.8rem;color:#7a6a52;margin:0 0 10px;text-align:center;">One payment, 3 plan lengths — pick what fits:</div>' +
        '<div style="font-size:.78rem;color:#2e7d32;margin:0 0 10px;text-align:center;font-weight:600;line-height:1.5;">After paying on Payhip, close that tab and refresh this page — Premium activates automatically.</div>' +
        planBtns +
        '<button class="opw-close" type="button">Maybe later — keep using the free version</button>' +
      '</div>';
    document.body.appendChild(mask);

    mask.querySelectorAll('[data-plan]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var plan = a.getAttribute('data-plan');
        if (_analytics()) _analytics().trackUpgradeClick('payhip_' + plan, opts.feature);
        var url = PAY_LINKS[plan];
        if (!url) { toast('⚠️ Payment link not configured yet.'); return; }
        _set(KEYS.PENDING_PLAN, plan); // 回跳时 success 页读此 plan 激活
        global.open(url, '_blank', 'noopener');
      });
    });
    mask.querySelector('.opw-close').addEventListener('click', function () { mask.remove(); });
    mask.addEventListener('click', function (e) { if (e.target === mask) mask.remove(); });
  }

  function toast(msg) {
    _ensureStyles();
    var t = document.createElement('div');
    t.className = 'opw-toast';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 3600);
  }

  /**
   * 在页面上渲染一个层级徽章（可选）
   * @param {string} selector - 容器选择器
   */
  function renderBadge(selector, tool) {
    var el = document.querySelector(selector);
    if (!el) return;
    if (isPremium()) {
      el.innerHTML = '<span style="background:#2e7d32;color:#fff;padding:4px 12px;border-radius:20px;font-size:.78rem;font-weight:700;">★ Premium · ' + daysRemaining() + 'd left</span>';
    } else {
      var q = quota(tool);
      var txt = q.limit === Infinity ? 'Free plan' : 'Free plan · ' + q.remaining + '/' + q.limit + ' runs left today';
      el.innerHTML = '<span style="background:#fdf8ef;border:1px solid #e6d9bd;color:#7a6a52;padding:4px 12px;border-radius:20px;font-size:.78rem;font-weight:700;">' + txt + '</span> ' +
        '<a href="#" class="opw-upsell" style="color:#2e7d32;font-weight:700;font-size:.8rem;text-decoration:none;">Upgrade →</a>';
      var link = el.querySelector('.opw-upsell');
      if (link) link.addEventListener('click', function (e) {
        e.preventDefault();
        if (_analytics()) _analytics().trackPaywallHit('badge_upsell', 'manual_click');
        showPaywall({ tool: tool, feature: 'adFree', title: 'OSRS Guru Premium' });
      });
    }
  }

  function onChange(fn) {
    if (typeof fn !== 'function') return function () {};
    _listeners.push(fn);
    try { fn({ tier: getTier(), isPremium: isPremium() }); } catch (e) {}
    return function () { var i = _listeners.indexOf(fn); if (i > -1) _listeners.splice(i, 1); };
  }
  function _notify() {
    var s = { tier: getTier(), isPremium: isPremium() };
    _listeners.forEach(function (f) { try { f(s); } catch (e) {} });
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
  }

  global.OSRSPremium = {
    init: init,
    getTier: getTier,
    isPremium: isPremium,
    daysRemaining: daysRemaining,
    features: features,
    hasFeature: hasFeature,
    require: require,
    consume: consume,
    quota: quota,
    showPaywall: showPaywall,
    renderBadge: renderBadge,
    activate: activate,
    deactivate: deactivate,
    onChange: onChange,
    toast: toast,
    getPlan: getPlan,
    MATRIX: MATRIX,
    FEATURE_LABELS: FEATURE_LABELS,
    PAY_LINKS: PAY_LINKS,
    PRICES: PRICES,
    PRICE: PRICE,
    PRICE_YEARLY: PRICE_YEARLY
  };
})(typeof window !== 'undefined' ? window : this);
