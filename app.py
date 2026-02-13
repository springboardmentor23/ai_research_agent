import gradio as gr
import os
import shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from paper_retrieval import fetch_papers
from pdf_downloader import download_pdf
from text_extractor import extract_all_pdfs_text
from text_to_json import convert_txt_to_json
from key_phrases import process_key_phrases
from tfidf_vectorizer import build_tfidf_vectors
from similarity import compute_similarity
from cross_compare import cross_compare_papers
from paper_generator import generate_paper
from review_module import review_paper


# ==================================================
# CLEAN DATA
# ==================================================

def clean_old_data():
    folders = ["pdfs", "extracted_texts", "extracted_texts_json", "key_phrases"]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder, exist_ok=True)
    return "✔ Old data cleaned\n"


# ==================================================
# PIPELINE
# ==================================================

def start_pipeline(topic, num_papers):

    log = ""

    if not topic:
        return "❌ Enter topic.", ""

    log += clean_old_data()

    papers = fetch_papers(topic, limit=int(num_papers))

    if not papers:
        return "❌ No papers fetched.", ""

    log += f"✔ {len(papers)} papers fetched\n"

    for paper in papers:
        pdf_info = paper.get("openAccessPdf")
        if pdf_info and pdf_info.get("url"):
            download_pdf(pdf_info["url"], paper.get("title", "paper"))

    log += "✔ PDFs downloaded\n"

    extract_all_pdfs_text()
    log += "✔ Text extraction done\n"

    convert_txt_to_json()
    log += "✔ TXT → JSON done\n"

    process_key_phrases()
    log += "✔ Key phrases extracted\n"

    tfidf_matrix, paper_names = build_tfidf_vectors()
    log += "✔ TF-IDF created\n"

    similarity_output = ""

    if len(paper_names) < 2:
        log += "⚠ Only one paper. Similarity skipped\n"
    else:
        similarity_matrix = compute_similarity(tfidf_matrix, paper_names)
        similarity_output = cross_compare_papers(similarity_matrix, paper_names)
        log += "✔ Similarity computed\n"

    return log, similarity_output


# ==================================================
# GENERATE PAPER (NO AUTO SCORE)
# ==================================================

def generate_final(mode, custom_prompt):

    if mode == "API":
        paper = generate_paper("api", custom_prompt)
    else:
        paper = generate_paper("local", custom_prompt)

    return paper


# ==================================================
# QUALITY SCORE BUTTON FUNCTION
# ==================================================

def get_quality_score():

    review_text, _ = review_paper("")
    score = "Not Found"

    for line in review_text.split("\n"):
        if "Quality Score" in line:
            score = line.strip()
            break

    return score


# ==================================================
# TXT → PDF
# ==================================================

def convert_txt_to_pdf(txt_path, pdf_path):
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    elements = []

    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            elements.append(Paragraph(line.strip(), styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)


def download_generated_pdf():
    pdf_path = "generated_paper.pdf"
    convert_txt_to_pdf("final_review.txt", pdf_path)
    return pdf_path


# ==================================================
# EXTRACTED PAGE
# ==================================================

def get_extracted_files():
    if os.path.exists("extracted_texts"):
        return os.listdir("extracted_texts")
    return []

def view_extracted_file(filename):
    path = os.path.join("extracted_texts", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def download_extracted_pdf(filename):
    txt_path = os.path.join("extracted_texts", filename)
    pdf_path = f"{filename}.pdf"
    convert_txt_to_pdf(txt_path, pdf_path)
    return pdf_path


# ==================================================
# REVISION
# ==================================================

def revise_paper(revision_prompt):

    _, revised_text = review_paper(revision_prompt)

    with open("revised_temp.txt", "w", encoding="utf-8") as f:
        f.write(revised_text)

    pdf_path = "revised_paper.pdf"
    convert_txt_to_pdf("revised_temp.txt", pdf_path)

    return revised_text


def download_revised_pdf():
    return "revised_paper.pdf"


# ==================================================
# UI
# ==================================================
custom_css = """

/* ===== LIGHTER MODERN BACKGROUND ===== */
html, body, .gradio-container {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c3c);
    background-size: 400% 400%;
    animation: gradientMove 18s ease infinite;
    color: white !important;
}

/* Animated Gradient */
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ===== GLASS PANELS ===== */
.gr-block {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(18px);
    border-radius: 18px !important;
    padding: 20px !important;
    border: 1px solid rgba(0, 255, 200, 0.3);
}

/* ===== HEADING ===== */
h1 {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    background: linear-gradient(90deg, #9b59b6, #3498db);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ===== TABS ===== */
button[data-testid="tab"] {
    background: transparent !important;
    color: #e0f7fa !important;
    font-weight: 600 !important;
    transition: 0.3s ease;
}

button[data-testid="tab"]:hover {
    color: #00ffcc !important;
    transform: scale(1.05);
}

button[data-testid="tab"][aria-selected="true"] {
    border-bottom: 3px solid #00ffcc !important;
    color: #00ffcc !important;
}

/* ===== GREEN GLOW BUTTONS ===== */
button {
    background: linear-gradient(90deg, #00ff99, #00ffcc) !important;
    color: black !important;
    border-radius: 14px !important;
    border: none !important;
    font-weight: 600;
    transition: 0.3s ease-in-out;
}

button:hover {
    box-shadow: 0 0 20px #00ffcc, 0 0 40px #00ff99;
    transform: scale(1.07);
}

/* ===== TEXTBOXES ===== */
textbox textarea {
    background: rgba(255, 255, 255, 0.12) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid #00ffcc !important;
    transition: 0.3s ease;
}

textbox textarea:focus {
    border: 1px solid #00ff99 !important;
    box-shadow: 0 0 12px #00ffcc;
}

/* ===== DROPDOWN ===== */
.gr-dropdown select {
    background: rgba(255, 255, 255, 0.12) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid #00ffcc !important;
}

/* ===== RADIO ===== */
.gr-radio {
    color: white !important;
}

/* ===== FILE COMPONENT ===== */
.gr-file {
    background: rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    border: 1px solid #00ffcc !important;
}

/* ===== LABELS ===== */
label {
    color: #e0f7fa !important;
    font-weight: 500;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(#00ff99, #00ffcc);
    border-radius: 10px;
}
"""


with gr.Blocks(css=custom_css) as app:


    gr.Markdown("# AI System to Automatically Review and Summarize Research Papers")

    with gr.Tabs():

        # =========================
        # TAB 1: PIPELINE
        # =========================
        with gr.Tab("Pipeline & Generation"):

            topic = gr.Textbox(label="Research Topic")
            num_papers = gr.Number(
                minimum=1,
                maximum=10,
                step=1,
                value=3,
                label="Number of Paperss"
            )           


            start_btn = gr.Button("Start Pipeline")

            with gr.Row():
                status_log = gr.Textbox(label="Status Log", lines=12)
                similarity_output = gr.Textbox(label="Similarity Output", lines=12)

            gr.Markdown("## Generate Paper")

            mode = gr.Radio(["Local", "API"], value="Local")
            custom_prompt = gr.Textbox(label="Custom Instruction")

            generate_btn = gr.Button("Generate Paper")

            generated_output = gr.Textbox(label="Generated Paper", lines=20)

            score_btn = gr.Button("Get Quality Score")
            quality_score = gr.Textbox(label="Quality Score")

            download_btn = gr.Button("Download Generated PDF")
            download_file = gr.File()

            start_btn.click(
                start_pipeline,
                inputs=[topic, num_papers],
                outputs=[status_log, similarity_output]
            )

            generate_btn.click(
                generate_final,
                inputs=[mode, custom_prompt],
                outputs=generated_output
            )

            score_btn.click(
                get_quality_score,
                outputs=quality_score
            )

            download_btn.click(
                download_generated_pdf,
                outputs=download_file
            )

        # =========================
        # TAB 2: EXTRACTED PAPERS
        # =========================
        with gr.Tab("Extracted Papers"):

            with gr.Row():

                with gr.Column(scale=2):

                    file_list = gr.Dropdown(
                        choices=get_extracted_files(),
                        label="Select Paper",
                        interactive=True
                    )

                with gr.Column(scale=1):

                    view_btn = gr.Button("🔍 View")

                    download_ex_btn = gr.Button("⬇ Download as PDF")

                with gr.Column(scale=1):

                    extracted_download = gr.File(label="Download File")

            extracted_content = gr.Textbox(
                label="Extracted Content",
                lines=30
            )

            view_btn.click(
                view_extracted_file,
                inputs=file_list,
                outputs=extracted_content
            )

            download_ex_btn.click(
                download_extracted_pdf,
                inputs=file_list,
                outputs=extracted_download
            )

        # =========================
        # TAB 3: REVISION
        # =========================
        with gr.Tab("Revision"):

            revision_prompt = gr.Textbox(label="Revision Instruction")

            revise_btn = gr.Button("Revise Paper")

            revised_output = gr.Textbox(label="Revised Paper", lines=20)

            download_revised_btn = gr.Button("Download Revised PDF")
            revised_download = gr.File()

            revise_btn.click(
                revise_paper,
                inputs=revision_prompt,
                outputs=revised_output
            )

            download_revised_btn.click(
                download_revised_pdf,
                outputs=revised_download
            )

app.launch()