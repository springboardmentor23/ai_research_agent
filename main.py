from modules.paper_search import fetch_papers
from modules.dataset_builder import save_datasets
from modules.pdf_downloader import download_pdfs


if __name__ == "__main__":
    topic = input("Enter the topic: ")

    print("Fetching papers...")
    papers = fetch_papers(topic)

    if not papers:
        print("No papers fetched. Exiting.")
        exit()

    print("\nPreparing dataset...")
    dataset = save_datasets(papers, topic)

    print("\nDownloading PDFs...")
    download_pdfs(dataset)

    print("\nFinish")
