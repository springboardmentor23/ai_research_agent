import os
import json
from google import genai
from google.genai import types

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options=types.HttpOptions(api_version="v1")
)

def generate_draft(prompt):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def main():
    #  data from previous milestones
    with open("common_findings.json", "r", encoding="utf-8") as f:
        common_findings = json.load(f)

    with open("papers_dataset.json", "r", encoding="utf-8") as f:
        papers = json.load(f)

    # Prompt 
    prompt = f"""
    You are an academic writing assistant.

    COMMON RESEARCH FINDINGS (from multiple papers):
    {json.dumps(common_findings, indent=2)}

    PAPER METADATA:
    {json.dumps(papers, indent=2)}

    TASK:
    Write a structured research paper draft with the following sections:
    1. Abstract
    2. Methodology
    3. Results
    4. References (APA 7th Edition)

    Use a formal academic tone suitable for undergraduate research.
    """

    draft = generate_draft(prompt)

    with open("research_paper_draft.txt", "w", encoding="utf-8") as f:
        f.write(draft)

    print("Generated successfully using gemini-2.5-flash.")


if __name__ == "__main__":
    main()
