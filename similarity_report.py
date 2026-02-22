import os
import numpy as np


def generate_similarity_report(sim_matrix, paper_titles=None):
    """
    Generates an interpretable similarity analysis report.
    Returns the report text (important for UI).
    """

    n = len(sim_matrix)

    if n < 2:
        return "Not enough papers for similarity analysis."

    max_sim = -1
    min_sim = 2
    max_pair = (0, 0)
    min_pair = (0, 0)

    total = 0
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            value = float(sim_matrix[i][j])

            total += value
            count += 1

            if value > max_sim:
                max_sim = value
                max_pair = (i, j)

            if value < min_sim:
                min_sim = value
                min_pair = (i, j)

    avg_sim = total / count if count > 0 else 0

    report_text = (
        "SIMILARITY ANALYSIS REPORT\n"
        + "=" * 40 + "\n\n"
        + f"Average Similarity: {avg_sim:.4f}\n\n"
        + f"Most Similar Pair: Paper {max_pair[0]+1} & Paper {max_pair[1]+1}\n"
        + f"Similarity Score: {max_sim:.4f}\n\n"
        + f"Least Similar Pair: Paper {min_pair[0]+1} & Paper {min_pair[1]+1}\n"
        + f"Similarity Score: {min_sim:.4f}\n"
    )

    # Save to file
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/similarity_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("Similarity report generated successfully.")
    print("Check: data/output/similarity_report.txt")

    return report_text  # ⭐ THIS LINE FIXES YOUR ISSUE
