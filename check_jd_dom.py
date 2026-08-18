# -*- coding: utf-8 -*-
"""CDP 检查京东搜索页实际 DOM"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()
    page.goto('https://search.jd.com/Search?keyword=%E5%8D%A1%E5%8C%85%20%E5%A4%9A%E5%8D%A1%E4%BD%8D', wait_until='domcontentloaded', timeout=45000)
    page.wait_for_timeout(8000)
    print("URL:", page.url[:80])
    text = page.inner_text('body')
    print("页面文本前 1200 字:")
    print(text[:1200])
    page.close()