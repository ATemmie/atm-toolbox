# -*- coding: utf-8 -*-
"""从 console JS 挖 usage/export 端点需要的参数"""
from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()
    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(1000)
    url = 'https://opencode.ai/console/assets/index-BpgkP-2x.js'
    body = page.request.get(url).text()

    # 找 usage export 上下文
    for m in re.finditer(r'usage/export', body):
        s = body[max(0, m.start()-400):m.start()+400]
        print("======")
        print(s[:800].replace('\n', ' '))

    # 找 x-org-id header 定义
    print("\n=== x-org-id 相关 ===")
    for m in list(re.finditer(r'x-org-id|orgId|org_id', body))[:10]:
        s = body[max(0, m.start()-150):m.start()+200]
        print("---")
        print(s.replace('\n', ' ')[:350])

    browser.close()