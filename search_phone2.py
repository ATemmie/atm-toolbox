# -*- coding: utf-8 -*-
"""挖一卡双号/电话卡具体细节"""
import sqlite3

db = r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\state.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

rows = cur.execute("SELECT DISTINCT session_id FROM messages WHERE content LIKE '%一卡双号%' AND active=1 LIMIT 5").fetchall()
for r in rows:
    msgs = cur.execute("SELECT role, content FROM messages WHERE session_id=? AND active=1 ORDER BY id", (r[0],)).fetchall()
    for m in msgs:
        c = (m[1] or '')
        if not c.startswith('{') and ('一卡双号' in c or '电话卡' in c or '电信' in c):
            print(f"=== ({m[0]}) ===")
            print(c[:800])
            print()

# 澳门通相关
print("\n===== 澳门通 =====")
rows = cur.execute("SELECT DISTINCT session_id FROM messages WHERE content LIKE '%澳门通%' AND active=1 LIMIT 3").fetchall()
for r in rows:
    msgs = cur.execute("SELECT role, content FROM messages WHERE session_id=? AND content LIKE '%澳门通%' AND active=1 ORDER BY id LIMIT 4", (r[0],)).fetchall()
    for m in msgs:
        c = (m[1] or '')
        if not c.startswith('{'):
            print(f"({m[0]}) {c[:500]}")
            print()
conn.close()