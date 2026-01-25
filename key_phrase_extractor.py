import os
import re
from pathlib import Path
from collections import Counter


KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art"
]


def clean_text(text):
    text = re.sub(r'---\s*Page\s*\d+\s*---', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\-\(\)]', '', text)
    return text.strip().lower()


def extract_key_findings_from_phrases(text, key_phrases=KEY_PHRASES, context_size=100):
    text_lower = text.lower()
    findings = {}
    
    for phrase in key_phrases:
        matches = []
        pattern = re.escape(phrase)
        for match in re.finditer(pattern, text_lower):
            start = max(0, match.start() - context_size)
            end = min(len(text_lower), match.end() + context_size)
            context = text_lower[start:end].replace('\n', ' ').strip()
            matches.append(context)
        
        if matches:
            findings[phrase] = matches
    
    return findings


def extract_frequency_keywords(text, top_n=30):
    text_lower = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text_lower)
    stop_words = {'the', 'and', 'for', 'are', 'that', 'with', 'from', 'this', 'which', 'have', 'been', 'can', 'will', 'not', 'were', 'has', 'was', 'all', 'their', 'more', 'when', 'used', 'would', 'into', 'being', 'such', 'each', 'or', 'also', 'other', 'where', 'some', 'than', 'them', 'its', 'our', 'we', 'as', 'to', 'in', 'is', 'by', 'on', 'at', 'an', 'a', 'of', 'it'}
    
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    word_freq = Counter(filtered_words)
    return word_freq.most_common(top_n)


def extract_noun_phrases(text, top_n=20):
    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
    except:
        return extract_frequency_keywords(text, top_n)
    
    try:
        doc = nlp(text[:1000000])
        phrases = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3 and len(chunk.text) > 3:
                phrases.append(chunk.text.lower())
        
        phrase_freq = Counter(phrases)
        return phrase_freq.most_common(top_n)
    except:
        return extract_frequency_keywords(text, top_n)


def extract_key_phrases_from_text(text_content, top_n=30):
    cleaned_text = clean_text(text_content)
    
    frequency_keywords = extract_frequency_keywords(cleaned_text, top_n)
    
    return {
        'frequency_keywords': frequency_keywords,
        'total_words': len(cleaned_text.split())
    }


def process_all_extracted_texts(input_folder='extracted_text', output_folder='key_phrases'):
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    results = []
    
    if not os.path.exists(input_folder):
        return results
    
    for text_file in os.listdir(input_folder):
        if text_file.endswith('.txt'):
            text_path = os.path.join(input_folder, text_file)
            output_filename = text_file.replace('.txt', '_keyphrases.txt')
            
            print(f"Extracting key phrases from {text_file}...")
            
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                
                phrases_data = extract_key_phrases_from_text(text_content)
                
                output_path = os.path.join(output_folder, output_filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"Key Phrases from: {text_file}\n")
                    f.write(f"Total Words: {phrases_data['total_words']}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    f.write("TOP KEYWORDS (Frequency-Based):\n")
                    f.write("-" * 80 + "\n")
                    for i, (phrase, freq) in enumerate(phrases_data['frequency_keywords'], 1):
                        f.write(f"{i:2d}. {phrase:40s} (frequency: {freq})\n")
                
                file_size = os.path.getsize(output_path) / 1024
                results.append({'text_file': text_file, 'output': output_filename, 'status': 'Success', 'size_kb': file_size})
                print(f"  Key phrases saved to {output_filename} ({file_size:.2f} KB)")
                
            except Exception as e:
                results.append({'text_file': text_file, 'output': output_filename, 'status': 'Failed', 'error': str(e)})
                print(f"  Failed: {str(e)}")
    
    return results
