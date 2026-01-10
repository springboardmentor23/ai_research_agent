

from retrieval.semantic_search import search_papers
from retrieval.pdf_downloader import download_pdf

def run_pipeline():
    topic = input("Enter Research Topic: ")
    papers = search_papers(topic, limit=3)

    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a["name"] for a in paper.get("authors", []))

        print(f"\nPaper {i}")
        print(f"Title: {paper.get('title')}")
        print(f"Authors: {authors}")
        print(f"Year: {paper.get('year')}")
        print(f"URL: {paper.get('url')}")
        print("-" * 50)

       # PDF download 
        pdf_url = paper.get("openAccessPdf", {}).get("url")
        if pdf_url:
            filename = f"paper_{i}.pdf"
            download_pdf(pdf_url, filename)

if __name__ == "__main__":
    run_pipeline()
