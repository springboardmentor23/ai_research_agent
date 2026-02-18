import os
import google.generativeai as genai


class MethodsGenerator:
    def __init__(self):
        """
        Initialize Gemini model using API key from environment variables.
        """

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config={
                "temperature": 0.3,   # lower = more academic + less creative
                "max_output_tokens": 1200,
            }
        )

    def generate(self, methods_data: str) -> str:
        """
        Generate a comparative Methods section from synthesized multi-paper methods content.

        Parameters:
        methods_data (str): Combined methodologies extracted from multiple research papers.

        Returns:
        str: Structured academic Methods comparison section.
        """

        if not methods_data or len(methods_data.strip()) < 50:
            raise ValueError("Insufficient methods data provided.")

        prompt = f"""
        You are an academic research analyst writing a literature review.

        Based on the following extracted methodology sections from multiple research papers,
        write a structured comparative Methods section.

        The section must include:

        1. Overview of methodological approaches across studies
        2. Common techniques or frameworks used
        3. Differences in experimental design
        4. Datasets used and evaluation metrics (if mentioned)
        5. Strengths and limitations observed
        6. Emerging methodological trends

        Requirements:
        - Formal academic tone
        - Paragraph format (no bullet points)
        - Analytical comparison (not just summarization)
        - Do NOT invent missing information
        - Do NOT hallucinate datasets or metrics
        - Avoid repetition

        Extracted Methods Data:
        {methods_data}
        """

        try:
            response = self.model.generate_content(prompt)

            if response and hasattr(response, "text"):
                return response.text.strip()

            return "Methods section generation failed: Empty response."

        except Exception as e:
            return f"Methods section generation failed: {str(e)}"
