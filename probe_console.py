# -*- coding: utf-8 -*-
"""抓 opencode console 页面 + 监听 API 请求"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()

    api_calls = []
    page.on('request', lambda req: api_calls.append(f"{req.method} {req.url}") if any(k in req.url for k in ['api', 'usage', 'billing', 'credit', 'balance', 'limit']) else None)

    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(2500)
    text = page.inner_text('body')
    print("=== /console 页面 ===")
    print(text[:1500])
    print("\n=== 捕获的 API 请求 ===")
    seen = set()
    for c in api_calls:
        if c not in seen:
            seen.add(c)
            print(c)
    browser.close()