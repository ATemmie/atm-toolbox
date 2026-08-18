# -*- coding: utf-8 -*-
"""CDP 连现有 Edge(9223)，新 tab 搜京东卡包"""
from playwright.sync_api import sync_playwright
import json, os

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()

    results = {}
    keywords = ['卡包 多卡位 防消磁 大学生', '卡包 男士 多卡位']
    for kw in keywords:
        try:
            page.goto(f'https://search.jd.com/Search?keyword={kw}', wait_until='domcontentloaded', timeout=45000)
            page.wait_for_timeout(6000)
            items = page.eval_on_selector_all('.gl-item',
                "els => els.slice(0,10).map(e => { const t = e.querySelector('.p-name em, .p-name a'); const p = e.querySelector('.p-price i, .p-price'); const shop = e.querySelector('.p-shop a, .p-shopnum'); return { title: t ? t.innerText.trim().replace(/\\s+/g,' ') : '', price: p ? p.innerText.trim() : '', shop: shop ? shop.innerText.trim() : '' }; })")
            good = [it for it in items if it['title']]
            print(f"\n=== [{kw}] {len(good)} 条 ===")
            for it in good[:10]:
                print(f"  ¥{it['price']} | {it['title'][:60]} | {it['shop'][:18]}")
            results[kw] = good
        except Exception as e:
            print(f"[{kw}] 失败: {str(e)[:120]}")

    with open(os.path.join(BASE, 'data', 'card_holder_search.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n✅ 已存 data/card_holder_search.json")
    page.close()