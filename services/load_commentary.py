import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "bible.db")


def normalize_book(book):
    return book.lower().strip()


def insert_commentary(book, chapter, verse_start, verse_end, text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO commentary (book, chapter, verse_start, verse_end, text)
        VALUES (?, ?, ?, ?, ?)
    """,
        (normalize_book(book), chapter, verse_start, verse_end, text),
    )

    conn.commit()
    conn.close()


def load_sample_data():
    print("Loading sample Matthew Henry commentary...")

    insert_commentary(
        "John",
        3,
        16,
        16,
        "This verse is the golden text of the gospel. It shows God's love in giving His Son...",
    )

    print("✅ Sample commentary loaded!")


if __name__ == "__main__":
    load_sample_data()
