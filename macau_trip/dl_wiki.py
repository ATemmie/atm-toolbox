"""通过Wikimedia API下载景点图片"""
import os, json, time, requests

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# Wikimedia搜索关键词 → 文件名
SEARCHES = {
    "a_ma_temple": "A-Ma Temple Macau",
    "macau_tower": "Macau Tower",
    "senado_square": "Senado Square Macau",
    "st_pauls": "Ruins of St. Paul's Macau",
    "st_dominic": "Church of St. Dominic Macau",
    "monte_fort": "Monte Fort Macau",
    "nam_van_lake": "Nam Van Lake Macau",
    "rua_cunha": "Rua do Cunha Macau",
    "carmel_church": "Our Lady of Carmel Church Macau",
    "taipa_houses": "Taipa Houses Museum",
    "wynn_palace": "Wynn Palace Cotai",
    "parisian": "Parisian Macao",
    "londoner": "Londoner Macao",
    "galaxy": "Galaxy Macau",
    "venetian": "Venetian Macao",
}

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "MacauTripPlanner/1.0 (family-trip)"}

def search_and_download():
    results = {}
    for key, query in SEARCHES.items():
        fp = os.path.join(IMG_DIR, f"{key}.jpg")
        if os.path.exists(fp) and os.path.getsize(fp) > 1000:
            results[key] = fp
            print(f"  [skip] {key}")
            continue
        
        # Step 1: 搜索图片
        try:
            r = requests.get(API, params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srnamespace": 6,  # File namespace
                "srlimit": 1,
                "format": "json",
            }, headers=HEADERS, timeout=10)
            data = r.json()
            results_list = data.get("query", {}).get("search", [])
            if not results_list:
                print(f"  [miss] {key}: no search results for '{query}'")
                time.sleep(0.5)
                continue
            
            title = results_list[0]["title"]
            
            # Step 2: 获取图片URL
            r2 = requests.get(API, params={
                "action": "query",
                "titles": title,
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": 800,
                "format": "json",
            }, headers=HEADERS, timeout=10)
            data2 = r2.json()
            pages = data2["query"]["pages"]
            page = next(iter(pages.values()))
            info = page.get("imageinfo", [{}])[0]
            img_url = info.get("thumburl") or info.get("url")
            
            if not img_url:
                print(f"  [miss] {key}: no image URL")
                time.sleep(0.5)
                continue
            
            # Step 3: 下载
            r3 = requests.get(img_url, headers=HEADERS, timeout=15)
            if r3.status_code == 200 and len(r3.content) > 1000:
                with open(fp, "wb") as f:
                    f.write(r3.content)
                results[key] = fp
                print(f"  [ok] {key}: {title} ({len(r3.content)//1024}KB)")
            else:
                print(f"  [fail] {key}: HTTP {r3.status_code}")
        except Exception as e:
            print(f"  [err] {key}: {e}")
        time.sleep(0.8)
    
    idx = os.path.join(IMG_DIR, "_index.json")
    with open(idx, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 下载完成: {len(results)}/{len(SEARCHES)} 张")
    return results

if __name__ == "__main__":
    search_and_download()
