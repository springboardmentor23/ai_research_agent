import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- KEY FINDING EXTRACTION ----------------

KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art"
]


def extract_key_findings(section_folder):
    
    #Extracts key finding sentences based on predefined key phrases.
    #Converts text to lowercase before processing.
    key_findings = {}
    documents_for_similarity = []

    for filename in os.listdir(section_folder):
        if not filename.endswith("_sections.json"):
            continue

        file_path = os.path.join(section_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            sections = json.load(file)

        # Combine sections and convert to lowercase
        combined_text = (
            sections.get("abstract", "") + " " +
            sections.get("methodology", "") + " " +
            sections.get("conclusion", "")
        ).lower()

        sentences = combined_text.split(".")

        matched_sentences = []

        for sentence in sentences:
            for phrase in KEY_PHRASES:
                if phrase in sentence:
                    matched_sentences.append(sentence.strip())
                    break

        paper_name = filename.replace("_sections.json", "")
        key_findings[paper_name] = matched_sentences

        # Prepare document for similarity (even if empty)
        documents_for_similarity.append(" ".join(matched_sentences))

    return key_findings, documents_for_similarity


# cross-paper comparison

def compare_papers_tfidf(documents):
    """
    Computes TF-IDF vectors and cosine similarity between papers.
    """

    if not documents or all(doc.strip() == "" for doc in documents):
        return None

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix


# result validation

def validate_results(key_findings, similarity_matrix):
    """
    Validates correctness and completeness of extracted data.
    """

    print("\n--- Validation Report ---")

    for paper, findings in key_findings.items():
        if findings:
            print(f"{paper}: ✅ {len(findings)} key findings extracted")
        else:
            print(f"{paper}: ❌ No key findings extracted")

    if similarity_matrix is None:
        print("❌ Similarity matrix could not be generated")
    else:
        print("✅ Similarity matrix generated successfully")


# save results in json file

def save_similarity_results(
    key_findings,
    similarity_matrix,
    output_path="data/datasets/similarity_results.json"
):
    """
    Saves key findings and cosine similarity matrix to JSON.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    results = {
        "key_findings": key_findings,
        "cosine_similarity": (
            similarity_matrix.tolist() if similarity_matrix is not None else []
        )
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print(f"\nResults saved to {output_path}")
