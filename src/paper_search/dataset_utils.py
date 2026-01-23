import json
import os

def prepare_cleaned_dataset(papers_by_topic):
    dataset = []

    for topic, papers in papers_by_topic.items():
        for paper in papers:

            raw_authors = paper.get("authors", [])
            authors = []

            # Handle both Semantic Scholar and arXiv formats
            for a in raw_authors:
                if isinstance(a, dict):
                    authors.append(a.get("name"))
                elif isinstance(a, str):
                    authors.append(a)

            dataset.append({
                "topic": topic,
                "title": paper.get("title"),
                "authors": authors,
                "year": paper.get("year"),
                "abstract": paper.get("abstract"),
                "url": paper.get("url") or paper.get("paper_url")
            })

    return dataset



def save_cleaned_dataset(dataset):
    os.makedirs("data/datasets", exist_ok=True)

    with open("data/datasets/cleaned_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)

    print("Cleaned dataset saved at: data/datasets/cleaned_dataset.json")
