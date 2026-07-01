#!/usr/bin/env python3
"""
P2 Phase 1 Batch Fix Script - Single File Version
修复 pt-br 站的 P2 问题：
- P2-1: 英文 alt 文本 → 葡语
- P2-2: img 缺 height → 加 height

用法: python fix_p2_part1.py <arquivo.html>
"""

import os
import re
import sys
import glob

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
    """处理单个文件"""
    filename = os.path.basename(filepath)

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

    # 如果有修改，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return total_count, alt_count, height_count

    return 0, 0, 0

def main():
    if len(sys.argv) < 2:
        print("Uso: python fix_p2_part1.py <arquivo.html>")
        print("Ou: python fix_p2_part1.py --all  (para processar todos os arquivos em pt-br/guides/)")
        sys.exit(1)

    if sys.argv[1] == '--all':
        # 处理所有文件
        guides_dir = r"C:\Users\Lenovo\osrs-guide-site\pt-br\guides"
        guide_files = glob.glob(os.path.join(guides_dir, "*.html"))

        total_files_modified = 0
        total_alt_fixed = 0
        total_height_fixed = 0

        print("Processando todos os arquivos em pt-br/guides/...")
        for filepath in guide_files:
            filename = os.path.basename(filepath)
            result = process_file(filepath)

            if result[0] > 0:
                total_files_modified += 1
                total_alt_fixed += result[1]
                total_height_fixed += result[2]
                print(f"  [OK] {filename}: {result[1]} alt fixados, {result[2]} height adicionados")

        print("\n" + "=" * 60)
        print("Resumo das Correcoes")
        print("=" * 60)
        print(f"Arquivos modificados: {total_files_modified}")
        print(f"Alt texts traduzidos: {total_alt_fixed}")
        print(f"Img heights adicionados: {total_height_fixed}")
        print("=" * 60)
    else:
        # 处理单个文件
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"Erro: Arquivo nao encontrado: {filepath}")
            sys.exit(1)

        result = process_file(filepath)
        if result[0] > 0:
            print(f"[OK] {os.path.basename(filepath)}: {result[1]} alt fixados, {result[2]} height adicionados")
        else:
            print(f"[INFO] Nenhuma alteracao necessaria em {os.path.basename(filepath)}")

if __name__ == "__main__":
    main()
