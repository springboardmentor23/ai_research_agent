import os
import json



from semantic_search import search_papers
from pdf_downloader import download_pdf


DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdfs")

os.makedirs(PDF_DIR, exist_ok=True)

def run_milestone_1(topic, paper_limit=3):
    papers = search_papers(topic, paper_limit)
    final_output = []

    for idx, paper in enumerate(papers, start=1):
        pdf_path = os.path.join(PDF_DIR, f"paper_{idx}.pdf")
        downloaded = download_pdf(paper["pdf_url"], pdf_path)

        paper["pdf_path"] = pdf_path if downloaded else "Not Available"
        final_output.append(paper)

    # Save structured output
    with open(os.path.join(DATA_DIR, "papers_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    # Print references
    print("\nGenerated APA References:\n")
    for i, paper in enumerate(final_output, start=1):
        print(f"[{i}] {paper['apa_reference']}")

    

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run_milestone_1(topic)

