import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf_vectors(keyphrase_folder="key_phrases"):

    documents = []
    paper_names = []

    # Read all key phrase json files from current run
    for file in os.listdir(keyphrase_folder):

        if file.endswith(".json"):

            file_path = os.path.join(keyphrase_folder, file)

            with open(file_path, "r", encoding="utf-8") as f:
                phrases = json.load(f)

                # Skip empty phrase files
                if phrases:
                    documents.append(" ".join(phrases))
                    paper_names.append(file.replace(".json", ""))

    if len(documents) < 1:
        print("⚠️ Not enough papers to compute similarity (need at least 2).")
        return None, None

    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    print("✅ TF-IDF vectors created successfully")
    print("Number of papers:", tfidf_matrix.shape[0])
    print("Number of features:", tfidf_matrix.shape[1])

    return tfidf_matrix, paper_names
