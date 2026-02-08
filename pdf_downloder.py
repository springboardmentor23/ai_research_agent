import os
import time
import requests

PDF_DIR = "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# Browser-like headers so PMC and other hosts don't block with 403
DOWNLOAD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}

def download_pdf(pdf_url, paper_id, retries=2):
    for attempt in range(retries + 1):
        try:
            response = requests.get(
                pdf_url,
                headers=DOWNLOAD_HEADERS,
                timeout=30,
                allow_redirects=True,
            )
            response.raise_for_status()

            file_path = os.path.join(PDF_DIR, f"{paper_id}.pdf")
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403 and attempt < retries:
                time.sleep(3)
                continue
            print(f"Failed to download PDF for paper id - {paper_id} due to error - {e}")
            return None
        except Exception as e:
            print(f"Failed to download PDF for paper id - {paper_id} due to error - {e}")
            return None
    return None
