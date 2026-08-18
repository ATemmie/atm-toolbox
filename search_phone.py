# -*- coding: utf-8 -*-
"""搜聊天记录里关于电话卡/电信澳门的内容"""
import sqlite3

db = r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\state.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

kws = ['电话卡', '一卡双号', '电信澳门', '澳门通', '中国电信']
for kw in kws:
    rows = cur.execute("SELECT DISTINCT session_id FROM messages WHERE content LIKE ? AND active=1 LIMIT 5", (f'%{kw}%',)).fetchall()
    print(f"[{kw}] 命中 {len(rows)} 个会话")
    for r in rows[:3]:
        msgs = cur.execute("SELECT role, content FROM messages WHERE session_id=? AND content LIKE ? AND active=1 ORDER BY id LIMIT 3", (r[0], f'%{kw}%')).fetchall()
        for m in msgs:
            c = (m[1] or '')
            if not c.startswith('{'):
                print(f"  ({m[0]}) {c[:400]}")
                print()
conn.close()