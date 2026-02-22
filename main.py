import os

from paper_fetcher import fetch_papers
from pdf_downloader import download_pdfs
from pdf_text_extractor import extract_text_from_pdf
from key_finder import extract_key_findings
from similarity_analyzer import compute_similarity
from dataset_builder import save_dataset
from analysis_synthesizer import combine_all_findings
from section_writer import generate_full_paper
from extract_common_terms import extract_common_terms
from similarity_report import generate_similarity_report
from critique_module import critique_paper, revise_paper


# ==========================================================
# CORE PIPELINE LOGIC (UI Compatible)
# ==========================================================
def run_pipeline_logic(topic, num_papers, user_extra_findings=""):
    """
    Full research pipeline:
    Milestone 1 → Fetch papers
    Milestone 2 → Extract + similarity
    Milestone 3 → Generate paper
    Milestone 4 → Critique
    """

    try:
        # -------------------------
        # Milestone 1: Fetch Papers
        # -------------------------
        papers = fetch_papers(topic, max_results=int(num_papers))

        if not papers:
            return "No papers found.", "No similarity report.", "No critique.", ""

        download_pdfs(papers)
        save_dataset(papers)

        # -------------------------
        # Milestone 2: Extraction + Similarity
        # -------------------------
        all_findings = []

        for paper in papers:
            if "local_path" not in paper:
                continue

            text = extract_text_from_pdf(paper["local_path"], paper["paperId"])

            if not text:
                continue

            findings = extract_key_findings(text)
            combined = " ".join(findings)

            if combined.strip():
                all_findings.append(combined)

        if not all_findings:
            return "No extractable findings found.", "No similarity report.", "No critique.", ""

        similarity_matrix = compute_similarity(all_findings)
        similarity_report_text = generate_similarity_report(similarity_matrix)

        if similarity_report_text is None:
            similarity_report_text = "Similarity report generated but no text returned."

        # -------------------------
        # Milestone 3: Paper Generation
        # -------------------------
        findings_text = combine_all_findings(all_findings)

        if user_extra_findings:
            findings_text += " " + user_extra_findings

        full_paper = generate_full_paper(findings_text)

        # Save generated paper
        os.makedirs("data/output", exist_ok=True)
        with open("data/output/final_paper.txt", "w", encoding="utf-8") as f:
            f.write(full_paper)

        # -------------------------
        # Milestone 4: Quality Evaluation
        # -------------------------
        critique_text = critique_paper(full_paper)

        with open("data/output/critique.txt", "w", encoding="utf-8") as f:
            f.write(critique_text)

        # -------------------------
        # Extract Common Terms
        # -------------------------
        extract_common_terms()

        return full_paper, similarity_report_text, critique_text, "Common terms extracted successfully."

    except Exception as e:
        return f"Error occurred: {str(e)}", "", "", ""


# ==========================================================
# REVISION FUNCTION (UI Button Use)
# ==========================================================
def revise_generated_paper(original_paper, critique_text):
    """
    Applies revision based on critique feedback.
    """

    try:
        revised = revise_paper(original_paper, critique_text)

        os.makedirs("data/output", exist_ok=True)
        with open("data/output/revised_paper.txt", "w", encoding="utf-8") as f:
            f.write(revised)

        return revised

    except Exception as e:
        return f"Revision failed: {str(e)}"


# ==========================================================
# CLI FALLBACK (Optional)
# ==========================================================
if __name__ == "__main__":

    topic = input("Enter research topic: ")
    num = int(input("How many papers to fetch? "))
    extra = input("Optional extra findings (press Enter to skip): ")

    paper, sim_report, critique, status = run_pipeline_logic(topic, num, extra)

    print("\n--- Similarity Report ---\n")
    print(sim_report)

    print("\n--- Generated Paper (Preview) ---\n")
    print(paper[:1000])  # preview first 1000 chars

    print("\n--- Critique ---\n")
    print(critique)

    print("\n--- Status ---\n")
    print(status)
