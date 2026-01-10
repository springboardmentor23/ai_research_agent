"""
Dataset handling module for research papers.
"""
import json
from typing import List, Dict, Any


def load_dataset(filepath: str = "papers_dataset.json") -> List[Dict[str, Any]]:
    """Load papers dataset from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_dataset(papers: List[Dict[str, Any]], filepath: str = "papers_dataset.json") -> None:
    """Save papers dataset to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)
    print(f"✅ Dataset saved to {filepath} ({len(papers)} papers)")


def prepare_dataset(papers):
    """Prepare dataset from fetched papers"""
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


def show_dataset(dataset):
    """Display dataset in the terminal"""
    for i, d in enumerate(dataset, start=1):
        print("Paper", i)
        print("Title:", d["title"])
        print("Authors:", ", ".join(d["authors"]))
        print("Year:", d["year"])
        print("URL:", d["paper_url"])
        print("-" * 50)


def format_paper(paper_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format paper data into standard structure."""
    return {
        "title": paper_data.get("title", ""),
        "authors": [author.get("name", "") for author in paper_data.get("authors", []) if author.get("name")],
        "year": paper_data.get("year"),
        "abstract": paper_data.get("abstract"),
        "paper_url": paper_data.get("url", "") or f"https://www.semanticscholar.org/paper/{paper_data.get('paperId', '')}"
    }

