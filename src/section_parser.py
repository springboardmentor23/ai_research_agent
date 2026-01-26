def extract_sections(text):
    sections = {
        "abstract": "",
        "introduction": "",
        "methodology": "",
        "results": "",
        "conclusion": ""
    }

    lower_text = text.lower()

    for key in sections.keys():
        if key in lower_text:
            start = lower_text.find(key)
            sections[key] = text[start:start+2000]

    return sections
