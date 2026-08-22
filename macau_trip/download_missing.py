"""补下载缺失图片"""
import subprocess, re, urllib.parse, os, time
from pathlib import Path
from PIL import Image as PILImage

PROXY = "http://127.0.0.1:7890"
IMG_DIR = Path(r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip\images')

def download(query, filename):
    filepath = IMG_DIR / filename
    encoded = urllib.parse.quote(query)
    url = f"https://cn.bing.com/images/search?q={encoded}&first=1&count=5"
    try:
        r = subprocess.run(
            ["curl","-sL","--proxy",PROXY,
             "-H","User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             "-H","Referer: https://www.bing.com/",
             "--connect-timeout","10","--max-time","15", url],
            capture_output=True, text=True, timeout=20
        )
        html = r.stdout
        # Try murl first
        urls = re.findall(r'"murl":"(https?://[^"]+)"', html)
        urls = [re.sub(r'[&].*$', '', u) for u in urls if 'bing.com' not in u and 'microsoft' not in u.lower()]
        if not urls:
            # Try all image URLs
            all_urls = re.findall(r'https?://[^"\'\\s<>]+', html)
            urls = [u for u in all_urls if any(ext in u.lower() for ext in ['.jpg','.jpeg','.png']) and 'bing.com' not in u]
        
        if not urls:
            print(f"  [no url] {query}")
            return False
            
        img_url = urls[0]
        print(f"  Downloading from: {img_url[:80]}...")
        subprocess.run(
            ["curl","-sL","-o",str(filepath),
             "-H","User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             "-H","Referer: https://www.bing.com/",
             "--proxy",PROXY,"--connect-timeout","10","--max-time","20", img_url],
            capture_output=True, timeout=25
        )
        if filepath.exists() and filepath.stat().st_size > 5000:
            try:
                img = PILImage.open(filepath)
                img.verify()
                print(f"  OK: {filename} ({filepath.stat().st_size//1024}KB)")
                return True
            except:
                filepath.unlink(missing_ok=True)
                print(f"  [invalid] {query}")
                return False
        filepath.unlink(missing_ok=True)
        print(f"  [failed] {query}")
        return False
    except Exception as e:
        print(f"  [error] {e}")
        return False

# 缺失的图片
missing = [
    ("永利皇宫 Wynn Palace Macau", "wynn_palace.jpg"),
    ("永利皇宫缆车 SkyCab Macau", "skycab.jpg"),
    ("玫瑰圣母堂 Macau church", "st_dominic_new.jpg"),
    ("澳门蛋挞 Portuguese egg tart Macau", "macau_food.jpg"),
    ("澳门猪扒包 Macau pork chop bun", "macau_food2.jpg"),
]

for query, fname in missing:
    print(f"\nDownloading: {fname}...")
    download(query, fname)
    time.sleep(1.5)

# 验证
print("\n=== 验证新下载 ===")
for fname in ["wynn_palace.jpg","skycab.jpg","st_dominic_new.jpg","macau_food.jpg","macau_food2.jpg"]:
    fp = IMG_DIR / fname
    if fp.exists():
        try:
            img = PILImage.open(fp)
            print(f"  OK  {fname} ({fp.stat().st_size//1024}KB)")
        except:
            print(f"  BAD {fname}")
    else:
        print(f"  MISSING {fname}")
