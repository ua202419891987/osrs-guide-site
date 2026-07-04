# OSRS Guru Article Production - Shared Writing Brief

## P0 STANDARDS (MUST FOLLOW ALL)

### 1. Reference Article (READ FIRST)
- OSRS: `C:\Users\Lenovo\osrs-guide-site\guides\osrs-prayer-training-beginner-guide-2026.html`
- CD: `C:\Users\Lenovo\osrs-guide-site\guides\crimson-desert\crimson-desert-new-player-guide-2026.html`
- Copy the EXACT HTML structure: head, header, hero, content, support card, footer, scripts

### 2. CSS Path
- OSRS articles (in `guides/`): `<link rel="stylesheet" href="../css/style.css">`
- CD articles (in `guides/crimson-desert/`): `<link rel="stylesheet" href="../../css/style.css">`

### 3. Required Head Elements
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Keyword-rich title 50-60 chars] | OSRS Guru</title>
<meta name="description" content="[150-160 chars with primary keyword]">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="dns-prefetch" href="//www.google-analytics.com">
<meta name="keywords" content="[5-7 relevant keywords]">
<meta name="copyright" content="(c) 2026 OSRS Guru (osrsguru.com). All rights reserved.">
<link rel="canonical" href="https://osrsguru.com/guides/[filename].html">
<link rel="stylesheet" href="../css/style.css">
<!-- GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S1BGC91MYV"></script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-S1BGC91MYV');</script>
<!-- AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435" crossorigin="anonymous"></script>
```
- Also include JSON-LD: Article schema + FAQPage schema

### 4. Header Structure
- OSRS Logo: `<a href="../index.html" class="logo">OSRS <span>Guru</span></a>`
- CD Logo: `<a href="../../index.html" class="logo">Crimson Desert <span>Guru</span></a>`
- Nav links: Home, Skill Training, Money Making, Boss Guides (OSRS)

### 5. Article Body Structure (IN ORDER)
1. `<section class="guide-hero">` with breadcrumb, h1, subtitle, weekly-badge, publish date
2. **30S Quick Preview** box (use this exact format):
```html
<div class="quick-preview-box" style="background:#fff;border:1px solid #D4CDE0;border-left:4px solid #9B84D4;border-radius:8px;padding:20px;margin:24px 0;">
  <h3 style="margin:0 0 12px 0;color:#7a64b8;font-size:1.1rem;">⚡ 30S Quick Preview</h3>
  <ul style="margin:0;padding-left:18px;">
    <li style="color:#2d2a33;margin-bottom:6px;line-height:1.6;"><strong>Point 1:</strong> ...</li>
    <li style="color:#2d2a33;margin-bottom:6px;line-height:1.6;"><strong>Point 2:</strong> ...</li>
    <li style="color:#2d2a33;margin-bottom:6px;line-height:1.6;"><strong>Point 3:</strong> ...</li>
    <li style="color:#2d2a33;line-height:1.6;"><strong>Point 4:</strong> ...</li>
  </ul>
</div>
```
3. TOC (Table of Contents) with anchor links
4. 5+ content sections with `<h2>` headings
5. FAQ section (3-5 questions)
6. Related Guides section (3-5 internal links)
7. Support Card (EXACT format from reference - $1.90 Early Access Pack)
8. Footer with copyright
9. Copyright protection notice
10. JS: `<script src="../js/features.js"></script>` and `<script src="../js/ai-qa-widget.js"></script>`
11. Bottom style override block (copy from reference article)

### 6. Content Requirements
- 2500-4000 words per article
- ALL ENGLISH (no Chinese characters anywhere in the article)
- Include data tables where appropriate
- Use tip-box, method-box, action-step CSS classes
- 3-5 internal links to related articles (check existing files in guides/ for relevant links)
- Mobile responsive (tables, images with max-width)
- FAQ with JSON-LD structured data
- Include publish date: "Published: July 4, 2026"

### 7. Support Card (EXACT - copy from reference, do NOT modify)
The support card uses the $1.90 Early Access Guide Pack format. Copy the exact HTML from the reference article's support card section.

### 8. Forbidden Colors
- NO red: #e74c3c, #ff4444, #8b0000, #ff8c00
- NO blue: #6ab8d4, #4a7a9a, #1a2a3a, #0a0a1a
- NO green except support card: #2aad56, #a0522d, #1a2e0a
- Use: #3b2615, #4a3320, #d4af37, #7a64b8, #9B84D4, #D4CDE0, #2d2a33, #1a1a1a

### 9. Bottom Style Block (add before </body>)
Copy the complete style override block from the reference article (the block starting with `.guide-content{color:#1a1a1a!important}`).

### 10. Internal Linking
- Check existing articles in `guides/` directory for relevant links
- Use relative paths: `osrs-[topic]-guide-2026.html` (same directory)
- For CD articles: use `crimson-desert-[topic]-guide-2026.html` (same directory)
- Link to at least 3 related articles
