import requests

def download_pdf(pdf_url, save_path):
    if not pdf_url:
        return False

    try:
        response = requests.get(
            pdf_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        if response.status_code == 200 and "pdf" in response.headers.get("Content-Type", "").lower():
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True

    except requests.exceptions.RequestException:
        return False

    return False
