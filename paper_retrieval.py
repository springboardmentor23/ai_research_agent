import time
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_papers(topic, limit=3, retries=3, wait_seconds=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,openAccessPdf"

    }

    for _ in range(retries):
        response = requests.get(url, params=params, headers=HEADERS)

        if response.status_code == 200:
            return response.json().get("data", [])

        elif response.status_code == 429:
            print("Rate limit hit. Waiting...")
            time.sleep(wait_seconds)

        else:
            print("Error:", response.status_code)
            return []

    return []


def show_papers(papers):
    if not papers:
        print("No papers found.")
        return

    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a["name"] for a in paper.get("authors", []))
        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Authors:", authors)
        print("Year:", paper.get("year"))
        print("Abstract:", paper.get("abstract"))
        print("Link:", paper.get("url"))
        print("-" * 60)