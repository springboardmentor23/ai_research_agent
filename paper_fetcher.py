from semantic_fetcher import fetch_from_semantic
from arxiv_fetcher import fetch_from_arxiv


def normalize_paper_fields(papers):
    """
    Ensures every paper dictionary contains
    required fields without breaking old structure.
    """

    normalized = []

    for paper in papers:

        # Keep existing fields
        paper_id = paper.get("paperId") or paper.get("id") or ""
        title = paper.get("title", "No Title")
        authors = paper.get("authors", "Unknown")
        year = paper.get("year", "Unknown")

        # Ensure URL exists
        url = paper.get("url") or paper.get("link") or "No URL"

        # Ensure PDF URL exists
        pdf_url = paper.get("pdf_url") or paper.get("pdfLink") or None

        normalized.append({
            "paperId": paper_id,
            "title": title,
            "authors": authors,
            "year": year,
            "url": url,
            "pdf_url": pdf_url
        })

    return normalized


def fetch_papers(topic, max_results=5):
    """
    Fetch papers from Semantic Scholar first.
    If it fails, fallback to arXiv.
    Always return normalized structure.
    """

    try:
        papers = fetch_from_semantic(topic, max_results)

        if papers:
            print("Using Semantic Scholar API...")
            return normalize_paper_fields(papers)

    except Exception as e:
        print(f"Semantic Scholar failed: {e}")

    # Fallback
    print("Using arXiv API (fallback)...")

    papers = fetch_from_arxiv(topic, max_results)

    if papers:
        return normalize_paper_fields(papers)

    return []
