# -*- coding: utf-8 -*-
"""抓 console 页面 JS 资源，搜索 API 路由关键字"""
from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()
    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(2000)

    # 收集所有 JS
    js_urls = page.eval_on_selector_all('script[src]', 'els => els.map(e => e.src)')
    print(f"找到 {len(js_urls)} 个 JS:")
    for u in js_urls[:10]:
        print(' ', u)

    # 抓全部 JS 内容搜 API 路径
    kws = ['usage', 'billing', 'balance', 'credit', 'limit', 'quota']
    for u in js_urls:
        try:
            resp = page.request.get(u)
            if resp.ok:
                body = resp.text()
                hits = set()
                for kw in kws:
                    for m in re.finditer(r'["\'`](/?(?:api|console|v1)[^"\'`]*' + kw + r'[^"\'`]*)["\'`]', body, re.I):
                        hits.add(m.group(1))
                if hits:
                    print(f"\n=== {u.split('/')[-1][:50]} ===")
                    for h in sorted(hits):
                        print(' ', h)
        except Exception as e:
            pass
    browser.close()