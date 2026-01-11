def search_papers(papers, query):
    if not papers:
        return []

    query = query.lower()
    results = []

    for p in papers:
        title = (p.get("title") or "").lower()
        abstract = (p.get("abstract") or "").lower()

        if query in title or query in abstract:
            results.append(p)

    return results

