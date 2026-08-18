# -*- coding: utf-8 -*-
"""查最新执行记录"""
import sqlite3

conn = sqlite3.connect(r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\cron\executions.db')
cur = conn.cursor()
rows = cur.execute("SELECT job_id, status, started_at, finished_at, error FROM executions ORDER BY rowid DESC LIMIT 6").fetchall()
for r in rows:
    print(f"job={r[0]} status={r[1]} start={r[2]} end={r[3]}")
    if r[4]:
        print(f"   err: {r[4][:200]}")
conn.close()