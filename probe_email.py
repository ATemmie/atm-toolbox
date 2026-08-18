# -*- coding: utf-8 -*-
"""探测 console email 登录端点"""
import urllib.request, urllib.error, json

op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36'

def probe(path, method='GET', payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request('https://opencode.ai' + path, data=data, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console')
    if payload:
        req.add_header('Content-Type', 'application/json')
    try:
        r = op.open(req, timeout=15)
        print(f"{method} {path} -> {r.status}: {r.read().decode('utf-8','ignore')[:250]}")
    except urllib.error.HTTPError as e:
        print(f"{method} {path} -> {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
    except Exception as e:
        print(f"{method} {path} -> ERR {type(e).__name__} {e}")

# email 登录相关端点猜一遍
paths = [
    ('/console/api/login', 'GET', None),
    ('/console/api/login', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/auth/login', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/auth/email', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/email/login', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/session', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/sessions', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/auth/session', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/auth/callback', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/signin', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/sign-in', 'POST', {'email': 't', 'password': 't'}),
    ('/console/api/auth?email=1', 'GET', None),
    ('/console/api/v1/auth/email', 'POST', {'email': 't', 'password': 't'}),
]
for p, m, pl in paths:
    probe(p, m, pl)