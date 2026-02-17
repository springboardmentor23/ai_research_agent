import os
import re
import json
import tempfile
import unicodedata
from typing import List, Tuple, Optional

import gradio as gr
from fpdf import FPDF

from fetch_paper import fetch_papers
from pdf_downloder import download_pdf
from text_extraction import extract_text_from_pdf
from key_phrases import extract_key_findings
from similarity import compute_similarity
from generate_paper import generate_synthesized_paper


DATA_DIR = "data"
METADATA_DIR = os.path.join(DATA_DIR, "metadata")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
TEXT_DIR = os.path.join(DATA_DIR, "texts")
FINDINGS_DIR = os.path.join(DATA_DIR, "dist_texts")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

os.makedirs(METADATA_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(FINDINGS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _text_to_ascii(text: str) -> str:
    """Convert Unicode text to ASCII so FPDF's default font can render it (e.g. š -> s)."""
    nfd = unicodedata.normalize("NFKD", text)
    return nfd.encode("ascii", "ignore").decode("ascii")


def _strip_markdown_bold(text: str) -> str:
    """Remove Markdown bold markers (**text** -> text) so papers display and export cleanly."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


# Section headers to detect for formatted PDF (case-insensitive, stripped of numbering).
_SECTION_HEADERS = (
    "title page", "abstract", "introduction", "method", "methods", "methodology",
    "results", "discussion", "conclusion", "references", "reference",
)


def _is_section_header(line: str) -> bool:
    """True if line looks like a section title (e.g. 'Abstract', '1. Methods')."""
    s = line.strip()
    if not s or len(s) > 80:
        return False
    # Remove leading numbering "1. ", "2. ", etc.
    t = s.lstrip("0123456789.).- ")
    return t.lower() in _SECTION_HEADERS or t.lower().rstrip("s") in _SECTION_HEADERS


def _make_pdf_from_text(text: str, filename: str) -> str:
    """
    Create a well-formatted PDF: margins, section headings in bold, spacing, page numbers.
    Saves under OUTPUT_DIR/filename. Returns the absolute file path.
    """

    class FormattedPDF(FPDF):
        def footer(self):
            self.set_y(-18)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")

    safe_text = _text_to_ascii(text)
    lines = safe_text.splitlines()

    pdf = FormattedPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.set_margins(left=28, top=28, right=28)
    pdf.add_page()
    pdf.set_font("Helvetica", "", size=11)
    line_height_body = 5.5
    line_height_heading = 8

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            pdf.ln(3)
            i += 1
            continue

        if _is_section_header(line):
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, line_height_heading, stripped)
            pdf.set_font("Helvetica", "", size=11)
            pdf.ln(2)
            i += 1
            continue

        pdf.multi_cell(0, line_height_body, line)
        i += 1

    out_path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(out_path)
    return out_path


def search_papers(topic: str, max_papers: int) -> Tuple[List[str], List[dict]]:
    """
    Search Semantic Scholar for papers and return (titles, raw paper dicts).
    """
    max_papers = max(1, min(int(max_papers), 6))
    papers = fetch_papers(topic, limit=max_papers)
    titles = [
        f"{p.get('title', 'Untitled')} (Year: {p.get('year', 'N/A')})"
        for p in papers
    ]
    return titles, papers


def _save_metadata(paper: dict) -> str:
    paper_id = paper.get("paperId")
    if not paper_id:
        return ""

    metadata = {
        "paperId": paper_id,
        "title": paper.get("title"),
        "authors": [a["name"] for a in paper.get("authors", [])],
        "year": paper.get("year"),
        "paper_url": paper.get("url"),
    }

    meta_path = os.path.join(METADATA_DIR, f"{paper_id}.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return paper_id


def download_and_process_selected(
    topic: str,
    max_papers: int,
    selected_indices: List[int],
    papers_json: str,
) -> Tuple[str, List[str]]:
    """
    Download PDFs and extract text for selected papers.
    Returns a status message and a list of file paths for download.
    """
    if not papers_json:
        return "No papers loaded. Please search first.", []

    try:
        papers = json.loads(papers_json)
    except json.JSONDecodeError:
        return "Internal error: could not decode papers list.", []

    if not selected_indices:
        return "No papers selected.", []

    downloaded_files = []
    messages = []

    for idx in selected_indices:
        if idx < 0 or idx >= len(papers):
            continue
        paper = papers[idx]
        paper_id = _save_metadata(paper)
        if not paper_id:
            messages.append("Skipping a paper without paperId.")
            continue

        pdf_url = paper.get("openAccessPdf", {}).get("url")
        if not pdf_url:
            messages.append(f"No PDF available for paper id {paper_id}.")
            continue

        pdf_path = download_pdf(pdf_url, paper_id)
        if not pdf_path:
            messages.append(f"Failed to download PDF for paper id {paper_id}.")
            continue

        downloaded_files.append(pdf_path)
        text_path = extract_text_from_pdf(pdf_path, paper_id)
        if text_path:
            messages.append(f"Downloaded and extracted text for {paper.get('title', 'Untitled')}.")
        else:
            messages.append(f"Downloaded PDF but failed to extract text for {paper.get('title', 'Untitled')}.")

    if not downloaded_files:
        return " | ".join(messages) or "No files downloaded.", []

    return " | ".join(messages), downloaded_files


def run_key_phrase_extraction() -> str:
    extract_key_findings()
    return "Key findings extracted for available texts."


def show_similarity_matrix() -> str:
    matrix, doc_names = compute_similarity()
    if matrix is None or not doc_names:
        return "Not enough documents for comparison. Make sure you have extracted key findings."

    # Build a simple text table
    lines = []
    n = len(doc_names)
    lines.append("Cosine similarity between papers:\n")
    for i in range(n):
        for j in range(i + 1, n):
            lines.append(f"{doc_names[i]} vs {doc_names[j]} -> {matrix[i][j]:.3f}")
    return "\n".join(lines)


def list_key_findings() -> List[Tuple[str, str]]:
    """
    Return a list of (paper_id, findings_text).
    """
    results = []
    for filename in os.listdir(FINDINGS_DIR):
        if not filename.endswith("_findings.txt"):
            continue
        path = os.path.join(FINDINGS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            findings = f.read().strip()
        paper_id = filename.replace("_findings.txt", "")
        results.append((paper_id, findings))
    return results


def generate_paper_ui() -> str:
    """
    Wrapper around generate_synthesized_paper() that also writes to OUTPUT_DIR.
    """
    # Check that we have key findings before calling Groq
    findings_list = list_key_findings()
    if not findings_list:
        return (
            "[Error] No key findings found. Please do this first:\n\n"
            "1. In tab 'Search & Download Papers': search for a topic, select papers, and click 'Download Selected & Extract Text'.\n"
            "2. In tab 'Compare Papers': click 'Extract Key Findings'.\n"
            "3. Then come back here and click 'Generate Synthesized Paper' again."
        )
    try:
        paper = generate_synthesized_paper()
        paper = _strip_markdown_bold(paper)
        out_path = os.path.join(OUTPUT_DIR, "synthesized_paper.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(paper)
        return paper
    except Exception as e:
        return f"[Error] Could not generate paper:\n\n{type(e).__name__}: {e}"


def revise_paper_ui(current_paper: str, user_feedback: str) -> str:
    """
    Simple revision: call Groq again with the current paper and user feedback.
    Implemented as a lightweight refinement prompt.
    """
    if not current_paper.strip():
        return "No paper to revise. Please generate a paper first."

    from groq import Groq

    # Reuse the same key resolution logic as generate_paper.py:
    try:
        from app_secrets import GROQ_API_KEY  # type: ignore
    except ImportError:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    if not GROQ_API_KEY:
        return (
            "GROQ_API_KEY is not set. Please create an 'app_secrets.py' file with "
            "GROQ_API_KEY = 'your_key' or set the GROQ_API_KEY environment variable."
        )

    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
You are an academic editor.

Here is a draft research paper:

{current_paper}

The user has the following feedback and requested changes:
{user_feedback}

Please produce a revised version of the paper that:
- Keeps the structure and academic tone.
- Only changes the content as needed to reflect the feedback.
- Do NOT use Markdown formatting (e.g. **bold**). Use plain text only.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    revised = response.choices[0].message.content
    revised = _strip_markdown_bold(revised)

    out_path = os.path.join(OUTPUT_DIR, "synthesized_paper_revised.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(revised)

    return revised


with gr.Blocks(title="AI Research Agent") as demo:
    gr.Markdown("## AI Research Agent\nSearch, compare, and synthesize research papers.")

    with gr.Tab("1. Search & Download Papers"):
        topic = gr.Textbox(label="Research topic or paper name", placeholder="e.g., Machine learning in healthcare")
        max_papers = gr.Slider(label="Max papers", minimum=1, maximum=6, value=3, step=1)
        search_btn = gr.Button("Search Papers")

        papers_state = gr.State("")  # JSON-encoded list of papers

        titles_output = gr.CheckboxGroup(label="Select papers to process", choices=[])
        search_status = gr.Markdown()

        download_btn = gr.Button("Download Selected & Extract Text")
        download_status = gr.Markdown()
        download_files = gr.Files(label="Downloaded PDFs")

        def on_search(topic_in, max_papers_in):
            titles, papers = search_papers(topic_in, max_papers_in)
            return gr.update(choices=[str(i) + ": " + t for i, t in enumerate(titles)]), json.dumps(papers), f"Found {len(titles)} papers."

        search_btn.click(
            fn=on_search,
            inputs=[topic, max_papers],
            outputs=[titles_output, papers_state, search_status],
        )

        def on_download(selected, papers_json):
            # selected entries look like "0: Title..."
            indices = []
            for s in selected or []:
                try:
                    idx = int(s.split(":", 1)[0])
                    indices.append(idx)
                except ValueError:
                    continue
            status, files = download_and_process_selected("", 0, indices, papers_json)
            return status, files

        download_btn.click(
            fn=on_download,
            inputs=[titles_output, papers_state],
            outputs=[download_status, download_files],
        )

    with gr.Tab("2. Compare Papers"):
        gr.Markdown("Compute similarity between papers based on extracted key findings.")
        extract_btn = gr.Button("Extract Key Findings")
        extract_status = gr.Markdown()

        similarity_btn = gr.Button("Show Similarity")
        similarity_output = gr.Textbox(label="Similarity matrix", lines=10)

        extract_btn.click(fn=run_key_phrase_extraction, inputs=None, outputs=extract_status)
        similarity_btn.click(fn=show_similarity_matrix, inputs=None, outputs=similarity_output)

    with gr.Tab("3. View Key Findings"):
        refresh_findings_btn = gr.Button("Refresh Key Findings")
        findings_output = gr.Dataframe(
            headers=["Paper ID", "Key Findings"],
            datatype=["str", "str"],
            row_count=(0, "dynamic"),
        )

        def on_refresh_findings():
            data = list_key_findings()
            # Dataframe expects list of rows
            return data

        refresh_findings_btn.click(fn=on_refresh_findings, inputs=None, outputs=findings_output)

    with gr.Tab("4. Generate & Revise Paper"):
        gr.Markdown("**Generate:** Click the button below. The synthesized paper will appear in the text area and you can download it as PDF.")
        generate_btn = gr.Button("Generate Synthesized Paper")
        generated_paper = gr.Textbox(
            label="Generated paper (shown on website)",
            placeholder="Generated paper will appear here after you click the button above.",
            lines=24,
            max_lines=30,
        )
        download_generated = gr.File(label="Download generated paper (PDF)")

        gr.Markdown("---\n**Revise:** Add your feedback below, then click Revise. The revised paper will appear and you can download it as PDF.")
        feedback_box = gr.Textbox(label="Your feedback / suggested changes", lines=5)
        revise_btn = gr.Button("Revise Paper")
        revised_paper = gr.Textbox(
            label="Revised paper (shown on website)",
            placeholder="Revised paper will appear here after you click Revise.",
            lines=24,
            max_lines=30,
        )
        download_revised = gr.File(label="Download revised paper (PDF)")

        def on_generate():
            try:
                paper = generate_paper_ui()
                if paper.strip().startswith("[Error]"):
                    return paper, None  # Show message in textbox, no PDF
                # Save text for reference
                txt_path = os.path.join(OUTPUT_DIR, "synthesized_paper.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(paper)
                pdf_path = _make_pdf_from_text(paper, "synthesized_paper.pdf")
                return paper, pdf_path
            except Exception as e:
                msg = f"[Error] Something went wrong:\n\n{type(e).__name__}: {e}"
                return msg, None

        generate_btn.click(
            fn=on_generate,
            inputs=None,
            outputs=[generated_paper, download_generated],
        )

        def on_revise(paper_text, feedback_text):
            try:
                revised = revise_paper_ui(paper_text, feedback_text)
                if revised.strip().startswith("No paper to revise") or revised.strip().startswith("GROQ_API_KEY"):
                    return revised, None
                # Save revised text for reference
                txt_path = os.path.join(OUTPUT_DIR, "synthesized_paper_revised.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(revised)
                pdf_path = _make_pdf_from_text(revised, "synthesized_paper_revised.pdf")
                return revised, pdf_path
            except Exception as e:
                msg = f"[Error] Could not revise paper:\n\n{type(e).__name__}: {e}"
                return msg, None

        revise_btn.click(
            fn=on_revise,
            inputs=[generated_paper, feedback_box],
            outputs=[revised_paper, download_revised],
        )


if __name__ == "__main__":
    # server_name="127.0.0.1" for local access. Port 7861 (7860 often in use)
    # Open in browser: http://127.0.0.1:7861
    demo.launch(server_name="127.0.0.1", server_port=7861)

