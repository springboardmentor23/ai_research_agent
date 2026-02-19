import json
from typing import Dict


def load_generated_draft(draft_path: str) -> Dict:
    with open(draft_path, "r", encoding="utf-8") as f:
        return json.load(f)


def split_sections(draft_text: str) -> Dict[str, str]:
    """
    Splits a draft into Abstract, Methods, Results sections.
    Works even if headings are missing or inconsistent.
    """
    sections = {"Abstract": "", "Methods": "", "Results": ""}

    current = None
    lines = draft_text.split("\n")

    for line in lines:
        clean = line.strip().lower()

        if "abstract" in clean:
            current = "Abstract"
            continue
        elif "methods" in clean:
            current = "Methods"
            continue
        elif "results" in clean:
            current = "Results"
            continue

        if current:
            sections[current] += line + "\n"

    return sections


def review_draft(draft_text: str) -> Dict:
    """
    Creates a structured review object.
    """
    sections = split_sections(draft_text)

    return {
        "sections": sections,
        "word_count": len(draft_text.split()),
        "has_abstract": len(sections["Abstract"].strip()) > 50,
        "has_methods": len(sections["Methods"].strip()) > 50,
        "has_results": len(sections["Results"].strip()) > 50
    }
