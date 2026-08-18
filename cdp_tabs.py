# -*- coding: utf-8 -*-
"""CDP: 依次点完所有 tab（使用量/计费/设置），抓全页面 + 找百分比"""
import json, time, os
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
OUT = os.path.join(BASE, 'data', 'ws_usage.json')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    if 'workspace' not in page.url:
        page.goto('https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go', wait_until='networkidle', timeout=60000)
        page.wait_for_timeout(4000)

    all_texts = {}
    for tab in ['使用量', '计费', '设置', 'API 密钥']:
        try:
            el = page.locator(f'text={tab}').first
            if el.is_visible(timeout=1500):
                el.click(timeout=4000)
                page.wait_for_timeout(3000)
                t = page.inner_text('body')
                all_texts[tab] = t
                print(f"=== [{tab}] 页面 ===")
                print(t[:1200])
                print()
        except Exception as e:
            print(f"tab {tab} 失败: {e}")

    page.screenshot(path=os.path.join(BASE, 'ws_billing.png'), full_page=True)
    print("📸 ws_billing.png（计费页全图）")

    # 合并保存
    merged = {
        'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'tabs': all_texts,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"💾 保存 -> {OUT}")