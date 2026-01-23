from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

def cross_paper_similarity(key_findings):
    """
    Input: key_findings dict
    Output: similarity matrix
    """

    paper_names = list(key_findings.keys())
    documents = [
        " ".join(key_findings[paper])
        for paper in paper_names
    ]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Cosine Similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)

    result = {
        "papers": paper_names,
        "similarity_matrix": similarity_matrix.tolist()
    }

    os.makedirs("data/analysis", exist_ok=True)
    with open("data/analysis/cross_paper_similarity.json", "w") as f:
        json.dump(result, f, indent=4)

    return result
