import os
from google import genai
from google.genai.types import HttpOptions

PROJECT_ID = os.getenv("GCP_PROJECT")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
MODEL_ID = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1"),
)

SYSTEM_INSTRUCTION = """
You are MindHello, a warm and emotionally aware wellness companion in a web app.

Rules:
- Be natural, conversational, and human
- Keep responses short to medium length
- Respond with empathy first
- Ask at most one follow-up question when useful
- Do not diagnose
- Do not claim to be a doctor or therapist
- If the user sounds in crisis, encourage them to reach out to a trusted person or professional support resource
""".strip()

def extract_text_from_response(response):
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    try:
        candidates = getattr(response, "candidates", None)
        if candidates and len(candidates) > 0:
            content = getattr(candidates[0], "content", None)
            if content and getattr(content, "parts", None):
                parts = content.parts
                texts = []
                for part in parts:
                    part_text = getattr(part, "text", None)
                    if part_text:
                        texts.append(part_text)
                if texts:
                    return "\n".join(texts).strip()
    except Exception as inner_error:
        print("Error while extracting Gemini text:", inner_error)

    return ""

def chat_with_gemini(history):
    if not PROJECT_ID:
        return "GCP_PROJECT is missing. Please set your project id first."

    try:
        contents = [
            {
                "role": "user",
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            }
        ]

        for msg in history:
            role = "model" if msg["role"] == "model" else "user"
            text = (msg.get("content") or "").strip()
            if text:
                contents.append({
                    "role": role,
                    "parts": [{"text": text}]
                })

        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
        )

        print("Gemini raw response:", response)

        text = extract_text_from_response(response)

        if not text:
            return "Gemini returned an empty response. Check terminal logs for details."

        return text

    except Exception as e:
        print("Gemini API error:", repr(e))
        return f"Gemini error: {str(e)}"
