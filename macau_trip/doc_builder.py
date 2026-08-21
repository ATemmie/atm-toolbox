"""生成澳门旅行Word文档 - Part 1: 基础框架和样式"""
import os, json
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "images")
MAP_DIR = os.path.join(BASE_DIR, "maps")

# ========== 样式工具 ==========
def set_cell_shading(cell, color_hex):
    """设置表格单元格背景色"""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_border(cell, **kwargs):
    """设置单元格边框"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}></w:tcBorders>')
    for edge, val in kwargs.items():
        element = parse_xml(
            f'<w:{edge} {nsdecls("w")} w:val="{val.get("val","single")}" '
            f'w:sz="{val.get("sz","4")}" w:space="0" '
            f'w:color="{val.get("color","auto")}"/>'
        )
        tcBorders.append(element)
    tcPr.append(tcBorders)

def add_heading_styled(doc, text, level=1, color=RGBColor(0x1a, 0x1a, 0x2e)):
    """添加带样式的标题"""
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = color
    return h

def add_para(doc, text, bold=False, size=11, color=None, align=None, space_after=6):
    """添加段落"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p

def add_image_if_exists(doc, img_path, width=Inches(5.5)):
    """添加图片（如果文件存在且是有效图片）"""
    if not img_path or not os.path.exists(img_path):
        return False
    size = os.path.getsize(img_path)
    if size < 5000:
        return False
    # 验证是否为真实图片文件
    try:
        from PIL import Image as PILImage
        img = PILImage.open(img_path)
        img.verify()
    except Exception:
        return False
    try:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(img_path, width=width)
        return True
    except Exception:
        return False

def load_images():
    """加载图片索引"""
    idx_path = os.path.join(IMG_DIR, "_index.json")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def create_document():
    """创建Word文档并设置基础样式"""
    doc = Document()
    # 页面设置
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    # 默认字体
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Microsoft YaHei"
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    rFonts = style.element.rPr.rFonts if style.element.rPr is not None else None
    if rFonts is None:
        style.element.get_or_add_rPr()
    rpr = style.element.rPr
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="Microsoft YaHei"/>')
        rpr.append(rfonts)
    else:
        rfonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    return doc
