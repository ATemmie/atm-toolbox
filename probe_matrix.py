# -*- coding: utf-8 -*-
"""/console/api/usage/export 全参数矩阵（cookie + x-org-id 已通过认证，差参数）"""
import json, urllib.request, urllib.error

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
ORG = 'org_01M0A41EXB0YVXZ5A05Q7P1SGN'

cookies = json.load(open(COOKIE_FILE, encoding='utf-8'))
ch = '; '.join(f"{c['name']}={c['value']}" for c in cookies if c.get('name'))

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

def probe(path, method='GET', payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request('https://opencode.ai' + path, data=data, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json, text/csv, */*')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console/' + ORG)
    req.add_header('Cookie', ch)
    req.add_header('x-org-id', ORG)
    if payload:
        req.add_header('Content-Type', 'application/json')
    try:
        r = op.open(req, timeout=20)
        body = r.read().decode('utf-8', 'ignore')[:300]
        print(f"{method} {path} -> {r.status}: {body}")
    except urllib.error.HTTPError as e:
        print(f"{method} {path} -> {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
    except Exception as e:
        print(f"{method} {path} -> ERR {type(e).__name__}")

# cookie 会话端点 + 各种参数猜
qs = [
    '', '?scope=organization', '?scope=member', '?scope=service_account',
    '?scope=organization&range=week', '?scope=organization&range=month',
    '?range=week', '?range=month', '?range=30d', '?range=7d', '?range=1d',
    '?from=2026-01-01&to=2026-12-31', '?start=2026-01-01&end=2026-01-01',
    '?since=30d', '?period=month', '?timeframe=month', '?interval=month',
    '?metric=cost', '?metric=requests', '?metric=tokens',
    '?scope=organization&range=month&metric=cost',
    '?scope=organization&range=month&metric=requests',
]
for q in qs:
    probe('/console/api/usage/export' + q)

print("\n--- POST body 变体 ---")
for payload in [
    {'scope': 'organization', 'range': 'month'},
    {'scope': 'organization'},
    {'start': '2026-07-01', 'end': '2026-08-18'},
    {'granularity': 'month'},
]:
    probe('/console/api/usage/export', method='POST', payload=payload)

print("\n--- 相关端点 ---")
for p in ['/console/api/usage/summary', '/console/api/usage/current', '/console/api/usage/report',
          '/console/api/usage/stats', '/console/api/usage/totals', '/console/api/usage/overview',
          '/console/api/usage?scope=organization', '/console/api/usage?scope=organization&range=month']:
    probe(p)