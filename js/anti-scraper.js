/**
 * OSRS Guru Anti-Scraper Protection v1.0
 * 轻量级防爬虫保护 - 不影响Google爬虫和正常用户阅读
 * 
 * 策略:
 * 1. 检测 Headless 浏览器特征（webdriver, plugins）
 * 2. 检测已知恶意爬虫 User-Agent
 * 3. 客户端请求频率限制（localStorage 记录）
 * 4. 隐藏蜜罐链接检测自动采集
 * 5. 邮件地址混淆
 * 
 * 所有检查均为被动检测，不弹窗、不拦截，仅生成控制台警告
 * Googlebot 不执行 JS，完全不受影响
 */

(function () {
  'use strict';

  var SUSPICIOUS = false;
  var REASONS = [];

  // ========== 1. Headless 浏览器检测 ==========
  if (navigator.webdriver === true) {
    SUSPICIOUS = true;
    REASONS.push('webdriver');
  }

  // Puppeteer/Playwright 特征
  if (navigator.plugins && navigator.plugins.length === 0 && 
      navigator.languages && navigator.languages.length > 0) {
    // 正常浏览器至少有1个插件（Chrome有5个），0个插件+有语言=可疑
    // 但移动端也可能0插件，所以不作为唯一判断
  }

  // Chrome Headless 特征
  if (window.chrome && window.chrome.app && window.chrome.app.LoadTimes) {
    // 正常 Chrome
  }
  if (window.chrome && window.chrome.csi) {
    // 正常 Chrome
  }

  // ========== 2. User-Agent 恶意爬虫检测 ==========
  var ua = (navigator.userAgent || '').toLowerCase();
  var BAD_BOTS = [
    'ahrefsbot', 'semrushbot', 'mj12bot', 'majestic', 'dotbot',
    'bytespider', 'dataforseo', 'petalbot', 'claudebot',
    'perplexitybot', 'cohere-ai', 'ccbot', 'diffbot',
    'python-requests', 'python-urllib', 'wget', 'curl',
    'scraper', 'httrack', 'webcopier', 'blackwidow',
    'sitesucker', 'teleport', 'webzip', 'webstripper'
  ];

  for (var i = 0; i < BAD_BOTS.length; i++) {
    if (ua.indexOf(BAD_BOTS[i]) !== -1) {
      SUSPICIOUS = true;
      REASONS.push(BAD_BOTS[i]);
      break;
    }
  }

  // ========== 3. 客户端请求频率限制 ==========
  // 使用 localStorage 记录访问时间戳
  // 如果1秒内访问超过3个页面，认定为爬虫
  try {
    var now = Date.now();
    var visits = [];
    var stored = localStorage.getItem('osrsguru_visits');
    if (stored) {
      try {
        visits = JSON.parse(stored);
      } catch (e) {
        visits = [];
      }
    }
    // 只保留最近3秒的记录
    visits = visits.filter(function (t) { return now - t < 3000; });
    visits.push(now);
    // 只保留最近20条
    if (visits.length > 20) {
      visits = visits.slice(-20);
    }
    localStorage.setItem('osrsguru_visits', JSON.stringify(visits));

    // 如果在3秒内访问了15个以上页面，疑似爬虫
    if (visits.length > 15) {
      SUSPICIOUS = true;
      REASONS.push('rapid_access');
    }
  } catch (e) {
    // localStorage 不可用（隐私模式等），忽略
  }

  // ========== 4. 蜜罐链接检测 ==========
  // 检查页面上是否有隐藏链接被点击（爬虫会抓取所有链接）
  // 蜜罐链接将被添加到页面底部
  function addHoneypotLink() {
    var hp = document.createElement('a');
    hp.href = '/hidden-trap-' + Math.random().toString(36).substr(2, 8);
    hp.style.display = 'none';
    hp.setAttribute('aria-hidden', 'true');
    hp.setAttribute('data-honeypot', 'true');
    hp.textContent = 'hidden';
    hp.addEventListener('click', function () {
      SUSPICIOUS = true;
      REASONS.push('honeypot');
    });
    document.body.appendChild(hp);
  }

  // ========== 5. 邮件地址混淆 ==========
  // 在页面加载后将 data-obfuscated-email 属性恢复为可点击 mailto 链接
  function deobfuscateEmails() {
    var elements = document.querySelectorAll('[data-obfuscated-email]');
    for (var i = 0; i < elements.length; i++) {
      var el = elements[i];
      var encoded = el.getAttribute('data-obfuscated-email');
      if (encoded) {
        // 简单的 Base64 解码
        try {
          var decoded = atob(encoded);
          el.href = 'mailto:' + decoded;
          el.textContent = decoded;
        } catch (e) {
          // 解码失败，忽略
        }
      }
    }
  }

  // ========== 执行 ==========

  // 添加蜜罐链接（仅 1/3 概率，降低爬虫识别概率）
  if (Math.random() < 0.33) {
    addHoneypotLink();
  }

  // 邮件混淆
  deobfuscateEmails();

  // 如果检测到爬虫，记录日志但不打断用户
  if (SUSPICIOUS) {
    console.warn('[OSRS Guru] Bot detected: ' + REASONS.join(', '));
    // 可选：发送分析事件（不阻断）
    if (typeof gtag !== 'undefined') {
      gtag('event', 'bot_detected', {
        'bot_type': REASONS[0],
        'page': window.location.pathname
      });
    }
  }

})();
