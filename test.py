import sqlite3
DB_PATH="data/nifty100.db"
conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

for table in cursor.fetchall():
    print(table[0])

conn.close()