from src.milestone_2.pdf_text_extractor import extract_text_from_all_pdfs
from src.milestone_2.section_extractor import process_all_text_files
from src.milestone_2.tfidf_similarity import (
    load_section_texts,
    extract_key_terms,
    compute_similarity_matrix
)
from src.milestone_2.validation import validate_section_files


PDF_FOLDER = "pdfs"
TEXT_OUTPUT_FOLDER = "data/extracted_text"

extract_text_from_all_pdfs(PDF_FOLDER, TEXT_OUTPUT_FOLDER)

print("PDF text extraction completed.")



TEXT_FOLDER = "data/extracted_text"
SECTION_OUTPUT_FOLDER = "data/section_wise_text"

process_all_text_files(TEXT_FOLDER, SECTION_OUTPUT_FOLDER)

print("Section-wise text extraction completed.")



SECTION_FOLDER = "data/section_wise_text"

documents, paper_names = load_section_texts(SECTION_FOLDER)

# -------- KEY FINDINGS --------
key_terms = extract_key_terms(documents)

print("\nKey Findings (Top Terms per Paper):")
for name, terms in zip(paper_names, key_terms):
    print(f"\n{name}:")
    print(", ".join(terms))

# -------- CROSS-PAPER COMPARISON --------
similarity_matrix = compute_similarity_matrix(documents)

print("\nCosine Similarity Matrix:")
for i, row in enumerate(similarity_matrix):
    print(paper_names[i], "->", row)




SECTION_FOLDER = "data/section_wise_text"

validate_section_files(SECTION_FOLDER)

print("\nValidation completed.")
