from sklearn.feature_extraction.text import TfidfVectorizer
import json

def extract_keywords(sections, top_n=5):
    """Extract top keywords per section using TF-IDF."""
    keywords_per_section = {}
    for section, text in sections.items():
        if text.strip():
            vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
            X = vectorizer.fit_transform([text])
            keywords_per_section[section] = vectorizer.get_feature_names_out().tolist()
        else:
            keywords_per_section[section] = []
    return keywords_per_section

def save_keywords(keywords, filename="keywords.json"):
    """Save keywords to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=4)
    print(f"Saved keywords to '{filename}'")
