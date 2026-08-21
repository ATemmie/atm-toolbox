"""下载景点图片 - 从Wikimedia Commons获取免费图片"""
import os, time, requests, json

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# Wikimedia Commons图片URL（直接可用的缩略图）
ATTRACTIONS = {
    "a_ma_temple": {
        "name": "妈阁庙",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/A-Ma_Temple_Macau_2019.jpg/800px-A-Ma_Temple_Macau_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/A-Ma_Temple.JPG/800px-A-Ma_Temple.JPG",
        ]
    },
    "macau_tower": {
        "name": "澳门旅游塔",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Macau_Tower_2019.jpg/600px-Macau_Tower_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Macau_Tower.jpg/600px-Macau_Tower.jpg",
        ]
    },
    "senado_square": {
        "name": "议事亭前地",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Senado_Square_Macau_2019.jpg/800px-Senado_Square_Macau_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Leal_Senado_Building%2C_Senado_Square%2C_Macau.jpg/800px-Leal_Senado_Building%2C_Senado_Square%2C_Macau.jpg",
        ]
    },
    "st_pauls": {
        "name": "大三巴牌坊",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Ruinas_de_Sao_Paulo%2C_Macau_%2836915534454%29.jpg/800px-Ruinas_de_Sao_Paulo%2C_Macau_%2836915534454%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Ruins_of_St._Paul%27s.jpg/800px-Ruins_of_St._Paul%27s.jpg",
        ]
    },
    "st_dominic": {
        "name": "玫瑰圣母堂",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Igreja_de_Santo_Domingos_2019.jpg/600px-Igreja_de_Santo_Domingos_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Church_of_St_Dominic_Macau.jpg/600px-Church_of_St_Dominic_Macau.jpg",
        ]
    },
    "monte_fort": {
        "name": "大炮台",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Monte_Fort_Macau_2019.jpg/800px-Monte_Fort_Macau_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Monte_Fort_Macau.jpg/800px-Monte_Fort_Macau.jpg",
        ]
    },
    "nam_van_lake": {
        "name": "南湾湖",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Nam_Van_Lake_Macau.jpg/800px-Nam_Van_Lake_Macau.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Central_Macau_skyline_from_Nam_Van_Lake_Nautical_Centre.jpg/800px-Central_Macau_skyline_from_Nam_Van_Lake_Nautical_Centre.jpg",
        ]
    },
    "rua_cunha": {
        "name": "官也街",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Rua_do_Cunha_2019.jpg/600px-Rua_do_Cunha_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Taipa_village_entrance.jpg/600px-Taipa_village_entrance.jpg",
        ]
    },
    "carmel_church": {
        "name": "嘉模圣母堂",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Igreja_de_Nossa_Senhora_do_Carmo%2C_Macau_%2801%29.jpg/600px-Igreja_de_Nossa_Senhora_do_Carmo%2C_Macau_%2801%29.jpg",
        ]
    },
    "taipa_houses": {
        "name": "龙环葡韵",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Taipa_Houses_Museum_2019.jpg/800px-Taipa_Houses_Museum_2019.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Casas-Museu_da_Taipa.jpg/800px-Casas-Museu_da_Taipa.jpg",
        ]
    },
    "wynn_palace": {
        "name": "永利皇宫",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Wynn_Palace_Cotai.jpg/800px-Wynn_Palace_Cotai.jpg",
        ]
    },
    "parisian": {
        "name": "巴黎人",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/The_Parisian_Macao.jpg/600px-The_Parisian_Macao.jpg",
        ]
    },
    "londoner": {
        "name": "伦敦人",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Londoner_Macao_2023.jpg/800px-Londoner_Macao_2023.jpg",
        ]
    },
    "galaxy": {
        "name": "银河",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Galaxy_Macau_2019.jpg/800px-Galaxy_Macau_2019.jpg",
        ]
    },
    "venetian": {
        "name": "威尼斯人",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Venetian_Macau_2019.jpg/800px-Venetian_Macau_2019.jpg",
        ]
    },
}

def download_images():
    """下载所有景点图片，每个景点取第一张可用的"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MacauTravelPlanner/1.0"
    }
    results = {}
    for key, info in ATTRACTIONS.items():
        filepath = os.path.join(IMG_DIR, f"{key}.jpg")
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            results[key] = filepath
            print(f"  [skip] {info['name']} 已存在")
            continue
        for url in info["urls"]:
            try:
                print(f"  下载 {info['name']}...")
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200 and len(r.content) > 1000:
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                    results[key] = filepath
                    print(f"  [ok] {info['name']} ({len(r.content)//1024}KB)")
                    break
            except Exception as e:
                print(f"  [fail] {info['name']}: {e}")
            time.sleep(0.5)
        else:
            print(f"  [miss] {info['name']} 所有URL均失败")
        time.sleep(0.3)
    
    # 保存索引
    idx_path = os.path.join(IMG_DIR, "_index.json")
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n共下载/缓存 {len(results)}/{len(ATTRACTIONS)} 张图片")
    return results

if __name__ == "__main__":
    download_images()
