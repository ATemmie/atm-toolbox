# -*- coding: utf-8 -*-
"""Playwright 截图本地页面验证效果"""
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8123/index.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    # 手机视口效果
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    page = ctx.new_page()
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.goto(URL, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(1500)
    page.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\preview_mobile.png', full_page=True)
    # 桌面视口
    ctx2 = browser.new_context(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
    page2 = ctx2.new_page()
    page2.goto(URL, wait_until='networkidle', timeout=30000)
    page2.wait_for_timeout(1500)
    page2.screenshot(path=r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\preview_desktop.png', full_page=True)
    print("截图完成")
    print("JS 错误:", errors if errors else "无")
    # 简单检查表格渲染
    rows = page.eval_on_selector_all('#tbody tr', 'els => els.length')
    first_cell = page.eval_on_selector('#tbody tr .mname', 'e => e ? e.innerText : "无"')
    print(f"表格行数: {rows}, 第一行: {first_cell}")
    print("更新时间:", page.inner_text('#update-time'))
    browser.close()