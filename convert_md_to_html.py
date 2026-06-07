import re, json, codecs

md = codecs.open(r'C:\Users\Lenovo\osrs-guide-site\medium-osrs-money-making-2026.md', 'r', 'utf-8').read()

title_match = re.search(r'^#\s+(.+)$', md, re.MULTILINE)
title = title_match.group(1).strip() if title_match else 'OSRS Money Making Guide 2026'

body = md

# Headers
body = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', body, flags=re.MULTILINE)
body = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', body, flags=re.MULTILINE)
body = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', body, flags=re.MULTILINE)
body = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', body, flags=re.MULTILINE)
body = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', body, flags=re.MULTILINE)

# Horizontal rule
body = re.sub(r'^---+$', r'<hr>', body, flags=re.MULTILINE)

# Blockquote
body = re.sub(r'^>\s*(.+)$', r'<blockquote>\1</blockquote>', body, flags=re.MULTILINE)

# Bold and italic
body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body)
body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', body)

# Inline code
body = re.sub(r'`([^`]+)`', r'<code>\1</code>', body)

# Links
body = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', body)

# Table rows
def table_row(m):
    cells = [c.strip() for c in m.group(1).split('|') if c.strip() and not re.match(r'[-:]+', c.strip())]
    return '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'

body = re.sub(r'\|(.+)\|', table_row, body)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>''' + title + '''</title>
<style>
body { margin:0; padding:40px 24px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; font-size:17px; line-height:1.8; color:#24292f; background:#fff; }
.markdown-body { max-width:760px; margin:0 auto; }
h1 { font-size:2em; border-bottom:2px solid #eaecef; padding-bottom:0.3em; margin-top:24px; margin-bottom:16px; }
h2 { font-size:1.5em; border-bottom:1px solid #eaecef; padding-bottom:0.3em; margin-top:24px; margin-bottom:16px; }
h3 { font-size:1.25em; margin-top:24px; margin-bottom:16px; }
p { margin-top:0; margin-bottom:16px; }
a { color:#0969da; text-decoration:none; }
a:hover { text-decoration:underline; }
code { background:#f6f8fa; padding:0.2em 0.4em; border-radius:6px; font-size:85%; font-family:SFMono-Regular,Consolas,monospace; }
pre { background:#f6f8fa; padding:16px; border-radius:6px; overflow-x:auto; margin-bottom:16px; }
pre code { background:transparent; padding:0; }
blockquote { border-left:4px solid #d1d9e0; padding:0 1em; color:#656d76; margin:0 0 16px; }
hr { height:2px; background:#eaecef; border:none; margin:24px 0; }
ul, ol { padding-left:2em; margin-bottom:16px; }
li { margin-bottom:6px; }
table { border-collapse:collapse; width:100%; margin-bottom:16px; }
th, td { padding:8px 14px; border:1px solid #d1d9e0; text-align:left; }
th { background:#f6f8fa; font-weight:600; }
strong { font-weight:600; }
em { color:#656d76; }
</style>
</head>
<body>
<article class="markdown-body">
''' + body + '''
</article>
</body>
</html>'''

with open(r'C:\Users\Lenovo\osrs-guide-site\medium-osrs-money-making-2026.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML written successfully")
print("Title:", title)
