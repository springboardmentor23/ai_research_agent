from src.draft_generator.gpt_client import generate_with_gemini
import json

def generate_draft(patterns: dict, key_findings: dict) -> str:

    # Convert to shorter summaries
    pattern_summary = "\n".join(
        f"- {k}: {v}" for k, v in patterns.items()
    )

    findings_summary = "\n".join(
        f"- {k}: {v}" for k, v in key_findings.items()
    )

    prompt = f"""
You are an academic research assistant.

Using the synthesized research insights below, write a structured academic draft with:
- Abstract
- Methods
- Results

Rules:
- Use APA-style academic tone
- Synthesize findings across papers
- Do NOT invent citations
- Keep language formal and neutral

Common Patterns:
{pattern_summary}

Key Findings:
{findings_summary}
"""

    print("Prompt length:", len(prompt))

    return generate_with_gemini(prompt)
