import requests
from config import SEMANTIC_SCHOLAR_API_KEY

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_from_semantic(topic, max_results=5):
    if not SEMANTIC_SCHOLAR_API_KEY:
        raise ValueError("Semantic Scholar API key not configured")

    print("Using Semantic Scholar API...")

    headers = {"x-api-key": SEMANTIC_SCHOLAR_API_KEY}

    params = {
        "query": topic,
        "limit": max_results,
        "fields": "paperId,title,authors,year,openAccessPdf"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    papers = []

    for item in data:
        pdf_url = item.get("openAccessPdf", {}).get("url")
        if not pdf_url:
            continue

        paper = {
            "paperId": item["paperId"],
            "title": item["title"],
            "authors": [a["name"] for a in item.get("authors", [])],
            "year": item.get("year"),
            "pdf_url": pdf_url,
            "source": "SemanticScholar"
        }
        papers.append(paper)

    return papers
