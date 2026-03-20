from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests
import urllib.parse
import os
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

BOOK_MAP = {
    "genesis": "GEN",
    "exodus": "EXO",
    "leviticus": "LEV",
    "numbers": "NUM",
    "deuteronomy": "DEU",
    "joshua": "JOS",
    "judges": "JDG",
    "ruth": "RUT",
    "1 samuel": "1SA",
    "2 samuel": "2SA",
    "1 kings": "1KI",
    "2 kings": "2KI",
    "1 chronicles": "1CH",
    "2 chronicles": "2CH",
    "ezra": "EZR",
    "nehemiah": "NEH",
    "esther": "EST",
    "job": "JOB",
    "psalm": "PSA",
    "psalms": "PSA",
    "proverbs": "PRO",
    "ecclesiastes": "ECC",
    "song of solomon": "SNG",
    "isaiah": "ISA",
    "jeremiah": "JER",
    "lamentations": "LAM",
    "ezekiel": "EZK",
    "daniel": "DAN",
    "hosea": "HOS",
    "joel": "JOL",
    "amos": "AMO",
    "obadiah": "OBA",
    "jonah": "JON",
    "micah": "MIC",
    "nahum": "NAM",
    "habakkuk": "HAB",
    "zephaniah": "ZEP",
    "haggai": "HAG",
    "zechariah": "ZEC",
    "malachi": "MAL",
    "matthew": "MAT",
    "mark": "MRK",
    "luke": "LUK",
    "john": "JHN",
    "acts": "ACT",
    "romans": "ROM",
    "1 corinthians": "1CO",
    "2 corinthians": "2CO",
    "galatians": "GAL",
    "ephesians": "EPH",
    "philippians": "PHP",
    "colossians": "COL",
    "1 thessalonians": "1TH",
    "2 thessalonians": "2TH",
    "1 timothy": "1TI",
    "2 timothy": "2TI",
    "titus": "TIT",
    "philemon": "PHM",
    "hebrews": "HEB",
    "james": "JAS",
    "1 peter": "1PE",
    "2 peter": "2PE",
    "1 john": "1JN",
    "2 john": "2JN",
    "3 john": "3JN",
    "jude": "JUD",
    "revelation": "REV",
}


def convert_reference(ref):
    ref = ref.lower().strip()

    # Handle cases like "1 Samuel 17"
    for book_name in sorted(BOOK_MAP.keys(), key=len, reverse=True):
        if ref.startswith(book_name):
            code = BOOK_MAP[book_name]
            rest = ref[len(book_name) :].strip()

            if ":" in rest:
                chapter, verse = rest.split(":")
                return f"{code}.{chapter}.{verse}"
            else:
                return f"{code}.{rest}"

    return ref  # fallback if not matched


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
BIBLES = {"csb": "a556c5305ee15c3f-01"}
app.mount("/static", StaticFiles(directory="static"), name="static")
# Templates (HTML)
templates = Jinja2Templates(directory="templates")

# API Key
ESV_API_KEY = os.getenv("ESV_API_KEY")
API_BIBLE_KEY = os.getenv("API_BIBLE_KEY")


# -----------------------------
# 🔍 ESV SEARCH (PAGINATED)
# -----------------------------
def fetch_esv_page(query: str, page: int):
    url = "https://api.esv.org/v3/passage/search/"

    params = {"q": query, "page-size": 50, "page": page}

    headers = {"Authorization": f"Token {ESV_API_KEY}"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {"error": "Could not fetch ESV"}

    data = response.json()

    results = []

    for r in data.get("results", []):
        results.append({"reference": r["reference"], "content": r["content"]})

    return {
        "query": query,
        "page": data.get("page", page),
        "total_pages": data.get("total_pages", 1),
        "total_results": data.get("total_results", 0),
        "results": results,
    }


# -----------------------------
# 📖 ESV PASSAGE READING
# -----------------------------
def fetch_passage(reference: str):
    url = "https://api.esv.org/v3/passage/text/"

    params = {"q": reference, "include-short-copyright": False}

    headers = {"Authorization": f"Token {ESV_API_KEY}"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {"error": "Could not fetch passage"}

    data = response.json()

    return {"reference": reference, "text": "".join(data.get("passages", []))}


import urllib.parse


def fetch_api_bible(reference, bible_id):

    print("ORIGINAL:", reference)  # 👈 raw input from user

    reference = convert_reference(reference)

    print("CONVERTED:", reference)  # 👈 after conversion

    encoded_ref = urllib.parse.quote(reference)

    url = f"https://rest.api.bible/v1/bibles/{bible_id}/passages/{encoded_ref}"

    headers = {"api-key": API_BIBLE_KEY}

    print("USING KEY:", API_BIBLE_KEY)

    response = requests.get(url, headers=headers)
    data = response.json()
    print("DATA JSON:", data)
    return {
        "reference": data["data"].get("reference", ""),
        "text": data["data"].get("content", ""),
    }


# -----------------------------
# 🚀 ROUTES
# -----------------------------


# Homepage (HTML UI)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 🔍 Search route
@app.get("/search")
def search(query: str, page: int = 1):
    return JSONResponse(fetch_esv_page(query, page))


# 📖 Read passage route
@app.get("/read")
def read(reference: str, version: str = "esv"):

    if version == "esv":
        return fetch_passage(reference)

    bible_id = BIBLES.get(version)

    if not bible_id:
        return {"error": "Invalid version"}

    return fetch_api_bible(reference, bible_id)


@app.get("/ask")
def ask(question: str):

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Bible assistant. Answer clearly and include Scripture references when possible.",
            },
            {"role": "user", "content": question},
        ],
    )

    answer = response.choices[0].message.content

    return {"answer": answer}
