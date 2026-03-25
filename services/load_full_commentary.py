import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "bible.db"
JSON_PATH = BASE_DIR / "services" / "data" / "matthew_henry.json"
PROVERBS_JSON_PATH = BASE_DIR / "services" / "data" / "proverbs_henry.json"
FIRST_COR_JSON_PATH = "services/data/first_corinthians_henry.json"
CALVIN_JSON_PATH = "services/data/calvin.json"


def insert_commentary(cursor, book, chapter, start_verse, end_verse, text, source):
    cursor.execute(
        """
        INSERT INTO commentary (book, chapter, start_verse, end_verse, text, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (book, chapter, start_verse, end_verse, text, source),
    )


def load_file(cursor, path, source_name):
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
                source_name,  # ✅ THIS is where source is passed
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

    total += load_file(cursor, JSON_PATH, "Henry")
    total += load_file(cursor, CALVIN_JSON_PATH, "Calvin")
    total += load_file(cursor, PROVERBS_JSON_PATH, "Henry")
    total += load_file(cursor, FIRST_COR_JSON_PATH, "Henry")
    conn.commit()
    conn.close()

    print(f"🎉 DONE! Total rows inserted: {total}")


if __name__ == "__main__":
    load_full()
