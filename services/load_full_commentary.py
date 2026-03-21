import json
import sqlite3
from pathlib import Path

DB_PATH = "database/bible.db"
JSON_PATH = "services/data/matthew_henry.json"


def insert_commentary(cursor, book, chapter, start, end, text):
    cursor.execute(
        """
        INSERT INTO commentary (book, chapter, verse_start, verse_end, text)
        VALUES (?, ?, ?, ?, ?)
        """,
        (book, chapter, start, end, text),
    )


def load_full():
    print("🔥 Loading FULL Matthew Henry Commentary...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0

    for entry in data:
        try:
            insert_commentary(
                cursor,
                entry["book"],
                entry["chapter"],
                entry["start_verse"],
                entry["end_verse"],
                entry["text"],
            )
            count += 1

            # 🔥 DEBUG every 100 rows
            if count % 100 == 0:
                print(f"Inserted {count} rows...")

        except Exception as e:
            print("❌ Error inserting row:", e)

    conn.commit()
    conn.close()

    print(f"✅ DONE! Inserted {count} rows.")


if __name__ == "__main__":
    load_full()
