import os
from sklearn.feature_extraction.text import TfidfVectorizer

KEY_FINDINGS_DIR = "key_findings"

def load_documents():
    """Load key findings documents from the key_findings directory."""
    documents = []
    doc_names = []

    for filename in os.listdir(KEY_FINDINGS_DIR):
        if not filename.endswith("_findings.txt"):
            continue

        path = os.path.join(KEY_FINDINGS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # skip empty papers (important)
        if text:
            documents.append(text)
            doc_names.append(filename)

    return documents, doc_names


def get_tfidf_matrix(documents):
    """Create TF-IDF matrix from documents."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer


if __name__ == "__main__":
    documents, doc_names = load_documents()
    print(f"Loaded {len(documents)} documents")
    
    if documents:
        tfidf_matrix, vectorizer = get_tfidf_matrix(documents)
        print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
        print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
