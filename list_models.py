import os
import requests

API_KEY = os.getenv("GOOGLE_API_KEY")

url = "https://generativelanguage.googleapis.com/v1beta/models"

response = requests.get(url, params={"key": API_KEY})
response.raise_for_status()

models = response.json()["models"]

for m in models:
    print(m["name"])
