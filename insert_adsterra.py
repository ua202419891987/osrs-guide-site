import os, re

GUIDES = r"C:/Users/Lenovo/osrs-guide-site/guides"

# Exact HTML copied from the reference file guides/slayer-1-99-guide-2026.html
AD_DIV = '<div class="ad-banner" style="text-align:center;margin:22px auto;padding:10px;border:1px dashed #d4af37;border-radius:8px;max-width:728px;min-height:90px;color:#d4af37;font-size:12px;box-sizing:border-box;">Adsterra ad slot — paste your Adsterra banner code here</div>'
TOP_BOX = "<!--ADSTERRA_TOP-->\n" + AD_DIV
MID_BOX = "<!--ADSTERRA_MID-->\n" + AD_DIV

RED_LINE_STEMS = {
    "osrs-how-to-make-money-with-zulrah",
    "osrs-wilderness-bosses-guide-2026",
    "osrs-gauntlet-meta-changes-2026",
    "osrs-hunter-money-making-guide-2026",
    "osrs-slayer-70-to-95-money-makers-2026",
}

def in_scope(name):
    # top-level only: caller already restricts to GUIDES root
    if not name.endswith(".html"):
        return False
    first = name[0].lower()
    if first not in "mnopqr":
        return False
    stem = name[:-5]  # drop .html
    if stem in RED_LINE_STEMS:
        return False
    if name.startswith("_") or name.startswith("__") or name.endswith(".backup"):
        return False
    return True

targets = []
for entry in os.listdir(GUIDES):
    full = os.path.join(GUIDES, entry)
    if not os.path.isfile(full):
        continue  # exclude subdirs (crimson-desert/, windrose/, zh/, pt-br/, etc.)
    if in_scope(entry):
        targets.append(entry)
targets.sort()

top_count = 0
mid_count = 0
top_skipped = []
mid_skipped = []

for name in targets:
    path = os.path.join(GUIDES, name)
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    if "ADSTERRA_TOP" in content or "ADSTERRA_MID" in content:
        top_skipped.append((name, "already has ADSTERRA marker"))
        continue

    changed = False

    # TOP: after first </header>, else after <body ...>
    if "</header>" in content:
        idx = content.index("</header>") + len("</header>")
        content = content[:idx] + "\n" + TOP_BOX + "\n" + content[idx:]
        top_count += 1
        changed = True
    elif re.search(r"<body[^>]*>", content):
        m = re.search(r"<body[^>]*>", content)
        idx = m.end()
        content = content[:idx] + "\n" + TOP_BOX + "\n" + content[idx:]
        top_count += 1
        changed = True
    else:
        top_skipped.append((name, "no </header> or <body>"))

    # MID: after first </h2>; skip MID if none
    if "</h2>" in content:
        idx = content.index("</h2>") + len("</h2>")
        content = content[:idx] + "\n" + MID_BOX + "\n" + content[idx:]
        mid_count += 1
        changed = True
    else:
        mid_skipped.append((name, "no </h2> for MID"))

    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

print("TARGET files processed:", len(targets))
print("TOP inserted:", top_count)
print("MID inserted:", mid_count)
print("TOP/MID skipped (already done or no anchor):", len(top_skipped))
for s in top_skipped:
    print("  SKIP", s)
print("MID-only skipped (no </h2>):", len(mid_skipped))
for s in mid_skipped:
    print("  NOMID", s)
