# Crimson Desert Article Writing Brief — June 2026

## ⚠️ CRITICAL: Writing Standards (MUST follow)

### 1. CD Guru Template (NOT OSRS Guru)
- Logo: `Crimson Desert <span>Guru</span>`
- Domain: `https://osrsguru.com/guides/crimson-desert/`
- CSS: `../../css/style.css`
- Header nav: Home / CD Guides / [section links] / FAQ

### 2. Color Theme (Purple "#7A64B8")
- Primary color: `#7A64B8` (purple)
- Background: `#f5f2f8` (light purple-gray)
- Cards/boxes: `#fff` with `1px solid #e0d8f0` border
- Text: `#2d2a33` (dark)
- Links: `#7A64B8`
- Tip-box: `background:#f8f6fc; border:1px solid #e0d8f0`
- Warn-box: `background:#fef9f5; border:1px solid #e8c8a0`
- Method-box: `background:#faf8fc; border:1px solid #e0d8f0`

### 3. Hero Section
```html
<section class="guide-hero">
  <div class="container">
    <p class="breadcrumb"><a href="../../index.html">Home</a> / <a href="index.html">Crimson Desert</a> / Article Name</p>
    <h1>Article Title</h1>
    <p class="subtitle">SEO description in 150 chars max</p>
    <div class="weekly-badge"><span class="badge-icon">🔧</span> <strong>Category</strong> — Part of the <strong>Crimson Desert Essentials Series</strong> · X min read</div>
    <p class="publish-date" style="color:#7A64B8;margin-top:8px;font-size:.85rem;">Published: June 28, 2026</p>
  </div>
</section>
```

### 4. TOC Format
```html
<div class="toc"><h3>Table of Contents</h3><ol>
  <li><a href="#section1">Section Title</a></li>
  <li><a href="#section2">Section Title</a></li>
  ...6-8 sections
</ol></div>
```

### 5. Body Structure
- h2 with emoji: 6-8 sections each with `<h2 id="sectionX">🎯 X. Title</h2>`
- Use tip-box/warn-box/method-box for callouts
- Use tables for comparison data
- FAQ section at end: `<h2 id="faq">❓ FAQ</h2>` with 6-8 `<div class="faq-item">`

### 6. Required Scripts
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S1BGC91MYV"></script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-S1BGC91MYV');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435" crossorigin="anonymous"></script>
```

### 7. Support Card (MUST copy exactly)
```html
<div class="support-card" style="margin:32px 0 0 0">
  <div class="support-inner">
    <span class="support-icon">🔓</span>
    <div class="support-text">
      <h3>Every guide is free — this one stays free either way.</h3>
      <p>No paywalls, no subscriptions. But the <strong>Early Access Guide Pack</strong> gives you more:</p>
      <p style="margin:6px 0 0 0;line-height:1.7">
        📚 <strong>10 Beginner Guides</strong> — zero to mid-game in one pack<br>
        ⭐ <strong>5 Premium Picks</strong> — our most popular expert deep-dives<br>
        ⏰ <strong>3-Day Early Access</strong> — read new guides before everyone else<br>
        🔄 <strong>3 New Guides Every Month</strong> — and each one fuels us to write faster
      </p>
      <p style="font-size:14px;margin:12px 0 0 0;opacity:0.85">✅ Your purchase includes instant access to everything above</p>
      <div class="support-amounts">
        <a href="https://www.paypal.com/paypalme/osrsguru/1.9" target="_blank" rel="noopener" class="support-amount-btn recommended">$1.90 — Get the Early Access Guide Pack 👑</a>
      </div>
      <p style="font-size:14px;margin:6px 0 0 0;opacity:0.85">Every guide stays free for everyone, always — no strings attached. 🤝</p>
    </div>
  </div>
</div>
```

### 8. Footer
```html
<footer>
  <div class="container">
    <p class="footer-bottom">&copy; 2026 CDGuru &middot; Not affiliated with Pearl Abyss &middot; <a href="../../index.html">Home</a></p>
    <p style="font-size:.78rem;color:#999;margin-top:4px">Crimson Desert&trade; is a trademark of Pearl Abyss Corp. All game content and materials are property of their respective owners. This guide is for informational purposes only and is not affiliated with, endorsed, or sponsored by Pearl Abyss.</p>
  </div>
</footer>
```

### 9. Bottom Scripts
```html
<script src="../../js/features.js"></script>
<script src="../../js/ai-qa-widget.js"></script>
<style>.guide-content li{color:#2d2a33!important}</style>
```

### 10. Style Block (inline in <head>)
```html
<style>
.guide-content h2{font-size:1.85rem !important}
.guide-content h3{font-size:1.35rem !important}
.guide-content p{font-size:1.08rem !important;line-height:1.85 !important}
.guide-content li{font-size:1.08rem !important;line-height:1.85 !important}
.tip-box{background:#f8f6fc;border:1px solid #e0d8f0;border-radius:8px;padding:1.2rem 1.5rem;font-size:1.06rem;color:#2d2a33;margin:1.5rem 0}
.tip-box strong{color:#7a64b8}
.warn-box{background:#fef9f5;border:1px solid #e8c8a0;border-radius:8px;padding:1.2rem 1.5rem;font-size:1.06rem;color:#2d2a33;margin:1.5rem 0}
.warn-box strong{color:#b84a3a}
.method-box{background:#faf8fc;border:1px solid #e0d8f0;border-radius:8px;padding:1.4rem;margin:1.25rem 0}
.method-box h4{color:#7a64b8;margin:0 0 .85rem 0;font-size:1.45rem}
.faq-item{margin:1rem 0;border-bottom:1px solid #e0d8f0;padding-bottom:1rem}
.faq-item h4{color:#7a64b8;font-size:1.15rem;margin-bottom:.6rem}
.toc{background:#fff;border:1px solid #e0d8f0 !important;border-radius:8px;padding:1.5rem 1.8rem;margin-bottom:2rem}
.toc h3{color:#7a64b8 !important;font-size:1.1rem !important;margin-bottom:12px}
.guide-hero .subtitle{font-size:1.15rem !important;max-width:700px;margin:0 auto 1.2rem}
.guide-content li{color:#2d2a33!important}
.progress-widget{display:none!important}
</style>
```

### 11. Canonical URL
```html
<link rel="canonical" href="https://osrsguru.com/guides/crimson-desert/[filename].html">
```

### 12. Meta Description
- Must be 150 chars or less
- Include keywords naturally
- Must be unique per article

### 13. Keywords
```html
<meta name="keywords" content="Crimson Desert, keyword1, keyword2, guide 2026">
```

### 14. Data Verification (CRITICAL!)
- All game data must be verified from official sources (Pearl Abyss website, patch notes)
- Reddit r/CrimsonDesert for player-reported issues and workarounds
- Google search to verify accuracy of common claims
- NEVER fabricate or guess game mechanics, drop rates, boss strategies, or item stats
- If unsure about a specific detail, indicate it with "(verify with in-game testing)"
- Use specific version numbers (e.g., Patch 1.12.02 from June 24, 2026)

### 15. SEO Strategy
- Target "Crimson Desert [topic]" keyword in title
- Use LSI keywords throughout body
- Target Google featured snippet with clear tables and lists
- Internal links to other CD Guru articles
- Minimum 1500 words per article, 2000+ recommended for key topics

### 16. Filename Convention
`crimson-desert-[topic-keywords]-guide-2026.html`
- All lowercase
- Hyphens between words
- Include "guide-2026" suffix
