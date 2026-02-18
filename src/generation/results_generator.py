import os
import google.generativeai as genai


class ResultsGenerator:
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
                "temperature": 0.2,   # very low = analytical, less creative
                "max_output_tokens": 1200,
            }
        )

    def generate(self, results_data: str) -> str:
        """
        Generate a synthesized Results section from multiple research papers.

        Parameters:
        results_data (str): Combined results extracted from multiple research papers.

        Returns:
        str: Structured academic Results synthesis section.
        """

        if not results_data or len(results_data.strip()) < 50:
            raise ValueError("Insufficient results data provided.")

        prompt = f"""
        You are an academic research analyst writing a comparative literature review.

        Based on the following extracted results from multiple research papers,
        write a structured Results section that synthesizes findings across studies.

        The section must include:

        1. Major performance trends observed across papers
        2. Consistent findings or agreement among studies
        3. Contradictions or conflicting results (if present)
        4. Quantitative improvements (only if explicitly mentioned)
        5. Performance metrics discussed (e.g., accuracy, F1-score, BLEU, etc.)
        6. Interpretation of why certain approaches perform better

        Important Rules:
        - Do NOT invent numerical values.
        - Do NOT fabricate datasets or metrics.
        - Only use information present in the provided content.
        - Maintain formal academic tone.
        - Write in paragraph format (no bullet points).
        - Avoid repetition.

        Extracted Results Data:
        {results_data}
        """

        try:
            response = self.model.generate_content(prompt)

            if response and hasattr(response, "text"):
                return response.text.strip()

            return "Results section generation failed: Empty response."

        except Exception as e:
            return f"Results section generation failed: {str(e)}"
