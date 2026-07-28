import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Wrong -> Correct mappings
replacements = {
    "https://payhip.com/b/MVtu5": "https://payhip.com/b/MVzaS",
    "https://payhip.com/b/qjkmVs": "https://payhip.com/b/qkmVs",
}

count = 0
for dp, dn, fn in os.walk(ROOT):
    low = dp.lower()
    if "crimson-desert" in low or "windrose" in low:
        continue
    for f in fn:
        if not f.endswith(".html"):
            continue
        p = os.path.join(dp, f)
        try:
            c = open(p, encoding="utf-8").read()
        except:
            continue
        changed = False
        for old, new in replacements.items():
            if old in c:
                c = c.replace(old, new)
                changed = True
        if changed:
            open(p, "w", encoding="utf-8").write(c)
            count += 1
            print(f"Fixed: {os.path.relpath(p, ROOT)}")

print(f"\nTotal files fixed: {count}")
