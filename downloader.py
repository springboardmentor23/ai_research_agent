import os
import requests


def download_pdf(pdf_url, paper_title, folder="downloaded_papers"):
    """Download a PDF from a URL and save it locally."""

    if not pdf_url:
        print("❌ No URL provided")
        return None

    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Make filename safe
    safe_title = "".join(
        c for c in paper_title if c.isalnum() or c in (" ", "_")
    ).rstrip()

    file_path = os.path.join(folder, f"{safe_title}.pdf")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            pdf_url,
            headers=headers,
            stream=True,
            timeout=30,
            allow_redirects=True
        )

        # Check success
        if response.status_code == 200:

            # Verify it's actually a PDF
            content_type = response.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower():
                print(f"⚠️ Not a PDF file for: {paper_title}")
                return None

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(8192):
                    if chunk:
                        f.write(chunk)

            print(f"✅ Saved: {file_path}")
            return file_path

        else:
            print(f"❌ Failed (status {response.status_code})")
            return None

    except Exception as e:
        print(f"❌ Error downloading {paper_title}: {e}")
        return None
