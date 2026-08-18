# -*- coding: utf-8 -*-
"""CDP 完整抓取 workspace 用量页：全页面文本 + 保存结构化数据"""
import json, time, re, os
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

    # 点使用量 tab
    try:
        el = page.locator('text=使用量').first
        if el.is_visible(timeout=2000):
            el.click(timeout=5000)
    except Exception:
        pass
    page.wait_for_timeout(3000)

    text = page.inner_text('body')
    print("=== 全页面文本 ===")
    print(text[:6000])

    # 结构化解析
    data = {
        'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'url': page.url,
        'text': text[:15000],
    }

    # 提取用量占比（滚动/每周/每月）
    for pat, key in [
        (r'滚动用量\s*([\d.]+)%', 'rolling_pct'),
        (r'每周用量\s*([\d.]+)%', 'weekly_pct'),
        (r'每月用量\s*([\d.]+)%', 'monthly_pct'),
        (r'重置于\s*([\d\s\w小时分钟天]+)', 'reset_text'),
        (r'当前余额\s*\$?([\d.]+)', 'balance'),
    ]:
        m = re.search(pat, text)
        if m:
            data[key] = m.group(1).strip()
            print(f"  {key} = {data[key]}")

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 已保存 -> {OUT}")

    # 截图
    page.screenshot(path=os.path.join(BASE, 'ws_full.png'), full_page=True)
    print("📸 ws_full.png")
    print("完成")