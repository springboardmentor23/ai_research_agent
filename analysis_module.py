import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KEY_PHRASES = [
    "we propose", "we introduce", "our approach",
    "our method", "we demonstrate",
    "outperforms", "achieves state-of-the-art"
]

def load_extracted_sections(extracted_dir):
    papers = []

    for file in os.listdir(extracted_dir):
        if file.endswith("_sections.json"):
            with open(os.path.join(extracted_dir, file), "r", encoding="utf-8") as f:
                data = json.load(f)

                full_text = " ".join(data.values()).lower()

                key_findings = [
                    sentence for sentence in full_text.split(".")
                    if any(k in sentence for k in KEY_PHRASES)
                ]

                papers.append({
                    "paper": file,
                    "text": full_text,
                    "key_findings": key_findings
                })

    return papers


def compute_similarity(papers):
    if len(papers) < 2:
        return {
            "message": "Not enough papers for cosine similarity (minimum 2 required)"
        }

    documents = [p["text"] for p in papers]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    return {
        "tfidf_shape": tfidf_matrix.shape,
        "cosine_similarity": similarity_matrix.tolist()
    }
def print_similarity_summary(papers, similarity_result):
    if "cosine_similarity" not in similarity_result:
        print("\n Cosine similarity not computed (need at least 2 papers)\n")
        return

    matrix = similarity_result["cosine_similarity"]
    paper_names = [p["paper"] for p in papers]

    print("\n📊 Cosine Similarity Summary:\n")

    for i in range(len(paper_names)):
        for j in range(i + 1, len(paper_names)):
            score = round(matrix[i][j], 3)
            print(f"{paper_names[i]}  ↔  {paper_names[j]}  :  {score}")

    print("\n✅ Similarity computation completed\n")

