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
        "fields": "paperId,title,authors,year,abstract,url,isOpenAccess,openAccessPdf"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                data = response.json().get("data", [])
                print(f"Successfully fetched papers for '{topic}'")
                return data

            elif response.status_code == 429:
                print(f"Rate limit hit. Retry {attempt + 1}/{retries}. Waiting {wait_seconds}s...")
                time.sleep(wait_seconds)

            else:
                print(f"Error: HTTP {response.status_code}")
                return []
        
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            if attempt < retries - 1:
                time.sleep(wait_seconds)

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
