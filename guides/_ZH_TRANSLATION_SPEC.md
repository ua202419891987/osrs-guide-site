# 中文站（zh/）翻译与本地化标准规范

> 版本: v1.0 | 创建日期: 2026-07-04 | 适用范围: `zh/guides/*.html`
>
> 本文档总结了过去两轮（51篇赚钱文章）中文翻译的实操经验，
> 作为未来所有中文翻译工作的强制性标准。

---

## 一、核心原则

1. **双语结构，非全文翻译**：英文正文保留不动，只对标题、摘要、目录、表格头做中文标注。
2. **cn-title / cn-summary 是硬性要求**：每篇中文文章的 Hero 区域必须有中文标题和中文摘要，放在英文标题上方。
3. **零占位符**：不允许出现 `[待补充]`、`[原文]`、`TODO` 等任何占位文本。所有标注必须完成。
4. **工具推广文案改用 Freemium 表述**：禁止出现"免费"字样，使用"free estimates, premium features available"。

---

## 二、Hero 区域规范

### 2.1 cn-title（中文标题）

```html
<h1 class="cn-title">OSRS 赚钱方法完整指南 2026</h1>
<h1>OSRS Best Money Making Methods Guide 2026</h1>
```

- **cn-title** 是单独的一行 `<h1>`，带上 `class="cn-title"`
- 放在英文 `<h1>` 上方
- 中文标题格式：`OSRS + 中文主题 + 指南年份`
- 不要直译，要用玩家熟悉的 OSRS 中文术语

### 2.2 cn-summary（中文摘要）

```html
<p class="cn-summary">想要在 OSRS 中快速赚取金币？本指南覆盖从零基础...</p>
<p>Looking for the best money making methods in OSRS?...</p>
```

- `class="cn-summary"` 放在英文 summary 上方
- 50-100字，概括文章核心价值
- 用"本指南"开头，不要用"本文将"

### 2.3 30S Quick Preview（快速预览框）

```html
<div class="quick-summary">
    <div class="quick-summary-content">
        <h3>30秒快速预览</h3>
        <ul>
            <li><strong>适合玩家：</strong>...（中文）</li>
            ...
        </ul>
    </div>
</div>
```

- 标题用 **30秒快速预览**（不要写"30S Quick Preview"）
- 列表项全部用中文
- 格式与英文版一致（quick-summary + quick-summary-content）

---

## 三、目录（TOC）规范

### 3.1 TOC 条目双语标注

```html
<li><a href="#method-1">1. High-Level Bossing（高级Boss战赚钱）</a></li>
```

- 英文标题后加 `（中文翻译）`
- 格式：`英文标题（中文翻译）`
- 括号使用全角中文括号 `（）`

### 3.2 特殊情况

```html
<li><a href="#reasons">为什么需要这份指南？（Why You Need This Guide）</a></li>
```

- 如果中文标题在前，英文在后用 `（English Title）`
- 保持一致性，同一篇文章内格式统一

---

## 四、正文标题规范

### 4.1 二级标题（h2）

```html
<h2 id="method-1">1. High-Level Bossing（高级Boss战赚钱方法）</h2>
```

- 格式：`英文标题（中文说明）`
- 中文说明在括号内，跟在英文标题后面

### 4.2 三级标题（h3）

```html
<h3>Vorkath（巫妖王）</h3>
```

- 格式：`英文名称（中文名称）`
- Boss 名称、地点名称、物品名称使用 OSRS 中文社区通用译名

---

## 五、表格头翻译

表格 `<thead>` 中的 `<th>` 必须加中文标注：

```html
<thead>
    <tr>
        <th>Method（方法）</th>
        <th>GP/Hour（每小时金币）</th>
        <th>Requirements（要求）</th>
    </tr>
</thead>
```

- 格式：`英文（中文）`
- 所有表格列头都要加
- 表头单元格颜色保持 `#7A64B8` 品牌色

---

## 六、正文内容规则

- **正文段落保持英文不变**，不翻译
- 只有以下元素需要中文标注：
  - ✅ Hero 区域（cn-title, cn-summary）
  - ✅ 30S Quick Preview 框
  - ✅ TOC 条目
  - ✅ h2 / h3 标题
  - ✅ 表格 th
  - ✅ 图片 alt 文本
  - ✅ 按钮/CTA 文字
  - ✅ 打赏模块文案（保留英文但可加中文括号注释）
- **例外情况**：如果某段英文过于复杂，可以在段落前加一句中文引导（需用 `<!-- zh: 引导语 -->` 注释标记）

---

## 七、工具推广文案规范

### 7.1 禁止用词
| 禁止 | 原因 |
|------|------|
| "免费" / "free" | 我们的工具是付费的，无免费方案 |
| "Try our free..." | 误导用户，已被 QA 发现并修正 |
| "免费试用" | Gear Recommender 有3次免费查询但工具本身是 $1.90/月 |

### 7.2 正确表述（中文站版本）
```html
<p>需要更精准的装备推荐？试试我们的 OSRS Gear Recommender 工具——免费估价，高级功能需订阅。</p>
```

### 7.3 正确表述（英文站版本）
```html
<p>Need better gear advice? Try our OSRS Gear Recommender — free estimates, premium features available.</p>
```

---

## 八、内链与 Related Guides 规范

### 8.1 中文站内链
- 优先链接到 `zh/guides/` 目录下的中文版本
- 如果某篇文章没有中文版，才链到英文原版 `../guides/`

### 8.2 Related Guides 卡片
- 必须使用 `zh/guides/` 路径
- 卡片标题用中文
- 至少推荐 4-6 篇强关联文章

---

## 九、文件与 Git 操作规范

### 9.1 文件命名
```bash
# 中文版使用与英文版相同的文件名，放在 zh/guides/ 下
zh/guides/osrs-best-money-making-methods-2026.html
```

### 9.2 Created / Updated 元数据
```html
<meta name="created" content="2026-07-03">
<meta name="updated" content="2026-07-04">
<!-- zh: 首次中文翻译日期 -->
```

---

## 十、常见错误防错清单（来自 QA 复盘）

### P0 级（必须避免）
| # | 错误 | 正确做法 | 发现时间 |
|---|------|---------|---------|
| 1 | TOC 条目没有中文标注 | 每个 `<li>` 加 `（中文翻译）` | 2026-07-03 |
| 2 | Hero 区域缺少 cn-title | 必须写 `<h1 class="cn-title">` | 2026-07-03 |
| 3 | 30S Quick Preview 框写英文 | 全部改用中文 | 2026-07-03 |
| 4 | 表格 `<th>` 没有中文 | 每个列头加 `（中文）` | 2026-07-04 |
| 5 | 工具推广文案写"免费" | 用"free estimates"表述 | 2026-07-04 |

### P1 级（强烈建议）
| # | 错误 | 正确做法 | 发现时间 |
|---|------|---------|---------|
| 6 | h2/h3 用纯中文替换英文 | 保留英文标题+中文括号注释 | 2026-07-03 |
| 7 | 括号使用半角 `()` | 必须用全角 `（）` | 2026-07-03 |
| 8 | 使用了 `[待补充]` 占位符 | 必须补齐所有中文字段 | 2026-07-04 |
| 9 | cn-title 与英文 h1 之间空行不一致 | 保持 1 个空行 | 2026-07-04 |

---

## 十一、发布前检查清单

- [ ] cn-title 存在且内容完整
- [ ] cn-summary 存在且内容完整
- [ ] 30S Quick Preview 框是中文
- [ ] TOC 每个条目有中文标注
- [ ] 每个 h2 有 `（中文说明）`
- [ ] 每个 h3 有 `（中文名称）`
- [ ] 表格所有 `<th>` 有中文
- [ ] 没有任何 `[待补充]` 或占位文本
- [ ] 工具推广文案没有"免费"字样
- [ ] Related Guides 链接指向 `zh/guides/`
- [ ] 英文章节正文未意外删除
- [ ] 中文术语使用 OSRS 社区通用译名
- [ ] 页面底部 copyright 和 GA4 脚本未丢失
