import os
from pathlib import Path

base = 'https://osrsguru.com'
urls = []

# Add index.html
urls.append(base + '/index.html')

# Add all guide HTML files
for root, dirs, files in os.walk('guides'):
    for f in files:
        if f.endswith('.html'):
            p = Path(root) / f
            rel = p.as_posix()
            urls.append(base + '/' + rel)

print('Total URLs found: ' + str(len(urls)))

# Save to workspace
out = 'C:/Users/Lenovo/WorkBuddy/2026-06-19-20-59-46/remaining_urls.txt'
with open(out, 'w', encoding='utf-8') as fp:
    for u in urls:
        fp.write(u + '\n')

print('Saved to: ' + out)
print('First 10 URLs:')
for u in urls[:10]:
    print('  ' + u)
