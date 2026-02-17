import os
import re
import requests

def _try_arxiv_fallback(title):
    """
    If title looks like an arXiv paper (contains arXiv ID), try to fetch PDF from arXiv.
    """
    m = re.search(r'arXiv[:\s]*(\d{4}\.\d{4,5})', title, re.IGNORECASE)
    if not m:
        return None
    arxiv_id = m.group(1)
    arxiv_pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    try:
        r = requests.get(arxiv_pdf_url, timeout=15)
        if r.status_code == 200:
            return arxiv_pdf_url
    except Exception:
        pass
    return None

def download_pdfs(dataset):
    os.makedirs("data/papers", exist_ok=True)

    for paper in dataset:
        pdf_url = paper.get("pdf_url")
        title = paper.get("title")
        paper_url = paper.get("paper_url")
        paper_id = paper.get("paper_id")

        if not pdf_url:
            # fallback: try Semantic Scholar paper page to sniff a PDF link
            if paper_url:
                try:
                    head = requests.head(paper_url, timeout=10, allow_redirects=True)
                    # Some publishers redirect to a PDF; detect by content-type
                    ct = head.headers.get("Content-Type", "")
                    if "pdf" in ct.lower():
                        pdf_url = paper_url
                except Exception:
                    pass

            # second fallback: arXiv ID in title
            if not pdf_url:
                pdf_url = _try_arxiv_fallback(title)

        if not pdf_url:
            print(f"No PDF for: {title}")
            continue

        filename = f"data/papers/{paper_id}.pdf"

        try:
            response = requests.get(pdf_url, timeout=20)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {title} (status {response.status_code})")
        except Exception as e:
            print(f"Error downloading {title}: {e}")