import json
import sqlite3

DB_PATH = "database/bible.db"
JSON_PATH = "services/data/institutes_calvin.json"


def load_institutes():
    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0

    for entry in data:
        cursor.execute(
            """
            INSERT INTO theology (source, work, book, chapter, section, text)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entry.get("source"),
                entry.get("work"),
                entry.get("book"),
                entry.get("chapter"),
                entry.get("section"),
                entry.get("text"),
            ),
        )
        count += 1

    conn.commit()
    conn.close()

    print(f"✅ Loaded {count} Institutes entries into theology table.")


if __name__ == "__main__":
    load_institutes()
