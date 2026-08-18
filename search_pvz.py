# -*- coding: utf-8 -*-
"""DDG 搜: 植物大战僵尸原版 下载渠道 (2026)"""
import urllib.request, urllib.error, re, html as H, urllib.parse, time

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

queries = [
    '植物大战僵尸原版 下载 2026',
    '植物大战僵尸 官方下载 原版 免费',
    '植物大战僵尸 steam 国区 下架 怎么办',
]
for q in queries:
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    st, body = get(url)
    print(f"\n===== [{q}] {st} =====")
    if st == 200:
        res2 = re.findall(r'class="result__a"[^>]*>(.*?)</a>', body, re.S)
        snips = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', body, re.S)
        hrefs = re.findall(r'class="result__a"[^>]*href="([^"]+)"', body)
        for i, t in enumerate(res2[:7]):
            clean = H.unescape(re.sub(r'<[^>]+>', '', t)).strip()
            sn = H.unescape(re.sub(r'<[^>]+>', '', snips[i])).strip() if i < len(snips) else ''
            hh = hrefs[i][:100] if i < len(hrefs) else ''
            print(f"  {i+1}. {clean}")
            print(f"     {sn[:130]}")
            print(f"     {hh}")
    time.sleep(2)