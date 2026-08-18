# -*- coding: utf-8 -*-
"""找 opencode 控制台 URL 和可能的用量 API"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()

    # 1. 抓 auth 页找控制台链接
    page.goto('https://opencode.ai/auth', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(2000)
    text = page.inner_text('body')
    print("=== /auth 页面 ===")
    print(text[:800])
    links = page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
    print("=== 链接 ===")
    for l in sorted(set(links)):
        if any(k in l.lower() for k in ['dashboard', 'console', 'usage', 'billing', 'account', 'auth', 'settings', 'app']):
            print(l)

    # 2. 试常见控制台路径
    for path in ['/dashboard', '/console', '/settings', '/account', '/app', '/usage', '/billing']:
        r = page.goto('https://opencode.ai' + path, wait_until='domcontentloaded', timeout=20000)
        status = r.status if r else '?'
        title = page.title()
        print(f"/{path} -> {status} | {title}")

    browser.close()