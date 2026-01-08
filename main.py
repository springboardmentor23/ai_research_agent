import os
import json
import requests
from tqdm import tqdm
from IPython.display import display, Markdown

import time
import requests
import json


# fetch papers
def fetch_papers(topic, limit=2, retries=3, wait_seconds=3):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "paperId,title,authors,year,abstract,url"
    }

    for attempt in range(retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json().get("data", [])

        elif response.status_code == 429:
            print("Rate limit reached. Waiting...")
            time.sleep(wait_seconds)

        else:
            response.raise_for_status()

    return []


# show papers
def show_papers(topic, papers):
    print(f"\nTopic: {topic}")

    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a["name"] for a in paper.get("authors", []))

        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Authors:", authors)
        print("Year:", paper.get("year"))
        print("Abstract:", paper.get("abstract"))
        print("Link:", paper.get("url"))
        print("Paper ID:", paper.get("paperId"))
        print("-" * 40)


# dataset creation
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


# saving papers to json file
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# fetch reference papers
def fetch_references(paper_id, limit=4):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"

    params = {
        "limit": limit,
        "fields": "title,authors,year,url"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Failed to fetch references")
        return []

    data = response.json().get("data")

    if not data:
        print("No references found for this paper.")
        return []

    references = []
    for r in data:
        cited = r.get("citedPaper")
        if cited:
            references.append(cited)

    return references


def show_references(references):
    for i, ref in enumerate(references, start=1):
        authors = ", ".join(a["name"] for a in ref.get("authors", []))

        print("\nReference", i)
        print("Title:", ref.get("title"))
        print("Authors:", authors)
        print("Year:", ref.get("year"))
        print("Link:", ref.get("url"))
        print("-" * 50)


# main execution
topics = [
    "rice crop disease detection",
    "emergency vehicle routing system",
    "kidney stone detection using image processing"
]

papers_by_topic = {}

for topic in topics:
    papers = fetch_papers(topic)

    if not papers:
        print(f"\nNo papers found for topic: {topic}")
        print("Manual search: https://www.semanticscholar.org/")
        papers_by_topic[topic] = []
        continue

    show_papers(topic, papers)

    clean_data = prepare_dataset(papers)
    papers_by_topic[topic] = clean_data

    # reference fetch
    paper_id = papers[0]["paperId"]
    print("\nFetching references for first paper...")
    references = fetch_references(paper_id)
    show_references(references)


# saving topic-wise papers
save_json(papers_by_topic, "papers_by_topic.json")

# creating dataset from last topic
dataset = prepare_dataset(papers)
print("Number of papers in dataset:", len(dataset))

