
import requests
import os
from tqdm import tqdm
from config.settings import DATA_PATH

def download_pdf(pdf_url, filename):
    os.makedirs(DATA_PATH, exist_ok=True)
    path = os.path.join(DATA_PATH, filename)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(pdf_url, stream=True, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"❌ PDF blocked or not accessible: {pdf_url}")
            return None

        total = int(response.headers.get("content-length", 0))

        with open(path, "wb") as file, tqdm(
            desc=filename,
            total=total,
            unit="B",
            unit_scale=True,
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    size = file.write(chunk)
                    bar.update(size)

        print(f"✅ Downloaded: {filename}")
        return path

    except Exception as e:
        print(f"⚠️ Failed to download PDF: {e}")
        return None
