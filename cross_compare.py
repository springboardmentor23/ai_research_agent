import numpy as np


def cross_compare_papers(similarity_matrix, paper_names):

    print("\n🔗 Paper Similarity Chain:\n")

    n = len(paper_names)

    for i in range(n):
        scores = similarity_matrix[i]

        # Ignore self similarity by setting it to -1
        scores[i] = -1

        # Get index of most similar paper
        most_similar_index = np.argmax(scores)

        similarity_score = scores[most_similar_index]

        paper1 = f"Paper{i+1}"
        paper2 = f"Paper{most_similar_index+1}"

        # Print simple chain with score
        print(f"{paper1} --> {paper2}   ({similarity_score:.2f})")
