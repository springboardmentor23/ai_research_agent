import re
from collections import Counter
import json
import os

DATASET_KEYWORDS = [
    "mnist", "cifar", "cifar-10", "cifar-100",
    "imagenet", "coco", "pascal voc",
    "uci", "kaggle"
]

def extract_common_datasets(sectioned_text):
    found = []

    for paper, sections in sectioned_text.items():
        for text in sections.values():
            if not text:
                continue
            text = text.lower()
            for ds in DATASET_KEYWORDS:
                if re.search(rf"\b{ds}\b", text):
                    found.append(ds)

    dataset_counts = Counter(found)

    os.makedirs("data/analysis", exist_ok=True)
    with open("data/analysis/common_datasets.json", "w") as f:
        json.dump(dataset_counts, f, indent=4)

    return dict(dataset_counts)
