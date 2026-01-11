import os
import time
import json
import requests

# ---------------------------------------
# Load API Key from Environment Variable
# ---------------------------------------
API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

if not API_KEY:
    raise ValueError("Semantic Scholar API key not found. Please set environment variable.")

# ---------------------------------------
# Fetch papers from Semantic Scholar
# ---------------------------------------
def fetch_papers(topic, limit=3, retries=3, wait_seconds=2):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url"
    }

    for attempt in range(retries):
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response.json().get("data", [])

        elif response.status_code == 429:
            print("Rate limit hit. Waiting...")
            time.sleep(wait_seconds)

        else:
            print("Error:", response.status_code)
            response.raise_for_status()

    return []


# ---------------------------------------
# Convert papers to structured dataset
# ---------------------------------------
def prepare_dataset(papers):
    dataset = []

    for paper in papers:
        dataset.append({
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "year": paper.get("year"),
            "abstract": paper.get("abstract"),
            "paper_url": paper.get("url")
        })

    return dataset


# ---------------------------------------
# Main pipeline
# ---------------------------------------
def main():
    topic = input("Enter research topic: ").strip()

    print("\nFetching papers...")
    papers = fetch_papers(topic)

    if not papers:
        print("No papers found.")
        return

    print(f"Fetched {len(papers)} papers.")

    dataset = prepare_dataset(papers)

    os.makedirs("outputs", exist_ok=True)

    output_path = "outputs/papers_dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Dataset saved successfully at: {output_path}")


if __name__ == "__main__":
    main()
