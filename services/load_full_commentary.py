import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "bible.db"
JSON_PATH = BASE_DIR / "services" / "data" / "matthew_henry.json"
PROVERBS_JSON_PATH = BASE_DIR / "services" / "data" / "proverbs_henry.json"


def insert_commentary(cursor, book, chapter, start, end, text):
    cursor.execute(
        """
        INSERT INTO commentary (book, chapter, verse_start, verse_end, text)
        VALUES (?, ?, ?, ?, ?)
        """,
        (book, chapter, start, end, text),
    )


def load_file(cursor, path):
    print(f"📘 Loading: {path}")

    with open(path, "r", encoding="utf-8") as f:
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

        except Exception as e:
            print("❌ Error inserting row:", e)

    print(f"✅ Inserted {count} rows from {path}")
    return count


def load_full():
    print("🔥 Loading FULL Commentary...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    total = 0

    # ✅ Load Matthew (existing)
    total += load_file(cursor, JSON_PATH)

    # ✅ Load Proverbs (new)
    total += load_file(cursor, PROVERBS_JSON_PATH)

    conn.commit()
    conn.close()

    print(f"🎉 DONE! Total rows inserted: {total}")


if __name__ == "__main__":
    load_full()
