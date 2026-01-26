def extract_keywords(text, top_n=10):
    words = text.lower().split()
    stopwords = {"the", "and", "is", "to", "of", "in", "for", "on"}
    keywords = [w for w in words if w.isalpha() and w not in stopwords]

    freq = {}
    for word in keywords:
        freq[word] = freq.get(word, 0) + 1

    return sorted(freq, key=freq.get, reverse=True)[:top_n]
