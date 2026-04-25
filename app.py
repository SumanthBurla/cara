import os
from flask import Flask, render_template, request, session, redirect, url_for
from ai import chat_with_gemini

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

@app.route("/", methods=["GET"])
def home():
    if "chat_history" not in session:
        session["chat_history"] = [
            {
                "role": "model",
                "content": "Hi, I’m here with you today. How are you feeling right now?"
            }
        ]
    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message", "").strip()
    history = session.get("chat_history", [])

    if not user_input:
        return render_template("index.html", chat_history=history)

    history.append({"role": "user", "content": user_input})

    ai_reply = chat_with_gemini(history)

    history.append({"role": "model", "content": ai_reply})

    session["chat_history"] = history[-12:]
    session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/reset", methods=["POST"])
def reset():
    session.pop("chat_history", None)
    return redirect(url_for("home"))

@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
