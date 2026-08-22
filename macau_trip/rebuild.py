"""修复图片映射 + 重新生成文档"""
import sys, os
sys.path.insert(0, r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip')
from config import DAY1_STOPS, DAY2_STOPS, MAP_DIR, FINAL_DOC, build_document, generate_map_html, screenshot_map
import asyncio

IMG_DIR = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip\images'

# 手动映射: en_name -> 本地文件名
IMAGE_MAP = {
    "The Venetian Macao": "venetian.jpg",
    "A-Ma Temple": "a_ma_temple.jpg",
    "Macau Tower": "macau_tower.jpg",
    "Nam Van Lake": "nam_van_lake.jpg",
    "Senado Square": "senado_square.jpg",
    "St. Dominic's Church": "st_dominic.jpg",  # BAD, will skip
    "Ruins of St. Paul's": "st_pauls.jpg",
    "Monte Fort": "monte_fort.jpg",
    "Dinner near Senado": None,
    "The Parisian Macao": "parisian.jpg",
    "The Londoner Macao": "londoner.jpg",
    "Rua do Cunha": "rua_cunha.jpg",
    "Chapel of Our Lady of Carmel": "carmel_church.jpg",
    "Taipa Houses-Museum": "taipa_houses.jpg",
    "Lunch Taipa": None,
    "Rest at Venetian": "venetian.jpg",
    "Wynn Palace": None,
    "SkyCab Wynn Palace": None,
    "Galaxy Macau": "galaxy.jpg",
    "Dinner Cotai": "Dinner_Cotai.jpg",
}

def get_img_dict():
    from PIL import Image as PILImage
    result = {}
    all_stops = DAY1_STOPS + DAY2_STOPS
    seen = set()
    for stop in all_stops:
        key = stop["en"]
        if key in seen:
            result[key] = result.get(key)
            continue
        seen.add(key)
        fname = IMAGE_MAP.get(key)
        if fname:
            fp = os.path.join(IMG_DIR, fname)
            if os.path.exists(fp) and os.path.getsize(fp) > 5000:
                try:
                    img = PILImage.open(fp)
                    img.verify()
                    result[key] = fp
                    print(f"  [mapped] {key} -> {fname}")
                    continue
                except Exception:
                    pass
        result[key] = None
        print(f"  [missing] {key}")
    return result

async def main():
    print("=== 修复版文档生成 ===\n")
    
    # 1. 图片映射
    print("[1/3] 映射图片...")
    img_dict = get_img_dict()
    ok = sum(1 for v in img_dict.values() if v)
    print(f"  成功映射: {ok}/{len(img_dict)}\n")
    
    # 2. 地图
    print("[2/3] 生成地图...")
    day1_html = generate_map_html(1, DAY1_STOPS, "Day 1: 澳门半岛 南→北")
    day2_html = generate_map_html(2, DAY2_STOPS, "Day 2: 氹仔+路氹")
    day1_png = str(MAP_DIR / "day1_map.png")
    day2_png = str(MAP_DIR / "day2_map.png")
    await screenshot_map(day1_html, day1_png)
    await screenshot_map(day2_html, day2_png)
    
    # 3. 文档
    print("\n[3/3] 组装Word文档...")
    output = build_document(day1_png, day2_png, img_dict)
    print(f"\n✅ 完成: {output}")

asyncio.run(main())
