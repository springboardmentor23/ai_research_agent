import os
import json


def extract_sections_from_text(text):

    text_lower = text.lower()

    sections = {
        "abstract": "",
        "methodology": "",
        "conclusion": ""
    }

    #extracting abstract
    if "abstract" in text_lower:
        start = text_lower.find("abstract")
        end = text_lower.find("introduction", start)
        sections["abstract"] = text[start:end].strip()

    # extracting methodology
    if "method" in text_lower:
        start = text_lower.find("method")
        end = text_lower.find("result", start)
        sections["methodology"] = text[start:end].strip()

    #extracting conclusion
    if "conclusion" in text_lower:
        start = text_lower.find("conclusion")
        sections["conclusion"] = text[start:].strip()

    return sections


def process_all_text_files(input_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            sections = extract_sections_from_text(text)

            output_file = filename.replace(".txt", "_sections.json")
            output_path = os.path.join(output_folder, output_file)

            with open(output_path, "w", encoding="utf-8") as json_file:
                json.dump(sections, json_file, indent=4)

            print(f"Section-wise data saved: {output_file}")
