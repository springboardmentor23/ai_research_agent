import fitz  # PyMuPDF
import os
import json

def extract_text_from_pdfs(pdf_folder="data/papers"):
    extracted = {}

    for file in os.listdir(pdf_folder):
        if not file.endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_folder, file)
        doc = fitz.open(pdf_path)

        full_text = ""
        for page in doc:
            full_text += page.get_text()

        extracted[file] = full_text.strip()

    os.makedirs("data/extracted_text", exist_ok=True)

    with open("data/extracted_text/raw_text.json", "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=4)

    print("✅ Raw text extracted from PDFs")
    return extracted
