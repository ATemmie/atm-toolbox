# -*- coding: utf-8 -*-
"""带 x-org-id header 探测用量端点"""
import json, urllib.request, urllib.error

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
ORG = 'org_01M0A41EXB0YVXZ5A05Q7P1SGN'

cookies = json.load(open(COOKIE_FILE, encoding='utf-8'))
ch = '; '.join(f"{c['name']}={c['value']}" for c in cookies if c.get('name'))

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

def probe(path, method='GET', extra=None):
    req = urllib.request.Request('https://opencode.ai' + path, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console/' + ORG)
    req.add_header('Cookie', ch)
    req.add_header('x-org-id', ORG)
    for k, v in (extra or {}).items():
        req.add_header(k, v)
    try:
        r = op.open(req, timeout=15)
        print(f"{method} {path} -> {r.status}: {r.read().decode('utf-8','ignore')[:400]}")
    except urllib.error.HTTPError as e:
        print(f"{method} {path} -> {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
    except Exception as e:
        print(f"{method} {path} -> ERR {type(e).__name__}")

probe('/console/api/usage/export')
probe('/console/api/usage')
probe('/console/api/billing')
probe('/console/api/budgets')
probe('/console/api/usage/export', method='POST', extra={'Content-Type': 'application/json'})