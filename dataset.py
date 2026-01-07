import json

def prepare_dataset(papers):
    dataset = []

    for paper in papers:
        record = {
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "year": paper.get("year"),
            "abstract": paper.get("abstract"),
            "paper_url": paper.get("url")
        }
        dataset.append(record)

    return dataset


def save_dataset(dataset, filename="papers_dataset.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)

    print(f"Dataset saved as {filename}")
