import os
import nltk

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

KEY_PHRASES = [
    "we propose",
    "we introduce",
    "our approach",
    "our method",
    "we demonstrate",
    "outperforms",
    "achieves state-of-the-art"
]

input_folder = "extracted_text"
output_folder = "key_sentences"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".txt"):
        with open(os.path.join(input_folder, file), "r", encoding="utf-8") as f:
            text = f.read().lower()

        sentences = sent_tokenize(text)
        key_sentences = []

        for sentence in sentences:
            for phrase in KEY_PHRASES:
                if phrase in sentence:
                    key_sentences.append(sentence)
                    break

        with open(os.path.join(output_folder, file), "w", encoding="utf-8") as f:
            for s in key_sentences:
                f.write(s + "\n\n")

print("✅ Key contribution sentences extracted")
