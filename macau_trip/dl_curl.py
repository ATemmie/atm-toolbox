"""用curl从Wikimedia下载图片，带完整headers"""
import os, json, subprocess, time

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 已知的Wikimedia Commons图片直链（thumb URL，800px宽）
# 直接用缩略图URL避免API限流
KNOWN_IMAGES = {
    "a_ma_temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/A-Ma_Temple_Macau_2019.jpg/800px-A-Ma_Temple_Macau_2019.jpg",
    "macau_tower": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Macau_Tower_2016.jpg/600px-Macau_Tower_2016.jpg",
    "senado_square": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Senado_Square_Macau_2019.jpg/800px-Senado_Square_Macau_2019.jpg",
    "st_pauls": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Ruins_of_St._Paul%27s.jpg/800px-Ruins_of_St._Paul%27s.jpg",
    "st_dominic": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Church_of_St_Dominic_Macau.jpg/600px-Church_of_St_Dominic_Macau.jpg",
    "monte_fort": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Monte_Fort_Macau.jpg/800px-Monte_Fort_Macau.jpg",
    "nam_van_lake": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Central_Macau_skyline_from_Nam_Van_Lake_Nautical_Centre.jpg/800px-Central_Macau_skyline_from_Nam_Van_Lake_Nautical_Centre.jpg",
    "rua_cunha": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Taipa_village_-_panoramio.jpg/600px-Taipa_village_-_panoramio.jpg",
    "carmel_church": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Igreja_de_Nossa_Senhora_do_Carmo_2024.jpg/600px-Igreja_de_Nossa_Senhora_do_Carmo_2024.jpg",
    "taipa_houses": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Casas-Museu_da_Taipa.jpg/800px-Casas-Museu_da_Taipa.jpg",
    "wynn_palace": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Wynn_Palace%2C_Cotai%2C_Macau_%2820230218170940%29.jpg/800px-Wynn_Palace%2C_Cotai%2C_Macau_%2820230218170940%29.jpg",
    "parisian": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/The_Parisian_Macao_%28exterior%29.jpg/600px-The_Parisian_Macao_%28exterior%29.jpg",
    "londoner": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/The_Londoner_Macao_%28exterior%29.jpg/800px-The_Londoner_Macao_%28exterior%29.jpg",
    "galaxy": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Galaxy_Macau_2019.jpg/800px-Galaxy_Macau_2019.jpg",
    "venetian": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/The_Venetian_Macao_%28exterior%29.jpg/800px-The_Venetian_Macao_%28exterior%29.jpg",
}

def download():
    results = {}
    for key, url in KNOWN_IMAGES.items():
        fp = os.path.join(IMG_DIR, f"{key}.jpg")
        if os.path.exists(fp) and os.path.getsize(fp) > 1000:
            results[key] = fp
            print(f"  [skip] {key}")
            continue
        cmd = [
            "curl", "-sL", "-o", fp,
            "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) MacauTrip/1.0",
            "-H", "Accept: image/webp,image/apng,image/*,*/*",
            "--connect-timeout", "10",
            "--max-time", "20",
            url
        ]
        r = subprocess.run(cmd, capture_output=True, timeout=30)
        if os.path.exists(fp) and os.path.getsize(fp) > 1000:
            size = os.path.getsize(fp) // 1024
            results[key] = fp
            print(f"  [ok] {key} ({size}KB)")
        else:
            print(f"  [fail] {key}")
            if os.path.exists(fp):
                os.remove(fp)
        time.sleep(1.5)
    
    idx = os.path.join(IMG_DIR, "_index.json")
    with open(idx, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {len(results)}/{len(KNOWN_IMAGES)} 张图片")
    return results

if __name__ == "__main__":
    download()
