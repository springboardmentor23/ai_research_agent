from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

def compute_similarity(texts):
    if len(texts) < 2:
        print("Not enough documents for similarity comparison.")
        return

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    os.makedirs("data", exist_ok=True)

    with open("data/similarity_results.json", "w") as f:
        json.dump(similarity_matrix.tolist(), f, indent=4)

    print("\nCosine Similarity Matrix:\n")
    print(similarity_matrix)

    return similarity_matrix

