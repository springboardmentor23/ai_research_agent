import os
import requests

DOWNLOAD_DIR = "outputs/downloaded_pdfs"

def download_pdf(pdf_url, filename):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(pdf_url, headers=headers, timeout=15)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Downloaded: {filename}")
        return file_path

    except Exception as e:
        print(f"❌ Failed to download {pdf_url}: {e}")
        return None
