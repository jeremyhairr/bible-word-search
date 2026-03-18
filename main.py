from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()

# Templates (HTML)
templates = Jinja2Templates(directory="templates")

# API Key
ESV_API_KEY = os.getenv("ESV_API_KEY")


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
def read(reference: str):
    return JSONResponse(fetch_passage(reference))
