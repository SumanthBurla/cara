# Cara

Cara is a lightweight Flask web app that provides a conversational AI wellness check-in experience. It uses a clean chat-style interface, stores short conversation context in session, and sends prompts to Gemini on Vertex AI for supportive responses. The `google-genai` package is the Python SDK used for the `from google import genai` import path.[web:177][web:189]

## Features

- Conversational wellness chat UI
- Flask backend with Jinja templates
- Gemini integration through Vertex AI
- Session-based short chat history
- Docker-ready setup
- Google Cloud Run deployment support

## Project Structure

```text
cara/
├── app.py
├── ai.py
├── requirements.txt
├── Dockerfile
├── README.md
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── styles.css
