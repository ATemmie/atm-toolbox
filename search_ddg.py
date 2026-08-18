# -*- coding: utf-8 -*-
"""DuckDuckGo 搜卡包推荐"""
import urllib.request, urllib.error, re, html as htmllib

PROXY = 'http://127.0.0.1:7890'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': PROXY, 'https': PROXY}))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def get(url, timeout=20):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', UA)
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.9')
    try:
        r = op.open(req, timeout=timeout)
        return r.status, r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'ignore')
    except Exception as e:
        return -1, str(e)

# DuckDuckGo html 版
st, body = get('https://html.duckduckgo.com/html/?q=%E5%A4%9A%E5%8D%A1%E4%BD%8D%E5%8D%A1%E5%8C%85+%E9%98%B2%E6%B6%88%E7%A3%81+%E6%8E%A8%E8%8D%90')
print(f"[DDG卡包] {st} len={len(body)}")
if st == 200:
    results = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S)
    snips = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', body, re.S)
    for i, (href, t) in enumerate(results[:8]):
        clean_t = htmllib.unescape(re.sub('<[^>]+>', '', t).strip())
        snip = htmllib.unescape(re.sub('<[^>]+>', '', snips[i]).strip()) if i < len(snips) else ''
        print(f"  {i+1}. {clean_t[:70]}")
        if snip:
            print(f"     {snip[:100]}")
        print(f"     {href[:70]}")
    if not results:
        print("  (无结果)")
        print(body[:300])

# 电信澳门一卡双号
st, body = get('https://html.duckduckgo.com/html/?q=%E7%94%B5%E4%BF%A1%E6%BE%B3%E9%97%A8+%E4%B8%80%E5%8D%A1%E5%8F%8C%E5%8F%B7+%E5%86%85%E5%9C%B0%E7%94%9F+%E5%8A%9E%E7%90%86')
print(f"\n[DDG电信澳门] {st} len={len(body)}")
if st == 200:
    results = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S)
    snips = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', body, re.S)
    for i, (href, t) in enumerate(results[:8]):
        clean_t = htmllib.unescape(re.sub('<[^>]+>', '', t).strip())
        snip = htmllib.unescape(re.sub('<[^>]+>', '', snips[i]).strip()) if i < len(snips) else ''
        print(f"  {i+1}. {clean_t[:70]}")
        if snip:
            print(f"     {snip[:100]}")
        print(f"     {href[:70]}")
    if not results:
        print("  (无结果)")