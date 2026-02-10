# src/section_generator.py

def generate_abstract(text):
    return (
        "ABSTRACT\n"
        "This study reviews recent research related to the given topic. "
        "The collected literature highlights key challenges, methodologies, "
        "and findings identified across multiple studies.\n"
    )


def generate_methods(text):
    return (
        "METHODS\n"
        "The reviewed papers employ diverse experimental and analytical methods. "
        "Most studies use data-driven approaches, evaluation metrics, and "
        "comparative analysis to validate results.\n"
    )


def generate_results(text):
    return (
        "RESULTS\n"
        "The results reported across the studies indicate consistent performance "
        "improvements, robustness, and reliability of proposed approaches.\n"
    )
