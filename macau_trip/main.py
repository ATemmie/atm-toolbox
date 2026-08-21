"""主入口：下载图片→生成地图→组装Word"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from download_images import download_images
from gen_map import generate_all_maps
from doc_content import (build_cover, build_day_section, build_weather_section,
                         build_transport_section, build_top10_section, build_day_type_table)
from doc_builder import create_document
from config import DAY1_STOPS, DAY2_STOPS

IMG_KEY_MAP = {
    "a_ma_temple": "妈阁庙", "macau_tower": "澳门旅游塔",
    "senado_square": "议事亭前地", "st_pauls": "大三巴",
    "st_dominic": "玫瑰圣母堂", "monte_fort": "大炮台",
    "nam_van_lake": "南湾湖", "rua_cunha": "官也街",
    "carmel_church": "嘉模圣母堂", "taipa_houses": "龙环葡韵",
    "wynn_palace": "永利皇宫", "parisian": "巴黎人",
    "londoner": "伦敦人", "galaxy": "银河", "venetian": "威尼斯人",
}

def main():
    print("=" * 50)
    print("🇲🇴 澳门家庭旅行文档生成器")
    print("=" * 50)

    # 1. 下载图片
    print("\n[1/3] 下载景点图片...")
    images = download_images()

    # 2. 生成路线地图
    print("\n[2/3] 生成路线地图...")
    map1, map2 = generate_all_maps()

    # 3. 组装Word文档
    print("\n[3/3] 组装Word文档...")
    doc = create_document()

    build_cover(doc)
    build_day_type_table(doc)
    build_day_section(
        doc, DAY1_STOPS,
        "🗓️ Day 1 · 8月24日（周一）· 澳门半岛 南→北",
        "E17055", IMG_KEY_MAP, map1, "day1_afternoon"
    )
    build_day_section(
        doc, DAY2_STOPS,
        "🗓️ Day 2 · 8月25日（周二）· 氹仔 + 路氹",
        "6C5CE7", IMG_KEY_MAP, map2, "day2_morning"
    )
    build_weather_section(doc)
    build_transport_section(doc)
    build_top10_section(doc)

    # 保存
    out = os.path.join(os.path.dirname(__file__), "澳门家庭旅行攻略.docx")
    doc.save(out)
    print(f"\n✅ 文档已保存: {out}")
    print(f"   图片: {len(images)} 张")
    print(f"   行程: Day1 {len(DAY1_STOPS)}站 + Day2 {len(DAY2_STOPS)}站")

if __name__ == "__main__":
    main()
