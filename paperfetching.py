import feedparser
from urllib.parse import quote_plus

query = "machine learning"
encoded_query = quote_plus(query)

url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=5"

feed = feedparser.parse(url)

for entry in feed.entries:
    print("Title:", entry.title)
    print("PDF:", entry.links[1].href)
    print("-" * 50)
