"""
Test script to verify all imports and functions are correctly implemented
"""

import sys
import os

print("Testing imports...")

try:
    from src.fetching import fetch_papers
    print("✓ fetching.py imported successfully")
except Exception as e:
    print(f"✗ Error importing fetching: {e}")
    sys.exit(1)

try:
    from src.download import download_pdf
    print("✓ download.py imported successfully")
except Exception as e:
    print(f"✗ Error importing download: {e}")
    sys.exit(1)

try:
    from src.extractor import extract_text_from_pdf
    print("✓ extractor.py imported successfully")
except Exception as e:
    print(f"✗ Error importing extractor: {e}")
    sys.exit(1)

try:
    from src.key_finding import extract_key_findings
    print("✓ key_finding.py imported successfully")
except Exception as e:
    print(f"✗ Error importing key_finding: {e}")
    sys.exit(1)

try:
    from src.tf_idf import compute_similarity, load_documents
    print("✓ tf_idf.py imported successfully")
except Exception as e:
    print(f"✗ Error importing tf_idf: {e}")
    sys.exit(1)

try:
    from main import run_pipeline, ensure_directories
    print("✓ main.py imported successfully")
except Exception as e:
    print(f"✗ Error importing main: {e}")
    sys.exit(1)

print("\n✓ All modules imported successfully!")
print("\nPipeline components:")
print("  1. fetch_papers() - Fetch papers from Semantic Scholar")
print("  2. download_pdf() - Download PDF files")
print("  3. extract_text_from_pdf() - Extract text from PDFs")
print("  4. extract_key_findings() - Distill key findings from text")
print("  5. compute_similarity() - Analyze similarity using TF-IDF")
print("  6. run_pipeline() - Orchestrate entire workflow")

print("\nTo run the pipeline, execute:")
print("  python main.py \"Your Research Topic\"")
