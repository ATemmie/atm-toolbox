# -*- coding: utf-8 -*-
"""生成 ATM 工具箱 PWA 图标（192/512 PNG，深色渐变底 + 猫爪/工具箱风格）"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\icons'
os.makedirs(OUT, exist_ok=True)

def make_icon(size, path):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 深色渐变圆角方底（靛紫青）
    for y in range(size):
        t = y / size
        r = int(15 + 30 * t)
        g = int(20 + 45 * t)
        b = int(45 + 90 * t)
        d.rectangle([0, y, size, y + 1], fill=(r, g, b, 255))
    # 圆角遮罩
    mask = Image.new('L', (size, size), 0)
    md = ImageDraw.Draw(mask)
    rad = int(size * 0.22)
    md.rounded_rectangle([0, 0, size, size], radius=rad, fill=255)
    img.putalpha(mask)

    # 中央发光圆圈（靛→紫→青渐变感：画三层圆）
    cx, cy = size // 2, size // 2
    r1 = int(size * 0.30)
    d.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], fill=(124, 92, 255, 230))       # 紫
    r2 = int(size * 0.22)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(72, 187, 255, 235))       # 青
    # 顶部高光
    r3 = int(size * 0.13)
    d.ellipse([cx - r3, cy - r3 - int(size*0.05), cx + r3, cy + r3 - int(size*0.05)], fill=(220, 240, 255, 255))

    # 猫耳（剪影）
    earh = int(size * 0.28)
    earw = int(size * 0.22)
    # 左耳
    d.polygon([(cx - r1, cy - r1 + int(size*0.10)), (cx - r1 - earw, cy - r1 - earh + int(size*0.10)),
               (cx - r1 + int(size*0.02), cy - r1 - earh + int(size*0.10))], fill=(72, 187, 255, 235))
    # 右耳
    d.polygon([(cx + r1, cy - r1 + int(size*0.10)), (cx + r1 + earw, cy - r1 - earh + int(size*0.10)),
               (cx + r1 - int(size*0.02), cy - r1 - earh + int(size*0.10))], fill=(72, 187, 255, 235))

    img.save(path, 'PNG')
    print(f"OK {path} {size}x{size}")

make_icon(192, os.path.join(OUT, 'icon-192.png'))
make_icon(512, os.path.join(OUT, 'icon-512.png'))
make_icon(180, os.path.join(OUT, 'apple-touch-icon.png'))