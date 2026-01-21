import os
from pdf_downloader import download_pdf
from semantic_search import fetch_papers
from dataset import prepare_dataset, save_dataset
import json
def show_papers(papers):
    for i, paper in enumerate(papers, start=1):
        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Year:", paper.get("year"))
        print("Abstract:", paper.get("abstract"))
        print("Link:", paper.get("url"))
        print("-" * 40)

topic = input("Enter research topic: ")
limit = int(input("Enter number of papers: "))
os.makedirs("pdfs", exist_ok=True)

papers = fetch_papers(topic, limit)
show_papers(papers)
dataset = prepare_dataset(papers)
save_dataset(dataset)

downloaded_count = 0

for idx, paper in enumerate(papers, start=1):
    pdf_info = paper.get("openAccessPdf")

    if pdf_info and pdf_info.get("url"):
        pdf_url = pdf_info["url"]
        pdf_path = f"pdfs/paper_{idx}.pdf"

        success = download_pdf(pdf_url, pdf_path)

        if success:
            print(f"Downloaded PDF for paper {idx}")
            downloaded_count += 1
        else:
            print(f"Failed to download PDF for paper {idx}")
    else:
        print(f"No open-access PDF for paper {idx}")

print(f"Total PDFs downloaded: {downloaded_count}")
