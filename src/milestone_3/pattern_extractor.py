def extract_common_patterns(cleaned_dataset):
    datasets = set()
    methods = set()
    algorithms = set()

    for paper in cleaned_dataset:
        text = (paper.get("abstract") or "").lower()

        if "dataset" in text:
            datasets.add("public benchmark datasets")

        if "method" in text or "approach" in text:
            methods.add("machine learning based approach")

        if "cnn" in text:
            algorithms.add("Convolutional Neural Network (CNN)")
        if "svm" in text:
            algorithms.add("Support Vector Machine (SVM)")

    return {
        "common_datasets": list(datasets),
        "common_methods": list(methods),
        "common_algorithms": list(algorithms)
    }
