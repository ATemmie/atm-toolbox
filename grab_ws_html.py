# -*- coding: utf-8 -*-
"""抓 workspace 页面 HTML 找 JS bundle 与 API 线索"""
import urllib.request, re

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

req = urllib.request.Request('https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go')
req.add_header('User-Agent', UA)
try:
    r = op.open(req, timeout=20)
    body = r.read().decode('utf-8', 'ignore')
    print(f"status {r.status}, len {len(body)}")
    # JS 资源
    for m in re.finditer(r'src="([^"]+\.js[^"]*)"', body):
        print("JS:", m.group(1))
    # 内联脚本中的线索
    for m in re.finditer(r'<script[^>]*>(.{0,200})</script>', body, re.S):
        t = m.group(1).strip()
        if t and 'src=' not in t:
            print("INLINE:", t[:200])
    print("\n=== body 前 800 ===")
    print(body[:800])
except urllib.error.HTTPError as e:
    print(f"ERR {e.code}: {e.read().decode('utf-8','ignore')[:300]}")
except Exception as e:
    print(f"ERR {e}")