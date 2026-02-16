def extract_key_findings(sections):
    findings = []

    if "results" in sections:
        findings.append(sections["results"][:500])

    if "conclusion" in sections:
        findings.append(sections["conclusion"][:500])

    return findings
