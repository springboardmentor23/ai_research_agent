import os
import json


def prepare_cleaned_dataset(papers_by_topic):
    """
    Converts raw paper data into a cleaned dataset
    suitable for analysis.
    """

    cleaned_dataset = []

    for topic, papers in papers_by_topic.items():
        for paper in papers:
            record = {
                "topic": topic,
                "title": paper.get("title"),
                "authors": paper.get("authors", []),
                "year": paper.get("year"),
                "abstract": paper.get("abstract"),
                "paper_url": paper.get("paper_url")
            }
            cleaned_dataset.append(record)

    return cleaned_dataset


def save_cleaned_dataset(cleaned_dataset):
    """
    Saves the cleaned dataset into
    data/datasets/cleaned_dataset.json
    """

    folder_path = os.path.join("data", "datasets")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "cleaned_dataset.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cleaned_dataset, file, indent=4)

    print("Cleaned dataset saved at:", file_path)
