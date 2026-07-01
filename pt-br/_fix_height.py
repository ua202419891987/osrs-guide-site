import re, glob

count = 0
for fpath in glob.glob('guides/*.html'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content, n = re.subn(r'width="500"(?!.*?height=)', 'width="500" height="300"', content)
    if n > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += n
        print(f"  OK: {fpath} ({n} fixes)")

print(f"\nDone! Fixed {count} img tags total.")
