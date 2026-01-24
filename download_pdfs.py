import feedparser
import requests
import os
from urllib.parse import quote_plus

query = "machine learning"
max_results = 10
save_folder = "pdfs"

# Create folder
os.makedirs(save_folder, exist_ok=True)

encoded_query = quote_plus(query)

url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"

feed = feedparser.parse(url)

print(f"Total papers found: {len(feed.entries)}\n")

for index, entry in enumerate(feed.entries, start=1):
    pdf_url = None

    for link in entry.links:
        if link.type == "application/pdf":
            pdf_url = link.href
            break

    if pdf_url:
        filename = f"paper_{index}.pdf"
        filepath = os.path.join(save_folder, filename)

        print(f"Downloading {filename}")

        response = requests.get(pdf_url, stream=True)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

print("\n✅ All PDFs downloaded successfully")
