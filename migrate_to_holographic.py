"""
Holographic Memory Migration Script
将 Wiki + MEMORY.md 数据迁移至 Holographic SQLite 数据库
"""
import sqlite3
import json
import os
from datetime import datetime

HERMES_HOME = os.environ.get(
    "HERMES_HOME",
    os.path.expanduser("~/AppData/Roaming/cn.org.hermesagent.desktop/runtime/hermes-home")
)
DB_PATH = os.path.join(HERMES_HOME, "memory_store.db")

def create_schema(conn):
    """创建 Holographic 记忆数据库 schema"""
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        entity TEXT,
        category TEXT DEFAULT 'general',
        trust_score REAL DEFAULT 0.5,
        source TEXT,
        tags TEXT DEFAULT '[]',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        access_count INTEGER DEFAULT 0,
        helpful_count INTEGER DEFAULT 0,
        unhelpful_count INTEGER DEFAULT 0,
        metadata TEXT DEFAULT '{}'
    );
    
    CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
        content, entity, category, tags,
        content='facts',
        content_rowid='id'
    );
    
    CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON facts BEGIN
        INSERT INTO facts_fts(rowid, content, entity, category, tags)
        VALUES (new.id, new.content, new.entity, new.category, new.tags);
    END;
    
    CREATE TRIGGER IF NOT EXISTS facts_ad AFTER DELETE ON facts BEGIN
        INSERT INTO facts_fts(facts_fts, rowid, content, entity, category, tags)
        VALUES ('delete', old.id, old.content, old.entity, old.category, old.tags);
    END;
    
    CREATE TRIGGER IF NOT EXISTS facts_au AFTER UPDATE ON facts BEGIN
        INSERT INTO facts_fts(facts_fts, rowid, content, entity, category, tags)
        VALUES ('delete', old.id, old.content, old.entity, old.category, old.tags);
        INSERT INTO facts_fts(rowid, content, entity, category, tags)
        VALUES (new.id, new.content, new.entity, new.category, new.tags);
    END;
    
    CREATE TABLE IF NOT EXISTS contradictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact_id_1 INTEGER NOT NULL,
        fact_id_2 INTEGER NOT NULL,
        resolved INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (fact_id_1) REFERENCES facts(id),
        FOREIGN KEY (fact_id_2) REFERENCES facts(id)
    );
    """)
    conn.commit()

def add_fact(conn, content, entity=None, category="general", trust=0.7, source="wiki-migration", tags=None):
    """添加一条事实"""
    now = datetime.now().isoformat()
    tags_json = json.dumps(tags or [], ensure_ascii=False)
    conn.execute(
        "INSERT INTO facts (content, entity, category, trust_score, source, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (content, entity, category, trust, source, tags_json, now, now)
    )

def main():
    print(f"数据库路径: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)
    
    now = datetime.now().isoformat()
    migrated = 0
    
    # ============================================
    # 1. 个人档案 (atemmie-profile.md)
    # ============================================
    profile_facts = [
        ("ATemmie 真名蔡璨徽，男，福建厦门人", "ATemmie", "profile", 0.9, ["personal", "name"]),
        ("ATemmie 2026届高考生，选科物化地", "ATemmie", "profile", 0.9, ["academic"]),
        ("ATemmie 高考成绩537分，位次50745（2026福建物理类）", "ATemmie", "profile", 0.9, ["academic"]),
        ("ATemmie 偏好自然轻松聊天风格，短句分段发，少用emoji", "ATemmie", "preference", 0.8, ["communication"]),
        ("ATemmie 不喜欢结构化/编号式回复", "ATemmie", "preference", 0.8, ["communication"]),
        ("ATemmie 喜欢被关心但有分寸的互动", "ATemmie", "preference", 0.8, ["communication"]),
    ]
    
    # ============================================
    # 2. 学业偏好 (academic-preferences.md)
    # ============================================
    academic_facts = [
        ("ATemmie 首推专业方向：地理信息科学、测绘工程、地质工程、新能源、网络工程、数学", "ATemmie", "academic", 0.9, ["major"]),
        ("ATemmie 避雷纯软件/AI方向", "ATemmie", "academic", 0.9, ["major"]),
        ("ATemmie 选校策略：行业特色院校王牌专业 > 综合性大学普通专业", "ATemmie", "academic", 0.9, ["strategy"]),
        ("ATemmie 偏好好就业、前景好、对学校要求低的方向", "ATemmie", "academic", 0.8, ["strategy"]),
    ]
    
    # ============================================
    # 3. 转专业计划 (major-transfer-plan.md)
    # ============================================
    transfer_facts = [
        ("ATemmie 被澳门科技大学环境科学与工程学士录取（创新工程学院FIE），2026秋入学", "ATemmie", "university", 0.95, ["must", "enrollment"]),
        ("ATemmie 转专业目标：人工智能理学学士/计算机科学软件工程方向/自动化与系统工程（均FIE院内）", "ATemmie", "university", 0.95, ["must", "transfer"]),
        ("澳科大新生首学年不允许转课程，须按录取专业注册入读", "MUST", "university", 0.95, ["must", "rules"]),
        ("澳科大转专业申请期：每年6月1日-7月8日，核准后下一学年生效", "MUST", "university", 0.95, ["must", "rules"]),
        ("澳科大转专业门槛：累计GPA≥2.8，部分专业要求3.0-3.2", "MUST", "university", 0.95, ["must", "rules"]),
        ("澳科大转专业：中英数必须全部通过不能挂科（硬性否决项）", "MUST", "university", 0.95, ["must", "rules"]),
        ("澳科大转专业需参加学院面试或评核试", "MUST", "university", 0.95, ["must", "rules"]),
        ("ATemmie 转专业行动：大一GPA目标3.2+，2027年6月窗口申请，机会只有一次", "ATemmie", "university", 0.9, ["must", "transfer", "plan"]),
        ("ATemmie 已发邮件admission@must.edu.mo说明转专业意向（2026-08-04）", "ATemmie", "university", 0.9, ["must", "transfer"]),
    ]
    
    # ============================================
    # 4. 游戏经历 (gaming-history.md + steam-games.md)
    # ============================================
    gaming_facts = [
        ("ATemmie CS2本命，1200h+，NiKo铁粉， Falcons粉丝", "ATemmie", "gaming", 0.95, ["cs2", "favorite"]),
        ("ATemmie Steam账号 gddty5，好友码76561199049468610", "ATemmie", "gaming", 0.9, ["steam"]),
        ("ATemmie 主力游戏：CS2(1200h+) > BFV(221h) > Terraria(160h) > 文明6(143h) > 赛博朋克2077(140h) > Forza Horizon5(109h)", "ATemmie", "gaming", 0.85, ["steam"]),
        ("ATemmie 其他喜爱游戏：Portal系列、Celeste、Stardew Valley、Disco Elysium", "ATemmie", "gaming", 0.8, ["preference"]),
        ("ATemmie Minecraft小学二年级入坑，165元买正版Java版，现在喜欢模组开发", "ATemmie", "gaming", 0.9, ["minecraft"]),
        ("ATemmie 杂食型玩家，涉猎广泛", "ATemmie", "gaming", 0.8, ["preference"]),
        ("ATemmie 游戏CP：里昂× Ashley（生化危机）", "ATemmie", "gaming", 0.7, ["preference"]),
        ("ATemmie 玩GWYF(3892270，存档103)，玩BR（内存助手看子弹/血量）", "ATemmie", "gaming", 0.85, ["gwyp", "buckshot"]),
        ("ATemmie 自建CS2服务器开黑（Desktop\\cs2-server），爱魔改：刀战/1血/3倍速/半重力等", "ATemmie", "gaming", 0.85, ["cs2", "server"]),
    ]
    
    # ============================================
    # 5. 硬件配置 (hardware-plan.md)
    # ============================================
    hardware_facts = [
        ("ATemmie 台式机：i5-13600KF + 华硕H610M + 金百达32G DDR4 + 七彩虹RTX4060", "ATemmie", "hardware", 0.9, ["desktop"]),
        ("ATemmie 显示器：华硕VG27AQL1A（27寸2K 170Hz）", "ATemmie", "hardware", 0.9, ["desktop"]),
        ("ATemmie 电源长城金牌600W需换，目标850W+ ATX3.1", "ATemmie", "hardware", 0.9, ["upgrade"]),
        ("ATemmie 计划升级RTX5080（16GB），为2K/4K 3A + AI本地训练", "ATemmie", "hardware", 0.85, ["upgrade"]),
        ("ATemmie 游戏本泰坦18Pro（R9-9955HX + RTX5070Ti 32G + 2TB）", "ATemmie", "hardware", 0.9, ["laptop"]),
        ("ATemmie 台式13600KF留厦门", "ATemmie", "hardware", 0.85, ["location"]),
        ("ATemmie 大学轻薄本候选：ThinkBook14+ 2026 / 联想小新Pro14 / 荣耀MagicBook Pro16", "ATemmie", "hardware", 0.8, ["laptop", "plan"]),
    ]
    
    # ============================================
    # 6. B站偏好 (bilibili-follows.md)
    # ============================================
    bili_facts = [
        ("ATemmie B站Lv6，UID567441725，1776个关注", "ATemmie", "bilibili", 0.9, ["account"]),
        ("ATemmie B站常看：CS-advent（前Tyloo职业选手）、小约翰可汗、极客湾、安迪视频", "ATemmie", "bilibili", 0.85, ["up主"]),
        ("ATemmie B站看：籽岷（童年最爱）、特厨隋坡、食贫道", "ATemmie", "bilibili", 0.8, ["up主"]),
        ("ATemmie 都市怪谈偏好：后室(Backrooms)、怪核、梦核、阈限空间", "ATemmie", "preference", 0.9, ["horror", "aesthetic"]),
    ]
    
    # ============================================
    # 7. 音乐偏好 (netease-music.md)
    # ============================================
    music_facts = [
        ("ATemmie 网易云ID 3395812344，红心歌单1152首", "ATemmie", "music", 0.9, ["netease"]),
        ("ATemmie 音乐口味换代：主力从PHONK转向港台经典情歌/华语细腻女声", "ATemmie", "music", 0.9, ["preference"]),
        ("ATemmie 现在常听：黄凯芹、陈奕迅、陈洁仪、孙盛希、王心凌、卫兰、徐佳莹", "ATemmie", "music", 0.85, ["preference"]),
        ("ATemmie 新兴兴趣：Emo/数学摇滚（Midwest Emo），Chinese Football《漂流人间》", "ATemmie", "music", 0.85, ["preference"]),
        ("ATemmie 旧本命PHONK，收藏大量但近期听得少（自述'小时候不懂事爱听的'）", "ATemmie", "music", 0.8, ["history"]),
        ("ATemmie 最喜欢的歌：Merry Christmas Mr. Lawrence（坂本龍一）、golden hour（JVKE）", "ATemmie", "music", 0.85, ["favorite"]),
        ("ATemmie 稳定辅线：华语R&B、日系、游戏OST、后室/怪核", "ATemmie", "music", 0.8, ["preference"]),
    ]
    
    # ============================================
    # 8. 澳门生活 (综合)
    # ============================================
    macau_facts = [
        ("ATemmie 澳门报到7月下旬签注，8.24-27到澳，9.1开学", "ATemmie", "macau", 0.9, ["timeline"]),
        ("ATemmie 澳门中行卡N座一层办，电信澳门一卡双号", "ATemmie", "macau", 0.85, ["logistics"]),
        ("ATemmie 档案留学服务中心，带英标插头，Pocket4拍视频", "ATemmie", "macau", 0.85, ["logistics"]),
    ]
    
    # ============================================
    # 9. 项目与开发
    # ============================================
    project_facts = [
        ("ATemmie MC Fabric模组开发中（taxes-mod，IDEA+JDK26）", "ATemmie", "project", 0.9, ["minecraft", "dev"]),
        ("ATemmie 梗博物馆项目：Pages部署，2015词条，方向CS/直播", "ATemmie", "project", 0.9, ["meme"]),
        ("ATemmie ATM工具箱：atemmie.github.io/atm-toolbox，cookie泄露后转私有", "ATemmie", "project", 0.9, ["toolbox"]),
        ("ATemmie BR助手：103机器开发，exe在I:\\BuckshotRoulette", "ATemmie", "project", 0.85, ["buckshot"]),
        ("ATemmie 未来方向：学计算机进AI公司/自建模型", "ATemmie", "career", 0.85, ["future"]),
    ]
    
    # ============================================
    # 10. 开发环境
    # ============================================
    env_facts = [
        ("ATemmie 开发环境：Win11，Python3.11/3.12，Playwright已装", "ATemmie", "devenv", 0.9, ["environment"]),
        ("ATemmie 走代理：ikuuu或Clash 127.0.0.1:7890（HTTPS_PROXY已永久setx）", "ATemmie", "devenv", 0.9, ["proxy"]),
        ("ATemmie GitHub: github.com/ATemmie，gh CLI已登录", "ATemmie", "devenv", 0.9, ["github"]),
        ("ATemmie 偏好：稳定>自动化，CLI优先，Python，JSON数据库", "ATemmie", "preference", 0.9, ["workflow"]),
        ("ATemmie 强隐私偏好：公开页面绝不能出现真实姓名/学校/地址等PII", "ATemmie", "preference", 0.95, ["privacy"]),
    ]
    
    # ============================================
    # 11. 103远程机
    # ============================================
    remote_facts = [
        ("103远程机：192.168.0.103/用户34934/id_rsa/RTX4060", "remote-103", "environment", 0.9, ["remote"]),
        ("103桌面已整理：hermes-work/{scripts,images,docs,backup}", "remote-103", "environment", 0.85, ["remote"]),
        ("QQ Bot必须本机运行，不能在远程机", "system", "rule", 0.95, ["qqbot"]),
    ]
    
    # ============================================
    # 12. Hermes配置
    # ============================================
    hermes_facts = [
        ("Hermes网页版：127.0.0.1:9120，局域网转发9121（手机访问）", "hermes", "config", 0.9, ["access"]),
        ("Hermes桌面端版本：0.19.0-cn.7", "hermes", "config", 0.9, ["version"]),
        ("Hermes语音：TTS用XiaoxiaoNeural（8-17定稿）", "hermes", "config", 0.9, ["tts"]),
        ("RVC变声已通（Neuro-sama，C:\\hermes\\rvc）", "hermes", "config", 0.85, ["voice"]),
        ("QQ主动通知格式：hermes send -t \"qqbot:OPENID\" \"消息\"", "hermes", "config", 0.9, ["qqbot"]),
        ("B站cookie在Desktop\\传输\\projects\\meme-museum\\data\\bili_cookies_api.json", "hermes", "config", 0.85, ["bilibili"]),
    ]
    
    # 合并所有事实
    all_facts = (
        profile_facts + academic_facts + transfer_facts + 
        gaming_facts + hardware_facts + bili_facts + 
        music_facts + macau_facts + project_facts + 
        env_facts + remote_facts + hermes_facts
    )
    
    # 写入数据库
    for content, entity, category, trust, tags in all_facts:
        add_fact(conn, content, entity, category, trust, "wiki-migration-20260820", tags)
        migrated += 1
    
    conn.commit()
    
    # 验证
    count = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    print(f"\n✅ 迁移完成！共写入 {count} 条事实")
    
    # 按分类统计
    print("\n📊 分类统计:")
    for row in conn.execute("SELECT category, COUNT(*) as cnt FROM facts GROUP BY category ORDER BY cnt DESC"):
        print(f"  {row[0]}: {row[1]} 条")
    
    # 测试FTS搜索
    print("\n🔍 测试搜索 'CS2':")
    for row in conn.execute("""
        SELECT f.content, f.entity, f.trust_score 
        FROM facts f 
        JOIN facts_fts fts ON f.id = fts.rowid 
        WHERE facts_fts MATCH 'CS2' 
        ORDER BY rank LIMIT 3
    """):
        print(f"  [{row[1]}] {row[0]} (信任度:{row[2]})")
    
    print("\n🔍 测试搜索 '澳门':")
    for row in conn.execute("""
        SELECT f.content, f.entity, f.trust_score 
        FROM facts f 
        JOIN facts_fts fts ON f.id = fts.rowid 
        WHERE facts_fts MATCH '澳门' 
        ORDER BY rank LIMIT 3
    """):
        print(f"  [{row[1]}] {row[0]} (信任度:{row[2]})")
    
    conn.close()
    print(f"\n📁 数据库: {DB_PATH}")
    print(f"📦 大小: {os.path.getsize(DB_PATH) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
