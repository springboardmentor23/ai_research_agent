def extract_sections(text):
    sections = {
        "introduction": [],
        "methodology": [],
        "results": [],
        "conclusion": []
    }

    lines = text.lower().split("\n")

    current_section = None

    for line in lines:
        if "introduction" in line:
            current_section = "introduction"
        elif "method" in line:
            current_section = "methodology"
        elif "result" in line:
            current_section = "results"
        elif "conclusion" in line:
            current_section = "conclusion"

        if current_section:
            sections[current_section].append(line)

    return sections
