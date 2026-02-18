import json
from datetime import datetime


def generate_final_report(
    topic: str,
    patterns: dict,
    key_findings: dict,
    draft_text: str,
    refined_text: str,
    quality_report: dict,
    output_path: str = "data/datasets/final_report.json"
):
    """
    Saves a complete final report into JSON.
    """

    report = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "common_patterns": patterns,
        "key_findings": key_findings,
        "initial_draft": draft_text,
        "refined_draft": refined_text,
        "quality_report": quality_report
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return output_path
