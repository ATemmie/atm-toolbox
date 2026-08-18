# -*- coding: utf-8 -*-
"""
用用户 Edge (Default profile) 的登录态抓 workspace Go 页面
前提：Edge 已被关闭（避免 user-data-dir 锁冲突）
用法: python fetch_with_edge_profile.py
"""
import json, os, time
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
EDGE_USER = r'C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data'
WS_URL = 'https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go'
OUT = os.path.join(BASE, 'data', 'go_usage.json')

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if not os.path.exists(edge_path):
    edge_path = r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'

print(f"使用 Edge: {edge_path}")
print(f"Profile: {EDGE_USER}")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        EDGE_USER,
        executable_path=edge_path,
        headless=False,
        args=['--no-sandbox', '--disable-features=msEdgeSidebarV2', '--start-maximized'],
        viewport={'width': 1400, 'height': 2000},
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    api_hits = []
    def on_resp(resp):
        u = resp.url
        if any(k in u for k in ['usage', 'billing', 'budget', 'balance', 'credit', 'limit', 'quota', 'cost', 'spend', '/go', 'usage/export']):
            try:
                body = resp.text()[:800]
            except Exception:
                body = ''
            api_hits.append({'status': resp.status, 'url': u, 'body': body})
    page.on('response', on_resp)

    # 直接导航到用户给的 workspace go 页面
    try:
        page.goto(WS_URL, wait_until='networkidle', timeout=60000)
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f"导航异常: {e}")

    text = page.inner_text('body')
    print("=== 页面 URL ===")
    print(page.url)
    print("\n=== 页面文本 ===")
    print(text[:3000])

    # cookie 备份
    cookies = ctx.cookies()
    with open(os.path.join(BASE, 'data', 'console_cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"\n📎 会话 cookie 已备份 ({len(cookies)} 个)")

    print("\n=== API 调用 ===")
    seen = set()
    for h in api_hits:
        key = f"{h['status']} {h['url'][:120]}"
        if key not in seen:
            seen.add(key)
            print(f"\n[{h['status']}] {h['url']}")
            if h['status'] == 200 and h['body']:
                print(f"    {h['body'][:400]}")

    data = {
        'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'url': page.url,
        'page_text': text[:8000],
        'api': api_hits,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 已保存 -> {OUT}")

    try:
        page.screenshot(path=os.path.join(BASE, 'go_page_profile.png'), full_page=True)
        print("📸 截图 go_page_profile.png")
    except Exception as e:
        print(f"截图失败: {e}")

    ctx.close()
    print("\n完成！")