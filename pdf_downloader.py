import os
import requests
from tqdm import tqdm
from src.config import PDF_DIR

def download_pdf(pdf_url: str, paper_id:str):
    if not pdf_url:
        print(f"skipping {paper_id}: No open-access PDF.")
        RETURN None
    pdf_path = os.path.join(PDF_DIR, f"{paper_id}.pdf")
    
    try:
        response = requests.get(pdf_url, stram=True, timeout=10)

        if response.status_code != 200:
            print(f"skipping {paper_id}: PDF access forbidden.")
            return None
        
        with open(pdf_path, "wb") as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)
        
        return pdf_path
    except requests.exceptions.RequestException:
        print(f"Skipping {paper_id}: Download failed.")
        return None