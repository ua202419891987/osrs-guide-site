#!/usr/bin/env python3
"""
Phase 5 (B Group): Copy 25 selected new articles from main site guides/
to pt-br/guides/, insert 30-Second Preview block (PT-BR first, then English).

25 articles selected by traffic potential (confirmed by user):
1. osrs-new-player-guide-2026
2. osrs-first-week-progression-guide-2026
3. osrs-f2p-gear-progression-guide-2026
4. osrs-common-beginner-mistakes-avoid-2026
5. osrs-money-making-zero-req-2026
6. osrs-bond-vs-subscription-2026
7. osrs-grand-exchange-flipping-guide-2026
8. osrs-birdhouse-runs-guide-2026
9. osrs-blast-furnace-smithing-guide-2026
10. osrs-zero-req-moneymaker-2026
11. osrs-diary-priority-order-beginner-2026
12. osrs-f2p-slayer-guide-2026
13. osrs-construction-1-99-guide-2026
14. osrs-clue-scrolls-beginner-guide-2026
15. osrs-achievement-diary-beginner-guide-2026
16. osrs-barrows-tunnel-optimization-2026
17. osrs-blood-moon-rises-guide-2026
18. osrs-dagannoth-kings-guide-2026
19. osrs-death-mechanics-guide-2026
20. osrs-gear-upgrade-priority-order-2026
(+ 5 extra from June 30 batch with internal links)
21. osrs-diary-easy-medium-complete-guide-2026
22. osrs-combat-achievements-easy-walkthrough-2026
23. osrs-blood-moon-rises-prep-checklist-detailed-2026
24. osrs-best-quests-per-skill-2026
25. osrs-1-99-prayer-guide-2026
"""

import re
import shutil
from pathlib import Path

MAIN = Path(r'C:\Users\Lenovo\osrs-guide-site\guides')
PTBR = Path(r'C:\Users\Lenovo\osrs-guide-site\pt-br\guides')

ARTICLES = [
    'osrs-new-player-guide-2026',
    'osrs-first-week-progression-guide-2026',
    'osrs-f2p-gear-progression-guide-2026',
    'osrs-common-beginner-mistakes-avoid-2026',
    'osrs-money-making-zero-req-2026',
    'osrs-bond-vs-subscription-2026',
    'osrs-grand-exchange-flipping-guide-2026',
    'osrs-birdhouse-runs-guide-2026',
    'osrs-blast-furnace-smithing-guide-2026',
    'osrs-zero-req-moneymaker-2026',
    'osrs-diary-priority-order-beginner-2026',
    'osrs-f2p-slayer-guide-2026',
    'osrs-construction-1-99-guide-2026',
    'osrs-clue-scrolls-beginner-guide-2026',
    'osrs-achievement-diary-beginner-guide-2026',
    'osrs-barrows-tunnel-optimization-2026',
    'osrs-blood-moon-rises-guide-2026',
    'osrs-dagannoth-kings-guide-2026',
    'osrs-death-mechanics-guide-2026',
    'osrs-gear-upgrade-priority-order-2026',
    'osrs-diary-easy-medium-complete-guide-2026',
    'osrs-combat-achievements-easy-walkthrough-2026',
    'osrs-blood-moon-rises-prep-checklist-detailed-2026',
    'osrs-best-quests-per-skill-2026',
    'osrs-1-99-prayer-guide-2026',
]

# 30S preview generator: extract h1 title and generate PT + EN preview
def generate_preview(html_content, fname):
    # Extract H1 title
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if h1_match:
        h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
    else:
        h1 = fname.replace('osrs-', '').replace('-guide-2026', '').replace('-', ' ').title()
    
    # Generate PT-BR preview (generic description based on article type)
    preview_pt = generate_pt_preview(h1, fname)
    preview_en = generate_en_preview(h1, fname)
    
    return preview_pt, preview_en


def generate_pt_preview(h1, fname):
    """Generate Brazilian Portuguese 30S preview based on article topic."""
    h1_lower = h1.lower()
    fname_lower = fname.lower()
    
    if 'money' in fname_lower or 'lucro' in h1_lower or 'gp' in fname_lower:
        return f"O guia definitivo sobre métodos de lucro em OSRS 2026, cobrindo estratégias do zero ao endgame com análises precisas de custo-benefício."
    elif 'beginner' in fname_lower or 'iniciante' in h1_lower or 'new player' in fname_lower:
        return f"Guia essencial para novos jogadores de OSRS em 2026, cobrindo os primeiros passos, progresão eficiente e erros comuns a evitar."
    elif 'boss' in fname_lower or 'chefe' in h1_lower or 'barrows' in fname_lower or 'dagannoth' in fname_lower:
        return f"Estratégias completas de combate para {h1} em OSRS, incluindo cargas, equipamentos recomendados e táticas de posicionamento."
    elif 'skill' in fname_lower or 'habilidade' in h1_lower or 'training' in fname_lower or '1-99' in fname_lower:
        return f"Guia de treinamento completo para {h1} em OSRS 2026, com métodos econômicos e rotas ótimas do nível 1 ao 99."
    elif 'quest' in fname_lower or 'missão' in h1_lower:
        return f"Guia completo de missões em OSRS, priorizando recompensas úteis e ordem eficiente de conclusão para novos jogadores."
    elif 'prayer' in fname_lower or 'oração' in h1_lower:
        return f"Guia completo de Oração (Prayer) em OSRS 2026, cobrindo métodos do nível 1 ao 99, ossos e altares eficientes."
    elif 'diary' in fname_lower or 'diário' in h1_lower:
        return f"Guia de prioridade para Diários de Conquistas em OSRS, com estratégias para completar tarefas simples, médias e difíceis na ordem mais eficiente."
    elif 'combat' in fname_lower or 'combate' in h1_lower:
        return f"Guia de mecânicas e conquistas de combate em OSRS, ajudando você a completar desafios de combate de forma eficiente e estratégica."
    elif 'blood moon' in fname_lower or 'lua sangrenta' in h1_lower:
        return f"Guia completo sobre o evento Ascensão da Lua Sangrenta em OSRS, incluindo preparação, mecânicas de combate e recompensas detalhadas."
    elif 'ge' in fname_lower or 'exchange' in fname_lower or 'flipping' in fname_lower:
        return f"Estratégias avançadas de lucro na Grand Exchange de OSRS, incluindo flipping eficiente, análise de mercado e gerenciamento de inventário."
    elif 'f2p' in fname_lower:
        return f"Guia completo para jogadores gratuitos (F2P) de OSRS em 2026, maximizando o progresso sem necessidade de membro."
    elif 'bond' in fname_lower or 'membro' in fname_lower:
        return f"Análise completa sobre os métodos de pagamento de OSRS em 2026, incluindo Bond vs Assinatura, preços regionais e estratégias de economia."
    else:
        return f"Guia completo e atualizado de OSRS 2026 sobre {h1}, com estratégias testadas, análises detalhadas e dicas de especialistas."


def generate_en_preview(h1, fname):
    """Generate English 30S preview — shorter version."""
    h1_lower = h1.lower()
    fname_lower = fname.lower()
    
    if 'money' in fname_lower or 'lucro' in h1_lower:
        return f"The definitive OSRS 2026 money making guide, covering zero-req methods to endgame strategies with accurate GP/hour analyses."
    elif 'beginner' in fname_lower or 'new player' in fname_lower:
        return f"Essential guide for new OSRS players in 2026, covering first steps, efficient progression and common mistakes to avoid."
    elif 'boss' in fname_lower or 'barrows' in fname_lower or 'dagannoth' in fname_lower:
        return f"Complete OSRS boss strategy guide for {h1}, including gear setups, attack patterns and efficient kill methods."
    elif 'skill' in fname_lower or '1-99' in fname_lower or 'training' in fname_lower:
        return f"Complete {h1} training guide for OSRS 2026, with cost-effective methods and optimal routes from level 1 to 99."
    elif 'prayer' in fname_lower:
        return f"Complete Prayer training guide for OSRS 2026, covering level 1-99 methods, efficient bones and altar routes."
    elif 'diary' in fname_lower:
        return f"OSRS Achievement Diary priority guide with efficient strategies to complete simple, medium and hard tasks in optimal order."
    elif 'blood moon' in fname_lower:
        return f"Complete guide to the Blood Moon Rises event in OSRS, including preparation, boss mechanics and detailed reward analysis."
    elif 'combat' in fname_lower:
        return f"OSRS combat achievements guide with efficient strategies to complete easy through elite combat challenges."
    elif 'f2p' in fname_lower:
        return f"Complete F2P guide for OSRS 2026, maximizing progress without membership requirements."
    elif 'bond' in fname_lower or 'subscription' in fname_lower:
        return f"Complete guide to OSRS membership options in 2026, comparing Bond vs Subscription with regional pricing analysis."
    else:
        return f"Complete and updated OSRS 2026 guide on {h1}, with tested strategies, detailed analyses and expert tips."


def insert_preview_block(html_content, preview_pt, preview_en):
    """Insert 30S preview block after the <h1> tag."""
    preview_html = f'''    
    <!-- 30S Preview Block -->
    <div class="preview-block" style="background:linear-gradient(135deg,#2a1a0a 0%,#3b2615 40%,#4a3320 100%);border-radius:10px;padding:20px;margin:20px 0;color:#e8d5b7;">
      <h3 style="color:#d4af37;margin:0 0 10px;">⚡ 30-Second Preview / Pré-visualização de 30 Segundos</h3>
      <p style="margin:0 0 8px;line-height:1.6;"><strong>🇧🇷 Português:</strong> {preview_pt}</p>
      <p style="margin:0;line-height:1.6;"><strong>🇬🇧 English:</strong> {preview_en}</p>
    </div>
    
'''
    
    # Insert after </h1> tag
    insert_pos = html_content.find('</h1>')
    if insert_pos == -1:
        return html_content
    
    insert_pos += len('</h1>')
    return html_content[:insert_pos] + preview_html + html_content[insert_pos:]


def fix_article_metadata(html_content, fname):
    """Fix metadata for pt-br articles: lang, canonical, nav links."""
    # Fix lang
    html_content = re.sub(r'lang="zh-Hans"', 'lang="pt-br"', html_content)
    html_content = re.sub(r'lang="en"', 'lang="pt-br"', html_content)
    
    # Fix canonical to pt-br
    html_content = re.sub(
        r'canonical" href="https://osrsguru\.com/[^"]*?"',
        f'canonical" href="https://osrsguru.com/pt-br/guides/{fname}.html"',
        html_content
    )
    
    # Fix nav links to pt-br
    html_content = html_content.replace('href="guides/', 'href="../guides/')
    html_content = html_content.replace('href="index.html"', 'href="../index.html"')
    html_content = html_content.replace('href="boss-guides.html"', 'href="../chefes.html"')
    html_content = html_content.replace('href="quest-guides.html"', 'href="../missoes.html"')
    html_content = html_content.replace('href="skill-guides.html"', 'href="../habilidades.html"')
    html_content = html_content.replace('href="money-guides.html"', 'href="../lucro.html"')
    
    return html_content


if __name__ == '__main__':
    print('=== Phase 5 (B Group): Copying 25 new articles to pt-br/guides/ ===\n')
    copied = 0
    skipped = 0
    for base in ARTICLES:
        fname = f'{base}.html'
        src = MAIN / fname
        dst = PTBR / fname
        
        if not src.exists():
            print(f'  [MISSING] {fname} not found in main guides/')
            skipped += 1
            continue
        
        if dst.exists():
            print(f'  [SKIP] {fname} already in pt-br/')
            skipped += 1
            continue
        
        # Read source
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate preview
        preview_pt, preview_en = generate_preview(content, base)
        
        # Insert preview block
        content = insert_preview_block(content, preview_pt, preview_en)
        
        # Fix metadata
        content = fix_article_metadata(content, base)
        
        # Write to pt-br/guides/
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'  [OK] {fname} copied + preview added')
        copied += 1
    
    print(f'\nDone! Copied: {copied}, Skipped: {skipped}')
    print(f'Total pt-br articles: {len(list(PTBR.glob("*.html")))}')
