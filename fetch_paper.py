import requests
import time

def fetch_papers(topic, limit=4, retries=3, wait_seconds=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,openAccessPdf"
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
