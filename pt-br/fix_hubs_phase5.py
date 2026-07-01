#!/usr/bin/env python3
"""
Phase 5: Final Chinese cleanup for 5 hub pages.
Translates remaining Chinese phrases embedded in Portuguese sentences.
"""

import re
from pathlib import Path

BASE = Path(r"C:\Users\Lenovo\osrs-guide-site\pt-br")

# Precise fixes for each hub page
FIXES = {
    "iniciante.html": [
        # pos=1952: 不管你是刚注册 -> Se você acabou de criar sua
        ("不管你是刚注册", "Se você acabou de criar sua"),
        # pos=1964: 还是 -> ou
        ("还是", "ou"),
        # pos=3786: 概览 -> Visão Geral
        ("概览", "Visão Geral"),
        # pos=6761: 友好 -> amigável
        ("友好", "amigável"),
        # pos=7258: 总览 -> Visão Geral
        ("总览", "Visão Geral"),
        # pos=7657: 买 -> Comprar
        ("买", "Comprar"),
    ],
    "topicos-populares.html": [
        # pos=5815: 操作 -> Operação / Controle
        ("操作", "Operação"),
        # pos=6063-6075: 让Seu手机também能畅玩OSRS -> para que seu celular também rode OSRS sem lag
        ("让Seu手机também能畅玩OSRS", "para que seu celular também rode OSRS sem lag"),
        ("让", "para que "),
        ("手机", "celular"),
        ("能畅玩", "rode bem"),
        # pos=7564: 战 -> de Combate
        ("战", " de Combate"),
        # pos=9113/9917/9923: 亿 -> 100 milhões / 1 bilhão
        ("0亿GP", "0 milhões de GP"),
        ("1亿GP", "100 milhões de GP"),
        ("20亿GP", "2 bilhões de GP"),
        # pos=11459: 房间 -> Sala
        ("房间", "Sala"),
        # pos=14024: 收集 -> Coleta
        ("收集", "Coleta"),
        # pos=15220: 看a更多 -> Ver mais
        ("看a更多", "Ver mais"),
        ("看", "Ver "),
        ("更多", "mais"),
    ],
    "membros.html": [
        # pos=3078/6247/6287/6363/7448/8008/10463: 独占 -> Exclusivo
        ("独占", "Exclusivo"),
        # pos=3482: 什么情况下回本 -> Em que situação o investimento vale a pena
        ("什么情况下回本", "Em que situação vale a pena"),
        # pos=3490: 最优利用 -> Melhor aproveitamento
        ("最优利用", "Melhor aproveitamento"),
        # pos=4392/4409: 最便宜da OSRS Membro方案 -> Plano mais barato de Membro OSRS
        ("最便宜da OSRS Membro方案", "Plano mais barato de Membro OSRS"),
        ("最便宜", "Mais barato"),
        ("方案", "Plano"),
        # pos=5373: 最 -> Mais
        ("最", "Mais "),
        # pos=5970: 旅行 -> Viagem
        ("旅行", "Viagem"),
        # pos=6004: 万 -> mil
        ("100 万", "1 milhão"),
        # pos=6733/6807: 版 -> versão
        ("版", "versão"),
        # pos=7715/7885/8104: 中心 -> Central
        ("中心", "Central"),
        # pos=9941: 用种植收益支付 -> Pagar com lucro de Farming
        ("用种植收益支付", "Pagar com lucro de Farming"),
        # pos=10365: 最便宜方案 -> Plano mais barato
        ("最便宜方案", "Plano mais barato"),
    ],
    "atualizacoes-mensais.html": [
        # pos=6146: 夏季 -> de Verão
        ("夏季", "de Verão"),
        # pos=6409: 傀儡 -> Marionete
        ("傀儡", "Marionete"),
    ],
    "atualizacoes-semanais.html": [
        # pos=3848: 快 -> Buff / Aumento
        ("快", "Aumento"),
        # pos=5896: 傀儡 -> Marionete
        ("傀儡", "Marionete"),
        # pos=6383: 重建 -> Reconstrução
        ("重建", "Reconstrução"),
    ],
}


def fix_page(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    fname = fpath.name
    if fname not in FIXES:
        return 0
    for old, new in FIXES[fname]:
        content = content.replace(old, new)
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        return 1
    return 0


def main():
    total_before = 0
    total_after = 0
    fixed = 0
    for fname in ["iniciante.html", "topicos-populares.html", "membros.html",
                  "atualizacoes-mensais.html", "atualizacoes-semanais.html"]:
        fpath = BASE / fname
        if not fpath.exists():
            print(f"[SKIP] {fname} not found")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        before = len(re.findall(r'[\u4e00-\u9fff]', content))
        total_before += before
        result = fix_page(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            content2 = f.read()
        after = len(re.findall(r'[\u4e00-\u9fff]', content2))
        total_after += after
        if result:
            fixed += 1
            print(f"[OK] {fname}: {before} -> {after}")
        else:
            print(f"[?] {fname}: {before} chars remaining (no matches found)")

    print(f"\n--- Summary ---")
    print(f"Pages fixed : {fixed}/5")
    print(f"Total before : {total_before}")
    print(f"Total after  : {total_after}")
    print(f"Reduction    : {total_before - total_after}")

    # Show remaining
    print(f"\n--- Remaining (if any) ---")
    for fname in ["iniciante.html", "topicos-populares.html", "membros.html",
                  "atualizacoes-mensais.html", "atualizacoes-semanais.html"]:
        fpath = BASE / fname
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        cn = len(re.findall(r'[\u4e00-\u9fff]', content))
        if cn > 0:
            print(f"  {fname}: {cn} chars")
            # Show them
            for m in re.finditer(r'[\u4e00-\u9fff]+', content):
                start = max(0, m.start()-30)
                end = min(len(content), m.end()+30)
                ctx = content[start:end].replace('\n',' ').strip()
                print(f"    [{m.start()}] \"{m.group()}\" -> {ctx[:120]}")


if __name__ == "__main__":
    main()
