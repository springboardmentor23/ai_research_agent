def combine_all_findings(findings_list):
    """
    Combines all extracted key findings into a single
    synthesized text block for Milestone 3 generation.

    Parameters:
        findings_list (list): List of combined findings per paper

    Returns:
        str: One large combined findings string
    """

    if not findings_list:
        return ""

    # Remove empty entries
    cleaned = [f for f in findings_list if f.strip()]

    combined_text = " ".join(cleaned)

    return combined_text.strip()
