from paper_retrieval import fetch_papers
from database import create_table, insert_paper
from json_store import save_to_json
from pdf_downloader import download_all_pdfs, list_downloaded_pdfs
from pdf_text_extractor import extract_all_pdfs_text
from key_phrase_extractor import process_all_extracted_texts
from cross_paper_analysis import create_cross_paper_analysis

print("\n===== AI Research Paper Fetcher =====\n")

topic = input("Enter research topic: ")
num_papers = int(input("Enter number of papers to fetch: "))
download_pdfs = input("Download papers as PDF? (yes/no): ").lower().strip()

papers = fetch_papers(topic, limit=num_papers)

print(f"\n{len(papers)} papers fetched for topic '{topic}'\n")

for i, paper in enumerate(papers, start=1):
    title = paper.get("title")
    authors = ", ".join(a["name"] for a in paper.get("authors", []))
    year = paper.get("year")
    abstract = paper.get("abstract")
    url = paper.get("url")

    print(f"Paper {i}")
    print("Title       :", title)
    print("Authors     :", authors)
    print("Year        :", year)
    print("Abstract    :", abstract)
    print("Download URL:", url)
    print("-" * 80)

save_to_json(topic, papers)

if download_pdfs in ['yes', 'y']:
    download_all_pdfs(papers)
    print("\nExtracting text from PDFs...")
    extract_all_pdfs_text()
    print("\nExtracting key phrases...")
    process_all_extracted_texts()

create_table()

for paper in papers:
    title = paper.get("title")
    authors = ", ".join(a["name"] for a in paper.get("authors", []))
    year = paper.get("year")
    url = paper.get("url")
    insert_paper(topic, title, authors, year, url)

print("\nPapers saved to:")
print("SQLite Database: papers.db")
print("JSON File: papers.json")

list_downloaded_pdfs()

create_cross_paper_analysis()

print("===== DONE =====\n")
