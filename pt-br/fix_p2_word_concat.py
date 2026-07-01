#!/usr/bin/env python3
"""P2: Fix word concatenation, 30S preview mismatch, cn- class names, hreflang, og:url."""
import re
from pathlib import Path

BASE = Path(r'C:\Users\Lenovo\osrs-guide-site\pt-br')
GUIDES = BASE / 'guides'

# ============================================================
# 1. Fix word concatenation patterns across all hub pages
# ============================================================
WORD_FIXES = {
    'Investimentoimento': 'Investimento',
    'Combatee': 'Combate',
    'Habilidadee': 'Habilidade',
    'Recompensasa': 'Recompensas',
    'Equipamentoento': 'Equipamento',
    'Iniciantee': 'Iniciante',
    'Avancadoo': 'Avancado',
    'Completotao': 'Completo',
    'Guiaa': 'Guia',
    'Melhorr': 'Melhor',
    'Conquistasa': 'Conquistas',
    'Missaoao': 'Missao',
    'Chefee': 'Chefe',
    'Tesouroo': 'Tesouro',
    'Magiaa': 'Magia',
    'Flechaas': 'Flechas',
    'Arcoo': 'Arco',
    'Espadaa': 'Espada',
    'Escudoo': 'Escudo',
    'Armaduraa': 'Armadura',
    'Pocaoao': 'Pocao',
    'Jogadorr': 'Jogador',
    'Mercadoo': 'Mercado',
}

FIXED_WORDS = 0

for html_file in sorted(BASE.rglob('*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for wrong, correct in WORD_FIXES.items():
        content = content.replace(wrong, correct)

    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        rel = html_file.relative_to(BASE)
        print(f'  WORD: {rel}')

        # Count actual fixes
        for wrong in WORD_FIXES:
            if wrong in original:
                FIXED_WORDS += original.count(wrong)

# ============================================================
# 2. Fix specific article issues
# ============================================================

# 2a. cn-title / cn-summary class names in slayer-beginner
slayer_path = GUIDES / 'osrs-slayer-beginner-guide-2026.html'
if slayer_path.exists():
    with open(slayer_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = content.replace('cn-title', 'guide-title')
    content = content.replace('cn-summary', 'guide-summary')
    if content != original:
        with open(slayer_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  CLASS: osrs-slayer-beginner-guide-2026 (cn-title/cn-summary)')

# 2b. Fix 30S preview in gear-upgrade (was describing GE flipping, not gear upgrade)
gear_path = GUIDES / 'osrs-gear-upgrade-priority-order-2026.html'
if gear_path.exists():
    with open(gear_path, 'r', encoding='utf-8') as f:
        content = f.read()
    old_preview = 'os melhores metodos de lucro'
    new_preview = 'a ordem de prioridade para upgrades de equipamento'
    if old_preview in content:
        content = content.replace(old_preview, new_preview)
        with open(gear_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  PREVIEW: gear-upgrade (fixed 30S preview)')

# 2c. Fix hreflang in blood-moon
blood_path = GUIDES / 'osrs-blood-moon-rises-guide-2026.html'
if blood_path.exists():
    with open(blood_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Fix hreflang pointing to English URL
    old_hreflang = 'hreflang="en" href="https://osrsguru.com/guides/osrs-blood-moon-rises-guide-2026.html"'
    new_hreflang = 'hreflang="pt-BR" href="https://osrsguru.com/pt-br/guides/osrs-blood-moon-rises-guide-2026.html"'
    if old_hreflang in content:
        content = content.replace(old_hreflang, new_hreflang)
        with open(blood_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  HREFLANG: blood-moon-rises (en->pt-BR)')

# 2d. Fix og:url in first-week-progression
firstweek_path = GUIDES / 'osrs-first-week-progression-guide-2026.html'
if firstweek_path.exists():
    with open(firstweek_path, 'r', encoding='utf-8') as f:
        content = f.read()
    old_og = 'og:url" content="https://osrsguru.com/guides/osrs-first-week-progression-guide-2026.html'
    new_og = 'og:url" content="https://osrsguru.com/pt-br/guides/osrs-first-week-progression-guide-2026.html'
    if old_og in content:
        content = content.replace(old_og, new_og)
        with open(firstweek_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  OGURL: first-week-progression (en->pt-br)')

# 2e. Fix og:description CJK punctuation in money-making-beginner
money_path = GUIDES / 'osrs-money-making-beginner-2026.html'
if money_path.exists():
    with open(money_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # P0 should have already fixed CJK punct, but double-check
    cn_punct = re.findall(r'[\u3000-\u303f\uff00-\uffef]', content)
    if cn_punct:
        print(f'  WARN: money-making-beginner still has {len(cn_punct)} CJK punct')

print(f'\nDone! Word fixes: {FIXED_WORDS}')
