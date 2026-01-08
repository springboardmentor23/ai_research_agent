from semantic_search import fetch_papers
from dataset import prepare_dataset, save_dataset
import json
def show_papers(papers):
    for i, paper in enumerate(papers, start=1):
        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Year:", paper.get("year"))
        print("Abstract:", paper.get("abstract"))
        print("Link:", paper.get("url"))
        print("-" * 40)

topic = input("Enter research topic: ")
limit = int(input("Enter number of papers: "))

papers = fetch_papers(topic, limit)
show_papers(papers)
dataset = prepare_dataset(papers)
save_dataset(dataset)
