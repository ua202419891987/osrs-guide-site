import os
import re
from pathlib import Path

GUIDES_DIR = r"C:\Users\Lenovo\osrs-guide-site\guides"

COPYRIGHT_META = '<meta name="copyright" content="(c) 2026 OSRS Guru (osrsguru.com). All rights reserved.">'

COPYRIGHT_BLOCK = """
<!-- Copyright & Anti-Scraping Notice -->
<div class="copyright-protection" style="background:#faf8f5;border:1px solid #e0d5c0;border-left:3px solid #d4af37;border-radius:4px;padding:10px 16px;margin:16px auto;max-width:780px">
    <p style="color:#1a1a1a;margin:0;font-size:0.78rem;line-height:1.55;">(c) 2026 <strong>OSRS Guru (osrsguru.com)</strong>. All rights reserved. This content is protected by copyright law. Unauthorized scraping, crawling, auto-republishing, or AI training data extraction is prohibited. Violations will be reported to search engines and hosting providers. | Content created under <a href="https://legal.jagex.com/docs/policies/fan-content-policy" target="_blank" rel="noopener" style="color:#3b2615;">Jagex Fan Content Policy</a>. Wiki content under <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener" style="color:#3b2615;">CC BY-SA 3.0</a>. Not affiliated with Jagex Ltd.</p>
</div>
"""

MOBILE_CSS = """
 /* ===== Mobile Responsive Overrides (P0 Standard) ===== */
 @media (max-width: 768px) {
  .guide-content table { font-size: 0.85rem; }
  .guide-content table thead tr th { padding: 8px 10px; font-size: 0.8rem; }
  .guide-content table tbody td { padding: 6px 10px; }
  .guide-content h2 { font-size: 1.4em; }
  .guide-content h3 { font-size: 1.15em; }
  .guide-content div[style*="border-radius:12px"] { padding: 16px !important; }
  .guide-content div[style*="border-radius:8px"] { padding: 14px !important; }
 }

 @media (max-width: 640px) {
  .guide-content table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .guide-content h2 { font-size: 1.25em; }
  .guide-content h3 { font-size: 1.05em; }
  .guide-content p { font-size: 0.95rem; line-height: 1.7; }
  .guide-content li { font-size: 0.95rem; line-height: 1.8; }
  .copyright-protection { margin: 12px 8px !important; padding: 8px 12px !important; }
  .copyright-protection p { font-size: 0.72rem !important; }
 }
"""


def has_copyright_meta(content):
    return 'name="copyright"' in content


def has_copyright_block(content):
    return 'copyright-protection' in content


def add_copyright_meta(content):
    canonical_pattern = r'(<link rel="canonical"[^>]+>)'
    match = re.search(canonical_pattern, content)
    if match:
        insert_pos = match.start()
        return content[:insert_pos] + COPYRIGHT_META + "\n" + content[insert_pos:]
    print("  [!] No canonical tag found")
    return content


def add_copyright_block(content):
    footer_pattern = r'(</footer>)'
    match = re.search(footer_pattern, content)
    if match:
        insert_pos = match.end()
        return content[:insert_pos] + "\n" + COPYRIGHT_BLOCK + "\n" + content[insert_pos:]
    print("  [!] No </footer> tag found")
    return content


def fix_text_color(content):
    content = re.sub(r'color:#2D2A33', 'color:#1a1a1a', content)
    content = re.sub(r'color: #2D2A33', 'color: #1a1a1a', content)
    return content


def add_mobile_css(content):
    if '@media (max-width:' in content:
        print("  [*] Already has mobile CSS")
        return content
    style_pattern = r'(</style>)'
    matches = list(re.finditer(style_pattern, content))
    if matches:
        last_match = matches[-1]
        insert_pos = last_match.start()
        return content[:insert_pos] + MOBILE_CSS + "\n" + content[insert_pos:]
    print("  [!] No </style> tag found")
    return content


def process_file(file_path):
    filename = os.path.basename(file_path)
    print("\nProcessing: " + filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print("  [ERROR] Cannot read: " + str(e))
        return False

    modified = False

    if not has_copyright_meta(content):
        print("  [+] Adding copyright meta")
        content = add_copyright_meta(content)
        modified = True
    else:
        print("  [OK] Already has copyright meta")

    if not has_copyright_block(content):
        print("  [+] Adding anti-scraping block")
        content = add_copyright_block(content)
        modified = True
    else:
        print("  [OK] Already has anti-scraping block")

    if '#2D2A33' in content:
        print("  [+] Fixing text color #2D2A33 -> #1a1a1a")
        content = fix_text_color(content)
        modified = True

    if '@media (max-width:' not in content:
        print("  [+] Adding mobile responsive CSS")
        content = add_mobile_css(content)
        modified = True
    else:
        print("  [OK] Already has mobile CSS")

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  [DONE] Updated OK")
            return True
        except Exception as e:
            print("  [ERROR] Cannot write: " + str(e))
            return False
    else:
        print("  [SKIP] No changes needed")
        return False


def main():
    print("=" * 60)
    print("P0 Standard Batch Upgrade Script v3")
    print("=" * 60)

    html_files = sorted(list(Path(GUIDES_DIR).glob("osrs-*-guide-2026.html")))
    print("\nFound " + str(len(html_files)) + " articles in guides/")

    need_upgrade = []
    for fp in html_files:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                c = f.read()
            if not has_copyright_meta(c) or not has_copyright_block(c):
                need_upgrade.append(fp)
        except:
            need_upgrade.append(fp)

    print("Need upgrade: " + str(len(need_upgrade)))

    if len(need_upgrade) == 0:
        print("\n[DONE] All files meet P0 standard!")
        return

    print("\nFiles to upgrade:")
    for i, fp in enumerate(need_upgrade[:20], 1):
        print("  " + str(i) + ". " + fp.name)
    if len(need_upgrade) > 20:
        print("  ... +" + str(len(need_upgrade) - 20) + " more")

    print("\nStarting...")

    ok = 0
    fail = 0
    for fp in need_upgrade:
        if process_file(fp):
            ok += 1
        else:
            fail += 1

    print("\n" + "=" * 60)
    print("[COMPLETE] " + str(ok) + "/" + str(len(need_upgrade)) + " files updated OK")
    if fail > 0:
        print("[WARN] " + str(fail) + " failed")
    print("=" * 60)
    print("\nNext step:")
    print('  git add guides/*.html')
    print('  git commit -m "P0 batch upgrade: anti-scrape + copyright + text-color + mobile"')
    print("  git push origin main")


if __name__ == "__main__":
    main()
