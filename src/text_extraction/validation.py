import os
import json

def validate_section_files(section_folder):
    validation_report = {}

    for filename in os.listdir(section_folder):
        if not filename.endswith("_sections.json"):
            continue

        file_path = os.path.join(section_folder, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            sections = json.load(f)

        key_findings_count = 0

        for key in ["abstract", "methodology", "conclusion"]:
            if sections.get(key):
                key_findings_count += 1

        if key_findings_count > 0:
            validation_report[filename.replace("_sections.json", "")] = "✅ Valid sections found"
        else:
            validation_report[filename.replace("_sections.json", "")] = "❌ No valid sections"

    return validation_report
