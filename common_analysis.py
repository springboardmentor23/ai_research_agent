import os
import json
from collections import Counter

# ============================
# FOLDERS
# ============================

INPUT_FOLDER = "ai_results"
OUTPUT_FILE = "common_results.json"

# ============================
# LOAD AI RESULTS
# ============================

def load_ai_results():
    all_data = []

    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(INPUT_FOLDER, file)
            with open(path, "r", encoding="utf-8") as f:
                all_data.append(json.load(f))

    return all_data

# ============================
# FIND COMMON ITEMS
# ============================

def find_common(list_of_lists, top_n=10):
    merged = []
    for sublist in list_of_lists:
        merged.extend(sublist)

    counter = Counter(merged)
    return [item for item, _ in counter.most_common(top_n)]

# ============================
# MAIN FUNCTION
# ============================

def main():

    data = load_ai_results()

    if len(data) == 0:
        print("❌ No AI result files found")
        return

    datasets = find_common([d.get("datasets", []) for d in data])
    methods = find_common([d.get("methods", []) for d in data])
    algorithms = find_common([d.get("algorithms", []) for d in data])
    findings = find_common([d.get("key_findings", []) for d in data])

    output = {
        "common_datasets": datasets,
        "common_methods": methods,
        "common_algorithms": algorithms,
        "common_key_findings": findings
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("✅ common_results.json created")

# ============================
# RUN
# ============================

if __name__ == "__main__":
    main()
