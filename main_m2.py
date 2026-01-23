from modules.text_extractor import extract_text_from_pdfs
from modules.section_parser import split_into_sections
from modules.key_finder import extract_key_findings
from modules.similarity import cross_paper_similarity

if __name__ == "__main__":
    print("📄 Extracting PDF text...")
    raw_text = extract_text_from_pdfs()

    print("📑 Parsing sections...")
    sectioned_text = split_into_sections(raw_text)

    print("🔑 Extracting key findings...")
    key_findings = extract_key_findings(sectioned_text)

    print("🔍 Performing cross-paper comparison...")
    similarity = cross_paper_similarity(key_findings)

    print("\n🎉 Finish")
