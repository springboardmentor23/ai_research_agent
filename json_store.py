import json
import os

JSON_FILE = "papers.json"

def save_to_json(topic, papers):
    data = {}

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    if topic not in data:
        data[topic] = []

    for paper in papers:
        paper_data = {
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "year": paper.get("year"),
            "download_link": paper.get("url")
        }

        if paper_data not in data[topic]:
            data[topic].append(paper_data)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Data saved to JSON file: {JSON_FILE}")

def load_from_json(topic=None):
    if not os.path.exists(JSON_FILE):
        return {}
    
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if topic:
        return data.get(topic, [])
    
    return data

def get_all_topics():
    data = load_from_json()
    return list(data.keys())

def clear_json_file():
    if os.path.exists(JSON_FILE):
        os.remove(JSON_FILE)
        print(f"JSON file cleared: {JSON_FILE}")
