import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.semanticscholar.org/graph/v1"
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_API_KEY")

# Path where PDFs will be stored
DATA_PATH = os.path.join("data", "papers")
