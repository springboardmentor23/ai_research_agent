from typing import List, Dict


class ReferenceFormatter:
    """
    Formats paper metadata into APA-style references.
    """

    def __init__(self, metadata_list: List[Dict]):
        """
        metadata_list should contain dictionaries like:

        {
            "authors": ["Author One", "Author Two"],
            "year": "2023",
            "title": "Paper Title",
            "journal": "Journal Name",
            "volume": "12",
            "issue": "3",
            "pages": "123-135",
            "doi": "https://doi.org/xxxxx"
        }
        """
        self.metadata_list = metadata_list

    def _format_authors(self, authors: List[str]) -> str:
        """
        Convert list of author names into APA format.
        Example:
        ["John Smith", "Alice Brown"]
        → "Smith, J., & Brown, A."
        """

        formatted_authors = []

        for author in authors:
            parts = author.strip().split()
            if len(parts) == 1:
                formatted_authors.append(parts[0])
            else:
                last_name = parts[-1]
                initials = " ".join([p[0] + "." for p in parts[:-1]])
                formatted_authors.append(f"{last_name}, {initials}")

        if len(formatted_authors) == 1:
            return formatted_authors[0]

        return ", ".join(formatted_authors[:-1]) + ", & " + formatted_authors[-1]

    def format_references(self) -> List[str]:
        """
        Generate APA formatted references.
        """

        references = []

        for paper in self.metadata_list:
            authors = self._format_authors(paper.get("authors", []))
            year = paper.get("year", "n.d.")
            title = paper.get("title", "")
            journal = paper.get("journal", "")
            volume = paper.get("volume", "")
            issue = paper.get("issue", "")
            pages = paper.get("pages", "")
            doi = paper.get("doi", "")

            reference = f"{authors} ({year}). {title}. {journal}"

            if volume:
                reference += f", {volume}"

            if issue:
                reference += f"({issue})"

            if pages:
                reference += f", {pages}"

            reference += "."

            if doi:
                reference += f" {doi}"

            references.append(reference)

        return references
