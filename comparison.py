def compare_papers(papers_analysis):
    comparison = []

    for paper in papers_analysis:
        summary = {
            "title": paper["title"],
            "key_points": paper["key_findings"]
        }
        comparison.append(summary)

    return comparison
