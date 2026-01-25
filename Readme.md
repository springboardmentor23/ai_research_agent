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
