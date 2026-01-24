import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

folder = "key_sentences"

documents = []
paper_names = []

for file in os.listdir(folder):
    if file.endswith(".txt"):
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            documents.append(f.read())
            paper_names.append(file)

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(documents)

similarity_matrix = cosine_similarity(tfidf_matrix)

print("\n📊 PAPER SIMILARITY MATRIX\n")

for i in range(len(paper_names)):
    for j in range(len(paper_names)):
        print(f"{paper_names[i]} ↔ {paper_names[j]} : {similarity_matrix[i][j]:.2f}")
    print()
