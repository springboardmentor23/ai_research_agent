import os
import fitz  # PyMuPDF

def extract_all_pdfs(pdf_dir="pdfs"):
    all_texts = []

    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file)
            doc = fitz.open(pdf_path)

            text = ""
            for page in doc:
                text += page.get_text()

            all_texts.append(text)
            print(f"Extracted text from {file}")

    return all_texts   # 🔴 THIS WAS MISSING
