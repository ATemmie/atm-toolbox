# -*- coding: utf-8 -*-
"""探测 /console/api/v1/ 系端点的存在性（401=存在需登录, 404=不存在）"""
import urllib.request

PROXY = 'http://127.0.0.1:7890'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))

def probe(path, method='GET'):
    url = 'https://opencode.ai' + path
    req = urllib.request.Request(url, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console')
    try:
        r = opener.open(req, timeout=15)
        body = r.read().decode('utf-8', 'ignore')[:200]
        print(f"{method} {path} -> {r.status}: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')[:150]
        print(f"{method} {path} -> {e.code}: {body}")
    except Exception as e:
        print(f"{method} {path} -> ERR {type(e).__name__}")

paths = [
    '/console/api/v1/usage',
    '/console/api/v1/usage/export',
    '/console/api/v1/usage/current',
    '/console/api/v1/billing',
    '/console/api/v1/billing/balance',
    '/console/api/v1/me',
    '/console/api/v1/account',
    '/console/api/v1/limits',
    '/console/api/v1/plan',
    '/console/api/v1/credits',
    '/console/api/v1/orgs',
    '/console/api/v1/members',
    '/console/api/v1/service-accounts',
    '/console/api/v1/entitlements',
    '/console/api/v1/balances',
    '/console/api/v1/subscription',
]
for p in paths:
    probe(p)
print("\n--- POST ---")
for p in ['/console/api/v1/usage', '/console/api/v1/usage/export']:
    probe(p, method='POST')