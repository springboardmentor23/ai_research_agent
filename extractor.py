import os
import fitz  # PyMuPDF

TEXT_DIR = "data/texts"
os.makedirs(TEXT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path, paper_id):
    """
    Extract all text from PDF and save to data/texts
    Returns file path on success, None on failure.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        if not text.strip():
            print(f"No text extracted from {pdf_path}")
            return None

        file_path = os.path.join(TEXT_DIR, f"{paper_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Extracted text from {pdf_path} → {file_path}")
        return file_path

    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None