# src/synthesis.py

def synthesize_findings(papers):
    """
    Combine insights from multiple papers into a unified synthesis.
    """

    if not papers:
        return "No papers available for synthesis."

    synthesis = "This section synthesizes findings across multiple studies.\n\n"

    for idx, paper in enumerate(papers, start=1):
        title = paper.get("title", "Unknown Title")
        year = paper.get("year", "Unknown Year")

        synthesis += (
            f"Study {idx} ({year}) titled '{title}' "
            "contributes insights relevant to the research topic.\n"
        )

    return synthesis
