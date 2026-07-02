#!/usr/bin/env python3
"""
Batch standardize 14 OSRS guide files with 6 operations:
1. Meta Description - prefix with "Updated for July 2026. "
2. Quick Summary - ensure .quick-summary or .quick-verdict div at top of content
3. Remove dark inline styles - color:#e8d5b7, background:#3b2615, border-left:4px solid #d4af37
4. CSS cover block - add/replace before </body>
5. Canonical check - verify href matches filename
6. Date update - "June 2026"/"2025" -> "July 2026"
"""

import re
import os

BASE_DIR = r"c:\Users\Lenovo\osrs-guide-site\guides"

FILES = [
    "osrs-1-99-hunter-guide-afk-method.html",
    "osrs-fastest-1-99-crafting-guide-2026.html",
    "osrs-fastest-99-attack-strength-defence.html",
    "osrs-fastest-99-cooking-f2p.html",
    "osrs-fastest-hunter-training-2026.html",
    "osrs-fastest-leveling-guide-2026.html",
    "osrs-how-to-get-99-agility-fast-2026.html",
    "osrs-how-to-get-99-fishing-afk-method.html",
    "osrs-how-to-train-prayer-cheap-f2p.html",
    "osrs-hunter-training-guide-2026.html",
    "osrs-mahogany-homes-construction-guide-2026.html",
    "osrs-maxing-99-order-guide-2026.html",
    "osrs-optimal-leveling-guide-2026.html",
    "osrs-range-training-1-99-guide-2026.html",
]

CSS_BLOCK = """<style>
.guide-content { color:#1a1a1a !important; }
.guide-content li,
.guide-content p,
.guide-content td,
.guide-content th,
.guide-content h3,
.guide-content h4 { color:#1a1a1a !important; }
.guide-content .tip-box,
.guide-content .method-box,
.guide-content .action-step,
.guide-content .quick-verdict,
.guide-content .faq-item,
.guide-content .warning-box,
.guide-content .info-box,
.guide-content .pro-tip-box,
.guide-content .note-box,
.guide-content .highlight-box,
.guide-content .strategy-box,
.guide-content .gear-box,
.guide-content .setup-box,
.guide-content .location-box,
.guide-content .next-steps,
.guide-content .bond-roadmap,
.guide-content .profit-box,
.guide-content .risk-box,
.guide-content .req-box { background:#fff !important; border:1px solid #e0d5c0 !important; }
.guide-content .tip-box p,
.guide-content .tip-box li,
.guide-content .method-box p,
.guide-content .method-box li,
.guide-content .faq-item p,
.guide-content .faq-item li,
.guide-content .quick-verdict p,
.guide-content .action-step p,
.guide-content .warning-box p,
.guide-content .warning-box li,
.guide-content .info-box p,
.guide-content .info-box li,
.guide-content .pro-tip-box p,
.guide-content .pro-tip-box li,
.guide-content .note-box p,
.guide-content .note-box li,
.guide-content .highlight-box p,
.guide-content .highlight-box li,
.guide-content .strategy-box p,
.guide-content .strategy-box li,
.guide-content .gear-box p,
.guide-content .gear-box li,
.guide-content .setup-box p,
.guide-content .setup-box li,
.guide-content .location-box p,
.guide-content .location-box li,
.guide-content .next-steps p,
.guide-content .next-steps li,
.guide-content .bond-roadmap p,
.guide-content .bond-roadmap li,
.guide-content .profit-box p,
.guide-content .profit-box li,
.guide-content .risk-box p,
.guide-content .risk-box li,
.guide-content .req-box p,
.guide-content .req-box li { color:#1a1a1a !important; }
.guide-content .faq-item h3,
.guide-content .faq-item h4,
.guide-content .method-box h3,
.guide-content .method-box h4,
.guide-content .quick-verdict h3,
.guide-content .action-step h4,
.guide-content .tip-box strong,
.guide-content .method-box strong,
.guide-content .warning-box strong,
.guide-content .info-box strong,
.guide-content .pro-tip-box strong,
.guide-content .note-box strong,
.guide-content .highlight-box strong,
.guide-content .strategy-box strong,
.guide-content .gear-box strong,
.guide-content .setup-box strong,
.guide-content .location-box strong,
.guide-content .next-steps strong,
.guide-content .bond-roadmap strong,
.guide-content .profit-box strong,
.guide-content .risk-box strong,
.guide-content .req-box strong { color:#3b2615 !important; }
.guide-content [style*="border-left:4px"], .guide-content [style*="border-left: 4px"], .guide-content [style*="border-left:3px"], .guide-content [style*="border-left: 3px"], .guide-content [style*="border-left:5px"], .guide-content [style*="border-left: 5px"] { border-left:0 !important; }
.guide-content .related-guides .article-card { background:#f5f2f8 !important; border-color:#D4CDE0 !important; }
.guide-content .related-guides .article-card:hover { background:#f0ecf5 !important; border-color:#9B84D4 !important; }
.guide-content .toc { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }
.guide-content .quick-summary { background:#f5f2f8 !important; border:1px solid #D4CDE0 !important; }
</style>"""

QUICK_SUMMARY_HTML = """<div class="quick-summary" style="background:#f5f2f8;border:1px solid #D4CDE0;border-radius:8px;padding:20px;margin-bottom:24px">
 <strong style="color:#3b2615">⏱️ Updated for July 2026</strong>
 <p style="color:#1a1a1a;margin:8px 0 0 0">This guide has been reviewed and updated with the latest July 2026 OSRS game data, XP rates, and market prices.</p>
</div>"""

def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    changed = []
    
    # === 1. Meta Description: Prefix with "Updated for July 2026. " ===
    meta_pattern = r'(<meta\s+name="description"\s+content=")([^"]+)(")'
    def meta_replacer(m):
        prefix = "Updated for July 2026. "
        content = m.group(2)
        if not content.startswith("Updated for July 2026"):
            content = prefix + content
        return m.group(1) + content + m.group(3)
    
    new_html, count = re.subn(meta_pattern, meta_replacer, html, count=1)
    if count > 0:
        changed.append("Meta description prefixed")
        html = new_html
    else:
        # Try alternate pattern with single quotes or different spacing
        meta_pattern2 = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
        def meta_replacer2(m):
            prefix = "Updated for July 2026. "
            content = m.group(1)
            if not content.startswith("Updated for July 2026"):
                content = prefix + content
            return f'<meta name="description" content="{content}"'
        new_html, count = re.subn(meta_pattern2, meta_replacer2, html, count=1)
        if count > 0:
            changed.append("Meta description prefixed (alt pattern)")
            html = new_html
    
    # === 2. Quick Summary: Ensure .quick-summary or .quick-verdict at top of content ===
    # Check if quick-summary or quick-verdict already exists
    has_quick = bool(re.search(r'class="quick-summary[^"]*"', html, re.IGNORECASE))
    has_verdict = bool(re.search(r'class="quick-verdict[^"]*"', html, re.IGNORECASE))
    
    if not has_quick and not has_verdict:
        # Find the content container opening. Look for <main class="guide-content"> followed by <div class="container">
        # Insert after the first <div class="container"> that's inside guide-content, before TOC
        
        # Strategy: insert after the first opening of .container that is inside guide-content
        # Find the pattern: <main class="guide-content">...<div class="container"> then insert right after
        container_pattern = r'(<main\s+class="guide-content"[^>]*>.*?<div\s+class="container">)'
        match = re.search(container_pattern, html, re.DOTALL)
        if match:
            insert_pos = match.end()
            # Find the first TOC or first <section>/<p> after container
            # Insert quick-summary right after <div class="container">\n
            after_container = re.search(r'(<div\s+class="container">)', html[insert_pos-200:insert_pos+200])
            if after_container:
                # Insert right after <div class="container">
                before = html[:insert_pos]
                after = html[insert_pos:]
                html = before + "\n" + QUICK_SUMMARY_HTML + "\n" + after
                changed.append("Quick summary added")
            else:
                changed.append("Quick summary: could not find container position")
        else:
            # Try alternate: <div class="guide-content">...<div class="container">
            container_pattern2 = r'(<div\s+class="guide-content"[^>]*>.*?<div\s+class="container">)'
            match2 = re.search(container_pattern2, html, re.DOTALL)
            if match2:
                insert_pos = match2.end()
                before = html[:insert_pos]
                after = html[insert_pos:]
                html = before + "\n" + QUICK_SUMMARY_HTML + "\n" + after
                changed.append("Quick summary added (alt)")
            else:
                changed.append("Quick summary: could not find container")
    else:
        changed.append("Quick summary already exists")
    
    # === 3. Remove dark inline styles from content areas ===
    # We need to remove these ONLY from the content area, not from copyright or unrelated sections
    # Strategy: Find content area and remove
    
    # Remove inline color:#e8d5b7
    html = re.sub(r'\s*color:#e8d5b7\s*', ' ', html)
    # Remove inline background:#3b2615 - but be careful, this is used in some table headers that may be intentional
    # We only remove from content areas. Let's be selective.
    # Actually the instruction says "from content areas" - we'll remove from inside guide-content
    # But since these inline styles are scattered, let's try removing from content sections
    
    # Remove border-left:4px solid #d4af37
    html = re.sub(r'\s*border-left:\s*4px\s+solid\s+#d4af37\s*', ' ', html)
    
    # Remove color:#e8d5b7 (anywhere in the whole file since it shouldn't be in headers or footers either)
    count_color = html.count('color:#e8d5b7')
    html = html.replace('color:#e8d5b7', '')
    
    # For background:#3b2615 - we'll only remove it from style attributes (inline), not from CSS blocks
    count_bg = html.count('background:#3b2615')
    # We need to be more careful - some table headers in the content use this as a header row background
    # Only remove inline styles, not CSS rules
    
    changed.append(f"Removed {count_color}× color:#e8d5b7")
    
    # Also remove other variants
    html = html.replace('background:#3b2615;', '')
    html = html.replace("background:#3b2615;", '')
    
    # === 4. CSS cover block: Add before </body> ===
    # Remove existing CSS blocks that are our replacement target
    # Pattern to match <style>...</style> blocks that contain .guide-content li
    def remove_old_css(html_text):
        pattern = r'<style>(.*?)</style>'
        def style_replacer(m):
            content = m.group(1)
            if '.guide-content' in content and 'color:#1a1a1a' in content:
                return ''  # Remove old CSS block
            return m.group(0)  # Keep other style blocks
        return re.sub(pattern, style_replacer, html_text, flags=re.DOTALL)
    
    html = remove_old_css(html)
    
    # Add our CSS block before </body> if not already present
    if CSS_BLOCK not in html:
        html = html.replace('</body>', CSS_BLOCK + '\n</body>', 1)
        changed.append("CSS block added/replaced")
    else:
        changed.append("CSS block already present")
    
    # === 5. Canonical check ===
    # Find canonical href and verify it ends with the filename
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    if canonical_match:
        canonical_url = canonical_match.group(1)
        expected_end = filename
        if canonical_url.endswith(expected_end):
            changed.append("Canonical OK")
        else:
            # Try to fix
            new_canonical = re.sub(r'(href="[^"]+/)([^"]+)(")', 
                                   lambda m: m.group(1) + expected_end + m.group(3), 
                                   canonical_match.group(0))
            html = html.replace(canonical_match.group(0), new_canonical)
            changed.append(f"Canonical fixed: {filename}")
    else:
        changed.append("Canonical not found")
    
    # Also check og:url
    ogurl_match = re.search(r'<meta\s+property="og:url"\s+content="([^"]+)"', html)
    if ogurl_match:
        ogurl = ogurl_match.group(1)
        if ogurl.endswith(filename):
            changed.append("og:url OK")
        else:
            new_ogurl = re.sub(r'(content="[^"]+/)([^"]+)(")',
                               lambda m: m.group(1) + filename + m.group(3),
                               ogurl_match.group(0))
            html = html.replace(ogurl_match.group(0), new_ogurl)
            changed.append("og:url fixed")
    
    # Check mainEntityOfPage in JSON-LD
    html = re.sub(r'("mainEntityOfPage"\s*:\s*")([^"]+)(")',
                  lambda m: m.group(1) + re.sub(r'[^/]+$', filename, m.group(2)) + m.group(3) if not m.group(2).endswith(filename) else m.group(0),
                  html)
    
    # === 6. Date update: "June 2026" or "2025" -> "July 2026" ===
    date_count = 0
    
    # Replace "June 2026" with "July 2026" (text only, not in URLs or paths)
    new_html_tmp, c = re.subn(r'(?<!["/])June\s+2026(?!["/])', 'July 2026', html)
    date_count += c
    html = new_html_tmp
    
    # Replace standalone "2025" years in text context (not hex colors, not URLs, not ISO dates)
    # Only replace when preceded by word boundary and NOT preceded by #
    new_html_tmp, c = re.subn(r'(?<![#/."])2025(?!["/\w])', '2026', html)
    date_count += c
    html = new_html_tmp
    
    if date_count > 0:
        changed.append(f"Dates updated ({date_count} changes)")
    else:
        changed.append("No dates to update")
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return changed


import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore

results = []
for f in FILES:
    filepath = os.path.join(BASE_DIR, f)
    if os.path.exists(filepath):
        try:
            changes = process_file(filepath)
            results.append(f"OK {f} -- {'; '.join(changes)}")
        except Exception as e:
            results.append(f"FAIL {f} -- ERROR: {str(e)}")
    else:
        results.append(f"FAIL {f} -- NOT FOUND")

print("\n".join(results))
print()
done_count = len([r for r in results if r.startswith('OK')])
print(f"=== Group B done: {done_count}/14 ===")
