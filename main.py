from fastapi import FastAPI
import sqlite3

app = FastAPI()


def search_bible(query: str):
    conn = sqlite3.connect("bible.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT book, chapter, verse, text
        FROM verses
        WHERE text LIKE ?
        LIMIT 20
    """,
        ("%" + query + "%",),
    )

    results = cursor.fetchall()
    conn.close()

    return [
        {"book": r[0], "chapter": r[1], "verse": r[2], "text": r[3]} for r in results
    ]


@app.get("/")
def root():
    return {"message": "Bible App Running"}


@app.get("/search")
def search(query: str):
    return search_bible(query)
