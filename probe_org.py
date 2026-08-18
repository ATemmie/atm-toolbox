# -*- coding: utf-8 -*-
"""用已保存的登录 cookie + org id 探测用量端点"""
import json, urllib.request, urllib.error

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
ORG = 'org_01M0A41EXB0YVXZ5A05Q7P1SGN'

cookies = json.load(open(COOKIE_FILE, encoding='utf-8'))
ch = '; '.join(f"{c['name']}={c['value']}" for c in cookies if c.get('name'))

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

def probe(path, method='GET'):
    req = urllib.request.Request('https://opencode.ai' + path, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console/' + ORG)
    req.add_header('Cookie', ch)
    try:
        r = op.open(req, timeout=15)
        print(f"{method} {path} -> {r.status}: {r.read().decode('utf-8','ignore')[:350]}")
    except urllib.error.HTTPError as e:
        print(f"{method} {path} -> {e.code}: {e.read().decode('utf-8','ignore')[:150]}")
    except Exception as e:
        print(f"{method} {path} -> ERR {type(e).__name__}")

# org 前缀 + v1 前缀 + 裸路径，全部扫一遍
paths = [
    f'/console/api/orgs/{ORG}/usage',
    f'/console/api/orgs/{ORG}/usage/export',
    f'/console/api/orgs/{ORG}/billing',
    f'/console/api/orgs/{ORG}/budgets',
    f'/console/api/orgs/{ORG}/limits',
    f'/console/api/orgs/{ORG}',
    f'/console/api/orgs/{ORG}/members',
    '/console/api/orgs',
    '/console/api/usage/export',
    '/console/api/v1/usage/export',
    f'/console/api/orgs/{ORG}/usage/export',
    f'/console/api/orgs/{ORG}/credits',
    f'/console/api/orgs/{ORG}/balance',
    f'/console/api/orgs/{ORG}/plan',
    f'/console/api/orgs/{ORG}/subscription',
    '/console/api/me',
    '/console/api/v1/me',
]
for p in paths:
    probe(p)
print()
probe('/console/api/usage/export', method='POST')