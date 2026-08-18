# -*- coding: utf-8 -*-
"""测试 sk- API key 能否直接查用量"""
import re, urllib.request, urllib.error, json

raw = open(r'C:\Users\Administrator\.config\opencode\opencode.jsonc', encoding='utf-8').read()
key = re.search(r'"apiKey"\s*:\s*"([^"]+)"', raw).group(1)
print(f"key: sk-...{key[-4:]}")

op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

def probe(path, headers, method='GET'):
    req = urllib.request.Request('https://opencode.ai' + path, method=method)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36')
    req.add_header('Accept', 'application/json')
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        r = op.open(req, timeout=15)
        print(f"{method} {path} -> {r.status}: {r.read().decode('utf-8','ignore')[:300]}")
    except urllib.error.HTTPError as e:
        print(f"{method} {path} -> {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
    except Exception as e:
        print(f"{method} {path} -> ERR {e}")

for name, h in [
    ('bearer-sk', {'Authorization': f'Bearer {key}'}),
    ('raw-sk', {'Authorization': key}),
    ('x-api-key', {'X-API-Key': key}),
]:
    for p in ['/console/api/v1/usage/export', '/console/api/v1/usage', '/api/v1/usage/export', '/api/usage']:
        probe(p, h)
    print()

# zen 模型 API 头信息看有没有 usage hint
req = urllib.request.Request('https://opencode.ai/zen/v1/models')
req.add_header('User-Agent', 'Mozilla/5.0')
req.add_header('Authorization', f'Bearer {key}')
try:
    r = op.open(req, timeout=15)
    print(f"zen/v1/models -> {r.status}")
    for h in ['x-ratelimit-remaining', 'x-ratelimit-limit', 'x-credits', 'x-balance', 'x-usage']:
        print(f"  {h}: {r.headers.get(h)}")
except urllib.error.HTTPError as e:
    print(f"zen/v1/models -> {e.code}")