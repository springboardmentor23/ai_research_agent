import json
import textwrap
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ============================
# CONFIG
# ============================

INPUT_FILE = "common_results.json"
EXTRACTED_FOLDER = "extracted_texts"
OUTPUT_FILE = "final_review.txt"
WRAP_WIDTH = 80

# ============================
# LOAD API KEY
# ============================

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
else:
    model = None

# ============================
# LOAD COMMON RESULTS
# ============================

def load_common_results():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================
# TEXT WRAP
# ============================

def wrap(text):
    return textwrap.fill(text.strip(), width=WRAP_WIDTH)

# ============================
# SIMPLE APA REFERENCES FROM FILE NAMES
# ============================

def format_references():

    if not os.path.exists(EXTRACTED_FOLDER):
        return "No references available."

    references = []
    files = os.listdir(EXTRACTED_FOLDER)

    for file in files:
        if file.endswith(".txt"):
            title = file.replace(".txt", "").replace("_", " ")
            reference = f"{title}. (n.d.). Retrieved research paper."
            references.append(reference)

    if not references:
        return "No references available."

    return "\n".join(references)

# ============================
# LOCAL GENERATION
# ============================

def generate_local_paper(data):

    datasets = ", ".join(data.get("common_datasets", []))
    methods = ", ".join(data.get("common_methods", []))
    algorithms = ", ".join(data.get("common_algorithms", []))
    findings = ". ".join(data.get("common_key_findings", []))

    title = "AI-Based Review of Selected Research Papers"

    abstract = f"""
This paper presents a structured review of selected research studies.
Common datasets include {datasets}. Frequently used methods include
{methods} and algorithms such as {algorithms}. The overall findings
indicate that {findings}.
"""

    words = abstract.split()
    if len(words) > 100:
        abstract = " ".join(words[:100])

    paper = f"""
{title}

ABSTRACT
{wrap(abstract)}

1. Introduction
{wrap("This study reviews selected research papers and summarizes major technological trends and methodological approaches.")}

2. Methods

2.1 Datasets
{wrap(f"The primary datasets identified across studies include {datasets}.")}

2.2 Algorithms
{wrap(f"The most commonly used algorithms include {algorithms}.")}

2.3 Analytical Approach
{wrap(f"The research methods primarily involve {methods}, enabling structured comparative analysis.")}

3. Results

3.1 Key Findings
{wrap(findings)}

3.2 Cross-Paper Comparison
{wrap("Comparative analysis reveals common methodological trends and recurring experimental strategies across the selected papers.")}

4. Conclusion
{wrap("The reviewed studies demonstrate consistent research trends and methodological alignment. Future work should focus on deeper domain-specific validation and optimization.")}

5. References
{format_references()}
"""

    return paper.strip()

# ============================
# AI GENERATION
# ============================

def generate_ai_paper(data, custom_prompt=""):

    if model is None:
        return None

    prompt = f"""
You are an academic research writer.

Strictly generate a structured research paper.
Return ONLY the paper content.

FORMAT:

TITLE

ABSTRACT (maximum 100 words)

1. Introduction

2. Methods
   2.1 Datasets
   2.2 Algorithms
   2.3 Analytical Approach

3. Results
   3.1 Key Findings
   3.2 Cross-Paper Comparison

4. Conclusion

5. References

Use the following extracted information:

Datasets: {data.get("common_datasets")}
Methods: {data.get("common_methods")}
Algorithms: {data.get("common_algorithms")}
Key Findings: {data.get("common_key_findings")}

Additional instruction: {custom_prompt}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

# ============================
# MAIN GENERATION FUNCTION (UI USE)
# ============================

def generate_paper(mode="local", custom_prompt=""):

    data = load_common_results()

    if mode.lower() == "api":
        paper = generate_ai_paper(data, custom_prompt)
        if paper is None:
            paper = generate_local_paper(data)
    else:
        paper = generate_local_paper(data)

    wrapped_output = "\n".join([wrap(line) for line in paper.split("\n")])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(wrapped_output)

    return wrapped_output
