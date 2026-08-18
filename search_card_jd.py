# -*- coding: utf-8 -*-
"""京东搜卡包（stealth + 真实 Edge，用已有京东登录态）"""
from playwright.sync_api import sync_playwright
import json, os, time, re

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
EDGE_USER = r'C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data Copy'
edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if not os.path.exists(edge_path):
    edge_path = r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'

keywords = ['卡包 多卡位 大学生', '卡包 防消磁 学生', '银行卡卡包 男士']

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        EDGE_USER, executable_path=edge_path, headless=False,
        args=['--no-sandbox', '--start-maximized'],
        viewport={'width': 1400, 'height': 900})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    results = {}
    for kw in keywords:
        try:
            page.goto(f'https://search.jd.com/Search?keyword={kw}', wait_until='domcontentloaded', timeout=45000)
            page.wait_for_timeout(5000)
            # 提取商品标题和价格
            items = page.eval_on_selector_all('.gl-item',
                "els => els.slice(0,8).map(e => { const t = e.querySelector('.p-name em, .p-name a'); const p = e.querySelector('.p-price i, .p-price'); const shop = e.querySelector('.p-shop a, .p-shopnum'); return { title: t ? t.innerText.trim().replace(/\\s+/g,' ') : '', price: p ? p.innerText.trim() : '', shop: shop ? shop.innerText.trim() : '' }; })")
            print(f"\n=== [{kw}] {len(items)} 条 ===")
            for it in items:
                if it['title']:
                    print(f"  ¥{it['price']} | {it['title'][:55]} | {it['shop'][:20]}")
                    results.setdefault(kw, []).append(it)
        except Exception as e:
            print(f"[{kw}] 失败: {str(e)[:100]}")

    with open(os.path.join(BASE, 'data', 'card_holder_search.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n✅ 结果已存 data/card_holder_search.json")
    ctx.close()