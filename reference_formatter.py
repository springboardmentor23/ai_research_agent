import json

DATASET_PATH = "data/cleaned_dataset.json"

def format_apa_references():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        papers = json.load(f)

    references = []

    for paper in papers:
        authors = ", ".join(paper.get("authors", []))
        year = paper.get("year", "n.d.")
        title = paper.get("title", "")
        url = paper.get("url", "")

        ref = f"{authors} ({year}). {title}. Retrieved from {url}"
        references.append(ref)

    return "\n".join(references)
