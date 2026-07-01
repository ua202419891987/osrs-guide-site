# Money Making 专栏标准化规范（2026-07-01）

> 本规范适用于 Money Making 专栏 38 篇文章的 P0 标准化升级。
> 目标：与已完成的 `osrs-money-making-beginner-2026.html` 保持同一套视觉和结构标准。

---

## 一、标准化动作清单（每篇必须做）

### 1. Meta Description 刷新
- 必须以 `Updated for July 2026.` 开头
- 包含具体数字（GP/hour、需求量、收益）
- 长度 150-160 字符
- 示例：
  ```html
  <meta name="description" content="Updated for July 2026. Make 200K-500K GP/h with these F2P money makers. Zero stats, step-by-step map routes, and verified GE prices.">
  ```

### 2. 更新日期
- `article-meta` 中的发布/更新日期改为 `July 2026`
- 文内出现的 `June 2026` / `2025` 等旧时间统一改为 `July 2026`

### 3. Quick Summary 置顶
- **位置**：正文内容区域最顶部，TOC 之前
- 正确结构示例：
  ```html
  <main class="guide-content">
      <div class="container">
          <div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem auto 2rem;max-width:780px;">
              <h3 style="color:#b8860b;font-size:1.05rem;margin:0 0 .8rem;font-weight:700;">⏱️ Quick Summary — 30-Second Read</h3>
              <ul style="margin:0;padding-left:1.2rem;list-style:none;color:#2D2A33;font-size:.92rem;line-height:1.8;">
                  <li>📌 <strong>要点 1</strong></li>
                  <li>📌 <strong>要点 2</strong></li>
                  <li>📌 <strong>要点 3</strong></li>
                  <li>📌 <strong>要点 4</strong></li>
                  <li>📌 <strong>要点 5</strong></li>
              </ul>
          </div>
          <div class="toc">...</div>
  ```
- 如果已有 Quick Summary，**剪切**到 container 之后；不要复制出两个
- 如果完全没有 Quick Summary，根据文章核心内容生成 4-5 条要点并插入

### 4. Quick Summary 边框加深
- 边框必须是 `#D4CDE0`
- 禁止使用 `#ebe5f0` 或更浅色

### 5. 正文颜色纯黑
- 搜索 `#e8d5b7`，如果在正文/段落/列表中出现，替换为 `#1a1a1a`
- 标题 `h1/h2` 可以保持棕色主题色，正文内容必须黑色

### 6. Box 背景变白 + 去掉深色边框
- 所有信息框、提示框、方法框必须白底 + 浅棕色边框
- 底部 CSS 必须覆盖以下类：
  `.tip-box`, `.method-box`, `.action-step`, `.quick-verdict`, `.faq-item`, `.warning-box`, `.info-box`, `.pro-tip-box`, `.note-box`, `.highlight-box`, `.strategy-box`, `.gear-box`, `.setup-box`, `.location-box`, `.next-steps`, `.bond-roadmap`, `.profit-box`, `.risk-box`, `.req-box`
- 同时加入通用规则清除 inline `border-left`：
  ```css
  .guide-content [style*="border-left:4px"],
  .guide-content [style*="border-left: 4px"],
  .guide-content [style*="border-left:3px"],
  .guide-content [style*="border-left: 3px"],
  .guide-content [style*="border-left:5px"],
  .guide-content [style*="border-left: 5px"] { border-left:0 !important; }
  ```

### 7. TOC 样式统一
- 如果 `<div class="table-of-contents">` 或 `<nav class="table-of-contents">`，改为 `class="toc"`
- 底部 CSS 中必须包含：
  ```css
  .guide-content .toc { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }
  ```

### 8. Related Guides article-card 样式
- 底部 CSS 必须包含：
  ```css
  .guide-content .related-guides .article-card { background:#f5f2f8 !important; border-color:#D4CDE0 !important; }
  .guide-content .related-guides .article-card:hover { background:#f0ecf5 !important; border-color:#9B84D4 !important; }
  ```

### 9. 底部 CSS 覆盖块（标准版）
在 `</body>` 前粘贴以下完整块（已有则替换）：

```html
<style>
.guide-content { color:#1a1a1a !important; }
.guide-content li,
.guide-content p,
.guide-content td,
.guide-content th,
.guide-content h3,
.guide-content h4 { color:#1a1a1a !important; }

.guide-content .tip-box,
.guide-content .method-box,
.guide-content .action-step,
.guide-content .quick-verdict,
.guide-content .faq-item,
.guide-content .warning-box,
.guide-content .info-box,
.guide-content .pro-tip-box,
.guide-content .note-box,
.guide-content .highlight-box,
.guide-content .strategy-box,
.guide-content .gear-box,
.guide-content .setup-box,
.guide-content .location-box,
.guide-content .next-steps,
.guide-content .bond-roadmap,
.guide-content .profit-box,
.guide-content .risk-box,
.guide-content .req-box { background:#fff !important; border:1px solid #e0d5c0 !important; }

.guide-content .tip-box p,
.guide-content .tip-box li,
.guide-content .method-box p,
.guide-content .method-box li,
.guide-content .faq-item p,
.guide-content .faq-item li,
.guide-content .quick-verdict p,
.guide-content .action-step p,
.guide-content .warning-box p,
.guide-content .warning-box li,
.guide-content .info-box p,
.guide-content .info-box li,
.guide-content .pro-tip-box p,
.guide-content .pro-tip-box li,
.guide-content .note-box p,
.guide-content .note-box li,
.guide-content .highlight-box p,
.guide-content .highlight-box li,
.guide-content .strategy-box p,
.guide-content .strategy-box li,
.guide-content .gear-box p,
.guide-content .gear-box li,
.guide-content .setup-box p,
.guide-content .setup-box li,
.guide-content .location-box p,
.guide-content .location-box li,
.guide-content .next-steps p,
.guide-content .next-steps li,
.guide-content .bond-roadmap p,
.guide-content .bond-roadmap li,
.guide-content .profit-box p,
.guide-content .profit-box li,
.guide-content .risk-box p,
.guide-content .risk-box li,
.guide-content .req-box p,
.guide-content .req-box li { color:#1a1a1a !important; }

.guide-content .faq-item h3,
.guide-content .faq-item h4,
.guide-content .method-box h3,
.guide-content .method-box h4,
.guide-content .quick-verdict h3,
.guide-content .action-step h4,
.guide-content .tip-box strong,
.guide-content .method-box strong,
.guide-content .warning-box strong,
.guide-content .info-box strong,
.guide-content .pro-tip-box strong,
.guide-content .note-box strong,
.guide-content .highlight-box strong,
.guide-content .strategy-box strong,
.guide-content .gear-box strong,
.guide-content .setup-box strong,
.guide-content .location-box strong,
.guide-content .next-steps strong,
.guide-content .bond-roadmap strong,
.guide-content .profit-box strong,
.guide-content .risk-box strong,
.guide-content .req-box strong { color:#3b2615 !important; }

.guide-content [style*="border-left:4px"],
.guide-content [style*="border-left: 4px"],
.guide-content [style*="border-left:3px"],
.guide-content [style*="border-left: 3px"],
.guide-content [style*="border-left:5px"],
.guide-content [style*="border-left: 5px"] { border-left:0 !important; }

.guide-content .related-guides .article-card { background:#f5f2f8 !important; border-color:#D4CDE0 !important; }
.guide-content .related-guides .article-card:hover { background:#f0ecf5 !important; border-color:#9B84D4 !important; }
.guide-content .toc { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }
.guide-content .quick-summary { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }

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
</style>
```

### 10. Canonical 标签检查
- 确保 `<link rel="canonical" href="https://osrsguru.com/guides/文件名">` 指向正确文件名

---

## 二、禁止事项

1. **不要改动 support-card 的格式**（绿色底色 + 白色文案是唯一允许的绿色区域）
2. **不要删除 GA4 / AdSense 脚本**
3. **不要修改文章内容、章节结构、FAQ、数据、表格内容**
4. **不要新增或删除章节**
5. **不要改变字体颜色覆盖逻辑**（正文黑，box 内黑，标题棕）
6. **不要出现 #e74c3c / #ff4444 / #8b0000 / #ff8c00 / #6ab8d4 / #4a7a9a / #1a2a3a / #0a0a1a / #2aad56 / #a0522d / #1a2e0a 等禁用颜色**

---

## 三、执行与验收

- 每组处理分配到的文件，每篇处理完汇报一行摘要
- 全部完成后，由另一组智能体交叉校对
- 校对重点：Quick Summary 置顶、边框 #D4CDE0、box 无深色边框、底部 CSS 完整
