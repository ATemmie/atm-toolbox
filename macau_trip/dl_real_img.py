"""用Unsplash搜索澳门景点图片"""
import urllib.request, urllib.parse, ssl, re, os, json, subprocess, time

ssl._create_default_https_context = ssl._create_unverified_context
PROXY = "http://127.0.0.1:7890"
proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(proxy_handler)
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

SEARCHES = {
    "a_ma_temple": "A-Ma Temple Macau",
    "macau_tower": "Macau Tower",
    "senado_square": "Senado Square Macau",
    "st_pauls": "Ruins of St. Paul's Macau",
    "st_dominic": "St Dominic Church Macau",
    "monte_fort": "Monte Fort Macau",
    "nam_van_lake": "Nam Van Lake Macau",
    "rua_cunha": "Rua do Cunha Macau",
    "carmel_church": "Our Lady of Carmel Macau",
    "taipa_houses": "Taipa Houses Macau",
    "wynn_palace": "Wynn Palace Macau",
    "parisian": "Parisian Macao Cotai",
    "londoner": "Londoner Macao Cotai",
    "galaxy": "Galaxy Macau Cotai",
    "venetian": "Venetian Macao Cotai",
}

def search_unsplash(query):
    """从Unsplash搜索页提取图片URL"""
    encoded = urllib.parse.quote(query)
    url = f"https://unsplash.com/s/photos/{encoded}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        resp = opener.open(req, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        # Unsplash图片URL模式: images.unsplash.com/photo-xxx
        urls = re.findall(r'https://images\.unsplash\.com/photo-[a-zA-Z0-9_-]+\?[^"\'\\s]+', html)
        if urls:
            # 取第一个，加上w=800参数
            base = urls[0].split("?")[0]
            return f"{base}?w=800&q=80&fit=crop"
    except Exception as e:
        print(f"    Unsplash搜索失败: {e}")
    return None

def search_pixabay(query):
    """从Pixabay搜索页提取图片URL（备选）"""
    encoded = urllib.parse.quote(query)
    url = f"https://pixabay.com/images/search/{encoded}/"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    })
    try:
        resp = opener.open(req, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        urls = re.findall(r'https://cdn\.pixabay\.com/photo/\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/[^"\'\\s]+', html)
        if urls:
            return urls[0]
    except Exception as e:
        print(f"    Pixabay搜索失败: {e}")
    return None

def download(url, fp):
    cmd = ["curl", "-sL", "-o", fp, "-H",
           "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
           "--proxy", PROXY, "--connect-timeout", "10", "--max-time", "20", url]
    subprocess.run(cmd, capture_output=True, timeout=30)
    if os.path.exists(fp) and os.path.getsize(fp) > 5000:
        import imghdr
        if imghdr.what(fp) in ("jpeg", "png", "webp", None):
            return True
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
        url = search_unsplash(query)
        if not url:
            print(f"    Unsplash无结果，试Pixabay...")
            url = search_pixabay(query)
        if not url:
            print(f"  [miss] {key}")
            time.sleep(1)
            continue
        
        print(f"  下载 {url[:70]}...")
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
