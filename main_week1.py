import os

from src.paper_search.paper_search import (
    fetch_papers,
    show_papers,
    fetch_references,
    show_references
)

from src.paper_search.dataset_utils import (
    prepare_cleaned_dataset,
    save_cleaned_dataset
)

from src.paper_search.pdf_downloader import download_pdf


# ---------------- MAIN EXECUTION ----------------

# ask how many topics user wants to search
num_topics = int(input("Enter number of research topics: "))

topics = []

# take topic input one by one
for i in range(num_topics):
    topic = input(f"Enter topic {i + 1}: ").strip()
    topics.append(topic)

papers_by_topic = {}

# ensure pdf folder exists
os.makedirs("pdfs", exist_ok=True)

# process each topic
for topic in topics:
    print(f"\nProcessing topic: {topic}")

    papers = fetch_papers(topic)

    if not papers:
        print(f"No papers found for topic: {topic}")
        print("Manual search: https://www.semanticscholar.org/")
        papers_by_topic[topic] = []
        continue

    # show papers
    show_papers(topic, papers)

    # store raw papers
    papers_by_topic[topic] = papers

    # -------- PDF DOWNLOAD (CORRECT PLACE) --------
    for index, paper in enumerate(papers, start=1):
        pdf_info = paper.get("openAccessPdf")

        if not pdf_info:
            print(f"No open-access PDF available for paper {index}")
            continue

        pdf_url = pdf_info.get("url")

        if not pdf_url:
            print(f"No PDF link found for paper {index}")
            continue

        filename = f"{topic.replace(' ', '_')}_{index}.pdf"
        save_path = os.path.join("pdfs", filename)

        success = download_pdf(pdf_url, save_path)

        if success:
            print(f"PDF downloaded: {filename}")
        else:
            print(f"Failed to download PDF for paper {index}")

    # -------- REFERENCE FETCH (DEMO) --------
    paper_id = papers[0]["paperId"]
    print("\nFetching references for first paper...")
    references = fetch_references(paper_id)

    if references:
        show_references(references)
    else:
        print("No references available for this paper.")


# -------- DATASET CREATION --------

cleaned_dataset = prepare_cleaned_dataset(papers_by_topic)
save_cleaned_dataset(cleaned_dataset)

print("\nNumber of records in cleaned dataset:", len(cleaned_dataset))
print("Milestone 1 completed successfully.")
