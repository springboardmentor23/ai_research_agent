import json
import time
import requests
import pandas as pd
def fetch_papers(topic, limit=10, retries=3, wait_seconds=5):
    """
    machine learning
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,citationCount,venue"
    }

    for attempt in range(retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json().get("data", [])

        elif response.status_code == 429:
            print(f"Rate limit hit. Waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)

        else:
            response.raise_for_status()

    print("Failed due to repeated rate limiting.")
    return []

# --------------------------------
# Display fetched papers
# --------------------------------
def show_papers(papers):
    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a.get("name", "") for a in paper.get("authors", []))

        print(f"\nPaper {i}")
        print("Title:", paper.get("title", "N/A"))
        print("Authors:", authors or "N/A")
        print("Year:", paper.get("year", "N/A"))
        print("Venue:", paper.get("venue", "N/A"))
        print("Citations:", paper.get("citationCount", 0))
        print("\nAbstract:")
        print(paper.get("abstract") or "Abstract not available")
        print("\nPaper Link:", paper.get("url", "N/A"))
        print("-" * 70)

# --------------------------------
# Convert papers to DataFrame
# --------------------------------
def create_dataset(papers):
    """
    Convert Semantic Scholar paper data into a structured DataFrame
    """
    data = {
        "Title": [],
        "Authors": [],
        "Year": [],
        "Venue": [],
        "CitationCount": [],
        "Abstract": [],
        "URL": []
    }

    for paper in papers:
        authors = ", ".join(a.get("name", "") for a in paper.get("authors", []))

        data["Title"].append(paper.get("title", ""))
        data["Authors"].append(authors)
        data["Year"].append(paper.get("year", ""))
        data["Venue"].append(paper.get("venue", ""))
        data["CitationCount"].append(paper.get("citationCount", 0))
        data["Abstract"].append(paper.get("abstract") or "")
        data["URL"].append(paper.get("url", ""))

    return pd.DataFrame(data)

# --------------------------------
# Main Execution
# --------------------------------
if __name__ == "__main__":

    topic = "Federated Learning in Healthcare"
    print(f"\nFetching papers on topic: {topic}\n")

    papers = fetch_papers(topic, limit=5)

    if not papers:
        print("No papers found.")
    else:
        show_papers(papers)

        # Save JSON
        with open("federated_learning_healthcare_papers.json", "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)

        print("\nJSON file saved successfully.")

        # Create dataset
        df = create_dataset(papers)

        print("\nDataset Preview:")
        print(df.head())

        # Save to Excel
        df.to_excel("federated_learning_healthcare_papers.xlsx", index=False)

        print("\nExcel file saved successfully.")
