import os
from google import genai
from google.genai.types import HttpOptions

client = genai.Client(
    vertexai=True,
    project=os.getenv("GCP_PROJECT"),
    location=os.getenv("GCP_LOCATION", "us-central1"),
    http_options=HttpOptions(api_version="v1"),
)

response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    contents="Reply in one sentence: say hello like a caring wellness companion."
)

print("TEXT:", getattr(response, "text", None))
print("FULL RESPONSE:", response)
