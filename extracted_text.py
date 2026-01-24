import pdfplumber
import os

pdf_folder = "pdfs"
output_folder = "extracted_text"

os.makedirs(output_folder, exist_ok=True)

for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        text = ""
        with pdfplumber.open(os.path.join(pdf_folder, pdf_file)) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"

        with open(os.path.join(output_folder, pdf_file.replace(".pdf", ".txt")), "w", encoding="utf-8") as f:
            f.write(text)

print("✅ Text extracted from all PDFs")
