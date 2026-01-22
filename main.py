import os
import json

from semantic_search import fetch_papers
from dataset import prepare_dataset, save_dataset
from pdf_downloader import download_pdf
from pdf_text_extraction import extract_all_pdfs
from section_extraction import extract_sections
from keyword_extraction import extract_key_sentences
from keyword_analysis import compare_papers


def show_papers(papers):
    for i, paper in enumerate(papers, start=1):
        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Year:", paper.get("year"))
        print("Abstract:", paper.get("abstract"))
        print("Link:", paper.get("url"))
        print("-" * 40)


#  STEP 1: Fetch papers 
topic = input("Enter research topic: ")
limit = int(input("Enter number of papers: "))

papers = fetch_papers(topic, limit)

if not papers:
    print("No papers fetched. Exiting.")
    exit()

show_papers(papers)


# STEP 2: Save dataset
dataset = prepare_dataset(papers)
save_dataset(dataset)


# STEP 3: Download PDFs
os.makedirs("pdfs", exist_ok=True)

for idx, paper in enumerate(papers, start=1):
    pdf_info = paper.get("openAccessPdf")

    if pdf_info and pdf_info.get("url"):
        pdf_path = f"pdfs/paper_{idx}.pdf"
        if download_pdf(pdf_info["url"], pdf_path):
            print(f"Downloaded PDF for paper {idx}")
        else:
            print(f"Failed to download PDF for paper {idx}")
    else:
        print(f"No open-access PDF for paper {idx}")


#  STEP 4: Extract text from PDFs
all_texts = extract_all_pdfs()

if not all_texts:
    print("No text extracted from PDFs. Exiting.")
    exit()


# STEP 5: Section-wise extraction
all_sections = {}

for idx, text in enumerate(all_texts, start=1):
    sections = extract_sections(text)
    all_sections[f"paper_{idx}"] = sections

with open("section_data.json", "w", encoding="utf-8") as f:
    json.dump(all_sections, f, indent=4)

print("Section-wise text saved.")


#  STEP 6: Key-phrase extraction 
all_key_sentences = {}

for idx, text in enumerate(all_texts, start=1):
    key_sentences = extract_key_sentences(text)
    all_key_sentences[f"paper_{idx}"] = key_sentences

with open("key_sentences.json", "w", encoding="utf-8") as f:
    json.dump(all_key_sentences, f, indent=4)

print("Key sentences extracted.")


#  STEP 7: Cross-paper comparison 
similarity_matrix, paper_names = compare_papers()

SIMILARITY_THRESHOLD = 0.5
results = []

for i in range(len(paper_names)):
    for j in range(i + 1, len(paper_names)):
        score = similarity_matrix[i][j]

        if score >= SIMILARITY_THRESHOLD:
            print(
                f"{paper_names[i]} is highly similar to {paper_names[j]} "
                f"(score: {score:.2f})"
            )

            results.append({
                "paper_1": paper_names[i],
                "paper_2": paper_names[j],
                "similarity_score": round(float(score), 2),
                "label": "highly similar"
            })

with open("paper_similarity.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)







