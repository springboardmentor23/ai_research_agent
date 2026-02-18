import gradio as gr
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

from src.paper_search.hybrid_search import fetch_papers_hybrid
from src.paper_search.pdf_downloader import download_pdf
from src.paper_search.dataset_utils import prepare_cleaned_dataset, save_cleaned_dataset

from src.text_extraction.pdf_text_extractor import extract_text_from_all_pdfs
from src.text_extraction.section_extractor import process_all_text_files
from src.text_extraction.tfidf_similarity import extract_key_findings, compare_papers_tfidf
from src.text_extraction.validation import validate_section_files

from src.milestone_3.pattern_extractor import extract_common_patterns
from src.milestone_3.draft_generator import generate_draft
from src.milestone_3.gpt_client import generate_with_gemini

from src.milestone_4.quality_evaluator import evaluate_quality


DATASET_PATH = "data/datasets/cleaned_dataset.json"
SIMILARITY_PATH = "data/datasets/similarity_results.json"

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


# ---------------- FETCH PAPERS ----------------
def fetch_papers(topic, limit):
    setup_folders()

    if not topic.strip():
        return "❌ Topic cannot be empty.", pd.DataFrame()

    papers = fetch_papers_hybrid(topic)[:limit]

    if not papers:
        return "❌ No papers found.", pd.DataFrame()

    with open("data/datasets/fetched_papers.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2)

    rows = []
    for idx, paper in enumerate(papers, start=1):
        title = paper.get("title", "Untitled")
        year = paper.get("year", "N/A")
        venue = paper.get("venue", "N/A")
        rows.append([idx, title, year, venue])

    df = pd.DataFrame(rows, columns=["#", "Paper Title", "Year", "Source"])
    return f"✅ Successfully fetched {len(papers)} papers.", df


# ---------------- DOWNLOAD PAPERS ----------------
def download_papers(topic):
    setup_folders()

    file_path = "data/datasets/fetched_papers.json"
    if not os.path.exists(file_path):
        return "❌ Fetch papers first.", []

    with open(file_path, "r", encoding="utf-8") as f:
        papers = json.load(f)

    topic_safe = topic.replace("/", "_").replace(" ", "_")
    topic_folder = os.path.join(PDF_FOLDER, topic_safe)
    os.makedirs(topic_folder, exist_ok=True)

    downloaded_files = []
    downloaded_count = 0

    for idx, paper in enumerate(papers, start=1):
        pdf_info = paper.get("openAccessPdf")

        if not pdf_info or not pdf_info.get("url"):
            continue

        pdf_url = pdf_info["url"]
        save_path = os.path.join(topic_folder, f"{topic_safe}_{idx}.pdf")

        try:
            download_pdf(pdf_url, save_path)
            downloaded_files.append(save_path)
            downloaded_count += 1
        except Exception:
            continue

    papers_by_topic = {topic: papers}
    cleaned_dataset = prepare_cleaned_dataset(papers_by_topic)
    save_cleaned_dataset(cleaned_dataset)

    return f"✅ Downloaded {downloaded_count} PDFs successfully.", downloaded_files


# ---------------- ANALYSIS ----------------
def run_analysis():
    setup_folders()

    if not os.path.exists(DATASET_PATH):
        return "❌ Dataset not found. Download papers first.", {}, pd.DataFrame()

    extract_text_from_all_pdfs(PDF_FOLDER, TEXT_FOLDER)
    process_all_text_files(TEXT_FOLDER, SECTION_FOLDER)

    validation_report = validate_section_files(SECTION_FOLDER)
    key_findings, documents = extract_key_findings(SECTION_FOLDER)

    similarity_matrix = []
    sim_df = pd.DataFrame()

    if documents:
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

    return "✅ Analysis completed successfully.", key_findings, sim_df


# ---------------- DRAFT GENERATION ----------------
def generate_ai_draft():
    if not os.path.exists(DATASET_PATH):
        return "❌ Dataset missing. Download papers first.", "", {}

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    if not os.path.exists(SIMILARITY_PATH):
        return "❌ Similarity results missing. Run analysis first.", "", {}

    with open(SIMILARITY_PATH, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    key_findings = sim_data.get("key_findings", {})
    patterns = extract_common_patterns(dataset)

    draft_text = generate_draft(patterns, key_findings)
    return "✅ Draft generated successfully.", draft_text, patterns


# ---------------- REVISION ----------------
def revise_with_feedback(draft_text, feedback):
    if not draft_text.strip():
        return "❌ Draft empty. Generate draft first.", "", {}, None

    prompt = f"""
You are an academic research assistant.

Draft:
{draft_text}

User Feedback:
{feedback}

Task:
Rewrite the draft incorporating feedback.

Structure must contain:
- Abstract
- Methods
- Results

Rules:
- Formal academic tone
- APA style writing
- Do not invent citations
"""

    revised_text = generate_with_gemini(prompt)
    quality_report = evaluate_quality(revised_text)

    filename = f"final_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_path = os.path.join(FINAL_REPORT_FOLDER, filename)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(revised_text)

    return "✅ Revision completed successfully.", revised_text, quality_report, save_path


# ---------------- CSS (KEEPING SAME AS YOUR CODE) ----------------
CUSTOM_CSS = """
body{
    background:#ffffff !important;
    font-family: Inter, system-ui, sans-serif;
    color:#0b1220;
}

.gradio-container{
    max-width: 1250px !important;
    margin: auto !important;
    padding-top: 25px !important;
}

/* HERO SECTION */
.hero{
    border-radius: 30px;
    padding: 60px;
    background: linear-gradient(135deg, #ffffff, #fff6f0);
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0px 18px 60px rgba(0,0,0,0.08);
    margin-bottom: 28px;
}

.hero-title{
    font-size: 50px;
    font-weight: 900;
    letter-spacing: -1px;
    color:#0b1220;
    margin-bottom: 12px;
}

.hero-subtitle{
    font-size: 18px;
    font-weight: 500;
    color:#475569;
    margin-bottom: 22px;
    line-height: 1.7;
}

.hero-tag{
    display:inline-block;
    padding: 10px 18px;
    border-radius: 999px;
    background: linear-gradient(90deg,#ff7a59,#ff3d81);
    color:white;
    font-weight: 800;
    font-size: 13px;
    margin-bottom: 22px;
    box-shadow: 0px 12px 35px rgba(255,61,129,0.25);
}

/* STEP BAR */
.stepbar{
    display:flex;
    justify-content: space-between;
    gap: 14px;
    margin-top: 15px;
    flex-wrap: wrap;
}

.step{
    flex: 1;
    min-width: 180px;
    padding: 14px 18px;
    border-radius: 18px;
    background: #f8fafc;
    border: 1px solid rgba(0,0,0,0.06);
    font-weight: 800;
    font-size: 14px;
    color:#0b1220;
}

/* CARD STYLE */
.card{
    border-radius: 26px;
    padding: 30px;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0px 12px 40px rgba(0,0,0,0.06);
    margin-bottom: 22px;
}

.section-title{
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 15px;
    color:#0b1220;
}

/* BUTTON STYLE */
button{
    border-radius: 16px !important;
    font-weight: 900 !important;
    padding: 14px 20px !important;
    background: linear-gradient(90deg,#ff7a59,#ff3d81) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0px 14px 35px rgba(255,61,129,0.22);
    transition: all 0.25s ease-in-out;
}

button:hover{
    transform: translateY(-2px);
    background: linear-gradient(90deg,#ff3d81,#ff7a59) !important;
    box-shadow: 0px 18px 55px rgba(255,61,129,0.32);
}

/* INPUTS */
textarea, input{
    border-radius: 16px !important;
    border: 1px solid rgba(0,0,0,0.12) !important;
    padding: 12px !important;
    font-size: 15px !important;
    background: #ffffff !important;
}

label{
    font-weight: 800 !important;
    color:#0b1220 !important;
}

.footer-note{
    margin-top: 25px;
    font-size: 13px;
    color:#64748b;
    text-align:center;
}
"""


# ---------------- UI ----------------
def launch_ui():
    setup_folders()

    with gr.Blocks(css=CUSTOM_CSS, title="LitWise AI") as demo:

        gr.HTML("""
        <div class="hero">
            <div class="hero-tag">AI Literature Review Platform</div>
            <div class="hero-title">LitWise AI</div>
            <div class="hero-subtitle">
                A professional AI-powered pipeline to fetch research papers, download PDFs,
                analyze extracted sections, compare similarity, generate structured drafts,
                and export final reports with quality evaluation.
            </div>

            <div class="stepbar">
                <div class="step">Fetch Papers</div>
                <div class="step">Download PDFs</div>
                <div class="step">Analyze & Compare</div>
                <div class="step">Generate Draft</div>
                <div class="step">Revise & Export</div>
            </div>
        </div>
        """)

        # INPUT CONFIGURATION
        with gr.Row():
            with gr.Column(scale=3):
                with gr.Group(elem_classes="card"):
                    gr.HTML("<div class='section-title'>Research Topic</div>")
                    topic_input = gr.Textbox(
                        placeholder="Example: Lung Disease Prediction using Machine Learning",
                        label=""
                    )

            with gr.Column(scale=1):
                with gr.Group(elem_classes="card"):
                    gr.HTML("<div class='section-title'>Paper Limit</div>")
                    limit_input = gr.Slider(1, 6, step=1, value=5, label="")

        # STATUS BOX
        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>System Status</div>")
            status_box = gr.Textbox(label="", lines=2)

        # FETCH + DOWNLOAD
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
                    pdf_files = gr.File(label="Download Links", file_count="multiple")

        # ANALYSIS
        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>Analyze & Compare Papers</div>")
            analyze_btn = gr.Button("Run Analysis & Similarity")
            key_findings_output = gr.JSON(label="Key Findings Extracted")
            similarity_output = gr.Dataframe(label="Cosine Similarity Matrix", interactive=False)

        # DRAFT
        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>Generate Draft (Gemini)</div>")
            draft_btn = gr.Button("Generate Draft")
            draft_output = gr.Textbox(label="Generated Draft", lines=18)
            patterns_output = gr.JSON(label="Common Patterns")

        # REVISION
        with gr.Group(elem_classes="card"):
            gr.HTML("<div class='section-title'>Revise Draft & Export Final Paper</div>")
            feedback_input = gr.Textbox(
                label="Mentor Feedback / User Suggestions",
                placeholder="Example: Improve abstract clarity, mention datasets, highlight results...",
                lines=4
            )

            revise_btn = gr.Button("Revise Draft")
            revised_output = gr.Textbox(label="Revised Draft", lines=18)
            quality_output = gr.JSON(label="Quality Report")
            final_report_file = gr.File(label="Download Final Paper", file_count="single")

        # gr.HTML("<div class='footer-note'>LitWise AI • Milestone 4 Final Professional UI</div>")

        # EVENTS
        fetch_btn.click(fetch_papers, inputs=[topic_input, limit_input], outputs=[status_box, paper_df])
        download_btn.click(download_papers, inputs=[topic_input], outputs=[status_box, pdf_files])
        analyze_btn.click(run_analysis, inputs=[], outputs=[status_box, key_findings_output, similarity_output])
        draft_btn.click(generate_ai_draft, inputs=[], outputs=[status_box, draft_output, patterns_output])
        revise_btn.click(
            revise_with_feedback,
            inputs=[draft_output, feedback_input],
            outputs=[status_box, revised_output, quality_output, final_report_file]
        )

    demo.launch(server_name="127.0.0.1", server_port=7860)


if __name__ == "__main__":
    launch_ui()
