# -*- coding: utf-8 -*-
"""查 executions.db 内容"""
import sqlite3

conn = sqlite3.connect(r'C:\Users\Administrator\AppData\Roaming\cn.org.hermesagent.desktop\runtime\hermes-home\cron\executions.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print('tables:', tables)
for t in tables:
    cols = [c[1] for c in cur.execute(f'PRAGMA table_info({t})')]
    print(f'\n  {t}: {cols}')
    try:
        rows = cur.execute(f'SELECT * FROM {t} ORDER BY rowid DESC LIMIT 8').fetchall()
        for r in rows:
            print('   ', str(r)[:400])
    except Exception as e:
        print('    err', e)
conn.close()