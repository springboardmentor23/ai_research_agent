import json
import csv
import os

def save_datasets(papers, topic):
    os.makedirs("data/datasets", exist_ok=True)

    json_path = "data/datasets/papers_metadata.json"
    csv_path = "data/datasets/papers_metadata.csv"

    structured_data = []

    for idx, paper in enumerate(papers, start=1):
        structured_data.append({
            "paper_id": f"{topic}_{idx}",
            "title": paper.get("title"),
            "authors": ", ".join(a["name"] for a in paper.get("authors", [])),
            "year": paper.get("year"),
            "abstract": paper.get("abstract"),
            "paper_url": paper.get("url"),
            "pdf_url": (
                paper.get("openAccessPdf", {}).get("url")
                if paper.get("openAccessPdf") else None
            )
        })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4, ensure_ascii=False)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=structured_data[0].keys())
        writer.writeheader()
        writer.writerows(structured_data)

    print("Datasets created:")
    print(f"- {json_path}")
    print(f"- {csv_path}")

    return structured_data
