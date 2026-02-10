import json
import textwrap
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ============================
# CONFIG
# ============================

INPUT_FILE = "common_results.json"
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

def wrap_text(text):
    return textwrap.fill(text.strip(), width=WRAP_WIDTH)

# ============================
# LOCAL GENERATION
# ============================

def generate_local_paper(data):

    datasets = data.get("common_datasets", [])
    methods = data.get("common_methods", [])
    algorithms = data.get("common_algorithms", [])
    findings = data.get("common_key_findings", [])

    user_prompt = input("\nEnter additional instruction (press Enter to skip): ")

    abstract = f"""
This paper presents a comprehensive review of recent research works.
Common datasets include {', '.join(datasets)}.
Methods such as {', '.join(methods)} and algorithms like {', '.join(algorithms)}
are widely used. The findings indicate that {', '.join(findings)}.
"""

    introduction = f"""
Recent advancements have increased interest in this domain.
{user_prompt}
This paper summarizes major trends and techniques.
"""

    methods_section = f"""
Most studies employ methods such as {', '.join(methods)}.
Popular algorithms include {', '.join(algorithms)}.
Datasets commonly used include {', '.join(datasets)}.
"""

    results_section = f"""
Key findings across papers:
{'. '.join(findings)}.
"""

    conclusion = """
This review highlights major research trends and future directions.
"""

    paper = (
        "ABSTRACT\n" + wrap_text(abstract) +
        "\n\nINTRODUCTION\n" + wrap_text(introduction) +
        "\n\nMETHODS\n" + wrap_text(methods_section) +
        "\n\nRESULTS\n" + wrap_text(results_section) +
        "\n\nCONCLUSION\n" + wrap_text(conclusion)
    )

    return paper

# ============================
# AI GENERATION
# ============================

def generate_ai_paper(data):

    if model is None:
        print("❌ Gemini API key not found")
        return None

    user_prompt = input("\nEnter additional instruction (press Enter to skip): ")

    prompt = f"""
You are an academic research writer.

Using the following information:

Datasets: {data.get("common_datasets")}
Methods: {data.get("common_methods")}
Algorithms: {data.get("common_algorithms")}
Key Findings: {data.get("common_key_findings")}

User instruction:
{user_prompt}

Generate a research paper with sections:
Abstract, Introduction, Methods, Results, Conclusion.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ AI generation failed:", e)
        return None

# ============================
# MAIN ENTRY
# ============================

def generate_paper():

    data = load_common_results()

    print("\nChoose paper generation mode:")
    print("1 → Local Template")
    print("2 → AI (Gemini)")
    choice = input("Enter choice: ")

    if choice == "2":
        paper = generate_ai_paper(data)
        if paper is None:
            print("Falling back to local generation...")
            paper = generate_local_paper(data)
    else:
        paper = generate_local_paper(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(wrap_text(paper))

    print("✅ final_review.txt generated")

# ============================
# RUN
# ============================

if __name__ == "__main__":
    generate_paper()
