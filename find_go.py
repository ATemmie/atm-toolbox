# -*- coding: utf-8 -*-
"""抓 opencode.ai/zen 页面，找 Go 相关内容（导航/链接/块）"""
from playwright.sync_api import sync_playwright

URL = 'https://opencode.ai/zen'

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

    # 抓所有含 Go 文本的链接和按钮
    els = page.eval_on_selector_all('a, button, [role="tab"], [role="menuitem"], nav *', 
        'els => els.map(e => ({tag: e.tagName, text: (e.innerText||"").trim().slice(0,80), href: e.href||""}))')
    print("=== 导航/按钮元素 ===")
    for e in els:
        if e['text'] and ('Go' in e['text'] or 'go' in e['text'].lower() or 'zen' in e['text'].lower()):
            print(e)

    # 页面里搜 “Go” 出现处
    html = page.content()
    idxs = []
    start = 0
    while True:
        i = html.find('>Go<', start)
        if i == -1: break
        idxs.append(i)
        start = i + 4
    print(f"\n=== '>Go<' 出现 {len(idxs)} 次 ===")

    browser.close()