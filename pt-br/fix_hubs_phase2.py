#!/usr/bin/env python3
"""
Phase 2: Fix remaining Chinese in hub pages only.
"""
import re
from pathlib import Path

BASE = Path(r'C:\Users\Lenovo\osrs-guide-site')
PT_DIR = BASE / 'pt-br'

# Remaining Chinese→Portuguese for hub page text
HUB_PT = {
    # chefes.html
    '低成本': 'Baixo Custo',
    '击败': 'Derrotar',
    '噩梦': 'Pesadelo',
    '团本': 'Raids',
    '团队': 'Grupo',
    '小时': 'Horas',
    '弯刀': 'Cimitarra',
    '成就': 'Conquistas',
    '新内容': 'Novo Conteúdo',
    '新武器': 'Novas Armas',
    '杀手': 'Assassino',
    '标志性': 'Icônico',
    '综合': 'Geral',
    '腐化': 'Corrompido',
    '荒野': 'Selvagem',
    '轮换': 'Rotação',
    '铁人': 'Ironman',
    '链锤': 'Maça Corrente',
    '高利润': 'Alto Lucro',
    
    # missoes.html
    '各': 'Cada',
    '图': 'Mapa',
    '屠龙者': 'Matador de Dragões',
    '必做': 'Obrigatório',
    '披风': 'Capa',
    '解锁': 'Desbloquear',
    '通关': 'Completar',
    '高难度': 'Dificuldade Alta',
    '魔法': 'Magia',
    
    # habilidades.html  
    '伐木': 'Corte de Madeira',
    '偷窃': 'Furto',
    '全': 'Tudo',
    '力量': 'Força',
    '完全': 'Completo',
    '工艺': 'Artesanato',
    '总览': 'Visão Geral',
    '战斗': 'Combate',
    '攻击': 'Ataque',
    '敏捷': 'Agilidade',
    '早期': 'Início',
    '最快': 'Mais Rápido',
    '烹饪': 'Culinária',
    '猎人': 'Caça',
    '生产': 'Produção',
    '生命值': 'Vida',
    '祷告': 'Oração',
    '终局': 'Endgame',
    '航海': 'Navegação',
    '药草学': 'Herborismo',
    '采集': 'Coleta',
    '钓鱼': 'Pesca',
    '锻造': 'Ferraria',
    '防御': 'Defesa',
    '高效': 'Eficiente',
    
    # lucro.html
    '与': 'e',
    '中期': 'Médio',
    '低强度': 'Baixa Intensidade',
    '倒卖': 'Flipping',
    '养殖': 'Criação',
    '利润': 'Lucro',
    '到中期': 'ao Médio',
    '年': 'Ano',
    '挂机': 'AFK',
    '排行榜': 'Ranking',
    '日常': 'Diário',
    '月': 'Mês',
    '杀绿龙': 'Matar Dragão Verde',
    '每小时': 'Por Hora',
    '每日': 'Diariamente',
    '航海后': 'Pós-Navegação',
    '起步': 'Iniciante',
    '非': 'Não',
    '图': 'Mapa',
}

def fix_hub(path):
    """Replace remaining Chinese phrases in a hub page."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for cn, pt in sorted(HUB_PT.items(), key=lambda x: -len(x[0])):
        if cn in content:
            content = content.replace(cn, pt)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def count_cn(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return len([c for c in content if '\u4e00' <= c <= '\u9fff'])

if __name__ == '__main__':
    print("Phase 2: Hub page remaining Chinese fix\n")
    for fname in ['index.html', 'chefes.html', 'missoes.html', 'habilidades.html', 'lucro.html']:
        fpath = PT_DIR / fname
        if fpath.exists():
            before = count_cn(fpath)
            if fix_hub(fpath):
                after = count_cn(fpath)
                print(f"  [OK] {fname}: {before} -> {after}")
            else:
                print(f"  [OK] {fname}: already clean ({before})")
    
    print("\nDone!")
