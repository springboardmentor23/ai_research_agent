import fitz  # PyMuPDF
import json
import os
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text


def extract_sections(text):
    sections = {
        "abstract": "",
        "introduction": "",
        "methodology": "",
        "results": "",
        "conclusion": ""
    }

    patterns = {
        "abstract": r"abstract(.*?)(introduction|methods|methodology)",
        "introduction": r"introduction(.*?)(methods|methodology|results)",
        "methodology": r"(methods|methodology)(.*?)(results|discussion)",
        "results": r"results(.*?)(conclusion|discussion)",
        "conclusion": r"(conclusion|discussion)(.*)"
    }

    lower_text = text.lower()

    for section, pattern in patterns.items():
        match = re.search(pattern, lower_text, re.DOTALL)
        if match:
            sections[section] = match.group(1).strip()

    return sections


def process_pdf(pdf_path, output_dir):
    text = extract_text_from_pdf(pdf_path)
    sections = extract_sections(text)

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        os.path.basename(pdf_path).replace(".pdf", "_sections.json")
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4)

    return output_file
