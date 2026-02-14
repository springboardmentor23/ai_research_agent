KEY_PHRASES = [
    "we propose",
    "this paper proposes",
    "in this paper",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "experimental results",
    "state-of-the-art",
    "conclusion"
]

def extract_key_sentences(text):
    extracted = []

    sentences = text.split(".")  # very simple sentence split

    for sentence in sentences:
        for phrase in KEY_PHRASES:
            if phrase.lower() in sentence.lower():
                extracted.append(sentence.strip())
                break

    return extracted
