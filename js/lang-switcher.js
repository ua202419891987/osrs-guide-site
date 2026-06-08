/**
 * OSRS Guru Language Switcher
 * 浮动语言切换按钮
 */
(function() {
  'use strict';

  function injectSwitcher() {
    var switcher = document.createElement('div');
    switcher.id = 'lang-switcher';
    switcher.innerHTML = '<a href="/">EN</a> | <a href="/zh/">中文</a>';
    switcher.style.cssText = 'position:fixed;top:10px;right:80px;z-index:9999;'
      + 'color:#d4af37;font-size:12px;font-family:sans-serif;'
      + 'background:rgba(39,33,26,0.9);padding:4px 10px;'
      + 'border:1px solid rgba(212,175,55,0.3);border-radius:4px;';
    document.body.appendChild(switcher);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectSwitcher);
  } else {
    injectSwitcher();
  }
})();