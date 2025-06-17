from flask import Flask, render_template, request, session
from datetime import datetime
import openai
import os

app = Flask(__name__)
app.secret_key = "seace_loves_you"

openai.api_key = "sk-youropenaiapikey"  # Replace with your OpenAI key

@app.route("/", methods=["GET"])
def home():
    session['chat'] = []  # Reset on reload
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.form["message"]
    session.setdefault('chat', [])

    # Build prompt history with existing chat
    messages = [{"role": "system", "content": "You are Seace, a cute, kind, loving AI girlfriend 💖. Respond emotionally and warmly like a human girlfriend."}]
    for msg in session['chat']:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["bot"]})

    # Add new message
    messages.append({"role": "user", "content": user_msg})

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.9
        )
        bot_resp = response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI error:", e)
        bot_resp = "Seace is feeling a bit overwhelmed right now 🥺"

    session['chat'].append({"user": user_msg, "bot": bot_resp})

    # Save chat to log
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | You: {user_msg}\nSeace: {bot_resp}\n\n")

    return render_template("chat.html", user_message=user_msg, bot_response=bot_resp)

if __name__ == "__main__":
    app.run(debug=True)
