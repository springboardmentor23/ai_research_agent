# src/section_generator.py

"""
Purpose:
Generate structured academic sections (Abstract, Methods, Results)
from extracted research paper content.
"""

def generate_abstract(extracted_text):
    """
    Generate an academic Abstract section.
    """
    return (
        "Abstract\n"
        "This study reviews and analyzes selected research papers to identify "
        "key objectives, methodologies, and findings. The analysis highlights "
        "common research trends and challenges based on the extracted content.\n"
    )


def generate_methods(extracted_text):
    """
    Generate a Methods section.
    """
    return (
        "Methods\n"
        "Relevant research papers were collected and processed using an automated "
        "pipeline. Text extraction and keyword analysis techniques were applied "
        "to examine methodological patterns across studies.\n"
    )


def generate_results(extracted_text):
    """
    Generate a Results section.
    """
    return (
        "Results\n"
        "The results indicate recurring themes and frequently used approaches "
        "across the analyzed papers. The findings provide insights into dominant "
        "research directions within the selected topic.\n"
    )
