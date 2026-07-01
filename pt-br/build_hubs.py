#!/usr/bin/env python3
"""
Build Brazilian Portuguese hub pages from Chinese hub pages.
Reads zh/*.html (excluding index.html), translates Chinese text, fixes links.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
import re
import shutil

BASE = Path("C:/Users/Lenovo/osrs-guide-site")
ZH = BASE / "zh"
PT = BASE / "pt-br"

HUB_MAP = {
    "money-making.html": "lucro.html",
    "skill-training.html": "habilidades.html",
    "quest-guides.html": "missoes.html",
    "boss-guides.html": "chefes.html",
    "membership.html": "membros.html",
    "beginner.html": "iniciante.html",
    "monthly-updates.html": "atualizacoes-mensais.html",
    "weekly-updates.html": "atualizacoes-semanais.html",
    "forum-hot-topics.html": "topicos-populares.html",
    "community.html": "comunidade.html",
}

TRANSLATIONS = {
    # UI text
    "OSRS 赚钱攻略": "OSRS Guias de Lucro",
    "OSRS 技能训练": "OSRS Treinamento de Habilidades",
    "OSRS 任务攻略": "OSRS Guias de Missões",
    "OSRS Boss 攻略": "OSRS Guias de Chefes",
    "OSRS 会员指南": "OSRS Guia de Membros",
    "OSRS 新手攻略": "OSRS Guia para Iniciantes",
    "OSRS 每月更新": "OSRS Atualizações Mensais",
    "OSRS 每周更新": "OSRS Atualizações Semanais",
    "OSRS 论坛热点": "OSRS Tópicos Populares",
    "OSRS 社区": "OSRS Comunidade",
    
    # Navigation
    "首页": "Início",
    "赚钱": "Lucro",
    "技能训练": "Habilidades",
    "任务": "Missões",
    "Boss攻略": "Chefes",
    "会员": "Membros",
    "新手": "Iniciante",
    "每月更新": "Atualizações Mensais",
    "每周更新": "Atualizações Semanais",
    "论坛热点": "Tópicos Populares",
    "社区": "Comunidade",
    "赚钱方法": "Métodos de Lucro",
    
    # Common words
    "攻略": "Guia",
    "指南": "Guia",
    "新手": "Iniciante",
    "完整": "Completo",
    "最佳": "Melhor",
    "方法": "Métodos",
    "赚钱": "Lucro",
    "技能": "Habilidade",
    "训练": "Treinamento",
    "任务": "Missão",
    "Boss": "Chefe",
    "会员": "Membro",
    "每月": "Mensal",
    "每周": "Semanal",
    "论坛": "Fórum",
    "热点": "Populares",
    "社区": "Comunidade",
    "更新": "Atualização",
    "排名": "Ranking",
    "对比": "Comparação",
    "进阶": "Avançado",
    "装备": "Equipamento",
    "快速": "Rápido",
    "终极": "Ultimate",
    "入门": "Introdução",
    "免费": "Grátis",
    "订阅": "Inscrição",
    "按等级": "Por Nível",
    "按类型": "Por Tipo",
    "其他攻略": "Outros Guias",
    "篇攻略": " Guias",
    "更新于": "Atualizado em",
    "覆盖所有等级": "Todos os Níveis",
    "无属性要求": "Sem Requisitos",
    "新手方法": "Métodos para Iniciantes",
    "中级": "Intermediário",
    "高级": "Avançado",
    "铁人方法": "Métodos Ironman",
    "被动方法": "Métodos Passivos",
    "每周 OSRS 赚钱技巧发送到你的邮箱": "Dicas Semanais de Lucro OSRS no Seu Email",
    "每周一封邮件": "Um email por semana",
    "随时可退订": "Cancele quando quiser",
    "爱好者站点": "Site de fãs",
    "与 Jagex Ltd 无关": "Não afiliado à Jagex Ltd",
    
    # Template strings
    "Every guide is free — this one stays free either way.": "Todo guia é gratuito — este continua gratuito de qualquer forma.",
    "No paywalls, no subscriptions.": "Sem paywalls, sem assinaturas.",
    "Early Access Guide Pack": "Pacote de Acesso Antecipado",
    "gives you more:": "te dá mais:",
    "10 Beginner Guides": "10 Guias para Iniciantes",
    "5 Premium Picks": "5 Escolhas Premium",
    "3-Day Early Access": "Acesso Antecipado de 3 Dias",
    "3 New Guides Every Month": "3 Novos Guias Todo Mês",
    "Your purchase includes instant access to everything above": "Sua compra inclui acesso instantâneo a tudo acima",
    "Get the Early Access Guide Pack": "Obtenha o Pacote de Acesso Antecipado",
    "Every guide stays free for everyone, always — no strings attached.": "Todo guia permanece gratuito para todos, sempre — sem compromisso.",
    "Subscribe Free": "Inscreva-se Grátis",
    "Unsubscribe anytime.": "Cancele quando quiser.",
}

def translate_text(text):
    for cn, pt in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        text = text.replace(cn, pt)
    return text

def transform_hub(src_file, dst_name):
    with open(src_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Chinese with Portuguese
    content = translate_text(content)
    
    # Replace lang attribute
    content = content.replace('<html lang="zh">', '<html lang="pt-br">')
    content = content.replace('<html lang="zh-Hans">', '<html lang="pt-br">')
    
    # Fix canonical and hreflang
    content = re.sub(r'https://osrsguru\.com/zh/([^"]+)', r'https://osrsguru.com/pt-br/\1', content)
    content = content.replace('hreflang="zh"', 'hreflang="pt-br"')
    
    # Fix hub links: map zh hub names to pt-br hub names
    for zh_hub, pt_hub in HUB_MAP.items():
        content = content.replace(f'href="{zh_hub}"', f'href="{pt_hub}"')
    
    # Fix logo link to /pt-br/
    content = content.replace('href="/zh/"', 'href="/pt-br/"')
    content = content.replace('href="/zh/"', 'href="/pt-br/"')
    
    # Add language switch to English
    if '<nav id="main-nav">' in content:
        content = content.replace(
            '<nav id="main-nav">',
            '<nav id="main-nav">\n      <a href="../index.html">🇺🇸 English</a>'
        )
    
    # Write output
    dst_path = PT / dst_name
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  [OK] {dst_name}")

if __name__ == '__main__':
    print("Building Brazilian hub pages...")
    for zh_name, pt_name in HUB_MAP.items():
        src = ZH / zh_name
        if src.exists():
            transform_hub(src, pt_name)
        else:
            print(f"  [SKIP] {zh_name} not found")
    print("Done")
