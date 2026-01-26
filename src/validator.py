def validate_sections(sections):
    report = {}
    for key, value in sections.items():
        report[key] = "OK" if value.strip() else "MISSING"
    return report
