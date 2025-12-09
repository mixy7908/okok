import re
import json
import requests
import openai
from flask import Flask, request

# ---------------------------------------------------
#   CONFIG
# ---------------------------------------------------
TELEGRAM_BOT_TOKEN = "7676279831:AAG7x8SJ7tZv6jF-TMTAy6tfdpenAUdMNR4"
OPENAI_KEY = "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"

openai.api_key = OPENAI_KEY

# Telegram API Base URL
TG_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Flask App
app = Flask(__name__)

BLOCK_WORDS = ["smm", "panel", "s.m.m", "pannel", "panal"]


def clean_text(text):
    t = text.lower()
    for w in BLOCK_WORDS:
        t = re.sub(rf"\b{w}\b", "Mixy Grow", t)
    return t


def get_ai_reply(user_msg):
    msg = clean_text(user_msg)

    # Order issue replies
    if any(x in msg for x in ["order", "not complete", "complete nahi"]):
        return "Sir 2-3 Ghante Wait Karo Aapka Order Complete Ho Jaye Ga 🙏"

    # Payment issue replies
    if "payment" in msg or "pay" in msg or "paisa" in msg:
        return "Payment Related Help Ke Liye Is Username Pe Message Kare: @ZoZyOx"

    # AI Response (new OpenAI format)
    prompt = f"""
    Tum MixyGrow.Shop ke support agent ho.
    Tum kabhi bhi SMM panel ka naam nahi loge.
    Agar user uska naam le to tum us word ko 'Mixy Grow' bana ke hi reply doge.

    User Message: {msg}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]


def send_message(chat_id, text):
    url = f"{TG_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)


# ---------------------------------------------------
#   TELEGRAM WEBHOOK
# ---------------------------------------------------
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"].get("text", "")

        reply = get_ai_reply(user_msg)
        send_message(chat_id, reply)

    return {"ok": True}


# ---------------------------------------------------
#   LOCAL TEST
# ---------------------------------------------------
if __name__ == "__main__":
    print("Bot running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
