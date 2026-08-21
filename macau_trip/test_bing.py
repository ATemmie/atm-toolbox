import re, urllib.request, urllib.parse, ssl
ssl._create_default_https_context = ssl._create_unverified_context
proxy_handler = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
opener = urllib.request.build_opener(proxy_handler)
url = "https://cn.bing.com/images/search?q=" + urllib.parse.quote("大三巴牌坊") + "&first=1&count=5"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
})
html = opener.open(req, timeout=15).read().decode("utf-8", errors="ignore")
# 找murl字段
murls = re.findall(r'"murl":"(https?://[^"]+)"', html)
print(f"Found {len(murls)} murl matches")
for u in murls[:5]:
    print(f"  {u}")
# 也找所有图片URL
all_urls = re.findall(r'https?://[^"\'\\s<>]+', html)
img_urls = [u for u in all_urls if any(ext in u.lower() for ext in [".jpg", ".jpeg", ".png"]) and "bing.com" not in u]
print(f"\nAll image URLs: {len(img_urls)}")
for u in img_urls[:10]:
    print(f"  {u[:120]}")
