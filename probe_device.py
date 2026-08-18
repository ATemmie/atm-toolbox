# -*- coding: utf-8 -*-
"""探测 auth.opencode.ai 的登录端点（含 device flow）"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()

    api_hits = []
    page.on('request', lambda req: api_hits.append(req.url) if 'auth' in req.url.lower() or 'device' in req.url.lower() or 'token' in req.url.lower() or 'oauth' in req.url.lower() else None)

    page.goto('https://auth.opencode.ai', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(2000)
    print("=== auth.opencode.ai 页面 ===")
    print(page.inner_text('body')[:1000])
    print("\n=== 捕获请求 ===")
    for u in sorted(set(api_hits))[:30]:
        print(u)

    # 试探常见 device flow 路径
    for path in ['/device', '/device/code', '/oauth/device', '/cli', '/login/device', '/login/cli']:
        r = page.goto('https://auth.opencode.ai' + path, wait_until='domcontentloaded', timeout=20000)
        print(f"\n{path} -> {r.status if r else '?'} | {page.title()}")
        try:
            t = page.inner_text('body')[:300]
            print(t)
        except Exception:
            pass

    browser.close()