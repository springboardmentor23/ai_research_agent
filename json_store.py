import json
import os

JSON_FILE = "papers.json"

def save_to_json(topic, papers):
    data = {}

    # Load existing data
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Create topic entry if not exists
    if topic not in data:
        data[topic] = []

    for paper in papers:
        paper_data = {
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "year": paper.get("year"),
            "download_link": paper.get("url")
        }

        # Avoid duplicates
        if paper_data not in data[topic]:
            data[topic].append(paper_data)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)