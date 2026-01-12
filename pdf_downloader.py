import requests
import os

def download_pdf(pdf_url, filename):
    if not pdf_url:
        return False

    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return True
    return False
