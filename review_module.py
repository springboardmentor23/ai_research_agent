import os
from dotenv import load_dotenv
import google.generativeai as genai
import textwrap

# ============================
# CONFIG
# ============================

INPUT_FILE = "final_review.txt"
REVIEW_FILE = "review_report.txt"
REVISED_FILE = "revised_paper.txt"
WRAP_WIDTH = 80

# ============================
# LOAD API
# ============================

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ============================
# TEXT WRAP
# ============================

def wrap(text):
    return textwrap.fill(text.strip(), width=WRAP_WIDTH)

# ============================
# LOAD PAPER
# ============================

def load_paper():
    if not os.path.exists(INPUT_FILE):
        print("❌ final_review.txt not found")
        exit()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.read()

# ============================
# REVIEW FUNCTION
# ============================

def review_paper():

    paper = load_paper()

    prompt = f"""
You are an academic research reviewer.

Review the following research paper draft.

Evaluate:

1. Structure completeness (Title, Abstract, Introduction, Methods, Results, Conclusion, References)
2. Academic tone
3. Clarity and coherence
4. APA formatting correctness
5. Logical flow
6. Overall quality score (0–10)

Return your response in the following format:

=== REVIEW REPORT ===

Strengths:
...

Weaknesses:
...

Suggestions for Improvement:
...

Quality Score: X/10

=== REVISED VERSION ===

(Provide a fully revised improved version of the paper below)

Paper:
{paper}
"""

    response = model.generate_content(prompt)
    output = response.text

    # Split review and revised content
    if "=== REVISED VERSION ===" in output:
        review_part, revised_part = output.split("=== REVISED VERSION ===", 1)
    else:
        review_part = output
        revised_part = ""

    # Save review report
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        f.write(wrap(review_part))

    # Save revised paper
    if revised_part.strip():
        wrapped_revised = "\n".join([wrap(line) for line in revised_part.split("\n")])
        with open(REVISED_FILE, "w", encoding="utf-8") as f:
            f.write(wrapped_revised)

    print("✅ review_report.txt generated")
    if revised_part.strip():
        print("✅ revised_paper.txt generated")

# ============================
# RUN
# ============================

if __name__ == "__main__":
    review_paper()
