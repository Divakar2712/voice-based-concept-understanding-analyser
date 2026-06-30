import os
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------------------------
# Load Environment Variables
# ---------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-2.5-flash-lite"


# ---------------------------------------------
# Generate AI Feedback
# ---------------------------------------------

def generate_feedback(reference_text, student_text, similarity_score):

    prompt = f"""
You are an expert teacher.

Evaluate the student's conceptual understanding.

Reference Answer:
{reference_text}

Student Answer:
{student_text}

Semantic Similarity Score:
{similarity_score:.2f}%

Provide the answer in exactly this format.

Overall Understanding:
(Excellent / Good / Moderate / Poor)

Strengths:
- Point 1
- Point 2

Weaknesses:
- Point 1
- Point 2

Suggestions:
- Point 1
- Point 2

Keep the feedback concise and encouraging.
"""

    try:

        print("=" * 60)
        print("Gemini Feedback Module Loaded")
        print("Using Model :", MODEL_NAME)
        print("=" * 60)

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No feedback generated."

    except Exception as e:

        available_models = []

        try:
            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception:
            pass

        error_message = f"""
❌ Gemini Error

Model Used:
{MODEL_NAME}

Actual Error:
{str(e)}

Available Models:
"""

        if available_models:
            error_message += "\n".join(available_models)
        else:
            error_message += "\nUnable to fetch model list."

        return error_message