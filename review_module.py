def evaluate_quality(text):
    issues = []

    if len(text.split()) < 50:
        issues.append("Text is too short.")

    if "not found" in text.lower():
        issues.append("Some sections contain missing information.")

    if text.count("Key results") > 5:
        issues.append("Possible repetition detected.")

    if not issues:
        issues.append("Content quality looks good.")

    return issues


def suggest_revisions(issues):
    suggestions = []

    for issue in issues:
        if "too short" in issue:
            suggestions.append("Expand the section with more details.")
        elif "missing" in issue:
            suggestions.append("Improve extraction logic or select better papers.")
        elif "repetition" in issue:
            suggestions.append("Condense repeated statements.")
        else:
            suggestions.append("No major revisions needed.")

    return suggestions


def revise_text(text):
    # Simple refinement (placeholder for AI rewrite)
    improved = text.replace("Key results", "Major findings")
    return improved
