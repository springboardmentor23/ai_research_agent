import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def critique_paper(paper_text):
    """
    Evaluates the generated research paper and
    provides structured critique and quality scores.
    """

    prompt = f"""
    You are an academic research reviewer.

    Evaluate the following research paper based on:

    1. Clarity
    2. Structure
    3. Logical flow
    4. Depth of analysis
    5. Academic tone
    6. Completeness of sections

    Provide:
    - Strengths
    - Weaknesses
    - Specific improvement suggestions
    - Overall quality score (1-10)

    Research Paper:
    {paper_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

def revise_paper(original_text, critique_text):
    """
    Revises the research paper based on critique feedback.
    """

    prompt = f"""
    Improve the following research paper based on
    the provided critique and suggestions.

    Critique:
    {critique_text}

    Original Paper:
    {original_text}

    Produce a fully revised improved version.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
