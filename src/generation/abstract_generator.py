import os
import google.generativeai as genai


class AbstractGenerator:
    def __init__(self):
        """
        Initialize Gemini model using API key from environment variables.
        """
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate(self, synthesized_text: str) -> str:
        """
        Generate a structured academic abstract from synthesized multi-paper content.

        Parameters:
        synthesized_text (str): Combined insights from multiple research papers.

        Returns:
        str: Structured academic abstract.
        """

        if not synthesized_text or len(synthesized_text.strip()) < 50:
            raise ValueError("Insufficient content provided for abstract generation.")

        prompt = f"""
        You are an academic research writer.

        Based on the synthesized findings from multiple research papers below,
        write a structured and formal academic abstract.

        The abstract must include:

        1. Background – Introduce the research domain and its importance.
        2. Objective – State the purpose of the comparative review.
        3. Methods Overview – Briefly summarize methodologies across studies.
        4. Key Results – Highlight major trends, improvements, and findings.
        5. Conclusion – Provide an overall insight and future direction.

        Requirements:
        - Formal academic tone
        - 200–300 words
        - No bullet points
        - No repetition
        - No hallucinated references
        - Do not invent new studies

        Synthesized Content:
        {synthesized_text}
        """

        try:
            response = self.model.generate_content(prompt)

            if response and hasattr(response, "text"):
                return response.text.strip()

            return "Abstract generation failed: Empty response."

        except Exception as e:
            return f"Abstract generation failed: {str(e)}"
