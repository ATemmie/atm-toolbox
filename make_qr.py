# -*- coding: utf-8 -*-
"""生成快捷指令安装二维码（指向 .shortcut 文件）"""
import qrcode, os

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
OUT = os.path.join(BASE, 'downloads', 'qr-go-usage.png')

# 二维码内容：shortcut 文件直链（Safari 打开后自动提示"在快捷指令中打开"）
url = 'https://atemmie.github.io/atm-toolbox/downloads/go-usage.shortcut'

qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=3)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color='#0b1020', back_color='white')
img.save(OUT)
print(f'✅ 二维码已生成: {OUT}')
print(f'   内容: {url}')
print(f'   大小: {os.path.getsize(OUT)} bytes')