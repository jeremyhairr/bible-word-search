import json
import sqlite3

with open("kjv.json", "r", encoding="utf-8") as f:
    data = json.load(f)

conn = sqlite3.connect("bible.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS verses (
    book TEXT,
    chapter INTEGER,
    verse INTEGER,
    text TEXT
)
""")

cursor.execute("DELETE FROM verses")

count = 0

for book in data["books"]:
    book_name = book["name"]

    for chapter in book["chapters"]:
        chapter_num = chapter["chapter"]

        for verse in chapter["verses"]:
            verse_num = verse["verse"]
            text = verse["text"]

            cursor.execute(
                """
                INSERT INTO verses (book, chapter, verse, text)
                VALUES (?, ?, ?, ?)
            """,
                (book_name, chapter_num, verse_num, text),
            )

            count += 1

conn.commit()
conn.close()

print(f"Loaded {count} verses!")
