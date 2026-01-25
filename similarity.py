from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(tfidf_matrix, paper_names):

    similarity_matrix = cosine_similarity(tfidf_matrix)

    print("\n📊 Paper Similarity Matrix (Clean):\n")

    # Print header
    print("        ", end="")
    for i in range(len(paper_names)):
        print(f"Paper{i+1}   ", end="")
    print()

    # Print rows
    for i in range(len(paper_names)):
        print(f"Paper{i+1}   ", end="")
        for j in range(len(paper_names)):
            print(f"{similarity_matrix[i][j]:.2f}     ", end="")
        print()

    return similarity_matrix
