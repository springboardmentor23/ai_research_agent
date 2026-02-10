import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# Load API key
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ API KEY NOT FOUND in .env file")
    exit()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================
# Folders
# =========================

INPUT_FOLDER = "extracted_texts_json"
OUTPUT_FOLDER = "ai_results"

Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# =========================
# TOKEN ESTIMATOR
# =========================

def estimate_tokens(text):
    return int(len(text) / 4)

# =========================
# PROMPT BUILDER
# =========================

def build_prompt(text):
    return f"""
You are a research assistant.

From the following research paper text, extract:

1. Datasets used
2. Methods / Approaches
3. Algorithms
4. Key Findings

Return ONLY valid JSON in this format:

{{
  "datasets": [],
  "methods": [],
  "algorithms": [],
  "key_findings": []
}}

Paper Text:
{text}
"""

# =========================
# AI PROCESSING
# =========================

def analyze_with_ai(text):

    try:
        tokens = estimate_tokens(text)
        print(f"Estimated Tokens: {tokens}")

        # limit input size
        if tokens > 12000:
            print("Truncating large text...")
            text = text[:48000]

        response = model.generate_content(
            build_prompt(text)
        )

        result = response.text.strip()

        # remove markdown if present
        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        return json.loads(result)

    except Exception as e:
        print("❌ AI ERROR:", e)
        return None

# =========================
# PROCESS ALL PAPERS
# =========================

def process_all_texts_with_ai():

    print("\n🤖 Starting AI Extraction...\n")

    success = 0
    failed = 0

    for file in os.listdir(INPUT_FOLDER):

        if not file.endswith(".json"):
            continue

        input_path = os.path.join(INPUT_FOLDER, file)
        print(f"Processing: {file}")

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            text = data.get("full_text", "")

            if len(text.strip()) < 100:
                print("Text too short, skipping")
                failed += 1
                continue

            ai_result = analyze_with_ai(text)

            if ai_result is None:
                failed += 1
                continue

            output_path = os.path.join(OUTPUT_FOLDER, file)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(ai_result, f, indent=4)

            print("Saved AI result\n")
            success += 1

        except Exception as e:
            print("File Error:", e)
            failed += 1

    print("\n========== SUMMARY ==========")
    print("Success:", success)
    print("Failed:", failed)
    print("=============================\n")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    process_all_texts_with_ai()
