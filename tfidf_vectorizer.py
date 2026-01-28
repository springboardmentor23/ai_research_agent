import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer


def flatten_list(data):
    flat = []

    for item in data:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(str(item))

    return flat


def build_tfidf_vectors(keyphrase_folder="key_phrases"):

    documents = []
    paper_names = []

    for file in os.listdir(keyphrase_folder):

        if not file.endswith(".json"):
            continue

        file_path = os.path.join(keyphrase_folder, file)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = ""

        # Case 1: list (maybe nested)
        if isinstance(data, list):
            flattened = flatten_list(data)
            text = " ".join(flattened)

        # Case 2: dict (friend approach)
        elif isinstance(data, dict):

            if "frequency_keywords" in data:
                words = [word for word, freq in data["frequency_keywords"]]
                text = " ".join(words)

        if text.strip() == "":
            continue

        documents.append(text)
        paper_names.append(file.replace(".json", ""))

    if len(documents) == 0:
        print("⚠️ No data for TF-IDF")
        return None, None

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    print(f"✅ TF-IDF created | Papers: {len(documents)} | Features: {tfidf_matrix.shape[1]}")

    return tfidf_matrix, paper_names
