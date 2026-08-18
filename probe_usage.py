# -*- coding: utf-8 -*-
"""用配置里的 API key 探测 opencode 用量/余额查询端点（key 从本地配置读取，不打印）"""
import json, re, os, subprocess, sys

# 从 opencode.jsonc 提取 apiKey（redacted 不打印）
cfg_path = r'C:\Users\Administrator\.config\opencode\opencode.jsonc'
with open(cfg_path, encoding='utf-8') as f:
    raw = f.read()

m = re.search(r'"apiKey"\s*:\s*"([^"]+)"', raw)
if not m:
    print('未找到 apiKey')
    sys.exit(1)
KEY = m.group(1)
print(f"从配置读取 apiKey (sk-…{KEY[-4:]})")

import urllib.request

PROXY = 'http://127.0.0.1:7890'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))

def probe(path, auth='bearer'):
    url = 'https://opencode.ai' + path
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console')
    if auth == 'bearer':
        req.add_header('Authorization', f'Bearer {KEY}')
    elif auth == 'raw':
        req.add_header('Authorization', KEY)
    elif auth == 'x-api-key':
        req.add_header('X-API-Key', KEY)
    try:
        r = opener.open(req, timeout=15)
        body = r.read().decode('utf-8', 'ignore')[:400]
        print(f"{path} [{auth}] -> {r.status}: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')[:200]
        print(f"{path} [{auth}] -> {e.code}: {body}")
    except Exception as e:
        print(f"{path} [{auth}] -> ERR {e}")

for path in ['/console/api/usage', '/console/api/usage/current', '/console/api/billing',
             '/console/api/balance', '/console/api/me', '/console/api/account',
             '/console/api/limits', '/console/api/plan', '/console/api/credits',
             '/zen/v1/usage', '/zen/v1/balance', '/zen/v1/me']:
    probe(path)