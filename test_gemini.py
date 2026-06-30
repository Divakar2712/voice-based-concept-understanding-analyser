import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("API Key Found:", API_KEY is not None)

genai.configure(api_key=API_KEY)

print("\nAvailable Models:\n")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)

print("\nTesting Gemini...\n")

model = genai.GenerativeModel("gemini-2.5-flash-lite")

response = model.generate_content("Say Hello")

print(response.text)