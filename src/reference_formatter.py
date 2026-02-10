# src/reference_formatter.py

def format_references_apa(papers):
    references = "REFERENCES (APA STYLE)\n"

    for idx, paper in enumerate(papers, start=1):
        title = paper.get("title", "Unknown Title")
        year = paper.get("year", "n.d.")
        authors = paper.get("authors", [])

        author_names = ", ".join(a.get("name", "") for a in authors)

        references += f"{idx}. {author_names} ({year}). {title}.\n"

    return references
