"""补下载缺失图片 - 修复URL清洗"""
import subprocess, re, urllib.parse, os, time, html as html_mod
from pathlib import Path
from PIL import Image as PILImage

PROXY = "http://127.0.0.1:7890"
IMG_DIR = Path(r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\macau_trip\images')

def clean_url(url):
    """清理Bing返回的URL中的HTML实体和JSON残留"""
    url = html_mod.unescape(url)  # &quot; -> "
    url = re.sub(r'["\'].+$', '', url)  # 截断到引号
    url = re.sub(r'&[^a-z].*$', '', url)  # 截断到非标签&
    return url.strip()

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
        html_text = r.stdout
        
        # Extract all potential image URLs
        raw_urls = re.findall(r'https?://[^"\'\\s<>]+', html_text)
        # Filter for image extensions
        img_urls = [u for u in raw_urls if any(ext in u.lower() for ext in ['.jpg','.jpeg','.png','.webp'])]
        # Clean each URL
        img_urls = [clean_url(u) for u in img_urls]
        # Remove bing/microsoft domains
        img_urls = [u for u in img_urls if 'bing.com' not in u and 'microsoft' not in u.lower() and len(u) > 20]
        
        if not img_urls:
            print(f"  [no url] {query}")
            return False
            
        # Try first 3 URLs
        for img_url in img_urls[:3]:
            print(f"  Trying: {img_url[:80]}...")
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
                    continue
            filepath.unlink(missing_ok=True)
        
        print(f"  [all failed] {query}")
        return False
    except Exception as e:
        print(f"  [error] {e}")
        return False

# 缺失的图片
missing = [
    ("永利皇宫 Wynn Palace Macau performance lake", "wynn_palace.jpg"),
    ("澳门永利皇宫缆车 Wynn SkyCab", "skycab.jpg"),
    ("玫瑰圣母堂 St Dominic Church Macau", "st_dominic_v2.jpg"),
    ("澳门蛋挞 egg tart Macau", "macau_food.jpg"),
    ("澳门猪扒包 pork chop bun Macau", "macau_food2.jpg"),
]

for query, fname in missing:
    print(f"\nDownloading: {fname}...")
    download(query, fname)
    time.sleep(2)

# 验证
print("\n=== 验证 ===")
for fname in ["wynn_palace.jpg","skycab.jpg","st_dominic_v2.jpg","macau_food.jpg","macau_food2.jpg"]:
    fp = IMG_DIR / fname
    if fp.exists():
        try:
            img = PILImage.open(fp)
            print(f"  OK  {fname} ({fp.stat().st_size//1024}KB)")
        except:
            print(f"  BAD {fname}")
    else:
        print(f"  MISSING {fname}")
