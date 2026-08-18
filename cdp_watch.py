# -*- coding: utf-8 -*-
"""通过 CDP 连接 Edge (9223)，在当前标签页导航到 workspace/go，监听 API"""
import json, time
from playwright.sync_api import sync_playwright

URL = 'https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go'

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    print(f"当前 URL: {page.url[:100]}")
    print("等待授权完成（如果停在登录/授权页，请在你屏幕上的 Edge 窗口操作）…")

    # 等待导航到目标页面（最多 90 秒，让用户点授权）
    for i in range(45):
        time.sleep(2)
        if 'workspace' in page.url and '/auth' not in page.url:
            print(f"✅ 已进入: {page.url[:90]}")
            break
        if i % 10 == 0:
            print(f"  …等待中 ({i*2}s) 当前: {page.url[:80]}")

    # 开始监听 API
    hits = []
    def on_resp(resp):
        u = resp.url
        if any(k in u for k in ['usage', 'limit', 'quota', 'billing', 'budget', 'balance', 'credit', 'rolling', 'api']):
            try:
                body = resp.text()[:600]
            except Exception:
                body = ''
            hits.append({'status': resp.status, 'url': u, 'body': body})
    page.on('response', on_resp)

    # 刷新页面触发数据加载
    page.reload(wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(6000)

    print("\n=== 页面文本 ===")
    print(page.inner_text('body')[:1800])

    print("\n=== API 响应 ===")
    seen = set()
    for h in hits:
        key = f"{h['status']} {h['url'][:120]}"
        if key not in seen:
            seen.add(key)
            print(f"\n[{h['status']}] {h['url']}")
            if h['status'] == 200 and h['body']:
                print(f"    {h['body'][:400]}")

    page.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\ws_live.png')
    print("\n📸 截图已保存 ws_live.png")

    # 保留浏览器不关（用户在用它）
    print("完成（浏览器保持打开）")