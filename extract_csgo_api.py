# -*- coding: utf-8 -*-
"""提取 csgo.com.cn 查询页的接口和参数结构"""
import urllib.request, re

PROXY = 'http://127.0.0.1:7890'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': PROXY, 'https': PROXY}))
req = urllib.request.Request('https://www.csgo.com.cn/hd/1705/query/')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0')
body = op.open(req, timeout=20).read().decode('utf-8', 'ignore')

print("=== 所有 ajax url ===")
for m in re.finditer(r"url\s*:\s*['\"]([^'\"]+)['\"]", body):
    print(" ", m.group(1))

print("\n=== 接口名/路径 ===")
for m in re.finditer(r"['\"](/?datacsgo/[^'\"]+)['\"]", body):
    print(" ", m.group(1))

print("\n=== search 相关 JS 片段 ===")
idx = body.find('startSearch')
if idx > 0:
    print(body[max(0, idx-300):idx+400].replace('\n', ' ')[:700])