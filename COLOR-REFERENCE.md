# OSRS Guru 网站颜色还原参考文档
**生成日期：2026-06-12**
**用途：改颜色后若不好看，按此文档一键还原**

---

## 📁 备份文件位置
```
C:\Users\Lenovo\osrs-guide-site\css\style-backup-2026-06-12.css
```
> 直接复制此文件覆盖 `style.css` 即可完全还原。

---

## 🎨 CSS 变量完整列表（:root 部分）

### 主金色（Gold）
| 变量名 | 颜色值 | 用途 |
|--------|--------|------|
| `--gold` | `#d4a030` | 主金色（标题、强调） |
| `--gold-light` | `#ecc468` | 浅金色（链接 hover） |
| `--gold-dark` | `#a87c1e` | 深金色（按钮阴影） |
| `--gold-glow` | `rgba(212,160,48,0.35)` | 金色光晕 |

### 棕色系（Brown Palette）
| 变量名 | 颜色值 | 用途 |
|--------|--------|------|
| `--brown-deep` | `#2e1c0e` | 最深棕色（Header 背景、Footer 渐变起点） |
| `--brown-dark` | `#3b2615` | 深棕色（tip-box/cta-box 背景、Hero 渐变中段） |
| `--brown-main` | `#4a3320` | 主棕色（Hero 渐变终点） |
| `--brown-card` | `#593f28` | 卡片背景色 |
| `--brown-card-hover` | `#6b4d32` | 卡片悬停色 |
| `--brown-light` | `#7a5a3a` | 浅棕色 |
| `--brown-border` | `#8b6b45` | 边框棕色 |

### 背景色（Backgrounds）
| 变量名 | 颜色值 | 用途 |
|--------|--------|------|
| `--bg-page` | `#3b2716` | 页面主背景 |
| `--bg-warm` | `#433020` | 暖色背景 |
| `--bg-parchment` | `#5c442c` | 羊皮纸色背景 |
| `--bg-header` | `#2e1c0e` | Header 背景 |
| `--bg-hero-from` | `#3b2716` | Hero 渐变起点 |
| `--bg-hero-to` | `#4d3522` | Hero 渐变终点 |

### 文字颜色（Text）
| 变量名 | 颜色值 | 用途 |
|--------|--------|------|
| `--text-bright` | `#f2e4ce` | 最亮文字（标题） |
| `--text-primary` | `#e8d9bc` | 主文字颜色（正文） |
| `--text-secondary` | `#b8a078` | 次要文字（卡片描述） |
| `--text-muted` | `#8a7a60` | 淡化文字（日期、分类标签） |

### 强调色（Accents）
| 变量名 | 颜色值 | 用途 |
|--------|--------|------|
| `--accent-green` | `#4a7c3f` | 绿色强调（技能标签） |
| `--accent-red` | `#b84a3a` | 红色强调（Boss标签） |
| `--accent-blue` | `#3a6a8a` | 蓝色强调（任务标签） |

### 边框与阴影（Borders & Shadows）
| 变量名 | 颜色值 | 用途 |
|--------|--------|------|
| `--border-bronze` | `#6b5030` | 青铜色边框 |
| `--border-gold` | `#8b7040` | 金色边框 |
| `--border-highlight` | `#9a8050` | 高亮边框 |

---

## 🖥️ HTML 文件内联颜色（不可忽略）

### Hero 背景渐变（每篇文章必须一致）
```css
background: linear-gradient(135deg, #2a1a0a 0%, #3b2615 40%, #4a3320 100%);
```
> 也可用 CSS 类：`class="guide-hero"`

### tip-box / cta-box / callout 背景
```css
background: #3b2615;  /* 统一用这个，不要用 #2a1a0a（太暗） */
```

### 文章内联样式（每篇文章底部）
```html
<style>.guide-content li{color:#e8d5b7!important}</style>
```
> 仅此一行，不额外添加 p/h2/h3 样式

---

## 🟢 打赏模块（绝对不改）
```css
background: #2e7d32;  /* 唯一允许的绿色 */
color: #ffffff;        /* 白色文字 */
```
> 这是整个网站唯一允许绿色的区域，格式绝对不能改！

---

## 🦶 Footer 规范
```css
.site-footer {
  background: linear-gradient(180deg, #2e1c0e 0%, #3b2615 100%);
}
```
> 之前错误用了 `#1a0f08`（太黑），已修正为 `#3b2615`

---

## 🚫 严格禁止的颜色（曾经多次犯错）

### ❌ 红色系（禁止）
- `#e74c3c`、`#ff4444`、`#8b0000`、`#ff8c00`

### ❌ 蓝色系（禁止）
- `#6ab8d4`、`#4a7a9a`、`#1a2a3a`、`#0a0a1a`

### ❌ 绿色系（禁止，打赏模块除外）
- `#2aad56`、`#a0522d`、`#1a2e0a`

### ✅ 允许的颜色汇总
```
棕色：#2a1a0a  #2e1c0e  #3b2615  #4a3320  #593f28  #6b4d32  #7a5a3a  #8b6b45
金色：#d4a030  #ecc468  #a87c1e
文字：#f2e4ce  #e8d9bc  #e8d5b7  #b8a078  #8a7a60
绿色：#2e7d32  (仅打赏模块)
```

---

## 🔄 如何还原

### 方法一：用备份 CSS 文件（推荐）
```bash
# 复制备份文件覆盖当前 CSS
copy css\style-backup-2026-06-12.css css\style.css
git add css/style.css
git commit -m "还原网站颜色到2026-06-12版本"
git push origin main
```

### 方法二：手动改回 CSS 变量
打开 `css/style.css`，找到 `:root{` （大约第11行），将上方表格里的颜色值逐个改回。

### 方法三：GitHub 历史版本
1. 打开 https://github.com/ua202419891987/osrs-guide-site
2. 进入 `css/style.css`
3. 点击 `History` → 找到 `2026-06-12` 的提交
4. 点击 `View` → `Raw` → 复制全部内容 → 粘贴覆盖本地文件

---

## 📝 记忆要点
- **Hero 背景只允许棕色渐变**，不允许蓝/红/绿/黑色
- **tip-box 背景统一 `#3b2615`**，不用 `#2a1a0a`
- **打赏模块绿色 `#2e7d32` 绝对不改**
- **Footer 渐变终点 `#3b2615`**，不用 `#1a0f08`
- 改颜色前先备份，或确保此文档在手边

---

*文档生成于 2026-06-12 00:30 (GMT+8)*
*对应 commit: 3d5d23e（中文站全面翻译上线版本）*
