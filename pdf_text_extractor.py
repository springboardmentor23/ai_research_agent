import os
import PyPDF2
from pathlib import Path


def ensure_folder_exists(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    text_content = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text_content.append(f"--- Page {page_num + 1} ---\n{page_text}\n")
        return ''.join(text_content)
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {str(e)}"


def save_extracted_text(text_content, output_filename, output_folder='extracted_text'):
    ensure_folder_exists(output_folder)
    output_path = os.path.join(output_folder, output_filename)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        return True, output_path
    except Exception as e:
        return False, str(e)


def extract_all_pdfs_text(pdf_folder='pdf', output_folder='extracted_text'):
    ensure_folder_exists(output_folder)
    results = []
    
    if not os.path.exists(pdf_folder):
        return results
    
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            output_filename = pdf_file.replace('.pdf', '.txt')
            
            print(f"Extracting text from {pdf_file}...")
            text_content = extract_text_from_pdf(pdf_path)
            
            success, message = save_extracted_text(text_content, output_filename, output_folder)
            
            if success:
                file_size = os.path.getsize(message) / 1024
                results.append({'pdf': pdf_file, 'text_file': output_filename, 'status': 'Success', 'size_kb': file_size})
                print(f"  Extracted to {output_filename} ({file_size:.2f} KB)")
            else:
                results.append({'pdf': pdf_file, 'text_file': output_filename, 'status': 'Failed', 'error': message})
                print(f"  Failed: {message}")
    
    return results
