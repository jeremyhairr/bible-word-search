import sqlite3

conn = sqlite3.connect("bible.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    translation TEXT NOT NULL,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database ready.")
