from fastapi import FastAPI
import sqlite3
import requests

app = FastAPI()


# -----------------------------
# 🔎 KJV SEARCH (LOCAL DATABASE)
# -----------------------------
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


# -----------------------------
# 🌐 ESV (API FETCH)
# -----------------------------
def fetch_esv(query: str):
    url = f"https://bible-api.com/{query}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Could not fetch ESV"}

    return response.json()


# -----------------------------
# 🚀 ROUTES
# -----------------------------


# Root (test)
@app.get("/")
def root():
    return {"message": "Bible App Running"}


# KJV Search
@app.get("/search")
def search(query: str):
    return search_bible(query)


# ESV Search (API)
@app.get("/search_esv")
def search_esv(query: str):
    return fetch_esv(query)
