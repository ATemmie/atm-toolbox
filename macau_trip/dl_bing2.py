"""Bing图片搜索 - 用多种regex模式提取图片URL"""
import urllib.request, urllib.parse, ssl, re, os, json, subprocess, time

ssl._create_default_https_context = ssl._create_unverified_context
PROXY = "http://127.0.0.1:7890"
proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(proxy_handler)
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

SEARCHES = {
    "a_ma_temple": "妈阁庙 澳门",
    "macau_tower": "澳门旅游塔",
    "senado_square": "议事亭前地 澳门",
    "st_pauls": "大三巴牌坊",
    "st_dominic": "玫瑰圣母堂 澳门",
    "monte_fort": "大炮台 澳门",
    "nam_van_lake": "南湾湖 澳门",
    "rua_cunha": "官也街 澳门",
    "carmel_church": "嘉模圣母堂 澳门",
    "taipa_houses": "龙环葡韵 澳门",
    "wynn_palace": "永利皇宫 澳门",
    "parisian": "巴黎人 澳门",
    "londoner": "伦敦人 澳门",
    "galaxy": "银河 澳门",
    "venetian": "威尼斯人 澳门",
}

def bing_search_debug(query):
    """搜索并调试输出HTML结构"""
    encoded = urllib.parse.quote(query)
    url = f"https://cn.bing.com/images/search?q={encoded}&first=1&count=5"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.9",
    })
    resp = opener.open(req, timeout=15)
    html = resp.read().decode("utf-8", errors="ignore")
    
    # 多种模式尝试提取
    patterns = [
        r'"murl":"(https?://[^"]+)"',
        r'"purl":"(https?://[^"]+)"',
        r'src2="(https?://[^"]+\.(jpg|jpeg|png))"',
        r'data-src="(https?://[^"]+\.(jpg|jpeg|png))"',
        r'"imgurl":"(https?://[^"]+)"',
        r'href="(https?://[^"]+\.(jpg|jpeg|png)[^"]*)"',
    ]
    
    for pat in patterns:
        matches = re.findall(pat, html, re.I)
        good = []
        for m in matches:
            u = m[0] if isinstance(m, tuple) else m
            if not isinstance(u, str) or len(u) < 20 or "bing.com" in u:
                continue
            # 清理URL尾巴的JSON残留
            u = re.sub(r'[&].*$', '', u)
            u = re.sub(r'\\u00.*$', '', u)
            if u.startswith("http"):
                good.append(u)
        if good:
            return good[0]
    
    # 最后手段：找所有http链接
    all_urls = re.findall(r'https?://[^"\'\\s<>]+', html)
    img_urls = [u for u in all_urls if any(ext in u.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) 
                and 'bing.com' not in u and 'microsoft' not in u and len(u) > 30]
    img_urls = [re.sub(r'[&].*$', '', u) for u in img_urls]
    if img_urls:
        return img_urls[0]
    
    # 保存HTML供调试
    debug_path = os.path.join(IMG_DIR, f"_debug_{query[:10]}.html")
    with open(debug_path, "w", encoding="utf-8") as f:
        f.write(html[:50000])
    return None

def download(url, fp):
    cmd = ["curl", "-sL", "-o", fp, "-H",
           "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
           "-H", "Referer: https://www.bing.com/",
           "--proxy", PROXY, "--connect-timeout", "10", "--max-time", "20", url]
    subprocess.run(cmd, capture_output=True, timeout=30)
    if os.path.exists(fp) and os.path.getsize(fp) > 5000:
        # 验证是否为真实图片
        try:
            from PIL import Image as PILImage
            img = PILImage.open(fp)
            img.verify()
            return True
        except Exception:
            pass
    if os.path.exists(fp):
        os.remove(fp)
    return False

def main():
    results = {}
    for key, query in SEARCHES.items():
        fp = os.path.join(IMG_DIR, f"{key}.jpg")
        if os.path.exists(fp) and os.path.getsize(fp) > 5000:
            results[key] = fp
            print(f"  [skip] {key}")
            continue
        
        print(f"  搜索 {query}...")
        url = bing_search_debug(query)
        if not url:
            print(f"  [miss] {key}")
            time.sleep(1)
            continue
        
        print(f"  下载 {url[:80]}...")
        if download(url, fp):
            size = os.path.getsize(fp) // 1024
            results[key] = fp
            print(f"  [ok] {key} ({size}KB)")
        else:
            print(f"  [fail] {key}")
        time.sleep(1.5)
    
    idx = os.path.join(IMG_DIR, "_index.json")
    with open(idx, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {len(results)}/{len(SEARCHES)} 张真实图片")
    return results

if __name__ == "__main__":
    main()
