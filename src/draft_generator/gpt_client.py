import os
import requests
import time

MODEL = "gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1"


def generate_with_gemini(prompt: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set in environment")

    url = f"{BASE_URL}/models/{MODEL}:generateContent"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    max_retries = 5

    for attempt in range(max_retries):
        try:
            time.sleep(2)

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=180
            )

            if response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            result = response.json()

            return result["candidates"][0]["content"]["parts"][0]["text"]

        except requests.exceptions.RequestException as e:
            print("Status Code:", response.status_code if 'response' in locals() else "No response")
            if 'response' in locals():
                print("Response Text:", response.text)

            if attempt == max_retries - 1:
                raise RuntimeError(f"Gemini API failed after retries: {e}")

            time.sleep(2 ** attempt)

    raise RuntimeError("Failed to generate response from Gemini.")
