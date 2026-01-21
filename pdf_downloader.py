import requests
import os

def download_pdf(pdf_url, save_path):
    try:
        response = requests.get(pdf_url, timeout=20)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print("Download failed:", e)

    return False
