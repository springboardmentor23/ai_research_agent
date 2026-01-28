import os
import json
from collections import Counter
from pathlib import Path
import re


INPUT_FOLDER = "extracted_texts_json"
OUTPUT_FOLDER = "key_phrases"


STOP_WORDS = {
    'the','and','for','that','with','from','this','which','have','been','can',
    'will','not','were','has','was','all','their','more','when','used','would',
    'into','being','such','each','also','other','where','some','than','them',
    'its','our','we','to','in','is','by','on','at','an','a','of','it'
}


def ensure_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def extract_keywords(text, top_n=30):

    words = re.findall(r'\b[a-z]{3,}\b', text.lower())

    filtered = [w for w in words if w not in STOP_WORDS]

    freq = Counter(filtered)

    return freq.most_common(top_n)


def process_key_phrases():

    ensure_folder(OUTPUT_FOLDER)

    for file in os.listdir(INPUT_FOLDER):

        if not file.endswith(".json"):
            continue

        path = os.path.join(INPUT_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = data["full_text"]

        keywords = extract_keywords(text)

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file.replace(".json", "_keywords.json")
        )

        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(keywords, out, indent=4)

        print(f"✅ Key phrases extracted: {file}")

    print("\n🎯 All key phrases done!")


if __name__ == "__main__":
    process_key_phrases()
