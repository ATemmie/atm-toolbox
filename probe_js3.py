# -*- coding: utf-8 -*-
"""深挖 console JS 的 API base URL 构造逻辑"""
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
    body = page.request.get(url).text()

    # 找 fetch 封装/API base 定义
    patterns = [
        r'["\'](/api/[^"\']+)["\']',
        r'["\'](https?://[^"\']*api[^"\']*)["\']',
        r'(prefix|baseURL|baseUrl|apiUrl|API_URL)\s*[:=]\s*["\']([^"\']+)["\']',
        r'"/[a-z-]+/api/',
    ]
    seen = set()
    for pat in patterns:
        for m in re.finditer(pat, body):
            s = m.group(0)[:120]
            if s not in seen:
                seen.add(s)
                print(s)

    # 找 useQuery/useFetch 调用附近
    print("\n=== '/api/' 所有出现上下文（含前 60 字符）===")
    for m in list(re.finditer(r'/api/', body))[:15]:
        s = body[max(0, m.start()-80):m.start()+60]
        print("   ...", s.replace('\n', ' ')[:140])
    browser.close()