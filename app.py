import json
import gradio as gr

from writing_module import (
    generate_abstract,
    generate_methods_comparison,
    generate_results_synthesis,
    format_apa_references
)

from review_module import (
    evaluate_quality,
    suggest_revisions,
    revise_text
)

from report_generator import build_final_report


# ---------- Load data ----------

with open("analysis_dataset.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

with open("research_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)


# ---------- Core pipeline ----------

def generate_review():
    abstract = generate_abstract(papers)
    methods = generate_methods_comparison(papers)
    results = generate_results_synthesis(papers)
    references = format_apa_references(dataset)

    report = build_final_report(abstract, methods, results, references)

    return abstract, methods, results, references, report


def critique_and_revise(abstract, methods, results):
    combined = abstract + methods + results

    issues = evaluate_quality(combined)
    suggestions = suggest_revisions(issues)

    revised = revise_text(combined)

    return "\n".join(issues), "\n".join(suggestions), revised


# ---------- Gradio UI ----------

with gr.Blocks(title="AI Research Review System") as app:

    gr.Markdown("# 🧠 AI Research Review Generator")

    generate_btn = gr.Button("Generate Review")

    abstract_box = gr.Textbox(label="Abstract")
    methods_box = gr.Textbox(label="Methods Comparison")
    results_box = gr.Textbox(label="Results Synthesis")
    refs_box = gr.Textbox(label="APA References")
    report_box = gr.Textbox(label="Final Report", lines=12)

    critique_btn = gr.Button("Critique / Revise")

    issues_box = gr.Textbox(label="Quality Issues")
    suggestions_box = gr.Textbox(label="Revision Suggestions")
    revised_box = gr.Textbox(label="Revised Text", lines=10)


    generate_btn.click(
        generate_review,
        outputs=[
            abstract_box,
            methods_box,
            results_box,
            refs_box,
            report_box
        ]
    )

    critique_btn.click(
        critique_and_revise,
        inputs=[abstract_box, methods_box, results_box],
        outputs=[issues_box, suggestions_box, revised_box]
    )


app.launch()
