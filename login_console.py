# -*- coding: utf-8 -*-
"""
OpenCode Console 登录助手（headed 模式）
- 打开可见浏览器 → 用户登录控制台（GitHub/Google/email）
- 登录成功后自动：保存 cookie 到本地 → 测试 /console/api/v1/usage/export → 输出用量
用法: python login_console.py
"""
import json, os, time, sys
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = os.path.join(BASE, 'data', 'console_cookies.json')
os.makedirs(os.path.join(BASE, 'data'), exist_ok=True)

print("=" * 50)
print("🧰 ATM 工具箱 - OpenCode 控制台登录助手")
print("=" * 50)
print("即将打开浏览器窗口，请在窗口中完成登录：")
print("  1. 浏览器会打开 opencode.ai/console")
print("  2. 点击 Continue with GitHub / Google / email 登录")
print("  3. 登录成功后回到这里等几秒，我会自动保存会话")
print("  （不需要点其他任何东西）")
print()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel='msedge', args=['--no-sandbox', '--start-maximized'])
    ctx = browser.new_context(
        viewport={'width': 1280, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
    )
    page = ctx.new_page()

    # 监听 usage API 响应（登录后会触发）
    usage_hits = []
    page.on('response', lambda resp: usage_hits.append({
        'url': resp.url, 'status': resp.status,
    }) if 'usage' in resp.url or 'billing' in resp.url or 'balance' in resp.url else None)

    page.goto('https://opencode.ai/console', wait_until='networkidle', timeout=60000)

    print("浏览器已打开，请登录…")
    print("（点 Continue with GitHub/Google → 完成授权 → 自动跳回控制台）")
    print("（我会一直等到你真正登录成功，放心操作）")

    # 等待登录成功：轮询检测（最多 10 分钟）
    # 判定标准：usage API 从 401 变成其他状态 = 真正登录成功！
    logged_in = False
    for i in range(300):  # 最多等 10 分钟
        time.sleep(2)
        # 实时刺探 usage API，看认证是否生效
        try:
            r = page.request.get('https://opencode.ai/console/api/v1/usage/export')
            if r.status not in (401, 404):
                logged_in = True
                print(f"\n✅ 检测到登录成功！usage API 返回 {r.status}")
                usage_hits.append({'url': '/console/api/v1/usage/export', 'status': r.status})
                break
        except Exception:
            pass
        # URL 变成 org 工作台 = 登录成功（usage API 判定不准时的兜底）
        if 'console/org_' in page.url:
            logged_in = True
            print(f"\n✅ 检测到登录成功！已进入组织工作台: {page.url[:60]}")
            break
        # 如果当前 URL 不是 opencode.ai 域（可能卡在 GitHub 授权页），提示但继续等
        if i % 30 == 0:
            cur = page.url
            print(f"  …等待中 ({i*2}s) 当前页面: {cur[:80]}")
            # 若跳回 console 域且无登录按钮，也视为可能成功（再用 API 验证）
            if 'opencode.ai' in cur and 'console' in cur:
                try:
                    has_login = page.is_visible("text=Continue with GitHub", timeout=1500) or page.is_visible("text=Log in to OpenCode Console", timeout=1500)
                except Exception:
                    has_login = False
                if not has_login:
                    # 再刺探一次 API
                    try:
                        r = page.request.get('https://opencode.ai/console/api/v1/usage/export')
                        if r.status not in (401, 404):
                            logged_in = True
                            print(f"\n✅ 检测到登录成功！usage API 返回 {r.status}")
                            usage_hits.append({'url': '/console/api/v1/usage/export', 'status': r.status})
                            break
                    except Exception:
                        pass

    if not logged_in:
        print("\n⚠️ 10 分钟超时。你完成登录了吗？")
        print("如果已经登录成功，直接按 Enter 继续保存会话…")
        input()

    if not logged_in:
        print("\n⚠️ 超时未检测到登录。你登录了吗？可以重试，或者手动确认页面已登录后按 Enter")
        input("按 Enter 继续保存会话…")

    # 保存 cookies
    cookies = ctx.cookies()
    with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 会话已保存 ({len(cookies)} 个 cookie) -> {COOKIE_FILE}")

    # 测试 usage API
    print("\n--- 测试用量 API ---")
    for path in ['/console/api/v1/usage/export', '/console/api/usage', '/console/api/billing']:
        try:
            r = page.request.get('https://opencode.ai' + path)
            body = r.text()[:500]
            print(f"GET {path} -> {r.status}: {body}")
        except Exception as e:
            print(f"GET {path} -> ERR {e}")

    # 截屏留档
    page.screenshot(path=os.path.join(BASE, 'console_logged_in.png'))
    browser.close()
    print("\n完成！会话已保存。接下来我可以配置自动抓取了。")