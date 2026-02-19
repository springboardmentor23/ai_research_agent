def evaluate_quality(draft_text: str) -> dict:
    """
    Simple scoring evaluation for mentor presentation.
    """

    word_count = len(draft_text.split())

    score = 0

    if "abstract" in draft_text.lower():
        score += 20
    if "methods" in draft_text.lower():
        score += 20
    if "results" in draft_text.lower():
        score += 20
    if word_count > 250:
        score += 20
    if word_count > 400:
        score += 20

    return {
        "word_count": word_count,
        "quality_score_out_of_100": score,
        "remarks": "Higher score indicates better structure and completeness."
    }
