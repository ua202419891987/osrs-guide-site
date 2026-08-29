/*
 * OSRS Guru — Guide Paywall (static, trust-based)
 * Used by the 5 paid "Pain Point Fixes Pack" articles.
 * Payhip product: https://payhip.com/b/MVz2S  ($51.90)
 *
 * Behavior:
 *  - If localStorage token set  -> full article shows, nothing hidden.
 *  - If not set                 -> everything after <!-- PAYWALL --> is hidden,
 *                                  a paywall box with the Payhip CTA is injected.
 *  - "Activate" writes the token and reloads (manual return from Payhip).
 *
 * Note: static-site limitation — full HTML is in source. Trust model is
 * acceptable for a small site (same as tools osrs-subscription.js).
 */
(function () {
  "use strict";

  var PAY_LINK = "https://payhip.com/b/MVz2S";
  var TOKEN_KEY = "osrsguru_premium_pack";

  function isUnlocked() {
    try { return localStorage.getItem(TOKEN_KEY) === "1"; } catch (e) { return false; }
  }

  function unlock() {
    try { localStorage.setItem(TOKEN_KEY, "1"); } catch (e) {}
    location.reload();
  }

  function findMarker(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_COMMENT, null, false);
    while (walker.nextNode()) {
      if (walker.currentNode.nodeValue.indexOf("PAYWALL") > -1) return walker.currentNode;
    }
    return null;
  }

  function applyPaywall() {
    var marker = findMarker(document.body);
    if (!marker) return;

    // Hide every element sibling after the marker (stops at parent close,
    // so the footer and the trailing <style> block are never touched).
    var n = marker.nextSibling;
    while (n) {
      if (n.nodeType === 1) n.style.display = "none";
      n = n.nextSibling;
    }

    var box = document.createElement("div");
    box.className = "paywall-box";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Paid guide");
    box.innerHTML =
      '<div class="pw-inner">' +
        '<div class="pw-lock">🔒</div>' +
        '<h3 class="pw-title">This Guide Is Part of the<br>OSRS Guru Pain Point Fixes Pack</h3>' +
        '<p class="pw-sub">You\'ve read the free preview above. The complete, battle-tested walkthrough — every table, every step, every profit number — is unlocked in the pack.</p>' +
        '<div class="pw-price">$51.90 <span class="pw-once">one-time · lifetime access</span></div>' +
        '<div class="pw-actions">' +
          '<a class="pw-buy" href="' + PAY_LINK + '" target="_blank" rel="noopener">Buy the Pack on Payhip →</a>' +
          '<button class="pw-activate" type="button" data-activate>Already purchased? Activate here</button>' +
        '</div>' +
        '<p class="pw-note">After paying on Payhip, close that tab and click <strong>Activate here</strong> — the full guide unlocks instantly.</p>' +
      '</div>';

    marker.parentNode.insertBefore(box, marker.nextSibling);
    box.querySelector("[data-activate]").addEventListener("click", unlock);
  }

  // Inject paywall styles once.
  var style = document.createElement("style");
  style.textContent =
    ".paywall-box{margin:32px 0;padding:36px 28px;text-align:center;border:2px solid #7A64B8;border-radius:14px;" +
    "background:linear-gradient(160deg,#EDE8F5 0%,#E0D8F0 100%);box-shadow:0 10px 30px rgba(122,100,184,.18);}" +
    ".pw-inner{max-width:560px;margin:0 auto;}" +
    ".pw-lock{font-size:2.4rem;line-height:1;margin-bottom:10px;}" +
    ".pw-title{font-family:'Cinzel',serif;font-size:1.5rem;color:#7A64B8;margin:0 0 12px;font-weight:900;}" +
    ".pw-sub{color:#3a3450;font-size:1.02rem;line-height:1.7;margin:0 0 18px;}" +
    ".pw-price{font-size:2rem;font-weight:900;color:#1A1625;margin-bottom:20px;}" +
    ".pw-once{display:block;font-size:.8rem;font-weight:600;color:#7A64B8;letter-spacing:.5px;text-transform:uppercase;margin-top:4px;}" +
    ".pw-actions{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:14px;}" +
    ".pw-buy{display:inline-block;padding:.8rem 1.6rem;background:#7A64B8;color:#fff;text-decoration:none;border-radius:8px;font-weight:700;font-size:1rem;transition:opacity .2s;}" +
    ".pw-buy:hover{opacity:.88;}" +
    ".pw-activate{display:inline-block;padding:.8rem 1.2rem;background:transparent;color:#7A64B8;border:1.5px solid #7A64B8;border-radius:8px;font-weight:700;font-size:.92rem;cursor:pointer;transition:background .2s;}" +
    ".pw-activate:hover{background:rgba(122,100,184,.1);}" +
    ".pw-note{color:#6b6480;font-size:.85rem;line-height:1.6;margin:0;}" +
    "@media(max-width:640px){.paywall-box{padding:28px 16px;}.pw-title{font-size:1.25rem;}.pw-buy,.pw-activate{flex:1 1 100%;}}";
  document.head.appendChild(style);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      if (!isUnlocked()) applyPaywall();
    });
  } else {
    if (!isUnlocked()) applyPaywall();
  }
})();
