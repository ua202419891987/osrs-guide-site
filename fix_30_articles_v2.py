#!/usr/bin/env python3
"""
批量修复30篇OSRS新手攻略的格式问题
"""

import re
import os

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

TARGET_FILES = [
    "osrs-money-making-beginner-2026.html",
    "osrs-new-player-guide-2026.html",
    "osrs-slayer-beginner-guide-2026.html",
    "osrs-money-making-zero-req-2026.html",
    "osrs-1-99-prayer-guide-2026.html",
    "osrs-barrows-tunnel-optimization-2026.html",
    "osrs-f2p-gear-progression-guide-2026.html",
    "osrs-diary-priority-order-beginner-2026.html",
    "osrs-clue-scrolls-beginner-guide-2026.html",
    "osrs-common-beginner-mistakes-avoid-2026.html",
    "osrs-combat-training-beginner-2026.html",
    "osrs-prayer-training-beginner-guide-2026.html",
    "osrs-1-99-mining-guide-beginner-2026.html",
    "osrs-1-99-farming-guide-beginner-profit-2026.html",
    "osrs-1-99-woodcutting-guide-early-game.html",
    "osrs-farming-herb-runs-beginner-guide-2026.html",
    "osrs-skill-training-beginner-complete-guide-2026.html",
    "osrs-skill-training-beginner-fast-track-2026.html",
    "osrs-efficient-training-routes-beginners-2026.html",
    "osrs-low-level-skilling-money-makers-2026.html",
    "osrs-f2p-combat-training-guide-2026.html",
    "osrs-f2p-leveling-guide-2026.html",
    "osrs-f2p-money-making-first-bond-2026.html",
    "osrs-f2p-money-making-no-stats.html",
    "osrs-f2p-quests-before-membership-2026.html",
    "osrs-f2p-slayer-guide-2026.html",
    "osrs-f2p-to-member-first-10-things-2026.html",
    "osrs-first-boss-progression-roadmap-2026.html",
    "osrs-flipping-guide-beginners-2026.html",
    "osrs-gear-beginner-guide-2026.html",
]

CSS_OVERRIDE = """<style>
.guide-content{color:#1a1a1a!important}
.guide-content li,.guide-content p,.guide-content td,.guide-content th,.guide-content h3,.guide-content h4{color:#1a1a1a!important}
.guide-content .tip-box,.guide-content .method-box,.guide-content .action-step,.guide-content .quick-verdict,.guide-content .faq-item,.guide-content .warning-box,.guide-content .info-box,.guide-content .pro-tip-box,.guide-content .note-box,.guide-content .highlight-box,.guide-content .strategy-box,.guide-content .gear-box,.guide-content .setup-box,.guide-content .location-box,.guide-content .next-steps,.guide-content .bond-roadmap{background:#fff!important;border:1px solid #e0d5c0!important}
.guide-content .tip-box p,.guide-content .tip-box li,.guide-content .method-box p,.guide-content .method-box li,.guide-content .faq-item p,.guide-content .faq-item li,.guide-content .quick-verdict p,.guide-content .action-step p,.guide-content .warning-box p,.guide-content .warning-box li,.guide-content .info-box p,.guide-content .info-box li,.guide-content .pro-tip-box p,.guide-content .pro-tip-box li,.guide-content .note-box p,.guide-content .note-box li,.guide-content .highlight-box p,.guide-content .highlight-box li,.guide-content .strategy-box p,.guide-content .strategy-box li,.guide-content .gear-box p,.guide-content .gear-box li,.guide-content .setup-box p,.guide-content .setup-box li,.guide-content .location-box p,.guide-content .location-box li,.guide-content .next-steps p,.guide-content .next-steps li,.guide-content .bond-roadmap p,.guide-content .bond-roadmap li{color:#1a1a1a!important}
.guide-content .faq-item h3,.guide-content .faq-item h4,.guide-content .method-box h3,.guide-content .method-box h4,.guide-content .quick-verdict h3,.guide-content .action-step h4,.guide-content .tip-box strong,.guide-content .method-box strong,.guide-content .warning-box strong,.guide-content .info-box strong,.guide-content .pro-tip-box strong,.guide-content .note-box strong,.guide-content .highlight-box strong,.guide-content .strategy-box strong,.guide-content .gear-box strong,.guide-content .setup-box strong,.guide-content .location-box strong,.guide-content .next-steps strong,.guide-content .bond-roadmap strong{color:#3b2615!important}
.guide-content [style*="border-left:4px"],.guide-content [style*="border-left: 4px"],.guide-content [style*="border-left:3px"],.guide-content [style*="border-left: 3px"]{border-left:0!important}
.guide-content .related-guides .article-card{background:#f5f2f8!important;border-color:#D4CDE0!important}
.guide-content .toc{background:#f5f2f8!important;border:1px solid #D4CDE0!important}
.guide-content .quick-summary{background:#f5f2f8!important;border:1px solid #D4CDE0!important}
@media (max-width: 768px) {
    .guide-content table { font-size: 0.85rem; }
    .guide-content table thead tr th { padding: 8px 10px; font-size: 0.8rem; }
    .guide-content table tbody td { padding: 6px 10px; }
    .guide-content h2 { font-size: 1.4em; }
    .guide-content h3 { font-size: 1.15em; }
}
@media (max-width: 640px) {
    .guide-content table { display: block; overflow-x: auto; }
    .guide-content h2 { font-size: 1.25em; }
    .guide-content h3 { font-size: 1.05em; }
}
</style>"""

def fix_problem_c1(content):
    """修复旧版结构"""
    modified = False
    
    # Case 1: <div class="container guide-content">...\n...</div>  ->  <main class="guide-content"><div class="container">...</div></main>
    if '<div class="container guide-content"' in content:
        # 替换开始标签
        content = content.replace('<div class="container guide-content">', 
                                  '<main class="guide-content">\n        <div class="container">', 1)
        
        # 找到文件末尾附近的 </div></body> 或 </body>
        # 替换为 </div></main></body>
        # 保守做法：在 </body> 前插入 </main>
        if '</main>' not in content:
            # 找到最后一个 </div> 前的位置（可能是 container 的闭合标签）
            # 简单做法：直接替换 </body> 为 </main></body>
            # 但需要确保有对应的 </div> 关闭 container
            pass  # 这个case需要更复杂的处理
        
        modified = True
    
    # Case 2: <main class="guide-main guide-content"> -> <main class="guide-content">
    if '<main class="guide-main guide-content"' in content:
        content = content.replace('<main class="guide-main guide-content"', 
                                  '<main class="guide-content"')
        modified = True
    
    return content, modified

def fix_toc_class(content):
    """修复 TOC 类名 table-of-contents -> toc"""
    modified = False
    
    # 替换 class="table-of-contents" 为 class="toc"
    pattern = re.compile(r'class="table-of-contents"')
    if pattern.search(content):
        content = pattern.sub('class="toc"', content)
        modified = True
    
    # 也检查 <nav class="table-of-contents"> 变体
    pattern_nav = re.compile(r'<nav class="table-of-contents"')
    if pattern_nav.search(content):
        content = pattern_nav.sub('<nav class="toc"', content)
        modified = True
    
    return content, modified

def fix_quick_summary_border(content):
    """修复 Quick Summary 的边框颜色"""
    modified = False
    
    # 找到 quick-summary div
    qs_pattern = re.compile(r'<div class="quick-summary"[^>]*style="([^"]*)"[^>]*>', re.IGNORECASE)
    match = qs_pattern.search(content)
    
    if match:
        style = match.group(1)
        if '#ebe5f0' in style or '#EBE5F0' in style or '#ebe5f0' in style.lower():
            old_tag = match.group(0)
            new_style = style.replace('#ebe5f0', '#D4CDE0').replace('#EBE5F0', '#D4CDE0').replace('#ebe5f0', '#D4CDE0')
            new_tag = old_tag.replace(style, new_style)
            content = content.replace(old_tag, new_tag)
            modified = True
    
    # 也全局替换 #ebe5f0 -> #D4CDE0（在style属性中）
    if '#ebe5f0' in content or '#EBE5F0' in content:
        content = content.replace('#ebe5f0', '#D4CDE0')
        content = content.replace('#EBE5F0', '#D4CDE0')
        modified = True
    
    return content, modified

def fix_quick_summary_position(content):
    """修复 Quick Summary 位置 - 移到内容区域最顶部（TOC前）"""
    modified = False
    
    # 查找 quick-summary div（完整）
    qs_start = content.find('<div class="quick-summary"')
    if qs_start == -1:
        return content, False
    
    qs_end = content.find('</div>', qs_start)
    if qs_end == -1:
        return content, False
    qs_end += 6  # 包含 </div>
    
    # 获取 quick-summary 完整内容
    qs_content = content[qs_start:qs_end]
    
    # 查找 main.guide-content 或 container 的开始位置
    main_pos = content.find('<main class="guide-content"')
    container_pos = content.find('<div class="container">', main_pos) if main_pos != -1 else -1
    
    if container_pos == -1 and main_pos != -1:
        container_pos = main_pos
    
    if container_pos == -1:
        return content, False
    
    # 查找 TOC 或第一个 section 的位置
    toc_pos = content.find('<div class="toc"', container_pos)
    nav_toc_pos = content.find('<nav class="toc"', container_pos)
    section_pos = content.find('<section', container_pos)
    
    # 找到第一个内容元素的位置
    positions = [p for p in [toc_pos, nav_toc_pos, section_pos] if p != -1]
    if not positions:
        return content, False
    
    first_content_pos = min(positions)
    
    # 检查 quick-summary 是否已经在正确位置（在第一个内容元素之前，且在 container 内）
    if qs_start < first_content_pos and qs_start > container_pos:
        # 已经在正确位置
        return content, False
    
    # 需要移动：先移除 quick-summary
    content_without_qs = content[:qs_start] + content[qs_end:]
    
    # 在 container 开始后、第一个内容元素前插入 quick-summary
    # 找到 container 标签后的位置
    insert_pos = content_without_qs.find('>\n', container_pos)
    if insert_pos == -1:
        insert_pos = content_without_qs.find('>', container_pos)
    if insert_pos == -1:
        return content, False
    insert_pos += 1  # 跳过 >
    
    # 插入 quick-summary
    content = content_without_qs[:insert_pos] + '\n' + qs_content + '\n            ' + content_without_qs[insert_pos:]
    modified = True
    
    return content, modified

def add_or_replace_css_block(content):
    """在 </body> 前添加或替换 CSS 覆盖块"""
    modified = False
    
    # 检查是否已有 <style> 块（包含 .guide-content 规则）
    style_pattern = re.compile(r'<style>\s*\.guide-content', re.DOTALL)
    existing = style_pattern.search(content)
    
    if existing:
        # 找到 <style> 的开始和结束位置
        style_start = content.rfind('<style>', 0, existing.end())
        style_end = content.find('</style>', style_start)
        if style_end != -1:
            style_end += 8  # 包含 </style>
            # 替换整个 style 块
            content = content[:style_start] + CSS_OVERRIDE + '\n' + content[style_end:]
            modified = True
    else:
        # 在 </body> 前添加
        if '</body>' in content:
            content = content.replace('</body>', CSS_OVERRIDE + '\n</body>')
            modified = True
    
    return content, modified

def fix_ebe5f0(content):
    """修复残留的 #ebe5f0 颜色"""
    modified = False
    
    replacements = [
        ('#ebe5f0', '#D4CDE0'),
        ('#EBE5F0', '#D4CDE0'),
        ('#Ebe5f0', '#D4CDE0'),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    return content, modified

def fix_file(filename):
    """修复单个文件"""
    filepath = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(filepath):
        return False, ["文件不存在"]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    problems = []
    
    # Problem C1: 修复结构
    content, modified = fix_problem_c1(content)
    if modified:
        problems.append("C1(结构)")
    
    # Problem C2: 修复 TOC 类名
    content, modified = fix_toc_class(content)
    if modified:
        problems.append("C2(TOC)")
    
    # Problem A: 修复 Quick Summary 位置
    content, modified = fix_quick_summary_position(content)
    if modified:
        problems.append("A(位置)")
    
    # Problem A: 修复 Quick Summary 边框
    content, modified = fix_quick_summary_border(content)
    if modified:
        problems.append("A(边框)")
    
    # Step 3: 添加/替换 CSS 覆盖块
    content, modified = add_or_replace_css_block(content)
    if modified:
        problems.append("Step3(CSS)")
    
    # Step 4: 修复 #ebe5f0
    content, modified = fix_ebe5f0(content)
    if modified:
        problems.append("Step4(#ebe5f0)")
    
    # 写回文件
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, problems
    
    return False, []

def main():
    results = []
    modified_count = 0
    skipped_count = 0
    
    for filename in TARGET_FILES:
        print(f"处理: {filename}")
        
        try:
            modified, problems = fix_file(filename)
            
            if modified:
                modified_count += 1
                problems_str = ",".join(problems) if problems else "已修改"
                print(f"  ✅ 已修复: {problems_str}")
                results.append(f"✅ {filename}: 已修复{problems_str}")
            else:
                skipped_count += 1
                print(f"  ⏭️ 无需修改")
                results.append(f"⏭️ {filename}: 无需修改")
        
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            results.append(f"❌ {filename}: 错误 - {e}")
    
    print(f"\n{'='*60}")
    print(f"修复完成：{modified_count+skipped_count}/{len(TARGET_FILES)}")
    print(f"修改：{modified_count} 篇，无需修改：{skipped_count} 篇")
    print(f"{'='*60}")
    
    print("\n详细结果：")
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
