# import os
# import fitz  # PyMuPDF


# def extract_text_from_pdf(pdf_path):
#     text = ""
#     document = fitz.open(pdf_path)

#     for page in document:
#         text += page.get_text()

#     document.close()
#     return text


# def extract_text_from_all_pdfs(pdf_folder, output_folder):

#     os.makedirs(output_folder, exist_ok=True)

#     for filename in os.listdir(pdf_folder):
#         if filename.endswith(".pdf"):
#             pdf_path = os.path.join(pdf_folder, filename)
#             text = extract_text_from_pdf(pdf_path)

#             text_filename = filename.replace(".pdf", ".txt")
#             text_path = os.path.join(output_folder, text_filename)

#             with open(text_path, "w", encoding="utf-8") as file:
#                 file.write(text)

#             print(f"Text extracted: {text_filename}")



import os
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path, output_folder=None):
    """
    Extracts text from a PDF.
    If output_folder is provided, saves extracted text into a .txt file.
    """

    text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:
        print(f"❌ PDF extraction failed for {pdf_path}: {e}")
        return ""

    # Save if output folder given
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

        filename = os.path.basename(pdf_path)
        text_filename = filename.replace(".pdf", ".txt")
        text_path = os.path.join(output_folder, text_filename)

        with open(text_path, "w", encoding="utf-8") as file:
            file.write(text)

        print(f"✅ Text extracted: {text_filename}")

    return text


def extract_text_from_all_pdfs(pdf_folder, output_folder):
    """
    Extracts text from all PDFs in pdf_folder and saves them into output_folder.
    """

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)

            # ✅ now this works even if function called with 2 args
            extract_text_from_pdf(pdf_path, output_folder)
