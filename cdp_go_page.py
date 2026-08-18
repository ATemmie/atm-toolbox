# -*- coding: utf-8 -*-
"""CDP: 导航到 workspace/go 子页面，抓用量占比"""
import json, time, os, re
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
OUT = os.path.join(BASE, 'data', 'ws_go_page.json')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    page.goto('https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go', wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text('body')
    print("=== /go 页面文本 ===")
    print(text[:4000])

    data = {
        'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'url': page.url,
        'text': text[:15000],
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 保存 -> {OUT}")

    page.screenshot(path=os.path.join(BASE, 'ws_go_page.png'), full_page=True)
    print("📸 ws_go_page.png")