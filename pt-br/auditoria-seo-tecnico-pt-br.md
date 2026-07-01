# Auditoria Técnica SEO — pt-br/ (OSRS Guru Brasil)

**Data**: 2026-07-01  
**Escopo**: 201 guides + 11 hub pages  
**Metodologia**: Amostragem aleatória de 30 guides + grep global em todos os arquivos

---

## RESUMO EXECUTIVO

| Severidade | Contagem | Impacto |
|------------|----------|---------|
| P0-Crítico | 4 problemas | Perda direta de tráfego/ranking |
| P1-Importante | 6 problemas | SEO prejudicado, UX ruim |
| P2-Menor | 4 problemas | Otimização futura |

---

## P0 — CRÍTICO (Correção Urgente)

### P0-1: Todas as 201 guides NÃO têm hreflang tags completas

**Arquivos afetados**: TODAS as 201 guides em `pt-br/guides/`  
**Problema**: Todas as guides têm apenas um único `<link rel="alternate" hreflang="pt-br">` apontando para `https://osrsguru.com/pt-br/guides/` (diretório, não o artigo específico). Faltam completamente os hreflang para `en`, `zh` e `x-default`.

Exemplo (`guides/combat-achievements-guide-2026.html`):
```html
<!-- ATUAL (Errado) -->
<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/guides/">

<!-- DEVERIA SER -->
<link rel="alternate" hreflang="en" href="https://osrsguru.com/guides/combat-achievements-guide-2026.html">
<link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/guides/combat-achievements-guide-2026.html">
<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/guides/combat-achievements-guide-2026.html">
<link rel="alternate" hreflang="x-default" href="https://osrsguru.com/guides/combat-achievements-guide-2026.html">
```

**Impacto**: Google não consegue relacionar versões de idioma, causando problemas de canonicalização e perda de tráfego internacional.

### P0-2: Hub pages com hreflang ERRADOS — en aponta para pt-br/

**Arquivos afetados**: 8 hub pages
- `chefes.html` — hreflang="en" → `pt-br/boss-guides.html` (deve ser `/boss-guides.html`)
- `habilidades.html` — hreflang="en" → `pt-br/skill-training.html`
- `iniciante.html` — hreflang="en" → `pt-br/beginner.html`
- `lucro.html` — hreflang="en" → `pt-br/money-making.html`
- `membros.html` — hreflang="en" → `pt-br/membership.html`
- `missoes.html` — hreflang="en" → `pt-br/quest-guides.html`
- `atualizacoes-mensais.html` — hreflang="pt-br" → `/pt-br/monthly-updates.html` (arquivo não existe, nome correto é `atualizacoes-mensais.html`)
- `atualizacoes-semanais.html` — hreflang="pt-br" → `/pt-br/weekly-updates.html` (mesmo problema)

Além disso, todos os 8 hubs têm `x-default` apontando para a versão pt-br em vez da versão en.

**Único hub correto**: `index.html` — tem os 4 hreflang (en, zh, pt-br, x-default) corretos.

### P0-3: comunidade.html NÃO tem hreflang tags

**Arquivo**: `comunidade.html`  
**Problema**: Faltam completamente os tags `<link rel="alternate" hreflang="...">`.  
**Solução**: Adicionar hreflang para en, zh, pt-br e x-default.

### P0-4: ~20 guides usam links de navegação com nomes em INGLÊS (404 no contexto pt-br/)

**Arquivos afetados** (amostra):
- `guides/osrs-barrows-tunnel-optimization-2026.html`
- `guides/osrs-dagannoth-kings-guide-2026.html`
- `guides/osrs-f2p-gear-progression-guide-2026.html`
- `guides/osrs-f2p-slayer-guide-2026.html`
- `guides/osrs-gear-upgrade-priority-order-2026.html`
- `guides/osrs-first-week-progression-guide-2026.html`
- `guides/osrs-new-player-guide-2026.html`
- `guides/osrs-money-making-zero-req-2026.html`
- `guides/osrs-common-beginner-mistakes-avoid-2026.html`
- E aproximadamente mais 10-15 guides com o mesmo padrão

**Problema**: Links como:
```html
<a href="../boss-guides.html">Bosses</a>
<a href="../money-making.html">Money</a>
<a href="../quest-guides.html">Quests</a>
<a href="../skill-training.html">Skills</a>
<a href="../monthly-updates.html">Updates</a>
```

Esses arquivos NÃO existem no diretório `pt-br/`. Os nomes corretos são:
- `chefes.html`, `lucro.html`, `missoes.html`, `habilidades.html`, `atualizacoes-mensais.html`

**Solução**: Substituir por:
```html
<a href="../chefes.html">Chefes</a>
<a href="../lucro.html">Lucro</a>
<a href="../missoes.html">Missões</a>
<a href="../habilidades.html">Habilidades</a>
<a href="../atualizacoes-mensais.html">Atualizações</a>
```

---

## P1 — IMPORTANTE (Corrigir em até 1 semana)

### P1-1: Canonical das hub pages usa nomes de arquivo em INGLÊS

**Arquivos afetados**: 9 hub pages
| Arquivo | Canonical atual | Deveria ser |
|---------|----------------|-------------|
| `chefes.html` | `/pt-br/boss-guides.html` | `/pt-br/chefes.html` |
| `habilidades.html` | `/pt-br/skill-training.html` | `/pt-br/habilidades.html` |
| `iniciante.html` | `/pt-br/beginner.html` | `/pt-br/iniciante.html` |
| `lucro.html` | `/pt-br/money-making.html` | `/pt-br/lucro.html` |
| `membros.html` | `/pt-br/membership.html` | `/pt-br/membros.html` |
| `missoes.html` | `/pt-br/quest-guides.html` | `/pt-br/missoes.html` |
| `atualizacoes-mensais.html` | `/pt-br/monthly-updates.html` | `/pt-br/atualizacoes-mensais.html` |
| `atualizacoes-semanais.html` | `/pt-br/weekly-updates.html` | `/pt-br/atualizacoes-semanais.html` |
| `topicos-populares.html` | `/pt-br/forum-hot-topics.html` | `/pt-br/topicos-populares.html` |

Embora o canonical atual funcione (se houver rewrite), usar o nome real do arquivo é a prática correta.

### P1-2: 7 hub pages NÃO têm tags Open Graph

**Arquivos SEM og:title, og:description, og:url**:
- `chefes.html`
- `habilidades.html`
- `iniciante.html`
- `lucro.html`
- `membros.html`
- `missoes.html`
- `comunidade.html`

**Impacto**: Sem OG tags, o compartilhamento em redes sociais (WhatsApp, Facebook, Twitter) mostra previews ruins ou inexistentes. O WhatsApp é o principal canal de compartilhamento no Brasil.

**Solução**: Adicionar pelo menos `og:title`, `og:description`, `og:url`, `og:type` para cada hub page.

### P1-3: Meta description com artefatos CJK "——" (em-dash chinês)

**Arquivos afetados** (amostra):
- `chefes.html`: `"...CompletoJadVorkathZulrahRaid——Equipamento"`
- `guides/combat-achievements-guide-2026.html`: `"...Ironman considerations. | ——"`
- `guides/blood-moon-rises-quest-guide-2026.html`: `"...Myreque—— Boss"`
- `guides/osrs-cheapest-membership-2026.html`: h2 com `"——"`
- `habilidades.html`: `"...Agilidade, Caça——Métodos mais eficientes..."`
- `topicos-populares.html`: MÚLTIPLOS "——" em descrições de cards

**Solução**: Substituir `——` (U+2014 U+2014, em-dash chinês) por `—` (U+2014 único, em-dash ocidental) ou por espaço normal.

### P1-4: Meta description com concatenação de palavras (P2 do audit anterior)

**Arquivos afetados** (amostra):
- `chefes.html`: `"CompletoJadVorkathZulrahRaid"` — palavras coladas
- `topicos-populares.html`: Vários casos como `"PureConta"`, `"Purede nívelRota"`, etc.
- `membros.html`: `"MembroExclusivoda12Habilidade"`, `"MembroeGrátisversãoConteúdo"`
- `iniciante.html`: `"IniciantedaMétodos de Lucro"`

Estes são resquícios do processo de tradução automática.

### P1-5: Meta description de guides em INGLÊS (não português)

**Arquivos afetados** — todas as guides do batch antigo (~30-40 guides):
- `guides/combat-achievements-guide-2026.html`: "Complete guide to OSRS Combat Achievements system 2026..."
- `guides/osrs-dragon-slayer-2-complete-guide-2026.html` (e muitas outras)

**Solução**: Traduzir meta descriptions para português brasileiro.

### P1-6: Links de navegação mostram "Chinese" em vez de "Chinês"

**Arquivos afetados** — todas as guides com nav antigo e algumas hub pages:
```html
<a href="../zh/index.html">Chinese</a>
```
Em um site pt-br, deveria ser `Chinês` (ou `中文` para o público-alvo).

---

## P2 — MENOR (Melhorias recomendadas)

### P2-1: Alguns `<img>` têm `width="500"` sem `height`

**Arquivos afetados** (amostra):
- `guides/osrs-1-99-mining-guide-beginner-2026.html`
- `guides/osrs-achievement-diary-beginner-guide-2026.html`
- `guides/osrs-best-quests-per-skill-2026.html`
- ~30+ guides com imagens `width="500"` sem `height` correspondente

**Impacto**: Sem `height`, causa Cumulative Layout Shift (CLS), prejudicando Core Web Vitals.

**Solução**: Adicionar `height="300"` ou proporção correspondente. Exemplo:
```html
<!-- Antes -->
<img src="..." loading="lazy" width="500">
<!-- Depois -->
<img src="..." loading="lazy" width="500" height="300">
```

### P2-2: comunidade.html é uma página muito básica

**Arquivo**: `comunidade.html`  
**Problemas**:
- Sem hreflang tags
- Sem OG tags
- Sem meta keywords
- HTML inteiro em uma linha
- Conteúdo mínimo (apenas 2 parágrafos)

**Solução**: Expandir o conteúdo ou redirecionar para a página principal.

### P2-3: CSS path inconsistente entre hub pages

Alguns hubs usam `<link rel="stylesheet" href="../css/style.css">` e guides usam `<link rel="stylesheet" href="../../css/style.css">`. Isso está correto para a hierarquia de diretórios, mas seria mais robusto usar caminho absoluto: `/css/style.css`.

### P2-4: AdSense count varia entre páginas

Alguns arquivos têm 1 ocorrência de `ca-pub-8532760886171435` enquanto outros têm 4. Em guias, o AdSense aparece tanto no `<head>` (script) quanto no `<body>` (ins tags). Nas hub pages mais simples, pode haver menos blocos de anúncio. Isso não é um erro, mas vale monitorar para garantir monetização consistente.

---

## ✅ ITENS QUE PASSARAM NA AUDITORIA

| Item | Status |
|------|--------|
| Todas as páginas têm meta description | ✅ Passou |
| Todas as páginas têm canonical tag | ✅ Passou |
| Não há tags canonical duplicadas | ✅ Passou |
| GA4 (G-S1BGC91MYV) presente em todas as páginas | ✅ Passou |
| AdSense (ca-pub-8532760886171435) presente em todas as páginas | ✅ Passou |
| index.html tem hreflang completo (en/zh/pt-br/x-default) | ✅ Passou |
| Imagens têm `loading="lazy"` (quando presente) | ✅ Passou |
| Não há `<img>` sem `alt` | ✅ Passou |
| CSS usa caminhos relativos corretos (../../ ou ../) | ✅ Passou |
| `<html lang="pt-br">` presente em todas as páginas | ✅ Passou |
| `<meta charset="UTF-8">` presente em todas as páginas | ✅ Passou |
| `<meta name="viewport">` presente em todas as páginas | ✅ Passou |
| Structured data (JSON-LD) presente nas guides | ✅ Passou |
| robots meta tag presente nas páginas principais | ✅ Passou |

---

## PLANO DE AÇÃO RECOMENDADO

### Sprint 1 (P0 — Urgente, 1-2 dias)
1. **Script batch para hreflang das guides**: Gerar hreflang tags completos (en/zh/pt-br/x-default) para todas as 201 guides
2. **Corrigir hreflang das 8 hub pages**: Consertar en apontando para pt-br/
3. **Adicionar hreflang em comunidade.html**
4. **Corrigir links de navegação em inglês** nas ~20 guides afetadas

### Sprint 2 (P1 — Importante, 2-3 dias)
5. **Adicionar OG tags** nas 7 hub pages faltantes
6. **Corrigir canonical para nomes pt-br** nas 9 hub pages
7. **Remover artefatos "——"** e concatenção de palavras
8. **Traduzir meta descriptions** para português

### Sprint 3 (P2 — Melhoria, 1-2 dias)
9. Adicionar `height` nos `<img>` faltantes
10. Melhorar comunidade.html ou redirecionar
11. Padronizar caminhos CSS

---

*Relatório gerado por auditoria automatizada. Amostragem: 30/201 guides + 11/11 hub pages.*
