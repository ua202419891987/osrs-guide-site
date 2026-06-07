import json, urllib.request, urllib.error, os

# Read HTML content
with open(r'C:\Users\Lenovo\osrs-guide-site\medium-osrs-money-making-2026.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read API key if exists
api_key = ""
cred_path = os.path.expanduser('~/.shippage/credentials.json')
if os.path.exists(cred_path):
    with open(cred_path) as f:
        cred = json.load(f)
        api_key = cred.get('api_key', '')

# Prepare request
url = 'https://shippage.ai/v1/publish'
payload = json.dumps({
    'html': html_content,
    'title': 'OSRS Money Making Guide 2026'
}).encode('utf-8')

req = urllib.request.Request(
    url,
    data=payload,
    headers={
        'Content-Type': 'application/json',
        'X-Skill-Version': '1.2.0',
        **({'Authorization': f'Bearer {api_key}'} if api_key else {})
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print(json.dumps(result, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
