import gradio as gr
import subprocess
import os

def run_pipeline(topic, num_papers):
    command = f'python main.py'
    subprocess.run(command, shell=True)

    if os.path.exists("final_review.txt"):
        with open("final_review.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "Paper generation failed."

def run_review():
    command = f'python review_module.py'
    subprocess.run(command, shell=True)

    review_text = ""
    revised_text = ""

    if os.path.exists("review_report.txt"):
        with open("review_report.txt", "r", encoding="utf-8") as f:
            review_text = f.read()

    if os.path.exists("revised_paper.txt"):
        with open("revised_paper.txt", "r", encoding="utf-8") as f:
            revised_text = f.read()

    return review_text, revised_text

with gr.Blocks() as app:

    gr.Markdown("# AI System to Automatically Review and Summarize Research Papers")

    topic = gr.Textbox(label="Enter Research Topic")
    num_papers = gr.Number(label="Number of Papers", value=3)

    generate_btn = gr.Button("Generate Paper")
    paper_output = gr.Textbox(label="Generated Paper", lines=20)

    review_btn = gr.Button("Review Paper")
    review_output = gr.Textbox(label="Review Report", lines=15)
    revised_output = gr.Textbox(label="Revised Paper", lines=20)

    generate_btn.click(run_pipeline, inputs=[topic, num_papers], outputs=paper_output)
    review_btn.click(run_review, inputs=[], outputs=[review_output, revised_output])

app.launch()
