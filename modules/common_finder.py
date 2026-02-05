import re
from collections import Counter

COMMON_METHOD_KEYWORDS = [
    "tf-idf", "bert", "cnn", "rnn", "lstm",
    "svm", "random forest", "naive bayes",
    "transformer", "resnet", "gpt"
]

def extract_common_methods(sectioned_text):
    all_methods = []

    for paper, sections in sectioned_text.items():
        methods_text = sections.get("methods") or sections.get("methodology")

        if not methods_text:
            continue

        text = methods_text.lower()

        for method in COMMON_METHOD_KEYWORDS:
            if re.search(rf"\b{method}\b", text):
                all_methods.append(method)

    method_counts = Counter(all_methods)

    return dict(method_counts)
