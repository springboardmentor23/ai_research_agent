import json



def generate_abstract(papers):
    combined = " ".join(
        " ".join(p.get("key_findings", [])) for p in papers
    )

    words = combined.split()[:100]   
    return " ".join(words)



def generate_methods_comparison(papers):
    methods_summary = []

    for p in papers:
        methods = p["sections"].get("method", "Method details not found.")
        snippet = methods[:300]

        methods_summary.append(
            f"{p['title']} uses the following methodology:\n{snippet}"
        )

    return "\n\n".join(methods_summary)



def generate_results_synthesis(papers):
    synthesis = []

    for p in papers:
        results = p["sections"].get("results", "")
        snippet = results[:300]

        synthesis.append(
            f"Key results from {p['title']}:\n{snippet}"
        )

    return "\n\n".join(synthesis)


# -------- APA REFERENCES --------

def format_apa_references(dataset):
    refs = []

    for paper in dataset:
        authors = ", ".join(paper.get("authors", []))
        year = paper.get("year", "n.d.")
        title = paper.get("title")
        url = paper.get("source_url")

        ref = f"{authors} ({year}). {title}. Retrieved from {url}"
        refs.append(ref)

    return "\n".join(refs)
