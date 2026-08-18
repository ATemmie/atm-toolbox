# -*- coding: utf-8 -*-
"""打开 workspace go 页面，监听所有 console API 请求（找用量占比数据源）"""
import json, os
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
        if '/console/api/' in u or '/api/' in u:
            body = ''
            try:
                body = resp.text()[:500]
            except Exception:
                pass
            calls.append({'status': resp.status, 'url': u, 'body': body})
    page.on('response', on_resp)

    page.goto(URL, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(5000)

    print("=== 页面文本 ===")
    print(page.inner_text('body')[:1500])

    print("\n=== console API 调用 ===")
    seen = set()
    for c in calls:
        key = f"{c['status']} {c['url'][:130]}"
        if key not in seen:
            seen.add(key)
            print(f"\n[{c['status']}] {c['url']}")
            if c['body'] and c['status'] == 200:
                print(f"    {c['body'][:350]}")
    print(f"\n共 {len(calls)} 次 API 调用, 独特 {len(seen)} 个")

    browser.close()