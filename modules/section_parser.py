import json
import re
import os

SECTION_HEADERS = [
    "abstract",
    "introduction",
    "methods",
    "methodology",
    "results",
    "discussion",
    "conclusion"
]

def split_into_sections(raw_texts):
    sectioned = {}

    for paper, text in raw_texts.items():
        sections = {}
        lower_text = text.lower()

        for i, header in enumerate(SECTION_HEADERS):
            pattern = rf"\n{header}\n|\n{header}:"
            matches = list(re.finditer(pattern, lower_text))

            if not matches:
                continue

            start = matches[0].start()
            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(lower_text)
            )

            sections[header] = text[start:end].strip()

        sectioned[paper] = sections

    os.makedirs("data/extracted_text", exist_ok=True)
    with open("data/extracted_text/sectioned_text.json", "w", encoding="utf-8") as f:
        json.dump(sectioned, f, indent=4)

    print("✅ Section-wise text extracted")
    return sectioned
