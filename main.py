from paper_retrieval import fetch_papers
from database import create_table, insert_paper
from json_store import save_to_json

print("\n===== AI Research Paper Fetcher =====\n")

# User inputs
topic = input("Enter research topic: ")
num_papers = int(input("Enter number of papers to fetch: "))

# Create DB table if not exists
create_table()

# Fetch papers
papers = fetch_papers(topic, limit=num_papers)

print(f"\n✅ {len(papers)} papers fetched for topic '{topic}'\n")

# Display papers in terminal
for i, paper in enumerate(papers, start=1):
    title = paper.get("title")
    authors = ", ".join(a["name"] for a in paper.get("authors", []))
    year = paper.get("year")
    abstract = paper.get("abstract")
    url = paper.get("url")

    print(f"🔹 Paper {i}")
    print("Title       :", title)
    print("Authors     :", authors)
    print("Year        :", year)
    print("Abstract    :", abstract)
    print("Download URL:", url)
    print("-" * 80)

    # Save to database
    insert_paper(topic, title, authors, year, url)

# Save to JSON file
save_to_json(topic, papers)

print("\n📁 Papers saved to:")
print("➡ SQLite Database: papers.db")
print("➡ JSON File: papers.json")
print("\n===== DONE =====\n")