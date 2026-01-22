import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_papers(section_file="section_data.json"):
    with open(section_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    paper_names = []

    for paper, sections in data.items():
        combined_text = " ".join(
            " ".join(v) if isinstance(v, list) else v
            for v in sections.values()
        )
        texts.append(combined_text)
        paper_names.append(paper)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(tfidf)

    return similarity_matrix, paper_names
