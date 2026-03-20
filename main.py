from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests
import urllib.parse
import os
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

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
    encoded_ref = urllib.parse.quote(reference)

    url = f"https://rest.api.bible/v1/bibles/{bible_id}/passages/{encoded_ref}"

    headers = {"api-key": API_BIBLE_KEY}
    print("USING KEY:", API_BIBLE_KEY)

    response = requests.get(url, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        return {"error": "API Bible request failed"}

    data = response.json()

    return {"reference": data["data"]["reference"], "text": data["data"]["content"]}


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
