"""Revert PayPal.me links back to QQ email, only keep 163 email for visible contact info."""
import os

OLD_EMAIL = "m15881172167@163.com"
PAYPAL_EMAIL = "1530398390@qq.com"  # Keep this for PayPal payments
BASE = r"C:\Users\Lenovo\osrs-guide-site"

# Only revert PayPal links (containing paypal.com)
reverted = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ["node_modules", ".git"]]
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            if "paypal.com" in content and OLD_EMAIL in content:
                new_content = content.replace(OLD_EMAIL, PAYPAL_EMAIL)
                with open(filepath, "w", encoding="utf-8") as fh:
                    fh.write(new_content)
                reverted += 1
                print("Reverted PayPal links:", os.path.relpath(filepath, BASE))

print(f"\nDone. Reverted {reverted} files' PayPal links back to {PAYPAL_EMAIL}")
