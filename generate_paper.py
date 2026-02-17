from groq import Groq
import os
import json

"""
Groq API key handling:
- Prefer a local app_secrets module with GROQ_API_KEY, if present.
- Fallback to the GROQ_API_KEY environment variable.
"""

try:
    from app_secrets import GROQ_API_KEY  # type: ignore
except ImportError:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Please create an 'app_secrets.py' file with "
        "GROQ_API_KEY = 'your_key' or set the GROQ_API_KEY environment variable."
    )

client = Groq(api_key=GROQ_API_KEY)

def load_all_findings_with_metadata():
    combined = ""

    for file in os.listdir("data/dist_texts"):
        if not file.endswith("_findings.txt"):
            continue

        paper_id = file.replace("_findings.txt", "")

        # load metadata (you already have this from Step 0)
        meta_path = f"data/metadata/{paper_id}.json"
        findings_path = f"data/dist_texts/{file}"

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
        raise ValueError("No key findings found. Cannot generate synthesized paper.")
    prompt = f"""
You are an academic research assistant.

Using the following key findings extracted from multiple research papers
on the same topic, generate a SINGLE synthesized research paper draft based ONLY on the provided content.

The paper MUST contain exactly these sections, in this order:
1. Title Page (paper title and optional author/affiliation line; keep brief)
2. Abstract (summary of the paper)
3. Introduction (context and objectives)
4. Method (or Methodology; approach used)
5. Results (findings)
6. Discussion (interpretation and implications)
7. References (APA style)

Rules:
- Do not invent new information.
- Base everything strictly on the input.
- Use academic tone.

STRICT CONSTRAINTS:
- Do NOT include any numerical values, percentages, counts, model sizes, 
  dataset sizes, hardware specifications, table numbers, or metric values.
- Replace quantitative claims with qualitative academic language.
- Treat this as a synthesis of prior work, NOT a new experiment.
- Do NOT use first-person language ("we", "our").
- Do NOT use Markdown formatting (e.g. **bold** or **Title:**). Use plain text only.

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

if __name__ == "__main__":
    paper = generate_synthesized_paper()

    os.makedirs("data/output", exist_ok=True)

    with open("data/output/synthesized_paper.txt", "w", encoding="utf-8") as f:
        f.write(paper)

    print("Synthesized research paper generated successfully.")