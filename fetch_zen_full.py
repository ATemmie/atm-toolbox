# -*- coding: utf-8 -*-
"""抓取 zen docs 全文存盘"""
from playwright.sync_api import sync_playwright

URL = 'https://opencode.ai/docs/zh-cn/zen/'
OUT = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\zen_docs_full.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(
        viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'},
    )
    page = ctx.new_page()
    page.goto(URL, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(3000)
    text = page.inner_text('body')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"已保存 {len(text)} 字符 -> {OUT}")
    browser.close()