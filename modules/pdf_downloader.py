import os
import requests

def download_pdfs(dataset):
    os.makedirs("data/papers", exist_ok=True)

    for paper in dataset:
        pdf_url = paper.get("pdf_url")
        title = paper.get("title")

        if not pdf_url:
            print(f"No PDF for: {title}")
            continue

        filename = f"data/papers/{paper['paper_id']}.pdf"

        try:
            response = requests.get(pdf_url, timeout=20)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {title}")
        except Exception as e:
            print(f"Error downloading {title}: {e}")