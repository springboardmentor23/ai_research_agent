import pdfplumber
import os
import re

def segment_sections(text):
    sections = {
        "INTRODUCTION": "",
        "METHODOLOGY": "",
        "RESULTS": "",
        "CONCLUSION": ""
    }

    patterns = {
        "INTRODUCTION": r"\bintroduction\b",
        "METHODOLOGY": r"\b(methodology|methods|materials and methods)\b",
        "RESULTS": r"\b(results|experiments)\b",
        "CONCLUSION": r"\b(conclusion|discussion|summary)\b"
    }

    text_lower = text.lower()
    indices = {}

    for sec, pat in patterns.items():
        match = re.search(pat, text_lower)
        if match:
            indices[sec] = match.start()

    sorted_sections = sorted(indices.items(), key=lambda x: x[1])

    for i, (sec, start) in enumerate(sorted_sections):
        end = sorted_sections[i + 1][1] if i + 1 < len(sorted_sections) else len(text)
        sections[sec] = text[start:end].strip()

    return sections


def extract_text_from_pdf(pdf_path):
    os.makedirs("extracted_texts", exist_ok=True)

    file_name = os.path.basename(pdf_path).replace(".pdf", ".txt")
    output_path = os.path.join("extracted_texts", file_name)

    full_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        sections = segment_sections(full_text)

        with open(output_path, "w", encoding="utf-8") as f:
            for sec, content in sections.items():
                f.write(f"\n===== {sec} =====\n")
                f.write(content + "\n")
        return output_path

    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return None
