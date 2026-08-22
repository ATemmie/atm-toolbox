from PIL import Image
import os
img_dir = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip\images'
for f in sorted(os.listdir(img_dir)):
    fp = os.path.join(img_dir, f)
    if os.path.isdir(fp) or f.endswith('.json') or f.endswith('.html'):
        continue
    try:
        img = Image.open(fp)
        sz = os.path.getsize(fp)
        print(f'  OK  {f:40s} {sz//1024:5d}KB')
    except Exception as e:
        print(f'  BAD {f:40s} {e}')
