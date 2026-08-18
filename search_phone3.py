# -*- coding: utf-8 -*-
"""找 Guidebook 电话卡完整内容（电信/一卡双号/其他运营商）"""
import sqlite3

db = r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\state.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

rows = cur.execute("SELECT DISTINCT session_id FROM messages WHERE content LIKE '%一卡双号%' AND active=1 LIMIT 5").fetchall()
for r in rows:
    msgs = cur.execute("SELECT role, content FROM messages WHERE session_id=? AND active=1 ORDER BY id", (r[0],)).fetchall()
    for m in msgs:
        c = (m[1] or '')
        if not c.startswith('{'):
            # 找电话卡相关段落
            import re
            if '电话卡' in c or '电信' in c or '一卡双号' in c or '运营商' in c or 'CTM' in c:
                # 打印整条消息含电话卡关键词附近的文本
                idx = c.find('电话卡')
                if idx == -1:
                    idx = c.find('电信')
                start = max(0, idx - 100)
                print(f"=== ({m[0]}) len={len(c)} ===")
                print(c[start:start + 2000])
                print()
conn.close()