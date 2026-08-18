# -*- coding: utf-8 -*-
"""探测 /api/billing 等：无 cookie vs 带 sk key 的响应差异"""
import json, re, urllib.request

cfg_path = r'C:\Users\Administrator\.config\opencode\opencode.jsonc'
with open(cfg_path, encoding='utf-8') as f:
    raw = f.read()
m = re.search(r'"apiKey"\s*:\s*"([^"]+)"', raw)
KEY = m.group(1)

PROXY = 'http://127.0.0.1:7890'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def probe(path, extra_headers=None):
    url = 'https://opencode.ai' + path
    req = urllib.request.Request(url)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console')
    for k, v in (extra_headers or {}).items():
        req.add_header(k, v)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))
    try:
        r = opener.open(req, timeout=15)
        body = r.read().decode('utf-8', 'ignore')[:500]
        print(f"{path} -> {r.status}: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')[:300]
        print(f"{path} -> {e.code}: {body}")
    except Exception as e:
        print(f"{path} -> ERR {e}")

print("== 无认证 ==")
probe('/api/billing')
probe('/api/usage')
print("\n== 带 Bearer sk- ==")
probe('/api/billing', {'Authorization': f'Bearer {KEY}'})
probe('/api/usage', {'Authorization': f'Bearer {KEY}'})
print("\n== 带 Authorization: sk- 裸值 ==")
probe('/api/billing', {'Authorization': KEY})
probe('/api/usage', {'Authorization': KEY})