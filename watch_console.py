# -*- coding: utf-8 -*-
"""用已保存 cookie 打开控制台，监听页面真实调用的 usage/billing API"""
import json, os
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
ORG = 'org_01M0A41EXB0YVXZ5A05Q7P1SGN'

cookies = json.load(open(COOKIE_FILE, encoding='utf-8'))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    # 注入 cookie
    ctx.add_cookies(cookies)
    page = ctx.new_page()

    calls = []
    def on_resp(resp):
        u = resp.url
        if any(k in u for k in ['usage', 'billing', 'budget', 'balance', 'credit', 'limit', 'quota', 'cost', 'spend']):
            body = ''
            try:
                body = resp.text()[:400]
            except Exception:
                pass
            calls.append(f"{resp.status} {resp.request.method} {u}\n    {body}")
    page.on('response', on_resp)

    page.goto('https://opencode.ai/console/' + ORG, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(4000)

    # 页面文本
    print("=== 页面可见内容 ===")
    print(page.inner_text('body')[:1200])

    print("\n=== 捕获的用量 API 调用 ===")
    seen = set()
    for c in calls:
        if c not in seen:
            seen.add(c)
            print(c)
    if not calls:
        print("（无）——可能页面需要点击进入用量页")

    # 找所有 visible 链接/按钮
    links = page.eval_on_selector_all('a, button, [role=tab]', 'els => els.map(e => (e.innerText||"").trim().slice(0,40))')
    print("\n=== 页面可点元素 ===")
    for l in links:
        if l and any(k in l.lower() for k in ['usage', 'billing', 'budget', 'cost', 'limit', 'credit', '用量', '费用', '余额']):
            print(" ", l)

    browser.close()