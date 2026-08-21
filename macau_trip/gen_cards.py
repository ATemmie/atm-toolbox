"""用Pillow生成精美景点占位卡片"""
import os
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 景点信息：名字、英文、渐变色
CARDS = {
    "a_ma_temple": ("妈阁庙", "A-Ma Temple", (139, 69, 19), (210, 105, 30)),
    "macau_tower": ("澳门旅游塔", "Macau Tower", (25, 25, 112), (0, 191, 255)),
    "senado_square": ("议事亭前地", "Senado Square", (70, 130, 180), (135, 206, 235)),
    "st_pauls": ("大三巴牌坊", "Ruins of St. Paul's", (178, 34, 34), (220, 20, 60)),
    "st_dominic": ("玫瑰圣母堂", "St. Dominic's", (188, 143, 143), (219, 112, 147)),
    "monte_fort": ("大炮台", "Monte Fort", (85, 107, 47), (107, 142, 35)),
    "nam_van_lake": ("南湾湖", "Nam Van Lake", (0, 128, 128), (72, 209, 204)),
    "rua_cunha": ("官也街", "Rua do Cunha", (210, 105, 30), (255, 165, 0)),
    "carmel_church": ("嘉模圣母堂", "Our Lady of Carmel", (139, 90, 43), (205, 133, 63)),
    "taipa_houses": ("龙环葡韵", "Taipa Houses", (46, 125, 50), (129, 199, 132)),
    "wynn_palace": ("永利皇宫", "Wynn Palace", (139, 0, 0), (220, 20, 60)),
    "parisian": ("巴黎人", "The Parisian", (0, 51, 102), (0, 102, 204)),
    "londoner": ("伦敦人", "Londoner Macao", (25, 25, 75), (65, 65, 130)),
    "galaxy": ("银河", "Galaxy Macau", (72, 61, 139), (138, 120, 200)),
    "venetian": ("威尼斯人", "The Venetian", (128, 0, 128), (186, 85, 211)),
}

def get_font(size):
    """尝试加载中文字体"""
    for name in ["msyh.ttc", "msyhbd.ttc", "simhei.ttf", "simsun.ttc"]:
        for root in [r"C:\Windows\Fonts"]:
            p = os.path.join(root, name)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except:
                    pass
    return ImageFont.load_default()

def make_card(key, cn_name, en_name, color1, color2):
    """生成渐变背景的景点卡片"""
    W, H = 800, 500
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    
    # 渐变背景
    for y in range(H):
        ratio = y / H
        r = int(color1[0] * (1-ratio) + color2[0] * ratio)
        g = int(color1[1] * (1-ratio) + color2[1] * ratio)
        b = int(color1[2] * (1-ratio) + color2[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # 半透明装饰条
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([0, H-120, W, H], fill=(0, 0, 0, 120))
    img.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (0,0,0,0)), overlay).convert("RGB"))
    draw = ImageDraw.Draw(img)
    
    # 装饰线条
    draw.line([(60, 180), (W-60, 180)], fill=(255, 255, 255, 180), width=1)
    
    # 中文名（大）
    font_cn = get_font(64)
    bbox = draw.textbbox((0, 0), cn_name, font=font_cn)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 220), cn_name, fill="white", font=font_cn)
    
    # 英文名
    font_en = get_font(28)
    bbox2 = draw.textbbox((0, 0), en_name, font=font_en)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, 300), en_name, fill=(220, 220, 220), font=font_en)
    
    # 底部装饰文字
    font_sm = get_font(16)
    draw.text((60, H-80), "🇲🇴 澳门 · Macau", fill=(180, 180, 180), font=font_sm)
    
    # 角落装饰
    draw.arc([W-100, 20, W-20, 100], 0, 360, fill=(255, 255, 255, 80), width=2)
    draw.arc([20, H-120, 100, H-40], 0, 360, fill=(255, 255, 255, 80), width=2)
    
    fp = os.path.join(IMG_DIR, f"{key}.jpg")
    img.save(fp, "JPEG", quality=90)
    return fp

def generate_all():
    for key, (cn, en, c1, c2) in CARDS.items():
        make_card(key, cn, en, c1, c2)
        print(f"  [ok] {cn}")
    print(f"\n✅ 生成 {len(CARDS)} 张景点卡片")

if __name__ == "__main__":
    generate_all()
