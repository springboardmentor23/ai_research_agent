from semantic_search import fetch_papers, fetch_references
from dataset import prepare_dataset, save_dataset, show_dataset


def show_papers(papers):
    """Display paper details in the terminal"""
    for i, paper in enumerate(papers, start=1):
        authors = ", ".join(a["name"] for a in paper.get("authors", []))

        print(f"\nPaper {i}")
        print("Title:", paper.get("title"))
        print("Authors:", authors)
        print("Year:", paper.get("year"))
        print("\nAbstract:")
        print(paper.get("abstract"))
        print("\nPaper Link:", paper.get("url"))
        print("-" * 60)


def show_references(references):
    """Display references in the terminal"""
    for i, ref in enumerate(references, start=1):
        authors = ", ".join(a["name"] for a in ref.get("authors", []))

        print("Reference", i)
        print("Title:", ref.get("title"))
        print("Authors:", authors)
        print("Year:", ref.get("year"))
        print("Link:", ref.get("url"))
        print("-" * 50)


def main():
    """Main function: Ask user for topic, search papers, and display results"""
    
    print("=" * 60)
    print("📚 Research Paper Search")
    print("=" * 60)
    topic = input("\nEnter a research topic to search: ")
    
    try:
        num_papers = int(input("How many papers to fetch? (default: 5): ") or "5")
    except ValueError:
        num_papers = 5
    
    print(f"\n🔍 Searching for papers on '{topic}'...")
    
    papers = fetch_papers(topic, limit=num_papers)
    
    if papers:
        print(f"\n✅ Found {len(papers)} papers!\n")
        show_papers(papers)
        
        # Ask if user wants to see references for a paper
        try:
            paper_num = input(f"\n📚 Enter paper number (1-{len(papers)}) to see references, or press Enter to skip: ").strip()
            if paper_num:
                paper_index = int(paper_num) - 1
                if 0 <= paper_index < len(papers):
                    paper = papers[paper_index]
                    # Extract paper ID from URL or use paperId if available
                    paper_id = paper.get("paperId")
                    if not paper_id and paper.get("url"):
                        # Try to extract from URL
                        paper_id = paper["url"].split("/")[-1] if "/paper/" in paper["url"] else None
                    
                    if paper_id:
                        print(f"\n🔍 Fetching references for: {paper.get('title')}")
                        references = fetch_references(paper_id, limit=5)
                        if references:
                            print(f"\n📖 Found {len(references)} references:\n")
                            show_references(references)
                        else:
                            print("No references found.")
                    else:
                        print("❌ Could not get paper ID to fetch references.")
                else:
                    print("❌ Invalid paper number.")
        except ValueError:
            print("Skipping references...")
        
        # Prepare dataset and save to file
        print("\n" + "=" * 60)
        print("📊 Preparing dataset...")
        dataset = prepare_dataset(papers)
        save_dataset(dataset, "papers_dataset.json")
        
        # Display dataset
        print("\n" + "=" * 60)
        print("📋 Dataset Contents:")
        print("=" * 60)
        show_dataset(dataset)
    else:
        print("❌ No papers found for this topic.")


if __name__ == "__main__":
    main()
