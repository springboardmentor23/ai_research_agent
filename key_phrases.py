import json
import os
import shutil
KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art",
    "this paper proposes",
    "we present",
    "this paper presents",
    "the proposed method",
    "the proposed approach",
    "experimental results show",
    "results show",
    "achieves better",
    "significantly improves"
]
if os.path.exists("key_phrases"):
    shutil.rmtree("key_phrases")
os.makedirs("key_phrases")
def extract_key_phrases(section_folder="section_texts",
                        output_folder="key_phrases"):
    
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(section_folder):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(section_folder, file), "r", encoding="utf-8") as f:
            sections = json.load(f)

        findings = []

        for section in ["introduction", "methodology", "results"]:
            text = sections.get(section, "")
            sentences = text.split(".")

            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(phrase in sentence_lower for phrase in KEY_PHRASES):
                    findings.append(sentence.strip())

        output_path = os.path.join(output_folder, file)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(findings, f, indent=4)

    print("✅ Key phrases extracted")

