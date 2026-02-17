import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

os.chdir(REPO_ROOT)

from modules.paper_search import fetch_papers
from modules.dataset_builder import save_datasets
from modules.pdf_downloader import download_pdfs
from modules.text_extractor import extract_text_from_pdfs
from modules.section_parser import split_into_sections
from modules.key_finder import extract_key_findings
from modules.similarity import cross_paper_similarity
from modules.common_finder import extract_common_methods
from modules.common_datasets import extract_common_datasets
from modules.synthesizer import synthesize_findings
from modules.draft_generator import generate_section
from modules.reference_formatter import format_apa_references
from modules.gemini_flash_client import generate_with_gemini_flash

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

app = Flask(__name__)
CORS(app)

DATA_DIR = os.path.join(REPO_ROOT, "data")
PAPERS_DIR = os.path.join(DATA_DIR, "papers")
DATASETS_DIR = os.path.join(DATA_DIR, "datasets")
EXTRACTED_DIR = os.path.join(DATA_DIR, "extracted_text")
ANALYSIS_DIR = os.path.join(DATA_DIR, "analysis")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")


def _ensure_dirs():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    os.makedirs(EXPORTS_DIR, exist_ok=True)


def _sanitize_topic(topic: str) -> str:
    return "_".join(topic.strip().split())


def _write_json(path: str, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)


def _read_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _draft_to_text(draft: dict) -> str:
    ordered = [
        "Abstract",
        "Introduction",
        "Methods",
        "Results",
        "Discussion",
        "Conclusion",
        "References",
    ]
    parts = []
    for key in ordered:
        if key in draft and draft[key]:
            parts.append(key)
            if isinstance(draft[key], list):
                parts.append("\n".join(draft[key]))
            else:
                parts.append(str(draft[key]))
            parts.append("")
    return "\n".join(parts).strip() + "\n"


def _clean_ai_markdown(text: str) -> str:
    """
    Remove common AI markdown artifacts:
    - Remove leading/trailing * and # markers
    - Ensure section headers are on their own line
    - Preserve paragraph breaks
    """
    import re
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Remove leading * or # and any extra surrounding spaces
        stripped = re.sub(r'^[\*#\s]+', '', stripped)
        stripped = re.sub(r'[\*#\s]+$', '', stripped)
        cleaned.append(stripped)
    return "\n".join(cleaned)

def _export_text_to_pdf(text: str, output_path: str, title: str = "Final Paper"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=54, rightMargin=54,
                            topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=12,
        alignment=1  # center
    )
    header_style = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=6,
        textColor="black"
    )
    body_style = ParagraphStyle(
        name="BodyText",
        parent=styles["Normal"],
        alignment=4,  # TA_JUSTIFY
        spaceAfter=6
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    # Clean markdown artifacts
    cleaned = _clean_ai_markdown(text)

    # Split into sections by headers that start with the section name followed by newline
    import re
    parts = re.split(r'(\n(?:Abstract|Introduction|Methods|Results|Discussion|Conclusion|References)\n)', cleaned)
    current_section_content = []
    for part in parts:
        if re.match(r'\n(?:Abstract|Introduction|Methods|Results|Discussion|Conclusion|References)\n', part):
            if current_section_content:
                for line in current_section_content:
                    if line.strip():
                        story.append(Paragraph(line, body_style))
                    else:
                        story.append(Spacer(1, 6))
                story.append(Spacer(1, 12))
            story.append(Paragraph(part.strip(), header_style))
            current_section_content = []
        else:
            current_section_content.extend(part.strip().splitlines())

    if current_section_content:
        for line in current_section_content:
            if line.strip():
                story.append(Paragraph(line, body_style))
            else:
                story.append(Spacer(1, 6))

    doc.build(story)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/search")
def api_search():
    _ensure_dirs()
    payload = request.get_json(force=True)
    topic = (payload.get("topic") or "").strip()
    limit = int(payload.get("limit") or 3)
    limit = max(1, min(limit, 6))

    if not topic:
        return jsonify({"error": "topic is required"}), 400

    papers = fetch_papers(topic, limit=limit)
    meta = save_datasets(papers, _sanitize_topic(topic))
    _write_json(os.path.join(DATA_DIR, "last_search.json"), {"topic": topic, "limit": limit})

    return jsonify({"topic": topic, "limit": limit, "papers": meta})


@app.post("/api/download")
def api_download():
    _ensure_dirs()
    metadata_path = os.path.join(DATASETS_DIR, "papers_metadata.json")
    dataset = _read_json(metadata_path, default=[])
    if not dataset:
        return jsonify({"error": "No papers metadata found. Run /api/search first."}), 400

    download_pdfs(dataset)

    available = []
    for paper in dataset:
        paper_id = paper.get("paper_id")
        if not paper_id:
            continue
        filename = f"{paper_id}.pdf"
        path = os.path.join(PAPERS_DIR, filename)
        available.append({
            "paper_id": paper_id,
            "title": paper.get("title"),
            "has_pdf": os.path.exists(path),
            "download_url": f"/api/papers/{paper_id}.pdf"
        })

    return jsonify({"downloaded": available})


@app.get("/api/papers")
def api_list_papers():
    metadata_path = os.path.join(DATASETS_DIR, "papers_metadata.json")
    dataset = _read_json(metadata_path, default=[])

    response = []
    for paper in dataset:
        paper_id = paper.get("paper_id")
        if not paper_id:
            continue
        filename = f"{paper_id}.pdf"
        response.append({
            "paper_id": paper_id,
            "title": paper.get("title"),
            "year": paper.get("year"),
            "authors": paper.get("authors"),
            "paper_url": paper.get("paper_url"),
            "has_pdf": os.path.exists(os.path.join(PAPERS_DIR, filename)),
            "download_url": f"/api/papers/{paper_id}.pdf"
        })

    return jsonify({"papers": response})


@app.get("/api/papers/<path:filename>")
def api_get_paper(filename):
    _ensure_dirs()
    return send_from_directory(PAPERS_DIR, filename, as_attachment=True)


@app.post("/api/analyze")
def api_analyze():
    _ensure_dirs()

    raw_text = extract_text_from_pdfs(pdf_folder=PAPERS_DIR)
    if not raw_text:
        return jsonify({"error": "No valid PDF text extracted. Try re-downloading papers or ensure PDFs are not corrupted."}), 400

    sectioned_text = split_into_sections(raw_text)
    key_findings = extract_key_findings(sectioned_text)
    similarity = cross_paper_similarity(key_findings)

    common_methods = extract_common_methods(sectioned_text)
    _write_json(os.path.join(ANALYSIS_DIR, "common_methods.json"), common_methods)

    common_datasets = extract_common_datasets(sectioned_text)

    result = {
        "key_findings": key_findings,
        "similarity": similarity,
        "common_methods": common_methods,
        "common_datasets": common_datasets
    }

    skipped_path = os.path.join(EXTRACTED_DIR, "skipped_files.json")
    if os.path.exists(skipped_path):
        skipped = _read_json(skipped_path, default=[])
        if skipped:
            result["skipped"] = skipped

    return jsonify(result)


@app.post("/api/draft")
def api_draft():
    _ensure_dirs()

    payload = request.get_json(silent=True) or {}
    mode = (payload.get("mode") or "full").strip().lower()
    section_name = (payload.get("section_name") or "").strip()
    draft_topic = (payload.get("draft_topic") or "").strip()

    key_findings = _read_json(os.path.join(ANALYSIS_DIR, "key_findings.json"))
    metadata = _read_json(os.path.join(DATASETS_DIR, "papers_metadata.json"))
    sectioned_text = _read_json(os.path.join(EXTRACTED_DIR, "sectioned_text.json"))

    if not key_findings or not metadata or not sectioned_text:
        return jsonify({"error": "Missing analysis inputs. Run /api/analyze first."}), 400

    common_methods = _read_json(os.path.join(ANALYSIS_DIR, "common_methods.json"), default={})
    common_datasets = _read_json(os.path.join(ANALYSIS_DIR, "common_datasets.json"), default={})

    combined_text = synthesize_findings(key_findings)

    valid_sections = ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]

    if mode not in {"full", "section"}:
        return jsonify({"error": "mode must be 'full' or 'section'"}), 400

    if mode == "section":
        if section_name not in valid_sections and section_name != "References":
            return jsonify({"error": f"Invalid section_name. Use one of: {', '.join(valid_sections + ['References'])}"}), 400

    sections = _read_json(os.path.join(ANALYSIS_DIR, "final_review_draft.json"), default={}) or {}

    if mode == "full":
        sections = {}
        for sec in valid_sections:
            sections[sec] = generate_section(
                sec,
                combined_text,
                key_findings,
                common_methods,
                common_datasets,
                draft_topic,
            )
        sections["References"] = format_apa_references(metadata)
    else:
        if section_name == "References":
            sections["References"] = format_apa_references(metadata)
        else:
            sections[section_name] = generate_section(
                section_name,
                combined_text,
                key_findings,
                common_methods,
                common_datasets,
                draft_topic,
            )

        if "References" not in sections:
            sections["References"] = format_apa_references(metadata)

    _write_json(os.path.join(ANALYSIS_DIR, "final_review_draft.json"), sections)

    return jsonify({"draft": sections, "mode": mode, "section_name": section_name})


@app.get("/api/export/draft")
def api_export_draft_pdf():
    _ensure_dirs()
    section = (request.args.get("section") or "").strip()

    draft = _read_json(os.path.join(ANALYSIS_DIR, "final_review_draft.json"))
    if not draft:
        return jsonify({"error": "No draft found. Run /api/draft first."}), 400

    if section:
        if section not in draft:
            return jsonify({"error": "Requested section not present in draft."}), 400
        draft_text = _draft_to_text({section: draft.get(section)})
        filename = f"draft_{section.lower()}.pdf"
        title = f"Draft - {section}"
    else:
        draft_text = _draft_to_text(draft)
        filename = "draft_paper.pdf"
        title = "Draft Paper"

    output_path = os.path.join(EXPORTS_DIR, filename)
    _export_text_to_pdf(draft_text, output_path, title=title)
    return send_file(output_path, as_attachment=True, download_name=filename)


@app.post("/api/revise")
def api_revise():
    _ensure_dirs()
    payload = request.get_json(force=True)
    suggestions = (payload.get("suggestions") or "").strip()

    draft = _read_json(os.path.join(ANALYSIS_DIR, "final_review_draft.json"))
    if not draft:
        return jsonify({"error": "No draft found. Run /api/draft first."}), 400

    draft_text = _draft_to_text(draft)

    prompt = f"""
You are an academic writing assistant.

Revise the following APA-style draft paper based on the user's suggestions.

User suggestions:
{suggestions if suggestions else "(no suggestions provided; improve clarity, coherence, and academic tone)"}

Draft paper:
{draft_text}

Return a revised full paper with the same main sections and an APA academic tone.
""".strip()

    revised_text = generate_with_gemini_flash(prompt)

    revised = {
        "revised_text": revised_text,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    _write_json(os.path.join(ANALYSIS_DIR, "revised_paper.json"), revised)

    return jsonify(revised)


@app.get("/api/export")
def api_export_pdf():
    _ensure_dirs()

    revised = _read_json(os.path.join(ANALYSIS_DIR, "revised_paper.json"))
    if not revised:
        return jsonify({"error": "No revised paper found. Run /api/revise first."}), 400

    text = revised.get("revised_text") or ""
    if not text.strip():
        return jsonify({"error": "Revised paper is empty."}), 400

    output_path = os.path.join(EXPORTS_DIR, "final_paper.pdf")
    _export_text_to_pdf(text, output_path, title="Final Paper")

    return send_file(output_path, as_attachment=True, download_name="final_paper.pdf")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
