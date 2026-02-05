def format_apa_references(metadata):
    references = []

    for paper in metadata:
        authors = paper["authors"]
        year = paper["year"]
        title = paper["title"]
        url = paper["paper_url"]

        ref = f"{authors} ({year}). {title}. Retrieved from {url}"
        references.append(ref)

    return references
