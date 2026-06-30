# OSRS Guru 文章写作规范（最终版）

> 更新时间：2026-06-09
> 适用范围：osrsguru.com 所有 guides/ 目录下的攻略文章

---

## 一、文件命名规则

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 新手攻略 | `osrs-{topic}-beginner-guide-2026.html` | `osrs-mining-beginner-guide-2026.html` |
| 综合攻略 | `osrs-{topic}-guide-2026.html` | `osrs-money-making-guide-2026.html` |

- 全部小写，连字符 `-` 连接
- 年份统一用 `2026`
- 放在 `guides/` 目录下

---

## 二、HTML 文件头 & Meta 规范

### 1. 必须包含的 canonical 标签
```html
<link rel="canonical" href="https://osrsguru.com/guides/文件名.html">
```

### 2. CSS 路径（⚠️ 特别注意）
```html
<link rel="stylesheet" href="../css/style.css">
```
> guides/ 下的文章引用必须是 `../css/style.css`，不是 `../style.css`！

### 3. GA4 追踪代码（保留）
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S1BGC91MYV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-S1BGC91MYV');
</script>
```

---

## 三、文章结构模板（必须严格遵循）

从上到下顺序：

```
1. hero-image 头图
   └── 主视觉横幅，中世纪风格
   
2. h1 标题
   └── 含年份，含数字利益点，SEO友好
   
3. article-meta（发布信息）
   └── 必须包含：发布日期、作者、更新时间
   
4. intro（引言段落）
   └── 200-300字，概括全文核心价值和阅读收益
   └── 前3段每段至少1个站内链接
   
5. Quick Summary（30秒速览）
   └── ⏱️ Quick Summary &mdash; 30-Second Read
   └── 极浅紫背景 `#f5f2f8` + 极淡边框 `#ebe5f0`
   └── 3-5个要点，无序列表
   └── 参考格式见 osrs-bank-tags-beginners-guide-2026.html
   
5. TOC（Table of Contents / 目录）
   └── 可点击跳转，锚点链接
   
6. 正文章节（至少 5+ 个 h2 章节）
   └── 每个 h2 下含 2-4 个 h3 小节
   └── 内容深度 >3000 字
   └── 用表格、列表、数据对比丰富内容
   
7. FAQ（常见问题）
   └── 至少 5 个问题
   
8. Final Tips（最终建议 / 总结）
   └── 简洁有力的行动建议
   
9. CTA（Call to Action）
   └── 引导阅读相关文章或返回首页
   
10. Related Guides（相关攻略推荐）⚠️ 内链必查
    └── 至少 4 篇站内相关文章，全部必须是 `<a>` 链接，不能是纯文本
    └── 链接必须指向真实存在的 HTML 文件（先 `ls guides/` 确认文件名）
    └── 优先链接同主题文章，形成内容簇效应
    └── 示例格式：`<li><a href="osrs-xxx-guide-2026.html">文章标题</a></li>`
    
11. Support Card（打赏模块）⚠️ 格式绝对不能改！
    └── 唯一允许绿色的区域
    └── 绿色底色 + 白色文案
    
12. Footer（页脚）
    └── 必须包含：版权声明（Copyright © 2026 OSRS Guru）
```

---

## 四、页面元素位置顺序（严格）

```
正文内容
  → Related Guides（相关攻略）
  → Support Card（打赏框）
  → Footer（页脚）
```

---

## 五、打赏模块 Support Card（⚠️ 严禁修改）

**格式规范：**
- 背景色：`#2e7d32`（深绿色）
- 文字颜色：白色
- 这是整站**唯一允许使用绿色**的区域
- **不要改动任何 HTML 结构或样式**

直接使用现有模板中的 support-card 代码，只改文案内容，不改 class/style。

---

## 六、颜色规范（2026-06-30 更新 — 浅紫品牌色）

### 6.1 品牌色系（全站统一）

| 用途 | 色值 | 说明 |
|------|------|------|
| H1/H2 标题色 | `#7A64B8` (lavender-dark) | 全局 CSS 定义，不要 inline 覆盖 |
| H3/H4 标题色 | `#3b2615` | box/faq 内标题用 |
| 链接默认色 | `#9B84D4` (lavender) | 全局 CSS 定义 |
| 链接悬停色 | `#7A64B8` (lavender-dark) | 全局 CSS 定义 |
| 强调色（金色） | `#d4af37` | 用作左框/点缀 |
| 页面的极浅紫 | `#F5F2F8` | 页面背景色 |

### 6.2 正文字体色（所有文章必须覆盖）

| 元素 | 色值 |
|------|------|
| 正文 p / li / td / th | `#1a1a1a`（**纯黑**，不是 `#e8d5b7`） |
| Box 内文字 | `#1a1a1a` |
| Box 标题 | `#3b2615` |

> ⚠️ **重要**：之前使用的是 `#e8d5b7`（中世纪棕色主题），2026-06-30 统一为 **纯黑 `#1a1a1a`**，全文易读性优先。

### 6.3 区块背景色

| 元素 | 背景色 | 边框 |
|------|--------|------|
| Quick Summary | `#f5f2f8`（极浅紫） | `1px solid #ebe5f0`（极淡近无） |
| method-box / tip-box / faq-item | `#fff`（纯白） | `1px solid #e0d5c0`（浅棕） |
| Related Guides 卡片 (article-card) | `#f5f2f8`（极浅紫） | `1px solid #ebe5f0` |
| article-card 悬停 | `#f0ecf5`（略深紫） | `1px solid #D4CDE0` |
| Day 1-7 检查清单盒 | `#fff`（纯白） | `2px solid #e0d5c0` + `border-left:4px solid #d4af37` |
| 打赏模块 | `#2e7d32`（绿色，唯一） | 无边框、白色文字 |

> ⚠️ **禁止**：橙色渐变（`background:linear-gradient(135deg,#f5e6d3,#e8d5b8)`）、直白金色边框（`border:2px solid #d4af37`）

### 6.4 禁止使用的颜色

| 色系 | 禁止色值 | 原因 |
|------|---------|------|
| 橙/暖黄渐变 | `#f5e6d3 → #e8d5b8` | 2026-06-30 已全部替换为白底 |
| 红色 (装饰/警告外) | `#e74c3c, #ff4444` | 仅用于 NEW 角标 |
| 左侧紫色粗竖线 | `border-left:4px solid #7A64B8` | 已取消，太突兀 |

---

## 七、CSS 冲突修复（⚠️ 每篇文章底部必须加 — 2026-06-30 更新）

在 `</body>` 前添加以下 style 标签：

```html
<style>
.guide-content{color:#1a1a1a!important}
.guide-content li,.guide-content p,.guide-content td,.guide-content th,.guide-content h3,.guide-content h4{color:#1a1a1a!important}
.guide-content .tip-box,.guide-content .method-box,.guide-content .action-step,.guide-content .quick-verdict,.guide-content .faq-item{background:#fff!important;border-color:#e0d5c0!important}
.guide-content .tip-box p,.guide-content .tip-box li,.guide-content .method-box p,.guide-content .method-box li,.guide-content .faq-item p,.guide-content .faq-item li,.guide-content .quick-verdict p,.guide-content .action-step p{color:#1a1a1a!important}
.guide-content .faq-item h3,.guide-content .faq-item h4,.guide-content .method-box h3,.guide-content .method-box h4,.guide-content .quick-verdict h3,.guide-content .action-step h4,.guide-content .tip-box strong,.guide-content .method-box strong{color:#3b2615!important}
.guide-content .related-guides .article-card{background:#f5f2f8!important;border-color:#ebe5f0!important}
.guide-content .related-guides .article-card:hover{background:#f0ecf5!important;border-color:#D4CDE0!important}
</style>
```

**原因：** 全局 CSS 使用 `var(--text-secondary)` 和浅紫品牌色，需要 local 覆盖确保正文可读性。其中 `article-card` 两行是 Related Guides 卡片的浅紫风格。

---

## 八、内容质量要求

| 指标 | 标准 |
|------|------|
| 字数 | 3000+ 字 |
| 章节数 | 至少 5 个 h2 章节 |
| 子章节 | 每个 h2 下 2-4 个 h3 |
| 表格 | 至少 1 个数据表格 |
| 列表 | 善用有序/无序列表 |
| 数据 | 包含具体数字、GP/小时、时间估算 |
| 图片 | 适当位置插入示意图片 |
| 内链 | ⚠️ 严格要求：<br>① Related Guides 区块至少 4 个有效 `<a>` 链接（不能是纯文本）<br>② 正文前 3 段，每段至少 1 个内链（指向站内文章）<br>③ 内链必须指向真实存在的文件（先 `ls guides/` 确认） |

---

## 九、SEO 要求

1. **Title 标签**：含年份 + 数字 + 核心关键词，60 字以内
   - 例：`OSRS Skill Training Guide 2026: 1-99 Fastest Methods`

2. **Meta Description**：150-160 字，含关键词 + 利益点 + 行动召唤
   - 例：`Updated for 2026. Complete 1-99 skill training guide with fastest methods, GP/hour breakdowns, and F2P/P2P routes. Start leveling today.`

3. **H1 标题**：只能有一个，包含主关键词

4. **图片 Alt 文本**：每张图都要写描述性 alt

5. **内部链接**：⚠️ 严格要求：<br>① Related Guides 区块至少 4 个有效 `<a>` 链接<br>② 正文前 3 段每段至少 1 个内链<br>③ 链接必须指向真实存在的文件（先 `ls guides/` 确认文件名）

6. **锚点链接**：TOC 目录必须可点击跳转

---

## 十、⚠️ 历史错误防错清单（2026-06-09 整理）

> 以下错误均在实际文章中发现并修复过，新写文章**必须逐条自查**，绝不能重复犯。

### 🔴 P0 级（致命错误 — 直接影响收入/追踪）

| # | 错误类型 | 错误表现 | 正确做法 | 涉及文章 |
|---|---------|---------|---------|---------|
| 1 | **GA4 占位符未替换** | 写了 `G-XXXXXXXXXX` 或 `G-YOUR-GA-ID` 等占位 | 必须使用真实 ID `G-S1BGC91MYV`，搜索全文确认无占位符 | 文1/2/3 |
| 2 | **AdSense 代码缺失** | `</head>` 前没有 AdSense 脚本 | 每篇文章 `</head>` 前必须加 `ca-pub-8532760886171435` 广告代码 | 文1/2/3 |
| 3 | **Meta Description 不符公式** | 泛泛描述，没有具体数字和紧迫感 | 必须用公式：`Updated for 2026. [具体数字] [利益点]. [紧迫感/稀缺性]` | 全部10篇 |

### 🟡 P1 级（严重错误 — 影响结构/SEO）

| # | 错误类型 | 错误表现 | 正确做法 | 涉及文章 |
|---|---------|---------|---------|---------|
| 4 | **Support Card 格式错误** | 用了 `<section class="support-card">` + 按钮样式 | 必须用绿色 div：`background-color: #2e7d32`，白色文案，不要加按钮 | 文1/2 |
| 5 | **字数不足 3000** | 文章只有 2000-2900 字 | 写之前先规划章节大纲，确保 5+ 个 h2 且每节内容充实，写完用 Python 计数验证 | 文1/2/3 |
| 6 | **Header/Nav 缺失** | 文章没有顶部导航栏 | 必须有完整的 `<header>` + `<nav>` 导航（首页链接 + 分类链接） | 文3 |
| 7 | **Hero Image + article-meta 缺失** | 没有头图区域或没有发布日期 | 必须有 hero-image → h1 → article-meta（含发布日期） | 文3 |
| 8 | **Related Guides 坏链** | 链接指向不存在的 HTML 文件 | **必须先 `ls guides/` 确认文件名再写链接**，绝不能凭记忆猜 | 文3 |
| 9 | **发布日期过旧** | 用了旧日期如 January 2026 | 日期应为实际发布日期（当前写文章的日期） | 文1/2 |

### 🟢 P2 级（需注意 — 影响 UI/一致性）

| # | 错误类型 | 错误表现 | 正确做法 | 涉及文章 |
|---|---------|---------|---------|---------|
| 10 | **CSS 冲突修复遗漏** | 文章底部没有 `.guide-content li` 修复代码 | 每篇 `</body>` 前必须加 `<style>.guide-content li { color: #e8d5b7 !important; }</style>` | 新写文章偶尔遗漏 |
| 11 | **canonical href 文件名不一致** | canonical 里的文件名和实际文件名不匹配 | canonical 的 href 必须和实际文件名完全一致 | - |

### 📋 新文章发布前完整检查流程

```
Step 1: 搜索全文占位符
  → 搜索 "XXXXXXX" / "YOUR-" / "placeholder" → 确认无残留

Step 2: 验证追踪代码
  → GA4: G-S1BGC91MYV 出现 2 次（gtag.js + config）
  → AdSense: ca-pub-8532760886171435 出现 1 次（</head> 前）

Step 3: 检查 Meta Description
  → 必须以 "Updated for 2026." 开头
  → 必须含至少 1 个具体数字（如 "5 weapons", "23 skills"）
  → 必须含紧迫感（如 "before you spend millions", "don't waste your time"）

Step 4: 结构完整性
  → Header/Nav ✅ → Hero Image ✅ → H1 ✅ → article-meta(日期) ✅
  → Intro → TOC → 5+ H2 → FAQ(≥5) → Final Tips → CTA
  → Related Guides(≥4 个 <a> 链接) → Support Card(绿色div) → Footer(版权)

Step 5: 内链验证
  → ls guides/ 获取文件列表
  → Related Guides 的每个 href 必须在列表中
  → 正文前 3 段每段 ≥1 个内链

Step 6: 字数验证
  → Python 脚本统计英文单词数，必须 ≥3000

Step 7: CSS 修复
  → </body> 前有 .guide-content li { color: #e8d5b7 !important; }
```

---

## 十二、当前内容缺口（根据 GSC 搜索词）

根据 Google Search Console 真实搜索数据，以下文章优先级最高：

| 搜索词 | 文章建议标题 | 优先级 |
|--------|------------|--------|
| osrs training guides | OSRS Complete Skill Training Guide 2026 | 🔴 高 |
| osrs skill guide | OSRS Skill Guide 2026: All 23 Skills | 🔴 高 |
| zulrah vs vorkath | Zulrah vs Vorkath: Money & Gear Comparison 2026 | 🔴 高 |
| hitpoints training osrs | OSRS Hitpoints Training: 1-99 Fast Guide 2026 | 🟡 中 |
| khopesh osrs | OSRS Khopesh Guide: How to Get & Worth It? | 🟡 中 |

---

## 十三、快速检查清单（发布前必查）

- [ ] 文件名符合命名规则
- [ ] canonical 标签正确
- [ ] CSS 路径是 `../css/style.css`
- [ ] article-meta 含发布日期
- [ ] 打赏模块格式未改动（绿色底 + 白字）
- [ ] 页脚有版权声明
- [ ] 底部有 CSS 冲突修复代码
- [ ] 字数 > 3000
- [ ] 至少 5 个 h2 章节
- [ ] 至少 1 个表格
- [ ] 有 FAQ 部分
- [ ] 有 Related Guides 部分，且至少 4 个 `<a>` 链接（不能是纯文本）
- [ ] Related Guides 的链接全部指向真实存在的文件（已用 `ls guides/` 确认）
- [ ] 正文前 3 段，每段至少 1 个内链（指向站内文章）
- [ ] 图片有 alt 文本
- [ ] Title 和 Description 已优化
- [ ] ⚠️ GA4 代码是 `G-S1BGC91MYV`（不是占位符 G-XXXXXXXXXX / G-YOUR-GA-ID）
- [ ] ⚠️ AdSense 代码 `ca-pub-8532760886171435` 在 `</head>` 前
- [ ] ⚠️ Meta Description 以 "Updated for 2026." 开头，含具体数字+紧迫感
- [ ] ⚠️ Support Card 是绿色 div（不是 section + 按钮格式）
- [ ] ⚠️ 全文搜索 "XXXXXXX" / "YOUR-" / "placeholder" 确认无残留占位符
