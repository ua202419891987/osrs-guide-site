import os
import glob

alt_replacements = {
    'OSRS Mining Guide': 'Guia de Mineração OSRS',
    'OSRS Woodcutting': 'Corte de Lenha OSRS',
    'OSRS Fishing': 'Pesca OSRS',
    'OSRS Firemaking': 'Arte do Fogo OSRS',
    'OSRS Cooking': 'Culinária OSRS',
    'OSRS Crafting': 'Artesanato OSRS',
    'OSRS Smithing': 'Ferraria OSRS',
    'OSRS Herblore': 'Herbologia OSRS',
    'OSRS Fletching': 'Arqueação OSRS',
    'OSRS Runecrafting': 'Criação de Runas OSRS',
    'OSRS Thieving': 'Roubo OSRS',
    'OSRS Agility': 'Agilidade OSRS',
    'OSRS Hunter': 'Caça OSRS',
    'OSRS Slayer': 'Extermínio OSRS',
    'OSRS Farming': 'Agricultura OSRS',
    'OSRS Construction': 'Construção OSRS',
    'OSRS Prayer': 'Oração OSRS',
    'OSRS Magic': 'Magia OSRS',
    'OSRS Ranged': 'Combate à Distância OSRS',
    'OSRS Melee': 'Corpo a Corpo OSRS',
    'OSRS Combat': 'Combate OSRS',
    'OSRS Quest': 'Missão OSRS',
    'OSRS Boss': 'Chefe OSRS',
    'OSRS Gold': 'Ouro OSRS',
    'OSRS Gear': 'Equipamento OSRS',
    'OSRS Map': 'Mapa OSRS',
    'OSRS Guide': 'Guia OSRS',
    'OSRS Training': 'Treinamento OSRS',
    'OSRS Beginner': 'Iniciante OSRS',
}

total_replacements = 0
files_modified = 0

for filepath in glob.glob('guides/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for eng, pt in alt_replacements.items():
        # exact match within alt="..."
        search = f'alt="{eng}"'
        replace = f'alt="{pt}"'
        count = content.count(search)
        if count > 0:
            content = content.replace(search, replace)
            total_replacements += count

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_modified += 1

print(f"Alt text replacements: {total_replacements}")
print(f"Files modified: {files_modified}")
