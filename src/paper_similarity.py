import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def load_extracted_texts(input_folder=os.path.join('outputs', 'extracted_text')):
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


def calculate_tfidf_similarity(texts):
    if len(texts) < 2:
        print("Need at least 2 papers to calculate similarity")
        return None, None, None
    
    paper_names = list(texts.keys())
    paper_texts = list(texts.values())
    
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(paper_texts)
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return similarity_matrix, paper_names, tfidf_matrix


def display_similarity_scores(similarity_matrix, paper_names):
    num_papers = len(paper_names)
    
    print("\n" + "=" * 140)
    print("COSINE SIMILARITY SCORES BETWEEN EVERY PAIR OF PAPERS")
    print("=" * 140)
    print(f"Total Papers: {num_papers}\n")
    
    pairs = []
    for i in range(num_papers):
        for j in range(i + 1, num_papers):
            similarity = similarity_matrix[i][j]
            pairs.append((paper_names[i], paper_names[j], similarity))
    
    pairs_sorted = sorted(pairs, key=lambda x: x[2], reverse=True)
    
    header = "Paper 1".ljust(50) + " || " + "Paper 2".ljust(50) + " || " + "Similarity Score"
    print(header)
    print("-" * 140)
    
    for idx, (paper1, paper2, score) in enumerate(pairs_sorted, 1):
        percentage = score * 100
        paper1_short = paper1[:47] + "..." if len(paper1) > 50 else paper1.ljust(50)
        paper2_short = paper2[:47] + "..." if len(paper2) > 50 else paper2.ljust(50)
        similarity_str = f"{score:.4f} ({percentage:.2f}%)"
        print(f"{paper1_short} || {paper2_short} || {similarity_str}")
    
    print("-" * 140)
    print()


def save_similarity_report(similarity_matrix, paper_names, output_folder=os.path.join('outputs', 'similarity_reports')):
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    output_file = os.path.join(output_folder, 'similarity_scores.txt')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("COSINE SIMILARITY SCORES BETWEEN EVERY PAIR OF PAPERS\n")
            f.write("=" * 140 + "\n")
            f.write(f"Total Papers: {len(paper_names)}\n\n")
            
            num_papers = len(paper_names)
            
            pairs = []
            for i in range(num_papers):
                for j in range(i + 1, num_papers):
                    similarity = similarity_matrix[i][j]
                    pairs.append((paper_names[i], paper_names[j], similarity))
            
            pairs_sorted = sorted(pairs, key=lambda x: x[2], reverse=True)
            
            header = "Paper 1".ljust(50) + " || " + "Paper 2".ljust(50) + " || " + "Similarity Score"
            f.write(header + "\n")
            f.write("-" * 140 + "\n")
            
            for idx, (paper1, paper2, score) in enumerate(pairs_sorted, 1):
                percentage = score * 100
                paper1_short = paper1[:47] + "..." if len(paper1) > 50 else paper1.ljust(50)
                paper2_short = paper2[:47] + "..." if len(paper2) > 50 else paper2.ljust(50)
                similarity_str = f"{score:.4f} ({percentage:.2f}%)"
                f.write(f"{paper1_short} || {paper2_short} || {similarity_str}\n")
            
            f.write("-" * 140 + "\n")
        
        return True, output_file
    except Exception as e:
        return False, str(e)


def analyze_paper_similarity(input_folder=os.path.join('outputs', 'extracted_text')):
    print("\nLoading extracted texts...")
    texts = load_extracted_texts(input_folder)
    
    if len(texts) < 2:
        print("Not enough papers to calculate similarity. Need at least 2 papers.")
        return
    
    print(f"Loaded {len(texts)} papers")
    print("Calculating TF-IDF and Cosine Similarity...")
    
    similarity_matrix, paper_names, tfidf_matrix = calculate_tfidf_similarity(texts)
    
    display_similarity_scores(similarity_matrix, paper_names)
    
    success, output_path = save_similarity_report(similarity_matrix, paper_names)
    if success:
        print(f"\nSimilarity report saved to: {output_path}")
    else:
        print(f"\nError saving report: {output_path}")
