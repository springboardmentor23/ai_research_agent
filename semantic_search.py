import requests
import time

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

HEADERS = {
    "User-Agent": "AI-Research-Reviewer/1.0 (educational-project)"
}

def search_papers(topic, limit=3, max_retries=3):
    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,openAccessPdf,venue"
    }

    for attempt in range(max_retries):
        response = requests.get(
            SEMANTIC_SCHOLAR_URL,
            params=params,
            headers=HEADERS
        )

        if response.status_code == 200:
            papers = response.json().get("data", [])
            results = []

            for paper in papers:
                authors = [a["name"] for a in paper.get("authors", [])]
                year = paper.get("year")
                title = paper.get("title")
                venue = paper.get("venue", "Unknown Venue")
                url = paper.get("url")

                pdf_url = paper.get("openAccessPdf", {}).get("url")

                apa_reference = f"{', '.join(authors)} ({year}). {title}. {venue}. {url}"

                results.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "abstract": paper.get("abstract"),
                    "venue": venue,
                    "paper_url": url,
                    "pdf_url": pdf_url,
                    "apa_reference": apa_reference
                })

            return results

        elif response.status_code == 429:
            wait_time = 2 ** attempt
            print(f"Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        else:
            response.raise_for_status()

    raise Exception("Semantic Scholar API unavailable after retries.")


