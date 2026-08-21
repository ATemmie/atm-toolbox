"""生成澳门路线地图 - matplotlib绘制路线图"""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from config import DAY1_STOPS, DAY2_STOPS, VENETIAN

MAP_DIR = os.path.join(os.path.dirname(__file__), "maps")
os.makedirs(MAP_DIR, exist_ok=True)

# 尝试找到中文字体
def get_cn_font():
    for name in ["Microsoft YaHei", "SimHei", "NSimSun", "KaiTi", "STKaiti"]:
        matches = [f for f in fm.fontManager.ttflist if name in f.name]
        if matches:
            return matches[0].fname
    # fallback: 搜索系统字体
    for root in [r"C:\Windows\Fonts"]:
        for fn in os.listdir(root):
            if "msyh" in fn.lower() or "simhei" in fn.lower():
                return os.path.join(root, fn)
    return None

FONT_PATH = get_cn_font()
if FONT_PATH:
    prop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = prop.get_name()
    plt.rcParams["axes.unicode_minus"] = False

# 类型→颜色/标记
TYPE_STYLE = {
    "hotel":    {"color": "#6C5CE7", "marker": "H", "label": "酒店"},
    "heritage": {"color": "#E17055", "marker": "s", "label": "世遗/古迹"},
    "attraction":{"color": "#00B894","marker": "^", "label": "景点"},
    "scenic":   {"color": "#0984E3", "marker": "D", "label": "风景"},
    "food":     {"color": "#FDCB6E", "marker": "o", "label": "餐饮"},
}

def draw_route(stops, title, filename, day_label):
    """绘制一条路线图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    # 提取坐标
    lats = [s["lat"] for s in stops]
    lons = [s["lon"] for s in stops]
    padding = 0.006
    ax.set_xlim(min(lons) - padding, max(lons) + padding)
    ax.set_ylim(min(lats) - padding, max(lats) + padding)

    # 绘制路线（连接线）
    ax.plot(lons, lats, "-", color="#4a4a6a", linewidth=2, zorder=1, alpha=0.7)
    # 箭头方向
    for i in range(len(stops)-1):
        mx = (lons[i] + lons[i+1]) / 2
        my = (lats[i] + lats[i+1]) / 2
        dx = lons[i+1] - lons[i]
        dy = lats[i+1] - lats[i]
        length = math.sqrt(dx**2 + dy**2)
        if length > 0:
            ax.annotate("", xy=(mx+dx*0.01, my+dy*0.01),
                       xytext=(mx-dx*0.01, my-dy*0.01),
                       arrowprops=dict(arrowstyle="->", color="#a0a0c0", lw=1.5),
                       zorder=2)

    # 绘制景点标记
    used_labels = set()
    for i, s in enumerate(stops):
        style = TYPE_STYLE.get(s["type"], TYPE_STYLE["attraction"])
        label = style["label"] if style["label"] not in used_labels else None
        used_labels.add(style["label"])
        ax.scatter(s["lon"], s["lat"], c=style["color"], marker=style["marker"],
                  s=180, zorder=3, edgecolors="white", linewidths=0.8, label=label)
        # 序号
        ax.scatter(s["lon"], s["lat"], c="white", marker="$%d$" % (i+1),
                  s=60, zorder=4)
        # 名字标签（交替偏移避免重叠）
        offset_y = 0.0012 if i % 2 == 0 else -0.0018
        ax.annotate(s["name"], (s["lon"], s["lat"]),
                   xytext=(0, offset_y * 10000),
                   textcoords="offset points",
                   fontsize=9, color="white", ha="center",
                   fontproperties=fm.FontProperties(fname=FONT_PATH, size=9) if FONT_PATH else None,
                   bbox=dict(boxstyle="round,pad=0.2", facecolor=style["color"],
                            alpha=0.85, edgecolor="none"))

    ax.set_title(title, fontsize=16, color="white", pad=20,
                fontproperties=fm.FontProperties(fname=FONT_PATH, size=16) if FONT_PATH else None)
    ax.legend(loc="upper right", fontsize=9, facecolor="#1a1a2e",
             edgecolor="#4a4a6a", labelcolor="white",
             prop=fm.FontProperties(fname=FONT_PATH, size=9) if FONT_PATH else None)
    ax.tick_params(colors="#4a4a6a", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#4a4a6a")
    # 标注方向
    ax.annotate("南 → 北", xy=(0.02, 0.02), xycoords="axes fraction",
               fontsize=11, color="#4a4a6a", fontstyle="italic")

    path = os.path.join(MAP_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"地图已保存: {path}")
    return path

def generate_all_maps():
    p1 = draw_route(DAY1_STOPS, "24日·澳门半岛路线（南→北）", "day1_route.png", "Day1")
    p2 = draw_route(DAY2_STOPS, "25日·氹仔+路氹路线", "day2_route.png", "Day2")
    return p1, p2

if __name__ == "__main__":
    generate_all_maps()
