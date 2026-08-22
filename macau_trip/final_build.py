"""最终版：完整图片映射 + 生成文档"""
import sys, os
sys.path.insert(0, r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip')
from config import DAY1_STOPS, DAY2_STOPS, MAP_DIR, FINAL_DOC, build_document, generate_map_html, screenshot_map
import asyncio
from PIL import Image as PILImage

IMG_DIR = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip\images'

# 完整映射: en_name -> 本地文件名
IMAGE_MAP = {
    "The Venetian Macao": "venetian.jpg",
    "A-Ma Temple": "a_ma_temple.jpg",
    "Macau Tower": "macau_tower.jpg",
    "Nam Van Lake": "nam_van_lake.jpg",
    "Senado Square": "senado_square.jpg",
    "St. Dominic's Church": "st_dominic.jpg",  # 会跳过(BAD)
    "Ruins of St. Paul's": "st_pauls.jpg",
    "Monte Fort": "monte_fort.jpg",
    "Dinner near Senado": "macau_food.jpg",
    "The Parisian Macao": "parisian.jpg",
    "The Londoner Macao": "londoner.jpg",
    "Rua do Cunha": "rua_cunha.jpg",
    "Chapel of Our Lady of Carmel": "carmel_church.jpg",
    "Taipa Houses-Museum": "taipa_houses.jpg",
    "Lunch Taipa": "macau_food2.jpg",
    "Rest at Venetian": "venetian.jpg",
    "Wynn Palace": "wynn_palace.jpg",
    "SkyCab Wynn Palace": "skycab.jpg",
    "Galaxy Macau": "galaxy.jpg",
    "Dinner Cotai": "Dinner_Cotai.jpg",
}

def get_img_dict():
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
                    print(f"  [ok] {key} -> {fname}")
                    continue
                except Exception as e:
                    print(f"  [bad] {key} -> {fname}: {e}")
        result[key] = None
        print(f"  [--] {key}")
    return result

async def main():
    print("=== 最终版文档生成 ===\n")
    
    print("[1/3] 映射图片...")
    img_dict = get_img_dict()
    ok = sum(1 for v in img_dict.values() if v)
    print(f"  成功: {ok}/{len(img_dict)}\n")
    
    print("[2/3] 生成地图...")
    day1_html = generate_map_html(1, DAY1_STOPS, "Day 1: 澳门半岛 南→北")
    day2_html = generate_map_html(2, DAY2_STOPS, "Day 2: 氹仔+路氹")
    day1_png = str(MAP_DIR / "day1_map.png")
    day2_png = str(MAP_DIR / "day2_map.png")
    await screenshot_map(day1_html, day1_png)
    await screenshot_map(day2_html, day2_png)
    
    print("\n[3/3] 组装Word文档...")
    output = build_document(day1_png, day2_png, img_dict)
    print(f"\n✅ 完成: {output}")

asyncio.run(main())
