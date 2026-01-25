import requests
import os

def download_pdf(pdf_url, paper_title):
    os.makedirs("pdfs", exist_ok=True)

    # sanitize title for filename
    safe_title = (
        paper_title.replace("/", "")
        .replace("\\", "")
        .replace(":", "")
        .replace("*", "")
        .replace("?", "")
        .replace("\"", "")
        .replace("<", "")
        .replace(">", "")
        .replace("|", "")
        .replace(" ", "_")
    )

    pdf_path = f"pdfs/{safe_title}.pdf"

    try:
        response = requests.get(pdf_url, timeout=30, allow_redirects=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "pdf" not in content_type.lower():
            print(f"⚠️ Warning: File may not be a PDF for '{paper_title}'")

        with open(pdf_path, "wb") as f:
            f.write(response.content)

        print(f"✅ PDF saved as: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"❌ Error downloading PDF for '{paper_title}': {e}")
        return None

