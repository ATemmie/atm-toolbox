# -*- coding: utf-8 -*-
"""提取 JS 中 API 路径的上下文（确认 base path）"""
from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()
    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=45000)
    page.wait_for_timeout(1500)

    url = 'https://opencode.ai/console/assets/index-BpgkP-2x.js'
    resp = page.request.get(url)
    body = resp.text()
    print(f"JS 大小: {len(body)}")

    # 找 apiFetch / fetch 调用附近的 baseURL 定义
    for kw in ['baseURL', 'API_URL', 'apiUrl', 'console/api', '/api/', 'apiFetch', 'api(']:
        idxs = [m.start() for m in re.finditer(re.escape(kw), body)]
        if idxs:
            print(f"\n=== '{kw}' 出现 {len(idxs)} 次，前 3 处上下文 ===")
            for i in idxs[:3]:
                ctx_s = body[max(0, i-120):i+180]
                print("   ...", ctx_s.replace('\n', ' ')[:280])
    browser.close()