def synthesize_findings(key_findings):
    synthesized_text = ""

    for paper, findings in key_findings.items():
        synthesized_text += f"\nFrom {paper}:\n"
        for point in findings:
            synthesized_text += f"- {point}\n"

    return synthesized_text
