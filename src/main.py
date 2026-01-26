import json
import os

from paper_fetcher import fetch_papers
from pdf_downloader import download_pdf
from pdf_text_extractor import extract_text_from_pdf
from section_parser import extract_sections
from key_finder import extract_keywords
from comparator import compare_keywords
from validator import validate_sections


DATASET_PATH = "outputs/papers_dataset.json"
PDF_FOLDER = "outputs/downloaded_pdfs"


def milestone_1():
    topic = input("Enter research topic: ")

    print("\nFetching papers...")
    papers = fetch_papers(topic)

    if not papers:
        print("No papers found. Exiting.")
        return []

    dataset = []
    for paper in papers:
        dataset.append({
            "title": paper.get("title"),
            "abstract": paper.get("abstract"),
            "paper_url": paper.get("url")
        })

    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Saved {len(dataset)} papers to papers_dataset.json")
    return dataset


def milestone_2(papers):
    all_keywords = []

    for idx, paper in enumerate(papers, start=1):
        print(f"\nProcessing paper {idx}...")
        pdf_path = f"{PDF_FOLDER}/paper_{idx}.pdf"

        success = download_pdf(paper["paper_url"], pdf_path)
        if not success:
            print("PDF download failed. Skipping paper.")
            continue

        text = extract_text_from_pdf(pdf_path)
        sections = extract_sections(text)
        keywords = extract_keywords(text)
        validation = validate_sections(sections)

        all_keywords.append(keywords)

    if all_keywords:
        common = compare_keywords(all_keywords)
    else:
        common = []

    print("\nMilestone 2 completed successfully.")


def main():
    papers = milestone_1()
    if papers:
        milestone_2(papers)


if __name__ == "__main__":
    main()
