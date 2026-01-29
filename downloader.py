import os
import requests

def download_pdf(pdf_url, paper_title, folder="downloaded_papers"):
    """Downloads a PDF from a URL and saves it locally."""
    if not pdf_url:
        return None

    if not os.path.exists(folder):
        os.makedirs(folder)

    # Clean title for a safe filename
    safe_title = "".join(c for c in paper_title if c.isalnum() or c in (' ', '_')).rstrip()
    file_path = os.path.join(folder, f"{safe_title}.pdf")

    try:
        # Use a User-Agent to avoid being blocked by publishers
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(pdf_url, headers=headers, stream=True, timeout=20)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192): # Stream large files
                    f.write(chunk)
            return file_path
    except Exception as e:
        print(f"Error downloading {paper_title}: {e}")
    
    return None