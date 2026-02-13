import requests
import time
import os

def fetch_papers(topic, limit=4, retries=3, wait_seconds=5):
    """
    Fetch papers from Semantic Scholar API with open-access PDFs.
    Returns list of papers with required fields.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers={
        "x-api-key" : "bVn5D8MT5sSfcjcAnKbZ7k2drrMw3sa8si1GyKpe"
    }

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,paperId,openAccessPdf"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 200:
                papers = response.json().get("data", [])
                # Filter papers with available PDFs
                papers_with_pdf = [p for p in papers if p.get("openAccessPdf", {}).get("url")]
                return papers_with_pdf

            elif response.status_code == 429:
                wait_time = wait_seconds * (attempt + 1)
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)

            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching papers (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                time.sleep(wait_seconds)

    print("Could not fetch papers due to repeated rate limiting or errors.")
    return []