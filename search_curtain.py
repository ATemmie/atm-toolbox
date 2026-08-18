# -*- coding: utf-8 -*-
"""搜 state.db 聊天记录里关于床帘的内容"""
import sqlite3, sys

db = r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\state.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

# 先看表结构
print('=== 表 ===')
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print(tables)

# 找含 "床帘" 的记录
for t in tables:
    try:
        cols = [c[1] for c in cur.execute(f'PRAGMA table_info({t})')]
        text_cols = [c for c in cols if any(k in c.lower() for k in ['content','text','message','body','prompt','data','transcript','title','name'])]
        if not text_cols:
            continue
        for tc in text_cols:
            try:
                rows = cur.execute(f"SELECT * FROM {t} WHERE {tc} LIKE '%床帘%' LIMIT 30").fetchall()
                if rows:
                    print(f"\n=== 表 {t} 列 {tc}: {len(rows)} 条 ===")
                    for r in rows[:10]:
                        for c, v in zip(cols, r):
                            if v and isinstance(v, str) and '床帘' in v:
                                print(f"  [{c}] {v[:600]}")
                                print()
            except Exception as e:
                pass
    except Exception:
        pass
conn.close()