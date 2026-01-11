import requests
import time

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_papers(query, limit=4, retries=3, wait_seconds=5): 
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,authors,year,openAccessPdf,url"
    }

    for attempt in range(1, retries + 1):
        response = requests.get(
            SEMANTIC_SCHOLAR_URL,
            params=params,
            timeout=10
        )

        # SUCCESS
        if response.status_code == 200:
            payload = response.json()
            if "data" not in payload:
                raise RuntimeError("Invalid API response structure")
            return payload["data"]

        # RATE LIMIT
        if response.status_code == 429:
            print(
                f"Rate limited by Semantic Scholar "
                f"(attempt {attempt}/{retries}). "
                f"Waiting {wait_seconds}s..."
            )
            time.sleep(wait_seconds)
            continue

        # OTHER ERRORS → FAIL FAST
        response.raise_for_status()

    raise RuntimeError("Failed to fetch papers due to repeated rate limiting")
