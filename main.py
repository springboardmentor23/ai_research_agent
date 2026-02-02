import os
import re
import json

def safe_filename(text):
    return re.sub(r'[\\/*?:"<>| ]+', "_", text)


def print_similarity_matrix(similarity_matrix, paper_names):
    if similarity_matrix is None or len(similarity_matrix) == 0:
        print("\nCosine similarity could not be computed.")
        return

    print("\n--- Cosine Similarity Matrix ---")
    header = "Paper".ljust(18)
    for name in paper_names:
        header += name[:10].ljust(12)
    print(header)

    for i, row in enumerate(similarity_matrix):
        line = paper_names[i][:15].ljust(18)
        for value in row:
            line += f"{value:.2f}".ljust(12)
        print(line)



from src.paper_search.hybrid_search import fetch_papers_hybrid
from src.paper_search.pdf_downloader import download_pdf
from src.paper_search.dataset_utils import (
    prepare_cleaned_dataset,
    save_cleaned_dataset
)

from src.text_extraction.pdf_text_extractor import extract_text_from_all_pdfs
from src.text_extraction.section_extractor import process_all_text_files
from src.text_extraction.tfidf_similarity import (
    extract_key_findings,
    compare_papers_tfidf
)
from src.text_extraction.validation import validate_section_files

print("\n=== AI Research Agent Started ===\n")

while True:
    user_input = input("Enter number of research topics: ").strip()

    if user_input.isdigit():
        num_topics = int(user_input)
        if num_topics > 0:
            break
        else:
            print("Please enter a number greater than 0.")
    else:
        print("Invalid input. Please enter a valid number.")

topics = [input(f"Enter topic {i + 1}: ").strip() for i in range(num_topics)]

os.makedirs("pdfs", exist_ok=True)
os.makedirs("data/datasets", exist_ok=True)
os.makedirs("data/extracted_text", exist_ok=True)
os.makedirs("data/section_wise_text", exist_ok=True)

papers_by_topic = {}

#milestone1
for topic in topics:
    print(f"\nSearching papers for: {topic}")
    papers = fetch_papers_hybrid(topic)

    if not papers:
        print("No papers found.")
        papers_by_topic[topic] = []
        continue

    papers_by_topic[topic] = papers
    topic_safe = safe_filename(topic)

    for idx, paper in enumerate(papers, start=1):
        pdf_info = paper.get("openAccessPdf")
        if not pdf_info or not pdf_info.get("url"):
            continue

        pdf_path = os.path.join("pdfs", f"{topic_safe}_{idx}.pdf")
        download_pdf(pdf_info["url"], pdf_path)

cleaned_dataset = prepare_cleaned_dataset(papers_by_topic)
save_cleaned_dataset(cleaned_dataset)

print("\nWeek 1 completed.")



#milestone2
extract_text_from_all_pdfs("pdfs", "data/extracted_text")
process_all_text_files("data/extracted_text", "data/section_wise_text")

validation_report = validate_section_files("data/section_wise_text")
key_findings, documents = extract_key_findings("data/section_wise_text")

if documents:
    similarity_matrix = compare_papers_tfidf(documents)
else:
    similarity_matrix = None

results = {
    "validation_report": validation_report,
    "key_findings": key_findings,
    "similarity_matrix": similarity_matrix.tolist() if similarity_matrix is not None else None
}

with open("data/datasets/similarity_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print("\n--- Validation Report ---")
for paper, status in (validation_report or {}).items():
    print(f"{paper}: {status}")

print_similarity_matrix(similarity_matrix, list(key_findings.keys()))




#milestone3
from src.milestone_3.pattern_extractor import extract_common_patterns
from src.milestone_3.draft_generator import generate_draft
import json

with open("data/datasets/cleaned_dataset.json", "r") as f:
    cleaned_dataset = json.load(f)

with open("data/datasets/similarity_results.json", "r") as f:
    similarity_data = json.load(f)

patterns = extract_common_patterns(cleaned_dataset)
key_findings = similarity_data.get("key_findings", {})

draft = generate_draft(patterns, key_findings)

with open("data/datasets/ai_draft.txt", "w", encoding="utf-8") as f:
    f.write(draft)

print("AI draft saved to data/datasets/ai_draft.txt")


with open("data/datasets/ai_draft_paper.txt", "w", encoding="utf-8") as f:
    f.write(draft)

print("AI draft generated.")



