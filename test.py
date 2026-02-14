import os
import json
from google import genai
from google.genai import types

# Create Gemini client
# We explicitly set api_version='v1' to avoid v1beta issues
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options=types.HttpOptions(api_version='v1')
)

def main():
    # --- STEP 1: AUTO-FIND AVAILABLE MODELS ---
    print("Checking for available models...")
    available_models = []
    try:
        for m in client.models.list():
            # Check if model supports text generation
            if 'generateContent' in m.supported_actions:
                available_models.append(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
        return

    if not available_models:
        print("No compatible models found. Please check your API key.")
        return

    # --- STEP 2: SELECT MODEL ---
    # Use 'gemini-1.5-flash' if available, otherwise pick the first working one
    target_model = "gemini-1.5-flash" if "gemini-1.5-flash" in available_models else available_models[0]
    print(f"Using model: {target_model}")

    # --- STEP 3: LOAD DATA AND GENERATE ---
    with open("common_findings.json", "r", encoding="utf-8") as f:
        findings = json.load(f)

    with open("papers_dataset.json", "r", encoding="utf-8") as f:
        paper_metadata = json.load(f)

    prompt = f"""
    TASK: Write a formal research paper draft.
    TERM FREQUENCIES: {json.dumps(findings)}
    CITED PAPERS: {json.dumps(paper_metadata)}

    SECTIONS: Abstract, Methodology, Results, and References (APA 7th Edition).
    """

    try:
        response = client.models.generate_content(
            model=target_model,
            contents=prompt
        )
        with open("research_paper_formate.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Success! Draft saved to 'research_paper_formate.txt'.")
    except Exception as e:
        print(f"Generation failed: {e}")

if __name__ == "__main__":
    main()