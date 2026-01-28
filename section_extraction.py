import re
import json

def extract_sections(text):
    """Split text into common sections like Introduction, Methods, Results, Conclusion."""
    sections = {}
    headings = ["Introduction", "Methods", "Methodology", "Results", "Discussion", "Conclusion"]
    splits = re.split(r'(?i)^\s*(' + '|'.join(headings) + r')\s*$', text, flags=re.MULTILINE)
    for i in range(1, len(splits), 2):
        section_name = splits[i].strip()
        section_text = splits[i+1].strip()
        sections[section_name] = section_text
    return sections

def save_sections(sections, filename="section_data.json"):
    """Save extracted sections to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=4)
    print(f"Saved sections to '{filename}'")
