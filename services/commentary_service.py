from database.db import get_connection


# ✅ ADD IT HERE
def normalize_book(book):
    book = book.lower().strip()

    mapping = {
        "jhn": "john",
        "gen": "genesis",
        "mt": "matthew",
    }

    return mapping.get(book, book)


# 👇 your existing function
def get_commentary(book, chapter, verse):
    book = normalize_book(book)  # ← already correct

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT text FROM commentary
        WHERE LOWER(book) = ?
        AND chapter = ?
        AND verse_start <= ?
        AND verse_end >= ?
        """,
        (book.lower(), chapter, verse, verse),
    )

    results = cursor.fetchall()
    conn.close()

    return [r["text"] for r in results]
