import os
import json



from semantic_search import search_papers
from pdf_downloader import download_pdf
from text_extraction import process_pdf
from analysis_module import (
    load_extracted_sections,
    compute_similarity,
    print_similarity_summary
)



DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
EXTRACTED_DIR = os.path.join(DATA_DIR, "extracted")
ANALYSIS_DIR = os.path.join(DATA_DIR, "analysis")

os.makedirs(PDF_DIR, exist_ok=True)

def run_milestone_1(topic, paper_limit=3):
    papers = search_papers(topic, paper_limit)
    final_output = []

    for idx, paper in enumerate(papers, start=1):
         if paper.get("pdf_url"):
            pdf_path = os.path.join(PDF_DIR, f"paper_{idx}.pdf")
            success = download_pdf(paper["pdf_url"], pdf_path)

            if not success:
                pdf_path = None

        paper["pdf_path"] = pdf_path
        final_output.append(paper)

    # Save structured output
    with open(os.path.join(DATA_DIR, "papers_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)
    for paper in final_output:
        if paper.get("pdf_path"):
            process_pdf(paper["pdf_path"], EXTRACTED_DIR)
    papers = load_extracted_sections(EXTRACTED_DIR)
    similarity = compute_similarity(papers)
    print_similarity_summary(papers, similarity)


    with open(os.path.join(ANALYSIS_DIR, "key_findings.json"), "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=4)

    with open(os.path.join(ANALYSIS_DIR, "similarity_scores.json"), "w", encoding="utf-8") as f:
        json.dump(similarity, f, indent=4)


    # Print references
    print("\nGenerated APA References:\n")
    for i, paper in enumerate(final_output, start=1):
        print(f"[{i}] {paper['apa_reference']}")

    

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run_milestone_1(topic,paper_limit=5)


