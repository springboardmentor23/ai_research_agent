import os
import json
import PyPDF2
from pathlib import Path


def ensure_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    full_text = ""

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()

            if page_text:
                full_text += f"--- Page {i+1} ---\n"
                full_text += page_text + "\n\n"

    return full_text


def extract_all_pdfs_text(pdf_folder="pdfs", output_folder="extracted_texts"):

    ensure_folder(output_folder)

    for pdf_file in os.listdir(pdf_folder):

        if not pdf_file.endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_folder, pdf_file)

        print(f"📄 Extracting: {pdf_file}")

        full_text = extract_text_from_pdf(pdf_path)

        output_path = os.path.join(
            output_folder,
            pdf_file.replace(".pdf", ".txt")
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    print("✅ All PDFs extracted into TXT files")
