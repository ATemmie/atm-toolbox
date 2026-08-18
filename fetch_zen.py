# -*- coding: utf-8 -*-
"""用 Playwright 抓取 opencode.ai/zen 页面内容（含 JS 渲染）"""
import json, sys
from playwright.sync_api import sync_playwright

URL = 'https://opencode.ai/zen'

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

    # 整个页面的文本
    text = page.inner_text('body')
    print("=== BODY TEXT ===")
    print(text[:6000])

    # 所有链接
    links = page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
    zen_links = [l for l in links if any(k in l.lower() for k in ['zen', 'plan', 'pricing', 'billing', 'usage', 'dashboard', 'console'])]
    print("\n=== ZEN/PLAN LINKS ===")
    for l in sorted(set(zen_links)):
        print(l)

    # 截图存下来
    page.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\opencode_zen.png', full_page=True)
    print("\n截图已保存")
    browser.close()