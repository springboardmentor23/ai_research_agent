import requests
import feedparser

BASE_URL = "http://export.arxiv.org/api/query"

def fetch_from_arxiv(topic, max_results=5):
    print("Using arXiv API (fallback)...")

    query = f"search_query=all:{topic}&start=0&max_results={max_results}"
    response = requests.get(f"{BASE_URL}?{query}")

    feed = feedparser.parse(response.text)
    papers = []

    for entry in feed.entries:
        paper = {
            "paperId": entry.id.split("/")[-1],
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "year": entry.published[:4],
            "pdf_url": entry.link.replace("abs", "pdf"),
            "source": "arXiv"
        }
        papers.append(paper)

    return papers
