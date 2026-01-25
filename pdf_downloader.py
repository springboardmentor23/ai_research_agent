import os
import requests
import time
import re
from pathlib import Path

PDF_FOLDER = "pdf"
PDF_DOWNLOAD_TIMEOUT = 15
MIN_PDF_SIZE = 1000
DOWNLOAD_DELAY = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def ensure_folder_exists(folder_path):
    output_path = Path(folder_path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

def sanitize_filename(filename):
    filename = filename.replace(" ", "_")
    filename = re.sub(r'[<>":\/\\|?*]', '', filename)
    return filename

def validate_pdf_content(content, min_size=MIN_PDF_SIZE):
    if not content:
        return False
    if len(content) < min_size:
        return False
    if not content.startswith(b'%PDF'):
        return False
    return True

def extract_pdf_url(paper):
    pdf_url = None
    
    if paper.get("openAccessPdf"):
        open_access = paper.get("openAccessPdf")
        if isinstance(open_access, dict):
            pdf_url = open_access.get("url")
        elif isinstance(open_access, str):
            pdf_url = open_access
    
    if not pdf_url and paper.get("arxivId"):
        arxiv_id = paper.get("arxivId")
        pdf_url = f"http://arxiv.org/pdf/{arxiv_id}.pdf"
    
    if not pdf_url and paper.get("url"):
        url = paper.get("url")
        if "arxiv.org" in url:
            arxiv_id = url.split("/abs/")[-1] if "/abs/" in url else url.split("/")[-1]
            pdf_url = f"http://arxiv.org/pdf/{arxiv_id}.pdf"
    
    return pdf_url

def download_pdf(pdf_url, title, output_folder=PDF_FOLDER):
    if not pdf_url:
        return None
    
    output_path = ensure_folder_exists(output_folder)
    
    safe_title = sanitize_filename(title)
    safe_title = safe_title[:100].strip()
    
    pdf_file = output_path / f"{safe_title}.pdf"
    
    if pdf_file.exists():
        print(f"  Already exists: {pdf_file.name}")
        return str(pdf_file)
    
    try:
        response = requests.get(pdf_url, headers=HEADERS, timeout=PDF_DOWNLOAD_TIMEOUT)
        
        if response.status_code == 200 and validate_pdf_content(response.content, MIN_PDF_SIZE):
            with open(pdf_file, 'wb') as f:
                f.write(response.content)
            size_mb = len(response.content) / (1024 * 1024)
            print(f"  Downloaded: {pdf_file.name} ({size_mb:.2f} MB)")
            return str(pdf_file)
        else:
            print(f"  Failed: {title}")
            return None
    
    except requests.RequestException as e:
        print(f"  Error: {str(e)[:50]}")
        return None

def download_all_pdfs(papers, output_folder=PDF_FOLDER):
    pdf_paths = []
    
    print(f"\nDownloading {len(papers)} PDFs...\n")
    
    downloaded = 0
    failed = 0
    
    for i, paper in enumerate(papers, 1):
        title = paper.get("title", "Unknown")
        
        pdf_url = extract_pdf_url(paper)
        
        if not pdf_url:
            print(f"{i}. {title}")
            print(f"  No direct PDF URL available")
            failed += 1
            continue
        
        print(f"{i}. {title}")
        pdf_path = download_pdf(pdf_url, title, output_folder)
        
        if pdf_path:
            pdf_paths.append({
                "title": title,
                "path": pdf_path,
                "paperId": paper.get("paperId")
            })
            downloaded += 1
        else:
            failed += 1
        
        time.sleep(DOWNLOAD_DELAY)
    
    print(f"\nDownload Summary:")
    print(f"  Downloaded: {downloaded}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(papers)}")
    
    return pdf_paths

def list_downloaded_pdfs(folder=PDF_FOLDER):
    output_path = ensure_folder_exists(folder)
    pdf_files = list(output_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\nNo PDFs in {folder}/")
        return []
    
    print(f"\nDownloaded PDFs ({len(pdf_files)}):")
    for i, pdf in enumerate(pdf_files, 1):
        size = pdf.stat().st_size / (1024 * 1024)
        print(f"  {i}. {pdf.name} ({size:.2f} MB)")
    
    return pdf_files

def get_pdf_count(folder=PDF_FOLDER):
    output_path = ensure_folder_exists(folder)
    return len(list(output_path.glob("*.pdf")))
