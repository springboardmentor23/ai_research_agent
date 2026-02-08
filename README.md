# AI Research Agent

An automated tool to fetch research papers from Semantic Scholar and create a structured dataset.

## Features

- 🔍 Search and fetch research papers from Semantic Scholar API
- 📚 Create structured JSON dataset with paper metadata
- 🎯 Support for multiple research topics
- 🚀 Easy to use command-line interface

## How to run in VS Code

1. Open the project folder in VS Code (File → Open Folder → select `ai_research_agent`).
2. Open the terminal: **Terminal → New Terminal** (or press `` Ctrl+` ``).
3. Create and activate a virtual environment (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies: `pip install -r requirements.txt`
5. Run the interactive download: `python download_papers.py`  
   Or run the main pipeline: `python main.py`

## Installation

1. **Activate your virtual environment** (recommended):
   ```bash
   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # On Windows (CMD)
   venv\Scripts\activate.bat
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Method 1: Interactive Download (Recommended)

Use the interactive script to search and download papers with a user-friendly interface:

```bash
python download_papers.py
```

This will:
1. Ask you to enter a research topic (e.g., "machine learning", "neural networks")
2. Ask how many papers you want to fetch
3. Show you a list of available papers
4. Let you choose which papers to download
5. Automatically download PDFs and extract text to JSON format

### Method 2: Programmatic Download

Edit `main.py` to change the topic and run:

```bash
python main.py
```

The default topic is "Economics & education". To change it, edit line 23 in `main.py`:

```python
if __name__ == "__main__":
    run_pipeline("your topic here")  # Change this line
```

**⚠️ Important Note about Rate Limiting:**
- Without an API key, Semantic Scholar limits to **100 requests per 5 minutes**
- The script includes automatic retry logic and delays to handle this
- If you get 429 errors, wait 5-10 minutes and try again
- For better results, consider getting a free API key (see below)

### Using the Semantic Scholar API Key

Get a free API key from [Semantic Scholar API](https://www.semanticscholar.org/product/api), then set it as an environment variable before running any script: in **PowerShell** use `$env:SEMANTIC_SCHOLAR_API_KEY="your_api_key_here"`, in **CMD** use `set SEMANTIC_SCHOLAR_API_KEY=your_api_key_here`, or in **macOS/Linux** use `export SEMANTIC_SCHOLAR_API_KEY="your_api_key_here"`. The project reads this variable automatically when you run `python main.py` or `python download_papers.py`; no code changes are needed, and using a key gives higher rate limits and fewer 429 errors when fetching many papers.

### Generating a research paper (Gemini)

The script `generate_paper.py` uses the **Google Gemini API** to write a full APA-style research paper (Introduction, Method, Results, Discussion) from your project’s common datasets/methods/algorithms, key findings, and optional external text. Set your Gemini API key (get one at [Google AI Studio](https://aistudio.google.com/apikey)), then run:

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key"
python generate_paper.py
```

Optional: `--external "your text"` or `--external-file path/to/file.txt` to add your own findings; `-o paper.txt` to set the output file; `--title "Your Title"` to suggest a title.

## Output Structure

When you download papers, the project creates:

1. **PDFs** in `pdfs/` directory: `<paper_id>.pdf`
2. **Extracted Text** in `extracted_texts/` directory: `<paper_id>.json`
   ```json
   {
     "paper_id": "5d6c6442923c87ca17e5399ecfe712b4f9ab1556",
     "pdf_path": "pdfs/5d6c6442923c87ca17e5399ecfe712b4f9ab1556.pdf",
     "text": "Full extracted text from PDF..."
   }
   ```
3. **Key Findings** in `key_findings/` directory: `<paper_id>_findings.json`
   ```json
   {
     "paper_id": "5d6c6442923c87ca17e5399ecfe712b4f9ab1556",
     "key_findings": ["sentence 1", "sentence 2", ...]
   }
   ```

## Converting Existing Text Files to JSON

If you have existing `.txt` files, convert them to JSON format:

```bash
python convert_to_json.py
```

This converts:
- `extracted_texts/*.txt` → `extracted_texts/*.json`
- `key_findings/*_findings.txt` → `key_findings/*_findings.json`

## Project Structure

- `main.py` - Main script to fetch papers programmatically
- `download_papers.py` - Interactive script to download papers (recommended)
- `fetch_paper.py` - Fetches papers from Semantic Scholar API
- `pdf_downloder.py` - Downloads PDF files
- `text_extraction.py` - Extracts text from PDFs and saves as JSON
- `key_phrases.py` - Extracts key findings and saves as JSON
- `similarity.py` - Computes similarity between papers
- `extract_common_terms.py` - Extracts common datasets, methods, algorithms to JSON
- `generate_paper.py` - Generates APA-style research paper via Gemini API
- `convert_to_json.py` - Converts existing text files to JSON format
- `requirements.txt` - Python dependencies

