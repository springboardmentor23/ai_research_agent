import re

KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art"
]

def extract_key_findings(sectioned_text):
    """
    Input: sectioned_text (dict)
    Output: key_findings (dict)
    """

    key_findings = {}

    for paper, sections in sectioned_text.items():
        findings = []

        for section, text in sections.items():
            if not text:
                continue

            # 🔹 Requirement: convert to lower case
            text = text.lower()

            # split into sentences
            sentences = re.split(r'\.|\n', text)

            for sentence in sentences:
                for phrase in KEY_PHRASES:
                    if phrase in sentence:
                        findings.append(sentence.strip())
                        break

        key_findings[paper] = list(set(findings))  # remove duplicates

    return key_findings
