import gradio as gr
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import shutil

# ✅ PROFESSIONAL IEEE-LIKE PDF
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Frame, PageTemplate, FrameBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors

from src.paper_search.hybrid_search import fetch_papers_hybrid
from src.paper_search.pdf_downloader import download_pdf
from src.paper_search.dataset_utils import prepare_cleaned_dataset, save_cleaned_dataset

from src.text_extraction.pdf_text_extractor import extract_text_from_all_pdfs
from src.text_extraction.section_extractor import process_all_text_files
from src.text_extraction.tfidf_similarity import extract_key_findings, compare_papers_tfidf
from src.text_extraction.validation import validate_section_files

from src.draft_generator.pattern_extractor import extract_common_patterns
from src.draft_generator.draft_generator import generate_draft
from src.draft_generator.gpt_client import generate_with_gemini

from src.ui_gradio.quality_evaluator import evaluate_quality


DATASET_PATH = "data/datasets/cleaned_dataset.json"
SIMILARITY_PATH = "data/datasets/similarity_results.json"
FETCHED_PAPERS_PATH = "data/datasets/fetched_papers.json"

PDF_FOLDER = "pdfs"
TEXT_FOLDER = "data/extracted_text"
SECTION_FOLDER = "data/section_wise_text"
FINAL_REPORT_FOLDER = "data/final_reports"


# ---------------- SETUP ----------------
def setup_folders():
    os.makedirs("data/datasets", exist_ok=True)
    os.makedirs(PDF_FOLDER, exist_ok=True)
    os.makedirs(TEXT_FOLDER, exist_ok=True)
    os.makedirs(SECTION_FOLDER, exist_ok=True)
    os.makedirs(FINAL_REPORT_FOLDER, exist_ok=True)


def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)


# ---------------- PDF URL NORMALIZER ----------------
def normalize_pdf_url(url: str):
    if not url:
        return None

    url = url.strip()

    if "arxiv.org/abs/" in url:
        return url.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"

    if "arxiv.org/pdf/" in url and not url.endswith(".pdf"):
        return url + ".pdf"

    return url


# ---------------- FETCH PAPERS ----------------
def fetch_papers(topic, limit):
    setup_folders()

    if not topic.strip():
        topic = "machine learning"

    search_attempts = [
        topic,
        " ".join(topic.split()[:3]),
        topic.replace("using", "").replace("system", ""),
        topic.replace("prediction", "").replace("classification", ""),
        "artificial intelligence",
        "machine learning"
    ]

    all_papers = []
    used_attempt = topic

    for attempt in search_attempts:
        try:
            papers = fetch_papers_hybrid(attempt)

            if papers:
                used_attempt = attempt
                for p in papers:
                    if p not in all_papers:
                        all_papers.append(p)

            if len(all_papers) >= limit:
                break

        except Exception:
            continue

    if len(all_papers) == 0:
        return "❌ No papers found even after fallback.", pd.DataFrame()

    all_papers = all_papers[:limit]

    with open(FETCHED_PAPERS_PATH, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, indent=2)

    rows = []
    for idx, paper in enumerate(all_papers, start=1):
        title = paper.get("title", "Untitled Paper")
        year = paper.get("year", "N/A")
        venue = paper.get("venue", "N/A")
        rows.append([idx, title, year, venue])

    df = pd.DataFrame(rows, columns=["#", "Paper Title", "Year", "Source"])

    msg = f"✅ Successfully fetched {len(all_papers)} papers."
    if used_attempt != topic:
        msg += f" (fallback search used: '{used_attempt}')"

    return msg, df


# ---------------- DOWNLOAD PAPERS ----------------
def download_papers(topic):
    setup_folders()

    if not os.path.exists(FETCHED_PAPERS_PATH):
        return "❌ Fetch papers first.", []

    with open(FETCHED_PAPERS_PATH, "r", encoding="utf-8") as f:
        papers = json.load(f)

    if not papers:
        return "❌ No papers saved. Fetch again.", []

    topic_safe = topic.replace("/", "_").replace(" ", "_").strip()
    if not topic_safe:
        topic_safe = "papers"

    topic_folder = os.path.join(PDF_FOLDER, topic_safe)
    os.makedirs(topic_folder, exist_ok=True)

    downloaded_files = []
    downloaded_count = 0
    skipped_count = 0

    for idx, paper in enumerate(papers, start=1):

        pdf_url = None

        if paper.get("openAccessPdf") and paper["openAccessPdf"].get("url"):
            pdf_url = paper["openAccessPdf"]["url"]
        elif paper.get("pdfUrl"):
            pdf_url = paper["pdfUrl"]
        elif paper.get("url"):
            pdf_url = paper["url"]

        pdf_url = normalize_pdf_url(pdf_url)

        if not pdf_url:
            skipped_count += 1
            continue

        save_path = os.path.join(topic_folder, f"{topic_safe}_{idx}.pdf")

        try:
            download_pdf(pdf_url, save_path)

            if os.path.exists(save_path) and os.path.getsize(save_path) > 5000:
                downloaded_files.append(os.path.abspath(save_path))
                downloaded_count += 1
            else:
                skipped_count += 1

        except Exception:
            skipped_count += 1
            continue

    papers_by_topic = {topic: papers}
    cleaned_dataset = prepare_cleaned_dataset(papers_by_topic)
    save_cleaned_dataset(cleaned_dataset)

    msg = f"✅ Download Completed: {downloaded_count} PDFs downloaded successfully."
    if skipped_count > 0:
        msg += f" | ⚠ Skipped: {skipped_count} papers (PDF not available)."

    return msg, downloaded_files


# ---------------- SIMILARITY TABLE ----------------
def simplify_similarity_matrix(sim_df):
    if sim_df.empty:
        return pd.DataFrame(columns=["Paper A", "Paper B", "Similarity %", "Interpretation"])

    titles = []
    if os.path.exists(FETCHED_PAPERS_PATH):
        with open(FETCHED_PAPERS_PATH, "r", encoding="utf-8") as f:
            papers = json.load(f)
        titles = [p.get("title", f"Paper {i+1}") for i, p in enumerate(papers)]

    pairs = []
    n = sim_df.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            score = float(sim_df.iloc[i, j])
            percent = round(score * 100, 2)

            if percent >= 70:
                label = "Very High"
            elif percent >= 40:
                label = "Moderate"
            elif percent >= 15:
                label = "Low"
            else:
                label = "Very Low"

            paper_a = titles[i] if i < len(titles) else f"Paper {i+1}"
            paper_b = titles[j] if j < len(titles) else f"Paper {j+1}"

            pairs.append([paper_a[:70], paper_b[:70], percent, label])

    pairs_df = pd.DataFrame(pairs, columns=["Paper A", "Paper B", "Similarity %", "Interpretation"])
    pairs_df = pairs_df.sort_values(by="Similarity %", ascending=False)

    return pairs_df.head(10)


# ---------------- ANALYSIS ----------------
def run_analysis(topic):
    setup_folders()

    topic_safe = topic.replace("/", "_").replace(" ", "_").strip()
    if not topic_safe:
        topic_safe = "papers"

    topic_folder = os.path.join(PDF_FOLDER, topic_safe)

    if not os.path.exists(topic_folder):
        return "❌ No PDFs folder found. Download PDFs first.", {}, pd.DataFrame()

    pdf_list = [f for f in os.listdir(topic_folder) if f.endswith(".pdf")]
    if len(pdf_list) == 0:
        return "❌ No PDFs found in topic folder. Download PDFs first.", {}, pd.DataFrame()

    clear_folder(TEXT_FOLDER)
    clear_folder(SECTION_FOLDER)

    extract_text_from_all_pdfs(topic_folder, TEXT_FOLDER)
    process_all_text_files(TEXT_FOLDER, SECTION_FOLDER)

    validation_report = validate_section_files(SECTION_FOLDER)

    key_findings, documents = extract_key_findings(SECTION_FOLDER)

    if not documents:
        return "❌ No documents extracted. PDFs may be scanned or extraction failed.", {}, pd.DataFrame()

    if len(documents) < 2:
        return "⚠ Only 1 valid document extracted. Similarity requires at least 2 papers.", key_findings, pd.DataFrame()

    similarity_matrix = compare_papers_tfidf(documents)

    if isinstance(similarity_matrix, np.ndarray):
        similarity_matrix = similarity_matrix.tolist()

    sim_df = pd.DataFrame(similarity_matrix)

    results = {
        "validation_report": validation_report,
        "key_findings": key_findings,
        "similarity_matrix": similarity_matrix
    }

    with open(SIMILARITY_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    simplified_similarity_df = simplify_similarity_matrix(sim_df)

    return "✅ Analysis completed successfully.", key_findings, simplified_similarity_df


# ---------------- DRAFT GENERATION ----------------
def generate_ai_draft(topic):
    if not os.path.exists(DATASET_PATH):
        return "❌ Dataset missing. Download papers first.", "", {}

    if not os.path.exists(SIMILARITY_PATH):
        return "❌ Similarity results missing. Run analysis first.", "", {}

    if not topic.strip():
        return "❌ Topic cannot be empty.", "", {}

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    with open(SIMILARITY_PATH, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    key_findings = sim_data.get("key_findings", {})
    patterns = extract_common_patterns(dataset)

    base_draft = generate_draft(patterns, key_findings)

    prompt = f"""
You are writing a professional academic research paper.

STRICT TOPIC: {topic}

Base Draft:
{base_draft}

Rewrite the draft STRICTLY related to "{topic}".
The paper must look like a real published research paper.

Structure must contain:
- Abstract
- Keywords
- Methods
- Results
- Conclusion
- References

Rules:
- Academic tone
- IEEE style writing (not markdown)
- No bullet stars
- No fake citations
- Keep everything topic-specific
"""

    final_draft = generate_with_gemini(prompt)

    return "✅ Draft generated successfully.", final_draft, patterns


# ---------------- CLEAN TEXT FOR PDF ----------------
def clean_pdf_text(text: str):
    text = text.replace("**", "")
    text = text.replace("*", "")
    text = text.replace("###", "")
    text = text.replace("##", "")
    text = text.replace("#", "")
    return text.strip()


# ---------------- PROFESSIONAL IEEE STYLE PDF (2 COLUMN) ----------------
def generate_professional_ieee_pdf(save_path, revised_text, topic="Final Research Paper"):

    revised_text = clean_pdf_text(revised_text)

    def add_header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(1 * inch, 10.75 * inch, topic[:60])
        canvas.drawRightString(7.5 * inch, 10.75 * inch, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        save_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "IEEE_Title",
        parent=styles["Title"],
        fontName="Times-Bold",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    author_style = ParagraphStyle(
        "IEEE_Author",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        "IEEE_Heading",
        parent=styles["Heading2"],
        fontName="Times-Bold",
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "IEEE_Body",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    abstract_style = ParagraphStyle(
        "IEEE_Abstract",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    keyword_style = ParagraphStyle(
        "IEEE_Keywords",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=10
    )

    reference_style = ParagraphStyle(
        "IEEE_References",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
        leftIndent=0.3 * inch,
        firstLineIndent=-0.3 * inch,
        spaceAfter=4
    )

    elements = []

    # Title Block
    elements.append(Paragraph(topic, title_style))
    elements.append(Paragraph("LitWise AI Research Paper Generator", author_style))
    elements.append(Paragraph("Department of Computer Science", author_style))
    elements.append(Paragraph(datetime.now().strftime("%d %B %Y"), author_style))
    elements.append(Spacer(1, 12))

    # Extract Abstract + Keywords separately
    lines = revised_text.split("\n")

    abstract_text = []
    keyword_text = ""
    body_lines = []
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower = line.lower()

        if lower == "abstract":
            current_section = "abstract"
            continue
        elif lower == "keywords":
            current_section = "keywords"
            continue
        elif lower in ["methods", "results", "discussion", "conclusion", "references", "introduction"]:
            current_section = "body"
            body_lines.append(line.upper())
            continue

        if current_section == "abstract":
            abstract_text.append(line)
        elif current_section == "keywords":
            keyword_text += " " + line
        else:
            body_lines.append(line)

    # Add Abstract
    elements.append(Paragraph("Abstract", section_heading))
    if abstract_text:
        elements.append(Paragraph(" ".join(abstract_text), abstract_style))
    else:
        elements.append(Paragraph("Abstract not found.", abstract_style))

    # Add Keywords
    elements.append(Paragraph("Keywords", section_heading))
    if keyword_text.strip():
        elements.append(Paragraph(keyword_text.strip(), keyword_style))
    else:
        elements.append(Paragraph("Keywords not found.", keyword_style))

    elements.append(Spacer(1, 10))

    # Two Column Frames
    frame1 = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        (doc.width / 2) - 10,
        doc.height - 180,
        id="col1"
    )

    frame2 = Frame(
        doc.leftMargin + (doc.width / 2) + 10,
        doc.bottomMargin,
        (doc.width / 2) - 10,
        doc.height - 180,
        id="col2"
    )

    template = PageTemplate(id="TwoCol", frames=[frame1, frame2], onPage=add_header_footer)
    doc.addPageTemplates([template])

    # Fill body in 2 columns
    in_references = False
    for line in body_lines:

        if line.lower() == "references":
            in_references = True
            elements.append(Paragraph("REFERENCES", section_heading))
            continue

        if line.isupper() and line.lower() in ["methods", "results", "discussion", "conclusion", "introduction"]:
            elements.append(Paragraph(line.title(), section_heading))
            continue

        if in_references:
            elements.append(Paragraph(line, reference_style))
        else:
            elements.append(Paragraph(line, body_style))

    doc.build(elements)


# ---------------- REVISION + FINAL PDF DOWNLOAD ----------------
def revise_with_feedback(draft_text, feedback, topic):
    if not draft_text.strip():
        return "❌ Draft empty. Generate draft first.", "", {}, []

    if not topic.strip():
        topic = "Literature Review"

    prompt = f"""
You are writing a professional research paper.

STRICT TOPIC: {topic}

Draft:
{draft_text}

Feedback:
{feedback}

Rewrite the draft and ensure it is STRICTLY based on the topic.
The final output must look like a real IEEE research paper.

Include:
- Abstract
- Keywords
- Methods
- Results
- Conclusion
- References

Rules:
- No markdown formatting
- No stars
- Professional academic writing
- IEEE style paragraph writing
"""

    revised_text = generate_with_gemini(prompt)
    quality_report = evaluate_quality(revised_text)

    filename = f"final_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    save_path = os.path.join(FINAL_REPORT_FOLDER, filename)

    generate_professional_ieee_pdf(save_path, revised_text, topic)

    save_path = os.path.abspath(save_path)

    if not os.path.exists(save_path):
        return "❌ PDF generation failed.", revised_text, quality_report, []

    return (
        "✅ Revision completed successfully. IEEE Research Paper PDF ready for download.",
        revised_text,
        quality_report,
        [save_path]
    )


# ---------------- PROFESSIONAL CSS + NAVBAR ----------------
CUSTOM_CSS = """
body{
    background:#f8fafc !important;
    font-family: Inter, system-ui, sans-serif;
    color:#0f172a;
}

.gradio-container{
    max-width: 1250px !important;
    margin: auto !important;
    padding-top: 20px !important;
}

.navbar{
    width: 100%;
    background: #ffffff;
    border-bottom: 1px solid rgba(15,23,42,0.08);
    padding: 14px 32px;
    position: sticky;
    top: 0;
    z-index: 999;
    display:flex;
    justify-content: space-between;
    align-items:center;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.04);
    border-radius: 14px;
    margin-bottom: 20px;
}

.brand{
    display:flex;
    align-items:center;
    gap:12px;
}

.logo{
    width:40px;
    height:40px;
    border-radius: 12px;
    background: linear-gradient(135deg,#2563eb,#1e3a8a);
    display:flex;
    justify-content:center;
    align-items:center;
    font-weight:900;
    color:white;
    font-size:16px;
}

.brand-text h2{
    font-size: 18px;
    font-weight: 900;
    margin: 0;
    color:#0f172a;
}

.brand-text p{
    font-size: 12px;
    font-weight: 600;
    margin: 0;
    color:#64748b;
}

.nav-links{
    display:flex;
    gap:18px;
    font-size: 13px;
    font-weight: 800;
    color:#334155;
}

.nav-links span:hover{
    color:#2563eb;
    cursor:pointer;
}

.hero{
    border-radius: 20px;
    padding: 40px;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0px 12px 40px rgba(15,23,42,0.06);
    margin-bottom: 22px;
}

.hero-title{
    font-size: 40px;
    font-weight: 900;
    margin-bottom: 8px;
    color:#0f172a;
}

.hero-subtitle{
    font-size: 15px;
    font-weight: 500;
    color:#475569;
    line-height: 1.7;
}

.card{
    border-radius: 18px;
    padding: 26px;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0px 8px 25px rgba(15,23,42,0.05);
    margin-bottom: 18px;
}

.section-title{
    font-size: 17px;
    font-weight: 900;
    margin-bottom: 12px;
    color:#0f172a;
}

button{
    border-radius: 12px !important;
    font-weight: 900 !important;
    padding: 12px 18px !important;
    background: #2563eb !important;
    border: none !important;
    color: white !important;
    box-shadow: 0px 10px 22px rgba(37,99,235,0.22);
}

button:hover{
    background: #1e40af !important;
    transform: translateY(-1px);
}

textarea, input{
    border-radius: 12px !important;
    border: 1px solid rgba(0,0,0,0.12) !important;
    padding: 12px !important;
    font-size: 14px !important;
    background: #ffffff !important;
}

label{
    font-weight: 800 !important;
    color:#0f172a !important;
}
"""


# ---------------- UI ----------------
def launch_ui():
    setup_folders()

    with gr.Blocks(
        css=CUSTOM_CSS,
        title="LitWise AI",
        theme=gr.themes.Base(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="gray",
            font=["Inter", "system-ui", "sans-serif"]
        )
    ) as demo:

        gr.HTML("""
        <script>
            localStorage.setItem("gradio_theme", "light");
            document.documentElement.classList.remove("dark");
            document.documentElement.classList.add("light");
        </script>
        """)

        gr.HTML("""
        <div class="navbar">
            <div class="brand">
                <div class="logo">LW</div>
                <div class="brand-text">
                    <h2>LitWise AI</h2>
                    <p>AI Research Paper Review & Draft Generator</p>
                </div>
            </div>
            <div class="nav-links">
                <span>Dashboard</span>
                <span>Papers</span>
                <span>Analysis</span>
                <span>Draft</span>
                <span>Export</span>
            </div>
        </div>
        """)

        gr.HTML("""
        <div class="hero">
            <div class="hero-title">LitWise AI Dashboard</div>
            <div class="hero-subtitle">
                Fetch papers, download PDFs, extract key findings, compute cosine similarity,
                generate professional drafts, and export IEEE-style research paper PDFs.
            </div>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=3):
                with gr.Group(elem_classes="card"):
                    gr.HTML("<div class='section-title'>Research Topic</div>")
                    topic_input = gr.Textbox(
                        placeholder="Example: Music Generation using Deep Learning",
                        label=""
                    )

            with gr.Column(scale=1):
                with gr.Group(elem_classes="card"):
                    gr.HTML("<div class='section-title'>Paper Limit</div>")
                    limit_input = gr.Slider(1, 10, step=1, value=5, label="")

        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>System Status</div>")
            status_box = gr.Textbox(label="", lines=2)

        with gr.Row():
            with gr.Column():
                with gr.Group(elem_classes="card"):
                    gr.HTML("<div class='section-title'>Fetch Research Papers</div>")
                    fetch_btn = gr.Button("Fetch Papers")
                    paper_df = gr.Dataframe(label="Fetched Papers", interactive=False)

            with gr.Column():
                with gr.Group(elem_classes="card"):
                    gr.HTML("<div class='section-title'>Download PDFs</div>")
                    download_btn = gr.Button("Download PDFs")
                    pdf_files = gr.File(label="Downloaded PDFs", file_count="multiple", type="filepath")

        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>Analyze & Compare Papers</div>")
            analyze_btn = gr.Button("Run Analysis & Similarity")
            key_findings_output = gr.JSON(label="Key Findings Extracted")

            similarity_output = gr.Dataframe(
                label="Top Similar Paper Pairs (Cosine Similarity %)",
                interactive=False
            )

        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>Generate Draft (Gemini)</div>")
            draft_btn = gr.Button("Generate Draft")
            draft_output = gr.Textbox(label="Generated Draft", lines=18)
            patterns_output = gr.JSON(label="Common Patterns")

        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>Revise Draft & Export Final Paper (IEEE PDF)</div>")
            feedback_input = gr.Textbox(
                label="Mentor Feedback / User Suggestions",
                placeholder="Example: Improve abstract clarity, mention datasets, highlight results...",
                lines=4
            )

            revise_btn = gr.Button("Revise Draft & Generate Final PDF")
            revised_output = gr.Textbox(label="Revised Draft", lines=18)
            quality_output = gr.JSON(label="Quality Report")

            final_report_file = gr.File(
                label="Download Final Paper (IEEE Research Paper PDF)",
                file_count="single",
                type="filepath"
            )

        fetch_btn.click(fetch_papers, inputs=[topic_input, limit_input], outputs=[status_box, paper_df])
        download_btn.click(download_papers, inputs=[topic_input], outputs=[status_box, pdf_files])
        analyze_btn.click(run_analysis, inputs=[topic_input], outputs=[status_box, key_findings_output, similarity_output])
        draft_btn.click(generate_ai_draft, inputs=[topic_input], outputs=[status_box, draft_output, patterns_output])

        revise_btn.click(
            revise_with_feedback,
            inputs=[draft_output, feedback_input, topic_input],
            outputs=[status_box, revised_output, quality_output, final_report_file]
        )

    demo.launch(server_name="127.0.0.1", server_port=7860)


if __name__ == "__main__":
    launch_ui()
