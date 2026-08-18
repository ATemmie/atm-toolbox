# -*- coding: utf-8 -*-
"""抓 1888.com.mo 电信澳门官网 + 知乎使用感受"""
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

# 电信澳门官网
st, body = get('https://www.1888.com.mo/home/index')
print(f"[电信澳门官网] {st} len={len(body)}")
if st == 200:
    text = re.sub('<[^>]+>', ' ', body)
    text = htmllib.unescape(re.sub(r'\s+', ' ', text))
    for kw in ['一卡', '雙號', '双号', '學生', '学生']:
        idx = text.find(kw)
        if idx >= 0:
            print(f"  找到[{kw}]: ...{text[max(0,idx-80):idx+200]}...")
    # 找链接
    links = re.findall(r'href="(/[^"]+)"', body)
    print(f"  内链 {len(links)} 个，示例:", links[:10])
    # 找导航里的产品名
    print("  页面文字片段:", text[:500])