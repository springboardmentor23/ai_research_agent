import os
import json
import re
from collections import Counter

TEXT_DIR = "data/texts"
OUTPUT_PATH = "data/common_terms.json"

KEY_PATTERNS = {
    "datasets": [
        r"\bMNIST\b", r"\bCIFAR\b", r"\bImageNet\b",
        r"\bMIMIC\b", r"\bUCI\b", r"\bUK Biobank\b"
    ],
    "algorithms": [
        r"\bSVM\b", r"\bRandom Forest\b",
        r"\bKNN\b", r"\bXGBoost\b",
        r"\bGradient Boosting\b"
    ],
    "models": [
        r"\bCNN\b", r"\bRNN\b", r"\bLSTM\b",
        r"\bTransformer\b", r"\bBERT\b",
        r"\bResNet\b", r"\bDeep Cox\b"
    ],
    "techniques": [
        r"\bcross-validation\b",
        r"\bMonte Carlo\b",
        r"\bExpectation-Maximization\b",
        r"\bregularization\b",
        r"\bcalibration\b"
    ]
}


def normalize_term(term):
    return term.strip().lower()


def extract_common_terms():
    collected = {
        "datasets": [],
        "algorithms": [],
        "models": [],
        "techniques": []
    }

    for filename in os.listdir(TEXT_DIR):
        if not filename.endswith(".txt"):
            continue

        with open(os.path.join(TEXT_DIR, filename), "r", encoding="utf-8") as f:
            text = f.read()

        for category, patterns in KEY_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                normalized = [normalize_term(m) for m in matches]
                collected[category].extend(normalized)

    result = {}

    for category, terms in collected.items():
        counter = Counter(terms)

        # Sort by frequency (descending)
        sorted_terms = dict(sorted(counter.items(),
                                   key=lambda x: x[1],
                                   reverse=True))

        result[category] = sorted_terms

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("Common terms extracted and normalized successfully.")
    print("Check: data/common_terms.json")

    return result
