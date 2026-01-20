import time
from urllib import response
import requests


# fetch papers
def fetch_papers(topic, limit=5, retries=3, wait_seconds=3):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "paperId,title,authors,year,abstract,url"
    }

    for attempt in range(retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json().get("data", [])

        elif response.status_code == 429:
            print("Rate limit reached. Waiting...")
            time.sleep(wait_seconds)

        else:
            response.raise_for_status()

    return []


def show_papers(topic, papers):
    print(f"\nTopic: {topic}")

    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a["name"] for a in paper.get("authors", []))

        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Authors:", authors)
        print("Year:", paper.get("year"))
        print("Abstract:", paper.get("abstract"))
        print("Link:", paper.get("url"))
        print("Paper ID:", paper.get("paperId"))
        print("-" * 40)


def fetch_references(paper_id, limit=4):
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

# SAFETY CHECK (IMPORTANT)
    if not data:
        return []

    references = []

    for r in data:
        cited = r.get("citedPaper")
    if cited:
        references.append(cited)

    return references

 


def show_references(references):
    for i, ref in enumerate(references, start=1):
        authors = ", ".join(a["name"] for a in ref.get("authors", []))

        print("\nReference", i)
        print("Title:", ref.get("title"))
        print("Authors:", authors)
        print("Year:", ref.get("year"))
        print("Link:", ref.get("url"))
        print("-" * 50)
