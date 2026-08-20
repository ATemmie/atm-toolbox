import sqlite3, os
db = os.path.expanduser('~/AppData/Roaming/cn.org.hermesagent.desktop/runtime/hermes-home/memory_store.db')
conn = sqlite3.connect(db)
# 查看澳门相关内容是否存在
rows = conn.execute("SELECT id, content FROM facts WHERE content LIKE '%澳门%'").fetchall()
print(f'澳门相关事实: {len(rows)} 条')
for r in rows:
    print(f'  [{r[0]}] {r[1][:80]}')
# 测试CS2
print()
rows2 = conn.execute("SELECT id, content FROM facts WHERE content LIKE '%CS2%'").fetchall()
print(f'CS2相关事实(LIKE): {len(rows2)} 条')
# 测试FTS搜索CS2
print()
rows3 = conn.execute("""
    SELECT f.id, f.content FROM facts f 
    JOIN facts_fts fts ON f.id = fts.rowid 
    WHERE facts_fts MATCH 'CS2' LIMIT 3
""").fetchall()
print(f'CS2 FTS搜索: {len(rows3)} 条')
# 测试FTS搜索中文
print()
try:
    rows4 = conn.execute("""
        SELECT f.id, f.content FROM facts f 
        JOIN facts_fts fts ON f.id = fts.rowid 
        WHERE facts_fts MATCH '澳门' LIMIT 3
    """).fetchall()
    print(f'澳门 FTS搜索: {len(rows4)} 条')
except Exception as e:
    print(f'澳门 FTS搜索出错: {e}')
conn.close()
