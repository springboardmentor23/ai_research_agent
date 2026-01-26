# AI Research Agent

An automated tool to fetch research papers from Semantic Scholar and create a structured dataset.

## Features

- 🔍 Search and fetch research papers from Semantic Scholar API
- 📚 Create structured JSON dataset with paper metadata
- 🎯 Support for multiple research topics
- 🚀 Easy to use command-line interface

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

### Basic Usage

Run the script to automatically fetch papers and create `papers_dataset.json`:

```bash
python main.py
```

**⚠️ Important Note about Rate Limiting:**
- Without an API key, Semantic Scholar limits to **100 requests per 5 minutes**
- The script includes automatic retry logic and delays to handle this
- If you get 429 errors, wait 5-10 minutes and try again
- For better results, consider getting a free API key (see below)

### Configuration

You can modify the following variables in `main.py`:

- `TOPICS`: List of research topics to search for
- `PAPERS_PER_TOPIC`: Number of papers to fetch per topic
- `OUTPUT_FILE`: Output JSON file name

### Optional: API Key for Higher Rate Limits

For higher rate limits (no API key needed, but recommended for production):

1. Get a free API key from [Semantic Scholar API](https://www.semanticscholar.org/product/api)
2. Set it as an environment variable:
   ```bash
   # Windows PowerShell
   $env:SEMANTIC_SCHOLAR_API_KEY="your_api_key_here"
   
   # Windows CMD
   set SEMANTIC_SCHOLAR_API_KEY=your_api_key_here
   
   # macOS/Linux
   export SEMANTIC_SCHOLAR_API_KEY=your_api_key_here
   ```

## Dataset Structure

The generated `papers_dataset.json` file contains an array of paper objects:

```json
[
  {
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "year": 2023,
    "abstract": "Paper abstract...",
    "paper_url": "https://www.semanticscholar.org/paper/..."
  }
]
```

## Project Structure

- `main.py` - Main script to fetch papers and create dataset
- `dataset.py` - Dataset handling utilities
- `semantic_search.py` - Semantic search functionality (for future use)
- `papers_dataset.json` - Generated dataset file
- `requirements.txt` - Python dependencies

