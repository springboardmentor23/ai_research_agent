from .paper_search import fetch_from_semantic_scholar
from .arxiv_search import fetch_from_arxiv

def fetch_papers_hybrid(topic):
    print(f"\nSearching Semantic Scholar for: {topic}")
    papers = fetch_from_semantic_scholar(topic)

    if papers:
        print("Papers fetched from Semantic Scholar")
        return papers

    print("Switching to arXiv fallback...")
    papers = fetch_from_arxiv(topic)

    if papers:
        print("Papers fetched from arXiv")
        return papers

    print("No papers found from any source.")
    return []
