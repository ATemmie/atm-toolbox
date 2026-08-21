"""步骤1：用Bing搜索真实景点图片URL，然后用curl下载"""
import urllib.request, urllib.parse, ssl, re, os, json, subprocess, time

ssl._create_default_https_context = ssl._create_unverified_context
PROXY = "http://127.0.0.1:7890"
proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(proxy_handler)
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 搜索关键词 → 文件名
SEARCHES = {
    "a_ma_temple": "澳门妈阁庙 A-Ma Temple",
    "macau_tower": "澳门旅游塔 Macau Tower",
    "senado_square": "议事亭前地 Senado Square Macau",
    "st_pauls": "大三巴牌坊 Ruins St Paul Macau",
    "st_dominic": "玫瑰圣母堂 Macau church",
    "monte_fort": "大炮台 Monte Fort Macau",
    "nam_van_lake": "南湾湖 Nam Van Lake Macau",
    "rua_cunha": "官也街 Rua do Cunha",
    "carmel_church": "嘉模圣母堂 Carmel Church Taipa",
    "taipa_houses": "龙环葡韵 Taipa Houses Macau",
    "wynn_palace": "永利皇宫 Wynn Palace Macau",
    "parisian": "巴黎人 Parisian Macao",
    "londoner": "伦敦人 Londoner Macao",
    "galaxy": "银河 Galaxy Macau",
    "venetian": "威尼斯人 Venetian Macao",
}

def bing_image_search(query):
    """用Bing搜索图片，返回第一个图片URL"""
    encoded = urllib.parse.quote(query + " photo")
    url = f"https://cn.bing.com/images/search?q={encoded}&first=1&count=3&FORM=QBLH"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    })
    try:
        resp = opener.open(req, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        # 从Bing图片结果中提取murl（媒体URL）
        murls = re.findall(r'"murl":"(https?://[^"]+\.(jpg|jpeg|png|webp))"', html, re.I)
        if murls:
            return murls[0][0]
        # 备选：提取src
        srcs = re.findall(r'src="(https?://[^"]+\.(jpg|jpeg|png|webp)[^"]*)"', html, re.I)
        if srcs:
            return srcs[0]
    except Exception as e:
        print(f"    搜索失败: {e}")
    return None

def download_image(url, filepath):
    """用curl下载图片"""
    cmd = [
        "curl", "-sL", "-o", filepath,
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "--connect-timeout", "10", "--max-time", "20",
        url
    ]
    r = subprocess.run(cmd, capture_output=True, timeout=30)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
        return True
    if os.path.exists(filepath):
        os.remove(filepath)
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
        url = bing_image_search(query)
        if not url:
            print(f"  [miss] {key}: 未找到图片")
            time.sleep(1)
            continue
        
        print(f"  下载 {url[:80]}...")
        if download_image(url, fp):
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
