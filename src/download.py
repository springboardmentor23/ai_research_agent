import os
import requests
PDF_DIR = "data/pdfs"
def download_pdf(pdf_url, paper_id):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(pdf_url, headers=headers, stream=True, timeout=20)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()

        # Check real PDF
        if "application/pdf" not in content_type:
            print(f"❌ Not a real PDF for {paper_id} | Content-Type: {content_type}")
            return None

        file_path = os.path.join(PDF_DIR, f"{paper_id}.pdf")

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"✅ Real PDF downloaded: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ PDF download failed for {paper_id}: {e}")
        return None
