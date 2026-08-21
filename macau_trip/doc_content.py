"""生成澳门旅行Word文档 - Part 2: 内容填充"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from config import DAY1_STOPS, DAY2_STOPS, WEATHER_PLANS, TRANSPORT, TOP10, VENETIAN
from doc_builder import (create_document, add_heading_styled, add_para,
                         add_image_if_exists, load_images, set_cell_shading)

IMG_MAP = {
    "a_ma_temple": "妈阁庙", "macau_tower": "澳门旅游塔",
    "senado_square": "议事亭前地", "st_pauls": "大三巴牌坊",
    "st_dominic": "玫瑰圣母堂", "monte_fort": "大炮台",
    "nam_van_lake": "南湾湖", "rua_cunha": "官也街",
    "carmel_church": "嘉模圣母堂", "taipa_houses": "龙环葡韵",
    "wynn_palace": "永利皇宫", "parisian": "巴黎人",
    "londoner": "伦敦人", "galaxy": "银河", "venetian": "威尼斯人",
}

def build_cover(doc):
    """封面页"""
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("🇲🇴 澳门家庭旅行攻略")
    run.font.size = Pt(28)
    run.bold = True
    run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run("6人家庭 · 2天1夜 · 威尼斯人出发")
    run2.font.size = Pt(14)
    run2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run3 = p3.add_run("2026年8月23日-25日")
    run3.font.size = Pt(13)
    run3.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

    doc.add_paragraph()
    info_lines = [
        "👨‍👩‍👧‍👦 3大人 + 2老人 + 1小孩",
        "🏨 住宿：威尼斯人",
        "✈️ 23日晚抵达 · 24/25日游玩",
        "🚌 交通：的士为主 + 公交为辅 + 步行",
    ]
    for line in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line)
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_page_break()

def build_timeline_table(doc, stops, day_label, color_hex):
    """为每天构建时间轴表格"""
    add_heading_styled(doc, day_label, level=2, color=RGBColor(*bytes.fromhex(color_hex)))
    doc.add_paragraph()

    cols_w = [Cm(1.2), Cm(3.2), Cm(3.8), Cm(6.5)]
    table = doc.add_table(rows=1, cols=4)
    table.alignment = 1  # CENTER
    table.style = "Table Grid"

    # 表头
    headers = ["序号", "时间", "地点", "备注/说明"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, color_hex)

    # 数据行
    for idx, s in enumerate(stops):
        row = table.add_row()
        cells = row.cells
        vals = [str(idx+1), s["time"], s["name"], s["note"]]
        for j, v in enumerate(vals):
            cells[j].text = ""
            p = cells[j].paragraphs[0]
            r = p.add_run(v)
            r.font.size = Pt(9)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j < 2 else WD_ALIGN_PARAGRAPH.LEFT
        # 交替背景色
        bg = "F5F5F5" if idx % 2 == 0 else "FFFFFF"
        for c in cells:
            set_cell_shading(c, bg)

    doc.add_paragraph()

def build_day_section(doc, stops, day_label, color_hex, img_keys_map, map_path, plan_key):
    """完整的一天行程"""
    build_timeline_table(doc, stops, day_label, color_hex)

    # 路线地图
    add_para(doc, "📍 路线地图", bold=True, size=13)
    if map_path and os.path.exists(map_path):
        add_image_if_exists(doc, map_path, width=Inches(5.8))
    doc.add_paragraph()

    # 景点图文卡片
    add_heading_styled(doc, "🏛️ 景点详情", level=3)
    for s in stops:
        if s["type"] == "food":
            continue
        # 景点名 + 时间
        p = doc.add_paragraph()
        r = p.add_run(f"▶ {s['name']}  ")
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)
        r2 = p.add_run(f"⏰ {s['time']}")
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

        # 图片
        for key, name in img_keys_map.items():
            if name in s["name"] or s["name"] in name:
                img_path = os.path.join("images", f"{key}.jpg")
                add_image_if_exists(doc, img_path, width=Inches(4.5))
                break

        add_para(doc, f"   {s['note']}", size=10, color=RGBColor(0x66, 0x66, 0x66))

    doc.add_page_break()

def build_weather_section(doc):
    """天气备选方案"""
    add_heading_styled(doc, "🌧️ 天气备选方案（A/B/C）", level=2)
    add_para(doc, "以下为关键时段的晴天/雨天/暴雨三套方案，随时切换：", size=10)

    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    headers = ["时段", "☀️ 晴天", "🌧️ 下雨", "⛈️ 暴雨"]
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "34495E")

    labels = {"day1_afternoon": "24日下午", "day2_morning": "25日上午", "day2_afternoon": "25日下午"}
    for key, label in labels.items():
        plans = WEATHER_PLANS[key]
        row = table.add_row()
        vals = [label, plans["sunny"], plans["rain"], plans.get("storm", "-")]
        for j, v in enumerate(vals):
            row.cells[j].text = ""
            p = row.cells[j].paragraphs[0]
            r = p.add_run(v)
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
    doc.add_paragraph()

def build_transport_section(doc):
    """交通指南"""
    add_heading_styled(doc, "🚕 交通指南", level=2)
    add_para(doc, "6人家庭出行，交通优先级排序：", size=10, bold=True)

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    for i, h in enumerate(["优先级", "方式", "说明"]):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, "2D3436")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for idx, (mode, desc) in enumerate(TRANSPORT["priority"]):
        row = table.add_row()
        for j, v in enumerate([medals[idx], mode, desc]):
            row.cells[j].text = ""
            p = row.cells[j].paragraphs[0]
            r = p.add_run(v)
            r.font.size = Pt(9)

    add_para(doc, "")
    add_para(doc, "⚠️ 注意：24/25号是周一/周二，不依赖21AT/26AT周末特别线路", size=10, color=RGBColor(0xE1, 0x70, 0x55))
    add_para(doc, "🏨 威尼斯人提供机场/码头/关闸免费穿梭巴士", size=10)

def build_top10_section(doc):
    """必去景点TOP10"""
    add_heading_styled(doc, "⭐ 必去景点TOP 10", level=2)
    add_para(doc, "如天气极差需砍行程，按此优先级保留：", size=10)

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    for i, h in enumerate(["优先级", "景点", "说明"]):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, "E17055")

    for stars, name in TOP10:
        row = table.add_row()
        for j, v in enumerate([stars, name, ""]):
            row.cells[j].text = ""
            p = row.cells[j].paragraphs[0]
            r = p.add_run(v)
            r.font.size = Pt(9)
            if j == 0:
                r.font.size = Pt(8)

    add_para(doc, "")
    add_para(doc, "💡 大炮台、南湾湖、SkyCab、湿地属于「天气好就赚到」类型，不强求", size=10, color=RGBColor(0x88, 0x88, 0x88))

def build_day_type_table(doc):
    """每日主题对比"""
    add_heading_styled(doc, "📅 每日主题概览", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    for i, h in enumerate(["时段", "24日（澳门半岛）", "25日（氹仔+路氹）"]):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, "6C5CE7")

    themes = [
        ("上午", "古迹 + 高空景观", "葡式生活 + 风景"),
        ("下午", "老城 + 人文", "度假酒店 + 缆车"),
        ("晚上", "酒店夜景", "路氹夜景"),
    ]
    for t, d1, d2 in themes:
        row = table.add_row()
        for j, v in enumerate([t, d1, d2]):
            row.cells[j].text = ""
            p = row.cells[j].paragraphs[0]
            r = p.add_run(v)
            r.font.size = Pt(9)
    doc.add_paragraph()
