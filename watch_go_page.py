# -*- coding: utf-8 -*-
"""用 cookie 打开用户给的 workspace Go 页面，监听 API 调用"""
import json
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
URL = 'https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go'

cookies = json.load(open(COOKIE_FILE, encoding='utf-8'))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    ctx.add_cookies(cookies)
    page = ctx.new_page()

    calls = []
    def on_resp(resp):
        u = resp.url
        if 'api' in u and any(k in u for k in ['usage', 'billing', 'budget', 'balance', 'credit', 'limit', 'quota', 'cost', 'spend', 'go', 'plan', 'sub']):
            body = ''
            try:
                body = resp.text()[:500]
            except Exception:
                pass
            calls.append(f"{resp.status} {resp.request.method} {u}\n    {body}")
    page.on('response', on_resp)

    page.goto(URL, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(4000)

    print("=== 页面内容 ===")
    print(page.inner_text('body')[:2000])

    print("\n=== API 调用 ===")
    seen = set()
    for c in calls:
        if c not in seen:
            seen.add(c)
            print(c)
    if not calls:
        print("（无用量 API 调用）")

    links = page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
    api_links = [l for l in set(links) if any(k in l for k in ['usage', 'billing', 'budget', 'cost', 'limit', 'api'])]
    print("\n=== API 相关链接 ===")
    for l in api_links[:15]:
        print(l)

    page.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\go_page.png', full_page=True)
    browser.close()