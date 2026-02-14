import json
import re
from collections import Counter

KEYWORDS = [
    "dataset", "datasets", "benchmark",
    "algorithm", "algorithms",
    "model", "models",
    "method", "methods",
    "approach", "framework"
]

def extract_common_terms(section_file="section_data.json"):
    with open(section_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_text = ""

    # data = { paper_1: {Introduction: [...], Method: [...]}, ... }
    for paper_sections in data.values():
        for section_text in paper_sections.values():

            # section_text can be list OR string
            if isinstance(section_text, list):
                section_text = " ".join(section_text)

            all_text += " " + section_text.lower()

    words = re.findall(r"\b[a-zA-Z\-]+\b", all_text)
    filtered = [w for w in words if w in KEYWORDS]

    counts = Counter(filtered)
    return dict(counts)


if __name__ == "__main__":
    common_info = extract_common_terms()

    with open("common_findings.json", "w", encoding="utf-8") as f:
        json.dump(common_info, f, indent=4)

    print("Common datasets / methods / algorithms saved to common_findings.json")
