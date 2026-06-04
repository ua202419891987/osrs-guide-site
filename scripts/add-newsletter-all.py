#!/usr/bin/env python3
"""
Batch add newsletter signup section to all HTML pages.
Usage: python scripts/add-newsletter-all.py
"""
import os
import re
from pathlib import Path

# The inline newsletter banner HTML (relative link aware)
NEWSLETTER_HTML = '''    <!-- Newsletter Signup -->
    <div class="container">
        <div class="newsletter-inline">
            <div class="nl-content">
                <h4>📬 Want More OSRS Tips?</h4>
                <p>Get one email per week with curated guides, money-making updates, and quest walkthroughs — no spam, unsubscribe anytime.</p>
            </div>
            <a href="https://docs.google.com/forms/d/12HzHFl1RNwoMdsfbxHGCEJoK59YUSaOAybxvd8L/viewform" target="_blank" rel="noopener" class="nl-btn">Subscribe Free</a>
        </div>
    </div>

'''

NEWSLETTER_HOME = '''<!-- Newsletter Signup -->
<section class="newsletter-section container" style="margin-top:40px;margin-bottom:40px">
  <span class="nl-icon">📬</span>
  <h3>Get Weekly OSRS Tips Delivered to Your Inbox</h3>
  <p>Join 500+ players receiving our weekly newsletter. One email per week — no spam, just curated money-making methods, quest walkthroughs, and meta updates you can actually use.</p>
  <a href="https://docs.google.com/forms/d/12HzHFl1RNwoMdsfbxHGCEJoK59YUSaOAybxvd8L/viewform" target="_blank" rel="noopener" class="nl-btn">Subscribe Free →</a>
  <div class="nl-note">Unsubscribe anytime. We never share your email.</div>
</section>

'''

def add_newsletter_to_file(filepath, is_home=False):
    """Add newsletter section before footer in an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has newsletter
    if 'newsletter-inline' in content or 'newsletter-section' in content:
        print(f"  SKIP (already has newsletter): {filepath}")
        return

    # For home page (index.html) use the full section
    if is_home:
        if '<footer' in content:
            content = content.replace('<footer', NEWSLETTER_HOME + '<footer', 1)
            print(f"  ADDED (home style): {filepath}")
        else:
            print(f"  SKIP (no footer found): {filepath}")
            return
    else:
        # For guide pages, add inline banner before footer
        if '<footer>' in content or '<footer ' in content:
            # Try to insert before footer with proper indentation
            content = re.sub(r'(\s+)(<footer[>\s])', r'\1<!-- Newsletter Signup -->\1<div class="container">\1    <div class="newsletter-inline">\1        <div class="nl-content">\1            <h4>📬 Want More OSRS Tips?</h4>\1            <p>Get one email per week with curated guides, money-making updates, and quest walkthroughs — no spam, unsubscribe anytime.</p>\1        </div>\1        <a href="https://docs.google.com/forms/d/12HzHFl1RNwoMdsfbxHGCEJoK59YUSaOAybxvd8L/viewform" target="_blank" rel="noopener" class="nl-btn">Subscribe Free</a>\1    </div>\1</div>\n\n\2', content, count=1)
            print(f"  ADDED (inline style): {filepath}")
        else:
            print(f"  SKIP (no footer found): {filepath}")
            return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    base_dir = Path(__file__).parent.parent
    html_files = []

    # Collect all HTML files
    for html_file in base_dir.rglob('*.html'):
        # Skip the formatted article
        if 'medium-article' in html_file.name:
            continue
        html_files.append(html_file)

    print(f"Found {len(html_files)} HTML files. Processing...\n")

    for html_file in sorted(html_files):
        rel_path = html_file.relative_to(base_dir)
        is_home = html_file.name == 'index.html' and html_file.parent == base_dir
        add_newsletter_to_file(html_file, is_home=is_home)

    print("\n✅ Done! Run 'git add . && git commit -m \"Add newsletter signup to all pages\"'")

if __name__ == '__main__':
    main()
