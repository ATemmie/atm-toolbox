"""澳门家庭旅行数据配置"""

# 威尼斯人坐标（参考点）
VENETIAN = (22.1447, 113.5583)

# === DAY 1: 澳门半岛 南→北 ===
DAY1_STOPS = [
    {"name": "威尼斯人", "en": "The Venetian", "lat": 22.1447, "lon": 113.5583,
     "time": "09:50", "note": "出发", "type": "hotel"},
    {"name": "妈阁庙", "en": "A-Ma Temple", "lat": 22.1892, "lon": 113.5353,
     "time": "10:20-11:00", "note": "免费·世界遗产·30-40min", "type": "heritage"},
    {"name": "澳门旅游塔", "en": "Macau Tower", "lat": 22.1788, "lon": 113.5438,
     "time": "11:30-13:00", "note": "观光层·室内避雨", "type": "attraction"},
    {"name": "午餐·澳门塔附近", "en": "Lunch near Tower", "lat": 22.1780, "lon": 113.5450,
     "time": "13:00-14:00", "note": "午餐休息", "type": "food"},
    {"name": "南湾湖", "en": "Nam Van Lake", "lat": 22.1740, "lon": 113.5490,
     "time": "14:15-14:45", "note": "免费·看城市湖景", "type": "scenic"},
    {"name": "议事亭前地", "en": "Senado Square", "lat": 22.1920, "lon": 113.5430,
     "time": "15:00-15:40", "note": "免费·世界遗产·步行区", "type": "heritage"},
    {"name": "玫瑰圣母堂", "en": "St. Dominic's", "lat": 22.1945, "lon": 113.5420,
     "time": "15:40-16:00", "note": "免费·快速参观", "type": "heritage"},
    {"name": "大三巴牌坊", "en": "Ruins of St. Paul's", "lat": 22.1972, "lon": 113.5430,
     "time": "16:20-17:00", "note": "免费·含恋爱巷/哪咤庙", "type": "heritage"},
    {"name": "大炮台", "en": "Monte Fort", "lat": 22.1980, "lon": 113.5445,
     "time": "17:00-17:40", "note": "晴天A·城市全景", "type": "attraction"},
    {"name": "晚餐·大三巴附近", "en": "Dinner near St. Paul's", "lat": 22.1955, "lon": 113.5410,
     "time": "18:00-19:30", "note": "葡国菜/本地餐厅", "type": "food"},
    {"name": "威尼斯人·夜游", "en": "Venetian Night", "lat": 22.1447, "lon": 113.5583,
     "time": "20:30-22:00", "note": "巴黎人+伦敦人夜景", "type": "hotel"},
]

# === DAY 2: 氹仔 东南→西北→路氹 ===
DAY2_STOPS = [
    {"name": "威尼斯人", "en": "The Venetian", "lat": 22.1447, "lon": 113.5583,
     "time": "10:15", "note": "出发·步行", "type": "hotel"},
    {"name": "官也街", "en": "Rua do Cunha", "lat": 22.1485, "lon": 113.5540,
     "time": "10:30-11:30", "note": "小吃·手信·葡挞", "type": "food"},
    {"name": "嘉模圣母堂", "en": "Our Lady of Carmel", "lat": 22.1505, "lon": 113.5530,
     "time": "11:30-11:40", "note": "免费·步行可达", "type": "heritage"},
    {"name": "龙环葡韵", "en": "Taipa Houses", "lat": 22.1535, "lon": 113.5540,
     "time": "12:00-13:00", "note": "澳门八景·葡式建筑群", "type": "scenic"},
    {"name": "午餐", "en": "Lunch", "lat": 22.1500, "lon": 113.5560,
     "time": "13:00-14:00", "note": "预约坐得舒服的餐厅", "type": "food"},
    {"name": "威尼斯人·午休", "en": "Venetian Rest", "lat": 22.1447, "lon": 113.5583,
     "time": "14:00-15:30", "note": "★关键休息·老人睡觉", "type": "hotel"},
    {"name": "永利皇宫", "en": "Wynn Palace", "lat": 22.1485, "lon": 113.5635,
     "time": "16:00-17:00", "note": "湖景·花艺·SkyCab", "type": "attraction"},
    {"name": "银河", "en": "Galaxy Macau", "lat": 22.1465, "lon": 113.5605,
     "time": "17:30-18:30", "note": "建筑·甜品·休息", "type": "hotel"},
    {"name": "巴黎人", "en": "Parisian Macao", "lat": 22.1445, "lon": 113.5585,
     "time": "19:00-19:30", "note": "巴黎铁塔夜景", "type": "hotel"},
    {"name": "伦敦人", "en": "Londoner Macao", "lat": 22.1435, "lon": 113.5565,
     "time": "19:30-20:00", "note": "大本钟·英伦建筑", "type": "hotel"},
    {"name": "晚餐·路氹", "en": "Dinner", "lat": 22.1440, "lon": 113.5575,
     "time": "20:00-21:00", "note": "伦敦人/威尼斯人内", "type": "food"},
    {"name": "威尼斯人", "en": "The Venetian", "lat": 22.1447, "lon": 113.5583,
     "time": "21:00", "note": "回酒店", "type": "hotel"},
]

# === 天气备选方案 ===
WEATHER_PLANS = {
    "day1_afternoon": {
        "sunny": "南湾湖→议事亭→大三巴→大炮台",
        "rain": "澳门塔→室内餐厅→议事亭短逛→大三巴→澳门博物馆",
        "storm": "澳门塔→室内商场→威尼斯人",
    },
    "day2_morning": {
        "sunny": "官也街→嘉模圣母堂→龙环葡韵→湿地",
        "rain": "官也街→室内商业区→午餐",
    },
    "day2_afternoon": {
        "sunny": "永利→SkyCab→银河→巴黎人→伦敦人",
        "rain": "永利室内→银河→巴黎人→伦敦人",
        "storm": "永利室内→威尼斯人→巴黎人→伦敦人",
    },
}

# 交通信息
TRANSPORT = {
    "priority": [
        ("🏨 酒店免费接驳", "免费、舒服"),
        ("🚕 6人特别的士", "6人一起走"),
        ("🚕 普通的士 ×2", "6人特别的士叫不到时"),
        ("🚌 公交", "天气好+不赶时间"),
        ("🚶 步行", "景点间很近时"),
    ],
    "bus_note": "24/25号是周一/周二，不依赖21AT/26AT周末特别线",
    "venetian_bus": "威尼斯人→机场/码头/关闸有免费穿梭巴士",
}

# 核心景点优先级
TOP10 = [
    ("⭐⭐⭐⭐⭐", "澳门旅游塔"),
    ("⭐⭐⭐⭐⭐", "大三巴牌坊"),
    ("⭐⭐⭐⭐⭐", "议事亭前地"),
    ("⭐⭐⭐⭐⭐", "官也街"),
    ("⭐⭐⭐⭐⭐", "龙环葡韵"),
    ("⭐⭐⭐⭐", "妈阁庙"),
    ("⭐⭐⭐⭐", "永利皇宫"),
    ("⭐⭐⭐⭐", "巴黎人"),
    ("⭐⭐⭐⭐", "伦敦人"),
    ("⭐⭐⭐⭐", "银河"),
]
