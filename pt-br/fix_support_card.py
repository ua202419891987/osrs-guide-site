#!/usr/bin/env python3
"""Batch translate English support cards to Portuguese in pt-br/guides/"""

import os
import re
import glob

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\pt-br\guides"

# Portuguese support card template
PT_CARD = """            <h3>Todo guia é gratuito — este continua gratuito de qualquer forma.</h3>
            <p>Sem paywalls, sem assinaturas. Mas o <strong>Pacote de Acesso Antecipado</strong> te dá mais:</p>
            <p style="margin:6px 0 0 0;line-height:1.7">
                📚 <strong>10 Guias para Iniciantes</strong> — do zero ao meio do jogo em um pacote<br>
                ⭐ <strong>5 Escolhas Premium</strong> — nossos guias mais populares<br>
                ⏰ <strong>Acesso Antecipado de 3 Dias</strong> — leia novos guias antes de todo mundo<br>
                🔄 <strong>3 Novos Guias Todo Mês</strong> — e cada um nos ajuda a escrever mais rápido
            </p>
            <p style="font-size:14px;margin:12px 0 0 0;opacity:0.85">✅ Sua compra inclui acesso instantâneo a tudo acima</p>
            <div class="support-amounts">
                <a href="https://www.paypal.com/paypalme/osrsguru/1.9" target="_blank" rel="noopener" class="support-amount-btn recommended">$1.90 — Obtenha o Pacote de Acesso Antecipado 👑</a>
            </div>
            <p style="font-size:14px;margin:6px 0 0 0;opacity:0.85">Todo guia permanece gratuito para todos, sempre — sem compromisso. 🤝</p>"""

# Patterns to match (the entire English support card block)
# Pattern 1: with dash "Every guide is free — this one stays free either way."
PATTERN1_START = '<h3>Every guide is free — this one stays free either way.</h3>'
PATTERN1_END = 'no strings attached. 🤝</p>'

# Pattern 2: without dash "Every guide is free this one stays free either way."
PATTERN2_START = '<h3>Every guide is free this one stays free either way.</h3>'
# Same end pattern

# Also need to replace the button text "Get the Early Access Guia Pack" -> "Obtenha o Pacote de Acesso Antecipado"
# And "Early Access Guide Pack" -> "Pacote de Acesso Antecipado" in other parts


def replace_support_card(content):
    """Replace English support card with Portuguese version"""
    modified = False
    
    # Pattern 1: with dash
    start_idx = content.find(PATTERN1_START)
    if start_idx == -1:
        # Pattern 2: without dash
        start_idx = content.find(PATTERN2_START)
    
    if start_idx != -1:
        # Find the end of the support card block
        end_idx = content.find(PATTERN1_END, start_idx)
        if end_idx != -1:
            end_idx += len(PATTERN1_END)
            # Replace entire block
            content = content[:start_idx] + PT_CARD + content[end_idx:]
            modified = True
    
    return content, modified


def main():
    html_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    total = len(html_files)
    fixed = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, modified = replace_support_card(content)
        
        # Also fix any remaining "Early Access Guia Pack" button text
        old_btn = 'Get the Early Access Guia Pack'
        new_btn = 'Obtenha o Pacote de Acesso Antecipado'
        if old_btn in new_content:
            new_content = new_content.replace(old_btn, new_btn)
            modified = True
        
        # And "Early Access Guide Pack" in paragraph text
        old_pack = 'Early Access Guide Pack'
        new_pack = 'Pacote de Acesso Antecipado'
        if old_pack in new_content:
            new_content = new_content.replace(old_pack, new_pack)
            modified = True
        
        # "Your purchase includes instant access" -> Portuguese
        old_purchase = '✅ Your purchase includes instant access to everything above'
        new_purchase = '✅ Sua compra inclui acesso instantâneo a tudo acima'
        if old_purchase in new_content:
            new_content = new_content.replace(old_purchase, new_purchase)
            modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            basename = os.path.basename(filepath)
            print(f"  ✅ {basename}")
        else:
            skipped += 1
    
    print(f"\n📊 Results: {fixed} fixed, {skipped} skipped, {total} total")

if __name__ == "__main__":
    main()
