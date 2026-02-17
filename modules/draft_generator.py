from modules.gemini_flash_client import generate_with_gemini_flash

def generate_section(
    section_name,
    combined_text,
    key_findings,
    common_methods,
    common_datasets,
    draft_topic=""
):
    prompt = f"""
    You are an academic research assistant.

    Use the following information to write the {section_name}:

    Topic:
    {draft_topic or "General research synthesis"}

    Key Findings:
    {key_findings}

    Common Methods:
    {common_methods}

    Common Datasets:
    {common_datasets}

    External Observations:
    - Methods are diverse
    - No single dominant architecture

    Write in APA academic style.
    """

    return generate_with_gemini_flash(prompt)
