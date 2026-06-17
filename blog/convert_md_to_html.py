import json, re, sys

# Read markdown
with open(r"C:\Users\Lenovo\osrs-guide-site\blog\osrs-money-making-12-guides-2026.md", "r", encoding="utf-8") as f:
    md = f.read()

# Remove frontmatter
html_body = re.sub(r'^---\n.*?\n---\n', '', md, flags=re.DOTALL)

# Simple conversions
html_body = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_body)
html_body = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html_body)
html_body = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_body)
html_body = re.sub(r'^---$', '<hr>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_body, flags=re.MULTILINE)

# Wrap in HTML
html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>12 New OSRS Money Making Guides — 2026 GP Roadmap</title>
<style>
body { margin:0; padding:24px 20px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; font-size:16px; line-height:1.7; color:#24292f; background:#fff; }
.container { max-width:800px; margin:0 auto; }
h1 { font-size:2em; margin:0.5em 0 0.3em; border-bottom:2px solid #d4af37; padding-bottom:0.3em; }
h2 { font-size:1.5em; margin:1.2em 0 0.5em; border-bottom:1px solid #e1e4e8; padding-bottom:0.3em; }
h3 { font-size:1.25em; margin:1em 0 0.4em; }
a { color:#d4af37; text-decoration:none; }
a:hover { text-decoration:underline; }
blockquote { border-left:4px solid #d4af37; padding:0.5em 1em; margin:1em 0; background:#fff8e1; }
code { background:#f6f8fa; padding:0.2em 0.4em; border-radius:4px; font-size:85%; }
pre { background:#f6f8fa; padding:16px; border-radius:6px; overflow-x:auto; }
pre code { background:transparent; padding:0; }
hr { border:none; border-top:2px solid #e1e4e8; margin:2em 0; }
ul, ol { padding-left:2em; }
li { margin:0.3em 0; }
</style>
</head>
<body>
<div class="container">
''' + html_body + '''
</div>
</body>
</html>'''

payload = json.dumps({"html": html, "title": "12 New OSRS Money Making Guides — 2026 GP Roadmap"})

with open(r"C:\Users\Lenovo\osrs-guide-site\blog\shippage_payload.json", "w", encoding="utf-8") as f:
    f.write(payload)

print("Payload written. Length:", len(payload))
