# -*- coding: utf-8 -*-
"""带 cookie 抓 workspace 页面 HTML，找 JS bundle"""
import json, urllib.request, urllib.error, re

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
cookies = json.load(open(COOKIE_FILE, encoding='utf-8'))
ch = '; '.join(f"{c['name']}={c['value']}" for c in cookies if c.get('name'))

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

req = urllib.request.Request('https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go')
req.add_header('User-Agent', UA)
req.add_header('Cookie', ch)
try:
    r = op.open(req, timeout=20)
    body = r.read().decode('utf-8', 'ignore')
    print(f"status {r.status}, len {len(body)}, final url: {r.geturl()}")
    for m in re.finditer(r'(?:src|href)="([^"]+\.(?:js|mjs)[^"]*)"', body):
        print("JS:", m.group(1))
    if not re.search(r'\.js', body):
        print("无 JS 资源，可能还是登录页")
        print(body[:400])
except urllib.error.HTTPError as e:
    print(f"ERR {e.code}")
except Exception as e:
    print(f"ERR {e}")