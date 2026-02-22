def extract_key_findings(text):
    sentences = text.split(".")
    keywords = [
        "propose",
        "introduce",
        "novel",
        "improve",
        "outperform",
        "we present",
        "we develop",
        "we design"
    ]

    findings = []

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            findings.append(sentence.strip())

    return findings[:10]
