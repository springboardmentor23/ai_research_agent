from src.generation.synthesizer import Synthesizer
from src.generation.abstract_generator import AbstractGenerator
from src.generation.methods_generator import MethodsGenerator
from src.generation.results_generator import ResultsGenerator


class ReportGenerator:
    """
    Orchestrates AI-based section generation.
    """

    def __init__(self, papers):
        self.papers = papers
        self.synthesizer = Synthesizer(papers)

    def generate_sections(self):
        """
        Generate abstract, methods, and results sections.
        """

        # Prepare synthesized data
        combined_findings = self.synthesizer.combine_key_findings()
        combined_methods = self.synthesizer.combine_methods()
        combined_results = self.synthesizer.combine_results()

        # Generate sections
        abstract = AbstractGenerator().generate(combined_findings)
        methods = MethodsGenerator().generate(combined_methods)
        results = ResultsGenerator().generate(combined_results)

        return {
            "abstract": abstract,
            "methods": methods,
            "results": results
        }
