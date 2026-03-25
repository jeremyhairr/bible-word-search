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
    SELECT text, source FROM commentary
    WHERE LOWER(book)=?
    AND chapter=?
    AND start_verse <= ?
    AND end_verse >= ?
    """,
        (book, chapter, verse, verse),
    )

    results = cursor.fetchall()
    conn.close()

    return [{"text": row[0], "source": row[1]} for row in results]
