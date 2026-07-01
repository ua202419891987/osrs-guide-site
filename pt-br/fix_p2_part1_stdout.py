#!/usr/bin/env python3
"""
P2 Phase 1 Fix Script - Output to stdout
修复 pt-br 站的 P2 问题：
- P2-1: 英文 alt 文本 → 葡语
- P2-2: img 缺 height → 加 height

用法: python fix_p2_part1_stdout.py <arquivo.html>
输出: 修改后的文件内容（标准输出）
"""

import os
import re
import sys

# P2-1: alt 文本替换映射
ALT_REPLACEMENTS = {
    'alt="OSRS Mining Guide"': 'alt="Guia de Mineração OSRS"',
    'alt="OSRS Woodcutting"': 'alt="Corte de Lenha OSRS"',
    'alt="OSRS Fishing spots"': 'alt="Pontos de Pesca OSRS"',
    'alt="OSRS Firemaking"': 'alt="Arte do Fogo OSRS"',
    'alt="OSRS Cooking"': 'alt="Culinária OSRS"',
    'alt="OSRS Crafting"': 'alt="Artesanato OSRS"',
    'alt="OSRS Smithing"': 'alt="Ferraria OSRS"',
    'alt="OSRS Herblore"': 'alt="Herbologia OSRS"',
    'alt="OSRS Fletching"': 'alt="Arqueação OSRS"',
    'alt="OSRS Runecrafting"': 'alt="Criação de Runas OSRS"',
    'alt="OSRS Thieving"': 'alt="Roubo OSRS"',
    'alt="OSRS Agility"': 'alt="Agilidade OSRS"',
    'alt="OSRS Hunter"': 'alt="Caça OSRS"',
    'alt="OSRS Slayer"': 'alt="Extermínio OSRS"',
    'alt="OSRS Farming"': 'alt="Agricultura OSRS"',
    'alt="OSRS Construction"': 'alt="Construção OSRS"',
    'alt="OSRS Prayer"': 'alt="Oração OSRS"',
    'alt="OSRS Magic"': 'alt="Magia OSRS"',
    'alt="OSRS Ranged"': 'alt="Combate à Distância OSRS"',
    'alt="OSRS Melee"': 'alt="Corpo a Corpo OSRS"',
    'alt="OSRS Combat"': 'alt="Combate OSRS"',
    'alt="OSRS Quest"': 'alt="Missão OSRS"',
    'alt="OSRS Boss"': 'alt="Chefe OSRS"',
    'alt="OSRS Gold"': 'alt="Ouro OSRS"',
    'alt="OSRS Gear"': 'alt="Equipamento OSRS"',
    'alt="OSRS Map"': 'alt="Mapa OSRS"',
    'alt="OSRS Level"': 'alt="Nível OSRS"',
    'alt="OSRS Training"': 'alt="Treinamento OSRS"',
    'alt="OSRS Beginner"': 'alt="Iniciante OSRS"',
    'alt="OSRS Guide"': 'alt="Guia OSRS"',
}

def fix_alt_text(content):
    """P2-1: 修复 alt 文本"""
    count = 0

    # 直接替换已知的 alt 文本
    for old, new in ALT_REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            count += 1

    return content, count

def fix_missing_height(content):
    """P2-2: 为缺少 height 的 img 标签添加 height"""
    count = 0

    # 查找 <img ... width="XXX" 但没有 height= 的标签
    img_pattern = r'<img([^>]*?)width="(\d+)"([^>]*?)>'

    def add_height(match):
        nonlocal count
        before_width = match.group(1)
        width = match.group(2)
        after_width = match.group(3)

        # 检查是否已经有 height
        full_tag = match.group(0)
        if 'height=' in full_tag:
            return full_tag

        # 计算合理的 height (假设 5:3 比例)
        try:
            width_int = int(width)
            height_int = int(width_int * 3 / 5)
            height = str(height_int)

            # 在 > 前插入 height
            new_tag = f'<img{before_width}width="{width}" height="{height}"{after_width}>'
            count += 1
            return new_tag
        except:
            return full_tag

    content = re.sub(img_pattern, add_height, content)

    return content, count

def process_file(filepath):
    """处理单个文件，返回修改后的内容和统计"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    total_count = 0

    # P2-1: 修复 alt 文本
    content, alt_count = fix_alt_text(content)
    total_count += alt_count

    # P2-2: 修复缺少 height 的 img 标签
    content, height_count = fix_missing_height(content)
    total_count += height_count

    return content, total_count, alt_count, height_count

def main():
    if len(sys.argv) < 2:
        print("Uso: python fix_p2_part1_stdout.py <arquivo.html>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo nao encontrado: {filepath}", file=sys.stderr)
        sys.exit(1)

    content, total_count, alt_count, height_count = process_file(filepath)

    # 输出统计到标准错误
    if total_count > 0:
        print(f"[OK] {os.path.basename(filepath)}: {alt_count} alt fixados, {height_count} height adicionados", file=sys.stderr)
    else:
        print(f"[INFO] Nenhuma alteracao necessaria em {os.path.basename(filepath)}", file=sys.stderr)

    # 输出修改后的内容到标准输出
    print(content, end='')

if __name__ == "__main__":
    main()
