# -*- coding: utf-8 -*-
"""探测 /console/api/ 前缀下的真实端点（GET/POST/方法矩阵）"""
import urllib.request, json, re

cfg_path = r'C:\Users\Administrator\.config\opencode\opencode.jsonc'
with open(cfg_path, encoding='utf-8') as f:
    raw = f.read()
m = re.search(r'"apiKey"\s*:\s*"([^"]+)"', raw)
KEY = m.group(1) if m else None

PROXY = 'http://127.0.0.1:7890'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))

def probe(path, method='GET', headers=None):
    url = 'https://opencode.ai' + path
    req = urllib.request.Request(url, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console')
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        r = opener.open(req, timeout=15)
        body = r.read().decode('utf-8', 'ignore')[:400]
        print(f"{method} {path} -> {r.status}: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')[:250]
        print(f"{method} {path} -> {e.code}: {body}")
    except Exception as e:
        print(f"{method} {path} -> ERR {type(e).__name__}")

# 已知工作的公开端点
probe('/console/api/setup/status')
probe('/console/api/sso/discover')
# 用量相关 - GET
for p in ['/console/api/usage', '/console/api/billing', '/console/api/usage/current',
          '/console/api/v1/usage/export', '/console/api/me', '/console/api/account']:
    probe(p)
# 带 key
if KEY:
    probe('/console/api/usage', headers={'Authorization': f'Bearer {KEY}'})
    probe('/console/api/usage', headers={'X-Zen-Api-Key': KEY})
# POST 试试
probe('/console/api/usage', method='POST')
probe('/console/api/billing', method='POST')