#!/usr/bin/env python3
"""Fix 8 guides with 🔓 unlock-style support cards + 6 hub pages with English residues"""

import glob
import os

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\pt-br\guides"

# The 8 files using 🔓 style
FILES = [
    "osrs-1-99-prayer-guide-2026.html",
    "osrs-1-99-thieving-guide-ironman.html",
    "osrs-1-99-woodcutting-guide-early-game.html",
    "osrs-agility-training-guide-2026.html",
    "osrs-all-skills-overview-guide-2026.html",
    "osrs-best-quests-per-skill-2026.html",
    "osrs-cheapest-99-runecrafting-2026.html",
    "osrs-combat-training-beginner-2026.html",
]

# Replacements for 🔓 style support cards
REPLACEMENTS = [
    # H3 title
    ('<h3>.</h3>', '<h3>Todo guia é gratuito — este continua gratuito de qualquer forma.</h3>'),
    # Intro paragraph
    ('No paywalls, no subscriptions. But the <strong>Pacote de Acesso Antecipado</strong> gives you more:', 
     'Sem paywalls, sem assinaturas. Mas o <strong>Pacote de Acesso Antecipado</strong> te dá mais:'),
    # Bullet 1
    ('📚 <strong>10 Beginner Guides</strong> — zero to mid-game in one pack', 
     '📚 <strong>10 Guias para Iniciantes</strong> — do zero ao meio do jogo em um pacote'),
    # Bullet 2
    ('⭐ <strong>5 Premium Picks</strong> — our most popular expert deep-dives', 
     '⭐ <strong>5 Escolhas Premium</strong> — nossos guias mais populares'),
    # Bullet 3
    ('⏰ <strong>3-Day Early Access</strong> — read new guides before everyone else', 
     '⏰ <strong>Acesso Antecipado de 3 Dias</strong> — leia novos guias antes de todo mundo'),
    # Bullet 4
    ('🔄 <strong>3 New Guides Every Month</strong> — and each one fuels us to write faster', 
     '🔄 <strong>3 Novos Guias Todo Mês</strong> — e cada um nos ajuda a escrever mais rápido'),
    # Purchase text
    ('✅ Sua compra inclui acesso instantâneo a tudo acima', None),  # already PT
    # Bottom disclaimer
    ('Every guide stays free for everyone, always — no strings attached. 🤝', 
     'Todo guia permanece gratuito para todos, sempre — sem compromisso. 🤝'),
]

fixed = 0
for fname in FILES:
    fpath = os.path.join(GUIDES_DIR, fname)
    if not os.path.exists(fpath):
        print(f"  ⚠️ Not found: {fname}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in REPLACEMENTS:
        if new and old in content:
            content = content.replace(old, new)
            modified = True
    
    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {fname}")
        fixed += 1
    else:
        print(f"  ⏭️ {fname} (no changes needed)")

print(f"\n📊 Guides fixed: {fixed}/{len(FILES)}")

# Now fix hub pages
HUB_DIR = r"C:\Users\Lenovo\osrs-guide-site\pt-br"
HUBS = ["chefes.html", "missoes.html", "iniciante.html", "habilidades.html", "lucro.html", "membros.html"]

hub_fixed = 0
for h in HUBS:
    hpath = os.path.join(HUB_DIR, h)
    with open(hpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    if 'read new guides before everyone else' in content:
        content = content.replace('read new guides before everyone else', 'leia novos guias antes de todo mundo')
        modified = True
    if '3 New Guides Every Month' in content:
        content = content.replace('3 New Guides Every Month', '3 Novos Guias Todo Mês')
        modified = True
    if 'Early Access Guide Pack' in content:
        content = content.replace('Early Access Guide Pack', 'Pacote de Acesso Antecipado')
        modified = True
    if 'No paywalls, no subscriptions.' in content:
        content = content.replace('No paywalls, no subscriptions.', 'Sem paywalls, sem assinaturas.')
        modified = True
    if 'Your purchase includes instant access' in content:
        content = content.replace('Your purchase includes instant access to everything above', 'Sua compra inclui acesso instantâneo a tudo acima')
        modified = True
    if 'Every guide stays free for everyone' in content:
        content = content.replace('Every guide stays free for everyone, always — no strings attached. 🤝', 'Todo guia permanece gratuito para todos, sempre — sem compromisso. 🤝')
        modified = True
    if 'Get the Early Access' in content:
        content = content.replace('Get the Early Access Guia Pack', 'Obtenha o Pacote de Acesso Antecipado')
        content = content.replace('Get the Early Access Guide Pack', 'Obtenha o Pacote de Acesso Antecipado')
        modified = True
    
    if modified:
        with open(hpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Hub: {h}")
        hub_fixed += 1
    else:
        print(f"  ⏭️ Hub: {h} (no changes)")

print(f"\n📊 Hub pages fixed: {hub_fixed}/{len(HUBS)}")
