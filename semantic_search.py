import time
import requests


def fetch_papers(topic, limit=3, retries=3, wait_seconds=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,paperId"
    }

    for attempt in range(retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()["data"]

        elif response.status_code == 429:
            print(f"Rate limit hit. Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)

        else:
            response.raise_for_status()

    print("Could not fetch papers due to repeated rate limiting.")
    return []


def fetch_references(paper_id, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"

    params = {
        "limit": limit,
        "fields": "title,authors,year,url"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Failed to fetch references")
        return []

    data = response.json().get("data")

    if not data:
        print("No references found for this paper.")
        return []

    references = []
    for r in data:
        cited = r.get("citedPaper")
        if cited:
            references.append(cited)

    return references
