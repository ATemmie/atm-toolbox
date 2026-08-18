# -*- coding: utf-8 -*-
"""抓 jiejingku.net/10860.html 看结构（捷径库页面怎么部署快捷指令）"""
import urllib.request, urllib.error, re, html as H

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

st, body = get('https://jiejingku.net/10860.html')
print(f"[jiejingku] {st} len={len(body)}")
if st == 200:
    # 标题
    m = re.search(r'<title>(.*?)</title>', body, re.S)
    print("标题:", H.unescape(m.group(1)).strip() if m else '?')
    # 找所有链接
    links = re.findall(r'href=["\']([^"\']+)["\']', body)
    print(f"\n链接数: {len(links)}")
    seen = set()
    for l in links:
        if any(k in l.lower() for k in ['shortcut', 'icloud', 'shortcuts', 'download', '.plist', 'https://www.icloud']) or 'shortcuts' in l.lower():
            if l not in seen and l.startswith('http'):
                seen.add(l)
                print("  ", l[:120])
    # 可能的关键词
    text = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.S)
    text = H.unescape(re.sub(r'<[^>]+>', ' ', text))
    text = re.sub(r'\s+', ' ', text)
    for kw in ['快捷指令', '添加', '安装', 'iCloud', '一键']:
        for mm in re.finditer(kw, text):
            s = max(0, mm.start() - 40)
            print(f"\n[{kw}]: ...{text[s:mm.start()+80]}...")
            break
    idx = text.find('快捷指令')
    print("\n页面开头:", text[:600])