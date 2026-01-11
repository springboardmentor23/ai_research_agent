import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PDF_DIR = os.path.join(DATA_DIR, "papers")
METADATA_FILE = os.path.join(DATE_DIR, "metadata.json")
SEMANTIC-SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
MAX_PAPERS = 3
os.makedirs(PDF_DIR, exist_ok=True)
