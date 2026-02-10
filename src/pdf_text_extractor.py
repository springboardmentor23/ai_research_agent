import os
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str or None: Extracted text if successful, else None
    """

    # -----------------------------
    # Safety checks
    # -----------------------------
    if not pdf_path:
        print("No PDF path provided.")
        return None

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return None

    try:
        reader = PdfReader(pdf_path)
        extracted_text = ""

        for page_number, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

        if not extracted_text.strip():
            print(f"No extractable text found in {pdf_path}")
            return None

        return extracted_text.strip()

    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None
