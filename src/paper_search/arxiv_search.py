import feedparser
from urllib.parse import quote_plus

def fetch_from_arxiv(topic, limit=5):
    # Encode topic to handle spaces and special characters
    encoded_topic = quote_plus(topic)

    query = f"search_query=all:{encoded_topic}&start=0&max_results={limit}"
    url = f"http://export.arxiv.org/api/query?{query}"

    feed = feedparser.parse(url)
    papers = []

    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "year": entry.published[:4],
            "abstract": entry.summary,
            "paper_url": entry.link,
            "openAccessPdf": {
                "url": entry.links[1].href if len(entry.links) > 1 else None
            }
        })

    return papers
