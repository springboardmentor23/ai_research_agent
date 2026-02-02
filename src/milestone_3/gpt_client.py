import os
import requests

MODEL = "models/gemini-flash-latest"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

def generate_with_gemini(prompt: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set in environment")

    url = f"{BASE_URL}/{MODEL}:generateContent"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(
        url,
        params={"key": api_key},
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]
