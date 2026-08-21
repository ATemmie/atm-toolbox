"""用Leaflet.js + OpenStreetMap生成真实地图，用Playwright截图"""
import os, json

MAP_DIR = os.path.join(os.path.dirname(__file__), "maps")
os.makedirs(MAP_DIR, exist_ok=True)

# 坐标数据
DAY1 = [
    {"name": "威尼斯人", "lat": 22.1447, "lon": 113.5583, "label": "1.威尼斯人"},
    {"name": "妈阁庙", "lat": 22.1892, "lon": 113.5353, "label": "2.妈阁庙"},
    {"name": "澳门旅游塔", "lat": 22.1788, "lon": 113.5438, "label": "3.澳门塔"},
    {"name": "南湾湖", "lat": 22.1740, "lon": 113.5490, "label": "4.南湾湖"},
    {"name": "议事亭前地", "lat": 22.1920, "lon": 113.5430, "label": "5.议事亭前地"},
    {"name": "玫瑰圣母堂", "lat": 22.1945, "lon": 113.5420, "label": "6.玫瑰堂"},
    {"name": "大三巴牌坊", "lat": 22.1972, "lon": 113.5430, "label": "7.大三巴"},
    {"name": "大炮台", "lat": 22.1980, "lon": 113.5445, "label": "8.大炮台"},
]

DAY2 = [
    {"name": "威尼斯人", "lat": 22.1447, "lon": 113.5583, "label": "1.威尼斯人"},
    {"name": "官也街", "lat": 22.1485, "lon": 113.5540, "label": "2.官也街"},
    {"name": "嘉模圣母堂", "lat": 22.1505, "lon": 113.5530, "label": "3.嘉模圣母堂"},
    {"name": "龙环葡韵", "lat": 22.1535, "lon": 113.5540, "label": "4.龙环葡韵"},
    {"name": "永利皇宫", "lat": 22.1485, "lon": 113.5635, "label": "5.永利皇宫"},
    {"name": "银河", "lat": 22.1465, "lon": 113.5605, "label": "6.银河"},
    {"name": "巴黎人", "lat": 22.1445, "lon": 113.5585, "label": "7.巴黎人"},
    {"name": "伦敦人", "lat": 22.1435, "lon": 113.5565, "label": "8.伦敦人"},
]

def make_html(stops, title, filename):
    """生成Leaflet HTML地图"""
    lats = [s["lat"] for s in stops]
    lons = [s["lon"] for s in stops]
    center_lat = (min(lats) + max(lats)) / 2
    center_lon = (min(lons) + max(lons)) / 2
    
    markers_js = ""
    for i, s in enumerate(stops):
        color = ["#E17055", "#6C5CE7", "#00B894", "#0984E3", "#FDCB6E", "#E17055", "#6C5CE7", "#00B894",
                 "#0984E3", "#FDCB6E"][i % 10]
        markers_js += f"""
        L.circleMarker([{s['lat']}, {s['lon']}], {{
            radius: 12, fillColor: '{color}', color: '#fff', weight: 2, fillOpacity: 0.9
        }}).addTo(map).bindTooltip('{i+1}', {{permanent: true, direction: 'center', className: 'num-label'}});
        """
    
    polyline = ",".join([f"[{s['lat']},{s['lon']}]" for s in stops])
    
    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
    body {{ margin: 0; padding: 0; }}
    #map {{ width: 1200px; height: 800px; }}
    .num-label {{
        background: transparent; color: white; border: none;
        font-size: 14px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        font-family: Arial, sans-serif; padding: 0;
    }}
</style></head><body>
<div id="map"></div>
<script>
var map = L.map('map', {{zoomControl: true}}).setView([{center_lat}, {center_lon}], 14);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
}}).addTo(map);
{markers_js}
L.polyline([{polyline}], {{color: '#E17055', weight: 4, opacity: 0.8, dashArray: '10, 6'}}).addTo(map);
map.fitBounds(L.latLngBounds([{polyline}]).pad(0.1));
</script></body></html>"""
    
    html_path = os.path.join(MAP_DIR, filename.replace(".png", ".html"))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML地图: {html_path}")
    return html_path

def generate_maps():
    p1 = make_html(DAY1, "24日·澳门半岛路线（南→北）", "day1_route.html")
    p2 = make_html(DAY2, "25日·氹仔+路氹路线", "day2_route.html")
    return p1, p2

if __name__ == "__main__":
    generate_maps()
