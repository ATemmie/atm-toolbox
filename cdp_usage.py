# -*- coding: utf-8 -*-
"""CDP: 进 workspace → 点「使用量」→ 抓全部 API 调用与数据"""
import json, time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    hits = []
    def on_resp(resp):
        u = resp.url
        if '/api/' in u or '/console/' in u:
            try:
                body = resp.text()[:800]
            except Exception:
                body = ''
            hits.append({'status': resp.status, 'url': u, 'body': body})
    page.on('response', on_resp)

    # 确保在 workspace
    if 'workspace' not in page.url:
        page.goto('https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go', wait_until='networkidle', timeout=60000)
        page.wait_for_timeout(4000)

    print(f"URL: {page.url[:90]}")

    # 找并点击「使用量」tab
    clicked = False
    for sel in ['text=使用量', 'text=Usage', 'text=用量']:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                el.click(timeout=5000)
                clicked = True
                print(f"点击了: {sel}")
                break
        except Exception:
            pass
    if not clicked:
        print("未找到用量 tab，尝试滚动页面找…")
        for _ in range(5):
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(500)

    page.wait_for_timeout(6000)

    print("\n=== 页面文本 ===")
    print(page.inner_text('body')[:2500])

    print("\n=== API 调用 ===")
    seen = set()
    for h in hits:
        key = f"{h['status']} {h['url'][:130]}"
        if key not in seen:
            seen.add(key)
            print(f"\n[{h['status']}] {h['url']}")
            if h['status'] == 200 and h['body'] and 'font' not in h['url']:
                print(f"    {h['body'][:400]}")

    page.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\ws_usage_live.png')
    print("\n📸 截图 ws_usage_live.png")
    print("完成（浏览器保持打开）")