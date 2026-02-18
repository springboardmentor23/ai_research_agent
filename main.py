# """
# AI Research Agent - Complete Pipeline
# Orchestrates: Fetching → Downloading → Extraction → Key Finding Distillation → Similarity Analysis
# """

# import os
# import sys
# import json
# import argparse
# from src.fetching import fetch_papers
# from src.download import download_pdf
# from src.extractor import extract_text_from_pdf
# from src.key_finding import extract_key_findings
# from src.tf_idf import compute_similarity

# def ensure_directories():
#     """Create necessary directories for the pipeline"""
#     dirs = ["data/pdfs", "data/texts", "data/dist_texts"]
#     for dir_path in dirs:
#         os.makedirs(dir_path, exist_ok=True)
#         print(f"✓ Directory ready: {dir_path}")

# def run_pipeline(topic, paper_limit=4):
#     """
#     Execute the complete research pipeline:
#     1. Fetch papers from Semantic Scholar
#     2. Download PDFs
#     3. Extract text from PDFs
#     4. Extract key findings
#     5. Compute similarity analysis
#     """
#     print("\n" + "="*70)
#     print("AI RESEARCH AGENT PIPELINE")
#     print("="*70 + "\n")

#     # Step 0: Setup
#     print("[STEP 0] Setting up directories...\n")
#     ensure_directories()

#     # Step 1: Fetch Papers
#     print("\n[STEP 1] Fetching papers from Semantic Scholar...\n")
#     print(f"Topic: {topic}")
#     print(f"Limit: {paper_limit}\n")
    
#     papers = fetch_papers(topic, limit=paper_limit)
#     if not papers:
#         print("❌ No papers found or API error occurred.")
#         return

#     # Save dataset for this topic
#     DATASET_DIR = os.path.join("data", "datasets")
#     os.makedirs(DATASET_DIR, exist_ok=True)

#     safe_topic = topic.lower().replace(" ", "_")
#     dataset_path = os.path.join(DATASET_DIR, f"{safe_topic}.json")

#     dataset = []
#     for p in papers:
#         dataset.append({
#             "title": p.get("title"),
#             "authors": [a.get("name") for a in p.get("authors", [])] if p.get("authors") else [],
#             "year": p.get("year"),
#             "abstract": p.get("abstract"),
#             "paper_url": p.get("url"),
#             "paper_id": p.get("paperId"),
#         })

#     try:
#         with open(dataset_path, "w", encoding="utf-8") as f:
#             json.dump(dataset, f, indent=2)
#         print(f"✓ Dataset saved at: {dataset_path}")
#     except Exception as e:
#         print(f"Failed to save dataset: {e}")
    
#     print(f"✓ Found {len(papers)} papers with open-access PDFs\n")

#     # Step 2: Download PDFs
#     print("[STEP 2] Downloading PDFs...\n")
#     downloaded_pdfs = []
#     for paper in papers:
#         paper_id = paper.get("paperId")
#         title = paper.get("title", "Unknown")
#         pdf_url = paper.get("openAccessPdf", {}).get("url")

#         if not pdf_url:
#             print(f"⊘ No PDF URL for: {title}")
#             continue

#         print(f"Downloading: {title}")
#         pdf_path = download_pdf(pdf_url, paper_id)
        
#         if pdf_path:
#             downloaded_pdfs.append((pdf_path, paper_id))
#         else:
#             print(f"❌ Failed to download: {title}\n")

#     if not downloaded_pdfs:
#         print("❌ No PDFs were successfully downloaded.")
#         return

#     print(f"\n✓ Successfully downloaded {len(downloaded_pdfs)} PDFs\n")

#     # Step 3: Extract Text from PDFs
#     print("[STEP 3] Extracting text from PDFs...\n")
#     extracted_texts = []
#     for pdf_path, paper_id in downloaded_pdfs:
#         text_path = extract_text_from_pdf(pdf_path, paper_id)
#         if text_path:
#             extracted_texts.append(text_path)

#     if not extracted_texts:
#         print("❌ No text was extracted from PDFs.")
#         return

#     print(f"\n✓ Successfully extracted text from {len(extracted_texts)} PDFs\n")

#     # Step 4: Extract Key Findings (Distillation)
#     print("[STEP 4] Extracting key findings and distilling text...\n")
#     distilled_count = extract_key_findings()
    
#     if distilled_count == 0:
#         print("❌ No key findings were extracted.")
#         return

#     print(f"\n✓ Successfully distilled {distilled_count} documents\n")

#     # Step 5: Compute Similarity
#     print("[STEP 5] Computing similarity between distilled texts...\n")
#     compute_similarity()

#     print("="*70)
#     print("✓ PIPELINE COMPLETED SUCCESSFULLY")
#     print("="*70)
#     print(f"\nResults saved in:")
#     print(f"  - Raw PDFs: data/pdfs/")
#     print(f"  - Extracted texts: data/texts/")
#     print(f"  - Distilled findings: data/dist_texts/\n")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="AI Research Agent pipeline runner")
#     # allow zero or more topic words so script can be run with no args
#     parser.add_argument("topic", nargs="*", help="Research topic to search for")
#     parser.add_argument("-n", "--limit", type=int, help="Number of papers to fetch/download")

#     args = parser.parse_args()

#     # If user provided topic words on the CLI, use them; otherwise prompt interactively
#     if args.topic:
#         topic = " ".join(args.topic).strip()
#         if not topic:
#             print("Error: Topic cannot be empty")
#             sys.exit(1)
#     else:
#         topic = input("Enter research topic: ").strip()
#         while not topic:
#             print("Topic cannot be empty")
#             topic = input("Enter research topic: ").strip()

#     # Determine default limit from environment or fallback
#     default_limit = int(os.getenv("PAPER_LIMIT", "4"))

#     # If user passed --limit on CLI, use it. If running fully interactively (no CLI topic), prompt for limit.
#     if args.limit is not None:
#         limit = args.limit
#     else:
#         if not args.topic:
#             # interactive prompt for limit with default shown
#             prompt = f"Enter number of papers to fetch [{default_limit}]: "
#             while True:
#                 val = input(prompt).strip()
#                 if not val:
#                     limit = default_limit
#                     break
#                 try:
#                     limit = int(val)
#                     if limit <= 0:
#                         print("Please enter a positive integer.")
#                         continue
#                     break
#                 except ValueError:
#                     print("Please enter a valid integer.")
#         else:
#             limit = default_limit

#     run_pipeline(topic, paper_limit=limit)


# from dotenv import load_dotenv
# import os

# from src.generator import ReportGenerator
# from src.generation.reference_formatter import ReferenceFormatter
# from src.generation.synthesizer import Synthesizer
# from src.report_builder import ReportBuilder

# # Load environment variables
# load_dotenv()

# def main():

#     # 🔥 Dummy papers (replace this with real extracted papers later)
#     papers = [
#         {
#             "title": "Deep Learning for NLP",
#             "methods": "The study used transformer-based architectures trained on large datasets.",
#             "results": "The model achieved improved accuracy and F1-score compared to CNN models.",
#             "key_findings": "Transformer models outperform traditional architectures in NLP tasks.",
#             "metadata": {
#                 "authors": ["John Smith", "Alice Brown"],
#                 "year": "2023",
#                 "title": "Deep Learning for NLP",
#                 "journal": "Journal of AI Research",
#                 "volume": "15",
#                 "issue": "2",
#                 "pages": "101-120",
#                 "doi": "https://doi.org/10.1234/example"
#             }
#         }
#     ]

#     topic = "Deep Learning in NLP"

#     # Generate AI sections
#     report_generator = ReportGenerator(papers)
#     sections = report_generator.generate_sections()

#     # Generate references
#     synthesizer = Synthesizer(papers)
#     metadata_list = synthesizer.extract_metadata()
#     references = ReferenceFormatter(metadata_list).format_references()

#     # Build final report
#     builder = ReportBuilder(topic)
#     final_report = builder.build_report(sections, references)

#     # Print to console
#     print("\n\n===== FINAL REPORT =====\n")
#     print(final_report)

#     # Save to file
#     builder.save_to_txt(final_report)


# if __name__ == "__main__":
#     main()



# AI Research Agent - Full Pipeline
# Fetch -> Download -> Extract -> Distill -> Draft Report

import os
import sys
import json
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Local imports (replace with your actual modules) ---
from src.fetching import fetch_papers
from src.download import download_pdf
from src.extractor import extract_text_from_pdf
from src.key_finding import extract_key_findings
from src.tf_idf import compute_similarity
from src.generator import ReportGenerator
from src.generation.reference_formatter import ReferenceFormatter
from src.generation.synthesizer import Synthesizer
from src.report_builder import ReportBuilder

# ------------------------------
# Helper: Ensure directories
# ------------------------------
def ensure_directories():
    dirs = ["data/pdfs", "data/texts", "data/dist_texts", "data/datasets"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Directory ready: {dir_path}")

# ------------------------------
# Pipeline Runner
# ------------------------------
def run_pipeline(topic, paper_limit=4):
    print("\n" + "="*70)
    print("AI RESEARCH AGENT PIPELINE")
    print("="*70 + "\n")

    ensure_directories()

    # Step 1: Fetch papers
    print(f"\n[STEP 1] Fetching papers on: {topic}\n")
    papers = fetch_papers(topic, limit=paper_limit)
    if not papers:
        print("❌ No papers found or API error.")
        return

    # Save fetched dataset
    safe_topic = topic.lower().replace(" ", "_")
    dataset_path = os.path.join("data/datasets", f"{safe_topic}.json")
    dataset = []
    for p in papers:
        dataset.append({
            "title": p.get("title"),
            "authors": [a.get("name") for a in p.get("authors", [])] if p.get("authors") else [],
            "year": p.get("year"),
            "abstract": p.get("abstract"),
            "paper_url": p.get("url"),
            "paper_id": p.get("paperId"),
            "pdf_url": p.get("openAccessPdf", {}).get("url")
        })
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"✓ Dataset saved: {dataset_path}")

    # Step 2: Download PDFs
    print("\n[STEP 2] Downloading PDFs...\n")
    downloaded_pdfs = []
    for paper in papers:
        pdf_url = paper.get("openAccessPdf", {}).get("url")
        if not pdf_url:
            print(f"⊘ No PDF URL for: {paper['title']}")
            continue
        pdf_path = download_pdf(pdf_url, paper["paperId"])
        if pdf_path:
            downloaded_pdfs.append((pdf_path, paper["paperId"]))

    if not downloaded_pdfs:
        print("❌ No PDFs downloaded.")
        return
    print(f"✓ Downloaded {len(downloaded_pdfs)} PDFs\n")

    # Step 3: Extract text
    print("[STEP 3] Extracting text from PDFs...\n")
    extracted_texts = []
    for pdf_path, paper_id in downloaded_pdfs:
        text_path = extract_text_from_pdf(pdf_path, paper_id)
        if text_path:
            extracted_texts.append(text_path)
    print(f"✓ Extracted text from {len(extracted_texts)} PDFs\n")

    # Step 4: Key Findings
    print("[STEP 4] Extracting key findings...\n")
    distilled_count = extract_key_findings()
    print(f"✓ Distilled key findings from {distilled_count} documents\n")

    # Step 5: Compute Similarity (optional)
    print("[STEP 5] Computing similarity...\n")
    compute_similarity()
    print("✓ Similarity analysis done\n")

    # ------------------------------
    # Step 6: Prepare Draft Report
    # ------------------------------
    print("[STEP 6] Generating draft report...\n")
    # Load distilled data (replace with your distilled JSON or structure)
    distilled_data_path = os.path.join("data/dist_texts", f"{safe_topic}.json")
    if os.path.exists(distilled_data_path):
        with open(distilled_data_path, "r", encoding="utf-8") as f:
            distilled_papers = json.load(f)
    else:
        # fallback: dummy example
        distilled_papers = [
            {
                "title": "Deep Learning for NLP",
                "methods": "Transformer-based models on large datasets.",
                "results": "Improved accuracy and F1-score vs CNN.",
                "key_findings": "Transformers outperform traditional models.",
                "metadata": {
                    "authors": ["John Smith", "Alice Brown"],
                    "year": "2023",
                    "journal": "Journal of AI Research",
                    "volume": "15",
                    "issue": "2",
                    "pages": "101-120",
                    "doi": "https://doi.org/10.1234/example"
                }
            }
        ]

    # Generate AI sections
    report_generator = ReportGenerator(distilled_papers)
    sections = report_generator.generate_sections()

    # Generate references
    synthesizer = Synthesizer(distilled_papers)
    metadata_list = synthesizer.extract_metadata()
    references = ReferenceFormatter(metadata_list).format_references()

    # Build final report
    builder = ReportBuilder(topic)
    final_report = builder.build_report(sections, references)

    # Print & save
    print("\n===== FINAL DRAFT REPORT =====\n")
    print(final_report)
    builder.save_to_txt(final_report)
    print("\n✓ Draft report saved.\n")

# ------------------------------
# CLI Entry
# ------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Research Agent pipeline runner")
    parser.add_argument("topic", nargs="*", help="Research topic to search for")
    parser.add_argument("-n", "--limit", type=int, help="Number of papers to fetch/download")
    args = parser.parse_args()

    topic = " ".join(args.topic) if args.topic else input("Enter research topic: ").strip()
    limit = args.limit if args.limit else int(os.getenv("PAPER_LIMIT", "4"))

    run_pipeline(topic, paper_limit=limit)
