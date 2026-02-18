from typing import Dict, List
from datetime import datetime


class ReportBuilder:
    """
    Responsible for assembling the final research report
    from generated sections and formatted references.
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.generated_date = datetime.now().strftime("%B %d, %Y")

    def build_report(self, sections: Dict[str, str], references: List[str]) -> str:
        """
        Combine all generated sections into a formatted research report.

        Parameters:
        sections: {
            "abstract": str,
            "methods": str,
            "results": str
        }

        references: List of APA formatted references

        Returns:
        str: Final formatted report
        """

        report = f"""
============================================================
AI-GENERATED LITERATURE REVIEW REPORT
============================================================

Topic: {self.topic}
Generated on: {self.generated_date}

------------------------------------------------------------
ABSTRACT
------------------------------------------------------------

{sections.get("abstract", "Abstract not available.")}


------------------------------------------------------------
METHODS
------------------------------------------------------------

{sections.get("methods", "Methods section not available.")}


------------------------------------------------------------
RESULTS
------------------------------------------------------------

{sections.get("results", "Results section not available.")}


------------------------------------------------------------
REFERENCES
------------------------------------------------------------

"""

        if references:
            for ref in references:
                report += ref + "\n"
        else:
            report += "No references available.\n"

        return report.strip()

    def save_to_txt(self, report: str, filename: str = "final_report.txt") -> None:
        """
        Save report to a text file.
        """

        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"Report successfully saved as {filename}")
