# -*- coding: utf-8 -*-
"""Bing 搜卡包推荐 + 电信号码办理细节"""
import urllib.request, urllib.error, re

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

queries = [
    ('卡包', 'https://www.bing.com/search?q=%E5%A4%A7%E5%AD%A6%E7%94%9F%E5%8D%A1%E5%8C%85%E6%8E%A8%E8%8D%90+%E5%A4%9A%E5%8D%A1%E4%BD%8D+%E9%98%B2%E6%B6%88%E7%A3%81'),
    ('电信澳门', 'https://www.bing.com/search?q=%E7%94%B5%E4%BF%A1%E6%BE%B3%E9%97%A8+%E4%B8%80%E5%8D%A1%E5%8F%8C%E5%8F%B7+%E5%86%85%E5%9C%B0%E5%AD%A6%E7%94%9F+%E5%8A%9E%E7%90%86'),
]

for name, url in queries:
    st, body = get(url)
    print(f"\n===== [{name}] {st} =====")
    if st == 200:
        # 提取搜索结果
        items = re.findall(r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></h2>', body, re.S)
        if not items:
            items = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)
            items = [(x, '') for x in items]
        for href, t in items[:8]:
            clean_t = re.sub('<[^>]+>', '', t).strip()
            if clean_t:
                print(f"  - {clean_t[:90]}")
                if href:
                    print(f"    {href[:80]}")
        if not items:
            # 尝试其他模式
            links = re.findall(r'<a[^>]*href="(http[^"]+)"[^>]*>(.{5,60})</a>', body)
            for href, t in links[:10]:
                clean_t = re.sub('<[^>]+>', '', t).strip()
                if clean_t and 'microsoft' not in href and 'bing' not in href and 'go.micro' not in href:
                    print(f"  - {clean_t[:80]}")