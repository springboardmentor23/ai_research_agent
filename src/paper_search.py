import requests
import json
import os
import time
from tqdm import tqdm

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
PAPER_DETAIL_URL = "https://api.semanticscholar.org/graph/v1/paper/{}"

HEADERS = {
    "User-Agent": "AI-Research-Agent/1.0 (educational project)"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ------------------ PAPER SEARCH ------------------

def fetch_papers(topic, limit=3, retries=3, wait_seconds=5):
    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,paperId"
    }

    for attempt in range(retries):
        response = requests.get(BASE_URL, params=params, headers=HEADERS)

        if response.status_code == 200:
            return response.json().get("data", [])

        elif response.status_code == 429:
            wait_time = wait_seconds * (attempt + 1)
            print(f"Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        else:
            response.raise_for_status()

    raise Exception("Failed after multiple retries due to rate limiting.")


# ------------------ DATASET PREPARATION ------------------

def prepare_dataset(papers):
    dataset = []
    for paper in papers:
        record = {
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "year": paper.get("year"),
            "abstract": paper.get("abstract"),
            "paper_url": paper.get("url"),
            "paper_id": paper.get("paperId")
        }
        dataset.append(record)
    return dataset


# ------------------ PDF DOWNLOADING ------------------

def get_pdf_url(paper_id):
    url = PAPER_DETAIL_URL.format(paper_id)
    params = {
        "fields": "openAccessPdf"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    pdf_info = data.get("openAccessPdf")

    if pdf_info:
        return pdf_info.get("url")

    return None



def download_pdfs(papers):
    pdf_dir = os.path.join(BASE_DIR, "data", "raw_pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    print("\nDownloading PDFs...\n")

    for paper in tqdm(papers):
        paper_id = paper.get("paperId")
        title = paper.get("title")

        if not paper_id or not title:
            continue

        pdf_url = get_pdf_url(paper_id)
        if not pdf_url:
            print(f"No open-access PDF for: {title}")
            continue


        safe_title = title.lower().replace(" ", "_").replace("/", "_")
        pdf_path = os.path.join(pdf_dir, f"{safe_title}.pdf")

        try:
            response = requests.get(pdf_url, stream=True, timeout=20)
            if response.status_code == 200:
                with open(pdf_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
        except Exception:
            continue



def fetch_references(paper_id, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"
    params = {
        "limit": limit,
        "fields": "title,authors,year,url"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json().get("data", [])
    references = []

    for r in data:
        cited = r.get("citedPaper")
        if cited:
            references.append(cited)

    return references


def show_references(references):
    if not references:
        return

    for i, ref in enumerate(references, start=1):
        authors = ", ".join(a["name"] for a in ref.get("authors", []))
        print(f"\nReference {i}")
        print("Title:", ref.get("title"))
        print("Authors:", authors)
        print("Year:", ref.get("year"))
        print("URL:", ref.get("url"))
        print("-" * 60)


# ------------------ MAIN ------------------

if __name__ == "__main__":
    topic = input("Enter research topic: ").strip()

    try:
        papers = fetch_papers(topic)
    except Exception as e:
        print(f"Error fetching papers: {e}")
        papers = []

    dataset = prepare_dataset(papers)

    # Save dataset per topic
    DATASET_DIR = os.path.join(BASE_DIR, "data", "datasets")
    os.makedirs(DATASET_DIR, exist_ok=True)

    safe_topic = topic.lower().replace(" ", "_")
    dataset_path = os.path.join(DATASET_DIR, f"{safe_topic}.json")

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    # Download PDFs
    download_pdfs(papers)

    print("\nMilestone 1 completed successfully 🚀")
    print(f"Dataset saved at: data/datasets/{safe_topic}.json")

    # Optional reference display
    if papers and papers[0].get("paperId"):
        refs = fetch_references(papers[0]["paperId"])
        show_references(refs)
