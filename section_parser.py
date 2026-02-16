def split_into_sections(text):
    sections = {}
    
    keywords = [
        "abstract",
        "introduction",
        "method",
        "results",
        "discussion",
        "conclusion"
    ]

    lower_text = text.lower()

    for key in keywords:
        idx = lower_text.find(key)
        if idx != -1:
            sections[key] = text[idx: idx + 2000]  # sample chunk

    return sections
