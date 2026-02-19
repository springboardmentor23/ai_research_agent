def build_gpt_prompt(patterns, key_findings):
    return f"""
You are an academic research assistant.

Using the information below:
- Common datasets
- Common methods
- Common algorithms
- Extracted key findings

Write a structured research paper draft with the following sections:
1. Abstract
2. Methods
3. Results

Rules:
- Use formal academic tone
- No assumptions beyond given data
- Write references in APA style
- Avoid plagiarism
- Clearly synthesize findings across papers

Common Patterns:
{patterns}

Key Findings:
{key_findings}
"""
