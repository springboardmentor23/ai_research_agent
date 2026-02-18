import os
import re
import json

TEXT_DIR = "data/texts"
OUTPUT_DIR = "data/dist_texts"
ANALYSIS_DIR = "data/analysis"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art"
]

def extract_key_findings():
    """
    Extract key findings from raw text files and save:
    1. Individual distilled text files
    2. Combined JSON file
    """

    if not os.path.exists(TEXT_DIR):
        print(f"Text directory {TEXT_DIR} not found")
        return 0

    all_findings = {}
    total_files = 0

    for filename in os.listdir(TEXT_DIR):
        if not filename.endswith(".txt"):
            continue

        input_path = os.path.join(TEXT_DIR, filename)
        output_filename = filename.replace(".txt", "_findings.txt")
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read().lower()  # ✅ convert to lowercase

            # Split into sentences
            sentences = re.split(r'\.|\n', text)

            key_sentences = []

            for sentence in sentences:
                for phrase in KEY_PHRASES:
                    if phrase in sentence:
                        key_sentences.append(sentence.strip())
                        break

            # ✅ Remove duplicates
            key_sentences = list(set(key_sentences))

            # Save individual findings file
            with open(output_path, "w", encoding="utf-8") as f:
                for s in key_sentences:
                    f.write(s + "\n")

            # Store for combined JSON
            paper_name = filename.replace(".txt", "")
            all_findings[paper_name] = key_sentences

            print(f"Extracted {len(key_sentences)} key findings from {filename}")
            total_files += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # ✅ Save combined JSON file
    json_output_path = os.path.join(ANALYSIS_DIR, "key_findings.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(all_findings, f, indent=4)

    print("✅ key_findings.json created successfully")
    return total_files


if __name__ == "__main__":
    extract_key_findings()
