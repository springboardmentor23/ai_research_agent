"""
AI Research Agent - Complete Pipeline
Orchestrates: Fetching → Downloading → Extraction → Key Finding Distillation → Similarity Analysis
"""

import os
import sys
from src.fetching import fetch_papers
from src.download import download_pdf
from src.extractor import extract_text_from_pdf
from src.key_finding import extract_key_findings
from src.tf_idf import compute_similarity

def ensure_directories():
    """Create necessary directories for the pipeline"""
    dirs = ["data/pdfs", "data/texts", "data/dist_texts"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Directory ready: {dir_path}")

def run_pipeline(topic, paper_limit=4):
    """
    Execute the complete research pipeline:
    1. Fetch papers from Semantic Scholar
    2. Download PDFs
    3. Extract text from PDFs
    4. Extract key findings
    5. Compute similarity analysis
    """
    print("\n" + "="*70)
    print("AI RESEARCH AGENT PIPELINE")
    print("="*70 + "\n")

    # Step 0: Setup
    print("[STEP 0] Setting up directories...\n")
    ensure_directories()

    # Step 1: Fetch Papers
    print("\n[STEP 1] Fetching papers from Semantic Scholar...\n")
    print(f"Topic: {topic}")
    print(f"Limit: {paper_limit}\n")
    
    papers = fetch_papers(topic, limit=paper_limit)
    if not papers:
        print("❌ No papers found or API error occurred.")
        return
    
    print(f"✓ Found {len(papers)} papers with open-access PDFs\n")

    # Step 2: Download PDFs
    print("[STEP 2] Downloading PDFs...\n")
    downloaded_pdfs = []
    for paper in papers:
        paper_id = paper.get("paperId")
        title = paper.get("title", "Unknown")
        pdf_url = paper.get("openAccessPdf", {}).get("url")

        if not pdf_url:
            print(f"⊘ No PDF URL for: {title}")
            continue

        print(f"Downloading: {title}")
        pdf_path = download_pdf(pdf_url, paper_id)
        
        if pdf_path:
            downloaded_pdfs.append((pdf_path, paper_id))
        else:
            print(f"❌ Failed to download: {title}\n")

    if not downloaded_pdfs:
        print("❌ No PDFs were successfully downloaded.")
        return

    print(f"\n✓ Successfully downloaded {len(downloaded_pdfs)} PDFs\n")

    # Step 3: Extract Text from PDFs
    print("[STEP 3] Extracting text from PDFs...\n")
    extracted_texts = []
    for pdf_path, paper_id in downloaded_pdfs:
        text_path = extract_text_from_pdf(pdf_path, paper_id)
        if text_path:
            extracted_texts.append(text_path)

    if not extracted_texts:
        print("❌ No text was extracted from PDFs.")
        return

    print(f"\n✓ Successfully extracted text from {len(extracted_texts)} PDFs\n")

    # Step 4: Extract Key Findings (Distillation)
    print("[STEP 4] Extracting key findings and distilling text...\n")
    distilled_count = extract_key_findings()
    
    if distilled_count == 0:
        print("❌ No key findings were extracted.")
        return

    print(f"\n✓ Successfully distilled {distilled_count} documents\n")

    # Step 5: Compute Similarity
    print("[STEP 5] Computing similarity between distilled texts...\n")
    compute_similarity()

    print("="*70)
    print("✓ PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"\nResults saved in:")
    print(f"  - Raw PDFs: data/pdfs/")
    print(f"  - Extracted texts: data/texts/")
    print(f"  - Distilled findings: data/dist_texts/\n")

if __name__ == "__main__":
    # Accept topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter research topic: ").strip()

    if not topic:
        print("Error: Topic cannot be empty")
        sys.exit(1)

    # Optional: Accept limit from environment variable
    limit = int(os.getenv("PAPER_LIMIT", "4"))

    run_pipeline(topic, paper_limit=limit)