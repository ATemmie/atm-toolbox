# -*- coding: utf-8 -*-
"""DDG 搜: 完美对战平台 玩家数据 个人主页 查询"""
import urllib.request, urllib.error, re, html as H, urllib.parse, json

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
    '完美对战平台 玩家数据 个人主页 查询',
    '完美电竞 平台 玩家 战绩 查询 网页',
    '完美世界电竞 PW 玩家数据 pvp',
]
for q in queries:
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    st, body = get(url)
    print(f"\n===== [{q}] {st} len={len(body)} =====")
    if st == 200:
        # 解析结果块
        results = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>', body, re.S)
        if not results:
            # 简化版解析
            res2 = re.findall(r'class="result__a"[^>]*>(.*?)</a>', body, re.S)
            snips = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', body, re.S)
            for i, t in enumerate(res2[:8]):
                clean = H.unescape(re.sub(r'<[^>]+>', '', t)).strip()
                sn = H.unescape(re.sub(r'<[^>]+>', '', snips[i])).strip() if i < len(snips) else ''
                print(f"  {i+1}. {clean}")
                print(f"      {sn[:120]}")
        else:
            for i, (href, t, sn) in enumerate(results[:8]):
                clean_t = H.unescape(re.sub(r'<[^>]+>', '', t)).strip()
                clean_s = H.unescape(re.sub(r'<[^>]+>', '', sn)).strip()
                print(f"  {i+1}. {clean_t}")
                print(f"      {clean_s[:120]}")
                print(f"      {href[:110]}")
    import time; time.sleep(2)