import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


# Make sure GEMINI_API_KEY is set in environment
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_full_paper(findings_text):
    """
    Generates a complete academic research paper
    in a single Gemini API call.
    """

    prompt = f"""
    Using the following synthesized research findings,
    generate a complete academic research paper with the
    following structured headings:

    Title
    Abstract
    Introduction
    Methods
    Results
    Discussion
    Conclusion
    References (APA format)

    Ensure the paper is formal, academic, and cohesive.
    Avoid markdown symbols. Use proper paragraph formatting.

    Research Findings:
    {findings_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
