import requests

def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200 and "pdf" in response.headers.get("Content-Type", ""):
        with open(save_path, "wb") as file:
            file.write(response.content)
        return True

    return False
