# -*- coding: utf-8 -*-
"""
登录 → 同一会话直接抓 workspace Go 页面用量（不依赖 cookie 重放）
用法: python login_and_fetch.py
1. 弹出浏览器，用户登录 opencode 控制台
2. 登录成功（URL 变 org_）后，自动导航到 workspace go 页面
3. 抓取页面文本 + 监听 API 响应 → 存 data/go_usage.json + console 截图
"""
import json, os, time, sys
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
OUT = os.path.join(BASE, 'data', 'go_usage.json')
WS_URL = 'https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go'

print("=" * 50)
print("🧰 ATM 工具箱 - 用量抓取（登录复用）")
print("=" * 50)
print("即将打开浏览器，请登录一次 opencode 控制台")
print("登录成功后我会自动去抓你的 Go 用量页面\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel='msedge', args=['--no-sandbox', '--start-maximized'])
    ctx = browser.new_context(viewport={'width': 1400, 'height': 950},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    page = ctx.new_page()

    api_hits = []
    def on_resp(resp):
        u = resp.url
        if any(k in u for k in ['usage', 'billing', 'budget', 'balance', 'credit', 'limit', 'quota', 'cost', 'spend', '/go']):
            try:
                body = resp.text()[:800]
            except Exception:
                body = ''
            hits = {'status': resp.status, 'url': u, 'body': body}
            api_hits.append(hits)
    page.on('response', on_resp)

    # 1. 登录
    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(2500)
    print("登录窗口已打开，请登录（GitHub/Google）…")

    logged_in = False
    for i in range(300):
        time.sleep(2)
        if 'console/org_' in page.url:
            logged_in = True
            print(f"\n✅ 登录成功！{page.url[:60]}")
            break
        if i % 30 == 0:
            print(f"  …等待中 ({i*2}s) {page.url[:60]}")

    if not logged_in:
        print("\n⚠️ 超时。你登录了吗？按 Enter 尝试继续…")
        input()

    # 保存 cookie 备份
    cookies = ctx.cookies()
    with open(os.path.join(BASE, 'data', 'console_cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"📎 已备份 {len(cookies)} 个 cookie")

    # 2. 导航到 workspace go 页面
    print("\n🚀 导航到 Go 用量页面…")
    page.goto(WS_URL, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text('body')
    print("=== 页面文本 ===")
    print(text[:2500])

    # 3. 汇总 API 响应
    print("\n=== 捕获的 API 响应 ===")
    seen = set()
    useful = []
    for h in api_hits:
        key = f"{h['status']} {h['url'][:100]}"
        if key not in seen:
            seen.add(key)
            print(f"\n[{h['status']}] {h['url']}")
            if h['status'] == 200 and h['body'] and 'font' not in h['url']:
                print(f"    {h['body'][:400]}")
                useful.append(h)
    if not api_hits:
        print("（无）")

    # 4. 存数据
    data = {
        'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'page_text': text[:5000],
        'api': api_hits,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 已保存 -> {OUT}")

    page.screenshot(path=os.path.join(BASE, 'go_page_usage.png'), full_page=True)
    print("📸 截图已保存 go_page_usage.png")
    browser.close()
    print("\n完成！数据拿到了。")