# -*- coding: utf-8 -*-
"""抓取 opencode.ai/zh/go 页面全文 + 链接"""
from playwright.sync_api import sync_playwright

URL = 'https://opencode.ai/zh/go'
OUT = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\zen_go_full.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(
        viewport={'width': 1400, 'height': 2500},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'},
    )
    page = ctx.new_page()
    page.goto(URL, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(2000)
    text = page.inner_text('body')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"已保存 {len(text)} 字符")
    print("===== 前 3000 字 =====")
    print(text[:3000])

    links = page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
    print("\n===== 关键链接 =====")
    for l in sorted(set(links)):
        if any(k in l.lower() for k in ['go', 'zen', 'plan', 'pric', 'bill', 'usage', 'dashboard', 'console', 'auth']):
            print(l)
    page.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\zen_go.png', full_page=True)
    browser.close()