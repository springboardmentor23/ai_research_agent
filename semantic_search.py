import time
import requests                         # pyright: ignore[reportMissingModuleSource]
import json

def fetch_papers(topic, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,openAccessPdf"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["data"]

    elif response.status_code == 429:
        print("Rate limit hit. Waiting...")
        time.sleep(5)
        return fetch_papers(topic, limit)

    else:
        response.raise_for_status()
