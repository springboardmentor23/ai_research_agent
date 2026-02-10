
import os
import json
from pathlib import Path


INPUT_FOLDER = "extracted_texts"
OUTPUT_FOLDER = "extracted_texts_json"


def ensure_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def convert_txt_to_json():

    ensure_folder(OUTPUT_FOLDER)

    for file in os.listdir(INPUT_FOLDER):

        if not file.endswith(".txt"):
            continue

        txt_path = os.path.join(INPUT_FOLDER, file)

        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()

        json_data = {
            "file": file.replace(".txt", ".json"),
            "full_text": content
        }

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file.replace(".txt", ".json")
        )

        with open(output_path, "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, indent=4, ensure_ascii=False)

        print(f"✅ Converted: {file} → JSON")

    print("\n🎉 All text files converted to JSON!")


if __name__ == "__main__":
    convert_txt_to_json()
