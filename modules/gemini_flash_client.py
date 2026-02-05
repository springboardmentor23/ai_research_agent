import requests
import json
import os

GEMINI_FLASH_URL = (
    "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
)

def generate_with_gemini_flash(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_FLASH_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Gemini API Error {response.status_code}: {response.text}"
        )

    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]
