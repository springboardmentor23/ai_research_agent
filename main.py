import os
import json
import requests
import time
from downloader import download_pdf

def fetch_papers(topic, limit=3, retries=3, wait_seconds=5):
    """Automated paper search via Semantic Scholar API[cite: 8]."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,paperId,openAccessPdf"
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
    return []

def prepare_and_download_dataset(papers):
    """Selection and download of research PDFs based on topic input."""
    final_dataset = []
    print(f"\n--- Starting PDF Retrieval for {len(papers)} papers ---")
    
    for i, paper in enumerate(papers, start=1):
        title = paper.get("title")
        oa_info = paper.get("openAccessPdf")
        # Use the direct PDF link if available, otherwise the main URL
        download_url = oa_info.get("url") if oa_info else paper.get("url")
        
        print(f"[{i}/{len(papers)}] Attempting download: {title}")
        
        # Call the downloader module [cite: 28]
        local_path = download_pdf(download_url, title)
        
        # Create the structured dataset record 
        record = {
            "paper_id": paper.get("paperId"),
            "title": title,
            "authors": [a["name"] for a in paper.get("authors", [])],
            "year": paper.get("year"),
            "abstract": paper.get("abstract"),
            "source_url": paper.get("url"),
            "local_pdf_path": local_path  # Stores the path if download succeeded
        }
        final_dataset.append(record)
    
    return final_dataset

# --- Execution Flow ---
user_topic = input("Enter research topic: ") 
fetch_limit = int(input("Enter the number of papers (max 3 suggested): "))

print("Fetching papers from Semantic Scholar...")
papers_metadata = fetch_papers(user_topic, fetch_limit)

if papers_metadata:
    # This step satisfies 'Automatic PDF retrieval' [cite: 10]
    complete_dataset = prepare_and_download_dataset(papers_metadata)
    
    # Save dataset to JSON for Milestone 2 
    with open("research_dataset.json", "w") as f:
        json.dump(complete_dataset, f, indent=4)
        
    print("\n" + "="*30)
    print("MILESTONE 1 COMPLETE")
    print(f"Dataset saved to 'research_dataset.json'")
    print(f"PDFs stored in 'downloaded_papers/' folder")
    print("="*30)
else:
    print("No papers found for this topic.")