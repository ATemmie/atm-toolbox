# -*- coding: utf-8 -*-
"""带完整参数调用 usage/export 端点"""
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
    req.add_header('Accept', 'application/json, text/csv, */*')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console/' + ORG)
    req.add_header('Cookie', ch)
    req.add_header('x-org-id', ORG)
    try:
        r = op.open(req, timeout=20)
        body = r.read().decode('utf-8', 'ignore')[:600]
        print(f"{path} -> {r.status}: {body}")
    except urllib.error.HTTPError as e:
        print(f"{path} -> {e.code}: {e.read().decode('utf-8','ignore')[:250]}")
    except Exception as e:
        print(f"{path} -> ERR {type(e).__name__} {e}")

# range 枚举：week/weekly/month/hour 等常见值
for rng in ['week', 'weekly', 'month', 'monthly', '30d', '7d', '1d', 'day', 'today', 'this_week', 'this_month', 'last_30_days']:
    probe(f'/console/api/v1/usage/export?scope=organization&range={rng}')

print("\n--- 无 range ---")
probe('/console/api/v1/usage/export?scope=organization')
print("\n--- 试 organizations/usage 常见路径 ---")
for p in ['/console/api/organizations/usage', '/console/api/org/usage', '/console/api/usage?scope=organization']:
    probe(p)