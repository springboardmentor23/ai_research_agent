import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KEY_FINDINGS_DIR = "../data/dist_texts"

def load_documents():
    """Load all distilled text documents from data/dist_texts"""
    documents = []
    doc_names = []

    if not os.path.exists(KEY_FINDINGS_DIR):
        print(f"Distilled texts directory {KEY_FINDINGS_DIR} not found")
        return documents, doc_names

    for filename in os.listdir(KEY_FINDINGS_DIR):
        if not filename.endswith("_findings.txt"):
            continue

        path = os.path.join(KEY_FINDINGS_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()

            # Skip empty papers
            if text:
                documents.append(text)
                doc_names.append(filename)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return documents, doc_names


def compute_similarity():
    """
    Compute cosine similarity between all distilled documents using TF-IDF.
    """
    documents, doc_names = load_documents()
    if len(documents) < 2:
        print("Not enough documents for comparison.")
        return

    vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    max_df=0.85,        # remove very common words
    min_df=2,           # remove rare noise words
    ngram_range=(1,2),  # unigrams + bigrams
    token_pattern=r'\b[a-zA-Z]{3,}\b'  # real words only
)

    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    print("\n" + "="*70)
    print("SIMILARITY ANALYSIS (TF-IDF Cosine Similarity)")
    print("="*70 + "\n")
    
    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            similarity_score = similarity_matrix[i][j]
            print(
                f"{doc_names[i]:30s} vs {doc_names[j]:30s} → {similarity_score:.4f}"
            )

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    compute_similarity()