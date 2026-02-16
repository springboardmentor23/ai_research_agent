import json
from extract_text import extract_text_from_pdf
from section_parser import split_into_sections
from key_findings import extract_key_findings

with open("research_dataset.json") as f:
    dataset = json.load(f)

analysis_results = []

for paper in dataset:
    pdf_path = paper["local_pdf_path"]

    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        sections = split_into_sections(text)
        findings = extract_key_findings(sections)

        analysis_results.append({
            "title": paper["title"],
            "sections": sections,
            "key_findings": findings
        })

with open("analysis_dataset.json", "w") as f:
    json.dump(analysis_results, f, indent=4)

print("Analysis dataset saved!")
