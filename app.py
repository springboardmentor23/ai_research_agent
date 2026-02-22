# app.py
import gradio as gr
import os
import json
import time
import base64
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, List, Dict

# Import backend functions from main.py
from main import run_pipeline_logic, revise_generated_paper

# ==========================================================
# CONFIGURATION
# ==========================================================
OUTPUT_DIR = Path("data/output")
PDFS_DIR = Path("data/pdfs")
EXPORTS_DIR = Path("data/exports")
DATASET_FILE = Path("data/cleaned_dataset.json")
HISTORY_FILE = Path("data/history.json")

# Create necessary directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDFS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Example topics for quick input
EXAMPLE_TOPICS = [
    ["Machine Learning in Healthcare", 8, "Focus on diagnostic applications and patient outcome prediction"],
    ["Reinforcement Learning in Autonomous Vehicles", 7, "Emphasis on safety-critical decision making and real-time adaptation"],
    ["NLP for Low-Resource Languages", 6, "Include transfer learning approaches and data augmentation techniques"],
    ["Quantum Machine Learning Algorithms", 5, "Focus on hybrid classical-quantum approaches"]
]

# ==========================================================
# HISTORY MANAGEMENT FUNCTIONS
# ==========================================================

def load_history() -> List[Dict]:
    """Load analysis history from history.json"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_history(topic: str, num_papers: int, timestamp: str, status: str = "completed"):
    """Save an analysis run to history"""
    history = load_history()
    
    # Create new history entry
    entry = {
        "id": len(history) + 1,
        "topic": topic,
        "num_papers": num_papers,
        "timestamp": timestamp,
        "status": status,
        "output_files": {
            "paper": f"generated_paper_{timestamp.replace(' ', '_').replace(':', '-')}.txt",
            "critique": f"critique_{timestamp.replace(' ', '_').replace(':', '-')}.txt"
        }
    }
    
    # Add to beginning of list
    history.insert(0, entry)
    
    # Keep only last 20 entries
    history = history[:20]
    
    # Save back to file
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)
    
    return history

def generate_history_html() -> str:
    """Generate HTML for history display"""
    history = load_history()
    
    if not history:
        return '''
        <div class="alert alert-info" style="margin: 1rem 0; text-align: center;">
            📭 No analysis history yet. Run an analysis to see it here.
        </div>
        '''
    
    html = '<div class="history-container">'
    
    for entry in history[:10]:  # Show last 10 entries
        # Format date for display
        try:
            dt = datetime.fromisoformat(entry['timestamp'].replace(' ', 'T'))
            display_date = dt.strftime("%b %d, %Y • %I:%M %p")
        except:
            display_date = entry['timestamp']
        
        # Truncate topic if too long
        topic_display = entry['topic'][:60] + "..." if len(entry['topic']) > 60 else entry['topic']
        
        # Escape single quotes in topic for JavaScript
        escaped_topic = entry['topic'].replace("'", "\\'")
        
        html += f'''
        <div class="history-item" onclick="(function(){{ 
            document.getElementById('topic-input').value = '{escaped_topic}'; 
            var slider = document.getElementById('num-papers');
            if (slider) {{
                slider.value = {entry['num_papers']};
                // Trigger input event for Gradio to detect the change
                var event = new Event('input', {{ bubbles: true }});
                slider.dispatchEvent(event);
            }}
        }})()">
            <div class="history-icon">📊</div>
            <div class="history-content">
                <div class="history-topic">{topic_display}</div>
                <div class="history-meta">
                    <span class="history-time">🕒 {display_date}</span>
                    <span class="history-papers">📚 {entry['num_papers']} papers</span>
                    <span class="history-status">{'✅' if entry['status'] == 'completed' else '❌'} {entry['status']}</span>
                </div>
            </div>
            <div class="history-arrow">→</div>
        </div>
        '''
    
    html += '''
        <div style="text-align: center; margin-top: 0.75rem;">
            <button class="clear-history-btn" onclick="clearHistory()">🗑️ Clear History</button>
        </div>
    </div>
    '''
    
    return html

def clear_history() -> str:
    """Clear all history"""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
    return generate_history_html()

# ==========================================================
# PROFESSIONAL CSS WITH NORMAL FONT SIZES - FIXED FOR BLACK TEXT
# ==========================================================
CUSTOM_CSS = """
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #7c3aed;
    --success: #059669;
    --warning: #d97706;
    --danger: #dc2626;
    --background: #ffffff;
    --surface: #f8fafc;
    --card-bg: #ffffff;
    --text-primary: #111827;
    --text-secondary: #374151;
    --text-muted: #6b7280;
    --border: #e5e7eb;
    --border-dark: #d1d5db;
}

/* Main container */
.gradio-container {
    max-width: 1400px !important;
    margin: 1rem auto !important;
    background: var(--background) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    padding: 1.5rem !important;
}

/* Typography - Normal website sizes */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif !important;
}

h1 {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.25rem !important;
    color: var(--text-primary) !important;
}

h2 {
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    margin: 1rem 0 0.75rem 0 !important;
    color: var(--text-primary) !important;
    border-bottom: 2px solid var(--border) !important;
    padding-bottom: 0.5rem !important;
}

h3 {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin: 0.75rem 0 !important;
    color: var(--text-primary) !important;
}

p, li, .gr-markdown p {
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    color: var(--text-secondary) !important;
}

label {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.25rem !important;
}

/* Statistics Cards - Compact design */
.stat-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 15px 0;
}

.stat-card {
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    border: 1px solid var(--border);
}

.stat-card-1 {
    background: linear-gradient(135deg, #2563eb, #1e40af);
}

.stat-card-2 {
    background: linear-gradient(135deg, #7c3aed, #5b21b6);
}

.stat-card-3 {
    background: linear-gradient(135deg, #059669, #065f46);
}

.stat-number {
    font-size: 2rem !important;
    font-weight: 700 !important;
    line-height: 1.2;
    margin-bottom: 0.25rem;
    color: #ffffff !important;
}

.stat-label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #ffffff !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Paper Cards */
.paper-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.75rem 0;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.paper-card:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.paper-title {
    font-weight: 600;
    color: var(--text-primary) !important;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}

.paper-meta {
    color: var(--text-secondary) !important;
    font-size: 0.9rem;
    margin-bottom: 0.35rem;
}

.paper-meta strong {
    color: var(--text-primary) !important;
    font-weight: 600;
}

/* Download buttons */
.download-btn {
    background: var(--primary) !important;
    color: #ffffff !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    display: inline-block !important;
    margin-top: 0.75rem !important;
    text-decoration: none !important;
    border: none !important;
    cursor: pointer !important;
    width: 100% !important;
    text-align: center !important;
    transition: all 0.2s ease !important;
}

.download-btn:hover {
    background: var(--primary-dark) !important;
}

/* Input fields */
input, textarea, select {
    color: var(--text-primary) !important;
    background: #ffffff !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: 6px !important;
    padding: 0.6rem !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
}

input:focus, textarea:focus, select:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    outline: none !important;
}

/* Buttons */
button {
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.2rem !important;
}

button.primary {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: #ffffff !important;
    border: none !important;
}

button.primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
}

button.secondary {
    background: #ffffff !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-dark) !important;
}

button.secondary:hover {
    background: var(--surface) !important;
}

/* Tabs */
.tabs {
    border-radius: 8px !important;
    overflow: hidden !important;
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 1rem !important;
}

.tab-nav {
    background: var(--surface) !important;
    padding: 0.5rem !important;
    border-bottom: 1px solid var(--border) !important;
}

.tab-nav button {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.8rem !important;
    background: transparent !important;
    border: none !important;
    font-size: 0.9rem !important;
}

.tab-nav button.selected {
    background: #ffffff !important;
    color: var(--primary) !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
}

/* Tab Content */
.tab-content {
    padding: 1rem !important;
    background: #ffffff !important;
}

.tab-content textarea {
    color: var(--text-primary) !important;
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.75rem !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
    font-family: 'Monaco', 'Menlo', monospace !important;
}

/* Alerts */
.alert {
    padding: 0.75rem 1rem;
    border-radius: 6px;
    margin: 0.75rem 0;
    font-weight: 500;
    font-size: 0.95rem;
    border: 1px solid transparent;
}

.alert-success {
    background: #dcfce7;
    color: #166534 !important;
    border-color: #86efac;
}

.alert-info {
    background: #dbeafe;
    color: #1e40af !important;
    border-color: #93c5fd;
}

.alert-error {
    background: #fee2e2;
    color: #991b1b !important;
    border-color: #fecaca;
}

/* Example topic buttons */
.example-btn {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    width: 100% !important;
    margin: 0.25rem 0 !important;
}

.example-btn:hover {
    background: #ffffff !important;
    border-color: var(--primary) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

/* History Section - FIXED: All text now black */
.history-section {
    margin-top: 2rem;
    padding: 1rem;
    background: var(--surface);
    border-radius: 10px;
    border: 1px solid var(--border);
}

.history-container {
    max-height: 300px;
    overflow-y: auto;
    padding-right: 0.5rem;
}

.history-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem;
    margin: 0.5rem 0;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
}

.history-item:hover {
    border-color: var(--primary);
    transform: translateX(4px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.history-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #2563eb10, #7c3aed10);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    color: var(--text-primary) !important;
}

.history-content {
    flex: 1;
}

.history-topic {
    font-weight: 600;
    color: #000000 !important;  /* Force black */
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
}

.history-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.8rem;
    color: #000000 !important;  /* Force black */
}

.history-time, .history-papers, .history-status {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: #000000 !important;  /* Force black */
}

.history-time span, .history-papers span, .history-status span {
    color: #000000 !important;  /* Force black */
}

.history-arrow {
    color: var(--border-dark);
    font-size: 1.2rem;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.history-item:hover .history-arrow {
    opacity: 1;
    color: var(--primary);
}

.clear-history-btn {
    background: #ffffff !important;
    color: #000000 !important;  /* Force black */
    border: 1px solid var(--border) !important;
    padding: 0.4rem 1rem !important;
    font-size: 0.85rem !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.clear-history-btn:hover {
    background: #fee2e2 !important;
    border-color: var(--danger) !important;
    color: #000000 !important;  /* Force black on hover */
}

/* Footer */
.footer {
    margin-top: 2rem;
    padding: 1rem;
    background: var(--surface);
    border-radius: 8px;
    text-align: center;
    border: 1px solid var(--border);
}

.footer p {
    color: var(--text-secondary) !important;
    margin: 0.25rem 0;
    font-size: 0.85rem;
}

/* Header section */
.header-container {
    text-align: center;
    margin-bottom: 1.5rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f0f9ff, #e6f0ff);
    border: 1px solid var(--border);
    border-radius: 10px;
}

.header-subtitle {
    color: var(--text-secondary) !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    margin-top: 0.25rem !important;
}

/* Status area */
.status-area {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem;
    margin: 1rem 0;
    font-size: 0.95rem;
}

/* Group boxes */
.gr-group {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    background: #ffffff !important;
}

/* JavaScript for clear history */
.js-clear-history {
    display: none;
}
"""

# Add JavaScript for clear history functionality
CUSTOM_JS = """
function clearHistory() {
    // Find the hidden clear history button and click it
    const buttons = document.querySelectorAll('button');
    for (let button of buttons) {
        if (button.innerText.includes('🗑️ Clear History')) {
            // Trigger the Gradio event
            const event = new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true
            });
            button.dispatchEvent(event);
            break;
        }
    }
    return false;
}

// Make function globally available
window.clearHistory = clearHistory;
"""

# [All helper functions remain exactly the same as before]
def load_papers_from_dataset() -> List[Dict]:
    """Load papers from cleaned_dataset.json"""
    if DATASET_FILE.exists():
        try:
            with open(DATASET_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def get_paper_display_info() -> Tuple[List[Dict], int, int]:
    """Get papers and statistics"""
    papers = load_papers_from_dataset()
    
    # Count PDFs downloaded
    pdf_count = 0
    for paper in papers:
        paper_id = paper.get('paperId', '')
        if paper_id and (PDFS_DIR / f"{paper_id}.pdf").exists():
            pdf_count += 1
    
    return papers, len(papers), pdf_count

def create_paper_card(paper: Dict) -> str:
    """Create HTML for a paper card with working download button"""
    paper_id = paper.get('paperId', 'N/A')
    title = paper.get('title', 'No Title')
    authors = paper.get('authors', [])
    year = paper.get('year', 'Unknown')
    
    # Format authors
    if isinstance(authors, list):
        author_str = ', '.join([str(a) for a in authors[:3]])
        if len(authors) > 3:
            author_str += ' et al.'
    else:
        author_str = str(authors)
    
    # Check if PDF exists locally
    pdf_path = PDFS_DIR / f"{paper_id}.pdf"
    pdf_button = ""
    
    if pdf_path.exists():
        try:
            with open(pdf_path, 'rb') as f:
                pdf_data = base64.b64encode(f.read()).decode('utf-8')
            
            pdf_button = f'''
            <a href="data:application/pdf;base64,{pdf_data}" 
               download="{paper_id}.pdf"
               style="text-decoration: none;">
                <button class="download-btn" style="background: #059669 !important;">
                    📥 Download PDF: {title[:50]}...
                </button>
            </a>
            '''
        except:
            pdf_button = '''
            <button class="download-btn" style="background: #94a3b8 !important;" disabled>
                ⏳ PDF Error
            </button>
            '''
    else:
        # Check if open access PDF URL exists
        if paper.get('openAccessPdf'):
            pdf_url = paper['openAccessPdf']
            pdf_button = f'''
            <a href="{pdf_url}" target="_blank" style="text-decoration: none;">
                <button class="download-btn" style="background: #7c3aed !important;">
                    🔗 Open Access PDF
                </button>
            </a>
            '''
        else:
            pdf_button = '''
            <button class="download-btn" style="background: #94a3b8 !important;" disabled>
                ⏳ PDF Not Available
            </button>
            '''
    
    return f'''
    <div class="paper-card">
        <div class="paper-title">📄 {title}</div>
        <div class="paper-meta"><strong>Authors:</strong> {author_str}</div>
        <div class="paper-meta"><strong>Year:</strong> {year}</div>
        <div class="paper-meta"><strong>Paper ID:</strong> {paper_id}</div>
        {pdf_button}
    </div>
    '''

def generate_papers_html() -> str:
    """Generate HTML for all papers"""
    papers, _, _ = get_paper_display_info()
    
    if not papers:
        return '''
        <div class="alert alert-info">
            No papers fetched yet. Run an analysis to fetch papers.
        </div>
        '''
    
    html = "<h2>📚 Fetched Papers</h2>"
    for paper in papers[:10]:  # Show up to 10 papers
        html += create_paper_card(paper)
    
    return html

def generate_stats_html() -> str:
    """Generate HTML for statistics cards"""
    papers, total_papers, pdf_count = get_paper_display_info()
    
    # Count analyses generated
    analyses_count = len(list(OUTPUT_DIR.glob("*.txt")))
    
    return f'''
    <div class="stat-container">
        <div class="stat-card stat-card-1">
            <div class="stat-number">{total_papers}</div>
            <div class="stat-label">TOTAL PAPERS</div>
        </div>
        <div class="stat-card stat-card-2">
            <div class="stat-number">{pdf_count}</div>
            <div class="stat-label">PDFS DOWNLOADED</div>
        </div>
        <div class="stat-card stat-card-3">
            <div class="stat-number">{analyses_count}</div>
            <div class="stat-label">ANALYSES GENERATED</div>
        </div>
    </div>
    '''

def run_analysis(
    topic: str,
    num_papers: int,
    extra_context: str,
    progress: gr.Progress = gr.Progress()
) -> Tuple[str, str, str, str, str, str, str]:
    """Run the full pipeline with progress tracking"""
    
    if not topic:
        return (
            "",
            "",
            "",
            '<div class="alert alert-error">❌ Please enter a research topic</div>',
            generate_papers_html(),
            generate_stats_html(),
            generate_history_html()
        )
    
    try:
        progress(0.1, desc="🔍 Initializing research pipeline...")
        
        # Call the main pipeline function
        full_paper, similarity_report, critique, status = run_pipeline_logic(
            topic,
            num_papers,
            extra_context
        )
        
        progress(0.6, desc="📊 Processing results...")
        
        # Handle None or empty values
        if similarity_report is None or similarity_report == "":
            similarity_report = "No similarity report available. This may happen if fewer than 2 papers were successfully processed."
        
        if critique is None or critique == "":
            critique = "No critique available for the generated paper."
        
        if full_paper is None or full_paper == "":
            full_paper = "No paper was generated. Please check the status message for details."
        
        progress(0.9, desc="✅ Finalizing...")
        
        # Generate success message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success_msg = f'<div class="alert alert-success">✅ Analysis completed at {timestamp}<br>{status}</div>'
        
        # Save to history
        save_to_history(topic, num_papers, timestamp, "completed")
        
        progress(1.0, desc="Complete!")
        
        return (
            full_paper,
            similarity_report,
            critique,
            success_msg,
            generate_papers_html(),
            generate_stats_html(),
            generate_history_html()
        )
        
    except Exception as e:
        error_msg = f'<div class="alert alert-error">❌ Error: {str(e)}</div>'
        
        # Save failed attempt to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_history(topic, num_papers, timestamp, "failed")
        
        return (
            "Error occurred during paper generation.",
            "Similarity analysis unavailable due to error.",
            "Critique unavailable due to error.",
            error_msg,
            generate_papers_html(),
            generate_stats_html(),
            generate_history_html()
        )

def generate_revision(
    original_paper: str,
    critique_text: str
) -> Tuple[str, str]:
    """Generate revised version of the paper"""
    
    if not original_paper or original_paper.startswith("Error"):
        return "Please generate a paper first.", ""
    
    if not critique_text or critique_text.startswith("No critique"):
        return "Please generate a critique first.", ""
    
    try:
        revised = revise_generated_paper(original_paper, critique_text)
        
        # Save revised paper
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        revised_path = OUTPUT_DIR / f"revised_paper_{timestamp}.txt"
        
        with open(revised_path, 'w', encoding='utf-8') as f:
            f.write(revised)
        
        # Create download link
        with open(revised_path, 'rb') as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')
        
        download_link = f'''
        <a href="data:text/plain;charset=utf-8;base64,{file_data}" 
           download="revised_paper_{timestamp}.txt"
           style="text-decoration: none;">
            <button class="download-btn" style="background: #7c3aed !important;">
                📥 Download Revised Paper
            </button>
        </a>
        '''
        
        return revised, download_link
        
    except Exception as e:
        return f"Revision failed: {str(e)}", ""

def create_download_link(content: str, filename: str) -> str:
    """Create a download link for content"""
    if not content or content.startswith("Error"):
        return ""
    
    try:
        # Encode content
        content_bytes = content.encode('utf-8')
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')
        
        return f'''
        <a href="data:text/plain;charset=utf-8;base64,{content_b64}" 
           download="{filename}"
           style="text-decoration: none;">
            <button class="download-btn" style="background: #2563eb !important;">
                📥 Download {filename}
            </button>
        </a>
        '''
    except:
        return ""

def clear_all() -> Tuple:
    """Clear all inputs and outputs"""
    return (
        "",  # topic
        5,   # num_papers
        "",  # extra context
        "",  # generated paper
        "",  # similarity report
        "",  # critique
        '<div class="alert alert-info">✅ Cleared. Ready for new analysis.</div>',  # status
        "",  # revised paper
        generate_papers_html(),  # papers display
        generate_stats_html(),  # stats display
        "",  # paper download link
        "",  # revised download link
        generate_history_html()  # history display
    )

# ==========================================================
# BUILD GRADIO INTERFACE
# ==========================================================

# Create the Gradio interface
with gr.Blocks(css=CUSTOM_CSS, theme=gr.themes.Default(), head=CUSTOM_JS) as app:
    
    # Header Section
    gr.HTML("""
    <div class="header-container">
        <h1>📚 AI Research Paper Review System</h1>
        <p class="header-subtitle">Automated paper fetching, analysis, and quality assessment powered by advanced AI</p>
    </div>
    """)
    
    # Statistics Section
    stats_display = gr.HTML(generate_stats_html())
    
    # Main Two-Column Layout
    with gr.Row():
        # LEFT COLUMN - Research Configuration
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("## 🔬 Research Configuration")
            
            with gr.Group():
                topic_input = gr.Textbox(
                    label="Research Topic",
                    placeholder="e.g., 'Machine Learning in Healthcare', 'Quantum Computing'...",
                    lines=2,
                    elem_id="topic-input"
                )
                
                num_papers_slider = gr.Slider(
                    label="Number of Papers to Fetch",
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    elem_id="num-papers"
                )
                
                extra_context_input = gr.Textbox(
                    label="Additional Context (Optional)",
                    placeholder="Add specific requirements, focus areas, or findings...",
                    lines=3
                )
            
            with gr.Row():
                run_btn = gr.Button(
                    "🚀 Start Analysis",
                    variant="primary",
                    size="lg"
                )
                clear_btn = gr.Button(
                    "🔄 Clear All",
                    variant="secondary",
                    size="lg"
                )
            
            # Status Message Area
            status_output = gr.HTML(
                value='<div class="alert alert-info">✅ System Ready — Enter a research topic to begin.</div>'
            )
            
            # Fetched Papers Display Section
            gr.Markdown("---")
            papers_display = gr.HTML(generate_papers_html())
            
            # Refresh Papers Button
            refresh_btn = gr.Button(
                "🔄 Refresh Papers List",
                variant="secondary",
                size="sm"
            )
            
            # History Section
            gr.Markdown("## 📜 Recent Analyses")
            history_display = gr.HTML(generate_history_html())
            
            # Clear History Button (visible for Gradio event, but hidden by CSS)
            clear_history_btn = gr.Button("🗑️ Clear History", visible=True, elem_classes="js-clear-history")
        
        # RIGHT COLUMN - Results Section
        with gr.Column(scale=2):
            gr.Markdown("## 📊 Analysis Results")
            
            # Tabs for results
            with gr.Tabs():
                with gr.TabItem("📝 Generated Paper"):
                    paper_output = gr.Textbox(
                        label="Generated Research Paper",
                        lines=20,
                        interactive=False
                    )
                    paper_download_link = gr.HTML("")  # For download button
                
                with gr.TabItem("📊 Similarity Report"):
                    similarity_output = gr.Textbox(
                        label="Cross-Paper Similarity Analysis",
                        lines=20,
                        interactive=False,
                        value="Run an analysis to see similarity reports."
                    )
                
                with gr.TabItem("🔍 Quality Review"):
                    critique_output = gr.Textbox(
                        label="AI Critique & Suggestions",
                        lines=20,
                        interactive=False,
                        value="Run an analysis to see quality reviews."
                    )
            
            # Revision Section
            gr.Markdown("## 🔄 Paper Revision")
            with gr.Row():
                revise_btn = gr.Button(
                    "✨ Generate Revised Version",
                    variant="primary",
                    size="lg"
                )
            
            revised_paper_output = gr.Textbox(
                label="Revised Paper",
                lines=10,
                interactive=False
            )
            revised_download_link = gr.HTML("")  # For revised download button
    
    # Example Topics Section
    gr.Markdown("## 📚 Example Topics")
    gr.Markdown("*Click any example to auto-fill the form:*")
    
    with gr.Row():
        for i, example in enumerate(EXAMPLE_TOPICS):
            btn = gr.Button(
                example[0][:30] + "..." if len(example[0]) > 30 else example[0],
                elem_id=f"example_{i}",
                size="sm"
            )
            btn.click(
                fn=lambda topic=example[0], num=example[1], context=example[2]: (topic, num, context),
                inputs=[],
                outputs=[topic_input, num_papers_slider, extra_context_input]
            )
    
    # Footer
    gr.HTML("""
    <div class="footer">
        <p><strong>⚡ Powered by Semantic Scholar & arXiv</strong> | 🔒 Secure Processing</p>
        <p>© 2024 AI Research Paper Review System | Version 2.0 with History</p>
    </div>
    """)
    
    # Hidden states for file paths
    current_paper = gr.State("")
    current_critique = gr.State("")

    # ==========================================================
    # EVENT HANDLERS
    # ==========================================================
    
    # Run Analysis
    run_btn.click(
        fn=run_analysis,
        inputs=[topic_input, num_papers_slider, extra_context_input],
        outputs=[
            paper_output,
            similarity_output,
            critique_output,
            status_output,
            papers_display,
            stats_display,
            history_display
        ]
    ).then(
        fn=lambda paper, critique: (paper, critique),
        inputs=[paper_output, critique_output],
        outputs=[current_paper, current_critique]
    ).then(
        fn=lambda paper: create_download_link(paper, "generated_paper.txt"),
        inputs=[paper_output],
        outputs=[paper_download_link]
    )
    
    # Generate Revision
    revise_btn.click(
        fn=generate_revision,
        inputs=[current_paper, current_critique],
        outputs=[revised_paper_output, revised_download_link]
    ).then(
        fn=lambda: generate_stats_html(),
        outputs=[stats_display]
    )
    
    # Clear All
    clear_btn.click(
        fn=clear_all,
        outputs=[
            topic_input,
            num_papers_slider,
            extra_context_input,
            paper_output,
            similarity_output,
            critique_output,
            status_output,
            revised_paper_output,
            papers_display,
            stats_display,
            paper_download_link,
            revised_download_link,
            history_display
        ]
    )
    
    # Refresh Papers Display
    refresh_btn.click(
        fn=lambda: (generate_papers_html(), generate_stats_html()),
        outputs=[papers_display, stats_display]
    )
    
    # Clear History - FIXED: Now working
    clear_history_btn.click(
        fn=clear_history,
        outputs=[history_display]
    )
    
    # Auto-create download links when paper changes
    paper_output.change(
        fn=lambda paper: create_download_link(paper, "generated_paper.txt"),
        inputs=[paper_output],
        outputs=[paper_download_link]
    )
    
    # Update current paper when it changes
    paper_output.change(
        fn=lambda paper: paper,
        inputs=[paper_output],
        outputs=[current_paper]
    )
    
    critique_output.change(
        fn=lambda critique: critique,
        inputs=[critique_output],
        outputs=[current_critique]
    )

# ==========================================================
# LAUNCH THE APP
# ==========================================================
if __name__ == "__main__":
    print("="*70)
    print("📚 AI Research Paper Review System")
    print("="*70)
    print("\n🚀 Starting server...")
    print("📱 Local URL: http://127.0.0.1:7860")
    print("\n✨ Features:")
    print("   • Complete integration with main.py backend")
    print("   • Automatic paper fetching from Semantic Scholar & arXiv")
    print("   • Real-time paper display with working PDF downloads")
    print("   • TF-IDF similarity analysis")
    print("   • AI-powered paper generation and critique")
    print("   • Paper revision functionality")
    print("   • Export all generated content")
    print("   • 📜 Analysis history with one-click reload")
    print("="*70)
    print("\n📁 Data directories:")
    print(f"   • PDFs: {PDFS_DIR.absolute()}")
    print(f"   • Outputs: {OUTPUT_DIR.absolute()}")
    print(f"   • Exports: {EXPORTS_DIR.absolute()}")
    print(f"   • History: {HISTORY_FILE.absolute()}")
    print("="*70)
    
    # Launch the app
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True
    )