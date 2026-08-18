# -*- coding: utf-8 -*-
"""找床帘会话的最终推荐结论（会话标题=床帘测评视频推荐）"""
import sqlite3

db = r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\state.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

# 找会话
rows = cur.execute("SELECT id, title, started_at FROM sessions WHERE title LIKE '%床帘%'").fetchall()
print(f"床帘会话数: {len(rows)}")
for r in rows:
    print(f"  session {r[0]} | {r[1]} | {r[2]}")

if not rows:
    conn.close()
    sys.exit(0)

# 查这个会话的所有消息
sid = rows[0][0]
msgs = cur.execute("SELECT id, role, content, timestamp FROM messages WHERE session_id=? AND active=1 ORDER BY id", (sid,)).fetchall()
print(f"\n消息总数: {len(msgs)}")

# 找 assistant 的最后回复（最终结论在末尾）
# 打印最后 12 条 assistant 消息
assistant_msgs = [m for m in msgs if m[1] == 'assistant']
print(f"\nassistant 消息数: {len(assistant_msgs)}")
for m in assistant_msgs[-12:]:
    c = m[2] or ''
    if c and not c.startswith('{'):
        print(f"\n--- [{m[3]}] ---")
        print(c[:1500])
conn.close()