

import requests
import time
from config.settings import BASE_URL, SEMANTIC_SCHOLAR_API_KEY

def search_papers(topic, limit=3, retries=3, wait_seconds=5):
    url = f"{BASE_URL}/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,openAccessPdf,url"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Add API key ONLY if it exists
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    for attempt in range(retries):
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response.json()["data"]

        elif response.status_code == 429:
            print(f"⚠️ Rate limit hit. Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)

        else:
            response.raise_for_status()

    print("❌ Failed due to repeated rate limiting.")
    return []
