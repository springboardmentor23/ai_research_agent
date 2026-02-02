import os
import requests

API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL = "models/gemini-flash-latest"

url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Explain Artificial Intelligence in one sentence."}
            ]
        }
    ]
}

response = requests.post(
    url,
    params={"key": API_KEY},
    json=payload,
    timeout=60
)

response.raise_for_status()

result = response.json()
print(result["candidates"][0]["content"]["parts"][0]["text"])
