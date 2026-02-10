# src/main.py

import os
import json
import requests

from src.paper_fetcher import fetch_papers
from src.section_generator import (
    generate_abstract,
    generate_methods,
    generate_results
)
from src.synthesis import synthesize_findings
from src.reference_formatter import format_references_apa


# -----------------------------
# CONSTANTS
# -----------------------------
OUTPUT_DIR = "outputs"
PDF_DIR = os.path.join(OUTPUT_DIR, "downloaded_pdfs")


# -----------------------------
# PDF DOWNLOAD HELPER
# -----------------------------
def download_pdf(pdf_url, save_path):
    """
    Download PDF from open-access URL.
    """
    try:
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"PDF download failed: {e}")
        return False


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():
    print("\nStarting Milestone 3: Automated Research Writing Pipeline\n")

    # Ensure directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)

    # -----------------------------
    # STEP 1: USER INPUT
    # -----------------------------
    topic = input("Enter research topic: ").strip()

    if not topic:
        print("Topic cannot be empty. Exiting.")
        return

    # -----------------------------
    # STEP 2: FETCH PAPERS (Milestone 1)
    # -----------------------------
    print("\nFetching papers...")
    papers = fetch_papers(topic, limit=3)

    if not papers:
        print("No papers found. Exiting pipeline.")
        return

    # Save metadata
    dataset_path = os.path.join(OUTPUT_DIR, "papers_dataset.json")
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2)

    print(f"Saved {len(papers)} papers to papers_dataset.json\n")

    # -----------------------------
    # STEP 3: DOWNLOAD PDFs + COLLECT TEXT (Milestone 2)
    # -----------------------------
    collected_text = ""

    for idx, paper in enumerate(papers, start=1):
        print(f"Processing paper {idx}...")

        # Always use abstract as fallback text
        abstract = paper.get("abstract")
        if abstract:
            collected_text += abstract + "\n"

        open_access = paper.get("openAccessPdf")

        if open_access and open_access.get("url"):
            pdf_url = open_access["url"]
            pdf_path = os.path.join(PDF_DIR, f"paper_{idx}.pdf")

            print("Downloading PDF...")
            success = download_pdf(pdf_url, pdf_path)

            if success:
                print("PDF downloaded successfully.\n")
            else:
                print("PDF download failed. Using abstract only.\n")
        else:
            print("No open-access PDF available. Using abstract only.\n")

    # -----------------------------
    # STEP 4: GENERATE SECTIONS (Milestone 3)
    # -----------------------------
    print("Generating Abstract...")
    abstract_text = generate_abstract(collected_text)

    print("Generating Methods...")
    methods_text = generate_methods(collected_text)

    print("Generating Results...")
    results_text = generate_results(collected_text)

    # -----------------------------
    # STEP 5: SYNTHESIS & REFERENCES
    # -----------------------------
    print("Synthesizing findings...")
    synthesis_text = synthesize_findings(papers)

    print("Formatting references (APA)...")
    references_text = format_references_apa(papers)

    # -----------------------------
    # STEP 6: SAVE FINAL DRAFT
    # -----------------------------
    final_draft = (
        "ABSTRACT\n"
        + abstract_text + "\n\n"
        + "METHODS\n"
        + methods_text + "\n\n"
        + "RESULTS\n"
        + results_text + "\n\n"
        + "SYNTHESIS OF FINDINGS\n"
        + synthesis_text + "\n\n"
        + "REFERENCES\n"
        + references_text
    )

    output_file = os.path.join(OUTPUT_DIR, "milestone3_draft.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_draft)

    print("\nMilestone 3 completed successfully.")
    print(f"Final draft saved to: {output_file}\n")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
