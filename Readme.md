# AI Research Agent Pipeline

A comprehensive Python pipeline for automated research paper analysis using Semantic Scholar API.

## Pipeline Overview

```
fetching.py → download.py → extractor.py → key_finding.py → tf_idf.py
    (Fetch)      (Download)   (Extract)    (Distill)       (Compare)
```

## Architecture

### 1. **fetching.py** - Paper Fetching
- Queries Semantic Scholar API for research papers
- Filters papers with available open-access PDFs
- Returns: Paper metadata (title, authors, year, abstract, paper_id, PDF URL)

### 2. **download.py** - PDF Download
- Downloads PDFs from provided URLs
- Validates PDF files (checks for %PDF header)
- Stores PDFs in: `data/pdfs/`
- Only saves valid PDF files

### 3. **extractor.py** - Text Extraction
- Extracts raw text from PDF files using PyMuPDF (fitz)
- Processes all pages of each PDF
- Saves extracted text to: `data/texts/`
- Output: `{paper_id}.txt` files

### 4. **key_finding.py** - Key Finding Distillation
- Extracts sentences containing research keywords
- Distills raw text into key findings
- Reads from: `data/texts/`
- Saves to: `data/dist_texts/`
- Output: `{paper_id}_findings.txt` files

### 5. **tf_idf.py** - Similarity Analysis
- Computes TF-IDF vectors for distilled texts
- Calculates cosine similarity between documents
- Reads from: `data/dist_texts/`
- Displays similarity matrix

### 6. **main.py** - Pipeline Orchestrator
- Runs all steps in sequence
- Handles errors and logging
- Manages directory creation
- Entry point for the entire pipeline

## Installation

```bash
# Install required packages
pip install -r requirements.txt
```

**Required packages:**
- requests
- scikit-learn
- PyMuPDF (fitz)
- tqdm

## Usage

### Basic Usage
```bash
python main.py "Machine Learning"
```

### With Command Line Arguments
```bash
python main.py "Natural Language Processing" "Computer Vision"
```

### Set Custom Paper Limit
```bash
set PAPER_LIMIT=10  # Windows
python main.py "AI Ethics"

export PAPER_LIMIT=10  # Linux/Mac
python main.py "AI Ethics"
```

## Directory Structure

```
data/
├── pdfs/              # Downloaded PDF files
├── texts/             # Extracted raw text from PDFs
└── dist_texts/        # Distilled key findings
```

## Output Example

```
======================================================================
AI RESEARCH AGENT PIPELINE
======================================================================

[STEP 0] Setting up directories...
✓ Directory ready: data/pdfs
✓ Directory ready: data/texts
✓ Directory ready: data/dist_texts

[STEP 1] Fetching papers from Semantic Scholar...
Topic: Machine Learning
Limit: 4

✓ Found 4 papers with open-access PDFs

[STEP 2] Downloading PDFs...
Downloading: Deep Neural Networks...
Downloaded PDF for paper xyz123 → data/pdfs/xyz123.pdf
...

[STEP 3] Extracting text from PDFs...
Extracted text from data/pdfs/xyz123.pdf → data/texts/xyz123.txt
...

[STEP 4] Extracting key findings and distilling text...
Extracted 24 key findings from xyz123.txt
...

[STEP 5] Computing similarity between distilled texts...

======================================================================
SIMILARITY ANALYSIS (TF-IDF Cosine Similarity)
======================================================================

xyz123_findings.txt        vs abc456_findings.txt         → 0.5432
...

======================================================================
✓ PIPELINE COMPLETED SUCCESSFULLY
======================================================================
```

## Key Features

✅ **Automatic Paper Fetching** - Query Semantic Scholar API  
✅ **PDF Validation** - Only downloads valid PDF files  
✅ **Text Extraction** - Full PDF to text conversion  
✅ **Intelligent Distillation** - Extracts key research findings  
✅ **Similarity Analysis** - Compares research papers using TF-IDF  
✅ **Error Handling** - Robust error management throughout pipeline  
✅ **Progress Tracking** - Clear logging of each step  

## Customization

### Modify Key Phrases (key_finding.py)
Edit `KEY_PHRASES` list to extract different types of sentences:
```python
KEY_PHRASES = [
    "we propose",
    "our method",
    # Add more phrases...
]
```

### Adjust Paper Limit
```python
run_pipeline(topic, paper_limit=10)  # Fetch up to 10 papers
```

### Change TF-IDF Parameters (tf_idf.py)
```python
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=100,  # Add custom parameters
    min_df=2
)
```

## Troubleshooting

**No PDFs downloaded?**
- Check API key validity in `fetching.py`
- Verify internet connection
- Check rate limiting (Semantic Scholar has rate limits)

**Text extraction issues?**
- Ensure PyMuPDF is installed: `pip install PyMuPDF`
- Some PDFs may be scanned images (not supported)

**Similarity always 0?**
- Ensure distilled texts have similar key phrases
- Check that key_finding.py extracted content

## API Keys

The Semantic Scholar API key is embedded in `fetching.py`. For production use, consider using environment variables:

```python
import os
api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
```

## Performance Notes

- **Initial run**: 2-10 minutes (depending on paper count & file sizes)
- **API rate limit**: ~100 requests per minute
- **Average PDF size**: 2-10 MB

## License

Educational project - Ensure compliance with paper usage rights and API terms.
