#!/usr/bin/env python3
"""
提交本周新写的5篇文章到Google Indexing API
必须在下午3点后运行（配额重置）
"""

import json
import time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# 5篇新文章URL
URLS = [
    "https://osrsguru.com/guides/osrs-lms-beginner-guide-2026.html",
    "https://osrsguru.com/guides/osrs-drop-rate-probability-guide-2026.html",
    "https://osrsguru.com/guides/osrs-soulreaper-axe-guide-2026.html",
    "https://osrsguru.com/guides/osrs-guardians-of-the-rift-stardust-guide-2026.html",
    "https://osrsguru.com/guides/osrs-account-security-guide-2026.html",
]

def submit_urls():
    # 加载credentials（请确保在运行前已设置GOOGLE_APPLICATION_CREDENTIALS环境变量）
    creds = Credentials.from_authorized_user_file(
        "C:/Users/Lenovo/osrs-guide-site/credentials.json"
    )
    
    service = build("indexing", "v3", credentials=creds)
    
    success = 0
    fail = 0
    
    for url in URLS:
        try:
            body = {
                "url": url,
                "type": "URL_UPDATED"
            }
            response = service.urlNotifications().publish(body=body).execute()
            print(f"✅ Success: {url}")
            success += 1
            time.sleep(1)  # 避免速率限制
        except Exception as e:
            print(f"❌ Failed: {url} — {e}")
            fail += 1
    
    print(f"\n完成: {success}/{len(URLS)} 成功, {fail} 失败")

if __name__ == "__main__":
    submit_urls()
