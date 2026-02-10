import os
import time
import requests


SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")


def fetch_papers(topic, limit=3):
    """
    Fetch research papers from Semantic Scholar.
    Returns a list of paper metadata dictionaries.
    """

    if not API_KEY:
        raise ValueError("Semantic Scholar API key not found in environment variables.")

    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,openAccessPdf"
    }

    print("Fetching papers...")

    response = requests.get(
        SEMANTIC_SCHOLAR_API_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    # Respect API rate limit
    time.sleep(1.1)

    response.raise_for_status()
    data = response.json()

    papers = data.get("data", [])
    return papers
