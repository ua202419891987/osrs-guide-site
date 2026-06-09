/**
 * OSRS Guru — 收藏 / 进度条 / 游戏化 Checklist
 * 动态注入所有 UI，无需手动修改 115 篇文章
 */
(function () {
  'use strict';

  /* ========== 1. 注入 CSS ========== */
  const CSS = `
/* 收藏按钮 */
.guide-bookmark-btn{
  position:absolute;top:18px;right:18px;z-index:10;
  background:rgba(59,38,21,0.85);border:1px solid var(--border-bronze,#8b6914);
  border-radius:50%;width:38px;height:38px;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .25s ease;font-size:1.15rem;
  color:var(--text-secondary,#c8aa6d);
}
.guide-bookmark-btn:hover{
  background:rgba(212,175,55,0.18);border-color:var(--gold,#d4af37);
  color:var(--gold,#d4af37);transform:scale(1.12);
}
.guide-bookmark-btn.bookmarked{
  color:#ff6b6b;border-color:rgba(255,107,107,0.5);
  background:rgba(255,107,107,0.10);
}

/* 进度条 */
.progress-widget{
  background:linear-gradient(145deg,rgba(74,51,32,0.7),rgba(59,38,21,0.7));
  border:1px solid var(--border-bronze,#8b6914);border-radius:10px;
  padding:20px 24px;margin:24px 0;
}
.progress-widget .progress-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:12px;
}
.progress-widget .progress-title{font-family:'Cinzel',serif;color:var(--gold,#d4af37);font-size:1rem}
.progress-widget .progress-count{font-size:0.85rem;color:var(--gold-light,#d4af37);font-weight:700}
.progress-widget .progress-bar-track{
  width:100%;height:14px;background:rgba(0,0,0,0.35);
  border-radius:7px;overflow:hidden;border:1px solid rgba(212,175,55,0.15);
}
.progress-widget .progress-bar-fill{
  height:100%;border-radius:7px;
  background:linear-gradient(90deg,var(--gold-dark,#8b6914),var(--gold,#d4af37),var(--gold-light,#f0d080));
  transition:width .6s ease;position:relative;
}
.progress-widget .progress-footer{
  display:flex;justify-content:space-between;align-items:center;
  margin-top:10px;font-size:0.8rem;color:var(--text-muted,#8a7a5a);
}
.progress-widget .progress-link{color:var(--gold,#d4af37);text-decoration:none;font-size:0.82rem}
.progress-widget .progress-link:hover{text-decoration:underline}

/* Checklist */
.guide-checklist{margin:20px 0}
.guide-checklist .checklist-title{
  font-family:'Cinzel',serif;color:var(--gold,#d4af37);font-size:0.95rem;
  margin-bottom:10px;display:flex;align-items:center;gap:8px;
}
.guide-checklist .checklist-item{
  display:flex;align-items:flex-start;gap:10px;
  padding:9px 12px;border-radius:6px;
  transition:background .2s;cursor:pointer;font-size:0.88rem;
  color:var(--text-secondary,#c8aa6d);
}
.guide-checklist .checklist-item:hover{background:rgba(212,175,55,0.06)}
.guide-checklist .checklist-item input[type="checkbox"]{
  appearance:none;-webkit-appearance:none;
  width:18px;height:18px;flex-shrink:0;
  border:2px solid var(--border-bronze,#8b6914);border-radius:4px;
  background:rgba(0,0,0,0.25);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:all .2s;margin-top:1px;
}
.guide-checklist .checklist-item input[type="checkbox"]:checked{
  background:var(--gold,#d4af37);border-color:var(--gold,#d4af37);
}
.guide-checklist .checklist-item input[type="checkbox"]:checked::after{
  content:'✓';color:var(--brown-deep,#1a0f08);font-size:0.75rem;font-weight:700;
}
.guide-checklist .checklist-item.checked-label{
  color:var(--text-muted,#8a7a5a);text-decoration:line-through;
}

/* Toast */
.osrs-toast{
  position:fixed;bottom:24px;right:24px;z-index:9999;
  background:linear-gradient(135deg,var(--brown-deep,#3b2615),#2a1a0e);
  border:1px solid var(--gold,#d4af37);border-radius:10px;
  padding:14px 22px;color:var(--gold-light,#f0d080);
  font-size:0.88rem;box-shadow:0 6px 24px rgba(0,0,0,0.5);
  transform:translateY(80px);opacity:0;
  transition:all .35s cubic-bezier(.4,0,.2,1);
  max-width:320px;pointer-events:none;
}
.osrs-toast.show{transform:translateY(0);opacity:1;pointer-events:auto}
.osrs-toast .toast-icon{margin-right:8px}

/* 收藏面板 */
.bookmark-panel{
  position:fixed;top:0;right:-360px;width:340px;height:100vh;
  background:linear-gradient(180deg,var(--brown-deep,#3b2615),#1a0f08);
  border-left:2px solid var(--border-bronze,#8b6914);z-index:9998;
  transition:right .35s cubic-bezier(.4,0,.2,1);
  overflow-y:auto;padding:20px;box-shadow:-4px 0 24px rgba(0,0,0,0.5);
}
.bookmark-panel.open{right:0}
.bookmark-panel .panel-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:16px;
}
.bookmark-panel .panel-header h3{
  font-family:'Cinzel',serif;color:var(--gold,#d4af37);font-size:1.05rem;
}
.bookmark-panel .panel-close{
  background:none;border:none;color:var(--text-muted,#8a7a5a);
  font-size:1.3rem;cursor:pointer;
}
.bookmark-panel .bm-empty{
  text-align:center;color:var(--text-muted,#8a7a5a);font-size:0.88rem;
  padding:40px 0;
}
.bookmark-panel .bm-item{
  display:block;padding:10px 12px;border-radius:6px;
  color:var(--text-secondary,#c8aa6d);text-decoration:none;
  font-size:0.85rem;transition:background .2s;margin-bottom:4px;
}
.bookmark-panel .bm-item:hover{background:rgba(212,175,55,0.08);color:var(--gold-light,#f0d080)}
.bookmark-panel .bm-item .bm-item-cat{font-size:0.75rem;color:var(--gold,#d4af37);opacity:0.7}

/* 订阅浮条 */
.subscribe-bar{
  position:fixed;bottom:-80px;left:0;width:100%;z-index:9990;
  background:linear-gradient(90deg,rgba(59,38,21,0.95),rgba(74,51,32,0.95));
  border-top:2px solid var(--gold,#d4af37);
  padding:12px 24px;display:flex;align-items:center;justify-content:center;gap:16px;
  transition:bottom .4s ease;flex-wrap:wrap;
}
.subscribe-bar.show{bottom:0}
.subscribe-bar .sb-text{color:var(--gold-light,#f0d080);font-size:0.88rem;font-family:'Cinzel',serif}
.subscribe-bar .sb-btn{
  background:linear-gradient(180deg,var(--gold-light,#f0d080),var(--gold,#d4af37));
  color:var(--brown-deep,#1a0f08);font-family:'Cinzel',serif;
  font-weight:700;font-size:0.82rem;padding:8px 20px;
  border-radius:6px;border:1px solid var(--gold-dark,#8b6914);
  text-decoration:none;transition:all .2s;cursor:pointer;
}
.subscribe-bar .sb-btn:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(212,175,55,0.3)}
.subscribe-bar .sb-close{
  background:none;border:none;color:var(--text-muted,#8a7a5a);
  font-size:1.1rem;cursor:pointer;margin-left:8px;
}
`;

  function injectCSS() {
    const style = document.createElement('style');
    style.id = 'osrs-features-css';
    style.textContent = CSS;
    document.head.appendChild(style);
  }

  /* ========== 2. 工具函数 ========== */
  function getArticleSlug() {
    const path = window.location.pathname;
    const m = path.match(/guides\/([^.]+)\.html/);
    return m ? m[1] : null;
  }
  function getArticleTitle() {
    const h1 = document.querySelector('h1');
    return h1 ? h1.textContent.trim() : document.title;
  }
  function showToast(icon, msg) {
    let t = document.querySelector('.osrs-toast');
    if (!t) {
      t = document.createElement('div');
      t.className = 'osrs-toast';
      document.body.appendChild(t);
    }
    t.innerHTML = `<span class="toast-icon">${icon}</span>${msg}`;
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => t.classList.remove('show'), 2800);
  }

  /* ========== 3. 收藏按钮 ========== */
  function injectBookmarkBtn() {
    const hero = document.querySelector('.guide-hero');
    if (!hero) return;
    const slug = getArticleSlug();
    if (!slug) return;
    const bms = JSON.parse(localStorage.getItem('osrs-bm') || '{}');
    const btn = document.createElement('div');
    btn.className = 'guide-bookmark-btn' + (bms[slug] ? ' bookmarked' : '');
    btn.title = bms[slug] ? 'Bookmarked ✓ — click to remove' : 'Bookmark this guide';
    btn.innerHTML = bms[slug] ? '❤️' : '🤍';
    btn.addEventListener('click', () => {
      const cur = JSON.parse(localStorage.getItem('osrs-bm') || '{}');
      if (cur[slug]) {
        delete cur[slug];
        btn.classList.remove('bookmarked');
        btn.innerHTML = '🤍';
        btn.title = 'Bookmark this guide';
        showToast('🤍', 'Bookmark removed');
      } else {
        cur[slug] = { title: getArticleTitle(), url: window.location.pathname, t: Date.now() };
        btn.classList.add('bookmarked');
        btn.innerHTML = '❤️';
        btn.title = 'Bookmarked ✓ — click to remove';
        showToast('❤️', 'Bookmarked! Find all in your bookmarks.');
      }
      localStorage.setItem('osrs-bm', JSON.stringify(cur));
    });
    hero.style.position = hero.style.position || 'relative';
    hero.appendChild(btn);
  }

  /* ========== 5. 进度条 ========== */
  const TOTAL_GUIDES = 115;

  function getReadSet() {
    return new Set(JSON.parse(localStorage.getItem('osrs-read') || '[]'));
  }
  function markRead(slug) {
    const s = getReadSet();
    s.add(slug);
    localStorage.setItem('osrs-read', JSON.stringify([...s]));
  }

  function injectProgressBar() {
    const content = document.querySelector('.guide-content .container') || document.querySelector('.guide-content');
    if (!content) return;
    const slug = getArticleSlug();
    if (!slug) return;
    markRead(slug);
    const readSet = getReadSet();
    const pct = Math.min(100, Math.round(readSet.size / TOTAL_GUIDES * 100));

    const widget = document.createElement('div');
    widget.className = 'progress-widget';
    widget.innerHTML = `
      <div class="progress-header">
        <span class="progress-title">📊 OSRS Guru Progress</span>
        <span class="progress-count">${readSet.size} / ${TOTAL_GUIDES} guides (${pct}%)</span>
      </div>
      <div class="progress-bar-track">
        <div class="progress-bar-fill" style="width:${pct}%"></div>
      </div>
      <div class="progress-footer">
        <span>${readSet.size < TOTAL_GUIDES ? 'Keep reading to unlock all!' : '🏆 All guides tracked!'}</span>
        <a class="progress-link" href="#" onclick="document.querySelector('.bookmark-panel')?.classList.toggle('open');return false;">📖 My Bookmarks</a>
      </div>
    `;
    content.insertBefore(widget, content.firstElementChild);
  }

  /* ========== 6. 收藏面板 ========== */
  function injectBookmarkPanel() {
    const panel = document.createElement('div');
    panel.className = 'bookmark-panel';
    panel.innerHTML = `
      <div class="panel-header">
        <h3>📖 My Bookmarks</h3>
        <button class="panel-close" onclick="this.parentElement.parentElement.classList.remove('open')">✕</button>
      </div>
      <div class="bm-list"></div>
    `;
    document.body.appendChild(panel);

    function render() {
      const bms = JSON.parse(localStorage.getItem('osrs-bm') || '{}');
      const list = panel.querySelector('.bm-list');
      const keys = Object.keys(bms);
      if (!keys.length) {
        list.innerHTML = '<div class="bm-empty">No bookmarks yet.<br>Click 🤍 on any guide to save it.</div>';
        return;
      }
      list.innerHTML = keys.reverse().map(k => {
        const g = bms[k];
        return `<a class="bm-item" href="${g.url || '/guides/' + k + '.html'}">
          <div style="font-weight:600">${g.title || k}</div>
          <div class="bm-item-cat">Bookmarked</div>
        </a>`;
      }).join('');
    }
    render();
    // Re-render when panel opens (in case changed in another tab)
    const observer = new MutationObserver(render);
    observer.observe(panel, { attributes: true, attributeFilter: ['class'] });
  }

  /* ========== 7. 订阅浮条 ========== */
  function injectSubscribeBar() {
    if (localStorage.getItem('osrs-sub-dismissed')) return;
    const bar = document.createElement('div');
    bar.className = 'subscribe-bar';
    bar.innerHTML = `
      <span class="sb-text">📬 Get new OSRS guides in your inbox — weekly, no spam</span>
      <a class="sb-btn" href="https://docs.google.com/forms/d/e/1FAIpQLScdGhEYGMa_-_PJMFw1BBj_LrYLLHgtBBOtqsQu8SJnDyabMA/viewform" target="_blank" rel="noopener">Subscribe Free</a>
      <button class="sb-close" onclick="this.parentElement.classList.remove('show');localStorage.setItem('osrs-sub-dismissed','1')">✕</button>
    `;
    document.body.appendChild(bar);
    setTimeout(() => bar.classList.add('show'), 6000);
  }

  /* ========== 8. 自动将 TOC 变成可勾选 Checklist ========== */
  function enhanceTOC() {
    const toc = document.querySelector('.toc');
    if (!toc) return;
    const items = toc.querySelectorAll('li a');
    if (!items.length) return;

    // Only add checkboxes if not already done
    if (toc.querySelector('.toc-check')) return;

    const slug = getArticleSlug();
    const ckKey = 'osrs-ck-' + slug;
    const ckState = JSON.parse(localStorage.getItem(ckKey) || '{}');

    items.forEach((a, i) => {
      const li = a.parentElement;
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.className = 'toc-check';
      cb.checked = !!ckState[i];
      cb.addEventListener('change', () => {
        ckState[i] = cb.checked;
        localStorage.setItem(ckKey, JSON.stringify(ckState));
        if (cb.checked) li.classList.add('checked-label');
        else li.classList.remove('checked-label');
      });
      if (cb.checked) li.classList.add('checked-label');
      li.insertBefore(cb, a);
    });
  }

  /* ========== 9. 初始化 ========== */
  function init() {
    injectCSS();
    injectBookmarkBtn();
    injectProgressBar();
    injectBookmarkPanel();
    injectSubscribeBar();
    enhanceTOC();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
