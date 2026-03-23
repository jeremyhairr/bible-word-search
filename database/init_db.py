import sqlite3

conn = sqlite3.connect("database/bible.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS commentary (
    id INTEGER PRIMARY KEY,
    book TEXT,
    chapter INTEGER,
    verse_start INTEGER,
    verse_end INTEGER,
    text TEXT
)
"""
)

conn.commit()
conn.close()

print("Database created successfully!")
