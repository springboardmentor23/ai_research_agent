from typing import List, Dict


class Synthesizer:
    """
    Responsible for combining and preparing extracted paper data
    for section generation (Abstract, Methods, Results).
    """

    def __init__(self, papers: List[Dict]):
        """
        papers: List of dictionaries.
        Each dictionary should contain:
        {
            "title": str,
            "methods": str,
            "results": str,
            "key_findings": str,
            "metadata": dict
        }
        """
        self.papers = papers

    def _clean_text(self, text: str) -> str:
        """
        Basic cleaning to remove excessive whitespace and invalid text.
        """
        if not text:
            return ""

        return " ".join(text.split())

    def combine_methods(self) -> str:
        """
        Combine methodology sections from all papers.
        """
        combined = ""

        for paper in self.papers:
            title = paper.get("title", "Unknown Title")
            methods = self._clean_text(paper.get("methods", ""))

            if methods:
                combined += f"\nPaper: {title}\nMethods: {methods}\n"

        return combined.strip()

    def combine_results(self) -> str:
        """
        Combine results sections from all papers.
        """
        combined = ""

        for paper in self.papers:
            title = paper.get("title", "Unknown Title")
            results = self._clean_text(paper.get("results", ""))

            if results:
                combined += f"\nPaper: {title}\nResults: {results}\n"

        return combined.strip()

    def combine_key_findings(self) -> str:
        """
        Combine key findings for abstract generation.
        """
        combined = ""

        for paper in self.papers:
            title = paper.get("title", "Unknown Title")
            findings = self._clean_text(paper.get("key_findings", ""))

            if findings:
                combined += f"\nPaper: {title}\nKey Findings: {findings}\n"

        return combined.strip()

    def extract_metadata(self) -> List[Dict]:
        """
        Collect metadata for reference formatting.
        """
        metadata_list = []

        for paper in self.papers:
            metadata = paper.get("metadata", {})
            if metadata:
                metadata_list.append(metadata)

        return metadata_list
