# bot/main.py
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import telebot

# ==============================
# Настройки бота
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://odwillio0702.github.io/personalinfo/")

bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# Flask app
# ==============================
app = Flask(__name__)

# ==============================
# /start handler для бота
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton(
            "Открыть профиль",
            web_app=telebot.types.WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(message.chat.id, "клац👇", reply_markup=markup)

# ==============================
# WebApp data handler
# ==============================
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        print("WEBAPP DATA:", data)

        text = (
            f"👤 Открытие профиля\n\n"
            f"ID: {data.get('id')}\n"
            f"Имя: {data.get('first_name','')}\n"
            f"Username: @{data.get('username','')}\n"
            f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )

        bot.send_message(CHANNEL_ID, text)

    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# Flask route для проверки сервера
# ==============================
@app.route("/")
def home():
    return "Bot server is running!"

# ==============================
# Flask route для TeleBot webhook (если нужно)
# ==============================
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return jsonify({"ok": True})

# ==============================
# Run TeleBot polling в фоне
# ==============================
import threading

def run_telebot():
    bot.infinity_polling()

threading.Thread(target=run_telebot).start()

# ==============================
# Запуск Flask (для локалки, на Railway Gunicorn)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))