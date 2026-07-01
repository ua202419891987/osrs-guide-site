"""
P1 修复脚本 - pt-br 巴西站
修复 6 个 P1 问题
"""
import os
import re
import glob
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(BASE_DIR, "guides")

# ─── 统计计数器 ───
stats = {
    "p1_1_cn_to_pt_files": 0,
    "p1_1_cn_title_replacements": 0,
    "p1_1_cn_summary_replacements": 0,
    "p1_2_canonical_fixes": 0,
    "p1_3_og_tags_added": 0,
    "p1_4_chinese_to_chines_files": 0,
    "p1_4_replacements": 0,
    "p1_5_double_dash_files": 0,
    "p1_5_replacements": 0,
    "p1_6_concat_fixes": 0,
}

# ═══════════════════════════════════════════════════════
# P1-1: cn-title/cn-summary → pt-title/pt-summary
# ═══════════════════════════════════════════════════════
def fix_p1_1():
    print("─── P1-1: cn-title/cn-summary → pt-title/pt-summary ───")
    html_files = glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    for fpath in html_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        original = content
        # Replace cn-title → pt-title
        cnt_title = content.count("cn-title")
        content = content.replace("cn-title", "pt-title")
        stats["p1_1_cn_title_replacements"] += cnt_title
        # Replace cn-summary → pt-summary
        cnt_summary = content.count("cn-summary")
        content = content.replace("cn-summary", "pt-summary")
        stats["p1_1_cn_summary_replacements"] += cnt_summary
        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["p1_1_cn_to_pt_files"] += 1
    print(f"  修复文件: {stats['p1_1_cn_to_pt_files']}")
    print(f"  cn-title → pt-title: {stats['p1_1_cn_title_replacements']} 次")
    print(f"  cn-summary → pt-summary: {stats['p1_1_cn_summary_replacements']} 次")

# ═══════════════════════════════════════════════════════
# P1-2: 9 个 hub canonical 英文→葡语文件名
# ═══════════════════════════════════════════════════════
CANONICAL_MAP = {
    "chefes.html": ("/pt-br/boss-guides.html", "/pt-br/chefes.html"),
    "habilidades.html": ("/pt-br/skill-training.html", "/pt-br/habilidades.html"),
    "iniciante.html": ("/pt-br/beginner.html", "/pt-br/iniciante.html"),
    "lucro.html": ("/pt-br/money-making.html", "/pt-br/lucro.html"),
    "membros.html": ("/pt-br/membership.html", "/pt-br/membros.html"),
    "missoes.html": ("/pt-br/quest-guides.html", "/pt-br/missoes.html"),
    "atualizacoes-mensais.html": ("/pt-br/monthly-updates.html", "/pt-br/atualizacoes-mensais.html"),
    "atualizacoes-semanais.html": ("/pt-br/weekly-updates.html", "/pt-br/atualizacoes-semanais.html"),
    "topicos-populares.html": ("/pt-br/forum-hot-topics.html", "/pt-br/topicos-populares.html"),
}

def fix_p1_2():
    print("─── P1-2: Hub canonical 英文→葡语 ───")
    for filename, (old_slug, new_slug) in CANONICAL_MAP.items():
        fpath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(fpath):
            print(f"  ⚠ 文件不存在: {filename}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        old_canonical = f'https://osrsguru.com{old_slug}'
        new_canonical = f'https://osrsguru.com{new_slug}'
        if old_canonical in content:
            content = content.replace(old_canonical, new_canonical)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["p1_2_canonical_fixes"] += 1
            print(f"  ✓ {filename}: {old_slug} → {new_slug}")
        else:
            print(f"  ⚠ {filename}: 未找到旧 canonical '{old_canonical}'，可能已修复")
    print(f"  修复总数: {stats['p1_2_canonical_fixes']}")

# ═══════════════════════════════════════════════════════
# P1-3: 7 个 hub 页面缺 OG 标签
# ═══════════════════════════════════════════════════════
OG_HUB_FILES = [
    "chefes.html", "habilidades.html", "iniciante.html",
    "lucro.html", "membros.html", "missoes.html", "comunidade.html",
]

def extract_h1(content):
    """提取页面 h1 标题文本"""
    match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if match:
        text = match.group(1)
        # 去掉 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()
    return ""

def extract_meta_description(content):
    """提取 meta description 内容"""
    match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content)
    if match:
        return match.group(1).strip()
    return ""

def fix_p1_3():
    print("─── P1-3: Hub 页面添加 OG 标签 ───")
    for filename in OG_HUB_FILES:
        fpath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(fpath):
            print(f"  ⚠ 文件不存在: {filename}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查是否已有 OG 标签
        if 'og:title' in content:
            print(f"  ⚠ {filename}: 已有 OG 标签，跳过")
            continue

        h1 = extract_h1(content)
        desc = extract_meta_description(content)
        og_url = f"https://osrsguru.com/pt-br/{filename}"

        og_block = f"""<meta property="og:title" content="{h1}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="website">"""

        # 插入到 canonical 行后面
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="[^"]*"[^>]*>\n?', content)
        if canonical_match:
            insert_pos = canonical_match.end()
            content = content[:insert_pos] + "\n" + og_block + "\n" + content[insert_pos:]
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["p1_3_og_tags_added"] += 1
            print(f"  ✓ {filename}: OG 标签已添加 (h1='{h1}', desc='{desc[:40]}...')")
        else:
            print(f"  ⚠ {filename}: 未找到 canonical 标签，无法插入 OG")
    print(f"  修复总数: {stats['p1_3_og_tags_added']}")

# ═══════════════════════════════════════════════════════
# P1-4: 导航 "Chinese" → "Chinês"
# ═══════════════════════════════════════════════════════
def fix_p1_4():
    print("─── P1-4: 'Chinese' → 'Chinês' (导航链接) ───")
    # 搜索所有 HTML 文件中的 <a href="../zh/index.html">Chinese</a> 和变体
    all_html = glob.glob(os.path.join(BASE_DIR, "*.html"))
    all_html += glob.glob(os.path.join(GUIDES_DIR, "*.html"))

    for fpath in all_html:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        # 匹配各种变体: href="../zh/index.html">Chinese, href="../zh/">Chinese, 等
        # 主要模式: 链接文本为 "Chinese" (不是内容中的 "Chinese Glossary" 等)
        patterns = [
            # <a href="../zh/index.html">Chinese</a> (with optional style attr)
            (r'<a\s+href="../zh/index\.html"[^>]*>Chinese</a>', r'<a href="../zh/index.html">Chinês</a>'),
            # <a href="../zh/">Chinese</a>
            (r'<a\s+href="../zh/">Chinese</a>', r'<a href="../zh/">Chinês</a>'),
            # <a href="../../zh/index.html">Chinese</a>
            (r'<a\s+href="../../zh/index\.html"[^>]*>Chinese</a>', r'<a href="../../zh/index.html">Chinês</a>'),
            # Versão Chinesa / Versão Chinese patterns in footer
            (r'Versão Chinese', r'Versão Chinesa'),
        ]

        replaced = False
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                count_diff = len(re.findall(pattern, content))
                stats["p1_4_replacements"] += count_diff
                content = new_content
                replaced = True

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["p1_4_chinese_to_chines_files"] += 1
            fname = os.path.relpath(fpath, BASE_DIR)
            print(f"  ✓ {fname}")

    print(f"  修复文件: {stats['p1_4_chinese_to_chines_files']}")
    print(f"  替换次数: {stats['p1_4_replacements']}")

# ═══════════════════════════════════════════════════════
# P1-5: "——" → "—" (双 em-dash → 单)
# ═══════════════════════════════════════════════════════
def fix_p1_5():
    print("─── P1-5: '——' (双em-dash) → '—' (单em-dash) ───")
    all_html = glob.glob(os.path.join(BASE_DIR, "*.html"))
    all_html += glob.glob(os.path.join(GUIDES_DIR, "*.html"))

    for fpath in all_html:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        count = content.count("\u2014\u2014")  # ——
        if count > 0:
            content = content.replace("\u2014\u2014", "\u2014")  # —— → —
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["p1_5_double_dash_files"] += 1
            stats["p1_5_replacements"] += count
            fname = os.path.relpath(fpath, BASE_DIR)
            print(f"  ✓ {fname}: {count} 处")

    print(f"  修复文件: {stats['p1_5_double_dash_files']}")
    print(f"  替换次数: {stats['p1_5_replacements']}")

# ═══════════════════════════════════════════════════════
# P1-6: Hub 页面单词拼接修复
# ═══════════════════════════════════════════════════════
CONCAT_MAP = {
    "CompletoJadVorkath": "Completo: Jad, Vorkath",
    "InicianteCompletoGuia": "Guia Completo para Iniciantes",
    "F2PLucro": "Lucro F2P",
    "MembroExclusivoda": "Exclusivo para Membros:",
    "MembroeGrátisversãoConteúdo": "Comparação entre versão Membro e Grátis",
    "PureConta": "Conta Pure",
    "Purede nívelRota": "Rota de nível para Pure",
    "IniciantedaMétodos": "Métodos para Iniciantes",
}

# 特殊: chefes.html meta description 中 "CompletoJadVorkathZulrahRaid" 也需要修复
# 它是 "CompletoJadVorkath" + "Zulrah" + "Raid" 拼在一起的
# 先修 CompletoJadVorkath → Completo: Jad, Vorkath，剩下 ZulrahRaid 也需要处理

# Also need to handle compound cases where concatenation has more parts merged
EXTRA_CONCAT_MAP = {
    "CompletoJadVorkathZulrahRaid": "Completo: Jad, Vorkath, Zulrah, Raid",
    "Iniciante4Crescimento semanalRota": "Rota de Crescimento Semanal para Iniciantes",
    "Iniciante4RotaMembroGuia": "Guia de Rota para Iniciantes e Membros",
    "Guia de Lucro PvM F2P MembroIniciante": "Guia de Lucro PvM: F2P, Membro, Iniciante",
    "MembroComparaçãoBond vs InscriçãoDicas": "Comparação de Membros: Bond vs Inscrição e Dicas",
    "MissãoGuiaIniciante Dragon Slayer 2Missão": "Guia de Missão: Iniciante, Dragon Slayer 2 e outras Missões",
}

def fix_p1_6():
    print("─── P1-6: Hub 页面单词拼接修复 ───")
    # 只处理 hub 页面 (9个)
    hub_files = [
        "chefes.html", "habilidades.html", "iniciante.html",
        "lucro.html", "membros.html", "missoes.html",
        "atualizacoes-mensais.html", "atualizacoes-semanais.html",
        "topicos-populares.html",
    ]

    total_fixes = 0

    for filename in hub_files:
        fpath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(fpath):
            print(f"  ⚠ 文件不存在: {filename}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        # 先处理 EXTRA (更长的拼接), 再处理标准拼接
        for old, new in EXTRA_CONCAT_MAP.items():
            if old in content:
                content = content.replace(old, new)
                total_fixes += 1
                print(f"  ✓ {filename}: '{old}' → '{new}'")

        for old, new in CONCAT_MAP.items():
            if old in content:
                content = content.replace(old, new)
                total_fixes += 1
                print(f"  ✓ {filename}: '{old}' → '{new}'")

        # 额外修复: iniciante.html h1 中的 "Iniciante4" 拼接
        # 其他残留拼接词
        extra_fixes = {
            "Habilidade 1-99 Guia de TreinamentoMineração": "Habilidade 1-99: Guia de Treinamento — Mineração",
            "Métodos mais eficientes": "Métodos mais eficientes",  # no change needed, just verify
            "OSRS FórumPopularGuia": "OSRS Fórum Popular Guia",
            "RedditTiebaNGAFórum": "Reddit, Tieba, NGA — Fórum",
            "PvPEquipamentoAvançadoIntroduçãoHabilidade": "PvP, Equipamento Avançado, Introdução, Habilidade",
            "ComparaçãoMembroeGrátisversãoConteúdo": "Comparação entre versão Membro e Grátis — Conteúdo",
            "Todos os tiposPurede nívelRota": "Todos os tipos: Rota de nível para Pure",
            "MissãoEscolha eEquipamentoAnálise completa de combinações": "Missão: Escolha e Equipamento — Análise completa de combinações",
        }

        for old, new in extra_fixes.items():
            if old != new and old in content:
                content = content.replace(old, new)
                total_fixes += 1
                print(f"  ✓ {filename}: '{old}' → '{new}'")

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["p1_6_concat_fixes"] += total_fixes

    print(f"  修复总数: {stats['p1_6_concat_fixes']}")

# ═══════════════════════════════════════════════════════
# 验证
# ═══════════════════════════════════════════════════════
def verify():
    print("\n─── 验证 ───")

    # V1: cn-title/cn-summary 应为 0
    all_html = glob.glob(os.path.join(BASE_DIR, "*.html"))
    all_html += glob.glob(os.path.join(GUIDES_DIR, "*.html"))
    cn_count = 0
    for fpath in all_html:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        if "cn-title" in c or "cn-summary" in c:
            cn_count += 1
    print(f"  cn-title/cn-summary 残留文件数: {cn_count} (应为 0)")

    # V2: "Chinese" 在导航链接中应为 0
    chinese_nav_count = 0
    for fpath in all_html:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        # 只检查链接文本中的 Chinese
        if re.search(r'<a[^>]*href="[^"]*zh[^"]*"[^>]*>Chinese</a>', c):
            chinese_nav_count += 1
    print(f"  导航链接 'Chinese' 残留文件数: {chinese_nav_count} (应为 0)")

    # V3: 双em-dash 应为 0
    dash_count = 0
    for fpath in all_html:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        if "\u2014\u2014" in c:
            dash_count += 1
    print(f"  双em-dash (——) 残留文件数: {dash_count} (应为 0)")

    # V4: 抽查 3 个 hub canonical
    print("  抽查 canonical:")
    for fn in ["chefes.html", "habilidades.html", "missoes.html"]:
        fpath = os.path.join(BASE_DIR, fn)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', c)
        if match:
            print(f"    {fn}: {match.group(1)}")

    # V5: OG 标签抽查
    print("  抽查 OG 标签:")
    for fn in ["chefes.html", "membros.html", "comunidade.html"]:
        fpath = os.path.join(BASE_DIR, fn)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        og_title = re.search(r'og:title.*content="([^"]*)"', c)
        og_type = re.search(r'og:type.*content="([^"]*)"', c)
        if og_title and og_type:
            print(f"    {fn}: og:title='{og_title.group(1)[:30]}...', og:type='{og_type.group(1)}'")
        else:
            print(f"    {fn}: ⚠ 缺少 OG 标签")

# ═══════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("pt-br P1 修复脚本")
    print("=" * 60)

    fix_p1_1()
    fix_p1_2()
    fix_p1_3()
    fix_p1_4()
    fix_p1_5()
    fix_p1_6()

    print("\n" + "=" * 60)
    print("修复完成，开始验证")
    print("=" * 60)
    verify()

    print("\n✅ 全部完成")
