import fitz
import os

def extract_text_from_pdf(pdf_path, paper_id):
    os.makedirs("data/texts", exist_ok=True)

    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page in doc:
            full_text += page.get_text()

        output_path = f"data/texts/{paper_id}.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        return full_text

    except Exception as e:
        print(f"[SKIPPED] Could not extract {paper_id}: {e}")
        return ""
