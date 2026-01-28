import requests
import time

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_papers(query, limit=10, retries=3, wait=5):
    """Search papers from Semantic Scholar with retry on 429."""
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,openAccessPdf,paperId"
    }
    attempt = 0
    while attempt <= retries:
        response = requests.get(SEMANTIC_SCHOLAR_API, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        elif response.status_code == 429:
            attempt += 1
            print(f"Rate limit reached. Waiting {wait} seconds... (Attempt {attempt}/{retries})")
            time.sleep(wait)
        else:
            raise Exception(f"Semantic Scholar API error: {response.status_code}")
    raise Exception(f"Failed after {retries} retries due to rate limiting.")
