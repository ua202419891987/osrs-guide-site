#!/usr/bin/env python3
"""Simple bulk replace: MVna5 -> MVa5 + update copy text."""
import os, sys

ROOT = r"C:\Users\Lenovo\osrs-guide-site"
DRY = "--dry-run" in sys.argv

count = 0

for dirpath, _, filenames in os.walk(ROOT):
    dp_lower = dirpath.lower()
    # skip CD/WR
    if "crimson-desert" in dp_lower or "windrose" in dp_lower:
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        fpath = os.path.join(dirpath, fn)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
        
        if "MVna5" not in content:
            continue
        
        # Do replacements
        new_content = content.replace("MVna5", "MVa5")
        
        # Update English copy
        new_content = new_content.replace("10 Beginner Guides", "5 Latest Guides")
        new_content = new_content.replace("zero to mid-game in one pack", "early access before anyone else")
        new_content = new_content.replace("5 Premium Picks", "4-Week Exclusive Window")
        new_content = new_content.replace("our most popular expert deep-dives", "guides go free after 4 weeks")
        new_content = new_content.replace("3-Day Early Access", "Profit Finder + Gear Tool")
        new_content = new_content.replace("read new guides before everyone else", "premium tools included in the pack")
        new_content = new_content.replace("3 New Guides Every Month", "New guides added regularly")
        new_content = new_content.replace("and each one fuels us to write faster", "your purchase always includes the latest pack")
        new_content = new_content.replace("Early Access Guide Pack", "Early Access 5-Pack")
        
        # Update Portuguese copy
        new_content = new_content.replace("10 Guias para Iniciantes", "5 Guias Recentes")
        new_content = new_content.replace("do zero ao meio do jogo em um pacote", "acesso antecipado antes de todos")
        new_content = new_content.replace("5 Escolhas Premium", "Janela Exclusiva de 4 Semanas")
        new_content = new_content.replace("nossos guias mais populares", "guias ficam gratis apos 4 semanas")
        new_content = new_content.replace("Acesso Antecipado de 3 Dias", "Profit Finder + Ferramenta de Gear")
        new_content = new_content.replace("leia novos guias antes de todo mundo", "ferramentas premium inclusas no pacote")
        new_content = new_content.replace("3 Novos Guias Todo Mes", "Novos guias adicionados regularmente")
        new_content = new_content.replace("e cada um nos ajuda a escrever mais rapido", "sua compra sempre inclui o pacote mais recente")
        new_content = new_content.replace("Pacote de Acesso Antecipado", "Pacote 5 Antecipado")
        
        if new_content != content:
            count += 1
            rel = os.path.relpath(fpath, ROOT)
            if not DRY:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
            if count <= 20 or DRY:
                print(f"  {'[DRY] ' if DRY else ''}Updated: {rel}")
            elif count == 21 and not DRY:
                print(f"  ... and more")

print(f"\n{'DRY-RUN: ' if DRY else ''}Total files updated: {count}")
