import numpy as np

def cross_compare_papers(similarity_matrix, paper_names):

    output = "\n🔗 Paper Similarity Chain:\n\n"

    n = len(paper_names)

    for i in range(n):

        scores = similarity_matrix[i].copy()  # avoid modifying original matrix

        # Ignore self similarity
        scores[i] = -1

        most_similar_index = np.argmax(scores)
        similarity_score = scores[most_similar_index]

        paper1 = paper_names[i]
        paper2 = paper_names[most_similar_index]

        output += f"{paper1}  -->  {paper2}   ({similarity_score:.2f})\n"

    return output
