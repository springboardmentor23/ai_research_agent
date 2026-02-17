import os
import PyPDF2
from pathlib import Path


def ensure_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


# ==================================================
# EXTRACT TEXT FROM SINGLE PDF
# ==================================================

def extract_text_from_pdf(pdf_path):

    full_text = ""

    try:
        with open(pdf_path, "rb") as f:

            try:
                reader = PyPDF2.PdfReader(f)
            except Exception:
                print(f"❌ Corrupted PDF: {os.path.basename(pdf_path)}")
                return None

            for page in reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                except:
                    continue

    except Exception:
        print(f"❌ File open error: {os.path.basename(pdf_path)}")
        return None

    return full_text


# ==================================================
# MAIN EXTRACTION
# ==================================================

def extract_all_pdfs_text(
    pdf_folder="pdfs",
    output_folder="extracted_texts"
):

    ensure_folder(output_folder)

    # 🚨 CLEAN WRONG FILE TYPES (IMPORTANT FIX)
    for f in os.listdir(output_folder):
        if not f.endswith(".txt"):
            try:
                os.remove(os.path.join(output_folder, f))
            except:
                pass

    extracted = 0
    skipped = 0

    for pdf_file in os.listdir(pdf_folder):

        # STRICT PDF CHECK
        if not pdf_file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_folder, pdf_file)

        print(f"📄 Extracting: {pdf_file}")

        full_text = extract_text_from_pdf(pdf_path)

        # SKIP EMPTY OR BROKEN PDFs
        if not full_text or len(full_text.strip()) < 100:
            print(f"⚠️ Skipped broken/empty PDF: {pdf_file}")
            skipped += 1
            continue

        # SAFELY FORCE TXT OUTPUT
        txt_name = os.path.splitext(pdf_file)[0] + ".txt"
        output_path = os.path.join(output_folder, txt_name)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_text)
        except Exception:
            print(f"❌ Failed writing text for {pdf_file}")
            skipped += 1
            continue

        extracted += 1

    print("\n==============================")
    print(f"✅ Extracted PDFs: {extracted}")
    print(f"⚠️ Skipped PDFs: {skipped}")
    print("==============================")
