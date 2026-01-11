from paper_fetcher import fetch_papers
from src.semantic_search import search_papers
from src.dataset_builder import build_dataset
import json
import os

def main():
    topic = input("Enter research topic: ")

    print("Fetching papers from Semantic Scholar...")
    raw_papers = fetch_papers(topic)
    print(f"Fetched {len(raw_papers)} papers")

    print("Applying semantic filtering...")
    filtered_papers = search_papers(raw_papers, topic)
    print(f"{len(filtered_papers)} papers after semantic filtering")

    print("Filtering papers with open-access PDFs...")
    papers_with_pdf = [
        p for p in filtered_papers
        if p.get("openAccessPdf") is not None
    ]

    print("\n==== RESEARCH PAPERS FOUND ====\n")

    for idx, p in enumerate(papers_with_pdf, start=1):
        title = p.get("title", "N/A")
        abstract = p.get("abstract", "N/A")
        year = p.get("year", "N/A")

        authors = ", ".join(
            a.get("name", "") for a in p.get("authors", [])
        )

        pdf_url = "N/A"
        if p.get("openAccessPdf"):
            pdf_url = p["openAccessPdf"].get("url", "N/A")

        print(f"Paper {idx}")
        print(f"Title    : {title}")
        print(f"Authors  : {authors}")
        print(f"Year     : {year}")
        print(f"Abstract : {abstract}")
        print(f"PDF Link : {pdf_url}")
        print("-" * 60)

    print("Building dataset...")
    dataset = build_dataset(papers_with_pdf)
    print(f"Dataset prepared with {len(dataset)} papers.")

    # Save output (trainer-proof)
    os.makedirs("output", exist_ok=True)
    with open("output/papers_output.json", "w", encoding="utf-8") as f:
        json.dump(papers_with_pdf, f, indent=2)

    print("\nDataset saved to output/papers_output.json")

if __name__ == "__main__":
    main()
