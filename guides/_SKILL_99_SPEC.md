# Skill/1-99 专栏标准化规范（2026-07-02）

> 本规范适用于 Phase 3：Skill/1-99 专栏 42 篇文章的 P0 标准化升级。
> 
> 基础规范与 `_MONEY_MAKING_SPEC.md` 完全一致；本文只补充 **Group B 14篇复盘后发现的坑点和模板差异**。

---

## 一、与 Money Making 完全一致的基础标准

参见 `guides/_MONEY_MAKING_SPEC.md` 第 1-10 条，核心要点：

1. Meta Description 必须以 `Updated for July 2026.` 开头
2. 文内日期统一改为 `July 2026`
3. Quick Summary 置顶，边框 `#D4CDE0`
4. 正文颜色 `#1a1a1a`
5. Box 背景变白，边框变浅棕色
6. 底部 CSS 覆盖块完整（含 `.quick-answer` / `.quick-jump`）
7. TOC 类名统一为 `toc`
8. Related Guides `.article-card` 样式覆盖
9. Canonical URL 正确
10. Header = 7 项导航（Home/Bosses/Money/Quests/Skills/Updates/Chinese）

---

## 二、Group B 复盘：必须避开的 7 个坑

### 坑 1：30秒快速预览不能是占位符

**错误示例（已发现多次）：**
```html
<div class="quick-summary">
  <h3>⏱️ Updated for July 2026</h3>
  <p>This guide has been reviewed and updated with the latest July 2026 OSRS game data...</p>
</div>
```

**正确标准：**
- 标题必须是 `30-Second Quick Summary` 或 `Quick Summary — 30-Second Read`
- 必须有 3-5 条 bullet points
- 每条 bullet 必须包含 **具体数字**：XP/hr、GP、时间、等级范围
- 必须让读者 30 秒内 get 到核心结论

**正确示例：**
```html
<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
  <strong style="color:#3b2615">⏱️ 30-Second Quick Summary</strong>
  <p style="color:#1a1a1a;margin:8px 0 0 0">Get 99 Crafting in OSRS by picking the right method for your budget:</p>
  <ul style="color:#1a1a1a;margin:10px 0 0 0;padding-left:18px">
    <li><strong>Fastest XP:</strong> Dragonhide bodies at 250K–350K XP/hr</li>
    <li><strong>Best Ironman:</strong> Giant seaweed glassblowing at ~120K XP/hr</li>
    <li><strong>Most profitable:</strong> Battlestaves at 100K–180K XP/hr</li>
    <li><strong>AFK friendly:</strong> Jewelry crafting at 30K–80K XP/hr</li>
  </ul>
</div>
```

---

### 坑 2：旧模板没有 Quick Summary，要主动插入

Group B 发现有 3 种旧模板：

**旧模板 A：guide-header 型**
```html
<main class="guide-content">
  <div class="container">
    <div class="guide-header">...</div>
    <div class="guide-intro">...</div>
    <!-- 这里缺 quick-summary -->
```
**处理方式：** 在 `guide-header` 或 `guide-intro` 之后插入 quick-summary，**然后再是 TOC**。

**旧模板 B：hero-section 图片型**
```html
<div class="hero-section">
  <img ... class="hero-image">
</div>
<article class="guide-content">
  <h1>...</h1>
  <div class="article-meta">...</div>
  <section class="intro">...</section>
  <nav class="table-of-contents">...</nav>
```
**处理方式：** 在 `article-meta` 之后、intro/TOC 之前插入 quick-summary。

**旧模板 C：hero-image 叠加型**
```html
<div class="hero-image">
  <img ...>
  <div class="hero-overlay">...</div>
</div>
<main class="main-content">
  <div class="container">
    <nav class="breadcrumb">...</nav>
    <header class="article-header">
      <h1>...</h1>
      <div class="article-meta">...</div>
    </header>
    <section class="article-intro">...</section>
    <nav class="table-of-contents">...</nav>
```
**处理方式：** 在 `article-header` 之后、`article-intro` 之前插入 quick-summary。

---

### 坑 3：TOC 类名不统一

Group B 发现旧模板使用：
- `<nav class="table-of-contents">`
- `<nav class="toc">`
- `<div class="toc">`

**标准：** 统一为 `<div class="toc">` 或 `<nav class="toc">`，结构必须是：
```html
<div class="toc">
  <h3>📋 Table of Contents</h3>
  <ol>
    <li><a href="#section-id">1. Section Title</a></li>
    ...
  </ol>
</div>
```

**如果文章完全没有 TOC：**
- 给每个 `<h2>` 添加 `id="xxx"`
- 提取 h2 标题生成 TOC
- 插入到 quick-summary 之后

---

### 坑 4：Hero 区域模板不一致

**标准 Hero：**
```html
<section class="guide-hero">
  <div class="container">
    <p class="breadcrumb"><a href="../index.html">Home</a> / ...</p>
    <h1>文章标题</h1>
    <p class="subtitle">副标题</p>
  </div>
</section>
```

**如果文章用的是旧 hero-section / hero-image：**
- 不要强制改成 `guide-hero`（会大改页面结构）
- 但需要在底部 CSS 中给 `.hero-section` / `.hero-image` 加上响应式规则，确保移动端不溢出
- 重点是：** visually 有 hero 即可，不强求 class 名**

---

### 坑 5：FAQ 只存在 JSON-LD，没有 HTML

Group B 发现多篇文章在 `<script type="application/ld+json">` 里有 FAQ，但正文没有 `<div class="faq-item">`。

**标准：** 每篇文章正文必须有 5-10 个 HTML faq-item：
```html
<div class="faq-item">
  <h3>❓ Question text?</h3>
  <p>Answer text...</p>
</div>
```

**如果文章没有 HTML FAQ：**
- 从 JSON-LD 中提取问答
- 或根据文章核心内容生成 5-8 个 FAQ
- 插入到正文末尾、Support Card 之前

---

### 坑 6：Support Card / Footer 在旧模板中缺失

**标准 Support Card（绝对不能改格式）：**
```html
<div class="support-card">
    <h3>🌿 Support This Guide</h3>
    <p>If this guide helped you, consider buying me a pack of gum! Your support keeps the guides coming.</p>
    <div class="support-buttons">
        <a href="https://www.paypal.com/paypalme/osrsguru/3usd" class="support-btn">$3</a>
        <a href="https://www.paypal.com/paypalme/osrsguru/5usd" class="support-btn support-btn-best">$5 ★</a>
        <a href="https://www.paypal.com/paypalme/osrsguru/10usd" class="support-btn">$10</a>
        <a href="https://www.paypal.com/paypalme/osrsguru" class="support-btn">Custom</a>
    </div>
</div>
```

**标准 Footer：**
```html
<footer>
  <p>&copy; 2026 OSRS Guru. All rights reserved.</p>
</footer>
```

**检查点：** 每篇文章 `</body>` 之前必须同时存在 support-card 和 footer。

---

### 坑 7：移动端适配缺 @media 查询

底部 CSS 覆盖块必须包含：
```css
@media (max-width: 768px) {
    .guide-content table { font-size: 0.85rem; }
    .guide-content table thead tr th { padding: 8px 10px; font-size: 0.8rem; }
    .guide-content table tbody td { padding: 6px 10px; }
    .guide-content h2 { font-size: 1.4em; }
    .guide-content h3 { font-size: 1.15em; }
}
@media (max-width: 640px) {
    .guide-content table { display: block; overflow-x: auto; }
    .guide-content h2 { font-size: 1.25em; }
    .guide-content h3 { font-size: 1.05em; }
}
```

**注意：** 如果文章有 `.hero-image` 或 `.hero-section` 等旧 hero 结构，额外加：
```css
@media (max-width: 768px) {
  .hero-image img, .hero-section img { max-width: 100%; height: auto; }
}
```

---

## 三、三组分工

### 一组：收尾 Group B（8 篇）
重点处理 Group B 中仍有结构问题的文章：
```
osrs-fastest-99-attack-strength-defence.html
osrs-fastest-99-cooking-f2p.html
osrs-how-to-get-99-agility-fast-2026.html
osrs-how-to-get-99-fishing-afk-method.html
osrs-how-to-train-prayer-cheap-f2p.html
osrs-maxing-99-order-guide-2026.html
osrs-optimal-leveling-guide-2026.html
osrs-range-training-1-99-guide-2026.html
```

**任务优先级：**
1. 确认 30s 摘要已存在且含 bullet
2. 给没有 TOC 的 5 篇生成 TOC
3. 给没有 HTML FAQ 的 7 篇生成 HTML FAQ
4. 确保 Support Card + Footer 存在
5. 确保底部 CSS 含 @media 768px/640px

### 二组：Group A 基础技能训练（14 篇）
```
osrs-1-99-crafting-guide-2026.html
osrs-1-99-hitpoints-training-guide-2026.html
osrs-1-99-hunter-guide-2026.html
osrs-1-99-magic-training-cheap-guide-2026.html
osrs-1-99-thieving-guide-ironman.html
osrs-agility-training-guide-2026.html
osrs-blast-furnace-smithing-guide-2026.html
osrs-cheapest-99-runecrafting-2026.html
osrs-construction-1-99-guide-2026.html
osrs-1-99-hitpoints-guide-2026.html
osrs-1-99-prayer-guide-2026.html
osrs-1-99-prayer-guide-all-methods-2026.html
osrs-ironman-1-99-smithing-guide.html
osrs-low-cost-1-99-herblore-guide.html
```

### 三组：Group C 综合技能策略（14 篇）
```
osrs-affordable-leveling-guide-2026.html
osrs-bond-farming-free-membership-2026.html
osrs-bond-farming-strategy-2026.html
osrs-complete-skill-training-guide-2026.html
osrs-leveling-milestones-guide-2026.html
osrs-sailing-1-99-guide-2026.html
osrs-sailing-afk-training-guide-2026.html
osrs-sailing-training-guide-2026.html
osrs-skill-training-after-sweep-up-2026.html
osrs-skill-training-endgame-guide-2026.html
osrs-skill-training-max-account-2026.html
osrs-skill-training-mid-game-guide-2026.html
osrs-skill-training-mid-game-optimization-2026.html
osrs-training-guide-complete-2026.html
```

---

## 四、验收脚本

运行以下脚本检查所有文件：
```bash
python .workbuddy/check_group_b_p0.py
```

目标结果：
- 30s: OK
- Meta: OK
- TOC: OK
- Hero: OK 或 已有 visual hero
- FAQ >= 5
- Support: OK
- Footer: OK
- CSS: OK
- Mobile: OK
- GA4/AdSense: OK

---

## 五、禁止事项

1. **不要改动正文内容、数据、表格内容**
2. **不要改动 support-card 格式**
3. **不要删除 GA4 / AdSense 脚本**
4. **不要引入禁用颜色**（红色系、蓝色系、绿色系）
5. **不要简单把旧模板全部推倒重写**——优先保留现有结构，只补缺失元素
