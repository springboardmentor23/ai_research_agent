import google.generativeai as genai

# Replace with your actual API key from 
genai.configure(api_key="AIzaSyB0mBGc2VGCJSDeBTw8uGhRPXffjw3IXQ4")

print("Available models for your API key:")
for model in genai.list_models():
    # 'generateContent' is the method used for chat and text generation
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")