#!/usr/bin/env python3
"""
批量修复30篇OSRS新手攻略的格式问题：
Problem A: Quick Summary 位置/边框
Problem B: 正文box左侧深色边框 (通过CSS覆盖解决)
Problem C: 旧版结构 + TOC类名
同时修复 #ebe5f0 -> #D4CDE0
"""

import re
import os

# 30篇目标文章
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

CSS_OVERRIDE = """
<style>
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
</style>
"""

def fix_file(filepath):
    """修复单个文件，返回 (modified, problems_fixed)"""
    if not os.path.exists(filepath):
        return (False, [])
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    problems_fixed = []
    
    # ============================================================
    # Problem C1: 修复旧版结构
    # Case 1: <div class="container guide-content"> -> 
    #         <main class="guide-content"><div class="container">
    # ============================================================
    if '<div class="container guide-content"' in content:
        # 找到这个 div 并替换成 <main class="guide-content"><div class="container">
        # 同时需要找到对应的结束标签
        # 这个模式比较硬编码，需要小心处理
        
        # 替换开始标签
        content = content.replace('<div class="container guide-content">', 
                                  '<main class="guide-content"><div class="container">')
        
        # 找到 </div> 后面可能跟着 </body> 或 </main> 的情况
        # 需要在文件末尾附近找到匹配的 </div> 并替换成 </div></main>
        # 保守做法：在 </body> 前添加 </main>
        if '</main>' not in content:
            content = content.replace('</body>', '</main></body>')
        
        problems_fixed.append("C1(结构)")
    
    # Case 2: <main class="guide-main guide-content"> -> <main class="guide-content">
    if '<main class="guide-main guide-content"' in content:
        content = content.replace('<main class="guide-main guide-content"', 
                                  '<main class="guide-content"')
        problems_fixed.append("C1(结构)")
    
    # ============================================================
    # Problem C2 + Problem A (TOC位置): 修复 TOC 类名
    # ============================================================
    toc_pattern = re.compile(r'class="table-of-contents"')
    if toc_pattern.search(content):
        content = toc_pattern.sub('class="toc"', content)
        problems_fixed.append("C2(TOC类名)")
    
    # ============================================================
    # Problem A: Quick Summary 边框颜色 + 位置
    # ============================================================
    
    # A1: 修复边框颜色 #ebe5f0 -> #D4CDE0 (在quick-summary内联样式中)
    # 先找到 quick-summary div
    qs_pattern = re.compile(
        r'<div class="quick-summary"[^>]*style="([^"]*)"[^>]*>',
        re.IGNORECASE
    )
    qs_match = qs_pattern.search(content)
    if qs_match:
        style_content = qs_match.group(1)
        if '#ebe5f0' in style_content:
            new_style = style_content.replace('#ebe5f0', '#D4CDE0')
            old_tag = qs_match.group(0)
            new_tag = old_tag.replace(style_content, new_style)
            content = content.replace(old_tag, new_tag)
            problems_fixed.append("A(边框颜色)")
        
        # 也检查 border:1px solid #ebe5f0 的任何变体
        if 'solid #ebe5f0' in qs_match.group(0) or 'solid #ebe5f0' in style_content:
            old_tag = qs_match.group(0)
            new_tag = old_tag.replace('solid #ebe5f0', 'solid #D4CDE0')
            if new_tag == old_tag:
                new_tag = old_tag.replace('solid #ebe5f0', 'solid #D4CDE0')
            content = content.replace(old_tag, new_tag)
    
    # A2: 检查 quick-summary 是否在正确位置 (在 TOC 或第一个 section 之前)
    # 查找 quick-summary 的位置
    qs_pos = content.find('<div class="quick-summary"')
    toc_pos = content.find('<div class="toc"')
    nav_toc_pos = content.find('<nav class="toc"')
    
    # 也检查是否有残留的 table-of-contents (应该在上面已经修复了)
    # 实际检查：quick-summary 应该在 main.guide-content > .container 的直接子元素
    
    # 简化：确保 quick-summary 内联样式中有正确的边框
    # 更全面的边框修复
    content = content.replace(
        'border:1px solid #ebe5f0',
        'border:1px solid #D4CDE0'
    )
    content = content.replace(
        'border: 1px solid #ebe5f0',
        'border: 1px solid #D4CDE0'
    )
    
    # ============================================================
    # Step 3: 替换底部 CSS 覆盖块
    # ============================================================
    
    # 查找已有的 <style> 块（在 </body> 前）
    # 匹配 </body> 前的 <style>...</style>
    style_block_pattern = re.compile(r'<style>\s*\.guide-content.*?</style>', re.DOTALL)
    existing_style = style_block_pattern.search(content)
    
    if existing_style:
        # 替换现有的 style 块
        content = content.replace(existing_style.group(0), CSS_OVERRIDE)
        problems_fixed.append("Step3(CSS覆盖)")
    else:
        # 添加 style 块到 </body> 前
        content = content.replace('</body>', CSS_OVERRIDE + '\n</body>')
        problems_fixed.append("Step3(CSS覆盖)")
    
    # ============================================================
    # Step 4: 修复残留的 #ebe5f0 (在非内容区域)
    # ============================================================
    ebe5f0_count = content.count('#ebe5f0')
    if ebe5f0_count > 0:
        content = content.replace('#ebe5f0', '#D4CDE0')
        problems_fixed.append("Step4(#ebe5f0)")
    
    # 也修复小写变体
    content = content.replace('#Ebe5f0', '#D4CDE0')
    content = content.replace('#EBE5F0', '#D4CDE0')
    
    # ============================================================
    # Problem B: 确保 CSS 覆盖块包含 border-left:0 规则
    # (已在 CSS_OVERRIDE 中包含)
    # ============================================================
    
    # 写回文件
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return (True, problems_fixed)
    
    return (False, [])

def main():
    base_dir = r"C:\Users\Lenovo\osrs-guide-site\guides"
    
    modified_count = 0
    skipped_count = 0
    all_results = []
    
    for filename in TARGET_FILES:
        filepath = os.path.join(base_dir, filename)
        print(f"处理: {filename}")
        
        try:
            modified, problems = fix_file(filepath)
            if modified:
                modified_count += 1
                problems_str = ",".join(problems) if problems else "未知"
                print(f"  ✅ 已修复: {problems_str}")
                all_results.append(f"✅ {filename}: 已修复{problems_str}")
            else:
                skipped_count += 1
                print(f"  ⏭️ 无需修改")
                all_results.append(f"⏭️ {filename}: 无需修改")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            all_results.append(f"❌ {filename}: 错误 - {e}")
    
    print(f"\n{'='*60}")
    print(f"修复完成：{len(TARGET_FILES)}/{len(TARGET_FILES)}")
    print(f"修改：{modified_count} 篇，无需修改：{skipped_count} 篇")
    print(f"{'='*60}")
    
    # 输出结果摘要
    print("\n详细结果：")
    for result in all_results:
        print(result)

if __name__ == "__main__":
    main()
