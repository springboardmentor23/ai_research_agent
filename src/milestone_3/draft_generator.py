from src.milestone_3.gpt_client import generate_with_gemini
import json

def generate_draft(patterns: dict, key_findings: dict) -> str:
    prompt = f"""
You are an academic research assistant.

Using the information below, write a structured academic draft with:
- Abstract
- Methods
- Results

Rules:
- Use APA-style academic tone
- Synthesize findings across papers
- Do NOT invent citations
- Keep language formal and neutral

Common Patterns:
{json.dumps(patterns, indent=2)}

Key Findings:
{json.dumps(key_findings, indent=2)}
"""

    return generate_with_gemini(prompt)
