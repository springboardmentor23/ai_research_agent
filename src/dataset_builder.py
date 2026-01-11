def build_dataset(papers):
    dataset = []

    for p in papers:
        pdf = p.get("openAccessPdf")
        if pdf and "url" in pdf:
            dataset.append({
                "title": p.get("title"),
                "pdf_url": pdf["url"]
            })

    return dataset



