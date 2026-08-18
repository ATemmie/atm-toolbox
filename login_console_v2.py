# -*- coding: utf-8 -*-
"""
OpenCode Console 登录助手 v2（复用用户 Edge 会话）
- 用用户的 Edge profile 打开（保留 GitHub/Google 登录态）
- 等真正登录成功（usage API 通了）才保存
"""
import json, os, time
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = os.path.join(BASE, 'data', 'console_cookies.json')
EDGE_USER = r'C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data'

print("=" * 50)
print("🧰 ATM 工具箱 - 登录助手 v2（复用 Edge 会话）")
print("=" * 50)
print("即将用 Edge 打开控制台，你的登录态在里面，可能直接就是登录好的！")
print()

# 用系统 Edge 的可执行文件 + 用户会话目录
edge_path = None
for cand in [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
]:
    if os.path.exists(cand):
        edge_path = cand
        break
if not edge_path:
    print("❌ 找不到 Edge")
    raise SystemExit(1)
print(f"使用 Edge: {edge_path}")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        EDGE_USER,
        executable_path=edge_path,
        headless=False,
        args=['--no-sandbox', '--start-maximized', '--disable-features=msEdgeSidebarV2'],
        proxy={'server': 'http://127.0.0.1:7890'},
        viewport={'width': 1280, 'height': 900},
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    usage_hits = []
    page.on('response', lambda resp: usage_hits.append(resp.status)
            if 'usage' in resp.url or 'billing' in resp.url else None)

    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(2500)

    text = page.inner_text('body')[:400]
    print("=== 当前页面内容 ===")
    print(text)
    print()

    if 'Continue with' in text or 'Log in' in text:
        print("⚠️ 还是登录页。请在浏览器里完成登录（优先 GitHub）…")
        print("（我会一直等到你真正登录成功，最多 10 分钟）")
        logged_in = False
        for i in range(300):
            time.sleep(2)
            try:
                r = page.request.get('https://opencode.ai/console/api/v1/usage/export')
                if r.status not in (401, 404):
                    logged_in = True
                    print(f"\n✅ 检测到登录成功！usage API -> {r.status}")
                    break
            except Exception:
                pass
            if i % 30 == 0:
                print(f"  …等待中 ({i*2}s) 当前: {page.url[:70]}")
    else:
        print("✅ 看起来已经在控制台里了！验证中…")
        logged_in = True

    # 保存 cookies（取当前会话的 cookie）
    cookies = ctx.cookies()
    with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"✅ 会话已保存 ({len(cookies)} cookie) -> {COOKIE_FILE}")

    # 测试用量 API
    print("\n--- 测试用量 API ---")
    for path in ['/console/api/v1/usage/export', '/console/api/usage', '/console/api/billing']:
        try:
            r = page.request.get('https://opencode.ai' + path)
            print(f"GET {path} -> {r.status}: {r.text()[:300]}")
        except Exception as e:
            print(f"GET {path} -> ERR {e}")

    page.screenshot(path=os.path.join(BASE, 'console_logged_in.png'))
    ctx.close()
    print("\n完成！接下来配置自动抓取。")