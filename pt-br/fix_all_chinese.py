#!/usr/bin/env python3
"""
Comprehensive Chinese→Brazilian Portuguese fix for OSRS Guru Brazilian site.
Handles: hub pages, guide article titles, meta, TOC, .d spans, 30-Second Preview.
"""
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

BASE = Path('C:/Users/Lenovo/osrs-guide-site')
PT_DIR = BASE / 'pt-br'

# ═══════════════════════════════════════════════════════════════
# HUB PAGE Chinese→Portuguese body text translations
# ═══════════════════════════════════════════════════════════════
HUB_CN2PT = {
    # chefes.html specific
    '用预算Equipamento配置和逐步策略征服Cada OSRS Chefe。Zulrah 轮换Guia、Vorkath Woox Walk、神战等——Tudo atualizado para 2026。': 
        'Conquiste cada chefe do OSRS com equipamento de orçamento e estratégias passo a passo. Guia de rotação de Zulrah, Woox Walk do Vorkath, God Wars e muito mais — tudo atualizado para 2026.',
    
    '预算装备和逐步策略征服每个OSRS首领。从Zulrah旋转到Vorkath Woox Walk和God Wars Dungeon，低门槛攻克Boss。': 
        'Equipamento de orçamento e estratégias passo a passo para conquistar cada chefe do OSRS. Da rotação de Zulrah ao Woox Walk do Vorkath e God Wars Dungeon — domine os chefes com requisitos baixos.',
    
    # missoes.html specific
    'OSRS任务Guia从新手到Cape的完整路线。最快的经验路径、奖励顺序、推荐任务2026。': 
        'Guia completo de missões do OSRS, do iniciante à Capa. Caminhos de XP mais rápidos, ordem de recompensas, missões recomendadas para 2026.',
    
    'Quer otimizar sua jornada de Missões OSRS? Nossos guias cobrem sequenciamento ideal、奖励选择、任务速通e muito mais.': 
        'Quer otimizar sua jornada de missões no OSRS? Nossos guias cobrem sequenciamento ideal, escolha de recompensas, speedrun de missões e muito mais.',
    
    # habilidades.html specific
    '从到顶，我们的技能指南涵盖所有技能从1到99。包括训练方法、利润率、武器、装备、等级划分等。Tudo atualizado para 2026。': 
        'Do início ao topo, nossos guias de habilidades cobrem todas as habilidades de 1 a 99. Inclui métodos de treinamento, margens de lucro, armas, equipamentos, faixas de nível e muito mais. Tudo atualizado para 2026.',
    
    '从新手到大师，我们覆盖所有OSRS技能——战斗、采集、生产。每个技能推荐最佳训练路径、装备和方法。': 
        'Do iniciante ao mestre, cobrimos todas as habilidades do OSRS — combate, coleta, produção. Recomendamos os melhores caminhos de treinamento, equipamentos e métodos para cada habilidade.',
    
    # lucro.html specific
    '从零到数百指南——按技能要求、利润率和风险分层的顶级赚钱方法。': 
        'Guias do zero a centenas de milhões — métodos de lucro mais bem classificados por requisito de habilidade, margem de lucro e risco.',
    
    '从F2P到P2P——基于真实GP/小时数据和装备要求的顶级OSRS赚钱方法。': 
        'Do F2P ao P2P — os melhores métodos de lucro do OSRS baseados em dados reais de GP/hora e requisitos de equipamento.',
    
    # index.html specific
    '中文攻略站点已上线，OSRS Guru - Old School RuneScape 指南、赚钱方法、技能训练、Boss攻略。面向巴西葡萄牙语玩家。': 
        'Site de guias em português brasileiro agora online. OSRS Guru — guias de Old School RuneScape, métodos de lucro, treinamento de habilidades, guias de chefes. Feito para jogadores brasileiros.',
    
    # Sub-titles and category names
    '新手起步': 'Primeiros Passos',
    '从零开始建立你的帐户': 'Construa sua conta do zero',
    '赚钱方法': 'Métodos de Lucro',
    'F2P和会员最佳赚钱策略': 'Melhores estratégias de lucro F2P e membro',
    '技能训练': 'Treinamento de Habilidades',
    '所有技能1-99指南': 'Guias de 1-99 para todas as habilidades',
    'Boss攻略': 'Guias de Chefes',
    '从入门到高手': 'Do iniciante ao avançado',
    '任务指南': 'Guias de Missões',
    '高效完成任务解锁奖励': 'Complete missões eficientemente e desbloqueie recompensas',
    '装备指南': 'Guias de Equipamento',
    '最佳装备推荐': 'Melhores recomendações de equipamento',
    '新手专区': 'Zona do Iniciante',
    '给零基础玩家的入门指南': 'Guias introdutórios para jogadores iniciantes',
    '点击查看': 'Clique para ver',
    '了解更多': 'Saiba mais',
    '快速入门': 'Início Rápido',
    '进阶攻略': 'Guias Avançados',
    '高手专区': 'Zona do Expert',
    '最新更新': 'Últimas Atualizações',
}

# ═══════════════════════════════════════════════════════════════
# Guide article: Chinese TOC parenthesis translations
# ═══════════════════════════════════════════════════════════════
TOC_CN2PT = {
    '研究方法': 'Metodologia',
    '装备要求': 'Requisitos de Equipamento',
    '收益分析': 'Análise de Lucro',
    '经验值': 'Experiência',
    '效率对比': 'Comparação de Eficiência',
    '步骤详解': 'Passos Detalhados',
    '进阶技巧': 'Dicas Avançadas',
    '常见问题': 'Perguntas Frequentes',
    '准备工作': 'Preparação',
    '最佳方法': 'Melhores Métodos',
    '推荐配置': 'Configuração Recomendada',
    '注意事项': 'Avisos',
    '小贴士': 'Dicas',
    '总结': 'Resumo',
    '前言': 'Introdução',
    '基础篇': 'Básico',
    '进阶篇': 'Avançado',
    '高手篇': 'Expert',
    '入门指南': 'Guia Iniciante',
    '详细攻略': 'Guia Detalhado',
    '速通路线': 'Rota Rápida',
    '效率最大化': 'Eficiência Máxima',
    '新手推荐': 'Recomendado para Iniciantes',
    '会员专属': 'Exclusivo para Membros',
    'F2P推荐': 'Recomendado para F2P',
    '核心机制': 'Mecânica Principal',
    '实战技巧': 'Dicas Práticas',
    '掉落列表': 'Lista de Drop',
    '战绩统计': 'Estatísticas',
    '收入统计': 'Estatísticas de Lucro',
    '视频教程': 'Tutorial em Vídeo',
    '其他推荐': 'Outras Recomendações',
    '替代方案': 'Alternativas',
    '风险提示': 'Aviso de Risco',
    '入门': 'Iniciante',
    '中级': 'Intermediário',
    '高级': 'Avançado',
    '专家': 'Expert',
    '前期准备': 'Preparação Inicial',
    '中期发展': 'Desenvolvimento Médio',
    '后期优化': 'Otimização Final',
    '赚钱篇': 'Lucro',
    '技能篇': 'Habilidades',
    '战斗篇': 'Combate',
    '任务篇': 'Missões',
    '配置篇': 'Configuração',
    '成长路线': 'Rota de Crescimento',
    '最低要求': 'Requisitos Mínimos',
    '推荐等级': 'Nível Recomendado',
    '目标收益': 'Lucro Alvo',
    '热门方法': 'Métodos Populares',
    '地图指引': 'Guia de Mapa',
    '解锁条件': 'Condições de Desbloqueio',
    '专属奖励': 'Recompensas Exclusivas',
    '更新日志': 'Registro de Atualizações',
}

# ═══════════════════════════════════════════════════════════════
# 30-Second Preview template: generate article-specific previews
# ═══════════════════════════════════════════════════════════════
def generate_preview(h1_text):
    """Generate an article-specific 30-Second Preview text based on H1 title."""
    h1 = h1_text.strip() if h1_text else ""
    
    # Identify topic from title
    topic_map = {
        'money making': 'métodos de lucro',
        'money': 'métodos de lucro',
        'slayer': 'treinamento de Slayer',
        'combat': 'treinamento de combate',
        'prayer': 'treinamento de Oração',
        'hunter': 'treinamento de Caça',
        'fishing': 'treinamento de Pesca',
        'mining': 'treinamento de Mineração',
        'smithing': 'treinamento de Smithing',
        'crafting': 'treinamento de Artesanato',
        'farming': 'treinamento de Agricultura',
        'woodcutting': 'treinamento de Corte de Madeira',
        'construction': 'treinamento de Construção',
        'runecrafting': 'treinamento de Runecrafting',
        'herblore': 'treinamento de Herblore',
        'thieving': 'treinamento de Furto',
        'fletching': 'treinamento de Fletching',
        'cooking': 'treinamento de Culinária',
        'firemaking': 'treinamento de Firemaking',
        'agility': 'treinamento de Agilidade',
        'barrows': 'Barrows',
        'zulrah': 'Zulrah',
        'vorkath': 'Vorkath',
        'inferno': 'Inferno',
        'quest': 'missões',
        'minigame': 'minigames',
        'gear': 'equipamento',
        'boss': 'chefes',
        'ironman': 'Ironman',
        'f2p': 'F2P',
        'beginner': 'iniciantes',
        'grand exchange': 'Grand Exchange',
        'raid': 'raids',
        'wilderness': 'Deserto Selvagem',
        'clue scroll': 'Clue Scrolls',
        'sailing': 'Sailing',
        'moneymaking': 'métodos de lucro',
        'new player': 'novos jogadores',
        'achievement diary': 'Diários de Conquistas',
        'diary': 'Diários',
        'birdhouse': 'Birdhouse Runs',
    }
    
    topic = 'este tópico'
    h1_lower = h1.lower()
    for key, val in topic_map.items():
        if key in h1_lower:
            topic = val
            break
    
    # Build PT-BR preview
    pt_text = (
        f"Quer dominar {topic}? "
        f"Este guia completo cobre tudo que você precisa saber — desde o básico até estratégias avançadas. "
        f"Preparado para jogadores brasileiros de Old School RuneScape."
    )
    en_text = (
        f"Looking to master {topic}? "
        f"This complete guide covers everything you need to know — from the basics to advanced strategies. "
        f"Prepared for Brazilian Old School RuneScape players."
    )
    return pt_text, en_text


def fix_file(path):
    """Fix all Chinese text in a single file."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
    if not has_chinese:
        return False  # No Chinese, skip
    
    # ═══ 1. Fix Hub page Chinese body text ═══
    for cn_text, pt_text in HUB_CN2PT.items():
        if cn_text in content:
            content = content.replace(cn_text, pt_text)
    
    # ═══ 2. Fix Chinese in og:description ═══
    def fix_og_desc(match):
        desc = match.group(1)
        if re.search(r'[\u4e00-\u9fff]', desc):
            # Try to salvage the English part, remove Chinese
            # Pattern: "Chinese 赚钱攻略" → keep English after Chinese
            cleaned = re.sub(r'^[\u4e00-\u9fff\s（）\(\)\d]+', '', desc)
            cleaned = re.sub(r'[\u4e00-\u9fff\s]+:', '', cleaned)
            cleaned = cleaned.strip().lstrip(',').lstrip('，').strip()
            if not cleaned:
                cleaned = "Complete guide for OSRS players — updated for 2026."
            return f'<meta property="og:description" content="{cleaned}">'
        return match.group(0)
    
    content = re.sub(
        r'<meta property="og:description" content="(.*?)">',
        fix_og_desc, content
    )
    
    # ═══ 3. Fix Chinese in meta description ═══
    def fix_meta_desc(match):
        desc = match.group(1)
        if re.search(r'[\u4e00-\u9fff]', desc):
            # Remove full Chinese sentences/phrases, keep English
            cleaned = re.sub(r'[\u4e00-\u9fff（）\(\)]+\s*', '', desc)
            cleaned = cleaned.strip().strip('—').strip('-').strip()
            if not cleaned:
                cleaned = "OSRS guide updated for 2026 — complete strategies for Brazilian players."
            return f'<meta name="description" content="{cleaned}">'
        return match.group(0)
    
    content = re.sub(
        r'<meta name="description" content="(.*?)">',
        fix_meta_desc, content
    )
    
    # ═══ 4. Fix Chinese in meta keywords ═══
    def fix_meta_kw(match):
        kw = match.group(1)
        if re.search(r'[\u4e00-\u9fff]', kw):
            cleaned = re.sub(r'[\u4e00-\u9fff、，]+\s*', '', kw)
            cleaned = cleaned.strip().strip(',').strip()
            if not cleaned:
                cleaned = "OSRS, RuneScape, guide, tips, 2026"
            return f'<meta name="keywords" content="{cleaned}">'
        return match.group(0)
    
    content = re.sub(
        r'<meta name="keywords" content="(.*?)">',
        fix_meta_kw, content
    )
    
    # ═══ 5. Fix Chinese in <title> tags ═══
    def fix_title_tag(match):
        title = match.group(1)
        # Remove Chinese characters from title
        cleaned = re.sub(r'[\u4e00-\u9fff（）\u2014\u2013]+', '', title)
        cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip().strip('—').strip('-').strip()
        if not cleaned:
            cleaned = "OSRS Guru Brasil — Guias de Old School RuneScape"
        return f'<title>{cleaned}</title>'
    
    content = re.sub(r'<title>(.*?)</title>', fix_title_tag, content)
    
    # ═══ 6. Fix TOC Chinese in parentheses e.g. (中文) ═══
    def fix_toc_cn(match):
        cn_text = match.group(1)
        # Look up translation
        if cn_text in TOC_CN2PT:
            return f'({TOC_CN2PT[cn_text]})'
        # If not in dictionary, just remove Chinese but keep parens
        return f'({cn_text})'
    
    content = re.sub(r'\(([\u4e00-\u9fff]+)\)', fix_toc_cn, content)
    
    # Also fix bare Chinese without parens in TOC-like contexts
    def fix_bare_cn(match):
        cn_text = match.group(1)
        if cn_text in TOC_CN2PT:
            return TOC_CN2PT[cn_text]
        return cn_text
    
    content = re.sub(r'>([\u4e00-\u9fff]+)<', fix_bare_cn, content)
    
    # ═══ 7. Fix .d span descriptions with Chinese ═══
    def fix_d_span(match):
        text = match.group(1)
        if re.search(r'[\u4e00-\u9fff]', text):
            # Remove Chinese characters from d span
            cleaned = re.sub(r'[\u4e00-\u9fff（）\u2014\u2013]+', '', text)
            cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip().strip('—').strip('-').strip()
            if not cleaned:
                cleaned = "Complete guide for OSRS players."
            return f'<span class="d">{cleaned}</span>'
        return match.group(0)
    
    content = re.sub(
        r'<span class="d">(.*?)</span>',
        fix_d_span, content
    )
    
    # ═══ 8. Fix remaining arbitrary Chinese text in body ═══
    # Remove Chinese chars in non-code content (keeping navigation, CSS, etc.)
    def clean_body_cn(text):
        """Remove Chinese characters from body text content."""
        lines = text.split('\n')
        clean_lines = []
        for line in lines:
            # Skip lines that are purely HTML tags, CSS, or JS
            stripped = line.strip()
            if not stripped:
                clean_lines.append(line)
                continue
            # Only process text-heavy lines (high text-to-tag ratio)
            tag_ratio = len(re.findall(r'<[^>]+>', stripped)) / max(len(stripped), 1)
            if tag_ratio > 0.3:
                clean_lines.append(line)
                continue
            # Replace Chinese with nothing (we've already handled known patterns)
            if re.search(r'[\u4e00-\u9fff]{4,}', stripped):
                # Long Chinese text in body - try to fix
                cleaned = re.sub(r'[\u4e00-\u9fff（）\u2014\u2013]+\s*', '', stripped)
                cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
                if cleaned and len(cleaned) > 3:
                    # Preserve indentation
                    indent = line[:len(line) - len(line.lstrip())]
                    clean_lines.append(indent + cleaned)
                else:
                    clean_lines.append(line)
            else:
                clean_lines.append(line)
        return '\n'.join(clean_lines)
    
    content = clean_body_cn(content)
    
    # ═══ 9. Fix 30-Second Preview text if it has Chinese ═══
    # Extract H1 to generate preview
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    if h1_match:
        h1_text = h1_match.group(1).strip()
        pt_preview, en_preview = generate_preview(h1_text)
        
        # Find and replace quick-preview 
        preview_pattern = r'(<div class="quick-preview"[^>]*>.*?<h3[^>]*>⚡ Visão Rápida de 30 Segundos</h3>\s*<p[^>]*>)\s*<strong>[^<]*</strong><br>(.*?)(</p>\s*<div[^>]*>\s*<p[^>]*>\s*<strong>Looking for the English version\?</strong><br>\s*)(.*?)(</p>)'
        
        def fix_preview(match):
            return f'{match.group(1)}<strong>{h1_text}</strong><br>{pt_preview}{match.group(3)}{en_preview}{match.group(5)}'
        
        content = re.sub(preview_pattern, fix_preview, content, flags=re.DOTALL)
    
    # ═══ 10. Clean up any remaining Chinese parentheses （）→ () ═══
    content = content.replace('（', '(').replace('）', ')')
    
    # ═══ 11. Fix JSON-LD headline with Chinese ═══
    def fix_json_headline(match):
        headline = match.group(1)
        if re.search(r'[\u4e00-\u9fff]', headline):
            cleaned = re.sub(r'[\u4e00-\u9fff（）]+', '', headline)
            cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip().strip('—').strip('-').strip()
            if not cleaned:
                cleaned = "OSRS Guide — Complete 2026"
            return f'"headline": "{cleaned}"'
        return match.group(0)
    
    content = re.sub(r'"headline": "(.*?)"', fix_json_headline, content)
    
    # ═══ 12. Fix JSON-LD description with Chinese ═══
    def fix_json_desc(match):
        desc = match.group(1)
        if re.search(r'[\u4e00-\u9fff]', desc):
            cleaned = re.sub(r'[\u4e00-\u9fff（）\u2014\u2013]+\s*', '', desc)
            cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
            if not cleaned:
                cleaned = "Complete OSRS guide updated for 2026."
            return f'"description": "{cleaned}"'
        return match.group(0)
    
    content = re.sub(r'"description": "(.*?)"', fix_json_desc, content)
    
    # Write if changed
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def scan_chinese(path):
    """Count remaining Chinese chars in a file."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    return cn_chars


if __name__ == '__main__':
    print("=" * 60)
    print("🇧🇷  BRAZILIAN SITE — CHINESE FIX SCRIPT")
    print("=" * 60)
    
    # Phase 1: Fix hub pages
    print("\n📋 Phase 1: Fixing hub pages...")
    hub_files = ['index.html', 'chefes.html', 'missoes.html', 'habilidades.html', 'lucro.html']
    hub_fixed = 0
    for fname in hub_files:
        fpath = PT_DIR / fname
        if fpath.exists():
            before = scan_chinese(fpath)
            if fix_file(fpath):
                after = scan_chinese(fpath)
                print(f"  ✅ {fname}: {before} → {after} Chinese chars")
                hub_fixed += 1
            elif before > 0:
                print(f"  ⚠️  {fname}: {before} Chinese chars (could not fix all)")
            else:
                print(f"  ✅ {fname}: clean (0 Chinese chars)")
    
    # Phase 2: Fix guide articles
    print("\n📋 Phase 2: Fixing guide articles...")
    guide_dir = PT_DIR / 'guides'
    fixed = 0
    total_cn_before = 0
    total_cn_after = 0
    still_dirty = []
    
    for fpath in sorted(guide_dir.glob('*.html')):
        before = scan_chinese(fpath)
        total_cn_before += before
        if before > 0:
            if fix_file(fpath):
                after = scan_chinese(fpath)
                total_cn_after += after
                fixed += 1
                if after > 0:
                    still_dirty.append((fpath.name, after))
                print(f"  ✅ {fpath.name}: {before} → {after} Chinese chars")
            else:
                after = scan_chinese(fpath)
                total_cn_after += after
                if after > 0:
                    still_dirty.append((fpath.name, after))
        else:
            total_cn_after += 0
    
    print(f"\n{'=' * 60}")
    print(f"📊 SUMMARY")
    print(f"  Hub pages fixed: {hub_fixed}")
    print(f"  Guide articles with fixes: {fixed}")
    print(f"  Total Chinese chars before: {total_cn_before}")
    print(f"  Total Chinese chars after: {total_cn_after}")
    print(f"  Reduction: {total_cn_before - total_cn_after} ({100 - (total_cn_after/max(total_cn_before,1)*100):.1f}%)")
    
    if still_dirty:
        print(f"\n⚠️  Articles still with Chinese ({len(still_dirty)}):")
        for name, count in sorted(still_dirty, key=lambda x: -x[1])[:20]:
            print(f"    {name}: {count} chars")
    else:
        print(f"\n✅ All Chinese text fixed! Zero remaining.")
    
    print(f"\n{'=' * 60}")
