# -*- coding: utf-8 -*-
"""查 console JS 认证 middleware (Jt) 与 cookie/token 逻辑 + /api/config 是否公开"""
from playwright.sync_api import sync_playwright
import re, urllib.request

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()
    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(1000)
    body = page.request.get('https://opencode.ai/console/assets/index-BpgkP-2x.js').text()

    # 找 Jt middleware 定义
    for pat in [r'Jt\s*=\s*[^;]{0,200}', r'const Jt[^;]{0,200}', r'middleware\(Jt\)[^;]{0,80}']:
        for m in list(re.finditer(pat, body))[:3]:
            print("Jt:", m.group(0)[:220].replace('\n', ' '))
    browser.close()

# 直接 GET /api/config 看是否公开（不需要登录的配置接口）
print("\n=== GET /api/config ===")
PROXY = 'http://127.0.0.1:7890'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36'
req = urllib.request.Request('https://opencode.ai/api/config')
req.add_header('User-Agent', UA)
req.add_header('Accept', 'application/json')
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))
try:
    r = opener.open(req, timeout=15)
    body = r.read().decode('utf-8', 'ignore')[:600]
    print(f"-> {r.status}: {body}")
except urllib.error.HTTPError as e:
    print(f"-> {e.code}: {e.read().decode('utf-8','ignore')[:300]}")
except Exception as e:
    print(f"-> ERR {e}")