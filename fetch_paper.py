import os
import requests
import time

def fetch_papers(topic, limit=4, retries=5, wait_seconds=6):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,openAccessPdf"
    }

    # Only use key if set and not a placeholder (invalid keys cause 403)
    api_key = (os.environ.get("SEMANTIC_SCHOLAR_API_KEY") or "").strip()
    placeholder = api_key.lower() in ("", "your_key_here", "your_api_key_here")
    if placeholder:
        if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
            print("SEMANTIC_SCHOLAR_API_KEY looks like a placeholder. Using unauthenticated requests (rate limits apply).")
        api_key = None
    use_headers = {"x-api-key": api_key} if api_key else None

    for attempt in range(retries):
        response = requests.get(url, params=params, headers=use_headers)

        if response.status_code == 200:
            return response.json().get("data", [])

        if response.status_code == 429:
            print(f"Rate limit hit. Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
            continue

        if response.status_code == 403:
            if use_headers:
                print("API key rejected (403). Retrying without key - you may hit rate limits.")
                use_headers = None
                continue
            response.raise_for_status()

        response.raise_for_status()

    print("Could not fetch papers due to repeated rate limiting.")
    return []
