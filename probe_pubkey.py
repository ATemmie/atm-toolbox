# -*- coding: utf-8 -*-
"""用 sk- API key + x-org-id 打正确的 usage/export 端点
JS 注释: "bound to the service API key" - 这是给 API key 用的端点！"""
import re, urllib.request, urllib.error, json

raw = open(r'C:\Users\Administrator\.config\opencode\opencode.jsonc', encoding='utf-8').read()
key = re.search(r'"apiKey"\s*:\s*"([^"]+)"', raw).group(1)
ORG = 'org_01M0A41EXB0YVXZ5A05Q7P1SGN'
print(f"key: sk-...{key[-4:]}")

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

def probe(path, host='https://opencode.ai', headers=None):
    req = urllib.request.Request(host + path)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json, text/csv, */*')
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('x-org-id', ORG)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        r = op.open(req, timeout=20)
        print(f"{path} [{host}] -> {r.status}: {r.read().decode('utf-8','ignore')[:400]}")
    except urllib.error.HTTPError as e:
        print(f"{path} [{host}] -> {e.code}: {e.read().decode('utf-8','ignore')[:250]}")
    except Exception as e:
        print(f"{path} [{host}] -> ERR {type(e).__name__}")

# 公开 API key 端点（JS 注释说的 service API key 绑定）
for host in ['https://opencode.ai', 'https://api.opencode.ai']:
    for q in ['scope=organization', 'scope=organization&range=week', 'scope=organization&range=month']:
        probe(f'/api/v1/usage/export?{q}', host)
    probe('/api/v1/usage/export', host, headers={'Content-Type': 'application/json'})
    print()