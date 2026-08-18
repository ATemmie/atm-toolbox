# -*- coding: utf-8 -*-
"""查电信澳门一卡双号最新信息 + 京东卡包推荐"""
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

# 1. 中国电信澳门官网
st, body = get('https://www.189.cn/mo/')
print(f"[澳门电信官网] {st} len={len(body)}")
if st == 200:
    # 找一卡双号相关内容
    for kw in ['一卡双号', '澳门', '学生']:
        idx = body.find(kw)
        if idx >= 0:
            print(f"  找到[{kw}]: {re.sub('<[^>]+>', '', body[max(0,idx-50):idx+200])[:220]}")

# 2. 尝试微信预定页/搜索
st, body = get('https://www.189.cn/mo/care/zh_cn/number_card.html')
print(f"\n[澳门电信卡页面] {st}")

# 3. 京东搜卡包（用 mobile.search 接口）
st, body = get('https://search.jd.com/Search?keyword=%E5%8D%A1%E5%8C%85%E5%A4%9A%E5%8D%A1%E4%BD%8D%20%E5%AD%A6%E7%94%9F')
print(f"\n[京东卡包搜索] {st} len={len(body)}")

# 4. 通用搜索（bing）
try:
    st, body = get('https://www.bing.com/search?q=%E7%94%B5%E4%BF%A1%E6%BE%B3%E9%97%A8+%E4%B8%80%E5%8D%A1%E5%8F%8C%E5%8F%B7+%E5%86%85%E5%9C%B0%E5%AD%A6%E7%94%9F')
    print(f"\n[Bing搜索] {st} len={len(body)}")
    title_re = re.findall(r'<h2>(.*?)</h2>', body)
    if title_re:
        for t in title_re[:8]:
            clean = re.sub('<[^>]+>', '', t)
            if clean.strip():
                print(f"  - {clean[:100]}")
    if not title_re:
        print("  (无搜索结果标题)")
except Exception as e:
    print(f"\n[Bing失败] {e}")