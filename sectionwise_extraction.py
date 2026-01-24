import pdfplumber
import os
import re

PDF_FOLDER = "pdfs"
OUTPUT_FOLDER = "sections"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Common research paper sections
SECTION_TITLES = [
    "abstract",
    "introduction",
    "related work",
    "methodology",
    "proposed method",
    "materials and methods",
    "results",
    "discussion",
    "conclusion",
    "future work",
    "references"
]

def extract_sections(text):
    sections = {}
    current_section = "other"
    sections[current_section] = ""

    lines = text.split("\n")

    for line in lines:
        clean_line = line.strip().lower()

        for title in SECTION_TITLES:
            if re.fullmatch(title, clean_line):
                current_section = title
                sections[current_section] = ""
                break
        else:
            sections[current_section] += line + "\n"

    return sections

for pdf_file in os.listdir(PDF_FOLDER):
    if pdf_file.endswith(".pdf"):
        full_text = ""

        with pdfplumber.open(os.path.join(PDF_FOLDER, pdf_file)) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    full_text += page.extract_text() + "\n"

        extracted_sections = extract_sections(full_text)

        base_name = pdf_file.replace(".pdf", "")

        for section, content in extracted_sections.items():
            if len(content.strip()) > 300:  # ignore very small sections
                file_name = f"{base_name}_{section.replace(' ', '_')}.txt"
                with open(os.path.join(OUTPUT_FOLDER, file_name), "w", encoding="utf-8") as f:
                    f.write(content)

        print(f"✅ Sections extracted for {pdf_file}")

print("\n🎉 Section-wise extraction completed")
