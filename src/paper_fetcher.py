import os
import time
import requests

API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_papers(topic, limit=3):
    headers = {
        "x-api-key": os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    }

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url"
    }

    response = requests.get(API_URL, headers=headers, params=params, timeout=20)

    if response.status_code == 200:
        return response.json().get("data", [])

    print("Failed to fetch papers.")
    return []
