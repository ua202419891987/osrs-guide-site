import json, re, os, urllib.request, urllib.parse

# Read API key
api_key = ""
with open(os.path.expanduser("~/.shippage/credentials.json"), "r") as f:
    creds = json.load(f)
    api_key = creds.get("api_key", "")

print("API key loaded:", "yes" if api_key else "no")

# Read OSRS blog markdown
with open("C:/Users/Lenovo/osrs-guide-site/blog/osrs-2026-roadmap-updates-guide.md", "r", encoding="utf-8") as f:
    md = f.read()

# Extract title
title_match = re.search(r'^title:\s*"([^"]+)"', md, re.MULTILINE)
title = title_match.group(1) if title_match else "OSRS 2026 Roadmap"

# Remove frontmatter
md_body = re.sub(r'^---\n.*?\n---\n', '', md, flags=re.DOTALL)

# Very basic markdown -> HTML (just wrap paragraphs)
lines = md_body.split('\n')
html_parts = []
in_code = False
code_lines = []
in_list = False

for line in lines:
    stripped = line.strip()
    if not stripped:
        if in_code:
            pass
        elif in_list:
            html_parts.append('</ul>')
            in_list = False
        html_parts.append('<br>')
        continue
    
    # Code blocks
    if line.startswith('```'):
        if in_code:
            html_parts.append('<pre><code>' + '\n'.join(code_lines) + '</code></pre>')
            code_lines = []
            in_code = False
        else:
            in_code = True
        continue
    if in_code:
        code_lines.append(line)
        continue
    
    # Headers
    if stripped.startswith('## '):
        html_parts.append('<h2>' + stripped[3:] + '</h2>')
    elif stripped.startswith('### '):
        html_parts.append('<h3>' + stripped[4:] + '</h3>')
    elif stripped.startswith('#### '):
        html_parts.append('<h4>' + stripped[5:] + '</h4>')
    elif stripped.startswith('- '):
        if not in_list:
            html_parts.append('<ul>')
            in_list = True
        item = stripped[2:]
        # Bold
        item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
        # Links
        item = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', item)
        html_parts.append('<li>' + item + '</li>')
    elif stripped.startswith('> '):
        html_parts.append('<blockquote>' + stripped[2:] + '</blockquote>')
    elif stripped.startswith('|'):
        # Skip table lines for now, just emit as-is in monospace
        html_parts.append('<code>' + stripped + '</code>')
    else:
        # Regular paragraph - bold, links
        p = stripped
        p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
        p = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', p)
        p = re.sub(r'`([^`]+)`', r'<code>\1</code>', p)
        if p:
            html_parts.append('<p>' + p + '</p>')

html_body = '\n'.join(html_parts)

# Wrap in full HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{ margin:0; padding:24px 20px; font-family:-apple-system,BlinkMacSystemFont,sans-serif; font-size:16px; line-height:1.7; color:#e8d5b7; background:#2a1a0a; }}
.article {{ max-width:820px; margin:0 auto; }}
h1,h2,h3,h4 {{ color:#d4af37; }}
h2 {{ border-bottom:1px solid #4a3320; padding-bottom:0.3em; margin-top:1.5em; }}
h3 {{ margin-top:1.2em; }}
a {{ color:#d4af37; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
code {{ background:#3b2615; padding:0.2em 0.4em; border-radius:4px; font-size:85%; color:#d4af37; }}
pre {{ background:#3b2615; padding:16px; border-radius:6px; overflow-x:auto; }}
blockquote {{ border-left:0.25em solid #d4af37; padding:0 1em; color:#ccc; margin:0 0 16px; }}
ul {{ padding-left:2em; }}
li {{ margin:0.3em 0; }}
strong {{ color:#d4af37; }}
hr {{ border:none; border-top:1px solid #4a3320; margin:1.5em 0; }}
p {{ margin:0.8em 0; }}
</style>
</head>
<body>
<article class="article">
{html_body}
</article>
</body>
</html>'''

print("HTML length:", len(html))

# Publish to ShipPage
url = "https://shippage.ai/v1/publish"
data = json.dumps({"html": html, "title": title}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "X-Skill-Version": "1.2.0"
})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print("Publish result:", json.dumps(result, indent=2))
        if "url" in result:
            print("\n=== PUBLISHED URL ===")
            print(result["url"])
except Exception as e:
    print("Error:", e)
