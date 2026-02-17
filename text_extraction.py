import os
import fitz  # PyMuPDF

TEXT_DIR = "data/texts"
os.makedirs(TEXT_DIR, exist_ok=True)


def extract_text_from_pdf(pdf_path, paper_id):
    """
    Extracts text from a PDF. If the PDF is missing or corrupt, logs and skips it.
    """
    try:
        # Quick sanity check in case the file is empty / zero bytes
        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
            print(f"Skipping text extraction for paper id - {paper_id}: PDF is missing or empty at {pdf_path}")
            return None

        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Failed to open PDF for paper id - {paper_id} at {pdf_path} due to error - {e}")
        return None

    text = ""
    for page in doc:
        try:
            text += page.get_text()
        except Exception as e:
            print(f"Failed to extract text from a page for paper id - {paper_id} due to error - {e}")

    if not text.strip():
        print(f"No text extracted for paper id - {paper_id}; skipping save.")
        return None

    file_path = os.path.join(TEXT_DIR, f"{paper_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    return file_path