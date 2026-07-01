import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re
from pathlib import Path

PT_DIR = Path('C:/Users/Lenovo/osrs-guide-site/pt-br')

# Exact phrase translations for article titles (longest first)
PHRASE_MAP = {
    # Exact article titles from main site
    'Beginner Complete Guide 2026': 'Guia Completo para Iniciantes 2026',
    'Beginner Fast Track 2026': 'Rota Rápida para Iniciantes 2026',
    'Mid-Game Guide 2026': 'Guia de Meio de Jogo 2026',
    'Mid-Game Optimization 2026': 'Otimização de Meio de Jogo 2026',
    'Endgame Guide 2026': 'Guia de Endgame 2026',
    'Max Account Ultimate 2026': 'Conta Máxima Ultimate 2026',
    'Hunter Training Guide 2026 (P1 Upgraded)': 'Guia de Treinamento de Caça 2026 (P1 Atualizado)',
    'Money Making Summer Sweep-Up 2026': 'Lucro Summer Sweep-Up 2026',
    'Under 1M Investment Money Making': 'Lucro com Investimento Abaixo de 1M',
    'Slayer Beginner First Master': 'Slayer Primeiro Mestre Iniciante',
    'Slayer Low-Level Money Makers': 'Métodos de Lucro com Slayer de Baixo Nível',
    'Combat Achievements Easy Walkthrough 2026': 'Passo a Passo Fácil de Conquistas de Combate 2026',
    'Ghommal Hilt Fast Guide': 'Guia Rápido de Ghommal Hilt',
    'First Boss Progression Roadmap': 'Roteiro de Progressão de Primeiro Chefe',
    'Obor & Bryophyta F2P Boss Guide': 'Guia de Chefes F2P Obor & Bryophyta',
    'Returning Player Catch-Up 2026': 'Recuperação para Jogador Retornando 2026',
    'Returning Player Fast Track 2026': 'Rota Rápida para Jogador Retornando 2026',
    'Diary Priority Order Beginner': 'Ordem de Prioridade de Diários para Iniciantes',
    'Diary Easy & Medium Complete': 'Diários Fácil e Médio Completo',
    'Skill Training After Sweep-Up': 'Treinamento de Habilidades Após Sweep-Up',
    'Top 10 Skills to Train First': 'Top 10 Habilidades para Treinar Primeiro',
    'Blood Moon Rises Prep Checklist Detailed 2026': 'Checklist de Preparação Blood Moon Rises 2026',
    'Best Quests Per Skill 2026': 'Melhores Missões por Habilidade 2026',
    'New Player Guide 2026': 'Guia para Novos Jogadores 2026',
    'All Skills Overview Guide': 'Guia Geral de Todas as Habilidades',
    'Combat Training Guide 1–70+': 'Guia de Treinamento de Combate 1–70+',
    'Gear Guide for Beginners': 'Guia de Equipamento para Iniciantes',
    'Safe Spots Guide': 'Guia de Safe Spots',
    'Budget Gear by Combat Level': 'Equipamento Econômico por Nível de Combate',
    'Beginner Money Making (F2P→Member)': 'Lucro para Iniciantes (F2P→Membro)',
    'Grand Exchange Complete Guide': 'Guia Completo da Grand Exchange',
    'Low-Level Skilling Money Makers': 'Métodos de Lucro com Habilidades de Baixo Nível',
    'F2P Money Making — GP/hr Ranking': 'Lucro F2P — Ranking GP/hora',
    'F2P to P2P Membership Guide': 'Guia de F2P para P2P Membro',
    'Prayer Training Guide': 'Guia de Treinamento de Oração',
    'Questing for Beginners': 'Missões para Iniciantes',
    'F2P Leveling — Max Efficiently': 'Nivelamento F2P — Máxima Eficiência',
    'Clan & Social Guide': 'Guia de Clã e Social',
    'Player Owned House (POH) Guide': 'Guia de Casa do Jogador (POH)',
    'Minigames Beginner Guide': 'Guia de Minigames para Iniciantes',
    'F2P Slayer — Complete Guide': 'Slayer F2P — Guia Completo',
    'Barrows Brothers Beginner Guide': 'Guia de Barrows para Iniciantes',
    'Nightmare Zone (NMZ) Guide': 'Guia da Nightmare Zone (NMZ)',
    'PvM Beginner Guide': 'Guia de PvM para Iniciantes',
    'Sub-70 Combat Bossing Guide': 'Guia de Chefes com Combate Abaixo de 70',
    'Barrows Tunnel Optimization': 'Otimização de Túneis de Barrows',
    'Daily/Weekly Reset Activities': 'Atividades Diárias/Semanais de Reset',
    '20 Common Beginner Mistakes': '20 Erros Comuns de Iniciantes',
    'Achievement Diaries Guide': 'Guia de Diários de Conquistas',
    'Viggora — Complete Lore & Quest': 'Viggora — Lore e Missão Completo',
    'OSRS Mobile Guide': 'Guia de OSRS Mobile',
    'Returning Player Catch-Up Guide': 'Guia de Recuperação para Jogador Retornando',
    'Ironman Beginner Guide': 'Guia de Ironman para Iniciantes',
    'Slayer Beginner Guide': 'Guia de Slayer para Iniciantes',
    '7-Day Beginner Roadmap': 'Roteiro de 7 Dias para Iniciantes',
    'First Boss Progression': 'Progressão de Primeiro Chefe',
    'Quest Cape Roadmap': 'Roteiro da Capa de Missões',
    'Mid-Game Money Roadmap': 'Roteiro de Lucro de Meio de Jogo',
    'Mid-to-High Progression': 'Progressão de Médio para Alto',
    
    # General phrases
    'Skill Training': 'Treinamento de Habilidades',
    'Money Making': 'Lucro',
    'Boss Guide': 'Guia de Chefe',
    'Boss Guides': 'Guias de Chefe',
    'Quest Guide': 'Guia de Missão',
    'Quest Guides': 'Guias de Missão',
    'Diary Guide': 'Guia de Diário',
    'Gear Guide': 'Guia de Equipamento',
    'Training Guide': 'Guia de Treinamento',
    'F2P Guide': 'Guia F2P',
    'Ironman Guide': 'Guia Ironman',
    'P2P Guide': 'Guia P2P',
    'Beginner Guide': 'Guia para Iniciantes',
    'Beginner Guides': 'Guias para Iniciantes',
    'Complete Guide': 'Guia Completo',
    'Fast Track': 'Rota Rápida',
    'Mid-Game': 'Meio de Jogo',
    'Endgame': 'Endgame',
    'Max Account': 'Conta Máxima',
    'Returning Player': 'Jogador Retornando',
    'Catch-Up': 'Recuperação',
    'Walkthrough': 'Passo a Passo',
    'Roadmap': 'Roteiro',
    'Progression': 'Progressão',
    'Priority Order': 'Ordem de Prioridade',
    'Easy & Medium': 'Fácil e Médio',
    'After Sweep-Up': 'Após Sweep-Up',
    'Best Quests': 'Melhores Missões',
    'Per Skill': 'por Habilidade',
    'Low-Level': 'Baixo Nível',
    'Combat Achievements': 'Conquistas de Combate',
    'Easy Walkthrough': 'Passo a Passo Fácil',
    'Hilt Fast': 'Hilt Rápido',
    'Prep Checklist': 'Checklist de Preparação',
    'Money Makers': 'Métodos de Lucro',
    'Budget Gear': 'Equipamento Econômico',
    'Combat Training': 'Treinamento de Combate',
    'Player Owned House': 'Casa do Jogador',
    'Daily & Weekly': 'Diário & Semanal',
    'Daily/Weekly': 'Diário/Semanal',
    'Achievement Diaries': 'Diários de Conquistas',
    'Common Beginner Mistakes': 'Erros Comuns de Iniciantes',
    'Investment': 'Investimento',
    'Makers': 'Métodos',
    'to Train': 'para Treinar',
    'Best': 'Melhores',
    'New': 'Novos',
    'Diary': 'Diário',
    'Diaries': 'Diários',
    'Guide': 'Guia',
    'Guides': 'Guias',
    'Beginner': 'Iniciante',
    'Complete': 'Completo',
    'Ultimate': 'Ultimate',
    'Fast': 'Rápido',
    'Training': 'Treinamento',
    'Skills': 'Habilidades',
    'Skill': 'Habilidade',
    'Boss': 'Chefe',
    'Bosses': 'Chefes',
    'Quest': 'Missão',
    'Quests': 'Missões',
    'Gear': 'Equipamento',
    'Combat': 'Combate',
    'Ironman': 'Ironman',
    'F2P': 'F2P',
    'P2P': 'P2P',
    'Prayer': 'Oração',
    'Hunter': 'Caça',
    'Slayer': 'Slayer',
    'Runecrafting': 'Runecrafting',
    'Agility': 'Agilidade',
    'Herblore': 'Herblore',
    'Thieving': 'Furto',
    'Crafting': 'Artesanato',
    'Fletching': 'Fletching',
    'Mining': 'Mineração',
    'Smithing': 'Smithing',
    'Fishing': 'Pesca',
    'Cooking': 'Culinária',
    'Firemaking': 'Firemaking',
    'Woodcutting': 'Corte de Madeira',
    'Farming': 'Agricultura',
    'Construction': 'Construção',
    'New Player': 'Novo Jogador',
    'Catch-Up': 'Recuperação',
    'Mobile': 'Mobile',
    'Minigames': 'Minigames',
    'Social': 'Social',
    'Clan': 'Clã',
    'Nightmare Zone': 'Nightmare Zone',
    'Barrows': 'Barrows',
    'Zulrah': 'Zulrah',
    'Vorkath': 'Vorkath',
    'Viggora': 'Viggora',
    'Obor': 'Obor',
    'Bryophyta': 'Bryophyta',
    'Ghommal': 'Ghommal',
    'Hilt': 'Hilt',
    'Membership': 'Membros',
    'Bond': 'Bond',
    'Subscription': 'Assinatura',
    'Flipping': 'Flipping',
    'Grand Exchange': 'Grand Exchange',
    'Daily': 'Diário',
    'Weekly': 'Semanal',
    'AFK': 'AFK',
    'Passive': 'Passivo',
    'Wilderness': 'Deserto',
    'Profit': 'Lucro',
    'GP': 'GP',
    'Per Hour': 'por Hora',
    'Per Skill': 'por Habilidade',
    'Checklist': 'Checklist',
    'Mistakes': 'Erros',
    'Tips': 'Dicas',
    'Strategies': 'Estratégias',
    'Sailing': 'Sailing',
    'Wyrmscraig': 'Wyrmscraig',
    'Blood Moon': 'Blood Moon',
    'Summer Sweep': 'Summer Sweep',
    'Top': 'Top',
    'First': 'Primeiro',
    'Master': 'Mestre',
    'Low': 'Baixo',
    'Level': 'Nível',
    'Invest': 'Investimento',
}


def translate_title(title):
    """Translate a title string to Brazilian Portuguese using exact phrase map."""
    if not title:
        return title
    
    # Fixups for already-broken mixed titles from previous runs
    fixups = {
        'Under 1M Investimentoment Lucro': 'Lucro com Investimento Abaixo de 1M',
        'Slayer Baixo Nível Lucro Makers': 'Métodos de Lucro com Slayer de Baixo Nível',
        'Top 10 Habilidades to Train Primeiro': 'Top 10 Habilidades para Treinar Primeiro',
        'Best Missões por Habilidade 2026': 'Melhores Missões por Habilidade 2026',
        'Diário Fácil e Médio Completo': 'Diários Fácil e Médio Completo',
        'Slayer, Boss & Lucro — 8 New Guias': 'Slayer, Chefes & Lucro — 8 Novos Guias',
        'Treinamento de Habilidades 2026 — 6 New Guias Detalhados': 'Treinamento de Habilidades 2026 — 6 Novos Guias Detalhados',
        'Jogador Retornando, Diário & Missões — 8 New Guias': 'Jogador Retornando, Diário & Missões — 8 Novos Guias',
        'Ghommal Hilt Rápido Guia': 'Guia Rápido de Ghommal Hilt',
        'Primeiro Chefe Progressão Roteiro': 'Roteiro de Progressão de Primeiro Chefe',
        'Obor & Bryophyta F2P Guia de Chefe': 'Guia de Chefes F2P Obor & Bryophyta',
        'Jogador Retornando Recuperação 2026': 'Recuperação para Jogador Retornando 2026',
        'Jogador Retornando Rota Rápida 2026': 'Rota Rápida para Jogador Retornando 2026',
        'Prioridade de Diários Order Iniciante': 'Ordem de Prioridade de Diários para Iniciantes',
        '8 New Guias': '8 Novos Guias',
        '6 New Guias Detalhados': '6 Novos Guias Detalhados',
        'New Guias': 'Novos Guias',
        'CA Passo a Passo Fácil 2026': 'Passo a Passo Fácil de Conquistas de Combate 2026',
        'Slayer Iniciante Primeiro Mestre': 'Slayer Primeiro Mestre Iniciante',
    }
    for broken, fixed in fixups.items():
        title = title.replace(broken, fixed)
    
    # Apply phrase translations - longest first
    for eng, pt in sorted(PHRASE_MAP.items(), key=lambda x: -len(x[0])):
        title = title.replace(eng, pt)
    
    return title


def fix_page(path):
    """Fix titles in a page."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Translate link text (only if it has English words)
    def translate_link_text(match):
        prefix = match.group(1)
        text = match.group(2)
        suffix = match.group(3)
        if text.strip() and re.search(r'[a-zA-Z]{3,}', text):
            translated = translate_title(text)
            return f'{prefix}{translated}{suffix}'
        return match.group(0)
    
    content = re.sub(r'(<a[^>]*>)([^<]+)(</a>)', translate_link_text, content)
    
    # Translate title tags
    def translate_title_tag(match):
        title = match.group(1)
        return f'<title>{translate_title(title)}</title>'
    
    content = re.sub(r'<title>(.*?)</title>', translate_title_tag, content, flags=re.DOTALL)
    
    # Translate h1 tags
    def translate_h1(match):
        text = match.group(1)
        if re.search(r'[a-zA-Z]{3,}', text):
            translated = translate_title(text)
            return f'<h1{match.group(2)}>{translated}</h1>'
        return match.group(0)
    
    content = re.sub(r'<h1([^>]*)>(.*?)</h1>', translate_h1, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    for page in PT_DIR.glob('*.html'):
        fix_page(page)
        print(f'Fixed: {page.name}')
    
    count = 0
    for guide in (PT_DIR / 'guides').glob('*.html'):
        fix_page(guide)
        count += 1
    
    print(f'\nFixed {count} guide articles')
