#!/usr/bin/env python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
OSRS Guru — Brazilian Portuguese Site Builder
1:1 copies and transforms the main English site into pt-br
"""

import re
import os
import shutil
from pathlib import Path

BASE = Path("C:/Users/Lenovo/osrs-guide-site")
SRC = BASE / "index.html"
DST = BASE / "pt-br"

# ============================================================
# TRANSLATION MAP: English/Chinese interface text → Brazilian Portuguese
# ============================================================
REPLACE = {
    # Language & SEO
    '<html lang="en">': '<html lang="pt-br">',
    '<title>OSRS Guru — Old School RuneScape Strategy Guides 2026</title>': 
        '<title>OSRS Guru Brasil — Guias de Old School RuneScape 2026</title>',
    '<link rel="alternate" hreflang="en" href="https://osrsguru.com/">\n  <link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/">':
        '<link rel="alternate" hreflang="en" href="https://osrsguru.com/">\n  <link rel="alternate" hreflang="zh" href="https://osrsguru.com/zh/">\n  <link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/">',
    'href="zh/index.html" class="nav-cta" style="color:#d4af37;">🇨🇳 Chinese Station':
        'href="../index.html" class="nav-cta" style="color:#d4af37;">🇺🇸 English Main Site',
    
    # Header
    '310+ OSRS Guides · Free': '310+ Guias OSRS · Grátis',
    '🗺️ Roadmaps': '🗺️ Roteiros',
    '5 NEW': '5 NOVOS',
    '🔥 Membership Guide': '🔥 Guia de Membros',
    'NEW</span></a>': 'NOVO</span></a>',
    '🔥 Hot Picks': '🔥 Destaques',
    '📅 Monthly Updates': '📅 Atualizações Mensais',
    '🔥 This Week\'s Hot': '🔥 Quente da Semana',
    '🆕 New Players': '🆕 Novatos',
    'Money Making': 'Lucro',
    'Skills': 'Habilidades',
    'Quests': 'Missões',
    'Bosses': 'Chefes',
    'AI Q&A': 'AI Perguntas',

    # NEW GAMES BAR - remove Crimson Desert & Windrose
    # We'll handle this separately

    # Search Box
    '🔍 Find Your Perfect OSRS Guide': '🔍 Encontre o Guia Perfeito de OSRS',
    'Search 180+ guides, or ask AI any OSRS question': 'Pesquise em 180+ guias, ou pergunte à AI qualquer duvida de OSRS',
    'e.g., Zulrah, Prayer, Money Making... (ask AI': 'Ex: Zulrah, Oração, Lucro... (pergunte a AI',
    'Search with AI': 'Pesquisar com AI',
    'Tip: Type any question above & press Enter, or click': 'Dica: Digite qualquer pergunta acima e pressione Enter, ou clique em',
    'Ask AI': 'Perguntar AI',
    '— OSRS Guru AI answers instantly!': '— a AI do OSRS Guru responde na hora!',
    '🔥 Popular:': '🔥 Popular:',
    'Money': 'Lucro',
    'Prayer': 'Oração',
    'New Player': 'Novato',
    'Close': 'Fechar',
    "Can't find what you're looking for?": 'Não encontrou o que procura?',
    'Search with AI': 'Pesquisar com AI',
    "AI assistant not loaded": 'Assistente AI não carregado',

    # Task Cards
    '💰 Money Making Hub — 29 Proven Methods': '💰 Central de Lucro — 29 Métodos Comprovados',
    'From 0 GP to 10M+. F2P, member, and ironman methods tested in 2026.': 'De 0 GP a 10M+. Métodos F2P, membros e ironman testados em 2026.',
    'See All 29 Methods →': 'Ver Todos os 29 Métodos →',
    '📊 Skill Training Hub — All 23 Skills Covered': '📊 Central de Habilidades — Todas as 23 Cobertas',
    'Fastest, cheapest, and AFK routes for all 23 skills. Save 200+ hours.': 'Rotas mais rápidas, baratas e AFK para todas as 23 habilidades. Economize 200+ horas.',
    'Explore 23 Skill Guides →': 'Explorar 23 Guias de Habilidades →',
    '⚔️ Boss Hub — From Barrows to Raids': '⚔️ Central de Chefes — De Barrows a Raids',
    'From Barrows to raids. Gear setups, rotations, and GP per hour.': 'De Barrows a raids. Configurações de equipamentos, rotações e GP por hora.',
    'See All Boss Guides →': 'Ver Todos os Guias de Chefes →',
    '🌐 Join the Community': '🌐 Junte-se à Comunidade',
    'Ask questions, share strategies, and connect with other OSRS players. Your private community hub.': 'Pergunte, compartilhe estratégias e conecte-se com outros jogadores de OSRS. Seu hub comunitário.',
    'Start Discussing →': 'Comece a Discutir →',

    # 30-Second Roadmap
    '⚡ Your OSRS Journey in 30 Seconds': '⚡ Sua Jornada OSRS em 30 Segundos',
    'Quick Start': 'Início Rápido',
    'From a brand-new account to your first boss kill — follow this 30-second roadmap.': 'De uma conta nova ao seu primeiro chefe morto — siga este roteiro de 30 segundos.',
    'Step 1': 'Passo 1',
    'Start F2P': 'Comece F2P',
    'Create your account, complete Tutorial Island, and explore Lumbridge.': 'Crie sua conta, complete a Ilha do Tutorial e explore Lumbridge.',
    'Step 2': 'Passo 2',
    'Get Members': 'Seja Membro',
    'Unlock skills, quests, and content that make OSRS truly massive.': 'Desbloqueie habilidades, missões e conteúdo que tornam o OSRS gigante.',
    'Step 3': 'Passo 3',
    'Train Skills': 'Treine Habilidades',
    'Level up combat and gathering skills with our optimized guides.': 'Suba de nível em combate e coleta com nossos guias otimizados.',
    'Step 4': 'Passo 4',
    'Kill Bosses': 'Mate Chefes',
    'From Barrows to God Wars Dungeon — conquer every challenge.': 'De Barrows a God Wars Dungeon — conquiste cada desafio.',
    'Step 5': 'Passo 5',
    'Make Bank': 'Ganhe Dinheiro',
    '29 verified money-making methods from 0 GP to 10M+.': '29 métodos comprovados de lucro de 0 GP a 10M+.',
    '🔥 <strong>Bonus:</strong>': '🔥 <strong>Bônus:</strong>',
    'Join the Community →': 'Junte-se à Comunidade →',
    'Ask questions, share strats, find your clan': 'Pergunte, compartilhe estratégias, encontre seu clã',

    # Game Roadmaps
    '🗺️ Game Roadmaps — Pick Your Path': '🗺️ Roteiros de Jogo — Escolha Seu Caminho',
    '5 Novos': '5 NOVOS',
    '5 NEW': '5 NOVOS',
    'NOVO</span>': 'NOVO</span>',
    '7-Day Beginner Roadmap': '7-Day Beginner Roadmap',
    'First 7 days from F2P to member': 'Primeiros 7 dias de F2P a membro',
    'First Boss Progression': 'First Boss Progression',
    'Obor → Bryophyta → Barrows → Zulrah — boss progression path': 'De Obor a Zulrah — progressão de chefes',
    'Quest Cape Roadmap': 'Quest Cape Roadmap',
    '170+ quests organized in clear progression order': 'Roteiro completo da capa de missões',
    'Mid-Game Money Roadmap': 'Mid-Game Money Roadmap',
    '15+ money-making methods ranked by gear requirement': 'Lucro estável de médio nível',
    'Mid-to-High Progression': 'Mid-to-High Progression',
    'The bridge between mid-game and late-game progression': 'Avance do médio ao alto nível',

    # New Player Banner
    'New to OSRS?': 'Novo no OSRS?',
    '📅 8-Week Learning Path': '📅 Roteiro de 8 Semanas',
    '24+ guides organized into an 8-week roadmap — from your first login to bossing like a pro': '24+ guias organizados em um roteiro de 8 semanas — do seu primeiro login até chefes como um pro',
    '🧭 Start Your Journey →': '🧭 Inicie Sua Jornada →',

    # Pain Points
    '🔥⚡🔥 Pain Points Solved This Week': '🔥⚡🔥 Problemas Resolvidos Esta Semana',
    'From real player discussions — the guides you actually need right now': 'Das discussões reais dos jogadores — os guias que você realmente precisa agora',
    '🔰 Skill Training': '🔰 Treinamento de Habilidades',
    '🎯 Skill Training 2026 — 6 New Deep Dive Guides': '🎯 Treinamento de Habilidades 2026 — 6 Novos Guias Detalhados',
    'From Beginner to Max Account. Complete skill training roadmap across all 23 skills.': 'Do iniciante à conta máxima. Roteiro completo de treinamento para todas as 23 habilidades.',
    '⚔️ Combat & Money': '⚔️ Combate & Lucro',
    '💰 Slayer, Boss & Money Making — 8 New Guides': '💰 Slayer, Chefes & Lucro — 8 Novos Guias',
    'Beginner-friendly money makers, Slayer progression, and first boss strategies.': 'Métodos de lucro para iniciantes, progressão de Slayer e estratégias de primeiro chefe.',
    '🗺 Returning & Progression': '🗺 Retorno & Progressão',
    '📋 Returning Player, Diary & Quest — 8 New Guides': '📋 Jogador Retornando, Diário & Missões — 8 Novos Guias',
    'Catch up from a break, complete achievement diaries, and master key quests.': 'Recupere o atraso de uma pausa, complete diários de conquistas e domine missões importantes.',

    # Ad Label
    'Sponsor Recommendation': 'Sponsor Recommendation',

    # Explore Gielinor
    'Explore Gielinor': 'Explore Gielinor',
    'All Categories →': 'Todas as Categorias →',
    '💰 I Want to Make Money': '💰 Quero Ganhar Dinheiro',
    '29 proven GP methods — fresh deep dives inside': '29 métodos comprovados de GP — novos guias detalhados',
    '💰 Money Making': '💰 Lucro',
    '⚔️ Skill Training Hub': '⚔️ Central de Treinamento',
    'Level up all 23 skills efficiently': 'Suba de nível em todas as 23 habilidades eficientemente',
    '🏔️ Mid-Game Breakthrough': '🏔️ Avanço de Médio Jogo',
    'Mid-game breakthrough & progression': 'Avanço de médio jogo e progressão',
    '📜 Quest Walkthroughs': '📜 Guias de Missões',
    'Quest walkthroughs & key unlocks': 'Guias de missões e desbloqueios importantes',
    '👹 Beast Slayer Hub': '👹 Central de Matador de Monstros',
    'From first boss to endgame raids for OSRS players': 'Do primeiro chefe a raids endgame para jogadores de OSRS',
    '📅 Top Guides This Month': '📅 Top Guias do Mês',
    'Most-read guides by OSRS players this month': 'Guias mais lidos por jogadores de OSRS este mês',
    '🔥 This Week\'s Hot': '🔥 Quente da Semana',
    'Fresh guides and weekly highlights for OSRS players': 'Guias novos e destaques semanais para jogadores de OSRS',
    '🌐 Chinese Station': '🌐 Site Brasileiro',
    'Simplified Chinese guides for OSRS players': 'Guias em português brasileiro para jogadores de OSRS',
    'Guides': 'Guias',

    # Monthly Updates
    'Monthly Update — June 2026': 'Atualização Mensal — Junho 2026',
    '🔥 12 new guides published this week!': '🔥 12 novos guias publicados esta semana!',
    'View All Monthly Updates →': 'Ver Todas as Atualizações →',

    # Weekly Updates
    "What's New This Week": 'Novidades da Semana',
    'View all new guides →': 'Ver todos os novos guias →',

    # Hot Picks
    '🔥 Community Hot Picks': '🔥 Destaques da Comunidade',
    'Hot Picks — Money Making Deep Dives': 'Destaques — Análises de Lucro',
    '💰 Built from trending player questions on forums & Reddit.': '💰 Baseado nas perguntas mais populares dos fóruns e Reddit.',
    'Browse All 28 Money Making Guides →': 'Ver Todos os 28 Guias de Lucro →',

    # 8-Week Beginner Roadmap
    '🗺️ Stage 0: 8-Week Beginner Roadmap — Start Here!': '🗺️ Estágio 0: Roteiro de 8 Semanas — Comece Aqui!',
    '📝 +8 Updated This Week': '📝 +8 Atualizados Esta Semana',
    '📚 All 31 Beginner Guides →': '📚 Todos os 31 Guias para Iniciantes →',
    'WEEK 1': 'SEMANA 1',
    'WEEK 2': 'SEMANA 2',
    'WEEK 3': 'SEMANA 3',
    'WEEK 4': 'SEMANA 4',
    'WEEK 5': 'SEMANA 5',
    'WEEK 6': 'SEMANA 6',
    'WEEK 7': 'SEMANA 7',
    'WEEK 8': 'SEMANA 8',
    '🎯 Goal: Learn the basics': '🎯 Meta: Aprender o básico',
    '🎯 Goal: Combat-ready': '🎯 Meta: Pronto para combate',
    '🎯 Goal: Earn your first 1M GP': '🎯 Meta: Ganhe seu primeiro 1M GP',
    "🎯 Goal: Unlock members' content": '🎯 Meta: Desbloquear conteúdo de membro',
    '🎯 Goal: Find your tribe': '🎯 Meta: Encontre sua tribo',
    '🎯 Goal: Kill your first boss': '🎯 Meta: Mate seu primeiro chefe',
    '🎯 Goal: Play smarter': '🎯 Meta: Jogue de forma mais inteligente',
    '🎯 Goal: Graduate from beginner': '🎯 Meta: Forme-se de iniciante',
    '🎮 First Steps': '🎮 Primeiros Passos',
    '⚔️ Build Your Character': '⚔️ Construa Seu Personagem',
    '💰 Make Gold': '💰 Ganhe Ouro',
    '💎 Unlock Membership': '💎 Desbloqueie Membros',
    '🏰 Join the Community': '🏰 Junte-se à Comunidade',
    '🐉 Start Bossing': '🐉 Comece a Enfrentar Chefes',
    '📅 Build Good Habits': '📅 Construa Bons Hábitos',
    '🚀 Level Up Everything': '🚀 Evolua Tudo',
    'Master controls, navigation, and core game mechanics.': 'Domine controles, navegação e mecânicas principais do jogo.',
    'Skills, combat training, gear — build a solid foundation.': 'Habilidades, treinamento de combate, equipamentos — construa uma base sólida.',
    'From zero to millionaire — money making fundamentals.': 'De zero a milionário — fundamentos de lucro.',
    'Get membership, train prayer, start questing properly.': 'Obtenha membros, treine oração, comece a fazer missões corretamente.',
    'Clans, POH, minigames — OSRS is better together.': 'Clãs, POH, minigames — OSRS é melhor juntos.',
    'Your first steps into PvM — Barrows, NMZ, and beyond.': 'Seus primeiros passos no PvM — Barrows, NMZ e além.',
    'Daily routines, common mistakes to avoid, diaries.': 'Rotinas diárias, erros comuns a evitar, diários.',
    'Mobile, returning players, account types — advanced beginner topics.': 'Mobile, jogadores retornando, tipos de conta — tópicos avançados para iniciantes.',
    'View all': 'Ver todos',
    'guides': 'guias',

    # Topic Roadmaps
    '🗺️ Game Roadmaps — Pick Your Path': '🗺️ Roteiros de Jogo — Escolha Seu Caminho',
    'ROADMAP': 'ROTEIRO',
    '🎯 Zero to Boss-ready': '🎯 De zero a pronto para chefes',
    '🎯 Kill Your First Boss': '🎯 Mate Seu Primeiro Chefe',
    '🎯 Unlock Quest Cape': '🎯 Desbloqueie a Capa de Missões',
    '🎯 1M to 100M GP': '🎯 1M a 100M GP',
    '🎯 Level 70 → Endgame': '🎯 Nível 70 → Endgame',

    # Membership Hub
    '🔥 OSRS Membership Guide Hub — 2026 Price Hike & Everything You Need': 
        '🔥 Central de Guias de Membros OSRS — 2026 Aumento de Preço & Tudo que Você Precisa',
    '📰 JUST PUBLISHED': '📰 ACABOU DE PUBLICAR',
    'View Full Hub →': 'Ver Central Completa →',
    'JUNE 2026': 'JUNHO 2026',
    '🚨 Price Hike': '🚨 Aumento de Preço',
    '2026 Price Increase': 'Aumento de Preço 2026',
    'Jagex raised prices in March 2026. Monthly $11.99→$14.99, yearly almost doubled!': 
        'Jagex aumentou os preços em Março 2026. Mensal $11.99→$14.99, anual quase dobrou!',
    'ANALYSIS': 'ANÁLISE',
    '🤔 Value & Savings': '🤔 Valor e Economia',
    "Worth It? & How to Save": 'Vale a Pena? & Como Economizar',
    'Is membership still worth it after the price hike? Which payment method saves the most?':
        'Ainda vale a pena ser membro após o aumento? Qual método de pagamento economiza mais?',
    'F2P→MEMBER': 'F2P→MEMBRO',
    '🗺️ Your Roadmap': '🗺️ Seu Roteiro',
    'From Free Player to Member': 'De Jogador Grátis a Membro',
    'Everything you need before and after buying membership.': 'Tudo que você precisa antes e depois de comprar membros.',
    '⭐ #1 READ': '⭐ #1 LEIA',
    '📘 Complete Guide': '📘 Guia Completo',
    'Membership Complete Guide': 'Guia Completo de Membros',
    'The definitive guide. What it unlocks, how to buy, F2P vs Members comparison.':
        'O guia definitivo. O que desbloqueia, como comprar, comparação F2P vs Membros.',

    # Money Making section
    '💰 Top Money Making Guides': '💰 Principais Guias de Lucro',
    'All 23 guides →': 'Todos os 23 guias →',
    'All 27 guides →': 'Todos os 27 guias →',

    # Support Card
    'Every guide is free — this one stays free either way.': 'Todo guia é gratuito — este continua gratuito de qualquer forma.',
    'No paywalls, no subscriptions. But the': 'Sem paywalls, sem assinaturas. Mas o',
    'Early Access Guide Pack': 'Pacote de Acesso Antecipado',
    'gives you more:': 'te dá mais:',
    '10 Beginner Guides': '10 Guias para Iniciantes',
    '5 Premium Picks': '5 Escolhas Premium',
    '3-Day Early Access': 'Acesso Antecipado de 3 Dias',
    '3 New Guides Every Month': '3 Novos Guias Todo Mês',
    'Your purchase includes instant access to everything above':
        'Sua compra inclui acesso instantâneo a tudo acima',
    'Get the Early Access Guide Pack': 'Obtenha o Pacote de Acesso Antecipado',
    'Every guide stays free for everyone, always — no strings attached.':
        'Todo guia permanece gratuito para todos, sempre — sem compromisso.',

    # Newsletter
    'Weekly OSRS Tips': 'Dicas Semanais de OSRS',
    'Join 500+ players. One email per week — no spam.':
        'Junte-se a 500+ jogadores. Um email por semana — sem spam.',
    'Subscribe Free →': 'Inscreva-se Grátis →',
    'Unsubscribe anytime.': 'Cancele quando quiser.',

    # Footer
    'Your go-to resource for OSRS strategy guides. 150+ verified articles updated for 2026. AI-powered Q&A included.':
        'Seu recurso essencial para guias de estratégia OSRS. 150+ artigos verificados atualizados para 2026. Perguntas e Respostas com AI incluso.',
    'Money Making': 'Lucro',
    'Skill Training': 'Treinamento de Habilidades',
    'New Players': 'Novatos',
    'Boss & Quests': 'Chefes & Missões',
    'All Skills →': 'Todas as Habilidades →',
    'All Methods →': 'Todos os Métodos →',
    'All Quests →': 'Todas as Missões →',
}

def translate_file(src_path, dst_path, remove_games_bar=True):
    """Copy and translate an HTML file from English to pt-br"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    for eng, ptbr in REPLACE.items():
        content = content.replace(eng, ptbr)
    
    # Remove Crimson Desert & Windrose section
    if remove_games_bar:
        pattern = r'<!-- ========== NEW GAMES BAR.*?</div>\s*</div>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        # Also remove the second occurrence pattern
        pattern2 = r'<div class="new-games-bar">.*?</div>\s*</div>\s*</div>'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
    
    # Fix path references: guides/ → ../guides/ (actually they're in pt-br/guides/ so guides/ is correct)
    # Actually pt-br/index.html links to guides/ which will be pt-br/guides/
    # The main site links to guides/ which is BASE/guides/
    # So the links are correct relative to pt-br/
    
    # Fix CSS path
    content = content.replace('href="css/style.css"', 'href="../css/style.css"')
    content = content.replace('src="js/', 'src="../js/')
    content = content.replace('src="images/', 'src="../images/')
    content = content.replace('href="mid-to-high.html"', 'href="../mid-to-high.html"')
    content = content.replace('src="../images/warriors_guild.png"', 'src="../images/warriors_guild.png"')
    content = content.replace('src="../images/fighting_graardor.png"', 'src="../images/fighting_graardor.png"')
    content = content.replace('src="../images/clan_wars.png"', 'src="../images/clan_wars.png"')
    
    # Add pt-br hreflang
    content = content.replace(
        '<link rel="alternate" hreflang="x-default" href="https://osrsguru.com/">',
        '<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/">\n  <link rel="alternate" hreflang="x-default" href="https://osrsguru.com/">'
    )
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {dst_path}")

def create_hub_page(name_pt, name_en, title_pt, desc_pt, category):
    """Create a hub page based on zh/ hub template"""
    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_pt} — OSRS Guru Brasil</title>
<link rel="canonical" href="https://osrsguru.com/pt-br/{name_pt}.html">
<link rel="stylesheet" href="../css/style.css">
<meta name="description" content="{desc_pt}">
<meta name="robots" content="index, follow">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S1BGC91MYV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-S1BGC91MYV');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532760886171435" crossorigin="anonymous"></script>
</head>
<body>
<header class="site-header"><div class="header-inner">
<a href="/pt-br/" class="logo">⚔ OSRS <span>Guru</span></a>
<nav class="main-nav">
<a href="iniciante.html">🗺️ Iniciante</a>
<a href="lucro.html">Lucro</a>
<a href="habilidades.html">Habilidades</a>
<a href="missoes.html">Missões</a>
<a href="chefes.html">Chefes</a>
<a href="membros.html">Membros</a>
<a href="../index.html">🇺🇸 English</a>
</nav></div></header>
<div class="container"><h1>{title_pt}</h1>
<p>{desc_pt}</p>
<p style="color:#888;">Guias em português brasileiro com conteúdo em inglês.</p>
</div>
<footer class="site-footer"><div class="footer-inner"><div class="footer-bottom">
<span>© 2026 OSRS Guru Brasil — Site de fãs, não afiliado à Jagex Ltd.</span>
<a href="../index.html" style="color:var(--text-muted);text-decoration:none;font-size:.82rem;margin-left:16px;">🇺🇸 English Main Site</a>
</div></div></footer>
</body>
</html>"""
    path = DST / f"{name_pt}.html"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Created hub: {name_pt}.html")

def add_30s_preview(html_content, guide_title_en):
    """Add a 30-second preview box at the start of guide body content"""
    preview_html = f'''
<div class="quick-preview" style="background:linear-gradient(135deg,#fdf8ef,#fff8e8);border:1.5px solid #d4af37;border-radius:12px;padding:20px 24px;margin-bottom:24px;">
  <h3 style="font-family:'Cinzel',serif;color:#3b2615;margin:0 0 8px;font-size:1.1rem;">⚡ Visão Rápida de 30 Segundos</h3>
  <p style="color:#3b2615;font-size:.92rem;line-height:1.5;margin:0 0 10px;">
    <strong>{guide_title_en}</strong><br>
    Quer dominar {guide_title_en.split("OSRS")[-1] if "OSRS" in guide_title_en else guide_title_en}? 
    Este guia completo cobre tudo que você precisa saber — desde o básico até estratégias avançadas. 
    Preparado para jogadores brasileiros de Old School RuneScape.
  </p>
  <div style="border-top:1px dashed #e0d5c0;padding-top:10px;">
    <p style="color:#8b7a6b;font-size:.82rem;margin:0;line-height:1.4;">
      <strong>Looking for the English version?</strong><br>
      Looking to master {guide_title_en.split("OSRS")[-1] if "OSRS" in guide_title_en else guide_title_en}? 
      This complete guide covers everything you need — from basics to advanced strats.
    </p>
  </div>
</div>
'''
    # Insert after <body> or after the hero image/h1
    # Look for the intro paragraph or first content after h1
    insert_pos = html_content.find('<div class="guide-content"')
    if insert_pos == -1:
        insert_pos = html_content.find('<article')
    if insert_pos == -1:
        # Just put it after the h1
        h1_pos = html_content.find('</h1>')
        if h1_pos > 0:
            insert_pos = h1_pos + 5
        else:
            insert_pos = html_content.find('<body') + 6
            if insert_pos == 5:
                insert_pos = 0
    
    return html_content[:insert_pos] + preview_html + html_content[insert_pos:]

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("OSRS Guru Brasil Builder iniciado!")
    
    # Step 1: Create pt-br/index.html from main index.html
    print("\n- Step 1: Creating pt-br/index.html ---")
    translate_file(SRC, DST / "index.html")
    
    # Step 2: Create hub pages
    print("\n--- Step 2: Creating hub pages ---")
    hubs = [
        ("iniciante", "beginner", "Guia para Iniciantes", "Guia completo para novos jogadores de OSRS. Aprenda o básico, treine habilidades e comece sua jornada."),
        ("chefes", "bosses", "Guias de Chefes", "Guias detalhados de chefes OSRS. De Barrows a Raids, estratégias de equipamento e rotações."),
        ("missoes", "quests", "Guias de Missões", "Guias de missões OSRS passo a passo. Desbloqueie equipamentos, áreas e recompensas exclusivas."),
        ("habilidades", "skills", "Treinamento de Habilidades", "Guias completos de treinamento para todas as 23 habilidades OSRS. Rotas rápidas, AFK e econômicas."),
        ("lucro", "money", "Guias de Lucro", "29 métodos comprovados de lucro OSRS. De F2P a membro, de 0 GP a 10M+."),
        ("membros", "membership", "Guia de Membros OSRS", "Tudo sobre membros OSRS: preços, benefícios, comparação F2P vs membro e dicas de economia."),
        ("atualizacoes-semanais", "weekly", "Atualizações Semanais", "Novos guias e destaques semanais para jogadores de OSRS."),
        ("atualizacoes-mensais", "monthly", "Atualizações Mensais", "Atualizações mensais OSRS com novos guias, análises de meta e notícias."),
        ("topicos-populares", "forum", "Tópicos Populares", "Tópicos mais discutidos pela comunidade OSRS brasileira."),
        ("comunidade", "community", "Comunidade OSRS", "Junte-se à comunidade OSRS Guru Brasil. Pergunte, compartilhe e conecte-se."),
    ]
    for name_pt, name_en, title, desc in hubs:
        create_hub_page(name_pt, name_en, title, desc, name_en)
    
    # Step 3: Copy zh/guides/ to pt-br/guides/ with modifications
    print("\n--- Step 3: Processing guide articles ---")
    src_guides = BASE / "zh" / "guides"
    dst_guides = DST / "guides"
    
    if src_guides.exists():
        os.makedirs(dst_guides, exist_ok=True)
        guide_files = list(src_guides.glob("*.html"))
        print(f"  Found {len(guide_files)} guides to process")
        
        for i, src_file in enumerate(guide_files):
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Step 3a: Translate title if it has Chinese
            # Get the title tag content
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                old_title = title_match.group(1)
                new_title = old_title
                # Translate common Chinese title prefixes
                cn_translations = {
                    '攻略': 'Guia',
                    '指南': 'Guia',
                    '完整': 'Completo',
                    '新手': 'Iniciante',
                    '赚钱': 'Lucro',
                    '技能': 'Habilidade',
                    '训练': 'Treinamento',
                    '任务': 'Missão',
                    '会员': 'Membro',
                    'Boss': 'Chefe',
                    'Boss 攻略': 'Guia de Chefe',
                    '教程': 'Tutorial',
                }
                for cn, pt in cn_translations.items():
                    new_title = new_title.replace(cn, pt)
                content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title} — OSRS Guru Brasil</title>')
                # Also replace description
                content = content.replace(
                    f'<meta name="description" content="{old_title}',
                    f'<meta name="description" content="{new_title}'
                )
            
            # Step 3b: Add hreflang for pt-br
            content = content.replace(
                '<link rel="canonical"',
                '<link rel="alternate" hreflang="pt-br" href="https://osrsguru.com/pt-br/guides/">\n<link rel="canonical"'
            )
            
            # Step 3c: Fix CSS and JS paths
            content = content.replace('href="css/style.css"', 'href="../../css/style.css"')
            content = content.replace('src="../css/style.css"', 'src="../../css/style.css"')
            content = content.replace('href="../css/style.css"', 'href="../../css/style.css"')
            
            # Step 3d: Fix image paths
            content = content.replace('src="images/', 'src="../../images/')
            
            # Step 3e: Add 30-second preview 
            # Use the file name as a guide title
            guide_name = src_file.stem.replace('osrs-', '').replace('-', ' ').replace('2026', '').strip()
            content = add_30s_preview(content, guide_name)
            
            # Step 3f: Fix canonical URL
            content = content.replace(
                f'canonical" href="https://osrsguru.com/guides/',
                f'canonical" href="https://osrsguru.com/pt-br/guides/'
            )
            
            # Write the file
            dst_file = dst_guides / src_file.name
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i+1}/{len(guide_files)} guides processed")
        
        print(f"  [OK] All {len(guide_files)} guides processed!")
    else:
        print("  [WARN] zh/guides/ directory not found, skipping")
    
    print("\nBrazil site build complete!")
    print(f"   Location: {DST}")
    print(f"   Total files: {len(list(DST.rglob('*.html')))} HTML pages")
