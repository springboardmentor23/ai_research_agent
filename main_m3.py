from modules.draft_generator import generate_section
from modules.synthesizer import synthesize_findings
from modules.reference_formatter import format_apa_references
from modules.common_finder import extract_common_methods
from modules.common_datasets import extract_common_datasets
import json

if __name__ == "__main__":

    # 1️⃣ Load key findings
    with open("data/analysis/key_findings.json") as f:
        key_findings = json.load(f)

    # 2️⃣ Load metadata0
    with open("data/datasets/papers_metadata.json") as f:
        metadata = json.load(f)

    # 3️⃣ Load sectioned text
    with open("data/extracted_text/sectioned_text.json") as f:
        sectioned_text = json.load(f)

    # 4️⃣ Extract common methods
    common_methods = extract_common_methods(sectioned_text)
    with open("data/analysis/common_methods.json", "w") as f:
        json.dump(common_methods, f, indent=4)

    # 5️⃣ Extract common datasets
    common_datasets = extract_common_datasets(sectioned_text)
    with open("data/analysis/common_datasets.json", "w") as f:
        json.dump(common_datasets, f, indent=4)

    # 6️⃣ Synthesize findings
    combined_text = synthesize_findings(key_findings)

    # 7️⃣ Generate paper sections using GPT
    print("🧠 Generating Abstract...")
    abstract = generate_section(
        "Abstract",
        combined_text,
        key_findings,
        common_methods,
        common_datasets
    )

    print("📚 Generating Introduction...")
    introduction = generate_section(
        "Introduction",
        combined_text,
        key_findings,
        common_methods,
        common_datasets
    )

    print("🧪 Generating Methods...")
    methods = generate_section(
        "Methods",
        combined_text,
        key_findings,
        common_methods,
        common_datasets
    )

    print("📊 Generating Results...")
    results = generate_section(
        "Results",
        combined_text,
        key_findings,
        common_methods,
        common_datasets
    )

    print("💬 Generating Discussion...")
    discussion = generate_section(
        "Discussion",
        combined_text,
        key_findings,
        common_methods,
        common_datasets
    )

    print("🏁 Generating Conclusion...")
    conclusion = generate_section(
        "Conclusion",
        combined_text,
        key_findings,
        common_methods,
        common_datasets
    )

    # 8️⃣ Format APA references
    references = format_apa_references(metadata)

    # 9️⃣ Save final draft
    final_draft = {
        "Abstract": abstract,
        "Introduction": introduction,
        "Methods": methods,
        "Results": results,
        "Discussion": discussion,
        "Conclusion": conclusion,
        "References": references
    }

    with open("data/analysis/final_review_draft.json", "w") as f:
        json.dump(final_draft, f, indent=4)

    print("\n🎉 Milestone 3 COMPLETED")
