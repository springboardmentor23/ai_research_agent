import re

# -------------------------------
# CLEAN TEXT & TOKENIZE
# -------------------------------
def clean_text(text):
    """
    Convert text to lowercase, remove symbols,
    and return a set of words
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    return set(words)

# -------------------------------
# JACCARD SIMILARITY
# -------------------------------
def jaccard_similarity(text1, text2):
    """
    Compute Jaccard similarity between two texts
    """
    set1 = clean_text(text1)
    set2 = clean_text(text2)

    if not set1 or not set2:
        return 0.0

    intersection = set1.intersection(set2)
    union = set1.union(set2)

    return len(intersection) / len(union)

# -------------------------------
# MULTI-PDF SIMILARITY
# -------------------------------
def compute_pdf_similarity(pdf_texts):
    """
    pdf_texts: dict -> { "file1.pdf": text1, "file2.pdf": text2 }
    """
    results = []
    files = list(pdf_texts.keys())

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            score = jaccard_similarity(
                pdf_texts[files[i]],
                pdf_texts[files[j]]
            )
            results.append({
                "pdf_1": files[i],
                "pdf_2": files[j],
                "similarity": round(score, 4)
            })

    return results
