# OSRS Guru pt-br/ 巴西站质量审核报告

**审核日期**: 2026-07-01  
**审核范围**: `C:\Users\Lenovo\osrs-guide-site\pt-br\` 下全部 214 个 HTML 文件  
**审核结论**: 不合格 — 发现 10 类问题，涉及大量文件

---

## 总体摘要

| 优先级 | 问题类别 | 涉及文件数 | 严重程度 |
|--------|----------|-----------|----------|
| P1 | 文章正文大量英文未翻译 | ~200+ | 严重 |
| P1 | og:title 全部为英文 | ~80+ | 严重 |
| P1 | meta description 英文未翻译 | ~80+ | 严重 |
| P1 | Footer 免责声明英文未翻译 | 38 | 高 |
| P1 | "Your go-to resource" 英文作者标签 | 42 | 高 |
| P1 | 页面内容提及"chinês/em chinês" | 2 | 高 |
| P2 | hreflang="x-default" 指向 pt-br 而非 en | 18 | 中 |
| P2 | 缺少 hreflang 标签 | 19 | 中 |
| P2 | 破损的 HTML 标签 | 1 | 高 |
| P3 | 单词拼接/损坏（Investimentoimentoment） | 4 | 中 |
| P3 | 中文全角双横线（——）残留 | 30+ | 低 |
| P3 | 缺少 og:title/og:description 标签 | 大量 | 中 |

---

## P1 — 未翻译内容（高优先级）

### 1.1 文章正文大量英文未翻译（~200+ 文件）

几乎所有 `pt-br/guides/` 下的攻略文章正文内容为**英文原文**，未翻译成葡萄牙语。包括：

- 标题/段落/列表项/TOC 目录/表格对比/FAQ 问答 — 全部英文
- 示例文件：`osrs-1-99-crafting-guide-2026.html`、`osrs-new-player-guide-2026.html` 等

抽查的 `osrs-new-player-guide-2026.html:66-87`：
```html
<li>📌 <strong>Account security in 5 min:</strong> Enable JAG + Authenticator + Bank PIN...</li>
```
```html
<h3>① Table of Contents</h3>
<ol>
    <li><a href="#what-is-osrs">What is OSRS? (30-Second Version)</a></li>
    <li><a href="#account-setup">Account Creation & Safety Basics</a></li>
    ...
</ol>
```

**影响**: 用户看到的攻略内容完全是英文，完全失去翻译价值。

---

### 1.2 og:title 全部为英文（~80+ 文件）

几乎所有攻略文章的 og:title 使用英文格式 `"OSRS — OSRS [English Title] 2026 — [English Subtitle]"`，例如：

| 文件 | og:title 内容 |
|------|--------------|
| `index.html` | `OSRS Guru — Complete OSRS Guias + AI Assistant 2026` |
| `guides/osrs-1-99-crafting-guide-2026.html` | `OSRS — OSRS 1-99 Crafting Guide (2026) – Fast, Cheap & Ironman Methods` |
| `guides/osrs-new-boss-loot-guide-2026.html` | `OSRS Boss — OSRS New Boss Guide 2026 — Kill Strategy & Loot Breakdown` |
| `guides/osrs-fire-cape-jad-guide-2026.html` | `OSRS — OSRS Fire Cape Guide 2026 — Jad Strategy & Budget Setup` |
| `guides/osrs-boss-profit-comparison-2026.html` | `OSRS — OSRS Boss Profit Comparison 2026: S-Tier Bosses Make 10M-15M GP/hr` |

---

### 1.3 meta description 英文未翻译（~80+ 文件）

绝大多数攻略文章的 meta description 使用英文：

| 文件 | meta description |
|------|-----------------|
| `guides/blood-moon-rises-quest-guide-2026.html` | `Complete OSRS The Blood Moon Rises quest guide 2026...` |
| `guides/osrs-1-99-crafting-guide-2026.html` | `OSRS (2026) GP/ Complete OSRS 1-99 Crafting guide...` |
| `guides/osrs-corrupted-gauntlet-guide-2026.html` | `Complete OSRS Corrupted Gauntlet guide for 2026...` |
| `guides/osrs-money-making-beginner-2026.html` | `OSRS (2026) GP/ Complete beginner money making guide...` |

且所有 meta description 前缀 `OSRS (2026) GP/` 应改为葡语如 `OSRS (2026) GP/h` 或类似本地化格式。

---

### 1.4 Footer 免责声明英文未翻译（38 文件）

**全英文版**（25 个文件）：
```
Some links on this site are affiliate links. We may earn a small commission at no extra cost to you.
```
文件列表：`osrs-1-99-hunter-guide-2026.html`, `osrs-best-money-making-methods-2026.html`, `osrs-bond-farming-free-membership-2026.html`, `osrs-bond-vs-subscription-2026.html`, `osrs-cancel-membership-refund-2026.html`, `osrs-cheapest-membership-2026.html`, `osrs-curse-of-the-empty-lord-quest-2026.html`, `osrs-f2p-leveling-guide-2026.html`, `osrs-f2p-money-making-first-bond-2026.html`, `osrs-f2p-quests-before-membership-2026.html`, `osrs-f2p-to-member-first-10-things-2026.html`, `osrs-fastest-hunter-training-2026.html`, `osrs-fastest-leveling-guide-2026.html`, `osrs-ironman-membership-guide-2026.html`, `osrs-leveling-milestones-guide-2026.html`, `osrs-members-vs-f2p-comparison-2026.html`, `osrs-membership-worth-it-2026.html`, `osrs-membership-price-increase-2026.html`, `osrs-training-guide-complete-2026.html`, `osrs-viggora-guide-2026.html`, `osrs-viggora-chainmace-guide-2026.html` 等

**混合版**（1 文件）：
- `index.html:1285` — 部分混合：`"Este site pode conter links de afiliados. Ganhamos uma pequena comissão at no extra cost to you."`

**Jagex Fan Content Policy 全英文版**（12+ 文件）：
```
Created using Jagex Limited's intellectual property. Complies with Jagex Fan Content Policy terms. This content is not endorsed by or affiliated with Jagex.
```
文件：`osrs-1-99-mining-guide-beginner-2026.html:1211`, `osrs-combat-training-beginner-2026.html:695`, `osrs-f2p-combat-training-guide-2026.html:796`, `osrs-money-making-beginner-2026.html:433`, `osrs-slayer-beginner-guide-2026.html:436` 等

**混合版**（`index.html:1286`）：
```
Criado usando propriedade intelectual da Jagex Limited's intellectual property.
...Este conteúdo não é endossado por or afiliado à Jagex. OSRS is a trademark of Jagex Ltd.
```
问题："or" 应为 "ou"，"is a trademark of" 应翻译。

---

### 1.5 "Your go-to resource" 英文作者标签（42 文件）

大量攻略文章的作者行使用英文：
```html
<strong>Author:</strong> OSRS Guru — Your go-to resource for Old School RuneScape strategy guides.
```
和 Footer 中的：
```html
<p>Your go-to resource for OSRS strategy guides. ...</p>
```

涉及文件：
- `index.html:1248`（footer）
- `guides/osrs-1-99-hunter-guide-afk-method.html:276`
- `guides/osrs-1-99-woodcutting-guide-early-game.html:284`
- `guides/osrs-1-99-thieving-guide-ironman.html:256`
- `guides/osrs-fire-cape-jad-guide-2026.html:265`
- `guides/osrs-how-to-beat-zulrah-beginners-rotation.html:271`
- `guides/osrs-ironman-money-making-f2p-2026.html:352`
- `guides/osrs-skills-overview-beginner-2026.html:601`
- 及其他 35+ 文件

---

### 1.6 页面内容提及"chinês/em chinês"（2 文件 — 严重）

`atualizacoes-mensais.html` 和 `atualizacoes-semanais.html` 的内容明确提及这是"中文站点"：

**atualizacoes-mensais.html**:
- `:15` `og:title`: `"OSRS Atualizações Mensais 2026 — Explicação detalhada em chinês"`
- `:16` `og:description`: `"Cada edição...Publicar interpretação detalhada em chinês dentro de horas"`
- `:48` body: `"Explicação detalhada em chinês dentro de horas"`
- `:127` body: `"Publicar explicação detalhada em chinêsGuia"`
- `:128` nav: `"Voltar OSRS Guru ChinêsInício"`
- `:135` footer: `"OSRSChinêsGuia"`

**atualizacoes-semanais.html**:
- `:14` `keywords`: `"OSRS ChinêsGuia"`
- `:15` `og:title`: `"OSRS Atualizações Semanais — Site chinês"`
- `:119` nav: `"Voltar OSRS Guru ChinêsInício"`
- `:126` footer: `"OSRSChinêsGuia"`

**这是严重的本地化错误**，巴西站不应该自称中文站点。

---

### 1.7 导航和按钮英文（多处）

- `index.html:64`: `"🇺🇸 English Main Site"` — 应为葡语如 `"🇺🇸 Site em Inglês"`
- `comunidade.html:15`: `"🇺🇸 English"` — 同上
- `index.html:1301` JS: `btn.textContent = 'Show less ↑'` — 应为葡语
- `lucro.html:33`: `"🇺🇸 English"` — 同上

---

### 1.8 广告标签英文（10+ 处）

多个 Hub 页面使用英文广告标签：
```html
<span class="ad-label">Sponsor Recommendation</span>
```
出现于：`chefes.html`, `habilidades.html`, `iniciante.html`, `missoes.html`（各 2-3 处）

---

## P2 — HTML 结构问题

### 2.1 破损的 HTML 标签（1 处）

**`lucro.html:50`** — h1 标签完整性损坏：
```html
<h1💰 OSRS Guias de Lucro 2026> class="article-title"</h1>
```
正确应为：
```html
<h1 class="article-title">💰 OSRS Guias de Lucro 2026</h1>
```

### 2.2 hreflang="x-default" 指向 pt-br 而非 en（18 文件）

根据 SEO 最佳实践，`x-default` 应指向站点的默认/英文版本。但在这些文件中 x-default 指向了 pt-br：

| 文件 | x-default href |
|------|---------------|
| `chefes.html` | `https://osrsguru.com/pt-br/boss-guides.html` |
| `habilidades.html` | `https://osrsguru.com/pt-br/skill-training.html` |
| `iniciante.html` | `https://osrsguru.com/pt-br/beginner.html` |
| `lucro.html` | `https://osrsguru.com/pt-br/money-making.html` |
| `membros.html` | `https://osrsguru.com/pt-br/membership.html` |
| `missoes.html` | `https://osrsguru.com/pt-br/quest-guides.html` |
| `guides/osrs-afk-money-making-ultimate-guide-2026.html` 等 12 个 guides |

同时这些文件的 `hreflang="en"` 也指向了 pt-br URL，需要修复。

### 2.3 缺少 hreflang 标签（19 文件）

**Hub 页面（1 个）**:
- `comunidade.html`

**攻略文章（18 个）**:
- `guides/osrs-achievement-diary-beginner-guide-2026.html`
- `guides/osrs-barrows-tunnel-optimization-2026.html`
- `guides/osrs-birdhouse-runs-guide-2026.html`
- `guides/osrs-blast-furnace-smithing-guide-2026.html`
- `guides/osrs-clue-scrolls-beginner-guide-2026.html`
- `guides/osrs-common-beginner-mistakes-avoid-2026.html`
- `guides/osrs-construction-1-99-guide-2026.html`
- `guides/osrs-dagannoth-kings-guide-2026.html`
- `guides/osrs-death-mechanics-guide-2026.html`
- `guides/osrs-f2p-gear-progression-guide-2026.html`
- `guides/osrs-f2p-slayer-guide-2026.html`
- `guides/osrs-first-week-progression-guide-2026.html`
- `guides/osrs-gear-upgrade-priority-order-2026.html`
- `guides/osrs-grand-exchange-flipping-guide-2026.html`
- `guides/osrs-money-making-zero-req-2026.html`
- `guides/osrs-new-player-guide-2026.html`
- `guides/osrs-zero-req-moneymaker-2026.html`
- `guides/vault-of-ralos-raid-guide-2026.html`

### 2.4 og:title/og:description 重复/乱码（3 文件）

`osrs-corrupted-gauntlet-guide-2026.html:17`:
```html
<meta property="og:title" content="OSRS OSRS Corrupted Gauntlet Guide 2026 Budget Setup">
<meta property="og:description" content="OSRS 2026:GP/,,.Master the Corrupted Gauntlet...">
```
问题："OSRS OSRS" 重复、og:description 包含乱码 `:GP/,,.`

`osrs-nightmare-phosanis-guide-2026.html:20`:
```html
<meta property="og:title" content="OSRS Boss OSRS Nightmare & Phosani's Guide 2026">
<meta property="og:description" content="OSRS Guias de Chefes2026:GP/,,.Complete Nightmare...">
```
问题：og:description 含葡语+英文混合乱码

`osrs-slayer-block-skip-list-2026.html:16`:
```html
<meta property="og:description" content="OSRS 2026:GP/,,.Complete Slayer task optimization...">
```
问题：前缀乱码

---

## P3 — 内容质量问题

### 3.1 单词拼接/损坏（4 处）

产品名/术语翻译过程中 "Investment" 与 "Investimento" 混合导致单词损坏：

| 文件 | 损坏的单词 |
|------|-----------|
| `guides/osrs-combat-money-making-non-boss-2026.html:427` | `Investimentoimentoments` |
| `guides/osrs-skilling-money-post-sailing-2026.html:407` | `Investimentoimentoments` |
| `guides/osrs-skills-progression-path-2026.html:81` | `Investimentoimentoment` |
| `guides/osrs-viggora-chainmace-guide-2026.html:89` | `Investimentoimentoment` |

正确应为葡语 **"Investimento"** 或 **"Retorno sobre Investimento"**。

### 3.2 中文全角双横线 "——" 残留（30+ 处）

虽然是标点符号（U+2014 × 2），不是中文字符，但全角双横线在葡语/英文排版中不应使用。应替换为半角双横线 `--` 或 em dash `—`。

主要出现文件：
- `habilidades.html:10,42`
- `chefes.html:10`
- `iniciante.html:114`
- `membros.html:93,123,129,153`
- `topicos-populares.html:78,86,94,102,126,134,150,174,182`
- `blood-moon-rises-quest-guide-2026.html:7`
- `combat-achievements-guide-2026.html:7`
- `osrs-cheapest-membership-2026.html:159`
- `osrs-desert-treasure-quest-guide-low-level.html:13`
- `osrs-goraik-rewards-worth-it-2026.html:7`
- `osrs-herb-run-mastery-guide-2026.html:192`
- `osrs-how-to-spend-gp-wisely-2026.html:164,196`
- `osrs-how-to-unlock-fairy-rings.html:13`
- `osrs-khopesh-guide-2026.html:7`
- `osrs-low-cost-1-99-herblore-guide.html:183`
- `osrs-money-making-fishing-2026.html:172`
- `osrs-poh-optimal-layout-guide-2026.html:141`

### 3.3 英文版权文本（更多文件）

大量文章使用 `All rights reserved` 和 `This site is not affiliated with Jagex`：

- Footer 版权：`© 2026 OSRS Guru. All rights reserved.` — 15+ 文件
- **`osrs-birdhouse-runs-guide-2026.html:764`**: `All rights reserved. Old School RuneScape is a trademark of Jagex Limited. This guide is for informational purposes only.`
- **`osrs-ironman-money-making-f2p-2026.html:382`**: `© 2026 OSRSGuideHub.com — Fan site, not affiliated with Jagex Ltd.` — 不仅英文且域名错误！

### 3.4 meta keywords 全英文（多处）

大量 meta keywords 全部使用英文关键词：

- `index.html:12`: `"OSRS guide 2026, OSRS money making, OSRS skill training, OSRS boss guide, OSRS quest guide, OSRS AI assistant"`
- `lucro.html:14`: `"OSRS money making 2026, OSRS best money making methods, OSRS gold farming guide, OSRS GP per hour"`
- `chefes.html:14`: `"OSRS boss guides 2026, OSRS bossing guide, Zulrah guide, Vorkath guide"`
- `habilidades.html:14`: `"OSRS skill training guides 2026, OSRS 1-99 guide, OSRS skill training"`
- `atualizacoes-semanais.html:14`: `"OSRS Atualizações Semanais, OSRS Guia, OSRS ChinêsGuia, OSRS meta, OSRS Mais recenteConteúdo"`

---

## 已通过的检查

- **P0 - 中文字符残留**: 通过 — 未在 214 个 HTML 文件中发现任何中文字符（`\u4e00-\u9fff`）
- **P0 - 中文标点**: 通过 — 未发现中文标点 `，。、：？！；（）《》【】`
- **中文词汇**: 通过 — 未发现 `如果你/我们/这个/什么/怎么/可以/应该` 等中文词
- **重复 canonical 标签**: 通过 — 未发现重复 canonical 标签
- **`../guides/` 路径错误**: 通过 — 未发现此路径问题
- **Script 路径**: 通过 — JS/CSS 引用路径正确（`../js/`, `../css/`）

---

## 修复优先级建议

1. **紧急**: 修复 `atualizacoes-mensais.html` 和 `atualizacoes-semanais.html` 中的"chinês/em chinês"声明
2. **紧急**: 修复 `lucro.html:50` 的破损 HTML 标签
3. **高优**: 将所有文章的 og:title、meta description 翻译成葡语
4. **高优**: 翻译所有文章的正文内容（主要工作量）
5. **高优**: 修复 hreflang="x-default" 指向
6. **中优**: 补充缺失的 hreflang 标签
7. **中优**: 翻译所有 Footer 免责声明和版权文本
8. **中优**: 修复 `Investimentoimentoment` 单词损坏
9. **低优**: 替换全角双横线 `——` 为 `—`
10. **低优**: 翻译 `Sponsor Recommendation` 广告标签
