"""主入口：使用config.py的完整流程"""
import sys, os, asyncio
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    download_all_images, generate_map_html, screenshot_map,
    build_document, MAP_DIR, DAY1_STOPS, DAY2_STOPS, FINAL_DOC
)

def main():
    print("=" * 60)
    print("澳门家庭旅行执行表 — 文档生成 v2（美化版）")
    print("=" * 60)

    # 1. 下载图片
    print("\n[1/4] 下载景点图片...")
    img_dict = download_all_images()
    ok_count = sum(1 for v in img_dict.values() if v)
    print(f"\n图片: {ok_count}/{len(img_dict)} 成功")

    # 2. 生成地图HTML
    print("\n[2/4] 生成路线地图...")
    day1_html = generate_map_html(1, DAY1_STOPS, "Day 1: 澳门半岛 南→北")
    day2_html = generate_map_html(2, DAY2_STOPS, "Day 2: 氹仔+路氹")

    # 3. Playwright截图
    print("\n[3/4] 截图地图...")
    day1_png = str(MAP_DIR / "day1_map.png")
    day2_png = str(MAP_DIR / "day2_map.png")
    asyncio.run(screenshot_map(day1_html, day1_png))
    asyncio.run(screenshot_map(day2_html, day2_png))

    # 4. 组装Word文档
    print("\n[4/4] 组装Word文档...")
    output = build_document(day1_png, day2_png, img_dict)

    print(f"\n{'='*60}")
    print(f"DONE! Output: {output}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
