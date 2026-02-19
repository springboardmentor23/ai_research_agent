from src.draft_generator.gpt_client import generate_with_gemini


def generate_critique(draft_text: str) -> str:
    """
    Generates critique suggestions using Gemini.
    """

    prompt = f"""
You are an expert academic mentor.

Critically review the following draft and provide improvement suggestions.

Your critique must cover:
1. Academic tone
2. Missing details
3. Logical flow
4. Repetition removal
5. APA style improvements

Return output in bullet points.

Draft:
{draft_text}
"""

    return generate_with_gemini(prompt)
