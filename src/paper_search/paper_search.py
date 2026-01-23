import time
from urllib import response
import requests


#fetch papers
def fetch_from_semantic_scholar(topic, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "paperId,title,authors,year,abstract,url,openAccessPdf"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json().get("data", [])

        if response.status_code == 429:
            print("Semantic Scholar rate limited.")
            return None

    except requests.exceptions.RequestException:
        return None

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


def fetch_from_semantic_scholar(topic, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "paperId,title,authors,year,abstract,url,openAccessPdf"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json().get("data", [])

        if response.status_code == 429:
            print("Semantic Scholar rate limited.")
            return None

    except requests.exceptions.RequestException:
        return None

    return []

 


def show_references(references):
    for i, ref in enumerate(references, start=1):
        authors = ", ".join(a["name"] for a in ref.get("authors", []))

        print("\nReference", i)
        print("Title:", ref.get("title"))
        print("Authors:", authors)
        print("Year:", ref.get("year"))
        print("Link:", ref.get("url"))
        print("-" * 50)
