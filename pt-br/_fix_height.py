import re, glob, os, shutil

count = 0
fixed_files = 0
os.makedirs('_temp_fix', exist_ok=True)

for fpath in glob.glob('guides/*.html'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content, n = re.subn(r'width="500"(?!.*?height=)', 'width="500" height="300"', content)
    if n > 0:
        fname = os.path.basename(fpath)
        tmp = os.path.join('_temp_fix', fname)
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += n
        fixed_files += 1
        # move back
        shutil.move(tmp, fpath)

print(f"Fixed {count} img tags in {fixed_files} files")

# cleanup
if os.path.exists('_temp_fix'):
    os.rmdir('_temp_fix')
