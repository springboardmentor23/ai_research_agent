import json
import os

def save_dataset(papers):
    os.makedirs("data", exist_ok=True)

    with open("data/cleaned_dataset.json", "w") as f:
        json.dump(papers, f, indent=4)
