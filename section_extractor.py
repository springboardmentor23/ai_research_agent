import json
import re
import os

SECTION_KEYWORDS = {
    "abstract": ["abstract"],
    "introduction": ["introduction", "background"],
    "methodology": ["methodology", "method", "approach"],
    "results": ["results", "experiments", "evaluation"],
    "conclusion": ["conclusion", "future work"]
}

def extract_sections(text):
    text = text.lower()
    sections = {key: "" for key in SECTION_KEYWORDS}
    current_section = None

    for line in text.split("\n"):
        line_clean = line.strip()

        for section, keywords in SECTION_KEYWORDS.items():
            if any(line_clean == k for k in keywords):
                current_section = section
                break

        if current_section:
            sections[current_section] += line + " "

    return sections


def process_all_texts(input_folder="extracted_texts", output_folder="section_texts"):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(input_folder, file), "r", encoding="utf-8") as f:
            text = f.read()

        sections = extract_sections(text)

        out_file = file.replace(".txt", ".json")
        with open(os.path.join(output_folder, out_file), "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=4)

    print("✅ Sections extracted")
