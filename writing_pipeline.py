import json
from writing_module import (
    generate_abstract,
    generate_methods_comparison,
    generate_results_synthesis,
    format_apa_references
)

print("\n--- Writing Phase ---")


with open("analysis_dataset.json", "r", encoding="utf-8") as f:
    analysis_data = json.load(f)


papers = analysis_data   # because JSON root is a list


# Generate sections
abstract = generate_abstract(papers)
methods = generate_methods_comparison(papers)
results = generate_results_synthesis(papers)


# Load original dataset for references
with open("research_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

references = format_apa_references(dataset)


# Combine final draft
final_report = f"""
===== ABSTRACT =====
{abstract}

===== METHODS COMPARISON =====
{methods}

===== RESULTS SYNTHESIS =====
{results}

===== REFERENCES (APA) =====
{references}
"""


# Save output
with open("final_review.txt", "w", encoding="utf-8") as f:
    f.write(final_report)


print("Final draft saved as final_review.txt")
