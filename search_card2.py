# -*- coding: utf-8 -*-
"""解析京东卡包搜索页 + 搜电信澳门微信入口"""
import urllib.request, urllib.error, re, json

PROXY = 'http://127.0.0.1:7890'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': PROXY, 'https': PROXY}))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def get(url, timeout=20):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', UA)
    try:
        r = op.open(req, timeout=timeout)
        return r.status, r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'ignore')
    except Exception as e:
        return -1, str(e)

# 京东卡包搜索结果解析（页面里可能含商品信息）
st, body = get('https://search.jd.com/Search?keyword=%E5%A4%9A%E5%8D%A1%E4%BD%8D%E5%8D%A1%E5%8C%85%20%E9%98%B2%E5%88%B7%E9%98%B2%E6%91%A9%E6%93%A6%20%E5%AD%A6%E7%94%9F')
print(f"[京东] {st} len={len(body)}")

# 尝试提取商品名称和价格 (jd 的 script 里有 sku 数据)
# 找 "wids"/"prices" 或 p-global 数据
goods = re.findall(r'"name":"([^"]{5,60})"', body)
prices = re.findall(r'"p":"(\d+)"', body)
imgs = re.findall(r'"id":"(\d+)"', body)
print(f"提取到名称 {len(goods)} 个, 价格 {len(prices)} 个")
for i, g in enumerate(goods[:10]):
    print(f"  {i+1}. {g}")

# 微信入口搜索 - 用 bing 简化版
st2, body2 = get('https://cn.bing.com/search?q=%E9%9B%BB%E4%BF%A1%E6%BE%B3%E9%96%80+%E5%85%A7%E5%9C%B0%E5%AD%B8%E7%94%9F+%E4%B8%80%E5%8D%A1%E9%9B%99%E8%99%9F+%E5%BE%AE%E4%BF%A1')
print(f"\n[Bing港版] {st2} len={len(body2)}")
# 提取标题和摘要
items = re.findall(r'<li class="b_algo".*?<h2><a[^>]*>(.*?)</a></h2>.*?(?:<p[^>]*>(.*?)</p>)?', body2, re.S)
if not items:
    items = re.findall(r'<h2>(.*?)</h2>', body2, re.S)
for t, s in items[:6]:
    clean_t = re.sub('<[^>]+>', '', t).strip()
    clean_s = re.sub('<[^>]+>', '', s or '').strip()
    if clean_t:
        print(f"  - {clean_t[:80]}")
        if clean_s:
            print(f"    {clean_s[:150]}")