import os
import shutil
import stat
import sys

from paper_retrieval import fetch_papers
from database import create_table
from json_store import save_to_json
from pdf_downloader import download_pdf
from text_extractor import extract_text_from_pdf
from text_to_json import convert_txt_to_json
from key_phrases import process_key_phrases
from tfidf_vectorizer import build_tfidf_vectors
from similarity import compute_similarity
from cross_compare import cross_compare_papers


# ===============================
# Terminal Section Formatter
# ===============================

def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


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
        "extracted_texts_json",
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

# Database safe create
try:
    create_table()
except:
    pass


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

print(f"\n✅ {len(papers)} papers fetched\n")

if len(papers) == 0:
    print("❌ No papers fetched. Process stopped.")
    sys.exit()


# ===============================
# Download PDFs + Extract Text
# ===============================

section("📄 DOWNLOADING PDFs & EXTRACTING TEXT")

downloaded = 0

for paper in papers:

    pdf_info = paper.get("openAccessPdf")

    if pdf_info and pdf_info.get("url"):

        pdf_url = pdf_info["url"]
        title = paper.get("title", "unknown_paper")

        pdf_path = download_pdf(pdf_url, title)

        if pdf_path:
            downloaded += 1
    else:
        print(f"⚠️ No open-access PDF: {paper.get('title')}")

if downloaded == 0:
    print("\n❌ No PDFs downloaded. Process stopped.")
    sys.exit()
from text_extractor import extract_all_pdfs_text
extract_all_pdfs_text()


# ===============================
# Save Metadata
# ===============================

section("💾 SAVING PAPER METADATA")

save_to_json(topic, papers)

print("✅ Metadata saved")


# ===============================
# TXT → JSON
# ===============================

section("🔁 CONVERTING TXT TO JSON")

convert_txt_to_json()


# ===============================
# Key Phrase Extraction
# ===============================

section("📌 KEY PHRASE EXTRACTION")

process_key_phrases()


# ===============================
# TF-IDF
# ===============================

section("📊 TF-IDF VECTOR CREATION")

tfidf_matrix, paper_names = build_tfidf_vectors()

if tfidf_matrix is None:
    print("\n❌ TF-IDF creation failed.")
    sys.exit()

if len(paper_names) == 1:
    print("\n⚠️ Only one paper found.")
    print("✅ TF-IDF created successfully.")
    print("⛔ Similarity requires at least 2 papers. Process stopped.")
    sys.exit()


# ===============================
# Similarity
# ===============================

section("📈 COSINE SIMILARITY MATRIX")

similarity_matrix = compute_similarity(tfidf_matrix, paper_names)


# ===============================
# Cross Paper Comparison
# ===============================

section("🔍 CROSS PAPER COMPARISON")

cross_compare_papers(similarity_matrix, paper_names)


# ===============================
# End
# ===============================

print("\n===== PROCESS COMPLETED SUCCESSFULLY =====\n")
