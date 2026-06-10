"""Batch replace QQ email with 163 email across all website files."""
import os

OLD_EMAIL = "m15881172167@163.com"
NEW_EMAIL = "m15881172167@163.com"
BASE = r"C:\Users\Lenovo\osrs-guide-site"

files_to_fix = [
    "js/main.js",
    "scripts/add_paypal_button.py",
    "replace_kofi_with_paypal.py",
]

# Also find all HTML files with the old email
for root, dirs, files in os.walk(BASE):
    # Skip node_modules and .git
    dirs[:] = [d for d in dirs if d not in ["node_modules", ".git"]]
    for f in files:
        if f.endswith(".html") or f.endswith(".js") or f.endswith(".py"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            if OLD_EMAIL in content:
                new_content = content.replace(OLD_EMAIL, NEW_EMAIL)
                with open(filepath, "w", encoding="utf-8") as fh:
                    fh.write(new_content)
                rel = os.path.relpath(filepath, BASE)
                files_to_fix.append(rel)

print(f"Replaced '{OLD_EMAIL}' -> '{NEW_EMAIL}' in {len(files_to_fix)} files:")
for f in sorted(set(files_to_fix)):
    print(f"  {f}")
