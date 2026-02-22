import os
import requests

def download_pdfs(papers):
    os.makedirs("data/pdfs", exist_ok=True)

    for paper in papers:
        try:
            response = requests.get(paper["pdf_url"], timeout=20)
            response.raise_for_status()

            file_path = f"data/pdfs/{paper['paperId']}.pdf"

            with open(file_path, "wb") as f:
                f.write(response.content)

            paper["local_path"] = file_path

        except Exception as e:
            print(f"Failed to download {paper['title']} → {e}")
