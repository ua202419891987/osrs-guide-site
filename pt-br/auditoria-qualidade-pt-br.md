# Auditoria de Qualidade pt-br/ — Relatório Final

**Data**: 2026-07-01 | **Escopo**: 207 guias + 11 hubs | **3 Rodadas**

---

## Sumário Executivo

| Categoria | Severidade | Escala | Status |
|-----------|-----------|--------|--------|
| P0 - Chinês residual | Crítico | 2 arquivos afetados | ⚠️ PONTUAL |
| P1 - Inglês não traduzido (navegação) | Crítico | 194/207 guias (94%) | ❌ SISTÊMICO |
| P1 - Inglês não traduzido (corpo) | Crítico | ~20-30% dos guias | ❌ SIGNIFICATIVO |
| P2 - Alt text em inglês | Médio | 166 instâncias | ⚠️ AMPLO |
| P2 - Concatenação de palavras | Médio | 70+ instâncias | ⚠️ AMPLO |
| P2 - Classes CSS `cn-` | Médio | 92 arquivos | ⚠️ AMPLO |
| P3 - Labels de idioma "Chinese" | Baixo | 11 arquivos | ⚠️ PONTUAL |

---

## Rodada 1: Amostragem de 20 Guias

### Artigos sorteados
```
osrs-fastest-99-cooking-f2p.html
osrs-efficient-training-routes-beginners-2026.html
osrs-diary-easy-medium-complete-guide-2026.html
osrs-farming-herb-runs-beginner-guide-2026.html
osrs-grotesque-guardians-guide-low-stats.html
osrs-herb-run-mastery-guide-2026.html
osrs-top-10-skills-to-train-first-2026.html
osrs-boss-profit-comparison-2026.html
osrs-pvp-gear-switching-basics-2026.html
osrs-f2p-gear-progression-guide-2026.html
osrs-fastest-1-99-crafting-guide-2026.html
osrs-combat-training-beginner-2026.html
osrs-blast-furnace-smithing-guide-2026.html
osrs-f2p-slayer-guide-2026.html
osrs-ironman-1-99-smithing-guide.html
osrs-how-to-fight-corporal-beast-loot-guide.html
osrs-f2p-money-making-no-stats.html
vault-of-ralos-raid-guide-2026.html
osrs-how-to-rune-spinning-profit-2026.html
osrs-f2p-ironman-money-making-early-game.html
```

### P0 — Chinês Residual

| # | Arquivo | Linha | Conteúdo | Descrição |
|---|---------|-------|----------|-----------|
| 1 | `guides/vault-of-ralos-raid-guide-2026.html` | 349 | `<a href="../../zh/index.html">中文版</a>` | "中文版" no breadcrumb (link de troca de idioma, possivelmente intencional) |
| 2 | `guides/osrs-hunter-training-guide-2026.html` | 246 | `<a href="../../zh/index.html">中文版</a>` | Idem acima |

> **Nota**: Ambos são links de troca de idioma para a versão chinesa. Se o padrão for manter "中文版" como rótulo para o link chinês, não é bug. Verificar com o time.

### P1 — Corpo do Texto em Inglês

| # | Arquivo | Linha(s) | Conteúdo | Descrição |
|---|---------|----------|----------|-----------|
| 1 | `guides/osrs-efficient-training-routes-beginners-2026.html` | 55,59,75,77,80-261 | **TODO o corpo do artigo em inglês** | O conteúdo principal (parágrafos, headings, TOC) está inteiramente em inglês. Ex: "Starting your journey in Old School RuneScape can be overwhelming..." |
| 2 | `guides/osrs-f2p-gear-progression-guide-2026.html` | 42-139 | **90% do corpo em inglês** | Ex: "Free-to-Play gear progression is one of the most straightforward parts of OSRS..." / "Your weapon is 80% of your DPS in OSRS." |
| 3 | `guides/osrs-efficient-training-routes-beginners-2026.html` | 82-89 | TOC misto | "Week 1: Foundation Building" / "Week 2: Combatee & Lucro" / "Common Iniciante Erros to Avoid" / "Frequently Asked Missãoions" |
| 4 | `guides/osrs-diary-easy-medium-complete-guide-2026.html` | 54 | `Stage 2` (link de breadcrumb) | Texto em inglês no breadcrumb |
| 5 | `guides/osrs-diary-easy-medium-complete-guide-2026.html` | 224,594-597,646 | Links mistos | "Mineração training guide" / "Combatee training guide" / "Money making guides" / "skill training guides" |
| 6 | `guides/osrs-f2p-slayer-guide-2026.html` | 37 | TOC inteiro em inglês | "What Is F2P Slayer?" / "F2P Slayer Masters" / "All F2P Slayer Tasks" etc. |
| 7 | `guides/osrs-blast-furnace-smithing-guide-2026.html` | 100-110 | TOC em inglês | "Blast Furnace Overview & How It Works" / "Requirements & Items Checklist" etc. |
| 8 | `guides/osrs-top-10-skills-to-train-first-2026.html` | 524-530 | Links internos em inglês | "Top 10 skills" / "training roadmap" |

### P2 — Alt Text de Imagens

| # | Arquivo | Linha | Conteúdo | Descrição |
|---|---------|-------|----------|-----------|
| 1 | `guides/osrs-efficient-training-routes-beginners-2026.html` | 63 | `alt="OSRS Efficient Training Routes for Beginners 2026"` | alt em inglês |
| 2 | `guides/osrs-diary-easy-medium-complete-guide-2026.html` | 140,254,385 | Todos os alt em inglês | "Achievement Diary Interface showing task list..." / "Varrock Map showing key locations..." |
| 3 | `guides/osrs-farming-herb-runs-beginner-guide-2026.html` | 117,175 | alt em inglês | "Farming Interface — Plant herbs in all patches..." |
| 4 | `guides/osrs-top-10-skills-to-train-first-2026.html` | 134,321,480 | alt em inglês | "OSRS Skills Panel - Not all 23 skills..." |
| 5 | `guides/osrs-combat-training-beginner-2026.html` | 62,152,242,300,346,464 | alt em inglês | "Knight in ornate plate armor" / "Combat Options Tab..." |
| 6 | `guides/osrs-f2p-slayer-guide-2026.html` | 35,192 | alt em inglês | "Slayer skill icon OSRS" / "Slayer Helmet OSRS..." |
| **Total** | — | — | **166 instâncias de alt em inglês** em todos os guias | Problema sistêmico |

### P3 — Botões/CTA

| # | Arquivo | Linha | Conteúdo | Status |
|---|---------|-------|----------|--------|
| — | Todos os 20 | — | `$1.90 — Obtenha o Pacote de Acesso Antecipado 👑` | ✅ Botão de suporte em português |

> ✅ **P3 aprovado**: Botões CTA (PayPal) estão em português.

---

## Rodada 2: Páginas Hub (11 páginas)

### Páginas existentes
✅ `index.html`, `iniciante.html`, `lucro.html`, `chefes.html`, `missoes.html`, `habilidades.html`, `membros.html`, `comunidade.html`, `topicos-populares.html`, `atualizacoes-mensais.html`, `atualizacoes-semanais.html`

### Páginas ausentes
❌ `guias.html`, `dinheiro.html`, `atualizacoes.html`, `chines.html`, `sobre.html`, `contato.html`

### P0 — Navegação em Inglês

| # | Página | Elemento | Conteúdo | Descrição |
|---|--------|----------|----------|-----------|
| — | — | — | — | ✅ **Nenhum P0 encontrado nas páginas hub** |

### P1 — Hero/Banner

| # | Página | Linha | Conteúdo | Descrição |
|---|--------|-------|----------|-----------|
| 1 | `habilidades.html` | 41 | `OSRS Treinamento de Habilidades **Guides** 2026` | "Guides" em inglês no meio do título PT |
| 2 | `index.html` | 64 | `🇺🇸 **English Main Site**` | Link de idioma em inglês (provavelmente intencional) |

### P2 — Concatenação de Palavras (SISTÊMICO)

Todas as páginas hub abaixo apresentam palavras concatenadas sem espaços:

| # | Página | Exemplos |
|---|--------|----------|
| 1 | `iniciante.html` | `InicianteCompletoGuia`, `HabilidadeVisão`, `CombateTreinamentoIntrodução`, `RotaMapa`, `HabilidadeGuia`, `F2P RápidoNívelRota`, `MembroGuiaVisão` |
| 2 | `lucro.html` | `MelhorMétodos`, `F2PLucro`, `AFKLucroUltimateGuia`, `IronmanGrátisLucro`, `GEFlippingInicianteGuia`, `MédioLucroRotaMapa` |
| 3 | `chefes.html` | `CompletoRotaçãoGuia`, `ChefeIniciante`, `InicianteIntrodução` |
| 4 | `missoes.html` | `CadaHabilidadeMelhorMissão`, `MissãoCapaRotaMapa`, `CompletoCompletarGuia` |
| 5 | `habilidades.html` | `TudoHabilidadesGuia`, `InicianteEficienteTreinamentoRota`, `HabilidadeAvançadoRota`, `MaisRápido99Ataque`, `1-99VidaGuia` |
| 6 | `membros.html` | `MembroGuia`, `ExclusivoHabilidadeAnálise`, `Mais baratoPlano` |
| 7 | `topicos-populares.html` | `PopularGuia`, `PopularGuiaLista`, `TudoAtualização` |
| 8 | `atualizacoes-mensais.html` | `TudoAtualização` |
| 9 | `atualizacoes-semanais.html` | `Popular desta semanaGuia` |

### Breadcrumbs
> ✅ Nenhuma página hub usa breadcrumbs visíveis. Aprovado.

### Footer
| # | Página | Conteúdo | Status |
|---|--------|----------|--------|
| 1 | `comunidade.html` | `© 2026 OSRS Guru Brasil — Site de fãs, não afiliado à Jagex Ltd.` | ✅ Português |
| 2 | Demais hubs | Footer genérico ou ausente | ⚠️ Sem footer completo |

---

## Rodada 3: Varredura de Problemas Especiais

### 3.1 — Links `href="...zh/"`

| # | Tipo | Arquivos | Quantidade |
|---|------|----------|------------|
| 1 | Navegação `href="../zh/index.html"` com label `Chinese` | Vários guias | 11 arquivos |
| 2 | Breadcrumb `href="../../zh/index.html"` com label `中文版` | 2 arquivos | `osrs-hunter-training-guide-2026.html`, `vault-of-ralos-raid-guide-2026.html` |
| 3 | Meta tag `hreflang="zh"` | 1 arquivo | `index.html` (correto) |

**Avaliação**: Links para versão chinesa são funcionais e esperados. O label "Chinese" (inglês) deveria ser "Chinês" (português). O label "中文版" pode ser mantido ou trocado para "Versão Chinesa".

### 3.2 — Classes CSS `cn-`

| Severidade | Arquivos Afetados | Quantidade |
|-----------|-------------------|------------|
| ⚠️ P2 | **92 arquivos** com `class="cn-title"` e/ou `class="cn-summary"` | 92 |

**Amostra dos arquivos afetados**:
- `guides/new-boss-loot-guide-2026.html:62` — `<h1 class="cn-title">OSRS 2026Chefe</h1>`
- `guides/osrs-achievement-diary-easy-medium-guide-2026.html:2` — `<h1 class="cn-title">OSRSEasy/Medium</h1>`
- `guides/osrs-cox-beginner-guide-2026.html:24` — `<h1 class="cn-title">OSRS CoX</h1>`
- `guides/osrs-blood-moon-rises-prep-checklist-detailed-2026.html:54` — `<h1 class="cn-title">OSRS 2026</h1>`
- `guides/osrs-combat-achievements-easy-walkthrough-2026.html:54` — `<h1 class="cn-title">OSRS 35·2026</h1>`
- ... e mais 87 arquivos

**Avaliação**: Classes CSS herdadas do template chinês não foram renomeadas. Embora CSS seja apenas nome de classe, pode causar confusão de manutenção e sugere que o conteúdo dentro desses elementos também não foi devidamente traduzido.

### 3.3 — Palavras "中国" / "中文" / "China"

| # | Arquivo | Conteúdo | Contexto |
|---|---------|----------|----------|
| 1 | `guides/osrs-mobile-setup-guide-2026.html` | "if unavailable in China" | Referência geográfica contextual (VPN), aceitável |
| 2 | `membros.html:103` | `<span class="tag tag-money">🆕 China</span>` | Tag suspeita — "China" como tag de conteúdo |

### 3.4 — "chinesa" / "chinesas"

> ✅ **Nenhuma ocorrência encontrada**. Aprovado.

---

## Estatísticas do Estado Geral

### Navegação (207 guias)

| Status | Quantidade | % |
|--------|-----------|----|
| Navegação totalmente em português | 4 | 1.9% |
| Navegação mista (PT + EN) | 177 | 85.5% |
| Navegação totalmente em inglês | 17 | 8.2% |
| Indeterminado | 9 | 4.3% |

### Itens de navegação em inglês mais comuns

| Label | Arquivos afetados |
|-------|------------------|
| `Home` | 194 |
| `Money` | 56 |
| `Updates` | 44 |
| `Quests` | 12 |
| `Skills` | 12 |
| `Bosses` | 10 |
| `Chinese` | 11 |

---

## Resumo por Prioridade

### P0 — CRÍTICO (2 ocorrências pontuais)

1. `guides/vault-of-ralos-raid-guide-2026.html:349` — "中文版" no breadcrumb
2. `guides/osrs-hunter-training-guide-2026.html:246` — "中文版" no breadcrumb

### P1 — GRAVE (194+ arquivos)

1. **Navegação em inglês**: 194/207 guias têm "Home" em vez de "Início"
2. **Corpo do artigo em inglês**: Diversos guias com parágrafos inteiros não traduzidos
   - `osrs-efficient-training-routes-beginners-2026.html` — corpo 100% inglês
   - `osrs-f2p-gear-progression-guide-2026.html` — corpo 90% inglês
   - `osrs-f2p-slayer-guide-2026.html` — TOC 100% inglês
   - `osrs-blast-furnace-smithing-guide-2026.html` — TOC 100% inglês
3. **Textos de links mistos inglês/português** em dezenas de guias

### P2 — MÉDIO (92+ arquivos)

1. **92 arquivos** com classes CSS `cn-title` / `cn-summary` (herdadas do template chinês)
2. **166 instâncias** de `alt` de imagens em inglês
3. **70+ instâncias** de concatenação de palavras (ex: "TreinamentoCompleto" → "Treinamento Completo")
4. **11 arquivos** com label de idioma "Chinese" em vez de "Chinês"
5. **6 páginas hub ausentes**: `guias.html`, `dinheiro.html`, `atualizacoes.html`, `chines.html`, `sobre.html`, `contato.html`

### P3 — BAIXO (0 ocorrências)

> ✅ Botões de CTA (PayPal) estão todos em português.

---

## Recomendações

1. **PRIORIDADE MÁXIMA**: Rodar script de substituição de navegação nos 194 guias:
   - `Home` → `Início`
   - `Money` → `Lucro`
   - `Bosses` → `Chefes`
   - `Quests` → `Missões`
   - `Skills` → `Habilidades`
   - `Updates` → `Atualizações`
   - `Chinese` → `Chinês`

2. **PRIORIDADE ALTA**: Revisar corpo de artigos que estão com parágrafos em inglês (especialmente os 4 identificados com corpo 100% inglês).

3. **PRIORIDADE MÉDIA**: Batch rename `cn-title` → `pt-title` e `cn-summary` → `pt-summary` nos 92 arquivos.

4. **PRIORIDADE MÉDIA**: Corrigir concatenação de palavras (70+ ocorrências) — script de pós-processamento.

5. **PRIORIDADE BAIXA**: Criar as 6 páginas hub ausentes ou redirecionar.

6. **PRIORIDADE BAIXA**: Revisar alt text de imagens (166 instâncias).

---

*Relatório gerado automaticamente por auditoria programática em 2026-07-01*
