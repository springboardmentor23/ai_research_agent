import os
import json
from groq import Groq
from fpdf import FPDF

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "Set GROQ_API_KEY environment variable before running. "
        "Example (PowerShell): $env:GROQ_API_KEY='your_api_key_here'"
    )
client = Groq(api_key=GROQ_API_KEY)

FINDINGS_DIR = "data/dist_texts"
METADATA_DIR = "data/metadata"

def load_all_findings_with_metadata():
    os.makedirs(FINDINGS_DIR, exist_ok=True)
    combined = ""

    for file in os.listdir(FINDINGS_DIR):
        if not file.endswith("_findings.txt"):
            continue

        paper_id = file.replace("_findings.txt", "")

        # load metadata (you already have this from Step 0)
        meta_path = f"{METADATA_DIR}/{paper_id}.json"
        findings_path = f"{FINDINGS_DIR}/{file}"

        if not os.path.exists(meta_path):
            continue

        with open(meta_path, "r", encoding="utf-8") as m:
            meta = json.load(m)

        with open(findings_path, "r", encoding="utf-8") as f:
            findings = f.read().strip()

        if not findings:
            continue

        combined += f"""
Paper:
Title: {meta['title']}
Authors: {", ".join(meta['authors'])}
Year: {meta['year']}
URL: {meta['paper_url']}

Key Findings:
{findings}
"""
    print(combined)
    return combined


def generate_synthesized_paper():
    content = load_all_findings_with_metadata()
    if not content.strip():
        raise ValueError(
            "No key findings found. Run key_phrases.py first to extract findings from data/texts into data/dist_texts. "
            "Then run generate_paper.py again."
        )
    prompt = f"""
You are an academic research assistant. Generate a SINGLE synthesized research paper in full APA 7 style.

FORMAT: Use APA 7th edition style for the ENTIRE paper.

Required structure (APA 7):
1. Title page: Include a concise title (recommended 12 words or fewer), and an author note line if needed.
2. Abstract: One paragraph, 150–250 words, summarizing the synthesis. No indentation for the abstract paragraph.
3. Main body with APA headings:
   - Use Level 1 (bold, centered) for main sections: Introduction, Method, Results, Discussion.
   - Use Level 2 (bold, left-aligned) for subsections where appropriate.
4. In-text citations: Use (Author, Year) or Author (Year) format. When synthesizing multiple sources, cite each: (Author1, Year; Author2, Year). Use the author names and years from the metadata provided.
5. References: End with a "References" section. Format every cited work in APA 7 style:
   - Journal: Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), page–page. https://doi.org/xxx (or URL if no DOI)
   - Use the exact titles, authors, years, and URLs from the provided metadata for the reference list.

Rules:
- Do not invent new information; base everything strictly on the input.
- Use formal, academic tone and third person.
- Do NOT include numerical values, percentages, model sizes, dataset sizes, or metric values; use qualitative academic language.
- Treat this as a synthesis of prior work, not a new experiment.
- Do NOT use first-person language ("we", "our").
- Every in-text citation must have a matching entry in the References list in correct APA 7 format.

Key Findings and Metadata:
{content}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


class PDF(FPDF):
    """APA-style PDF with 1-inch margins and 12pt body text."""
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(True, margin=25)
        self.set_margins(25.4, 25.4)  # 1 inch in mm
        self.set_auto_page_break(True, margin=25.4)

    def header(self):
        self.set_font("Helvetica", "", 10)
        self.cell(0, 10, "", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_body_text(self, text):
        self.set_font("Helvetica", "", 12)
        # Ensure we can write common UTF-8 (replace chars that fail in Latin-1)
        safe = text.encode("latin-1", errors="replace").decode("latin-1")
        for block in safe.split("\n\n"):
            block = block.strip()
            if block:
                self.multi_cell(0, 6, block)
                self.ln(4)


def save_paper_to_pdf(text, filepath):
    pdf = PDF()
    pdf.add_page()
    pdf.add_body_text(text)
    pdf.output(filepath)


if __name__ == "__main__":
    paper = generate_synthesized_paper()

    os.makedirs("data/output", exist_ok=True)
    out_dir = "data/output"

    txt_path = os.path.join(out_dir, "synthesized_paper.txt")
    pdf_path = os.path.join(out_dir, "synthesized_paper.pdf")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(paper)

    save_paper_to_pdf(paper, pdf_path)

    print("Synthesized research paper generated successfully.")
    print(f"  Text: {txt_path}")
    print(f"  PDF:  {pdf_path}")