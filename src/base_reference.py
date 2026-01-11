import os
import json
import requests
import time

def fetch_papers(topic, limit=3, retries=3, wait_seconds=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url"
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


def show_papers(papers):
    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a["name"] for a in paper.get("authors", []))

        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Authors:", authors)
        print("Year:", paper.get("year"))
        print("\nAbstract:")
        print(paper.get("abstract"))
        print("\nPaper Link:", paper.get("url"))
        print("-" * 60)
