#!/usr/bin/env python3
"""精确修复30篇OSRS攻略的格式问题"""

import re
import os

BASE_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

FILES = [
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

CSS_BLOCK = """
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

def fix_structure(content):
    """修复Problem C1: 旧版结构"""
    modified = False
    log = []
    
    # Case 1: <div class="container guide-content"> -> 需要改成 <main class="guide-content"><div class="container">
    if '<div class="container guide-content"' in content:
        # 替换开始标签
        content = content.replace('<div class="container guide-content">', 
                                  '<main class="guide-content">\n        <div class="container">', 1)
        
        # 找到对应的 </div> (应该是文件末尾附近的那个)
        # 找最后一个 </div> 在 </body> 前
        body_pos = content.rfind('</body>')
        if body_pos != -1:
            # 在 </body> 前插入 </main>
            # 先检查是否已经有 </main>
            last_div_pos = content.rfind('</div>', 0, body_pos)
            if last_div_pos != -1:
                # 在这个 </div> 后添加 </main>
                # 但需要确保这个 </div> 是 container 的关闭标签
                # 保守做法：直接在 </body> 前添加 </main>
                pass
        
        # 简化：在 </body> 前添加 </main></div> 或 </main>
        if '</main>' not in content:
            content = content.replace('</body>', '</main></body>')
        
        modified = True
        log.append("C1(div->main)")
    
    # Case 2: <main class="guide-main guide-content"> -> <main class="guide-content">
    if '<main class="guide-main guide-content"' in content:
        content = content.replace('<main class="guide-main guide-content"', 
                                  '<main class="guide-content"')
        modified = True
        log.append("C1(guide-main)")
    
    return content, modified, log

def fix_toc_class(content):
    """修复Problem C2: TOC类名"""
    modified = False
    log = []
    
    # 替换所有 table-of-contents 为 toc
    if 'class="table-of-contents"' in content:
        content = content.replace('class="table-of-contents"', 'class="toc"')
        modified = True
        log.append("C2(TOC)")
    
    # 也检查 <nav class="table-of-contents">
    if '<nav class="table-of-contents"' in content:
        content = content.replace('<nav class="table-of-contents"', '<nav class="toc"')
        modified = True
        if "C2(TOC)" not in log:
            log.append("C2(TOC)")
    
    return content, modified, log

def fix_css_block(content):
    """Step 3: 替换底部CSS覆盖块为完整版"""
    modified = False
    log = []
    
    # 查找是否已有 <style> 块（在文件末尾附近）
    # 匹配 </body> 前的 <style>...</style>
    style_pattern = re.compile(r'<style>\s*\.guide-content.*?</style>', re.DOTALL)
    match = style_pattern.search(content)
    
    if match:
        # 替换现有的 style 块
        content = content.replace(match.group(0), CSS_BLOCK)
        modified = True
        log.append("Step3(替换CSS)")
    else:
        # 添加 CSS 块到 </body> 前
        if '</body>' in content:
            content = content.replace('</body>', CSS_BLOCK + '\n</body>')
            modified = True
            log.append("Step3(添加CSS)")
    
    return content, modified, log

def fix_ebe5f0(content):
    """Step 4: 修复残留的 #ebe5f0"""
    modified = False
    log = []
    
    for old in ['#ebe5f0', '#EBE5F0', '#Ebe5f0']:
        if old in content:
            content = content.replace(old, '#D4CDE0')
            modified = True
    
    if modified:
        log.append("Step4(#ebe5f0)")
    
    return content, modified, log

def fix_quick_summary_border(content):
    """Problem A: 修复Quick Summary边框颜色"""
    modified = False
    log = []
    
    # 找到 quick-summary 的 style 属性并修复边框颜色
    qs_pattern = re.compile(r'(<div class="quick-summary"[^>]*style=")([^"]*?)(")', re.IGNORECASE)
    
    def replace_border(match):
        nonlocal modified
        style = match.group(2)
        new_style = style
        for old in ['#ebe5f0', '#EBE5F0']:
            if old in new_style:
                new_style = new_style.replace(old, '#D4CDE0')
        
        if new_style != style:
            modified = True
            return match.group(1) + new_style + match.group(3)
        return match.group(0)
    
    content = qs_pattern.sub(lambda m: replace_border(m), content)
    
    if modified:
        log.append("A(QS边框)")
    
    return content, modified, log

def process_file(filename):
    """处理单个文件"""
    filepath = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(filepath):
        return "❌ 文件不存在", []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    all_logs = []
    
    # 按顺序应用修复
    # 1. Problem C1: 结构
    content, modified, logs = fix_structure(content)
    all_logs.extend(logs)
    
    # 2. Problem C2: TOC类名
    content, modified, logs = fix_toc_class(content)
    all_logs.extend(logs)
    
    # 3. Problem A: Quick Summary 边框
    content, modified, logs = fix_quick_summary_border(content)
    all_logs.extend(logs)
    
    # 4. Step 3: CSS 覆盖块
    content, modified, logs = fix_css_block(content)
    all_logs.extend(logs)
    
    # 5. Step 4: #ebe5f0
    content, modified, logs = fix_ebe5f0(content)
    all_logs.extend(logs)
    
    # 写回文件
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return "✅ " + ", ".join(all_logs) if all_logs else "已修改", all_logs
    
    return "⏭️ 无需修改", []

def main():
    results = []
    modified = 0
    skipped = 0
    
    for f in FILES:
        status, logs = process_file(f)
        if status.startswith("✅"):
            modified += 1
        elif status.startswith("⏭️"):
            skipped += 1
        results.append(f + ": " + status)
    
    print("=" * 60)
    print(f"修复完成：{modified+skipped}/{len(FILES)}")
    print(f"修改：{modified} 篇，无需修改：{skipped} 篇")
    print("=" * 60)
    
    print("\n详细结果：")
    for r in results:
        print(r)
    
    # 遗留问题
    print("\n遗留问题：")
    print("- Problem B (border-left) 通过CSS覆盖块中的规则自动处理")
    print("- 如需进一步调整，请检查CSS覆盖规则是否生效")

if __name__ == "__main__":
    main()
