import os
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art"
]


def load_extracted_texts(input_folder='extracted_text'):
    texts = {}
    
    if not os.path.exists(input_folder):
        return texts
    
    for text_file in sorted(os.listdir(input_folder)):
        if text_file.endswith('.txt'):
            text_path = os.path.join(input_folder, text_file)
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    paper_name = text_file.replace('.txt', '')
                    texts[paper_name] = content
            except Exception as e:
                print(f"Error loading {text_file}: {str(e)}")
    
    return texts


def extract_key_findings(text, key_phrases=KEY_PHRASES):
    text_lower = text.lower()
    findings = {}
    
    for phrase in key_phrases:
        if phrase.lower() in text_lower:
            findings[phrase] = True
        else:
            findings[phrase] = False
    
    return [phrase for phrase in key_phrases if findings.get(phrase, False)]


def calculate_tfidf_similarity(texts):
    if len(texts) < 2:
        return None, None, None
    
    paper_names = list(texts.keys())
    paper_texts = list(texts.values())
    
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(paper_texts)
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return similarity_matrix, paper_names, tfidf_matrix


def get_pdf_names(pdf_folder='pdf'):
    pdf_files = []
    if os.path.exists(pdf_folder):
        pdf_files = sorted([f for f in os.listdir(pdf_folder) if f.endswith('.pdf')])
    return pdf_files


def create_cross_paper_analysis(input_folder='extracted_text', output_folder='analysis'):
    print("\nExtracting key findings...")
    texts = load_extracted_texts(input_folder)
    
    if len(texts) < 2:
        print("Need at least 2 papers for cross-paper analysis")
        return
    
    paper_names = list(texts.keys())
    pdf_names = get_pdf_names()
    
    findings_dict = {}
    for paper_name, text in texts.items():
        findings = extract_key_findings(text, KEY_PHRASES)
        findings_dict[paper_name] = findings
    
    print("Computing pairwise TF-IDF similarities between all papers...")
    similarity_matrix, _, _ = calculate_tfidf_similarity(texts)
    
    similarity_matrix_list = similarity_matrix.tolist()
    
    output_data = {
        "total_papers": len(pdf_names),
        "papers": pdf_names,
        "paper_names": paper_names,
        "key_findings": findings_dict,
        "similarity_matrix": similarity_matrix_list
    }
    
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(output_folder, 'cross_paper_similarity.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    display_cross_paper_analysis(output_data, pdf_names, findings_dict, similarity_matrix)
    
    save_table_report(pdf_names, findings_dict, similarity_matrix, output_folder)
    
    print(f"\nFinish")
    print(f"Cross-paper analysis saved to: {output_file}")


def save_table_report(pdf_names, findings_dict, similarity_matrix, output_folder='analysis'):
    output_file = os.path.join(output_folder, 'similarity_table.txt')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n" + "=" * 140 + "\n")
            f.write("CROSS-PAPER SIMILARITY ANALYSIS & KEY FINDINGS\n")
            f.write("=" * 140 + "\n\n")
            
            f.write(f"Total Papers Analyzed: {len(pdf_names)}\n\n")
            
            for idx, (pdf_name, findings) in enumerate(zip(pdf_names, findings_dict.values()), 1):
                f.write(f"{idx}. {pdf_name}\n")
                if findings:
                    f.write(f"   Key Findings: {', '.join(findings)}\n")
                else:
                    f.write(f"   Key Findings: None found from predefined phrases\n")
            
            f.write("\n" + "-" * 140 + "\n")
            f.write("SIMILARITY MATRIX - TABLE FORMAT\n")
            f.write("-" * 140 + "\n\n")
            
            pairs = []
            for i in range(len(pdf_names)):
                for j in range(i + 1, len(pdf_names)):
                    score = similarity_matrix[i][j]
                    pairs.append((pdf_names[i], pdf_names[j], score))
            
            pairs_sorted = sorted(pairs, key=lambda x: x[2], reverse=True)
            
            header = "| # | Paper 1                                        | Paper 2                                        | Score    | % Similarity|"
            f.write(header + "\n")
            f.write("|---|------------------------------------------------|------------------------------------------------|----------|-------------|" + "\n")
            
            for idx, (paper1, paper2, score) in enumerate(pairs_sorted, 1):
                percentage = score * 100
                paper1_short = paper1[:43] + "..." if len(paper1) > 43 else paper1
                paper2_short = paper2[:43] + "..." if len(paper2) > 43 else paper2
                
                f.write(f"| {idx} | {paper1_short:<44} | {paper2_short:<44} | {score:.6f} | {percentage:>10.2f}% |\n")
            
            f.write("-" * 140 + "\n")
            f.write("\n" + "=" * 140 + "\n\n")
        
        return True, output_file
    except Exception as e:
        return False, str(e)


def display_cross_paper_analysis(output_data, pdf_names, findings_dict, similarity_matrix):
    print("\n" + "=" * 140)
    print("CROSS-PAPER SIMILARITY ANALYSIS & KEY FINDINGS")
    print("=" * 140)
    
    print(f"\nTotal Papers Analyzed: {output_data['total_papers']}\n")
    
    for idx, (pdf_name, findings) in enumerate(zip(pdf_names, findings_dict.values()), 1):
        print(f"{idx}. {pdf_name}")
        if findings:
            print(f"   Key Findings: {', '.join(findings)}")
        else:
            print(f"   Key Findings: None found from predefined phrases")
    
    print("\n" + "-" * 140)
    print("SIMILARITY MATRIX - TABLE FORMAT")
    print("-" * 140)
    
    pairs = []
    for i in range(len(pdf_names)):
        for j in range(i + 1, len(pdf_names)):
            score = similarity_matrix[i][j]
            pairs.append((pdf_names[i], pdf_names[j], score))
    
    pairs_sorted = sorted(pairs, key=lambda x: x[2], reverse=True)
    
    header = "| # | Paper 1                                        | Paper 2                                        | Score    | % Similarity|"
    print(header)
    print("|---|------------------------------------------------|------------------------------------------------|----------|-------------|")
    
    for idx, (paper1, paper2, score) in enumerate(pairs_sorted, 1):
        percentage = score * 100
        paper1_short = paper1[:43] + "..." if len(paper1) > 43 else paper1
        paper2_short = paper2[:43] + "..." if len(paper2) > 43 else paper2
        
        print(f"| {idx} | {paper1_short:<44} | {paper2_short:<44} | {score:.6f} | {percentage:>10.2f}% |")
    
    print("-" * 140)
    print("\n" + "=" * 140 + "\n")
