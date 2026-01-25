# ===============================
# Terminal Section Formatter
# ===============================

def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ===============================
# Imports
# ===============================

from paper_retrieval import fetch_papers
from database import create_table
from json_store import save_to_json
from pdf_downloader import download_pdf
from text_extractor import extract_text_from_pdf
from section_extractor import process_all_texts
from key_phrases import extract_key_phrases
from tfidf_vectorizer import build_tfidf_vectors
from similarity import compute_similarity
from cross_compare import cross_compare_papers

import os
import shutil
import stat
import sys


# ===============================
# Force delete handler
# ===============================

def force_delete(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


# ===============================
# Clean Old Data
# ===============================

def clean_old_data():

    folders = [
        "pdfs",
        "extracted_texts",
        "section_texts",
        "key_phrases"
    ]

    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, onerror=force_delete)

        os.makedirs(folder)

    if os.path.exists("papers.json"):
        os.remove("papers.json")

    print("🧹 Old project data cleaned!\n")


# ===============================
# Main Program
# ===============================

print("\n===== AI Research Paper Fetcher =====\n")

clean_old_data()

# Create database safely
try:
    create_table()
except Exception as e:
    print("⚠️ Database issue:", e)


# ===============================
# User Input
# ===============================

topic = input("Enter research topic: ")
num_papers = int(input("Enter number of papers to fetch: "))


# ===============================
# Fetch Papers
# ===============================

section("📥 FETCHING RESEARCH PAPERS")

papers = fetch_papers(topic, limit=num_papers)

print(f"\n✅ {len(papers)} papers fetched for topic '{topic}'\n")

# ❌ STOP if no papers
if len(papers) == 0:
    print("❌ No papers fetched. Process stopped.")
    sys.exit()


# ===============================
# Download PDFs + Extract Text
# ===============================

section("📄 DOWNLOADING PDFs & EXTRACTING TEXT")

downloaded_count = 0

for paper in papers:

    pdf_info = paper.get("openAccessPdf")

    if pdf_info and pdf_info.get("url"):

        pdf_url = pdf_info["url"]
        paper_title = paper.get("title", "unknown_paper")

        pdf_path = download_pdf(pdf_url, paper_title)

        if pdf_path:
            extract_text_from_pdf(pdf_path)
            downloaded_count += 1

    else:
        print(f"⚠️ No open-access PDF for: {paper.get('title')}")

# ❌ STOP if no PDFs
if downloaded_count == 0:
    print("\n❌ No PDFs downloaded. Cannot continue.")
    sys.exit()


# ===============================
# Save Metadata
# ===============================

section("💾 SAVING PAPER DETAILS")

save_to_json(topic, papers)
print("✅ Paper metadata saved successfully")


# ===============================
# Section Segmentation
# ===============================

section("📃 SECTION SEGMENTATION")

process_all_texts()


# ===============================
# Key Phrase Extraction
# ===============================

section("📌 KEY PHRASE EXTRACTION")

extract_key_phrases()


# ===============================
# TF-IDF Vectorization
# ===============================

section("📊 TF-IDF VECTOR CREATION")

tfidf_matrix, paper_names = build_tfidf_vectors()

if tfidf_matrix is None:
    print("\n❌ TF-IDF could not be created. Stopping process.")
    sys.exit()

# ✅ If only 1 paper → stop after TF-IDF
if len(paper_names) == 1:
    print("\n⚠️ Only one paper available.")
    print("✅ TF-IDF created successfully.")
    print("⛔ Similarity comparison needs at least 2 papers. Process stopped.")
    sys.exit()

# ===============================
# Cosine Similarity
# ===============================

section("📈 COSINE SIMILARITY MATRIX")

similarity_matrix = compute_similarity(tfidf_matrix, paper_names)


# ===============================
# Cross Paper Comparison
# ===============================

section("🔍 CROSS PAPER COMPARISON")

if len(paper_names) < 2:
    print("⚠️ Only one paper available — cross comparison skipped.")
else:
    cross_compare_papers(similarity_matrix, paper_names)


# ===============================
# End
# ===============================

print("\n===== PROCESS COMPLETED SUCCESSFULLY =====\n")
